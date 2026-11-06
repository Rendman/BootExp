from common import *
from unicorn.x86_const import *
class Broken(AssemblerMachine):
 def __init__(self,files,action):super().__init__(files);self.action=action;self.used=False;self.renames=0
 def interrupt(self,c,n,_):
  if n!=0x21:return super().interrupt(c,n,_)
  ah=c.reg_read(UC_X86_REG_AH);ds=c.reg_read(UC_X86_REG_DS);dx=c.reg_read(UC_X86_REG_DX);bx=c.reg_read(UC_X86_REG_BX)
  target='';chosen=False
  if ah in [0x3d,0x3c,0x41,0x56]:target=self.filename(ds*16+dx)
  if ah==0x56:self.renames+=1
  if not self.used:
   chosen=(self.action=='result exists' and ah==0x3d and target.startswith('RESULT.')) or (self.action=='input open' and ah==0x3d and target.startswith('SOURCE.')) or (self.action=='read' and ah==0x3f and bx>=5) or (self.action=='create' and ah==0x3c) or (self.action=='write' and ah==0x40 and bx>=5) or (self.action=='close' and ah==0x3e) or (self.action=='backup rename' and ah==0x56 and self.renames==1) or (self.action=='publish rename' and ah==0x56 and self.renames==2) or (self.action=='backup delete' and ah==0x41 and target.endswith('.BAK')) or (self.action=='allocate' and ah==0x48) or (self.action=='free' and ah==0x49)
  if chosen:
   self.used=True;c.reg_write(UC_X86_REG_AX,5);self.carry(True);return
  if self.action=='short write' and not self.used and ah==0x40 and bx>=5:
   self.used=True;count=c.reg_read(UC_X86_REG_CX);c.reg_write(UC_X86_REG_CX,max(0,count-1));super().interrupt(c,n,_);c.reg_write(UC_X86_REG_CX,count);return
  if self.action=='short reads' and ah==0x3f and bx>=5:
   count=c.reg_read(UC_X86_REG_CX);c.reg_write(UC_X86_REG_CX,min(count,7));super().interrupt(c,n,_);c.reg_write(UC_X86_REG_CX,count);return
  return super().interrupt(c,n,_)
logs=[]
for name,kind,result,source in [('RILL','RIL','RESULT.IR',b'fn main(){putc(65);return 0;}'),('IR86','IR','RESULT.ASM',b'PROC MAIN 0 0\nLIT 0\nRETURN\n'),('ASM86A','ASM','RESULT.COM',b'DB 1,2,3\n')]:
 image=(W/(name+'.COM')).read_bytes();base={'SOURCE.'+kind:source,result:b'OLD'}
 normal=run(image,files=base);assert normal.exitcode==0
 actions=['result exists','input open','read','create','write','short write','close','backup rename','publish rename','backup delete']
 if name!='IR86':actions+=['allocate','free']
 for action in actions:
  r=Broken(base,action).run(image,limit=2_000_000_000)
  assert r.used and r.exitcode!=0 and b'OK ' not in r.output,(name,action,r.output)
  if action not in ['backup delete','free']:assert r.files[result]==b'OLD',(name,action,r.files.keys())
  if action=='backup delete':assert r.files[{'RILL':'RILL.BAK','IR86':'IRRES.BAK','ASM86A':'RESULT.BAK'}[name]]==b'OLD'
  assert not r.allocations,(name,action,r.allocations)
  logs.append('PASS '+name+' '+action+': no false OK, correct result/recovery state, no allocated blocks left')
 short=Broken(base,'short reads').run(image,limit=2_000_000_000);assert short.exitcode==0 and short.files[result]==normal.files[result],(name,short.output)
 logs.append('PASS '+name+' consumes short positive input reads')
 for reserved in {'RILL':['RILL.TMP','RILL.BAK'],'IR86':['IRTX.TMP','IRRES.BAK'],'ASM86A':['ASMA.TMP','RESULT.BAK']}[name]:
  f={**base,reserved:b'RECOVERY'};r=run(image,files=f);assert r.exitcode==1 and r.files[reserved]==b'RECOVERY' and r.files[result]==b'OLD' and not r.allocations,(name,reserved,r.output)
  logs.append('PASS '+name+' preserves reserved recovery file '+reserved)
(Q/'failure-results.txt').write_text('\n'.join(logs)+'\n');print('PASS',len(logs),'streaming, allocation, file-failure and recovery checks')
