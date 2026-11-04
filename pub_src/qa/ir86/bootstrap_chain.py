"""Execute the complete published BASIC -> ASM86 -> IR86 -> target chain."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'qa/asm86'))
from bootstrap import basic_build
from dos_machine import DosMachine,assemble
W=ROOT/'workbench/ir86';Q=ROOT/'qa/ir86'
log=basic_build()
assert 'OK ASM86.COM' in log,log
assembler=(ROOT/'workbench/asm86/ASM86.COM').read_bytes()
selfbuild=assemble(assembler,(ROOT/'workbench/asm86/ASM86.ASM').read_bytes(),'SELF')
assert selfbuild.exitcode==0 and selfbuild.files['SELF.COM']==assembler,selfbuild.output
built=assemble(assembler,(W/'IR86.ASM').read_bytes(),'IR86')
assert built.exitcode==0,built.output
image=built.files['IR86.COM']
if (W/'IR32.COM').exists():
 assert image==(W/'IR32.COM').read_bytes(),'Standalone translator differs from final checkpoint'
(W/'IR86.COM').write_bytes(image)
translated=DosMachine({'PROBE.IR':(W/'HELLO.IR').read_bytes()},['PROBE']).run(image)
assert translated.exitcode==0,translated.output
program=assemble(assembler,translated.files['PROBE.ASM'],'PROBE')
assert program.exitcode==0,program.output
run=DosMachine().run(program.files['PROBE.COM'])
assert run.exitcode==0 and run.output==b'HI',run.output
text=f'PASS published BOOTASM.BAS builds ASM86.COM ({len(assembler)} bytes).\nPASS ASM86 self-assembly matches the BASIC-produced executable.\nPASS that ASM86 builds IR86.COM ({len(image)} bytes) directly.\nPASS IR86 emits ASM86-accepted assembly; the resulting COM displays HI and returns zero.\n'
(Q/'bootstrap-results.txt').write_text(text);print(text)
