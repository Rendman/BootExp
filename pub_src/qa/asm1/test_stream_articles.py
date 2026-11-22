"""Execute the published block and line-count exercises with project binaries."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'qa/asm86'))
from machine import run_assembler

def source(n,statement='DB 65',last='DB 66'):
 # GW-BASIC sequential PRINT writes CR/LF; CLOSE adds the text EOF byte.
 return ((statement+'\r\n')*n+last+'\r\n').encode('ascii')+b'\x1a'

def run(number,text,old=b'ACCEPTED'):
 image=(ROOT/f'workbench/asm86/A{number:02}.COM').read_bytes()
 return run_assembler(image,files={'LONG.ASM':text,'RESULT.COM':old},command_line=' LONG.ASM RESULT.COM')

blocks=source(1024)
assert len(blocks)==7176
accepted=run(2,blocks)
expected=b'A'*1024+b'B'
assert accepted.exitcode==0 and accepted.files['RESULT.COM']==expected,accepted.output
assert accepted.output==b'OK RESULT.COM 01025 bytes\r\n'
rejected=run(2,source(1024,last='DB 256'),expected)
assert rejected.exitcode==1 and rejected.output==b'ERROR 01025 CODE 4\r\n',rejected.output
assert rejected.files['RESULT.COM']==expected
print('PASS A02: source spans refills; 1025 exact data bytes; final-statement error preserves output',flush=True)

copied=run(3,blocks)
assert copied.exitcode==0 and copied.files['ASMA.TMP']==blocks,copied.output
assert copied.files['RESULT.COM']==b'ACCEPTED'
assert copied.output==b'OK ASMA.TMP 07176 bytes\r\n'
print('PASS A03: seven full output blocks and an eight-byte tail match the entire input, including Control-Z',flush=True)

long=source(4000,';')
accepted=run(8,long)
assert accepted.exitcode==0 and accepted.files['RESULT.COM']==b'B',accepted.output
earlier=run(7,long)
assert earlier.exitcode==1 and earlier.output==b'ERROR 04001 CODE 5\r\n',earlier.output
assert earlier.files['RESULT.COM']==b'ACCEPTED'
print('PASS A08: 4001 physical lines succeed; A07 rejects the same source at its old limit',flush=True)

accepted=run(8,source(65534,';'))
assert accepted.exitcode==0 and accepted.files['RESULT.COM']==b'B',accepted.output
assert accepted.output==b'OK RESULT.COM 00001 bytes\r\n'
rejected=run(8,source(65535,';'),b'B')
assert rejected.exitcode==1 and rejected.output==b'ERROR 65535 CODE 5\r\n',rejected.output
assert rejected.files['RESULT.COM']==b'B' and 'ASMA.TMP' not in rejected.files
print('PASS A08: 65535 lines succeed; 65536 lines fail with a saturated report and preserve accepted output',flush=True)
