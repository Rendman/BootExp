"""Executable IR contract, with no processor registers, flags, DOS, or code generation.
Data addresses and file-handle values intentionally differ from the native binding.
This validation interpreter never supplies an executable to the bootstrap chain.
"""
from dataclasses import dataclass,field
import re
class InvalidIR(ValueError):pass
@dataclass
class Machine:
 files:dict=field(default_factory=dict)
 stdin:bytes=b''
 data_base:int=0x4000
 handle_base:int=101
 write_limit:int|None=None
 def __post_init__(self):
  self.files={k.upper():bytes(v) for k,v in self.files.items()}
  self.a=0;self.stack=[];self.calls=[];self.io_status=0;self.output=bytearray();self.exitcode=None
  self.handles={};self.input_position=0;self.memory=bytearray(65536);self.objects={};self.labels={}
  self.code=[];self.data_end=self.data_base
 def access(self,address,count):
  if count and not self.data_base<=address<=address+count<=self.data_end:raise InvalidIR('Access outside declared storage')
 def word(self,address):self.access(address,2);return int.from_bytes(self.memory[address:address+2],'little')
 def store(self,address,value,size):self.access(address,size);self.memory[address:address+size]=(value&((1<<(8*size))-1)).to_bytes(size,'little')
 def string(self,address):
  value=bytearray()
  for i in range(256):
   self.access(address+i,1);b=self.memory[address+i]
   if b==0:return value.decode('ascii').upper()
   value.append(b)
  raise InvalidIR('Unterminated file name')
 def pop(self):
  if not self.stack:raise InvalidIR('Expression stack underflow')
  return self.stack.pop()
 def empty(self):
  if self.stack:raise InvalidIR('Nonempty expression boundary')
 def service(self,op):
  self.io_status=0
  if op=='PUTC':self.empty();self.output.append(self.a&255);self.a=1;return
  if op=='GETC':
   self.empty()
   if self.input_position==len(self.stdin):self.a=65535
   else:self.a=self.stdin[self.input_position];self.input_position+=1
   return
  if op in ['OPEN','CREATE']:
   self.empty();name=self.string(self.a)
   if not name or (op=='OPEN' and name not in self.files) or len(self.handles)>=8:self.a=0;self.io_status=1;return
   h=next(self.handle_base+3*i for i in range(8) if self.handle_base+3*i not in self.handles)
   if op=='CREATE':self.files[name]=b''
   self.handles[h]=[name,0,'read' if op=='OPEN' else 'write'];self.a=h;return
  if op=='CLOSE':
   self.empty()
   if self.a not in self.handles:self.a=0;self.io_status=1;return
   del self.handles[self.a];self.a=0;return
  address=self.pop();handle=self.pop();self.empty();count=self.a
  entry=self.handles.get(handle)
  if entry is None or entry[2]!=('read' if op=='READ' else 'write'):self.a=0;self.io_status=1;return
  name,position,mode=entry
  if op=='READ':
   raw=self.files[name][position:position+count];self.access(address,len(raw))
   self.memory[address:address+len(raw)]=raw;self.a=len(raw)
  else:
   actual=count if self.write_limit is None else min(count,self.write_limit)
   self.access(address,count);raw=bytes(self.memory[address:address+actual]);old=self.files[name]
   self.files[name]=old[:position]+raw+old[position+len(raw):];self.a=len(raw)
   if actual!=count:self.io_status=1
  entry[1]+=self.a
 def run(self,source,limit=1_000_000):
  if isinstance(source,bytes):source=source.decode('ascii')
  lines=source.split('\x1a',1)[0].replace('\r\n','\n').replace('\r','\n').splitlines()
  for raw in lines:
   words=raw.split(';',1)[0].upper().split()
   if not words:continue
   op,*args=words
   if op in ['WORD','BYTE','BUFFER']:
    name,value=args;n=int(value[:-1],16) if value.endswith('H') else int(value)
    if name in self.objects or name in self.labels:raise InvalidIR('Duplicate name')
    size=n if op=='BUFFER' else 2 if op=='WORD' else 1
    self.objects[name]=self.data_end
    if op!='BUFFER':self.store_new(self.data_end,n,size)
    self.data_end+=size
   else:
    if op=='LABEL':
     if args[0] in self.labels or args[0] in self.objects:raise InvalidIR('Duplicate name')
     self.labels[args[0]]=len(self.code)
    self.code.append((op,args))
  if 'MAIN' not in self.labels:raise InvalidIR('Missing MAIN')
  pc=self.labels['MAIN'];count=0
  while pc<len(self.code):
   count+=1
   if count>limit:raise InvalidIR('Execution limit')
   op,args=self.code[pc];pc+=1
   if op=='LABEL':self.empty()
   elif op=='NOP':pass
   elif op=='LIT':self.a=int(args[0][:-1],16) if args[0].endswith('H') else int(args[0])
   elif op=='ADDR':self.a=self.objects[args[0]]
   elif op in ['LD','LDB']:
    p=self.objects[args[0]];self.access(p,2 if op=='LD' else 1);self.a=self.word(p) if op=='LD' else self.memory[p]
   elif op in ['ST','STB']:self.store(self.objects[args[0]],self.a,2 if op=='ST' else 1)
   elif op in ['FETCH','FETCHB']:
    p=self.a;self.access(p,2 if op=='FETCH' else 1);self.a=self.word(p) if op=='FETCH' else self.memory[p]
   elif op in ['PUT','PUTB']:self.store(self.pop(),self.a,2 if op=='PUT' else 1)
   elif op=='PUSH':
    if len(self.stack)==32:raise InvalidIR('Expression capacity')
    self.stack.append(self.a)
   elif op=='POP':self.a=self.pop()
   elif op in ['ADD','SUB','AND','OR','XOR']:
    left=self.pop();self.a={'ADD':lambda:(left+self.a)&65535,'SUB':lambda:(left-self.a)&65535,'AND':lambda:left&self.a,'OR':lambda:left|self.a,'XOR':lambda:left^self.a}[op]()
   elif op in ['JMP','JZ','JNZ']:
    self.empty()
    if op=='JMP' or (op=='JZ' and self.a==0) or (op=='JNZ' and self.a!=0):pc=self.labels[args[0]]
   elif op in ['EQ','NE','ULT','ULE','UGT','UGE','SLT','SLE','SGT','SGE']:
    left=self.pop();self.empty();right=self.a
    if op.startswith('S'):left=left if left<32768 else left-65536;right=right if right<32768 else right-65536
    kind=op if op in ['EQ','NE'] else op[1:]
    if {'EQ':left==right,'NE':left!=right,'LT':left<right,'LE':left<=right,'GT':left>right,'GE':left>=right}[kind]:pc=self.labels[args[0]]
   elif op=='CALL':self.empty();self.calls.append(pc);pc=self.labels[args[0]]
   elif op=='RET':
    self.empty()
    if not self.calls:raise InvalidIR('Return without call')
    pc=self.calls.pop()
   elif op=='STATUS':self.a=self.io_status
   elif op in ['PUTC','GETC','OPEN','CREATE','READ','WRITE','CLOSE']:self.service(op)
   elif op in ['HALT','EXIT']:self.empty();self.exitcode=0 if op=='HALT' else self.a&255;return self
   else:raise InvalidIR('Unknown operation '+op)
  self.empty();self.exitcode=0;return self
 def store_new(self,address,value,size):self.memory[address:address+size]=(value&((1<<(8*size))-1)).to_bytes(size,'little')
