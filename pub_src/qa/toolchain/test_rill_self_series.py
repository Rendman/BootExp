from common import *
import json,re
cases=json.loads((Q/'rill-self-series.json').read_text());logs=[];seed=(W/'RILLBOOT.COM').read_bytes()
for c in cases:
 n=c['number'];r=run(seed,(W/c['source']).read_bytes(),'RIL');assert r.exitcode==0,(n,'source',r.output)
 text=r.files['RESULT.IR'];a,image=ir(text);(W/f'RC{n:02}.COM').write_bytes(image)
 files={'RESULT.IR':b'OLD'}
 if c['fixture'] is not None:files['SOURCE.RIL']=(W/f'TRC{n:02}.RIL').read_bytes()
 r=run(image,files=files);assert r.exitcode==c.get('accept_exit',0),(n,c['title'],r.output)
 if c['key'].upper()=='MAIN':assert r.output==f'OK RESULT.IR {len(r.files["RESULT.IR"]):010}\r\n'.encode()
 else:assert r.output.decode()==c['expected'],(n,c['title'],r.output,c['expected'])
 c.update(binary_bytes=len(image),ir_bytes=len(text),assembly_bytes=len(a),console=r.output.decode())
 result=r.files.get('RILL.TMP')
 if c['key']=='main':result=r.files['RESULT.IR'];assert image==(W/'RILL.COM').read_bytes()
 if c['fragment'] is not None:assert result==c['fragment'].encode(),(n,result,c['fragment'])
 if result is not None:c.update(result=result.decode(),result_bytes=len(result),result_hex=result[:32].hex(' ').upper())
 if c['complete']:
  _,program=ir(result);child=run(program);expect=b'HI' if c['key']=='main' else b'A' if c['key']=='function' else b'AB'
  assert child.exitcode==0 and child.output==expect,(n,child.exitcode,child.output)
  c.update(program_bytes=len(program),program_output=expect.decode())
 if c['code']:
  rejected=run(image,c['bad'],'RIL',{'RESULT.IR':b'OLD'})
  assert rejected.exitcode==1 and rejected.files['RESULT.IR']==b'OLD' and re.search(rb'CODE 0*'+str(c['code']).encode()+rb'\r\n',rejected.output),(n,rejected.output)
  c['error']=rejected.output.decode()
 else:c['boundary']=None
 logs.append(f'PASS RC{n:02}: IR-written compiler seed/native IR86/ASM86A build, exact helper or parser result'+(', executable output' if c['complete'] else '')+(', rejection and preservation' if c['code'] else ', status/value check'))
 print(logs[-1],flush=True)
(Q/'rill-self-series.json').write_text(json.dumps(cases,indent=2)+'\n');(Q/'rill-self-series-results.txt').write_text('\n'.join(logs)+'\n')
