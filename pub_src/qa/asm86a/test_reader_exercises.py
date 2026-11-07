"""Execute the large text exercises at the precise published stopping points."""
from machine import *
import json,re
W=ROOT/'workbench/asm86a';Q=ROOT/'qa/asm86a';C=ROOT/'site/content/bootstrap/asm86a';logs=[]
for n,limit in [(9,2048),(17,8192)]:
 image=(W/f'A{n:02}.COM').read_bytes()
 for count in [limit,limit+1]:
  source=''.join(f'S{i}:\r\n' for i in range(count))+f'DW S0,S{count-1}\r\n\x1a'
  r=run_assembler(image,source,{'RESULT.COM':b'OLD'})
  if count==limit:assert r.exitcode==0 and r.files['RESULT.COM']==bytes.fromhex('00010001'),(n,r.output)
  else:assert r.exitcode==1 and f'ERROR {count:05} CODE 5'.encode() in r.output and r.files['RESULT.COM']==b'OLD',(n,r.output)
 logs.append(f'PASS A{n:02} SYMS.BAS source: exact {limit}-symbol result and definition {limit+1} rejection')
image=(W/'A19.COM').read_bytes()
for tail in ['DB 1','UNKNOWN']:
 source=';\r\n'*65536+tail+'\r\n\x1a';r=run_assembler(image,source,{'RESULT.COM':b'OLD'})
 if tail=='DB 1':assert r.exitcode==0 and r.files['RESULT.COM']==b'\x01',r.output
 else:assert r.exitcode==1 and b'ERROR 0000065537 CODE 1' in r.output and r.files['RESULT.COM']==b'OLD',r.output
logs.append('PASS A19 LONGSRC.BAS source: 65537 physical lines, exact byte, full error line and preservation')
image=(W/'A23.COM').read_bytes()
for size in [61184,61185]:
 r=run_assembler(image,f'RESB {size}\r\n',{'RESULT.COM':b'OLD'})
 if size==61184:assert r.exitcode==0 and r.files['RESULT.COM']==bytes(size),r.output
 else:assert r.exitcode==1 and b'ERROR 0000000001 CODE 5' in r.output and r.files['RESULT.COM']==b'OLD',r.output
logs.append('PASS A23 exact image boundary and overflow rejection')
# The assembler collection stops at its own self-assembly handoff.
text=(C/'41-the-bootstrap-ladder.md').read_text()
for command in ['CHECK ASM1','CHECK A0','CHECK A1','COMP A0.COM A1.COM <NO.TXT','COMP A0.COM A2.COM <NO.TXT']:assert command in text
assert str(len((W/'ASM86A.COM').read_bytes())) in text
logs.append('PASS printed assembler handoff preserves all builders and compares both self-generations')
(Q/'reader-results.txt').write_text('\n'.join(logs)+'\n');print('\n'.join(logs))
