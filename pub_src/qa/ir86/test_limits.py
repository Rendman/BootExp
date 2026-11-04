"""Check portable IR semantics and the actual 8086/DOS binding independently."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/ir86';Q=ROOT/'qa/ir86'
sys.path.insert(0,str(ROOT/'qa/asm86'))
from dos_machine import DosMachine,assemble
from portable_machine import Machine,InvalidIR
from unicorn.x86_const import UC_X86_REG_AH,UC_X86_REG_AX,UC_X86_REG_BX,UC_X86_REG_CX
IR=(W/'IR86.COM').read_bytes();ASM=(ROOT/'workbench/asm86/ASM86.COM').read_bytes();results=[]
profile=json.loads((Q/'runtime-sizes.json').read_text())['30']
def translate(source):return DosMachine({'TEST.IR':source.encode() if isinstance(source,str) else source,'TEST.ASM':b'OLD'},['TEST']).run(IR)
def build(source):
 t=translate(source);assert t.exitcode==0,t.output
 assert t.operations==[('open','TEST.IR'),('create','TEST.ASM')],t.operations
 a=assemble(ASM,t.files['TEST.ASM'],'TEST');assert a.exitcode==0,(a.output,t.files['TEST.ASM'])
 return a.files['TEST.COM']
def run(label,source,status=0,output=b'',files=None,stdin=b''):
 native=DosMachine(files,stdin=stdin).run(build(source))
 for base,handle in [(0x4000,101),(0x8000,301)]:
  portable=Machine(files or {},stdin,data_base=base,handle_base=handle).run(source)
  assert (native.exitcode,native.output,native.files)==(portable.exitcode,portable.output,portable.files),(label,'portable behavior differs')
 assert native.exitcode==status and native.output==output,(label,native.output,native.exitcode)
 results.append('PASS '+label);return native
def bad(label,source,code):
 t=translate(source);assert t.exitcode==1 and f'CODE {code}'.encode() in t.output,(label,t.output)
 assert t.files['TEST.ASM']==b'OLD' and not any(o[0]=='create' for o in t.operations),label
 results.append('PASS '+label)
def name(label,value):return ''.join(f'BYTE {label}{i} {b}\n' for i,b in enumerate(value.encode()+b'\0'))
def branch(a,b,op):return f'LABEL MAIN\nLIT {a}\nPUSH\nLIT {b}\n{op} GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n'
for op,fn in [('ADD',lambda a,b:(a+b)&65535),('SUB',lambda a,b:(a-b)&65535),('AND',lambda a,b:a&b),('OR',lambda a,b:a|b),('XOR',lambda a,b:a^b)]:
 for a,b in [(7,3),(0,1),(65535,1),(32768,32768),(21845,43690)]:
  src=f'LABEL MAIN\nLIT {a}\nPUSH\nLIT {b}\n{op}\nPUSH\nLIT {fn(a,b)}\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n'
  run(f'{op} word semantics {a},{b}',src)
def signed(n):return n if n<32768 else n-65536
for op in ['EQ','NE','ULT','ULE','UGT','UGE','SLT','SLE','SGT','SGE']:
 for a,b in [(0,1),(1,0),(65535,0),(32768,32767),(32767,32768),(65535,65535)]:
  x,y=(signed(a),signed(b)) if op.startswith('S') else (a,b)
  truth={'EQ':x==y,'NE':x!=y,'LT':x<y,'LE':x<=y,'GT':x>y,'GE':x>=y}[op if op in ['EQ','NE'] else op[1:]]
  run(f'{op} {a},{b}',branch(a,b,op),0 if truth else 1)
for op,zero in [('JZ',True),('JNZ',False)]:
 for value in [0,65535]:run(f'{op} {value}',f'LABEL MAIN\nLIT {value}\n{op} GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n',0 if (value==0)==zero else 1)
run('LIFO order','LABEL MAIN\nLIT 7\nPUSH\nLIT 3\nPUSH\nPOP\nPOP\nPUSH\nLIT 7\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
run('word fetch/store','BUFFER DATA 4\nLABEL MAIN\nADDR DATA\nPUSH\nLIT 4660\nPUT\nADDR DATA\nFETCH\nPUSH\nLIT 4660\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
run('canonical word byte order','WORD DATA 4660\nLABEL MAIN\nADDR DATA\nFETCHB\nPUSH\nLIT 52\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
for op in ['LDB DATA','ADDR DATA\nFETCHB']:run('zero extension '+op,'BYTE DATA 0\nLABEL MAIN\nLIT 65535\n'+op+'\nJZ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
run('byte store retains value','BYTE DATA 0\nLABEL MAIN\nLIT 65535\nSTB DATA\nPUSH\nLIT 65535\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
run('nested abstract calls','LABEL MAIN\nCALL OUTER\nEXIT\nLABEL OUTER\nCALL INNER\nRET\nLABEL INNER\nLIT 0\nRET\n')
run('empty body and initial status','LABEL MAIN\nSTATUS\nEXIT\n')
run('case tabs and EOF','word\tax\t0 ;note\rlabel main\nld ax\r\nexit\x1aUNKNOWN')
run('full name length','WORD ABCDEFGHIJKLMN 0\nLABEL MAIN\nLD ABCDEFGHIJKLMN\nEXIT\n')
run('32 expression words','LABEL MAIN\nLIT 0\n'+'PUSH\n'*32+'POP\n'*32+'EXIT\n')
bad('33 expression words','LABEL MAIN\nLIT 0\n'+'PUSH\n'*33,5)
for end in ['HALT','EXIT','RET','JMP MAIN','CALL MAIN','JZ MAIN','JNZ MAIN','PUTC','GETC','OPEN','CREATE','CLOSE','LABEL MORE']:bad('nonempty boundary '+end,'LABEL MAIN\nLIT 1\nPUSH\n'+end+'\n',4)
for op in ['POP','ADD','SUB','AND','OR','XOR','PUT','PUTB','EQ MAIN','SLT MAIN','READ','WRITE']:bad('underflow '+op,'LABEL MAIN\n'+op+'\n',4)
bad('transfer leaves unrelated temporary','LABEL MAIN\nLIT 1\nPUSH\nPUSH\nPUSH\nREAD\n',4)
for op in ['TOBX','TOCX','TODX','FROMBX','FROMCX','FROMDX','DOS','JC MAIN','JNC MAIN','INT 21H','MOV AX,1']:bad('no processor escape '+op,'LABEL MAIN\n'+op+'\n',1)
for text,error in [('',3),('HALT',1),('LABEL ELSE',3),('WORD X 0',3),('LABEL MAIN\nWORD X 0',1),('LABEL MAIN\nNOP 1',1),('LABEL MAIN\nLIT 65536',2),('LABEL MAIN\nLIT -1',2),('LABEL MAIN\nLIT X',2),('LABEL MAIN\nLIT 0GH',2),('LABEL MAIN\nLIT 1+2',2),('BYTE X 256',4),('BUFFER X 0',4),('BUFFER X 257',4),('WORD 1BAD 0',3),('WORD ABCDEFGHIJKLMNO 0',3),('LABEL MAIN\nLD A+B',3)]:bad('reject '+repr(text),text,error)
for value in [0,1,27,127,128,255]:bad('invalid source byte '+str(value),b'LABEL MAIN\n'+bytes([value]),6)
run('120 physical characters',';'+'X'*119+'\nLABEL MAIN\nHALT\n')
bad('121 physical characters',';'+'X'*120+'\nLABEL MAIN\nHALT\n',5)
bad('4001 source lines',';\n'*4001,5)
bad('assembly-text capacity','LABEL MAIN\n'+('LIT '+'0'*16+'\n')*1400,5)
# The target profile reserves runtime resources, rather than changing IR semantics.
from importlib.util import spec_from_file_location,module_from_spec
spec=spec_from_file_location('rt',ROOT/'tools/ir86_runtime_text.py');rt=module_from_spec(spec);spec.loader.exec_module(rt)
line_count=len(rt.runtime(30).splitlines())
nop_count=4000-8-2-line_count
run('exact generated line capacity','LABEL MAIN\n'+'NOP\n'*nop_count)
bad('generated line capacity overflow','LABEL MAIN\n'+'NOP\n'*(nop_count+1),5)
user_defs=256-1-profile['definitions']
names='LABEL MAIN\n'+''.join(f'LABEL L{i}\n' for i in range(user_defs-1))
run('exact backend definition capacity',names+'HALT\n')
bad('backend definition capacity overflow',names+'LABEL EXTRA\nHALT\n',5)
branches=256-1-profile['definitions']-2
run('conditional skip accounting','LABEL MAIN\nLIT 0\n'+'JZ GOOD\n'*branches+'LABEL GOOD\nHALT\n')
room=8192-15-5-profile['bytes'];full,tail=divmod(room,256)
data=''.join(f'BUFFER B{i} 256\n' for i in range(full))+(f'BUFFER LAST {tail}\n' if tail else '')
code=build(data+'LABEL MAIN\nHALT\n');assert len(code)==8192
assert DosMachine().run(code).exitcode==0;results.append('PASS exact native image capacity including runtime')
bad('native image overflow',data.replace(f'BUFFER LAST {tail}',f'BUFFER LAST {tail+1}')+'LABEL MAIN\nHALT\n',5)
# Stream behavior, including the byte 255 versus the EOF word 65535.
echo=(W/'ECHOIR.IR').read_text()
for raw in [b'',b'Q',bytes(range(256)),b'A\r\nB\x00\xff']:run('byte stream '+repr(raw[:8]),echo,output=raw,stdin=raw)
copy=(W/'COPYFILE.IR').read_text()
for raw in [b'',b'ABC\r\n',bytes(range(256))]:
 m=run('portable file copy '+str(len(raw)),copy,files={'IN.TXT':raw,'OUT.TXT':b'old tail'});assert m.files['OUT.TXT']==raw
run('missing input normalized',copy,1,files={'OUT.TXT':b'old'})
# STATUS is ordinary data and survives computations which change native flags.
for file,expected in [('PRESENT',0),('MISSING',1)]:
 src=name('F',file)+'WORD H 0\nLABEL MAIN\nADDR F0\nOPEN\nST H\nLIT 0\nPUSH\nLIT 1\nSUB\nSTATUS\nEXIT\n'
 run('status survives arithmetic '+file,src,expected,files={'PRESENT':b'abc'})
for create in [False,True]:
 operation='CREATE' if create else 'OPEN';transfer='READ' if create else 'WRITE'
 src=name('F','DATA')+'WORD H 0\nBUFFER B 1\nLABEL MAIN\nADDR F0\n'+operation+'\nST H\nLD H\nPUSH\nADDR B\nPUSH\nLIT 1\n'+transfer+'\nSTATUS\nEXIT\n'
 m=run('access mode '+transfer,src,1,files={'DATA':b'abc'})
 assert m.files['DATA']==(b'' if create else b'abc')
for op in ['CLOSE','READ','WRITE']:
 args='PUSH\nADDR B\nPUSH\nLIT 1\n' if op!='CLOSE' else ''
 run('invalid handle '+op,'BUFFER B 1\nLABEL MAIN\nLIT 0\n'+args+op+'\nSTATUS\nEXIT\n',1)
close=name('F','DATA')+'WORD H 0\nLABEL MAIN\nADDR F0\nOPEN\nST H\nLD H\nCLOSE\nLD H\nCLOSE\nSTATUS\nEXIT\n'
run('closed handle invalid',close,1,files={'DATA':b'abc'})
for operation in ['OPEN','CREATE']:
 src=name('F','DATA')+'LABEL MAIN\n'+('ADDR F0\n'+operation+'\n')*8+'ADDR F0\nCREATE\nSTATUS\nEXIT\n'
 m=run('handle exhaustion '+operation,src,1,files={'DATA':b'original'})
 if operation=='OPEN':assert m.files['DATA']==b'original'
# Zero-count transfer does not access the pointer or change a file.
for operation,transfer in [('OPEN','READ'),('CREATE','WRITE')]:
 src=name('F','DATA')+'WORD H 0\nLABEL MAIN\nADDR F0\n'+operation+'\nST H\nLD H\nPUSH\nLIT 0\nPUSH\nLIT 0\n'+transfer+'\nSTATUS\nEXIT\n'
 run('zero count '+transfer,src,files={'DATA':b'abc'})
# Binding failures expose normalized status, never an operating-system error code.
class FaultMachine(DosMachine):
 def __init__(self,function,**kw):super().__init__(**kw);self.function=function
 def interrupt(self,c,n,data):
  if n==0x21 and c.reg_read(UC_X86_REG_AH)==self.function:
   c.reg_write(UC_X86_REG_AX,123);self.carry(True);return
  super().interrupt(c,n,data)
for service,function in [('PUTC',0x40),('GETC',0x3f),('OPEN',0x3d),('CREATE',0x3c)]:
 prefix=name('F','DATA');arg='ADDR F0\n' if service in ['OPEN','CREATE'] else 'LIT 65\n'
 expected=65535 if service=='GETC' else 0
 src=prefix+'WORD RESULT 0\nWORD FLAG 0\nLABEL MAIN\n'+arg+service+f'\nST RESULT\nSTATUS\nST FLAG\nLD RESULT\nPUSH\nLIT {expected}\nEQ GOOD\nLIT 99\nEXIT\nLABEL GOOD\nLD FLAG\nEXIT\n'
 m=FaultMachine(function,files={'DATA':b'abc'},stdin=b'X').run(build(src))
 assert m.exitcode==1,(service,m.exitcode,m.output)
 results.append('PASS normalized binding failure '+service)
class ShortWrite(DosMachine):
 def interrupt(self,c,n,data):
  if n==0x21 and c.reg_read(UC_X86_REG_AH)==0x40 and c.reg_read(UC_X86_REG_BX)>=5:
   count=c.reg_read(UC_X86_REG_CX);c.reg_write(UC_X86_REG_CX,min(count,1));super().interrupt(c,n,data);c.reg_write(UC_X86_REG_CX,count);return
  super().interrupt(c,n,data)
partial=name('F','DATA')+'WORD H 0\nWORD COUNT 0\nWORD FLAG 0\nBYTE D0 65\nBYTE D1 66\nBYTE D2 67\nLABEL MAIN\nADDR F0\nCREATE\nST H\nLD H\nPUSH\nADDR D0\nPUSH\nLIT 3\nWRITE\nST COUNT\nSTATUS\nST FLAG\nLD COUNT\nPUSH\nLIT 1\nEQ GOOD\nLIT 99\nEXIT\nLABEL GOOD\nLD FLAG\nEXIT\n'
native=ShortWrite().run(build(partial));portable=Machine(write_limit=1).run(partial)
assert (native.exitcode,native.output,native.files)==(portable.exitcode,portable.output,portable.files)==(1,b'',{'DATA':b'A'})
results.append('PASS short write retains partial count and normalized failure status')
for function in [0x3d,0x3f,0x3e,0x3c,0x40]:
 m=FaultMachine(function,files={'TEST.IR':b'LABEL MAIN\nHALT\n','TEST.ASM':b'OLD'},inputs=['TEST']).run(IR)
 assert m.exitcode==1 and b'CODE 6' in m.output,(function,m.output)
 if function!=0x40:assert m.files['TEST.ASM']==b'OLD'
 results.append(f'PASS compiler I/O failure {function:02X}')
for src in ['LABEL MAIN\nJMP MISSING\n','WORD X 0\nWORD X 0\nLABEL MAIN\nHALT\n']:
 t=translate(src);assert t.exitcode==0
 a=assemble(ASM,t.files['TEST.ASM'],'CHECK',old=b'OLD COM');assert a.exitcode==1 and b'CODE 3' in a.output and a.files['CHECK.COM']==b'OLD COM'
 results.append('PASS delegated symbol error')
small=DosMachine({'TEST.IR':b'LABEL MAIN\nHALT\n'},['TEST'],sp=0x8000).run(IR)
assert small.exitcode==1 and b'IR ERROR 00000 CODE 7' in small.output
assert DosMachine(sp=0x8000).run(build('LABEL MAIN\nHALT\n')).exitcode==7
results.append('PASS 8086 profile entry guards, separate from portable machine')
(Q/'limit-results.txt').write_text('\n'.join(results)+'\n')
print(f'PASS {len(results)} portable-contract and native-binding checks')
