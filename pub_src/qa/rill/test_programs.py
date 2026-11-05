"""Compile and execute complete printed RILL programs without a host compiler."""
from common import *
import json
records=[];logs=[]
for name,expected in [('HELLO',b'HI'),('COUNT',b'012'),('CHOICE',b'U!'),('RLECHO',b'RILL echo.\r\n')]:
 source=(W/(name+'.RIL')).read_bytes();r=run_compiler(source)
 assert r.exitcode==0,(name,r.output)
 ir=r.files['RESULT.IR'];(W/(name+'.IR')).write_bytes(ir)
 assembly,code=build_ir(ir,name);(W/(name+'.ASM')).write_bytes(assembly);(W/(name+'.COM')).write_bytes(code)
 streams=[expected,b'',bytes(range(256))] if name=='RLECHO' else [b'']
 for stdin in streams:
  native=DosMachine(stdin=stdin).run(code);portable=Machine(stdin=stdin).run(ir)
  out=stdin if name=='RLECHO' else expected
  assert (native.exitcode,native.output)==(0,out),(name,native.output)
  assert (portable.exitcode,portable.output)==(native.exitcode,native.output)
 model=Machine({'SOURCE.RIL':source}).run((W/'RILL.IR').read_bytes(),limit=10_000_000)
 assert (model.exitcode,model.output,model.files)==(r.exitcode,r.output,r.files),(name,'IR-written compiler differs in the portable model')
 text=source.decode('ascii')
 edits={'HELLO':('putc','putcat',2,2),'COUNT':('    let mut x = 48;\r\n','',2,4),'CHOICE':('65535','65536',2,3),'RLECHO':('getc()','getc(1)',4,2)}
 before,after,line,error=edits[name]
 rejected=run_compiler(text.replace(before,after,1),files={'RESULT.IR':b'OLD RESULT'})
 assert rejected.exitcode==1 and rejected.output==f'ERROR {line:05} CODE {error:05}\r\n'.encode(),(name,'printed rejection',rejected.output)
 assert rejected.files['RESULT.IR']==b'OLD RESULT'
 if name=='COUNT':
  rejected=run_compiler(text.replace('x = x + 1;','x = x + 1'),files={'RESULT.IR':b'OLD RESULT'})
  assert rejected.exitcode==1 and rejected.output==b'ERROR 00006 CODE 00002\r\n',rejected.output
 records.append(dict(name=name,output=expected.decode(),text_bytes=len(ir),assembly_bytes=len(assembly),binary_bytes=len(code)))
 logs.append('PASS '+name+': IR-written compiler agrees in portable/native execution; emitted IR and machine program agree, including byte-stream cases')
 print(logs[-1],flush=True)
(Q/'examples.json').write_text(json.dumps(records,indent=2)+'\n');(Q/'example-results.txt').write_text('\n'.join(logs)+'\n')
