"""Verify the reader's diagnostic builds and output on private DOS 3.10 disks."""
from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import time

from test_memory_checks import ROOT, WORK, INPUT, build, replace_once


def command(args):
    return subprocess.run(args, check=True, capture_output=True)


def main():
    facts = json.loads((ROOT / 'qa/asm86/memory-checks.json').read_text())
    with tempfile.TemporaryDirectory(prefix='bootexp-memory-dos-') as temporary:
        folder = Path(temporary)
        boot, disk = folder / 'boot.img', folder / 'work.img'
        shutil.copyfile(ROOT / 'qa/dos-original.img', boot)
        command(['mformat', '-C', '-f', '360', '-i', str(disk), '::'])

        def copy(path, name, image=disk):
            command(['mcopy', '-o', '-i', str(image), str(path), '::' + name])

        def text(name, value):
            path = folder / name
            path.write_bytes(value.replace('\r\n', '\n').replace('\n', '\r\n').encode('ascii'))
            return path

        copy(WORK / 'ASMA0.COM', 'ASM1.COM')
        copy(WORK / 'CHECK.BAT', 'CHECK.BAT')
        copy(text('INPUT.ASM', INPUT.decode('ascii')), 'INPUT.ASM')
        commands = ['ECHO OFF', 'B:']
        for number in (13, 14, 15):
            copy(WORK / f'M{number}.ASM', f'M{number}.ASM')
            commands += [
                f'A:\\COMMAND /C CHECK ASM1 M{number}.ASM M{number}.COM >B{number}.TXT',
                f'A:\\COMMAND /C CHECK M{number} INPUT.ASM O{number}.COM >R{number}.TXT',
            ]
        forced = replace_once((WORK / 'M13.ASM').read_text(), 'PROBELIMIT:\nDW 0', 'PROBELIMIT:\nDW 2')
        copy(text('F13.ASM', forced), 'F13.ASM')
        commands += ['A:\\COMMAND /C CHECK ASM1 F13.ASM F13.COM >BF13.TXT',
                     'A:\\COMMAND /C CHECK F13 INPUT.ASM O13.COM >RF13.TXT',
                     'ECHO DONE >DONE.TXT']
        copy(text('CONFIG.SYS', 'FILES=30\n'), 'CONFIG.SYS', boot)
        copy(text('AUTOEXEC.BAT', '\n'.join(commands) + '\n'), 'AUTOEXEC.BAT', boot)
        with (folder / 'qemu.log').open('wb') as log:
            process = subprocess.Popen([
                'qemu-system-i386', '-machine', 'pc', '-m', '1M',
                '-drive', f'file={boot},format=raw,if=floppy,index=0',
                '-drive', f'file={disk},format=raw,if=floppy,index=1',
                '-boot', 'a', '-display', 'none', '-monitor', 'none',
                '-serial', 'none', '-no-reboot',
            ], stdout=log, stderr=log)
            try:
                deadline = time.monotonic() + 120
                while time.monotonic() < deadline:
                    if subprocess.run(['mdir', '-i', str(disk), '::DONE.TXT'], capture_output=True).returncode == 0:
                        break
                    if process.poll() is not None:
                        raise AssertionError((folder / 'qemu.log').read_text())
                    time.sleep(.5)
                else:
                    raise AssertionError('DOS memory checks did not finish within 120 seconds')
            finally:
                process.terminate()
                process.wait(timeout=10)

        def read(name):
            return command(['mtype', '-i', str(disk), '::' + name]).stdout

        def report(raw):
            # DOS 3.10's nested COMMAND echoes the batch's first ECHO OFF;
            # CHECK also surrounds its status with blank lines.
            return [line for line in raw.splitlines() if line and line != b'B>ECHO OFF']

        for number in (13, 14, 15):
            compiled = read(f'B{number}.TXT')
            assert f'OK M{number}.COM {facts[str(number)]["binary_bytes"]:05} bytes'.encode() in compiled and b'PASS' in compiled, compiled
            assert read(f'M{number}.COM') == (WORK / f'M{number}.COM').read_bytes()
            expected = facts[str(number)]['output'].replace('RESULT.COM', f'O{number}.COM').encode('ascii') + b'PASS\r\n'
            actual = read(f'R{number}.TXT')
            assert report(actual) == report(expected), (number, actual, expected)
            assert read(f'O{number}.COM') == bytes.fromhex('B241B402CD21B8004CCD21')
            print(f'PASS DOS 3.10 M{number}: ASM1-built bytes and diagnostic output match', flush=True)
        assert read('F13.COM') == build(forced)
        assert report(read('RF13.TXT')) == [b'MEMORY RELEASE PASS', b'ERROR 00000 CODE 7', b'FAIL']
        print('PASS DOS 3.10 F13: partial failure restores the largest free block and preserves the old result', flush=True)


if __name__ == '__main__':
    main()
