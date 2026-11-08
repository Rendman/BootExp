"""Independent native encoding, grammar, boundary, and DOS-I/O checks."""
from pathlib import Path
import json
from dos_machine import DosMachine,assemble
from unicorn.x86_const import UC_X86_REG_AH,UC_X86_REG_AX
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/asm86';Q=ROOT/'qa/asm86'
IMAGE=(W/'ASM86.COM').read_bytes();results=[]
accepted=set(json.loads((Q/'checkpoints.json').read_text())[-1]['names'])
def ok(label,source,expected):
 m=assemble(IMAGE,source,old=b'old file tail')
 assert m.exitcode==0,(label,m.output)
 assert m.files['RESULT.COM']==expected,(label,m.files['RESULT.COM'],expected)
 assert m.operations==[('open','SOURCE.ASM'),('open','SOURCE.ASM'),('create','RESULT.COM')],(label,m.operations)
 results.append('PASS '+label)
 return m
def bad(label,source,code,line=1):
 m=assemble(IMAGE,source,old=b'old file tail')
 assert m.exitcode==1 and f'ERROR {line:05} CODE {code}'.encode() in m.output,(label,m.output)
 assert m.files['RESULT.COM']==b'old file tail' and not any(op[0]=='create' for op in m.operations),label
 results.append('PASS '+label)
for c in json.loads((ROOT/'qa/checkpoints.json').read_text()):
 ok('BOOTASM language fixture '+c['fixture'],(ROOT/'workbench/bootasm'/(c['fixture']+'.ASM')).read_bytes(),bytes.fromhex(c['expected']))
for source,expected in [('',b''),(';empty',b''),('db 0,255\ndw 0,65535',bytes.fromhex('00 FF 00 00 FF FF')),
 ('\t db\t65 ; comment\rDB 66\nDB 67\r\nDB 68\x1aDB 99',b'ABCD'),
 ('ABCDEFGHIJKLMNOP:\nDW ABCDEFGHIJKLMNOP',bytes.fromhex('00 01')),
 ('DW END\nDB 65\nEND:',bytes.fromhex('03 01 41'))]:ok('source '+repr(source),source,expected)
for reg8,reg16,i in zip('AL CL DL BL AH CH DH BH'.split(),'AX CX DX BX SP BP SI DI'.split(),range(8)):
 ok('register encodings '+reg8, f'MOV {reg8},255\nMOV {reg16},65535\nINC {reg16}\nDEC {reg16}\nPUSH {reg16}\nPOP {reg16}',bytes([0xb0+i,255,0xb8+i,255,255,0x40+i,0x48+i,0x50+i,0x58+i]))
 for r,width in [(reg8,0),(reg16,1)]:
  ok('memory encodings '+r,f'MOV {r},[BX]\nMOV [BX],{r}\nMOV {r},[1234H]\nMOV [1234H],{r}',bytes([0x8a+width,8*i+7,0x88+width,8*i+7,0x8a+width,8*i+6,0x34,0x12,0x88+width,8*i+6,0x34,0x12]))
for name,group in [('ADD',0),('OR',1),('AND',4),('SUB',5),('XOR',6),('CMP',7)]:
 if name not in accepted:continue
 ok('arithmetic '+name,f'{name} DL,AH\n{name} SI,DI\n{name} BL,255\n{name} BP,65535',bytes([8*group+2,0xd4,8*group+3,0xf7,0x80,0xc3+8*group,255,0x81,0xc5+8*group,255,255]))
for name,opcode in [('JB',0x72),('JAE',0x73),('JE',0x74),('JNE',0x75),('JBE',0x76),('JA',0x77),('JL',0x7c),('JGE',0x7d),('JLE',0x7e),('JG',0x7f)]:
 if name not in accepted:continue
 ok('branch +127 '+name,name+' 181H',bytes([opcode,127]))
 ok('branch -128 '+name,name+' 82H',bytes([opcode,128]))
 bad('branch +128 '+name,name+' 182H',4)
 bad('branch -129 '+name,name+' 81H',4)
ok('near displacement wrap','CALL 0\nJMP 65535',bytes.fromhex('E8 FD FE E9 F9 FE'))
ok('fixed instruction set','RET\nCLD\nLODSB\nSTOSB\nINT 255',bytes.fromhex('C3 FC AC AA CD FF'))
for source,code in [('DW 65536',2),('DW 10000H',2),('DW 0GH',2),('DW 12A',2),('DB 256',4),('INT 256',4),('MOV AL,256',4),('DW -1',3),('DW +1',3),('DW 1+2',2),('DB',3),('DB 1,',3),('DB 1 2',1),('MOV AX,AL',1),('ADD AX,AL',1),('MOV [BX],1',1),('ADD AX,[BX]',1),('MOV AX,[SI]',3),('MOV AX,[BX+1]',3),('MOV AX,[BX',1),('MOV AX,',3),('MOV AX,1,2',1),('NOP 1',1),('RET 2',1),('INC AL',1),('PUSH 1',1),('JZ 100H',1),('ORG 100H',1),('AX:',3),('1BAD:',3),('DW UNDEFINED',3),('DUP:\nDUP:',3),('LABEL: DB 1',1),('ABCDEFGHIJKLMNOPQ:',1)]:bad('reject '+repr(source),source,code,2 if source=='DUP:\nDUP:' else 1)
ok('physical line 120',';'+'x'*119,b'')
bad('physical line 121',';'+'x'*120,5)
ok('4000 lines',';\n'*4000,b'')
bad('4001 lines',';\n'*4001,5,4001)
symbols=''.join(f'L{i}:\n' for i in range(256))
ok('256 labels',symbols+'DW L255',bytes.fromhex('00 01'))
bad('257 labels',symbols+'L256:\n',5,257)
data='DB '+','.join(['0']*40)+'\n'
ok('8192 bytes',data*204+'DB '+','.join(['0']*32),bytes(8192))
bad('8193 bytes',data*204+'DB '+','.join(['0']*33),5,205)
for value in [0,1,27,127,128,255]:bad('invalid source byte '+str(value),b'DB 1\n'+bytes([value]),6,2)
class FaultMachine(DosMachine):
 def __init__(self,fail):super().__init__({'SOURCE.ASM':b'DB 65\n','RESULT.COM':b'old'},['TRY']);self.fail=fail
 def interrupt(self,c,number,unused):
  if number==0x21 and c.reg_read(UC_X86_REG_AH)==self.fail:
   c.reg_write(UC_X86_REG_AX,0);self.carry(self.fail!=0x40);return
  super().interrupt(c,number,unused)
for function in [0x3d,0x3f,0x3e,0x3c,0x40]:
 m=FaultMachine(function).run(IMAGE)
 assert m.exitcode==1 and b'CODE 6' in m.output,(function,m.output)
 results.append(f'PASS DOS failure {function:02X}'+(' (short write)' if function==0x40 else ''))
assert (ROOT/'workbench/bootasm/BOOTASM.BAS').read_bytes()==(W/'BOOTASM.BAS').read_bytes()
results.append('PASS canonical BOOTASM source is identical in both collections')
(Q/'limit-results.txt').write_text('\n'.join(results)+'\n')
print(f'PASS {len(results)} independent encoding, grammar, resource, and I/O cases')
