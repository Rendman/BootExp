"""Follow the canonical filenames with the project's native bootstrap tools."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'qa/toolchain'))
from common import run,ir
from machine import assemble,run_assembler
D=ROOT/'site/static/downloads/tools';W=ROOT/'workbench/toolchain'
source=lambda group,name:(D/group/name).read_bytes()
initial=(ROOT/'workbench/asm0/ASM86.COM').read_bytes()
seed=assemble(initial,source('asm1','ASM1.ASM'),'ASM1');assert seed.exitcode==0 and 'RESULT.COM' in seed.files
r=run_assembler(seed.files['RESULT.COM'],source('asm86','ASM86.ASM'));assert r.exitcode==0
assembler=r.files['RESULT.COM'];r=run_assembler(assembler,source('asm86','ASM86.ASM'));assert r.exitcode==0 and r.files['RESULT.COM']==assembler
_,image=ir(source('rillboot','RILLBOOT.IR'));assert image==(W/'RILLBOOT.COM').read_bytes()
r=run(image,source('rill','RILL.RIL'),'RIL');assert r.exitcode==0
_,seedcompiler=ir(r.files['RESULT.IR'])
# The seed uses smaller frames; the first compiler self-build establishes
# the sixty-four-slot convention used by the preserved R0 executable.
r=run(seedcompiler,source('rill','RILL.RIL'),'RIL');assert r.exitcode==0
_,compiler=ir(r.files['RESULT.IR']);assert compiler==(W/'RILL.COM').read_bytes()
for name,binary in [('IR86.RIL','IR86.COM'),('ASM86.RIL','ASM86A.COM')]:
 r=run(compiler,source('toolchain',name),'RIL');assert r.exitcode==0
 _,image=ir(r.files['RESULT.IR']);assert image==(W/binary).read_bytes()
# Both authored scalar-check forms must reject a deliberately wrong expected value.
seedcase=(ROOT/'workbench/rill0/R05.IR').read_text();a,b=seedcase.split('PROC PRINT',1)
assert 'LIT 1\nCNE\nRETURN' in a;a=a.replace('LIT 1\nCNE\nRETURN','LIT 0\nCNE\nRETURN')
_,image=ir((a+'PROC PRINT'+b).encode());assert run(image).exitcode==1
selfcase=(ROOT/'workbench/toolchain/RC05.RIL').read_text();assert 'return (letter(95))!=1;' in selfcase
r=run((W/'RILLBOOT.COM').read_bytes(),selfcase.replace('return (letter(95))!=1;','return (letter(95))!=0;'),'RIL');assert r.exitcode==0
_,image=ir(r.files['RESULT.IR']);assert run(image).exitcode==1
text='PASS canonical reader handoffs: ASM0 → ASM1 → ASM86 with fixed RESULT.COM; RILLBOOT → RBOOT → normalized RILL; both RILL-written ports match; scalar-check mismatch returns FAIL'
print(text);(ROOT/'qa/reader-handoff-results.txt').write_text(text+'\n')
