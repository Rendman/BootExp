"""Build and execute the complete printed ASM86A examples with the published tool."""
from machine import *
import json
W=ROOT/'workbench/asm86';Q=ROOT/'qa/asm86';image=(W/'ASM86A.COM').read_bytes();records=[];logs=[]
for name,out in [('HELLO',b'Hello\r\n'),('FRAME',b'A'),('BRIDGE',b'B'),('COPYTEXT',b'Hi')]:
 source=(W/(name+'.ASM')).read_bytes();r=run_assembler(image,source);assert r.exitcode==0,(name,r.output)
 code=r.files['RESULT.COM'];(W/(name+'.COM')).write_bytes(code)
 child=DosMachine().run(code);assert child.exitcode==0 and child.output==out,(name,child.output)
 edits={'HELLO':('DB "Hello",13,10','DB "Hello,13,10',18,1),'FRAME':('[BP+4]','[SP+4]',17,1),'BRIDGE':('JNE NEAR SHOW','JNE SHOW',3,4),'COPYTEXT':('LODSB','LODSB 1',5,1)}
 before,after,_,category=edits[name];text=source.decode().replace('\r\n','\n');badtext=text.replace(before,after,1)
 line=next(i for i,(a,b) in enumerate(zip(text.splitlines(),badtext.splitlines()),1) if a!=b)
 bad=run_assembler(image,badtext,{'RESULT.COM':b'OLD'})
 assert bad.exitcode==1 and f'ERROR {line:010} CODE {category}'.encode() in bad.output and bad.files['RESULT.COM']==b'OLD',(name,bad.output)
 records.append(dict(name=name,output=out.decode(),binary_bytes=len(code),hex=code[:32].hex(' ').upper(),bad_before=before,bad_after=after,bad_line=line,bad_code=category))
 logs.append('PASS '+name+': source assembled, native output/status correct, exact printed rejection preserves prior output')
 print(logs[-1])
(Q/'examples.json').write_text(json.dumps(records,indent=2)+'\n');(Q/'example-results.txt').write_text('\n'.join(logs)+'\n')
