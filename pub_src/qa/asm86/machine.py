"""Execute published native assemblers; model DOS services, never encode instructions."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'qa/asm0'))
from dos_machine import DosMachine,assemble
from unicorn.x86_const import *
class AssemblerMachine(DosMachine):
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.allocations={};self.next_segment=0x3000
 def interrupt(self,c,number,_):
  if number!=0x21:return super().interrupt(c,number,_)
  ah=c.reg_read(UC_X86_REG_AH);bx=c.reg_read(UC_X86_REG_BX);ds=c.reg_read(UC_X86_REG_DS);es=c.reg_read(UC_X86_REG_ES);dx=c.reg_read(UC_X86_REG_DX)
  def fail(code):c.reg_write(UC_X86_REG_AX,code);self.carry(True)
  if ah in [0x41,0x56]:
   source=self.filename(ds*16+dx)
   if source not in self.files:fail(2);return
   if any(h[0]==source for h in self.handles.values()):fail(5);return
   if ah==0x41:
    del self.files[source];self.operations.append(('delete',source));self.carry(False);return
   dest=self.filename(es*16+c.reg_read(UC_X86_REG_DI))
   if dest in self.files:fail(5);return
   self.files[dest]=self.files.pop(source);self.operations.append(('rename',source,dest));self.carry(False);return
  if ah==0x4a:
   if es!=0x1000 or bx!=0x1000:fail(9);return
   self.operations.append(('resize',es,bx));self.carry(False);return
  if ah==0x48:
   seg=self.next_segment
   if bx==0 or seg+bx>0xa000:fail(8);return
   self.allocations[seg]=bx;self.next_segment+=bx+1
   c.mem_write(seg*16,bytes([0xa5])*(bx*16))
   c.reg_write(UC_X86_REG_AX,seg);self.operations.append(('allocate',seg,bx));self.carry(False);return
  if ah==0x49:
   if es not in self.allocations:fail(9);return
   self.operations.append(('free',es,self.allocations.pop(es)));self.carry(False);return
  return super().interrupt(c,number,_)
def run_assembler(image,source=None,files=None,**kwargs):
 given=dict(files or {})
 if source is not None:given['SOURCE.ASM']=source.encode('ascii') if isinstance(source,str) else source
 return AssemblerMachine(given,**kwargs).run(image,limit=1_000_000_000)
if __name__=='__main__':
 w=ROOT/'workbench/asm86';image=(w/'ASMA0.COM').read_bytes();source=(w/'ASMA0.ASM').read_bytes()
 first=run_assembler(image,source);print(first.exitcode,first.output);assert first.exitcode==0
 assert first.files['RESULT.COM']==image,'seed self-build differs'
 second=run_assembler(first.files['RESULT.COM'],source);assert second.exitcode==0 and second.files['RESULT.COM']==image
 for text,expected in [('MOV AX,ES\nMOV ES,BX\n',bytes.fromhex('8CC0 8EC3')),('MOV AX,ES:[BX]\nMOV ES:[1234H],DX\n',bytes.fromhex('26 8B07 26 8916 3412'))]:
  r=run_assembler(image,text);print(r.output,r.files.get('RESULT.COM'));assert r.exitcode==0 and r.files['RESULT.COM']==expected
 print('PASS seed direct build, two self-builds, and segment encodings')
