"""Execute the complete published ladder without any outside executable encoder."""
from machine import *
import sys,json
sys.path.insert(0,str(ROOT/'qa/asm86'))
from bootstrap import basic_build
W=ROOT/'workbench/asm86a';Q=ROOT/'qa/asm86a'
log=basic_build();assert 'OK ASM86.COM' in log,log
asm=(ROOT/'workbench/asm86/ASM86.COM').read_bytes()
rebuilt=assemble(asm,(ROOT/'workbench/asm86/ASM86.ASM').read_bytes(),'SELF');assert rebuilt.exitcode==0 and rebuilt.files['SELF.COM']==asm
first=assemble(asm,(W/'ASMA0.ASM').read_bytes(),'ASMA0');assert first.exitcode==0,first.output
seed=first.files['ASMA0.COM'];assert seed==(W/'ASMA0.COM').read_bytes()
full=run_assembler(seed,(W/'ASM86A.ASM').read_bytes());assert full.exitcode==0,full.output
image=full.files['RESULT.COM'];assert image==(W/'ASM86A.COM').read_bytes()
for _ in range(2):
 same=run_assembler(image,(W/'ASM86A.ASM').read_bytes());assert same.exitcode==0 and same.files['RESULT.COM']==image
irbuild=run_assembler(image,(ROOT/'workbench/ir86/IR86.ASM').read_bytes());assert irbuild.exitcode==0
ir=irbuild.files['RESULT.COM'];assert ir==(ROOT/'workbench/ir86/IR86.COM').read_bytes()
rilltext=DosMachine({'RILL.IR':(ROOT/'workbench/rill/RILL.IR').read_bytes()},['RILL']).run(ir);assert rilltext.exitcode==0
rillbuild=run_assembler(image,rilltext.files['RILL.ASM']);assert rillbuild.exitcode==0
rill=rillbuild.files['RESULT.COM'];assert rill==(ROOT/'workbench/rill/RILL.COM').read_bytes()
compiled=DosMachine({'SOURCE.RIL':(ROOT/'workbench/rill/HELLO.RIL').read_bytes()}).run(rill);assert compiled.exitcode==0
translated=DosMachine({'HELLO.IR':compiled.files['RESULT.IR']},['HELLO']).run(ir);assert translated.exitcode==0
program=run_assembler(image,translated.files['HELLO.ASM']);assert program.exitcode==0
child=DosMachine().run(program.files['RESULT.COM']);assert child.exitcode==0 and child.output==b'HI'
lines=[f'PASS canonical BOOTASM.BAS builds ASM86; native self-assembly matches ({len(asm)} bytes)',f'PASS unchanged ASM86 directly builds ASMA0 ({len(seed)} bytes)',f'PASS ASMA0 builds ASM86A; two ASM86A self-builds match ({len(image)} bytes)',f'PASS ASM86A builds the published IR86 without changing any byte ({len(ir)} bytes)',f'PASS IR86 and ASM86A build the IR-written RILL compiler without changing any byte ({len(rill)} bytes)','PASS RILL -> IR86 -> ASM86A -> COM displays HI and returns zero']
(Q/'bootstrap-results.txt').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
