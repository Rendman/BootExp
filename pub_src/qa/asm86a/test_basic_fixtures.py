"""Execute the small reader BASIC text generators; they supply no executable bytes."""
from pathlib import Path
import sys,io,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/python-pcbasic207'));sys.path.insert(0,str(ROOT/'tools/python'))
import pcbasic
W=ROOT/'workbench/asm86a';Q=ROOT/'qa/asm86a';scratch=Q/'basic-fixtures';scratch.mkdir(exist_ok=True)
records=[]
for name in ['LONGSRC','SYMS']:
 source=(W/(name+'.BAS')).read_bytes();(scratch/(name+'.BAS')).write_bytes(source)
 assert len(source.splitlines())<=50
 out=io.BytesIO()
 with pcbasic.Session(input_streams=io.BytesIO(),output_streams=out,devices={'A':str(scratch)},current_device='A:') as session:
  session.execute('LOAD "'+name+'.BAS"');session.execute('RUN')
 assert b'SOURCE.ASM READY' in out.getvalue(),out.getvalue()
 text=(scratch/'SOURCE.ASM').read_bytes()
 if name=='LONGSRC':assert text==b';\r\n'*65536+b'DB 1\r\n\x1a'
 else:assert text==''.join(f'S{i}:\r\n' for i in range(8192)).encode()+b'DW S0,S8191\r\n\x1a'
 records.append('PASS '+name+': published BASIC generates the exact stated ASCII/CRLF source fixture')
(Q/'basic-fixture-results.txt').write_text('\n'.join(records)+'\n');print('\n'.join(records))
