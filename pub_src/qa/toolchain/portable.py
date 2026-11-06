"""Processor-independent IR execution. This model never emits bootstrap source or bytes."""
from dataclasses import dataclass,field
class InvalidIR(ValueError):pass

def literal(text):
 text=text.strip();out=bytearray();i=1
 if not text.startswith('"'):raise InvalidIR('Expected quoted literal')
 escapes={'n':10,'r':13,'t':9,'0':0,'"':34,'\\':92}
 while i<len(text):
  c=text[i];i+=1
  if c=='"':
   if text[i:].strip() and not text[i:].lstrip().startswith(';'):raise InvalidIR('Literal tail')
   return bytes(out)+b'\0'
  if c=='\\':
   if i==len(text) or text[i] not in escapes:raise InvalidIR('Invalid escape')
   out.append(escapes[text[i]]);i+=1
  else:out.append(ord(c))
 raise InvalidIR('Unterminated literal')
@dataclass
class Machine:
 files:dict=field(default_factory=dict)
 stdin:bytes=b''
 data_base:int=0x2000
 handle_base:int=101
 block_base:int=501
 write_limit:int|None=None
 def __post_init__(self):
  self.files={k.upper():bytes(v) for k,v in self.files.items()};self.output=bytearray();self.exitcode=None
  self.memory=bytearray(65536);self.static_end=self.data_base;self.a=0;self.status=0;self.stack=[];self.calls=[];self.frame=None
  self.handles={};self.blocks={};self.input_position=0;self.frame_top=0xe000;self.code=[];self.labels={};self.objects={};self.procs={};self.literals={}
 def access(self,p,n):
  if n==0:return
  static=self.data_base<=p and p+n<=self.static_end
  frame=any(a<=p and p+n<=b for a,b in ([self.frame['range']] if self.frame else [])+[f['range'] for _,_,f in self.calls if f])
  if p<0 or p+n>65536 or not (static or frame):raise InvalidIR(f'Invalid byte range {p:04x}+{n}')
 def word(self,p):self.access(p,2);return self.memory[p]+256*self.memory[p+1]
 def store(self,p,v,n):self.access(p,n);self.memory[p:p+n]=(v&((1<<(n*8))-1)).to_bytes(n,'little')
 def alloc_static(self,b):
  p=self.static_end;self.static_end+=len(b)
  if self.static_end>0xb000:raise InvalidIR('Static data profile')
  self.memory[p:self.static_end]=b;return p
 def string(self,p):
  b=bytearray()
  for i in range(128):
   self.access(p+i,1);c=self.memory[p+i]
   if c==0:return b.decode('ascii').upper()
   b.append(c)
  raise InvalidIR('File name extent')
 def pop(self):
  if not self.stack:raise InvalidIR('Expression underflow')
  return self.stack.pop()
 def enter(self,name,args):
  spec=self.procs.get(name)
  if spec is None:
   if args:raise InvalidIR('Arguments without procedure')
   return None
  argc,n=spec
  if argc!=len(args):raise InvalidIR('Arity mismatch')
  end=self.frame_top;start=end-2*(n+argc)
  if start<0xc000:raise InvalidIR('Frame capacity')
  self.frame_top=start
  self.memory[start:end]=b'\xa5'*(end-start)
  for i,v in enumerate(args):self.memory[start+i*2:start+i*2+2]=v.to_bytes(2,'little')
  return {'range':(start,end),'args':start,'locals':start+argc*2,'argc':argc,'count':n}
 def service(self,op):
  self.status=0
  if op=='PUTC':self.output.append(self.a&255);self.a=1;return
  if op=='GETC':
   self.a=65535 if self.input_position==len(self.stdin) else self.stdin[self.input_position]
   if self.a!=65535:self.input_position+=1
   return
  if op in ['OPEN','CREATE','EXISTS','DELETE','RENAME']:
   name=self.string(self.a)
   if op=='EXISTS':self.a=int(name in self.files);return
   if op=='DELETE':
    if name not in self.files or any(h[0]==name for h in self.handles.values()):self.a=0;self.status=1;return
    del self.files[name];self.a=0;return
   if op=='RENAME':
    old=self.string(self.pop())
    if old not in self.files or name in self.files or any(h[0] in [old,name] for h in self.handles.values()):self.a=0;self.status=1;return
    self.files[name]=self.files.pop(old);self.a=0;return
   if len(self.handles)==8 or (op=='OPEN' and name not in self.files):self.a=0;self.status=1;return
   h=next(self.handle_base+i*3 for i in range(8) if self.handle_base+i*3 not in self.handles)
   if op=='CREATE':self.files[name]=b''
   self.handles[h]=[name,0,op=='CREATE'];self.a=h;return
  if op=='CLOSE':
   if self.a not in self.handles:self.a=0;self.status=1;return
   del self.handles[self.a];self.a=0;return
  if op in ['READ','WRITE']:
   p=self.pop();h=self.pop();n=self.a;entry=self.handles.get(h)
   if entry is None or entry[2]!=(op=='WRITE'):self.a=0;self.status=1;return
   name,at,_=entry
   if op=='READ':
    b=self.files[name][at:at+n];self.access(p,len(b));self.memory[p:p+len(b)]=b;self.a=len(b)
   else:
    self.access(p,n);actual=n if self.write_limit is None else min(n,self.write_limit)
    b=bytes(self.memory[p:p+actual]);old=self.files[name];self.files[name]=old[:at]+b+old[at+len(b):];self.a=actual
    if actual!=n:self.status=1
   entry[1]+=self.a;return
  if op=='ALLOC':
   if self.a==0 or len(self.blocks)==16:self.a=0;self.status=1;return
   h=next(self.block_base+i*7 for i in range(16) if self.block_base+i*7 not in self.blocks)
   self.blocks[h]=bytearray(b'\xa5'*self.a);self.a=h;return
  if op=='FREEBLOCK':
   if self.a not in self.blocks:self.a=0;self.status=1;return
   del self.blocks[self.a];self.a=0;return
  if op in ['GET8','GET16','SET8','SET16']:
   width=1 if op.endswith('8') else 2
   if op.startswith('SET'):v=self.a;p=self.pop();h=self.pop()
   else:p=self.a;h=self.pop()
   b=self.blocks.get(h)
   if b is None or p+width>len(b):self.a=0;self.status=1;return
   if op.startswith('SET'):b[p:p+width]=(v&((1<<(width*8))-1)).to_bytes(width,'little');self.a=v
   else:self.a=int.from_bytes(b[p:p+width],'little')
   return
  raise InvalidIR('Unknown service '+op)
 def run(self,source,limit=50_000_000):
  if isinstance(source,bytes):source=source.decode('ascii')
  for raw in source.split('\x1a',1)[0].splitlines():
   raw=raw.strip()
   if not raw or raw.startswith(';'):continue
   op,_,tail=raw.partition(' ');op=op.upper()
   if op=='LITS':self.literals[len(self.code)]=self.alloc_static(literal(tail));args=[]
   else:args=tail.split(';',1)[0].upper().split()
   if op in ['WORD','BYTE','BUFFER']:
    name,num=args;num=int(num[:-1],16) if num.endswith('H') else int(num)
    if name in self.objects or name in self.labels:raise InvalidIR('Duplicate symbol')
    b=bytes(num) if op=='BUFFER' else num.to_bytes(2 if op=='WORD' else 1,'little')
    self.objects[name]=self.alloc_static(b);continue
   if op in ['LABEL','PROC']:
    if args[0] in self.labels or args[0] in self.objects:raise InvalidIR('Duplicate label')
    self.labels[args[0]]=len(self.code)
    if op=='PROC':self.procs[args[0]]=tuple(map(int,args[1:]))
   self.code.append((op,args))
  if 'MAIN' not in self.labels:raise InvalidIR('Missing MAIN')
  pc=self.labels['MAIN'];self.frame=self.enter('MAIN',[])
  for count in range(limit):
   if pc>=len(self.code):raise InvalidIR('Fall through')
   location=pc;op,args=self.code[pc];pc+=1
   if op in ['LABEL','PROC','NOP']:continue
   if op=='LIT':self.a=int(args[0][:-1],16) if args[0].endswith('H') else int(args[0])
   elif op=='LITS':self.a=self.literals[location]
   elif op=='ADDR':self.a=self.objects[args[0]]
   elif op in ['LD','LDB']:
    p=self.objects[args[0]];self.a=self.word(p) if op=='LD' else self.memory[p]
   elif op in ['ST','STB']:self.store(self.objects[args[0]],self.a,2 if op=='ST' else 1)
   elif op in ['LOCAL','SETLOCAL','LADDR','PARAM','SETPARAM','PADDR']:
    frame=self.frame;i=int(args[0]);param=op in ['PARAM','SETPARAM','PADDR']
    if frame is None or i>=(frame['argc'] if param else frame['count']):raise InvalidIR('Frame index')
    p=frame['args' if param else 'locals']+i*2
    if op in ['LADDR','PADDR']:self.a=p
    elif op.startswith('SET'):self.store(p,self.a,2)
    else:self.a=self.word(p)
   elif op in ['FETCH','FETCHB']:
    self.access(self.a,2 if op=='FETCH' else 1);self.a=self.word(self.a) if op=='FETCH' else self.memory[self.a]
   elif op in ['PUT','PUTB']:self.store(self.pop(),self.a,2 if op=='PUT' else 1)
   elif op=='PUSH':
    if len(self.stack)==256:raise InvalidIR('Expression capacity')
    self.stack.append(self.a)
   elif op=='POP':self.a=self.pop()
   elif op in ['NEG','NOT']:self.a=(-self.a if op=='NEG' else ~self.a)&65535
   elif op in ['ADD','SUB','MUL','DIV','MOD','AND','OR','XOR','SHL','SHR']:
    a=self.pop();b=self.a
    if op in ['DIV','MOD'] and b==0:self.exitcode=2;return self
    self.a={'ADD':lambda:a+b,'SUB':lambda:a-b,'MUL':lambda:a*b,'DIV':lambda:a//b,'MOD':lambda:a%b,'AND':lambda:a&b,'OR':lambda:a|b,'XOR':lambda:a^b,'SHL':lambda:a<<(b&15),'SHR':lambda:a>>(b&15)}[op]()&65535
   elif op in ['JMP','JZ','JNZ']:
    if self.stack:raise InvalidIR('Branch boundary')
    if op=='JMP' or (op=='JZ' and self.a==0) or (op=='JNZ' and self.a!=0):pc=self.labels[args[0]]
   elif op in ['EQ','NE','ULT','ULE','UGT','UGE','SLT','SLE','SGT','SGE'] or op.startswith('C') and op[1:] in ['EQ','NE','ULT','ULE','UGT','UGE','SLT','SLE','SGT','SGE']:
    val=op.startswith('C');condition=op[1:] if val else op;a=self.pop();b=self.a
    if condition.startswith('S'):a=a if a<32768 else a-65536;b=b if b<32768 else b-65536
    rel=condition if condition in ['EQ','NE'] else condition[1:]
    yes={'EQ':a==b,'NE':a!=b,'LT':a<b,'LE':a<=b,'GT':a>b,'GE':a>=b}[rel]
    if not val and self.stack:raise InvalidIR('Comparison branch boundary')
    if val:self.a=int(yes)
    elif yes:pc=self.labels[args[0]]
   elif op in ['CALL','INVOKE']:
    n=int(args[1]) if op=='INVOKE' else 0
    if n>len(self.stack):raise InvalidIR('Argument underflow')
    argv=self.stack[-n:] if n else []
    if n:del self.stack[-n:]
    self.calls.append((pc,self.stack,self.frame));self.stack=[];self.frame=self.enter(args[0],argv);pc=self.labels[args[0]]
   elif op in ['RET','RETURN']:
    if self.stack:raise InvalidIR('Return boundary')
    if self.frame:self.frame_top=self.frame['range'][1]
    if not self.calls:self.exitcode=self.a&255;return self
    pc,self.stack,self.frame=self.calls.pop()
   elif op=='STATUS':self.a=self.status
   elif op in ['PUTC','GETC','OPEN','CREATE','READ','WRITE','CLOSE','EXISTS','DELETE','RENAME','ALLOC','FREEBLOCK','GET8','GET16','SET8','SET16']:self.service(op)
   elif op in ['HALT','EXIT']:self.exitcode=0 if op=='HALT' else self.a&255;return self
   else:raise InvalidIR('Unknown IR '+op)
  raise InvalidIR('Execution limit')
