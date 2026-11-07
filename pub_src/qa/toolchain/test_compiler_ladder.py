"""Execute the single compiler construction and its continuing complete profiles."""
from common import *
import json,re
logs=[]
for family,folder,prefix in [('rill-initial-series',ROOT/'workbench/rill','R'),('rill-seed-series',W,'RB')]:
 cases=json.loads((Q/(family+'.json')).read_text())
 for c in cases:
  n=c['number'];assembly,image=ir((folder/c['source']).read_bytes())
  (folder/f'{prefix}{n:02}.ASM').write_bytes(assembly);(folder/f'{prefix}{n:02}.COM').write_bytes(image)
  files={'RESULT.IR':b'OLD'}
  if c['fixture'] is not None:files['SOURCE.RIL']=c['fixture'].encode()
  r=run(image,files=files)
  assert r.exitcode==c.get('accept_exit',0),(family,n,c['title'],r.output)
  if c['key']=='MAIN':assert r.output==f'OK RESULT.IR {len(r.files["RESULT.IR"]):010}\r\n'.encode(),(family,n,r.output)
  else:assert r.output.decode()==c['expected'],(family,n,c['title'],r.output,c['expected'])
  c.update(binary_bytes=len(image),assembly_bytes=len(assembly),console=r.output.decode())
  result=r.files.get('RILL.TMP') if c['key']!='MAIN' else r.files['RESULT.IR']
  if c['fragment'] is not None:assert result==c['fragment'].encode(),(family,n,result,c['fragment'])
  if result is not None:c.update(result=result.decode(),result_bytes=len(result),result_hex=result[:32].hex(' ').upper())
  if c['complete']:
   _,target=ir(result);child=run(target,files={k:v.encode() for k,v in c.get('files',{}).items()})
   expected=c.get('program_output','HI' if c['key']=='MAIN' else 'AB').encode()
   assert child.exitcode==0 and child.output==expected,(family,n,child.exitcode,child.output,expected)
   c.update(program_bytes=len(target),program_output=expected.decode())
   if c.get('result_file'):assert child.files[c['result_file']]==c['result_data'].encode(),(n,child.files)
  if c.get('code'):
   rejected=run(image,c['bad'],'RIL',{'RESULT.IR':b'OLD'})
   assert rejected.exitcode==1 and rejected.files['RESULT.IR']==b'OLD' and re.search(rb'CODE 0*'+str(c['code']).encode()+rb'\r\n',rejected.output),(family,n,rejected.output)
   c['error']=rejected.output.decode()
  if prefix=='RB':
   # Each complete continuation must retain the earlier core language.
   retained=run(image,'fn main(){let mut x=48;while x<51{putc(x);x=x+1;}}','RIL');assert retained.exitcode==0,(n,retained.output)
   _,check=ir(retained.files['RESULT.IR']);check=run(check);assert check.exitcode==0 and check.output==b'012'
  logs.append(f'PASS {prefix}{n:02}: project IR/assembler build; exact result and status'+('; source rejection preserves previous output' if c.get('code') else ''))
  print(logs[-1],flush=True)
 # Complete milestones retain all programs supported by preceding complete profiles.
 final=cases[-1];image=(folder/f'{prefix}{final["number"]:02}.COM').read_bytes()
 if prefix=='R':
  (folder/'RILL.COM').write_bytes(image);(folder/'RILL.ASM').write_bytes((folder/f'R{final["number"]:02}.ASM').read_bytes())
 else:
  (ROOT/'workbench/rill/RILLBOOT.COM').write_bytes(image);(W/'RILLBOOT.COM').write_bytes(image)
  (W/'RILLBOOT.ASM').write_bytes((folder/f'RB{final["number"]:02}.ASM').read_bytes())
 (Q/(family+'.json')).write_text(json.dumps(cases,indent=2)+'\n')
 # Exercise core language and failures with actual compiler outputs.
 programs=[('fn main(){putc(65);}',b'A'),('fn main(){let mut count=48;while count<51{putc(count);count=count+1;}}',b'012'),('fn main(){if 65535>1{putc(89);}else{putc(78);}}',b'Y')]
 for source,expected in programs:
  r=run(image,source,'RIL');assert r.exitcode==0,r.output
  _,child=ir(r.files['RESULT.IR']);child=run(child);assert child.exitcode==0 and child.output==expected
 for source in ['fn main(){putc(65536);}','fn main(){missing=1;}','fn main(){let mut x=x;}','fn main(){putc(65) }']:
  r=run(image,source,'RIL',{'RESULT.IR':b'OLD'});assert r.exitcode==1 and r.files['RESULT.IR']==b'OLD',(source,r.output)
 if prefix=='R':
  for source in ['fn main(){putc(1*2);}','fn main(){putc(load8("A"));}','fn other(){}','fn main(x){}','fn main(){return getc();}']:
   r=run(image,source,'RIL',{'RESULT.IR':b'OLD'});assert r.exitcode==1 and r.files['RESULT.IR']==b'OLD',(source,r.output)
 else:
  for c in cases:
   r=run(image,c['fixture'],'RIL');assert r.exitcode==0,(c['number'],r.output)
  for source in ['fn main(){return 1<<2;}','fn main(){return 1^2;}','fn main(){return -1;}','fn main(){return ~1;}','fn main(){let mut x=0;return &x;}','fn main(){return getc();}']:
   r=run(image,source,'RIL',{'RESULT.IR':b'OLD'});assert r.exitcode==1 and r.files['RESULT.IR']==b'OLD',(source,r.output)
(Q/'compiler-ladder-results.txt').write_text('\n'.join(logs)+'\n')
print('PASS both required compiler milestones, retained programs, and exact subset rejections')
