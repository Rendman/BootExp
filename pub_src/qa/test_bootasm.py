"""Run the actual published BASIC listings in a GW-BASIC-compatible interpreter.
No assembler or compiler generates expected bytes or COM files here.
"""
from pathlib import Path
import io,json,sys,shutil, tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/python'))
sys.path.insert(0,str(ROOT/'tools/python-pcbasic207'))
import pcbasic
from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_INTR
from unicorn.x86_const import *
WORK=ROOT/'workbench/bootasm'
CASES=json.loads((ROOT/'qa/checkpoints.json').read_text())
RESULT=[]
def assemble(source, name, text=None):
    if text is not None:
        (WORK/(name+'.ASM')).write_bytes((text+'\r\n').replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
    out=io.BytesIO()
    # Reproduce COPY fixture.ASM SOURCE.ASM and preserve the named result.
    with tempfile.TemporaryDirectory() as directory:
        work=Path(directory)
        shutil.copyfile(WORK/source,work/source)
        shutil.copyfile(WORK/(name+'.ASM'),work/'SOURCE.ASM')
        target=WORK/(name+'.COM')
        if target.exists():shutil.copyfile(target,work/'RESULT.COM')
        with pcbasic.Session(input_streams=io.BytesIO(),output_streams=out,devices={'A':str(work)},current_device='A:') as session:
            session.execute(f'LOAD "{source}"')
            session.execute('RUN')
        if (work/'RESULT.COM').exists():shutil.copyfile(work/'RESULT.COM',target)
    return out.getvalue().decode('ascii',errors='replace')

def execute_com(code):
    cpu=Uc(UC_ARCH_X86,UC_MODE_16);cpu.mem_map(0,0x100000)
    base=0x10000
    cpu.mem_write(base,b'\xcd\x20')
    cpu.mem_write(base+0x100,code)
    for reg in (UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_ES,UC_X86_REG_SS):cpu.reg_write(reg,0x1000)
    cpu.reg_write(UC_X86_REG_SP,0xfffe);cpu.mem_write(base+0xfffe,b'\0\0')
    output=[]; exitcode=[]
    def interrupt(c,num,data):
        assert num in (0x20,0x21),f'Unexpected interrupt {num:x}'
        if num==0x20:exitcode.append(0);c.emu_stop();return
        ah=c.reg_read(UC_X86_REG_AH)
        if ah==2:
            char=c.reg_read(UC_X86_REG_DL);output.append(chr(char));c.reg_write(UC_X86_REG_AL,char)
        elif ah==9:
            at=c.reg_read(UC_X86_REG_DS)*16+c.reg_read(UC_X86_REG_DX)
            for offset in range(4096):
                ch=bytes(c.mem_read(at+offset,1))[0]
                if ch==36:break
                output.append(chr(ch))
            else:raise AssertionError('Unterminated DOS string')
            c.reg_write(UC_X86_REG_AL,36)
        elif ah==0x4c:exitcode.append(c.reg_read(UC_X86_REG_AL));c.emu_stop()
        else:raise AssertionError(f'Unexpected DOS function {ah:x}')
    cpu.hook_add(UC_HOOK_INTR,interrupt)
    cpu.emu_start(base+0x100,base+0x10000,count=100000)
    assert exitcode,'Program did not terminate'
    return ''.join(output),exitcode[0]

def require(condition,message):
    if not condition:raise AssertionError(message)

for case in CASES:
    i=case['number'];name=case['fixture'];source=case['source']
    log=assemble(source,name)
    require('OK RESULT.COM' in log, f'{source}: {log}')
    actual=(WORK/(name+'.COM')).read_bytes();expected=bytes.fromhex(case['expected'])
    require(actual==expected,f'{source}: {actual.hex(" ")} != {expected.hex(" ")}')
    badname=f'X{i:02}'
    old=WORK/(badname+'.COM');old.write_bytes(b'OLD')
    badlog=assemble(source,badname)
    require(case['diagnostic'] in badlog and 'OK ' not in badlog,f'{source} rejection: {badlog}')
    require(old.read_bytes()==b'OLD',f'{source}: rejection changed output')
    old.unlink()
    if case['run'] is not None:
        output,code=execute_com(actual)
        require((output,code)==(case['run'],0),f'{source}: runtime {(output,code)}')
    RESULT.append(f'PASS {source}: exact bytes; expected rejection; old output preserved'+('; executable output and return code' if case['run'] is not None else ''))
    print(RESULT[-1],flush=True)

# Full language: representative independent encodings and important boundaries.
final='BOOTASM.BAS'
valid=[
 ('EMPTY','',b''),
 ('NUMBERS','DB 0,255\nDW 0,32768,65535',bytes.fromhex('00 FF 00 00 00 80 FF FF')),
 ('FIXED','RET\nCLD\nLODSB\nSTOSB',bytes.fromhex('C3 FC AC AA')),
 ('BACK','HERE:\nDB 1\nDW HERE',bytes.fromhex('01 00 01')),
 ('ALIAS','A:\nB:\nDW A,B',bytes.fromhex('00 01 00 01')),
 ('MEMORY','MOV BX,DATA\nMOV AL,[BX]\nMOV [DATA],AX\nDATA:\nDW 0',bytes.fromhex('BB 09 01 8A 07 89 06 09 01 00 00')),
 ('NEAR','HERE:\nCALL THERE\nJMP HERE\nTHERE:\nRET',bytes.fromhex('E8 03 00 E9 FA FF C3')),
 ('MAXIMUM','\n'.join(['DB '+','.join(['0']*40)]*102+['DB '+','.join(['0']*16)]),bytes(4096)),
 ('JPLUS','JE 181H',bytes.fromhex('74 7F')),
 ('JMINUS','DB '+','.join(['0']*100)+'\n'+'DB '+','.join(['0']*26)+'\nJE 100H',bytes(126)+bytes.fromhex('74 80')),
 ('LOWER',' ; note\n\tmov al,0ffh ; note',bytes.fromhex('B0 FF')),
]
# Keep source lines within the published 120-character bound.
valid=[v for v in valid if v[0] not in ('MAXIMUM','JMINUS')]+[
 ('MAXIMUM','\n'.join(['DB '+','.join(['0']*32)]*128),bytes(4096)),
 ('JMINUS','\n'.join(['DB '+','.join(['0']*32)]*3+['DB '+','.join(['0']*30),'JE 100H']),bytes(126)+bytes.fromhex('74 80')),
 ('LABELS','\n'.join(f'L{i}:\nDB 0' for i in range(256)),bytes(256)),
 ('LINES','\n'.join([';']*2000),b''),
]
for name,text,expected in valid:
    log=assemble(final,name,text)
    require('OK ' in log,f'{name}: {log}')
    require((WORK/(name+'.COM')).read_bytes()==expected,f'{name}: incorrect bytes')
    RESULT.append(f'PASS boundary {name}');print(RESULT[-1],flush=True)

invalid=[
 ('UNUSED','NOP','Unknown instruction'),('UNUSEDOR','OR AX,BX','Unknown instruction'),('UNUSEDX','XOR AX,BX','Unknown instruction'),('SIGNED','JL 100H','Unknown instruction'),
 ('BIGBYTE','DB 256','Byte out of range'),('BIGWORD','DW 65536','Number too large'),
 ('BADHEX','DB 12ZH','Bad number'),('NEGATIVE','DB -1','Bad label'),
 ('EXPR','DW 1+2','Bad number'),('BADLABEL','1NAME:\nDB 0','Bad label'),
 ('REGNAME','AX:\nDB 0','Reserved label'),('UNDEF','DW UNKNOWN','Undefined label'),
 ('DUP','A:\nA:','Duplicate label'),('TOOLONG',';'+('x'*120),'Source line too long'),
 ('TWOCOMMA','DB 1,,2','Missing value'),('TRAIL','DB 1,','Missing value'),
 ('NOARG','INT','Missing value'),('BADREG','MOV AX,AL','Register sizes differ'),
 ('MEMIMM','MOV [BX],1','Register required'),('MEMMEM','MOV [BX],[BX]','Register required'),
 ('BADMEM','MOV AL,[BX','Bad memory operand'),('NEWCPU','PUSHA','Unknown instruction'),
 ('JTOOFAR','JE 182H','Branch out of range'),('NEGJUMP','\n'.join(['DB '+','.join(['0']*32)]*3+['DB '+','.join(['0']*31),'JE 100H']),'Branch out of range'),
 ('OVERFLOW','\n'.join(['DB '+','.join(['0']*32)]*128+['DB 0']),'Program too large'),
 ('MANYLAB','\n'.join(f'L{i}:' for i in range(257)),'Too many labels'),
 ('MANYLINE','\n'.join([';']*2001),'Too many source lines'),
]
for name,text,diagnostic in invalid:
    # Keep the retained inspection copies within DOS 8.3 naming.
    name=name[:8]
    target=WORK/(name+'.COM');target.write_bytes(b'UNCHANGED')
    log=assemble(final,name,text)
    require(diagnostic in log and 'OK ' not in log,f'{name}: {log}')
    require(target.read_bytes()==b'UNCHANGED',f'{name}: changed rejected output')
    target.unlink()
    RESULT.append(f'PASS rejection {name}: {diagnostic}');print(RESULT[-1],flush=True)

# A successful shorter assembly must truncate an existing output.
assemble(final,'SHORT','DB 1,2,3,4')
log=assemble(final,'SHORT','DB 9')
require((WORK/'SHORT.COM').read_bytes()==b'\x09','Old output tail remained')
# Reader's viewer: includes empty file length, has no BASIC header interpretation.
for filename,expected in [('EMPTY.COM','Length: 0'),('T02.COM','41 42 43')]:
    out=io.BytesIO()
    with pcbasic.Session(input_streams=io.BytesIO((filename+'\r\n').encode()),output_streams=out,devices={'A':str(WORK)},current_device='A:') as s:
        s.execute('LOAD "VIEW.BAS"');s.execute('RUN')
    rendered=' '.join(out.getvalue().decode().split())
    require(expected in rendered,f'Viewer {filename}: {rendered}')
RESULT.append('PASS successful output truncation; viewer bytes and empty-file length')
(ROOT/'qa/test-results.txt').write_text('\n'.join(RESULT)+'\n')
print(f'PASS: {len(RESULT)} groups')

# Published complete examples, with hand-calculated expected encodings.
for name,expected,output,exitcode in [
 ('HELLO','BA 0C 01 B4 09 CD 21 B8 00 4C CD 21 48 45 4C 4C 4F 0D 0A 24','HELLO\r\n',0),
 ('COPYBYTE','BB 16 01 8A 07 88 06 17 01 8A 16 17 01 B4 02 CD 21 B8 00 4C CD 21 4D 00','M',0),
 ('FAIL','B8 01 4C CD 21','',1),
]:
    log=assemble(final,name)
    require('OK ' in log,f'{name}: {log}')
    code=(WORK/(name+'.COM')).read_bytes()
    require(code==bytes.fromhex(expected),f'{name}: published bytes differ')
    require(execute_com(code)==(output,exitcode),f'{name}: runtime differs')
    RESULT.append(f'PASS complete example {name}: exact bytes, output, return code')

# All supported condition opcodes, both arithmetic directions, and immediate groups.
encoding_cases=[
 ('BRANCHES','JB END\nJAE END\nJE END\nJNE END\nJBE END\nJA END\nEND:',
  '72 0A 73 08 74 06 75 04 76 02 77 00'),
 ('REGOPS','ADD AX,BX\nAND AX,BX\nSUB AX,BX\nCMP AX,BX',
  '03 C3 23 C3 2B C3 3B C3'),
 ('IMMOPS','ADD AX,1\nAND AX,3\nSUB AX,4\nCMP AX,6',
  '81 C0 01 00 81 E0 03 00 81 E8 04 00 81 F8 06 00'),
 ('BYTEREG','MOV AL,1\nMOV CL,2\nMOV DL,3\nMOV BL,4\nMOV AH,5\nMOV CH,6\nMOV DH,7\nMOV BH,8',
  'B0 01 B1 02 B2 03 B3 04 B4 05 B5 06 B6 07 B7 08'),
 ('WORDREG','MOV AX,1\nMOV CX,2\nMOV DX,3\nMOV BX,4\nMOV SP,5\nMOV BP,6\nMOV SI,7\nMOV DI,8',
  'B8 01 00 B9 02 00 BA 03 00 BB 04 00 BC 05 00 BD 06 00 BE 07 00 BF 08 00'),
]
for name,text,expected in encoding_cases:
    log=assemble(final,name,text)
    require('OK ' in log,f'{name}: {log}')
    require((WORK/(name+'.COM')).read_bytes()==bytes.fromhex(expected),f'{name}: encoding differs')
    RESULT.append(f'PASS instruction table {name} (inspect only)')

for value,byte in [('0',0),('65',65),('255',255),('256',None),('-1',None)]:
    out=io.BytesIO();before=(WORK/'BYTE.COM').read_bytes() if (WORK/'BYTE.COM').exists() else None
    with pcbasic.Session(input_streams=io.BytesIO((value+'\r\n').encode()),output_streams=out,devices={'A':str(WORK)},current_device='A:') as s:
        s.execute('LOAD "BYTE.BAS"');s.execute('RUN')
    log=out.getvalue().decode()
    if byte is None:
        require('Bad byte' in log and (WORK/'BYTE.COM').read_bytes()==before,f'BYTE.BAS rejection {value}')
    else:require('Wrote' in log and (WORK/'BYTE.COM').read_bytes()==bytes([byte]),f'BYTE.BAS {value}')
RESULT.append('PASS first byte writer: 0, 65, 255; 256 and negative rejected without changing output')
out=io.BytesIO()
missing=WORK/'MISSING.COM'
if missing.exists():missing.unlink()
with pcbasic.Session(input_streams=io.BytesIO(b'MISSING.COM\r\n'),output_streams=out,devices={'A':str(WORK)},current_device='A:') as s:
    s.execute('LOAD "VIEW.BAS"');s.execute('RUN')
require('Cannot read file' in out.getvalue().decode() and not missing.exists(),'Viewer created missing file')
RESULT.append('PASS viewer: missing file reports error and is not created')
(ROOT/'qa/test-results.txt').write_text('\n'.join(RESULT)+'\n')
print(f'PASS FINAL: {len(RESULT)} groups')
