from common import *
from portable import Machine
import json,re
cases=json.loads((ROOT/'tools/toolchain_examples.json').read_text());logs=[]
for c in cases:
 source=c['source'].encode('ascii').replace(b'\n',b'\r\n');(W/(c['name']+'.RIL')).write_bytes(source)
 r=run((W/'RILL.COM').read_bytes(),source,'RIL');assert r.exitcode==0,(c['name'],r.output)
 text=r.files['RESULT.IR'];a,image=ir(text,(W/'IR86.COM').read_bytes());given={n:b.encode() for n,b in c.get('files',{}).items()}
 native=run(image,files=given);p=Machine(given,data_base=0x4000,handle_base=137,block_base=707).run(text)
 assert native.exitcode==p.exitcode==0 and native.output==p.output==c['output'].encode(),(c['name'],native.output,native.exitcode,p.output)
 if c.get('result_file'):assert native.files[c['result_file']]==p.files[c['result_file']]==given['IN.TXT']
 bad=run((W/'RILL.COM').read_bytes(),c['bad'],'RIL',{'RESULT.IR':b'OLD'})
 assert bad.exitcode==1 and bad.files['RESULT.IR']==b'OLD' and re.search(rb'CODE 0*'+str(c['code']).encode()+rb'\r\n',bad.output),(c['name'],bad.output)
 c.update(ir_bytes=len(text),assembly_bytes=len(a),binary_bytes=len(image),hex=image[:32].hex(' ').upper(),error=bad.output.decode().strip())
 logs.append('PASS '+c['name']+': complete source, native/portable output and files, exact rejection and preservation')
# Counted copying also preserves all possible byte values and empty input.
c=next(c for c in cases if c['name']=='ECOPY');r=run((W/'RILL.COM').read_bytes(),c['source'],'RIL');_,image=ir(r.files['RESULT.IR'])
for data in [b'',bytes(range(256))*3]:
 n=run(image,files={'IN.TXT':data});assert n.exitcode==0 and n.files['OUT.TXT']==data
 logs.append('PASS ECOPY byte transfer '+str(len(data)))
(Q/'examples.json').write_text(json.dumps(cases,indent=2)+'\n');(Q/'example-results.txt').write_text('\n'.join(logs)+'\n');print('PASS all toolchain-language examples')
