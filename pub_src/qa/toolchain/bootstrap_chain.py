"""Recreate every executable from canonical BASIC and the published native sources."""
from common import *
import sys,runpy,json
sys.path.insert(0,str(ROOT/'qa/asm86'))
from bootstrap import basic_build
text=basic_build();assert 'OK ASM86.COM' in text,text
from machine import assemble
from dos_machine import DosMachine
old=(ROOT/'workbench/asm86/ASM86.COM').read_bytes()
seed=assemble(old,(ROOT/'workbench/asm86a/ASMA0.ASM').read_bytes(),'ASMA0');assert seed.exitcode==0,seed.output
full=run(seed.files['ASMA0.COM'],(ROOT/'workbench/asm86a/ASM86A.ASM').read_bytes(),'ASM');assert full.exitcode==0,full.output
nativeasm=full.files['RESULT.COM']
wide=run(nativeasm,(ROOT/'workbench/ir86/IRWIDE.ASM').read_bytes(),'ASM');assert wide.exitcode==0,wide.output
irboot=wide.files['RESULT.COM']
# The one native IR construction is the prerequisite of both compiler milestones.
small_source=(ROOT/'workbench/ir86/IR86.ASM').read_bytes()
assert small_source==(ROOT/'workbench/ir86/IRWIDE.ASM').read_bytes()
r=run(irboot,(ROOT/'workbench/rill/RILL.IR').read_bytes());assert r.exitcode==0,r.output
r=run(nativeasm,r.files['RESULT.ASM'],'ASM');assert r.exitcode==0,r.output
small_result=run(r.files['RESULT.COM'],'fn main(){putc(65);}','RIL');assert small_result.exitcode==0,small_result.output
bridge=run(irboot,small_result.files['RESULT.IR']);assert bridge.exitcode==0,bridge.output
bridge=run(nativeasm,bridge.files['RESULT.ASM'],'ASM');assert bridge.exitcode==0,bridge.output
bridge=run(bridge.files['RESULT.COM']);assert bridge.exitcode==0 and bridge.output==b'A',bridge.output
r=run(irboot,(ROOT/'workbench/rill/RILLBOOT.IR').read_bytes());assert r.exitcode==0,r.output
r=run(nativeasm,r.files['RESULT.ASM'],'ASM');assert r.exitcode==0,r.output
rillboot=r.files['RESULT.COM'];images={}
for name in ['RILL','IR86','ASM86A']:
 r=run(rillboot if name=='RILL' else images['RILL'],(W/(name+'.RIL')).read_bytes(),'RIL');assert r.exitcode==0,(name,r.output)
 r=run(irboot,r.files['RESULT.IR']);assert r.exitcode==0,(name,r.output)
 r=run(nativeasm,r.files['RESULT.ASM'],'ASM');assert r.exitcode==0,(name,r.output)
 images[name]=r.files['RESULT.COM'];assert images[name]==(W/(name+'.COM')).read_bytes(),name
logs=['PASS canonical BOOTASM.BAS -> ASM86 -> ASMA0 -> ASM86A -> streaming IR86 -> IR-written compiler seed','PASS single required native IR86 -> RILL0 -> accepted executable; RILLBOOT continues the same IR compiler source', 'PASS compiler seed -> RILL compiler -> IR86 and ASM86 implementations -> identical executables']
for gen in [1,2]:
 nextimages={}
 for name in ['RILL','IR86','ASM86A']:
  r=run(images['RILL'],(W/(name+'.RIL')).read_bytes(),'RIL');assert r.exitcode==0,(gen,name,r.output)
  r=run(images['IR86'],r.files['RESULT.IR']);assert r.exitcode==0,(gen,name,r.output)
  r=run(images['ASM86A'],r.files['RESULT.ASM'],'ASM');assert r.exitcode==0,(gen,name,r.output)
  nextimages[name]=r.files['RESULT.COM'];assert nextimages[name]==images[name],(gen,name)
  logs.append(f'PASS fresh ladder generation {gen}: {name} reproduces {len(images[name])} bytes')
 images=nextimages
(Q/'bootstrap-results.txt').write_text('\n'.join(logs)+'\n');print('\n'.join(logs))
