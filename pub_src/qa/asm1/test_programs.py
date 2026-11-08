"""Run the seed collection's published programs with the verified native seed."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'qa/asm86'))
from machine import run_assembler,AssemblerMachine,assemble
W=ROOT/'workbench/asm1';Q=ROOT/'qa/asm1';seed=(ROOT/'workbench/asm86/ASMA0.COM').read_bytes();records=[];logs=[]
first=assemble((ROOT/'workbench/asm0/ASM86.COM').read_bytes(),(W/'ASMA0.ASM').read_bytes(),'ASMA0')
assert first.exitcode==0 and first.files['ASMA0.COM']==seed
for _ in range(2):
 r=run_assembler(seed,(W/'ASMA0.ASM').read_bytes());assert r.exitcode==0 and r.files['RESULT.COM']==seed
logs.append('PASS ASMA0: unchanged ASM86 builds the seed; two seed self-builds reproduce 3342 bytes')
for name,expected,before,after,code in [('HELLO',b'Hello\r\n','INT 21H','INT 256',4),('MEMORY',b'M','MOV AL,[BX]','MOV AX,AL',1),('COUNT',b'012','JB AGAIN','JB 400H',4)]:
 source=(W/(name+'.ASM')).read_text();r=run_assembler(seed,source);assert r.exitcode==0,(name,r.output)
 image=r.files['RESULT.COM'];target=AssemblerMachine().run(image);assert target.exitcode==0 and target.output==expected,(name,target.output)
 rejected=run_assembler(seed,source.replace(before,after,1),{'RESULT.COM':image});line=next(i for i,l in enumerate(source.splitlines(),1) if before in l)
 assert rejected.exitcode==1 and rejected.output==f'ERROR {line:05} CODE {code}\r\n'.encode() and rejected.files['RESULT.COM']==image,(name,rejected.output)
 records.append(dict(name=name,output=expected.decode(),binary_bytes=len(image),hex=image[:32].hex(' ').upper(),bad_before=before,bad_after=after,bad_line=line,bad_code=code))
 logs.append('PASS '+name+': seed assembly, exact output/status, rejection and preservation')
(Q/'examples.json').write_text(json.dumps(records,indent=2)+'\n');(Q/'program-results.txt').write_text('\n'.join(logs)+'\n');print('\n'.join(logs))
