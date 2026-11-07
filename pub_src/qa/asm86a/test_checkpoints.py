"""Build each published checkpoint with its actual preceding project assembler."""
from machine import *
import json,re
W=ROOT/'workbench/asm86a';Q=ROOT/'qa/asm86a';old=(ROOT/'workbench/asm86/ASM86.COM').read_bytes()
cases=json.loads((Q/'checkpoints.json').read_text());results=[];seed=None
for c in cases:
 n=c['number'];name=f'A{n:02}';source=(W/(name+'.ASM')).read_bytes()
 assert all(len(row)<=120 for row in source.splitlines()),(name,'source width')
 if n<=12:built=assemble(old,source,name);key=name+'.COM'
 else:built=run_assembler(seed,source);key='RESULT.COM'
 assert built.exitcode==0,(name,'build',built.output)
 image=built.files[key];(W/(name+'.COM')).write_bytes(image);c['binary_bytes']=len(image)
 if n==12:
  seed=image;(W/'ASMA0.COM').write_bytes(image)
 text=(W/c['fixture_ref']).read_bytes() if c.get('fixture_ref') else (W/f'T{n:02}.ASM').read_bytes()
 r=run_assembler(image,text,{'RESULT.COM':b'OLD'})
 assert r.exitcode==0,(name,'acceptance',r.output)
 outname=c.get('output_file','RESULT.COM');target=r.files[outname]
 if c.get('self_build'):
  assert target==image,(name,'first self-build differs')
  again=run_assembler(target,text);assert again.exitcode==0 and again.files['RESULT.COM']==image,(name,'second self-build differs')
  c['expected']=None
 elif c.get('expected') is not None:assert target==bytes.fromhex(c['expected']),(name,'bytes',target[:40],c['expected'])
 c.update(target_bytes=len(target),target_hex=target[:64].hex(' ').upper())
 assert r.output==c.get('prefix','').encode()+f'OK {outname} {len(target):05} bytes\r\n'.encode(),(name,r.output)
 if c.get('program_output') is not None:
  child=AssemblerMachine().run(target)
  assert child.exitcode==c.get('program_exit',0) and child.output.decode()==c['program_output'],(name,'target runtime',child.exitcode,child.output)
 bad=c['bad'];f={'RESULT.COM':b'OLD'}
 if bad['kind']=='source':f['SOURCE.ASM']=(W/f'X{n:02}.ASM').read_bytes()
 elif bad['kind']=='reserved':f.update({'SOURCE.ASM':text,bad['name']:b'RECOVERY'})
 rejected=run_assembler(image,files=f)
 width=10 if n>=19 else 5
 expected=f'ERROR {bad["line"]:0{width}} CODE {bad["code"]}'.encode()
 assert rejected.exitcode==1 and expected in rejected.output,(name,'rejection',rejected.output,expected)
 assert rejected.files['RESULT.COM']==b'OLD',(name,'changed prior output')
 if n>=4 and bad['kind']!='reserved':assert 'ASMA.TMP' not in rejected.files,(name,'orphan temporary')
 if bad['kind']=='reserved':assert rejected.files[bad['name']]==b'RECOVERY'
 assert not r.allocations and not rejected.allocations,(name,'allocation leak')
 c['builder']='ASM86' if n<=12 else 'ASMA0'
 results.append(f'PASS {name}: {c["builder"]} build, exact acceptance, rejection and prior-output preservation'+(', executable result' if c.get('program_output') is not None else ', inspected data or self-build'))
 print(results[-1],flush=True)
assert (W/'ASMA0.ASM').read_bytes()==(W/'A12.ASM').read_bytes()
assert (W/'ASM86A.ASM').read_bytes()==(W/'A40.ASM').read_bytes()
(W/'ASM86A.COM').write_bytes((W/'A40.COM').read_bytes())
(Q/'checkpoints.json').write_text(json.dumps(cases,indent=2)+'\n');(Q/'checkpoint-results.txt').write_text('\n'.join(results)+'\n')
print('PASS all',len(cases),'ASM1/ASM86 construction checkpoints')
