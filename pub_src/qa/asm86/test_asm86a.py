"""Check native ASM86A artifacts against independent encoding and behavior expectations."""
from machine import *
import sys
sys.path.insert(0,str(ROOT/'tools'))
from project_paths import directory_name
import json,re
W=ROOT/'workbench/asm86';Q=ROOT/'qa/asm86'
seed=(W/'ASMA0.COM').read_bytes();image=(W/'ASM86A.COM').read_bytes();records=[]
def log(s):records.append('PASS '+s)
def good(source,expected=None,tool=image):
 r=run_assembler(tool,source,{'RESULT.COM':b'OLD'})
 assert r.exitcode==0,(source[:120],r.output)
 b=r.files['RESULT.COM'];assert r.output==f'OK RESULT.COM {len(b):05} bytes\r\n'.encode(),r.output
 assert 'ASMA.TMP' not in r.files and 'RESULT.BAK' not in r.files and not r.allocations
 if expected is not None:assert b==(bytes.fromhex(expected) if isinstance(expected,str) else expected),(source[:100],b[:50],expected)
 return b

def bad(source,code=None,tool=image,files=None):
 f={'RESULT.COM':b'OLD'};f.update(files or {})
 r=run_assembler(tool,source,f)
 assert r.exitcode==1,(source,r.output)
 assert r.files['RESULT.COM']==b'OLD' and not r.allocations,(source,'changed old result or leaked memory')
 if code is not None:assert f'CODE {code}\r\n'.encode() in r.output,(source,r.output,code)
 return r
# The only initial artifact producer is the preceding project assembler.
built=assemble((ROOT/'workbench/asm0/ASM86.COM').read_bytes(),(W/'ASMA0.ASM').read_bytes(),'ASMA0')
assert built.exitcode==0 and built.files['RESULT.COM']==seed
assert len(seed)<=8192
log('unchanged ASM86 directly builds ASMA0')
for name,tool in [('ASMA0',seed),('ASM86A',image)]:
 source=(W/(name+'.ASM')).read_bytes()
 first=good(source,tool=seed if name=='ASM86A' else seed)
 assert first==tool
 assert good(source,tool=first)==tool and good(source,tool=tool)==tool
 log(name+' builder and two self-assembly generations match')
for folder,name in [('asm86','ASM86'),('ir86','IR86'),('rill','RILL')]:
 good((ROOT/'workbench'/directory_name(folder)/(name+'.ASM')).read_bytes(),(ROOT/'workbench'/directory_name(folder)/(name+'.COM')).read_bytes());log('exact prior-tool compatibility '+name)
for c in json.loads((ROOT/'qa/asm0/checkpoints.json').read_text()):
 if c.get('image') is not None and c['number']>=29:
  good(c['fixture'],c['image']);log('published ASM86 executable fixture')
# Directly specified encodings, not a host instruction encoder.
cases=[
 ('MOV AX,ES\nMOV ES,BX\n','8CC08EC3'),
 ('MOV DS,AX\nMOV AX,CS\nMOV SS,DX\n','8ED88CC88ED2'),
 ('MOV AX,ES:[BX]\nMOV DS:[1234H],DX\n','268B073E89163412'),
 ('DB "Hello; x",13,10,0\n','48656C6C6F3B20780D0A00'),
 ('DB "a""b",0,""\n','61226200'),
 ('N EQU 3\nRESB N\nRESW 2\n','00000000000000'),
 ('DB 1+2,4-1,(5-2),-(-3)\n','03030303'),
 ('A:\nDB 1,2\nN EQU $-A\nDW N\n','01020200'),
 ('MOV AX,[SI]\nMOV AX,[DI]\nMOV AX,[BP]\n','8B048B058B4600'),
 ('MOV AX,[BX+SI+4]\nMOV [BP-2],AX\n','8B8004008986FEFF'),
 ('MOV AX,[BX+DI]\nMOV AX,[BP+SI]\nMOV AX,[BP+DI]\n','8B018B028B03'),
 ('MOV AX,[BX+0]\nMOV AX,[BP+0]\n','8B8700008B860000'),
 ('MOV WORD [BX],1234H\nADD WORD [BP-2],1\n','C70734128186FEFF0100'),
 ('MOV BYTE [DI],255\nMOV [DI],AL\n','C605FF8805'),
 ('ADD AX,[SI]\nSUB [DI],BX\nCMP BYTE [BX],1\n','0304291D803F01'),
 ('LEA AX,[BX+SI+4]\nCALL AX\nJMP [BX]\nRET\n','8D800400FFD0FF27C3'),
 ('SHL AX,1\nSHR AX,CL\nMUL BX\nDIV BL\n','D1E0D3E8F7E3F6F3'),
 ('DW FORWARD-$\nFORWARD:\nRET\n','0200C3')]
for source,expected in cases:good(source,expected);log('encoding '+source.splitlines()[0])
for op,inv in [('JB','73'),('JAE','72'),('JE','75'),('JNE','74'),('JBE','77'),('JA','76')]:
 b=good(op+' NEAR X\nRESB 200\nX:\nRET\n');assert b[:5]==bytes.fromhex(inv+'03E9C800') and len(b)==206
 log('five-byte 8086 conditional expansion '+op)
