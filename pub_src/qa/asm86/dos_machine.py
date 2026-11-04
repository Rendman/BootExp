"""Execute BASIC-produced 8086 COM files with documented DOS file services.
This module never translates assembly source or constructs instruction bytes.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/python'))
from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_INTR
from unicorn.x86_const import *
class DosMachine:
 def __init__(self,files=None,inputs=(),sp=0xfffe,stdin=b''):
  self.files={k.upper():bytes(v) for k,v in (files or {}).items()}
  self.inputs=list(inputs);self.output=bytearray();self.exitcode=None
  self.handles={};self.next_handle=5;self.operations=[];self.sp=sp
  self.stdin=bytes(stdin);self.stdin_position=0
 def run(self,image,limit=100_000_000):
  c=Uc(UC_ARCH_X86,UC_MODE_16);self.cpu=c;c.mem_map(0,0x100000)
  self.base=0x10000
  c.mem_write(self.base,b'\xcd\x20\x00\x20')
  c.mem_write(self.base+0x100,image)
  for r in [UC_X86_REG_AX,UC_X86_REG_BX,UC_X86_REG_CX,UC_X86_REG_DX,UC_X86_REG_SI,UC_X86_REG_DI,UC_X86_REG_BP]:c.reg_write(r,0xbeef)
  for r in [UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_ES,UC_X86_REG_SS]:c.reg_write(r,0x1000)
  c.reg_write(UC_X86_REG_SP,self.sp);c.reg_write(UC_X86_REG_EFLAGS,0x602)
  c.mem_write(self.base+self.sp,b'\0\0')
  c.hook_add(UC_HOOK_INTR,self.interrupt)
  c.emu_start(self.base+0x100,self.base+0x10000,count=limit)
  if self.exitcode is None:raise AssertionError(f'COM did not terminate; IP={c.reg_read(UC_X86_REG_IP):04X}, output={self.output!r}')
  return self
 def carry(self,value):
  flags=self.cpu.reg_read(UC_X86_REG_EFLAGS)
  self.cpu.reg_write(UC_X86_REG_EFLAGS,(flags|1) if value else (flags&~1))
 def filename(self,address):
  raw=bytearray()
  for offset in range(128):
   ch=self.cpu.mem_read(address+offset,1)[0]
   if ch==0:return raw.decode('ascii').upper()
   raw.append(ch)
  raise AssertionError('Unterminated DOS filename')
 def interrupt(self,c,number,_):
  if number==0x20:self.exitcode=0;c.emu_stop();return
  assert number==0x21,f'Unexpected interrupt {number:02X}'
  ah=c.reg_read(UC_X86_REG_AH);ax=c.reg_read(UC_X86_REG_AX)
  bx=c.reg_read(UC_X86_REG_BX);cx=c.reg_read(UC_X86_REG_CX);dx=c.reg_read(UC_X86_REG_DX)
  address=c.reg_read(UC_X86_REG_DS)*16+dx
  if ah==2:
   self.output.append(dx&255);c.reg_write(UC_X86_REG_AL,dx&255);return
  if ah==9:
   for i in range(65536):
    ch=c.mem_read(address+i,1)[0]
    if ch==36:c.reg_write(UC_X86_REG_AL,36);return
    self.output.append(ch)
   raise AssertionError('Unterminated DOS message')
  if ah==10:
   if not self.inputs:raise AssertionError('Program requested unexpected console input')
   raw=self.inputs.pop(0).encode('ascii');maximum=c.mem_read(address,1)[0]
   raw=raw[:max(0,maximum-1)]
   c.mem_write(address+1,bytes([len(raw)])+raw+b'\r')
   self.output.extend(raw+b'\r');return
  if ah==0x4c:
   self.exitcode=ax&255;c.emu_stop();return
  if ah in [0x3c,0x3d]:
   name=self.filename(address);self.operations.append(('create' if ah==0x3c else 'open',name))
   if ah==0x3d and name not in self.files:
    c.reg_write(UC_X86_REG_AX,2);self.carry(True);return
   if ah==0x3c:self.files[name]=b''
   handle=self.next_handle;self.next_handle+=1
   self.handles[handle]=[name,0,ah==0x3c]
   c.reg_write(UC_X86_REG_AX,handle);self.carry(False);return
  if ah==0x3e:
   if bx not in self.handles:
    c.reg_write(UC_X86_REG_AX,6);self.carry(True);return
   del self.handles[bx];self.carry(False);return
  if ah in [0x3f,0x40]:
   if ah==0x3f and bx==0:
    raw=self.stdin[self.stdin_position:self.stdin_position+cx]
    if raw:c.mem_write(address,raw)
    self.stdin_position+=len(raw);c.reg_write(UC_X86_REG_AX,len(raw));self.carry(False);return
   if ah==0x40 and bx in [1,2]:
    self.output.extend(c.mem_read(address,cx));c.reg_write(UC_X86_REG_AX,cx);self.carry(False);return
   if bx not in self.handles:
    c.reg_write(UC_X86_REG_AX,6);self.carry(True);return
   name,position,writable=self.handles[bx]
   if ah==0x3f:
    raw=self.files[name][position:position+cx]
    if raw:c.mem_write(address,raw)
    amount=len(raw)
   else:
    if not writable:
     c.reg_write(UC_X86_REG_AX,5);self.carry(True);return
    raw=bytes(c.mem_read(address,cx));old=self.files[name]
    self.files[name]=old[:position]+raw+old[position+len(raw):]
    amount=len(raw)
   self.handles[bx][1]+=amount
   c.reg_write(UC_X86_REG_AX,amount);self.carry(False);return
  raise AssertionError(f'Unexpected DOS function {ah:02X}')
def assemble(image,source,stem='TRY',old=None,**kwargs):
 files={stem+'.ASM':source.encode('ascii') if isinstance(source,str) else source}
 if old is not None:files[stem+'.COM']=old
 return DosMachine(files,[stem],**kwargs).run(image)
