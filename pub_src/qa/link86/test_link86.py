"""Execute every published LINK86 checkpoint using the self-hosted trio."""
from pathlib import Path
import json,sys,re
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'qa/toolchain'))
from common import run,W as TOOLS
W=ROOT/'workbench/link86';Q=ROOT/'qa/link86'
cases=json.loads((Q/'checkpoints.json').read_text());logs=[]
def build(source):
 r=run((TOOLS/'RILL.COM').read_bytes(),source,'RIL');assert r.exitcode==0,r.output
 ir=r.files['RESULT.IR'];r=run((TOOLS/'IR86.COM').read_bytes(),ir);assert r.exitcode==0,r.output
 asm=r.files['RESULT.ASM'];r=run((TOOLS/'ASM86A.COM').read_bytes(),asm,'ASM');assert r.exitcode==0,r.output
 return ir,asm,r.files['RESULT.COM']
for c in cases:
 n=c['number'];ir,asm,image=build((W/c['source']).read_bytes());(W/f'L{n:02}.COM').write_bytes(image)
 files={'MAIN.OBJ':(W/f'M{n:02}.OBJ').read_bytes(),'RESULT.COM':b'OLD'}
 if c['util'] is not None:files['UTIL.OBJ']=(W/f'U{n:02}.OBJ').read_bytes()
 r=run(image,files=files);assert r.exitcode==0,(n,r.output)
 if c['expected'] is not None:
  actual=r.files[c['output_file']];assert actual==bytes.fromhex(c['expected']),(n,actual)
  assert r.output==f'OK {c["output_file"]} {len(actual):05} bytes\r\n'.encode(),(n,r.output)
  if c['program_output'] is not None:
   child=run(actual);assert child.exitcode==0 and child.output.decode()==c['program_output'],(n,child.output,child.exitcode)
 else:assert r.output==b'',(n,r.output)
 assert not r.allocations,(n,'allocation leak')
 bad=dict(files)
 if c['bad'] is None:bad.pop('MAIN.OBJ')
 else:bad['MAIN.OBJ']=(W/f'X{n:02}.OBJ').read_bytes()
 x=run(image,files=bad);assert x.exitcode==1 and x.files['RESULT.COM']==b'OLD',(n,x.output)
 if c['code'] is not None:assert f'CODE {c["code"]:05}'.encode() in x.output,(n,x.output)
 assert 'LINK.TMP' not in x.files and not x.allocations,(n,'failure cleanup')
 c.update(ir_bytes=len(ir),assembly_bytes=len(asm),binary_bytes=len(image),binary_hex=image[:32].hex(' ').upper(),console=r.output.decode(),error=x.output.decode())
 logs.append(f'PASS L{n:02}: RILL-written compiler/IR86/ASM86 build; exact result/status; rejection and prior-output preservation')
 print(logs[-1],flush=True)
(W/'LINK86.COM').write_bytes(image)
(Q/'checkpoints.json').write_text(json.dumps(cases,indent=2)+'\n')
# Final linker: grammar, relocation, and resource boundaries.
logs.append('PASS relative-call and absolute-data programs execute with expected output/status')
def execute(main,util='OBJ1\nEND\n',extra=None):
 f={'MAIN.OBJ':main.encode(),'UTIL.OBJ':util.encode(),'RESULT.COM':b'OLD'};f.update(extra or {})
 return run(image,files=f)
def reject(main,code,util='OBJ1\nEND\n',extra=None):
 r=execute(main,util,extra);assert r.exitcode==1 and f'CODE {code:05}'.encode() in r.output and r.files.get('RESULT.COM')==b'OLD',(main[:80],r.output)
 assert not r.allocations
 if not extra:assert 'LINK.TMP' not in r.files
 return r
for source,code in [('OBJ1\nB F\nEND\n',2),('OBJ1\nB 100\nEND\n',2),('OBJ1\nB\nEND\n',1),('OBJ1\nB '+'00 '*17+'\nEND\n',5),('OBJ1\nEND\nB 00\n',1),('OBJ1\nP 1BAD 0000\nEND\n',3),('OBJ1\nP X 0001\nEND\n',4),('OBJ1\nP X 00000\nEND\n',2),('OBJ1\nR X\nEND\n',3),('OBJ1\nA X\nEND\n',3),('OBJ1\nR X EXTRA\nEND\n',1),('OBJ1\nQ\nEND\n',1)]:reject(source,code)
logs.append('PASS malformed records, byte/word spelling, name/extent errors and unresolved references preserve output')
reject('OBJ1\nP X 0000\nEND\n',3,'OBJ1\nP x 0000\nEND\n')
name='A'*31;r=execute('OBJ1\nP '+name+' 0000\nB C3\nEND\n','OBJ1\nA '+name.lower()+'\nR '+name+'\nEND\n')
assert r.exitcode==0 and r.files['RESULT.COM']==bytes.fromhex('C3 00 01 FB FF'),r.output
reject('OBJ1\nP '+'A'*32+' 0000\nEND\n',5)
logs.append('PASS complete 31-character folded names, duplicates across modules, and backward relative displacement')
publics=''.join(f'P S{i} 0000\n' for i in range(256));r=execute('OBJ1\n'+publics+'END\n');assert r.exitcode==0 and r.files['RESULT.COM']==b''
reject('OBJ1\n'+publics+'P EXTRA 0000\nEND\n',5)
logs.append('PASS exactly 256 public records and rejection of record 257')
row='B '+'00 '*15+'00\n';full='OBJ1\n'+row*3824+'END\n'
r=execute(full);assert r.exitcode==0 and r.files['RESULT.COM']==bytes(61184),r.output
reject(full,5,'OBJ1\nB 00\nEND\n')
logs.append('PASS exactly 61184 bytes and rejection of one more byte across the second module')
for source in ['obj1\r\n; comment\r\nb 00 ff 1a\r\nend','OBJ1\rB 00 FF 1A\rEND\x1aignored','OBJ1\nB 00 FF 1A\nEND\n']:
 r=execute(source);assert r.exitcode==0 and r.files['RESULT.COM']==bytes([0,255,26]),r.output
