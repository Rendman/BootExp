"""Build the reader's memory diagnostics and prove they reject broken helpers."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from asm86_memory_checks import diagnostic, prepare, replace_once
from machine import AssemblerMachine, run_assembler
from unicorn.x86_const import UC_X86_REG_AX, UC_X86_REG_BX, UC_X86_REG_AH

WORK = ROOT / 'workbench/asm86'
QA = ROOT / 'qa/asm86'
SEED = (WORK / 'ASMA0.COM').read_bytes()
INPUT = b'MOV DL,41H\r\nMOV AH,2\r\nINT 21H\r\nMOV AX,4C00H\r\nINT 21H\r\n'


class ProbeMachine(AssemblerMachine):
    """Add the DOS largest-free-block query used by the reader's A13 check."""
    def interrupt(self, cpu, number, data):
        if number == 0x21 and cpu.reg_read(UC_X86_REG_AH) == 0x48 and cpu.reg_read(UC_X86_REG_BX) == 0xffff:
            # Existing allocations are disjoint DOS blocks with one MCB paragraph.
            cursor = 0x3000
            largest = 0
            for segment, paragraphs in sorted(self.allocations.items()):
                largest = max(largest, segment - cursor - 1)
                cursor = segment + paragraphs + 1
            largest = max(largest, 0xa000 - cursor)
            cpu.reg_write(UC_X86_REG_AX, 8)
            cpu.reg_write(UC_X86_REG_BX, largest)
            self.carry(True)
            return
        return super().interrupt(cpu, number, data)


def build(source):
    result = run_assembler(SEED, source)
    assert result.exitcode == 0, result.output
    return result.files['RESULT.COM']


def execute(image):
    return ProbeMachine({'SOURCE.ASM': INPUT, 'RESULT.COM': b'OLD RESULT'}).run(image, limit=100_000_000)


def validate_printed_edits(number, source):
    from assembly_edits import patch
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location('label_steps', ROOT / 'qa/asm1/validate_steps.py')
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    printed, changes = patch(source.splitlines(), diagnostic(number, source).splitlines())
    # Follow labels and context with extra comments/blank lines, not edit indices.
    stage = {'page': f'M{number}', 'changes': changes}
    text = '## Enter the source\n\n' + printed + '## Build\n'
    actual = module.apply_label_edits(['; reader note', ''] + source.splitlines(), stage, text)
    assert actual == module.code(diagnostic(number, source).splitlines())


def main():
    prepare()
    facts = {}
    mutation_count = 0
    for number in (13, 14, 15):
        source = (WORK / f'A{number}.ASM').read_text()
        validate_printed_edits(number, source)
        test = diagnostic(number, source)
        image = build(test)
        assert len(image) + 0x100 < 0x4000, 'diagnostic overlaps the seed line buffer'
        result = execute(image)
        assert result.exitcode == 0, result.output
        assert not result.allocations and not result.handles
        assert result.files['RESULT.COM'] == bytes.fromhex('B241B402CD21B8004CCD21')
        assert b'PASS\r\nOK RESULT.COM 00011 bytes\r\n' in result.output
        (WORK / f'M{number}.COM').write_bytes(image)
        facts[str(number)] = {'binary_bytes': len(image), 'output': result.output.decode('ascii')}
        print(f'PASS M{number}: {len(image)} bytes; labelled edits reconstruct; diagnostic and ordinary assembly pass', flush=True)
        if number == 13:
            for count in range(1, 9):
                forced = replace_once(test, 'PROBELIMIT:\nDW 0', f'PROBELIMIT:\nDW {count}')
                failed = execute(build(forced))
                assert failed.exitcode == 1 and failed.output == b'MEMORY RELEASE PASS\r\nERROR 00000 CODE 7\r\n', (count, failed.output)
                assert failed.files['RESULT.COM'] == b'OLD RESULT' and not failed.allocations and not failed.handles
            mutations = [
                ('bucket clear skips last word', 'MOV CX,4096\nMOV AX,0\nMEMCLEAR:', 'MOV CX,4095\nMOV AX,0\nMEMCLEAR:'),
                ('free skips allocated blocks', 'MOV BP,[MEMCOUNT]', 'MOV BP,0'),
                ('DOS free omitted', 'MOV AH,49H\nINT 21H\nJAE MEMFREEOK', 'MOV AX,0\nCMP AX,0\nJAE MEMFREEOK'),
            ]
        elif number == 14:
            mutations = [
                ('one-based ID error', 'SYMPTR:\nDEC AX', 'SYMPTR:\nINC AX'),
                ('wrong page stride', 'SUB AX,1024\nADD DX,2', 'SUB AX,1024\nADD DX,0'),
                ('wrong record stride', 'ADD AX,CX\nMOV BX,AX', 'ADD AX,AX\nMOV BX,AX'),
                ('incorrect saved offset', 'MOV [RECORDPTR],BX', 'MOV [RECORDPTR],AX\nINC AX\nMOV [RECORDPTR],AX'),
            ]
        else:
            mutations = [
                ('record not cleared', 'MOV CX,40\nMOV AL,0\nDEFINITIONCLEAR:', 'MOV CX,1\nMOV AL,0\nDEFINITIONCLEAR:'),
                ('neighbor overwritten', 'MOV CX,40\nMOV AL,0\nDEFINITIONCLEAR:', 'MOV CX,41\nMOV AL,0\nDEFINITIONCLEAR:'),
                ('wrong link', 'MOV AX,[HEADID]', 'MOV AX,0'),
                ('wrong kind', 'MOV AX,[DEFTYPE]', 'MOV AX,0'),
                ('wrong bucket', 'MOV BX,[BUCKET]', 'MOV BX,0'),
                ('one-based record error', 'SYMPTR:\nDEC AX', 'SYMPTR:\nINC AX'),
            ]
        for name, before, after in mutations:
            mutant = build(replace_once(test, before, after))
            rejected = execute(mutant)
            assert rejected.exitcode == 1 and b'MEMORY TEST FAILED\r\n' in rejected.output, (number, name, rejected.output)
            if name in ('free skips allocated blocks', 'DOS free omitted'):
                # This fault is observed after the ordinary output was committed.
                # The process must report failure even though the bytes are valid.
                assert rejected.files['RESULT.COM'] == bytes.fromhex('B241B402CD21B8004CCD21')
                assert rejected.allocations
            else:
                assert rejected.files['RESULT.COM'] == b'OLD RESULT'
                assert not rejected.allocations
            print(f'PASS M{number} catches {name}', flush=True)
            mutation_count += 1
    (QA / 'memory-checks.json').write_text(json.dumps(facts, indent=2) + '\n')
    print(f'PASS reader memory diagnostics: all three positive cases, eight partial-allocation failures, {mutation_count} broken-helper cases and label reconstruction', flush=True)


if __name__ == '__main__':
    main()
