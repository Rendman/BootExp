"""Run complete hand-authored IR programs and publish their actual target text."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'qa/asm86'))
from dos_machine import DosMachine,assemble
W=ROOT/'workbench/ir86';IR=(W/'IR86.COM').read_bytes();ASM=(ROOT/'workbench/asm86/ASM86.COM').read_bytes()
results=[];metadata=[]
for name,output in [('HELLO','HI'),('COUNT','012'),('BYTES','OK'),('COPYFILE','')]:
 text=(W/(name+'.IR')).read_text();(W/(name+'.IR')).write_bytes(text.replace('\n','\r\n').encode('ascii'))
 result=DosMachine({name+'.IR':(W/(name+'.IR')).read_bytes()},[name]).run(IR)
 assert result.exitcode==0,(name,result.output)
 source=result.files[name+'.ASM'];(W/(name+'.ASM')).write_bytes(source)
 built=assemble(ASM,source,name);assert built.exitcode==0,(name,built.output)
 code=built.files[name+'.COM'];(W/(name+'.COM')).write_bytes(code)
 if name=='COPYFILE':
  for payload in [b'',b'An IR86 file copy.\r\n',bytes(range(256)),bytes(range(256))*3]:
   run=DosMachine({'IN.TXT':payload,'OUT.TXT':b'old file tail'},[]).run(code)
   assert run.exitcode==0 and run.files['OUT.TXT']==payload and run.files['IN.TXT']==payload,(name,run.output,run.exitcode)
  missing=DosMachine({'OUT.TXT':b'old'}).run(code)
  assert missing.exitcode==1 and missing.files['OUT.TXT']==b'old'
 else:
  run=DosMachine().run(code);assert run.exitcode==0 and run.output.decode()==output,(name,run.output,run.exitcode)
  edits={'HELLO':('TODX','TODX EXTRA',3,1),'COUNT':('PUSH\nLIT 51','LIT 51',13,4),'BYTES':('BYTE TEXT0','BYTE 1TEXT',1,3)}
  before,after,line,error=edits[name]
  rejected=DosMachine({'BAD.IR':text.replace(before,after,1).encode('ascii')},['BAD']).run(IR)
  assert rejected.exitcode==1 and f'IR ERROR {line:05} CODE {error}'.encode() in rejected.output,(name,rejected.output)
 metadata.append(dict(name=name,output=output,text_bytes=len(source),binary_bytes=len(code)))
 results.append(f'PASS {name}: native IR translation, ASM86 assembly, expected runtime'+('; empty/text/binary copy and missing-input failure' if name=='COPYFILE' else ''))
 print(results[-1])
(ROOT/'qa/ir86/example-results.txt').write_text('\n'.join(results)+'\n')
(ROOT/'qa/ir86/examples.json').write_text(json.dumps(metadata,indent=2)+'\n')