for text,code in [('RET 4',1),('NOP',1),('ADC AX,BX',1),('SBB AX,BX',1),('NEG AX',1),('NOT AX',1),('IMUL BX',1),('IDIV BX',1),('SAR AX,CL',1),('ROL AX,1',1),('REP MOVSB',1),('JZ X\nX:',1),('JL X\nX:',1),('MOV CS,AX',1),('MOV AX,CS:[BX+SI+DI]',1),('MOV AX,[AX]',1),('MOV AX,[BX+BP]',1),('MOV AX,[SI+DI]',1),('MOV AX,[BX+BX]',1),('MOV AX,[BX-SI]',1),('MOV AX,[SI*2]',3),('MOV AX,[SP]',1),('MOV AX,AL',1),('MOV BYTE [BX],AX',1),('MOV [BX],1',1),('ADD [BX],[DI]',1),('SHL AX,2',4),('SHL AX,0',4),('PUSH 1',1),('IMUL AX,BX',1),('REP RET',1),('DW "X"',1),('DB -1',4),('DB 256',4),('RESW 32768',5),('RESB -1',5),('N EQU LATER\nLATER:',3),('RESB LATER\nLATER:',3),('X:\nX:',3),('DW LOST',3),('MOV AX,65536',2),('DB "open',1),('MOV AX,[]',3)]:
 bad(text+'\n',code);log('reject '+text.splitlines()[0])
# Real target programs exercise frames, indexing, quoted data, and distant control.
program='''MOV AX,7
PUSH AX
CALL F
ADD SP,2
MOV DX,AX
ADD DL,48
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
F:
PUSH BP
MOV BP,SP
SUB SP,2
MOV AX,[BP+4]
MOV [BP-2],AX
MOV AX,[BP-2]
MOV SP,BP
POP BP
RET
'''
child=AssemblerMachine().run(good(program));assert child.exitcode==0 and child.output==b'7';log('executed BP frame argument and local')
program='''MOV SI,TEXT
MOV CX,LENGTH
LOOP:
MOV DL,[SI]
MOV AH,2
INT 21H
INC SI
DEC CX
JNE NEAR LOOP
MOV AX,4C00H
INT 21H
TEXT:
DB "Hi"
LENGTH EQU $-TEXT
'''
child=AssemblerMachine().run(good(program));assert child.exitcode==0 and child.output==b'Hi';log('executed indexed quoted string, EQU, and long condition')
for n in [0,1,1023,1024,1025,4095,4096,4097,8193,61184]:
 good(f'RESB {n}\n',bytes(n));log('streamed image length '+str(n))
bad('RESB 61185\n',5);bad('RESB 61184\nDB 0\n',5);log('reject output overflow without PC wrap')
# Seed has a separate capacity while output is already streamed.
good('DB 0\n'*8193,bytes(8193),tool=seed);log('seed emits beyond the preceding 8192-byte output limit')
for n in [2048,8192]:
 tool=seed if n==2048 else image
 text=''.join(f'S{i}:\n' for i in range(n))+'DW S0,S'+str(n-1)+'\n'
 good(text,'00010001',tool=tool);log('exact symbol capacity '+str(n))
 bad(text+f'S{n}:\n',5,tool=tool);log('symbol capacity overflow '+str(n))
for n in [31,32]:
 text='A'*n+':\nDW '+'A'*n+'\n'
 if n==31:good(text,'0001')
 else:bad(text,3)
 log('name boundary '+str(n))
for name in ['A'*30+'X','A'*30+'Y']:good(name+':\nDW '+name+'\n','0001')
log('full spelling at the last name character')
def bucket(name):
 h=0
 for ch in name.encode():h=(((h<<5)|(h>>11))^ch)&65535
 return h&4095
seen={};collision=None
for i in range(10000):
 name='HASH_'+str(i);h=bucket(name)
 if h in seen:collision=(seen[h],name);break
 seen[h]=name
assert collision is not None
first,last=collision
good(first+':\nDB 1\n'+last+':\nDB 2\nDW '+first+','+last+'\n','010200010101');log('deliberate bucket collision with distinct values')
text=''.join(f'COLLISION_PREFIX_{i}:\n' for i in range(3000))+'DW COLLISION_PREFIX_0,COLLISION_PREFIX_2999\n'
good(text,'00010001');log('bucket chaining across symbol pages')
good('; comment\r\n'*65536,b'');log('source exceeds 64 KB and 65535 lines')
r=bad(';\n'*65536+'UNKNOWN\n',1);assert b'ERROR 0000065537 CODE 1' in r.output,r.output;log('full 32-bit error line report')
for ending in ['\r\n','\r','\n','']:
 good('DB 1'+ending,'01');log('source line termination '+repr(ending))
for offset in [1023,1024,4095,4096]:
 text=';'+'x'*(offset-3)+'\r\nDB 1\r\n' if offset<1024 else (';\r\n'*(offset//3))+'DB 1\r\n'
 good(text,'01');log('input block crossing '+str(offset))
good(';'+'x'*1022+'\nDB 1\n','01');bad(';'+'x'*1023+'\n',5);log('physical line boundary')
good('DB '+('0'*63)+'\n','00');bad('DB '+('0'*64)+'\n',1);log('token boundary')
good('DW '+'('*15+'1'+')'*15+'\n','0100');bad('DW '+'('*16+'1'+')'*16+'\n',5);log('expression depth boundary')
good(b'DB 1\x1a\x80','01');log('Control-Z source termination')
for byte in [0,1,127,128,255]:bad(b'DB 1\n'+bytes([byte])+b'\n',6);log('reject source byte '+str(byte))
for old in ['ASMA.TMP','RESULT.BAK']:
 r=bad('RET\n',8,files={old:b'RECOVERY'});assert r.files[old]==b'RECOVERY';log('reserved recovery file '+old)
bad(None,6);log('missing input preserves old result')
(Q/'test-results.txt').write_text('\n'.join(records)+'\n');(Q/'build-facts.json').write_text(json.dumps({'seed_bytes':len(seed),'binary_bytes':len(image),'checks':len(records)},indent=2)+'\n')
print('PASS',len(records),'ASM86A encoding, bootstrap, compatibility, streaming, capacity, and runtime checks')
