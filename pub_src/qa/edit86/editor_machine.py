"""BIOS surface model for executing the actual RILL-built screen editor."""
from services import ROOT
import sys
sys.path.insert(0,str(ROOT/'qa/asm86'))
from machine import AssemblerMachine
from unicorn.x86_const import *
class EditorMachine(AssemblerMachine):
 def __init__(self,files=None,keys=(),mode=3,**kwargs):
  super().__init__(files,**kwargs);self.keys=list(keys);self.mode=mode;self.cursor=0;self.shape=0x607;self.screen_log=[];self.key_count=0
 def interrupt(self,c,num,unused):
  if num==0x16:
   assert self.keys,'Editor requested an unexpected key'
   key=self.keys.pop(0);self.key_count+=1
   if callable(key):key=key(self)
   self.screen_log.append(bytes(c.mem_read((0xb000 if self.mode==7 else 0xb800)*16,4000))[::2])
   c.reg_write(UC_X86_REG_AX,key);return
  if num!=0x10:return super().interrupt(c,num,unused)
  ah=c.reg_read(UC_X86_REG_AH);cx=c.reg_read(UC_X86_REG_CX);dx=c.reg_read(UC_X86_REG_DX)
  if ah==0x0f:c.reg_write(UC_X86_REG_AX,80*256+self.mode);c.reg_write(UC_X86_REG_BH,0);return
  if ah==3:
   c.reg_write(UC_X86_REG_CX,self.shape);c.reg_write(UC_X86_REG_DX,(self.cursor//80)*256+self.cursor%80);return
  if ah==1:self.shape=cx;return
  if ah==2:
   row,col=dx>>8,dx&255;assert row<25 and col<80,(row,col)
   self.cursor=row*80+col;return
  if ah==6:
   address=(0xb000 if self.mode==7 else 0xb800)*16
   c.mem_write(address,bytes([32,7])*2000);return
  raise AssertionError(('unsupported BIOS video function',ah))
def key(event):
 scans={256:75,257:77,258:72,259:80,260:71,261:79,262:73,263:81,264:83,265:60,266:68,267:62,268:61,269:63,270:64,271:65}
 return scans[event]*256 if event>=256 else event
