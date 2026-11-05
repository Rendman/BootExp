"""Build every published IR checkpoint using IR86 and ASM86 and test its visible stops."""
from common import *
import json
cases=json.loads((Q/'checkpoints.json').read_text());records=[]
for c in cases:
 n=c['number'];name=f'R{n:02}';source=(W/c['source']).read_bytes()
 assembly,image=build_ir(source,name)
 (W/(name+'.ASM')).write_bytes(assembly);(W/(name+'.COM')).write_bytes(image)
 fixture=(W/f'T{n:02}.RIL').read_bytes() if n>=6 and n!=7 else b''
 if c.get('stdin'):r=DosMachine(stdin=fixture).run(image)
 else:r=run_compiler(fixture,image,{'RESULT.IR':b'OLD RESULT'})
 assert r.exitcode==0,(name,r.output)
 c.update(binary_bytes=len(image),assembly_bytes=len(assembly))
 if n<15:assert r.output.decode()==c['output'],(name,r.output,c['output'])
 else:
  ir=r.files['RESULT.IR'];(W/f'T{n:02}.IR').write_bytes(ir)
  assert r.output==f'OK RESULT.IR {len(ir):05}\r\n'.encode(),(name,r.output)
  targetasm,target=build_ir(ir,f'T{n:02}');(W/f'T{n:02}.ASM').write_bytes(targetasm);(W/f'T{n:02}.COM').write_bytes(target)
  c.update(text_bytes=len(ir),target_bytes=len(target),target_hex=target.hex(' ').upper())
  child=DosMachine(stdin=c.get('program_stdin','').encode()).run(target)
  assert (child.exitcode,child.output.decode())==(c.get('program_exit',0),c['program_output']),(name,child.exitcode,child.output)
  portable=Machine(stdin=c.get('program_stdin','').encode()).run(ir)
  assert (portable.exitcode,portable.output)==(child.exitcode,child.output),(name,'portable target differs')
 bad=c['bad'];suffix='IR' if bad['kind']=='ir' else 'RIL';badsource=(W/f'X{n:02}.{suffix}').read_bytes()
 if bad['kind']=='ir':
  translator=(ROOT/'workbench/ir86/IR86.COM').read_bytes()
  rejected=DosMachine({'BAD.IR':badsource,'BAD.ASM':b'OLD RESULT'},['BAD']).run(translator)
  diagnostic=f'IR ERROR {bad["line"]:05} CODE {bad["code"]}'.encode()
  assert diagnostic in rejected.output and rejected.exitcode==1,(name,rejected.output)
  assert rejected.files['BAD.ASM']==b'OLD RESULT'
 else:
  if c.get('stdin'):rejected=DosMachine(stdin=badsource).run(image)
  else:rejected=run_compiler(None if bad['kind']=='missing' else badsource,image,{'RESULT.IR':b'OLD RESULT'})
  diagnostic=f'ERROR {bad["line"]:05} CODE {bad["code"]:05}\r\n'.encode()
  assert rejected.exitcode==1 and rejected.output==diagnostic,(name,rejected.output,diagnostic)
  if not c.get('stdin'):assert rejected.files['RESULT.IR']==b'OLD RESULT',(name,'rejection overwrote old result')
 records.append(f'PASS {name}: published IR86 translation and ASM86 assembly; exact visible acceptance; rejection'+('; emitted program assembles and runs with portable agreement' if n>=15 else ''))
 print(records[-1],flush=True)
assert (W/'RILL.IR').read_bytes()==(W/'R29.IR').read_bytes()
(W/'RILL.ASM').write_bytes((W/'R29.ASM').read_bytes());(W/'RILL.COM').write_bytes((W/'R29.COM').read_bytes())
(Q/'checkpoints.json').write_text(json.dumps(cases,indent=2)+'\n')
(Q/'checkpoint-results.txt').write_text('\n'.join(records)+'\n')
print('PASS all 29 gradual RILL construction checkpoints')
