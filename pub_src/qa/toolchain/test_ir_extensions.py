from common import *
import json
cases=json.loads((Q/'ir-extensions.json').read_text());logs=[]
for c in cases:
 n=c['number'];image=asm((W/c['source']).read_bytes());(W/f'IW{n:02}.COM').write_bytes(image)
 r=run(image,(W/f'TIW{n:02}.IR').read_bytes(),files={'RESULT.ASM':b'OLD'})
 assert r.exitcode==0,(n,r.output)
 c.update(binary_bytes=len(image),output=r.output.decode())
 if n<=2 or n==4:assert r.files['RESULT.ASM']==b'OLD'
 elif n==3:assert r.files['RESULT.ASM']==b'ABC\r\n'
 else:
  assembly=r.files['RESULT.ASM'];target=asm(assembly);files={'A':b'A'} if n in [13,15,17,21] else {}
  child=AssemblerMachine(files,stdin=b'A').run(target);expected=b'A' if n in [11,12] else b'H' if n==20 else b'';status=65 if n in [7,10] else 0
  assert child.exitcode==status and child.output==expected,(n,child.exitcode,child.output)
  c.update(assembly_bytes=len(assembly),target_bytes=len(target),target_hex=target[:32].hex(' ').upper(),program_output=expected.decode(),program_exit=status)
 if n<=4:
  rejected=run(image,files={'RESULT.ASM':b'OLD'})
  assert rejected.exitcode==1 and rejected.files['RESULT.ASM']==b'OLD'
  c.update(bad=None,error=rejected.output.decode())
 else:
  rejected=run(image,'UNKNOWN\n',files={'RESULT.ASM':b'OLD'})
  assert rejected.exitcode==1 and rejected.files['RESULT.ASM']==b'OLD'
  c.update(bad='UNKNOWN\n',error=rejected.output.decode())
 logs.append(f'PASS IW{n:02}: preceding assembler build, diagnostic or executable output, rejection and preservation')
 print(logs[-1],flush=True)
(Q/'ir-extensions.json').write_text(json.dumps(cases,indent=2)+'\n');(Q/'ir-extension-results.txt').write_text('\n'.join(logs)+'\n')