logs.append('PASS CR/LF, bare CR/LF, final unterminated record, Control-Z text end and all materialized byte values')
for recovery in ['LINK.TMP','LINK.BAK']:
 r=reject('OBJ1\nEND\n',8,extra={recovery:b'RECOVERY'});assert r.files[recovery]==b'RECOVERY'
logs.append('PASS existing recovery files block publication without being changed')
# Reuse DOS fault injection at the actual file service boundary.
from machine import AssemblerMachine
from unicorn.x86_const import UC_X86_REG_AH,UC_X86_REG_AX,UC_X86_REG_BX
class Fault(AssemblerMachine):
 def __init__(self,which):super().__init__({'MAIN.OBJ':b'OBJ1\nB C3\nEND\n','UTIL.OBJ':b'OBJ1\nEND\n','RESULT.COM':b'OLD'});self.which=which
 def interrupt(self,c,num,unused):
  if num==0x21 and c.reg_read(UC_X86_REG_AH)==self.which and (self.which!=0x40 or c.reg_read(UC_X86_REG_BX)>2):
   c.reg_write(UC_X86_REG_AX,0);self.carry(self.which!=0x40);return
  super().interrupt(c,num,unused)
for function in [0x3f,0x3c,0x40,0x56]:
 r=Fault(function).run(image);assert r.exitcode==1 and b'CODE 00006' in r.output and r.files['RESULT.COM']==b'OLD',(function,r.output)
logs.append('PASS read/create/short-write/rename failures stop without replacing the accepted image')
(Q/'test-results.txt').write_text('\n'.join(logs)+'\n')
print('\n'.join(logs[-8:]))
class Changed(AssemblerMachine):
 def __init__(self,replacement):
  super().__init__({'MAIN.OBJ':b'OBJ1\nP X 0000\nB C3\nEND\n','UTIL.OBJ':b'OBJ1\nEND\n','RESULT.COM':b'OLD'});self.replacement=replacement;self.opens=0
 def interrupt(self,c,num,unused):
  from unicorn.x86_const import UC_X86_REG_DS,UC_X86_REG_DX
  if num==0x21 and c.reg_read(UC_X86_REG_AH)==0x3d and self.filename(c.reg_read(UC_X86_REG_DS)*16+c.reg_read(UC_X86_REG_DX))=='MAIN.OBJ':
   self.opens+=1
   if self.opens==2:self.files['MAIN.OBJ']=self.replacement
  super().interrupt(c,num,unused)
for replacement in [b'OBJ1\nP X 0001\nB C3\nEND\n',b'OBJ1\nB C3\nEND\n',b'OBJ1\nP X 0000\nB C3 C3\nEND\n']:
 r=Changed(replacement).run(image);assert r.exitcode==1 and b'CODE 00007' in r.output and r.files['RESULT.COM']==b'OLD' and 'LINK.TMP' not in r.files,(replacement,r.output)
logs.append('PASS changed public values, removed definitions and changed module lengths are rejected between passes')
class RenameFailure(AssemblerMachine):
 def __init__(self,restore=False,delete_backup=False):
  super().__init__({'MAIN.OBJ':b'OBJ1\nB C3\nEND\n','UTIL.OBJ':b'OBJ1\nEND\n','RESULT.COM':b'OLD'});self.restore=restore;self.delete_backup=delete_backup
 def interrupt(self,c,num,unused):
  from unicorn.x86_const import UC_X86_REG_DS,UC_X86_REG_DX
  ah=c.reg_read(UC_X86_REG_AH)
  if num==0x21 and ah in [0x56,0x41]:
   name=self.filename(c.reg_read(UC_X86_REG_DS)*16+c.reg_read(UC_X86_REG_DX))
   chosen=(ah==0x56 and not self.delete_backup and (name=='LINK.TMP' or self.restore and name=='LINK.BAK')) or (ah==0x41 and self.delete_backup and name=='LINK.BAK')
   if chosen:c.reg_write(UC_X86_REG_AX,5);self.carry(True);return
  super().interrupt(c,num,unused)
r=RenameFailure().run(image);assert r.exitcode==1 and r.files['RESULT.COM']==b'OLD' and 'LINK.TMP' not in r.files and 'LINK.BAK' not in r.files
r=RenameFailure(restore=True).run(image);assert r.exitcode==1 and 'RESULT.COM' not in r.files and r.files['LINK.BAK']==b'OLD' and r.files['LINK.TMP']==b'\xc3'
r=RenameFailure(delete_backup=True).run(image);assert r.exitcode==1 and r.files['RESULT.COM']==b'\xc3' and r.files['LINK.BAK']==b'OLD'
logs.append('PASS publication restoration and retained recovery files after restoration/backup-deletion failure')
(Q/'test-results.txt').write_text('\n'.join(logs)+'\n')
print('\n'.join(logs[-2:]))
