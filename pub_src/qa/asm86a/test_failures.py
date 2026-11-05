"""Exercise DOS failure paths without supplying any encoded executable bytes."""
from machine import *
W=ROOT/'workbench/asm86a';Q=ROOT/'qa/asm86a';image=(W/'ASM86A.COM').read_bytes();logs=[]
class Fault(AssemblerMachine):
 def __init__(self,which):super().__init__({'SOURCE.ASM':b'RET\r\n','RESULT.COM':b'OLD'});self.which=which;self.seen={};self.fired=False
 def interrupt(self,c,number,_):
  if number!=0x21:return super().interrupt(c,number,_)
  ah=c.reg_read(UC_X86_REG_AH);bx=c.reg_read(UC_X86_REG_BX);cx=c.reg_read(UC_X86_REG_CX);dx=c.reg_read(UC_X86_REG_DX)
  self.seen[ah]=self.seen.get(ah,0)+1
  name=self.handles.get(bx,[''])[0]
  chosen=False
  if self.which=='allocate':chosen=ah==0x48
  if self.which=='partial allocation':chosen=ah==0x48 and self.seen[ah]==4
  if self.which=='resize':chosen=ah==0x4a
  if self.which=='open':chosen=ah==0x3d and self.filename(c.reg_read(UC_X86_REG_DS)*16+dx)=='SOURCE.ASM'
  if self.which=='read first pass':chosen=ah==0x3f
  if self.which=='read second pass':chosen=ah==0x3f and len([x for x in self.operations if x==('open','SOURCE.ASM')])==2
  if self.which=='create':chosen=ah==0x3c
  if self.which=='write':chosen=ah==0x40
  if self.which=='input close':chosen=ah==0x3e and name=='SOURCE.ASM'
  if self.which=='output close':chosen=ah==0x3e and name=='ASMA.TMP'
  if self.which=='first rename':chosen=ah==0x56 and self.seen[ah]==1
  if self.which=='publish rename':chosen=ah==0x56 and self.seen[ah]==2
  if self.which=='restore rename':chosen=ah==0x56 and self.seen[ah] in [2,3]
  if self.which=='backup delete':chosen=ah==0x41 and self.filename(c.reg_read(UC_X86_REG_DS)*16+dx)=='RESULT.BAK'
  if self.which=='free':chosen=ah==0x49
  if self.which=='short write' and ah==0x40 and not self.fired:
   self.fired=True;c.reg_write(UC_X86_REG_CX,cx-1);super().interrupt(c,number,_);c.reg_write(UC_X86_REG_CX,cx);return
  if chosen and (not self.fired or self.which=='restore rename'):
   self.fired=True;c.reg_write(UC_X86_REG_AX,8 if ah==0x48 else 5);self.carry(True);return
  return super().interrupt(c,number,_)
for which in ['allocate','partial allocation','resize','open','read first pass','read second pass','create','write','short write','input close','output close','first rename','publish rename','restore rename','backup delete','free']:
 r=Fault(which).run(image,limit=100_000_000)
 assert r.fired and r.exitcode==1 and b'OK RESULT.COM' not in r.output,(which,r.output)
 assert not r.allocations,(which,'memory leak')
 if which=='restore rename':assert r.files.get('RESULT.BAK')==b'OLD' and 'ASMA.TMP' in r.files and 'RESULT.COM' not in r.files
 elif which=='backup delete':assert r.files['RESULT.COM']==b'\xc3' and r.files['RESULT.BAK']==b'OLD'
 elif which=='free':assert r.files['RESULT.COM']==b'\xc3'
 else:assert r.files['RESULT.COM']==b'OLD' and 'ASMA.TMP' not in r.files,(which,r.files)
 logs.append('PASS '+which+': nonzero report, expected result/recovery state, all allocated blocks released')
class ShortRead(AssemblerMachine):
 def interrupt(self,c,number,_):
  if number==0x21 and c.reg_read(UC_X86_REG_AH)==0x3f:c.reg_write(UC_X86_REG_CX,min(c.reg_read(UC_X86_REG_CX),7))
  return super().interrupt(c,number,_)
r=ShortRead({'SOURCE.ASM':b'DB "Mixed; text",13,10\r\n'}).run(image)
assert r.exitcode==0 and r.files['RESULT.COM']==b'Mixed; text\r\n';logs.append('PASS short positive reads continue through EOF')
class ChangedSource(AssemblerMachine):
 def __init__(self,first,second):super().__init__({'SOURCE.ASM':first,'RESULT.COM':b'OLD'});self.second=second;self.opens=0
 def interrupt(self,c,number,_):
  if number==0x21 and c.reg_read(UC_X86_REG_AH)==0x3d and self.filename(c.reg_read(UC_X86_REG_DS)*16+c.reg_read(UC_X86_REG_DX))=='SOURCE.ASM':
   self.opens+=1
   if self.opens==2:self.files['SOURCE.ASM']=self.second
  return super().interrupt(c,number,_)
for first,second in [(b'X:\nDB 0\n',b'NOP\nX:\n'),(b'X:\n',b';\n')]:
 r=ChangedSource(first,second).run(image);assert r.exitcode==1 and b'CODE 3' in r.output and r.files['RESULT.COM']==b'OLD' and not r.allocations
 logs.append('PASS changed pass-two definition or missing definition preserves prior output')
(Q/'failure-results.txt').write_text('\n'.join(logs)+'\n');print('PASS',len(logs),'allocation, I/O, publication, recovery, and phase-failure checks')
