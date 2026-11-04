"""Compare unchanged portable example sources across two execution models."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'qa/asm86'))
from dos_machine import DosMachine,assemble
from portable_machine import Machine
W=ROOT/'workbench/ir86';IR=(W/'IR86.COM').read_bytes();ASM=(ROOT/'workbench/asm86/ASM86.COM').read_bytes()
results=[];metadata=[]
for name,output in [('HELLO','HI'),('COUNT','012'),('BYTES','OK'),('ECHOIR','IR86 echo.\r\n'),('COPYFILE','')]:
 text=(W/(name+'.IR')).read_text();(W/(name+'.IR')).write_bytes(text.replace('\n','\r\n').encode('ascii'))
 result=DosMachine({name+'.IR':(W/(name+'.IR')).read_bytes()},[name]).run(IR)
 assert result.exitcode==0,(name,result.output)
 source=result.files[name+'.ASM'];(W/(name+'.ASM')).write_bytes(source)
 built=assemble(ASM,source,name);assert built.exitcode==0,(name,built.output)
 code=built.files[name+'.COM'];(W/(name+'.COM')).write_bytes(code)
 if name=='COPYFILE':
  samples=[({'IN.TXT':b'','OUT.TXT':b'old'},b'',0),({'IN.TXT':b'An IR86 file copy.\r\n','OUT.TXT':b'old'},b'',0),({'IN.TXT':bytes(range(256))},b'',0),({'IN.TXT':bytes(range(256))*3},b'',0),({'OUT.TXT':b'old'},b'',1)]
 elif name=='ECHOIR':samples=[({},output.encode(),0),({},b'',0),({},bytes(range(256)),0)]
 else:samples=[({},b'',0)]
 for files,stdin,status in samples:
  native=DosMachine(files,stdin=stdin).run(code);portable=Machine(files,stdin).run(text)
  assert (native.exitcode,native.output,native.files)==(portable.exitcode,portable.output,portable.files),(name,'behavior differs')
  assert native.exitcode==status,(name,native.exitcode)
  if name=='COPYFILE':
   assert native.files.get('OUT.TXT')==(files['IN.TXT'] if status==0 else files['OUT.TXT'])
  elif name=='ECHOIR':assert native.output==stdin
  else:assert native.output.decode()==output
 if name!='COPYFILE':
  edits={'HELLO':('PUTC','PUTC EXTRA',3,1),'COUNT':('PUSH\nLIT 51','LIT 51',13,4),'BYTES':('BYTE TEXT0','BYTE 1TEXT',1,3),'ECHOIR':('GETC','GETC EXTRA',4,1)}
  before,after,line,error=edits[name]
  rejected=DosMachine({'BAD.IR':text.replace(before,after,1).encode()},['BAD']).run(IR)
  assert rejected.exitcode==1 and f'IR ERROR {line:05} CODE {error}'.encode() in rejected.output,(name,rejected.output)
 metadata.append(dict(name=name,output=output,stdin=output if name=='ECHOIR' else '',text_bytes=len(source),binary_bytes=len(code)))
 results.append(f'PASS {name}: identical IR source; portable VM and native backend agree on status, output, and files')
 print(results[-1])
(ROOT/'qa/ir86/example-results.txt').write_text('\n'.join(results)+'\n')
(ROOT/'qa/ir86/examples.json').write_text(json.dumps(metadata,indent=2)+'\n')
