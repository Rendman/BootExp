"""Measure and execute each published editor construction with project tools."""
import json
from services import ROOT,W,Q,TOOLS,build,run
from editor_machine import EditorMachine,key
cases=json.loads((Q/'checkpoints.json').read_text());logs=[]
c=(W/'RILLED.COM').read_bytes();i=(W/'IRED.COM').read_bytes()
for case in cases:
 n=case['number'];source=(W/case['source']).read_bytes()
 if n<3:
  result=build(source);image=result[2]
  assert image==(W/('RILLEDB.COM' if n==1 else 'IREDB.COM')).read_bytes()
  if n==1:
   r=run(image,b'fn main(){vbegin();vend();return 0;}','RIL');assert r.exitcode==0 and b'VBEGIN' in r.files['RESULT.IR'] and b'VEND' in r.files['RESULT.IR']
   (W/'P01.IR').write_bytes(r.files['RESULT.IR'])
   # Built-in arity is checked by the real compiler.
   r=run(image,b'fn main(){vpos();return 0;}','RIL');assert r.exitcode==1
  else:
   r=run(image,b'PROC MAIN 0 0\nBMOVE\nRETURN\n',files={'EDITRT.ASM':(W/'EDITRT.ASM').read_bytes()});assert r.exitcode==1 and b'CODE 00004' in r.output
   _,_,ordinary=build((W/'P02.RIL').read_bytes(),(W/'RILLEDB.COM').read_bytes(),image,runtime=b'')
   assert run(ordinary).exitcode==0
   r=run(image,b'PROC MAIN 0 0\nLIT 0\nRETURN\n',files={'RESULT.ASM':b'OLD'})
   assert r.exitcode==1 and b'CODE 00006' in r.output and r.files['RESULT.ASM']==b'OLD'
 else:
  if n<8:source=(W/case['probe']).read_bytes()
  result=build(source,c,i,runtime=(W/case['source']).read_bytes() if n<8 else None)
  image=result[2];(W/(('S' if n<8 else 'E')+f'{n:02}.COM')).write_bytes(image)
  events=[266] if n in [5,15] else [271,270,263,262,266] if n==16 else [ord('!'),265,266] if n==17 else [264,ord('!'),265,266] if n==18 else [264,ord('!'),267,267,265,266] if n==19 else [268,ord('t'),ord('w'),ord('o'),13,ord('!'),265,266] if n==20 else []
  files={} if n<10 else {'EDIT.TXT':(W/case['fixture']).read_bytes()}
  r=EditorMachine(files,keys=[key(e) for e in events]).run(image,limit=1000000000)
  assert r.exitcode==0 and not r.keys and not r.allocations,(n,r.exitcode,r.output,r.keys)
  expected=(b'!one\r\ntwo\r\n' if n==17 else b'!ne\r\ntwo\r\n' if n==18 else b'one\r\n!two\r\n' if n==20 else b'one\r\ntwo\r\n') if n>=10 else None
  if n==14:expected=b'T\tX\r\nabc\r\n'
  if n>=10:assert r.files['EDIT.TXT']==expected,(n,r.files,expected)
  if n in [9,10,11,12]:
   # Required resource/input boundary, without adding display scaffolding.
   badfiles={'EDIT.TXT':b'123'} if n in [10,12] else {'EDIT.TXT':b'one\r\ntwo\r\n','EDIT.TMP':b'RECOVERY'} if n==11 else {}
   if n==9:
    from unicorn.x86_const import UC_X86_REG_AH,UC_X86_REG_AX
    class LowMemory(EditorMachine):
     def interrupt(self,c,num,unused):
      if num==0x21 and c.reg_read(UC_X86_REG_AH)==0x48 and len(self.allocations)==3:
       c.reg_write(UC_X86_REG_AX,8);self.carry(True);return
      super().interrupt(c,num,unused)
    bad=LowMemory(badfiles).run(image)
   else:bad=EditorMachine(badfiles).run(image)
   assert bad.exitcode==1 and not bad.allocations,(n,bad.exitcode,bad.output)
 case.update(ir_bytes=len(result[0]),assembly_bytes=len(result[1]),binary_bytes=len(image),binary_hex=image[:32].hex(' ').upper())
 logs.append(f'PASS {n:02}: project-built image, intended status, exact file/screen behavior and resource cleanup');print(logs[-1],flush=True)
(Q/'checkpoints.json').write_text(json.dumps(cases,indent=2)+'\n')
(Q/'checkpoint-results.txt').write_text('\n'.join(logs)+'\n')
