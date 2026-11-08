"""Check the three printed complete examples and their rejection edits."""
from pathlib import Path
from dos_machine import DosMachine,assemble
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/asm0';image=(W/'ASM86.COM').read_bytes()
cases=[('HELLO',20,'Hello\r\n','MOV DX,MESSAGE','MOV DX,MISSING',1,3),('MEMORY',24,'M','MOV AL,[BX]','MOV AL,[SI]',2,3),('COUNT',17,'012','JB AGAIN','JB 400H',7,4)]
lines=[]
for name,size,output,old,new,line,code in cases:
 source=(W/(name+'.ASM')).read_bytes();result=assemble(image,source,name)
 assert result.exitcode==0,(name,result.output)
 program=result.files['RESULT.COM'];assert len(program)==size,(name,len(program))
 executed=DosMachine().run(program)
 assert executed.exitcode==0 and executed.output.decode('ascii')==output,(name,executed.output)
 bad=assemble(image,source.decode('ascii').replace(old,new),'BAD')
 assert bad.exitcode==1 and f'ERROR {line:05} CODE {code}'.encode() in bad.output,(name,bad.output)
 (W/(name+'.COM')).write_bytes(program)
 lines.append(f'PASS {name}: {size} bytes, expected display/status, exact rejection diagnostic')
(ROOT/'qa/asm0/example-results.txt').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
