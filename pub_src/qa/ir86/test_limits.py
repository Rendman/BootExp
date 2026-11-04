"""Independent semantics, control boundaries, limits, and file-failure tests."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/ir86';Q=ROOT/'qa/ir86'
sys.path.insert(0,str(ROOT/'qa/asm86'))
from dos_machine import DosMachine,assemble
from unicorn.x86_const import UC_X86_REG_AH,UC_X86_REG_AX
IR=(W/'IR86.COM').read_bytes();ASM=(ROOT/'workbench/asm86/ASM86.COM').read_bytes();results=[]
def translate(source):
 raw=source.encode('ascii') if isinstance(source,str) else source
 return DosMachine({'TEST.IR':raw,'TEST.ASM':b'OLD'},['TEST']).run(IR)
def build(source):
 t=translate(source);assert t.exitcode==0,t.output
 assert t.operations==[('open','TEST.IR'),('create','TEST.ASM')],t.operations
 a=assemble(ASM,t.files['TEST.ASM'],'TEST');assert a.exitcode==0,(a.output,t.files['TEST.ASM'])
 return a.files['TEST.COM']
def run(label,source,status=0,output=b'',files=None,**kw):
 m=DosMachine(files,**kw).run(build(source))
 assert m.exitcode==status and m.output==output,(label,m.output,m.exitcode)
 results.append('PASS '+label)
 return m
def bad(label,source,code):
 t=translate(source)
 assert t.exitcode==1 and f'CODE {code}'.encode() in t.output,(label,t.output)
 assert t.files['TEST.ASM']==b'OLD' and not any(o[0]=='create' for o in t.operations),label
 results.append('PASS '+label)
def condition(a,b,op):return f'LABEL MAIN\nLIT {a}\nPUSH\nLIT {b}\n{op} GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n'
for op,compute in [('ADD',lambda a,b:(a+b)&65535),('SUB',lambda a,b:(a-b)&65535),('AND',lambda a,b:a&b),('OR',lambda a,b:a|b),('XOR',lambda a,b:a^b)]:
 for a,b in [(7,3),(0,1),(65535,1),(32768,32768),(21845,43690)]:
  source=f'LABEL MAIN\nLIT {a}\nPUSH\nLIT {b}\n{op}\nPUSH\nLIT {compute(a,b)}\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n'
  run(f'{op} word semantics {a},{b}',source)
def signed(n):return n if n<32768 else n-65536
for op in ['EQ','NE','ULT','ULE','UGT','UGE','SLT','SLE','SGT','SGE']:
 for a,b in [(0,1),(1,0),(65535,0),(32768,32767),(32767,32768),(65535,65535)]:
  x,y=(signed(a),signed(b)) if op.startswith('S') else (a,b)
  truth={'EQ':x==y,'NE':x!=y,'LT':x<y,'LE':x<=y,'GT':x>y,'GE':x>=y}[op if op in ['EQ','NE'] else op[1:]]
  run(f'{op} {a},{b}',condition(a,b,op),0 if truth else 1)
for op,truth in [('JZ',True),('JNZ',False)]:
 for value in [0,65535]:
  expected=(value==0)==truth
  source=f'LABEL MAIN\nLIT {value}\n{op} GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n'
  run(f'{op} {value}',source,0 if expected else 1)
for name in ['BX','CX','DX']:
 run('register bridge '+name,f'LABEL MAIN\nLIT 65535\nTO{name}\nLIT 0\nFROM{name}\nPUSH\nLIT 65535\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
run('LIFO order','LABEL MAIN\nLIT 7\nPUSH\nLIT 3\nPUSH\nLIT 0\nPOP\nPOP\nPUSH\nLIT 7\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
run('wrap to zero','LABEL MAIN\nLIT 65535\nPUSH\nLIT 1\nADD\nJZ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
run('word fetch/store','BUFFER DATA 4\nLABEL MAIN\nADDR DATA\nPUSH\nLIT 4660\nPUT\nADDR DATA\nFETCH\nPUSH\nLIT 4660\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
for op in ['LDB DATA','ADDR DATA\nFETCHB']:
 run('zero-extended '+op,'BYTE DATA 0\nLABEL MAIN\nLIT 65535\n'+op+'\nJZ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
run('byte store retains AX','BYTE DATA 0\nLABEL MAIN\nLIT 65535\nSTB DATA\nPUSH\nLIT 65535\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
run('pointer byte store retains AX','BUFFER DATA 1\nLABEL MAIN\nADDR DATA\nPUSH\nLIT 65535\nPUTB\nPUSH\nLIT 65535\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
run('native procedure and AX result','LABEL MAIN\nCALL OUTER\nEXIT\nLABEL OUTER\nCALL INNER\nRET\nLABEL INNER\nLIT 0\nRET\n')
run('implicit normal exit','LABEL MAIN\nNOP\n')
run('empty MAIN body','LABEL MAIN\n')
run('register spelling is a user name','WORD AX 0\nLABEL MAIN\nLD AX\nEXIT\n')
run('lowercase tabs and comments','word\tax\t0 ;a note\rlabel main\nld ax\r\nexit\x1aINVALID')
run('full name length','WORD ABCDEFGHIJKLMN 0\nLABEL MAIN\nLD ABCDEFGHIJKLMN\nEXIT\n')
run('word literal boundary','LABEL MAIN\nLIT 0FFFFH\nPUSH\nLIT 65535\nEQ GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n')
for op,expected in [('JC',0),('JNC',1)]:
 run('DOS carry '+op,'LABEL MAIN\nLIT 65535\nTOBX\nLIT 3E00H\nDOS\n; carry survives comments\n\n'+op+' GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n',expected)
run('DOS clear carry','BYTE F0 88\nBYTE F1 0\nLABEL MAIN\nADDR F0\nTODX\nLIT 3D00H\nDOS\nJNC GOOD\nLIT 1\nEXIT\nLABEL GOOD\nHALT\n',files={'X':b''})
run('32 expression words','LABEL MAIN\nLIT 0\n'+'PUSH\n'*32+'POP\n'*32+'EXIT\n')
bad('33 expression words','LABEL MAIN\nLIT 0\n'+'PUSH\n'*33,5)
for end in ['HALT','EXIT','RET','JMP MAIN','CALL MAIN','JZ MAIN','JNZ MAIN','DOS','LABEL MORE']:
 bad('nonempty boundary '+end,'LABEL MAIN\nLIT 1\nPUSH\n'+end+'\n',4)
bad('comparison leaves an unrelated temporary','LABEL MAIN\nLIT 1\nPUSH\nPUSH\nEQ MAIN\n',4)
bad('unclosed expression at EOF','LABEL MAIN\nLIT 1\nPUSH\n',4)
for op in ['POP','ADD','SUB','AND','OR','XOR','PUT','PUTB','EQ MAIN','SLT MAIN']:
 bad('missing expression word '+op,'LABEL MAIN\n'+op+'\n',4)
for text,code in [('',3),('HALT',1),('LABEL ELSE',3),('WORD X 0',3),('LABEL MAIN\nWORD X 0',1),('LABEL MAIN\nNOP 1',1),('LABEL MAIN\nLIT 65536',2),('LABEL MAIN\nLIT 10000H',2),('LABEL MAIN\nLIT -1',2),('LABEL MAIN\nLIT X',2),('LABEL MAIN\nLIT 0GH',2),('LABEL MAIN\nLIT FFH',2),('LABEL MAIN\nLIT 1+2',2),('BYTE X 256',4),('BUFFER X 0',4),('BUFFER X 257',4),('WORD 1BAD 0',3),('WORD ABCDEFGHIJKLMNO 0',3),('LABEL MAIN\nLD A+B',3),('LABEL MAIN\nLABEL X EXTRA',1),('LABEL MAIN\nJC MAIN',4),('LABEL MAIN\nLIT 65535\nTOBX\nLIT 3E00H\nDOS\nNOP\nJC MAIN',4),('LABEL MAIN\nLIT 65535\nTOBX\nLIT 3E00H\nDOS\nLABEL X\nJC MAIN',4),('LABEL MAIN\nUNKNOWN',1)]:bad('reject '+repr(text),text,code)
for byte in [0,1,27,127,128,255]:bad('invalid input byte '+str(byte),b'LABEL MAIN\n'+bytes([byte]),6)
run('120 physical characters',';'+'X'*119+'\nLABEL MAIN\nHALT\n')
bad('121 physical characters',';'+'X'*120+'\nLABEL MAIN\nHALT\n',5)
bad('4001 source lines',';\n'*4001,5)
run('4000 generated assembly lines','LABEL MAIN\n'+'NOP\n'*3990)
bad('4001 generated assembly lines','LABEL MAIN\n'+'NOP\n'*3991,5)
bad('assembly-text capacity','LABEL MAIN\n'+('LIT '+'0'*16+'\n')*1400,5)
names='LABEL MAIN\n'+''.join(f'LABEL L{i}\n' for i in range(254))
run('256 generated definitions',names+'HALT\n')
bad('257 generated definitions',names+'LABEL EXTRA\nHALT\n',5)
branches='LABEL MAIN\nLIT 0\n'+'JZ GOOD\n'*253+'LABEL GOOD\nHALT\n'
run('generated branch names count toward symbol budget',branches)
bad('generated branch budget overflow',branches.replace('LABEL GOOD','JZ GOOD\nLABEL GOOD'),5)
data=''.join(f'BUFFER B{i} 256\n' for i in range(31))
code=build(data+'BUFFER LAST 236\nLABEL MAIN\nHALT\n');assert len(code)==8192
assert DosMachine().run(code).exitcode==0
results.append('PASS exact 8192-byte target')
bad('8193-byte target',data+'BUFFER LAST 237\nLABEL MAIN\nHALT\n',5)
for src in ['LABEL MAIN\nJMP MISSING\n','WORD X 0\nWORD X 0\nLABEL MAIN\nHALT\n']:
 t=translate(src);assert t.exitcode==0,t.output
 a=assemble(ASM,t.files['TEST.ASM'],'CHECK',old=b'OLD COM')
 assert a.exitcode==1 and b'CODE 3' in a.output and a.files['CHECK.COM']==b'OLD COM',a.output
 results.append('PASS delegated assembler symbol error')
small=DosMachine({'TEST.IR':b'LABEL MAIN\nHALT\n'},['TEST'],sp=0x8000).run(IR)
assert small.exitcode==1 and b'IR ERROR 00000 CODE 7' in small.output
results.append('PASS translator memory guard')
run('generated program memory guard','LABEL MAIN\nHALT\n',7,sp=0x8000)
class FaultMachine(DosMachine):
 def __init__(self,fail):super().__init__({'TEST.IR':b'LABEL MAIN\nHALT\n','TEST.ASM':b'OLD'},['TEST']);self.fail=fail
 def interrupt(self,c,number,data):
  if number==0x21 and c.reg_read(UC_X86_REG_AH)==self.fail:
   c.reg_write(UC_X86_REG_AX,0);self.carry(self.fail!=0x40);return
  super().interrupt(c,number,data)
for function in [0x3d,0x3f,0x3e,0x3c,0x40]:
 m=FaultMachine(function).run(IR)
 assert m.exitcode==1 and b'CODE 6' in m.output,(function,m.output)
 results.append(f'PASS DOS error {function:02X}'+(' (short write)' if function==0x40 else ''))
(Q/'limit-results.txt').write_text('\n'.join(results)+'\n')
print(f'PASS {len(results)} independent IR semantics, boundaries, grammar, and DOS-I/O cases')
