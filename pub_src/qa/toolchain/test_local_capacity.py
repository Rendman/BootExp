"""Exercise RILL's local/frame limits through actual tools."""
from common import *
from portable import Machine
import json,re

compiler=(W/'RILL.COM').read_bytes()
facts=json.loads((Q/'local-capacity.json').read_text())
logs=[]
for name in ['TLOCAL.RIL','TSCOPE.RIL']:
 source=(W/name).read_bytes()
 r=run(compiler,source,'RIL');assert r.exitcode==0,r.output
 text=r.files['RESULT.IR'];assert b' 64\r\n' in text
 assembly,image=ir(text)
 child=run(image);assert child.exitcode==0 and child.output==b'',(name,child.exitcode,child.output)
 for base in [0x2000,0x4000]:
  p=Machine(data_base=base,handle_base=131,block_base=701).run(text)
  assert p.exitcode==0 and p.output==b'',(name,'portable',p.output,p.exitcode)
 facts[name]=dict(ir_bytes=len(text),assembly_bytes=len(assembly),binary_bytes=len(image),hex=image[:32].hex(' ').upper())
 logs.append('PASS '+name+': native and portable execution; zero status without display scaffolding')

old=b'accepted output\r\n'
r=run(compiler,(W/'XLOCAL.RIL').read_bytes(),'RIL',{'RESULT.IR':old})
assert r.exitcode==1 and r.files['RESULT.IR']==old and re.search(rb'CODE 00005\r\n',r.output),r.output
facts['error']=r.output.decode().strip()
logs.append('PASS local 65 rejected with code 5; accepted RESULT.IR preserved')

source='fn main(){'+''.join(f'let mut v{i}={i};' for i in range(16))+'return v15;}'
for image in [(ROOT/'workbench/rill0/RILL.COM').read_bytes(),(W/'RILLBOOT.COM').read_bytes()]:
 r=run(image,source,'RIL');assert r.exitcode==0,r.output
 r=run(image,source.replace('return v15;','let mut extra=0;return v15;'),'RIL',{'RESULT.IR':old})
 assert r.exitcode==1 and r.files['RESULT.IR']==old and b'CODE 00005' in r.output,r.output
logs.append('PASS RILL0 and RILLBOOT retain the 16-local boundary')
image=(W/'RC43.COM').read_bytes()
r=run(image,(W/'TLOCAL.RIL').read_bytes(),'RIL');assert r.exitcode==0,r.output
r=run(image,(W/'XLOCAL.RIL').read_bytes(),'RIL',{'RESULT.IR':old})
assert r.exitcode==1 and r.files['RESULT.IR']==old and b'CODE 00005' in r.output,r.output
logs.append('PASS seed-built RC43 already accepts 64 locals and rejects local 65')
(Q/'local-capacity.json').write_text(json.dumps(facts,indent=2)+'\n')
(Q/'local-capacity-results.txt').write_text('\n'.join(logs)+'\n')
print('\n'.join(logs))
