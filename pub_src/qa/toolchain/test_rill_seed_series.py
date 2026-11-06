from common import *
import json,re
cases=json.loads((Q/'rill-seed-series.json').read_text());logs=[]
for c in cases:
 n=c['number'];assembly,image=ir((W/c['source']).read_bytes());(W/f'RB{n:02}.COM').write_bytes(image)
 files={'RESULT.IR':b'OLD'}
 if c['fixture'] is not None:files['SOURCE.RIL']=(W/f'TRB{n:02}.RIL').read_bytes()
 r=run(image,files=files);assert r.exitcode==0,(n,c['title'],r.output)
 if c['expected']:assert r.output.decode()==c['expected'],(n,c['title'],r.output,c['expected'])
 c.update(binary_bytes=len(image),assembly_bytes=len(assembly),console=r.output.decode())
 result=r.files.get('RILL.TMP')
 if c['key']=='MAIN':result=r.files['RESULT.IR']
 if c['fragment'] is not None:assert result==c['fragment'].encode(),(n,result,c['fragment'])
 if result is not None:
  c.update(result=result.decode(),result_bytes=len(result),result_hex=result[:32].hex(' ').upper())
 if c['complete']:
  _,program=ir(result);child=run(program);expect=b'HI' if c['key']=='MAIN' else b'A' if c['key']=='FUNCTION' else b'AB'
  assert child.exitcode==0 and child.output==expect,(n,child.exitcode,child.output)
  c.update(program_bytes=len(program),program_output=expect.decode())
 if c['code']:
  rejected=run(image,c['bad'],'RIL',{'RESULT.IR':b'OLD'})
  assert rejected.exitcode==1 and rejected.files['RESULT.IR']==b'OLD' and re.search(rb'CODE 0*'+str(c['code']).encode()+rb'\r\n',rejected.output),(n,rejected.output)
  c['error']=rejected.output.decode()
 else:
  # A direct representable boundary value for scalar helpers; never a generated artifact.
  c['boundary']='IR86 must reject LIT 65536 before building a diagnostic executable.'
 logs.append(f'PASS RB{n:02}: native IR86/ASM86A build, exact helper or parser result'+(', executable output' if c['complete'] else '')+(', rejection and old-result preservation' if c['code'] else ', preceding-language word boundary'))
 print(logs[-1],flush=True)
(Q/'rill-seed-series.json').write_text(json.dumps(cases,indent=2)+'\n');(Q/'rill-seed-results.txt').write_text('\n'.join(logs)+'\n')
