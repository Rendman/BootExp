"""Verify native builds, allocated workspace, and the bootstrap ladder under DOS 3.10."""
from project_paths import directory_name
from pathlib import Path
import subprocess,shutil,socket,time
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa/asm86';W=ROOT/'workbench/asm86';scratch=Q/'dos';scratch.mkdir(exist_ok=True)
def dos(name,text):
 p=scratch/name;p.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'));return p
def vm(group,copies,commands,outputs):
 boot=Q/(group+'-boot.img');disk=Q/(group+'-work.img');shutil.copyfile(ROOT/'qa/dos-original.img',boot)
 subprocess.run(['mformat','-C','-f','360','-i',str(disk),'::'],check=True)
 def copy(p,name=None,image=disk):subprocess.run(['mcopy','-o','-i',str(image),str(p),'::'+(name or p.name)],check=True)
 copy(ROOT/'workbench/bootasm/CHECK.BAT')
 for p,name in copies:copy(p,name)
 copy(dos('CONFIG.SYS','FILES=30\n'),image=boot)
 copy(dos('AUTOEXEC.BAT','ECHO OFF\nB:\n'+'\n'.join(commands)+'\nECHO DONE >DONE.TXT\n'),image=boot)
 monitor='/tmp/bootexp-asma-'+group+'.sock';Path(monitor).unlink(missing_ok=True)
 p=subprocess.Popen(['qemu-system-i386','-machine','pc','-m','16M','-drive',f'file={boot},format=raw,if=floppy,index=0','-drive',f'file={disk},format=raw,if=floppy,index=1','-boot','a','-display','none','-monitor','unix:'+monitor+',server=on,wait=off','-serial','none','-no-reboot'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 try:
  for attempt in range(360):
   if subprocess.run(['mtype','-i',str(disk),'::DONE.TXT'],capture_output=True).returncode==0:break
   if p.poll() is not None:raise RuntimeError(p.stderr.read().decode())
   time.sleep(.5)
  else:raise RuntimeError(group+' did not finish within 180 seconds')
  s=socket.socket(socket.AF_UNIX);s.connect(monitor);s.sendall(b'quit\n');s.close();p.wait(timeout=10)
  dest=scratch/group;dest.mkdir(exist_ok=True)
  for name in outputs:subprocess.run(['mcopy','-o','-i',str(disk),'::'+name,str(dest/name)],check=True)
  return dest
 finally:
  if p.poll() is None:p.terminate();p.wait(timeout=10)

records=[]
copies=[(ROOT/'workbench/asm0/ASM86.COM','ASM86.COM'),(W/'ASMA0.ASM','ASMA0.ASM'),(W/'ASM86A.ASM','ASM86A.ASM'),(ROOT/'workbench/ir86/IR86.ASM','IR86.ASM'),(ROOT/'workbench/rill0/RILL.IR','RILL.IR'),(ROOT/'workbench/rill0/HELLO.RIL','RLSRC.RIL')]
for name in ['ASMA0','RILL','RLHI']:copies.append((dos(name+'.IN',name+'\n'),name+'.IN'))
commands=[r'A:\COMMAND /C CHECK ASM86 <ASMA0.IN >SEED.BLD','COPY ASMA0.ASM SOURCE.ASM >NUL',r'A:\COMMAND /C CHECK ASMA0 >SEED.SEL','COPY RESULT.COM SGEN1.COM >NUL',r'A:\COMMAND /C CHECK SGEN1 >SEED.TWO','COPY RESULT.COM SGEN2.COM >NUL','COPY ASM86A.ASM SOURCE.ASM >NUL',r'A:\COMMAND /C CHECK ASMA0 >FULL.BLD','COPY RESULT.COM AKEEP.COM >NUL',r'A:\COMMAND /C CHECK AKEEP >FULL.SEL','COPY RESULT.COM FGEN1.COM >NUL',r'A:\COMMAND /C CHECK FGEN1 >FULL.TWO','COPY RESULT.COM FGEN2.COM >NUL','COPY IR86.ASM SOURCE.ASM >NUL',r'A:\COMMAND /C CHECK AKEEP >IR.BLD','COPY RESULT.COM IR86.COM >NUL',r'A:\COMMAND /C CHECK IR86 <RILL.IN >RILL.TRN','COPY RILL.ASM SOURCE.ASM >NUL',r'A:\COMMAND /C CHECK AKEEP >RILL.BLD','COPY RESULT.COM RILL.COM >NUL','COPY RLSRC.RIL SOURCE.RIL >NUL',r'A:\COMMAND /C CHECK RILL >RLHI.CMP','COPY RESULT.IR RLHI.IR >NUL',r'A:\COMMAND /C CHECK IR86 <RLHI.IN >RLHI.TRN','COPY RLHI.ASM SOURCE.ASM >NUL',r'A:\COMMAND /C CHECK AKEEP >RLHI.BLD','COPY RESULT.COM RLHI.COM >NUL',r'A:\COMMAND /C CHECK RLHI >RLHI.OUT']
outputs=['ASMA0.COM','SGEN1.COM','SGEN2.COM','AKEEP.COM','FGEN1.COM','FGEN2.COM','IR86.COM','RILL.COM','RLHI.COM','SEED.BLD','SEED.SEL','SEED.TWO','FULL.BLD','FULL.SEL','FULL.TWO','IR.BLD','RILL.TRN','RILL.BLD','RLHI.CMP','RLHI.TRN','RLHI.BLD','RLHI.OUT']
for name in ['HELLO','FRAME','BRIDGE','COPYTEXT']:
 copies.append((W/(name+'.ASM'),name+'.ASM'));commands += [f'COPY {name}.ASM SOURCE.ASM >NUL',fr'A:\COMMAND /C CHECK AKEEP >{name}.BLD',f'COPY RESULT.COM {name}.COM >NUL',fr'A:\COMMAND /C CHECK {name} >{name}.OUT'];outputs.extend([name+'.COM',name+'.BLD',name+'.OUT'])
b=vm('build',copies,commands,outputs)
for name in ['ASMA0','SGEN1','SGEN2']:assert (b/(name+'.COM')).read_bytes()==(W/'ASMA0.COM').read_bytes(),name
for name in ['AKEEP','FGEN1','FGEN2']:assert (b/(name+'.COM')).read_bytes()==(W/'ASM86A.COM').read_bytes(),name
for folder,name in [('ir86','IR86'),('rill','RILL')]:assert (b/(name+'.COM')).read_bytes()==(ROOT/'workbench'/directory_name(folder)/(name+'.COM')).read_bytes(),name
for name in outputs:
 if name.endswith(('.BLD','.SEL','.TWO','.TRN','.CMP','.OUT')):assert b'PASS' in (b/name).read_bytes(),name
assert b'HI' in (b/'RLHI.OUT').read_bytes()
records += ['PASS DOS 3.10 ASM86 builds the seed; two seed self-builds match the initial executable','PASS DOS 3.10 seed builds ASM86A; two allocated-workspace self-builds match','PASS DOS 3.10 ASM86A builds IR86; IR86 and ASM86A build RILL; RILL -> IR86 -> ASM86A -> COM displays HI']
for name,out in [('HELLO',b'Hello\r\n'),('FRAME',b'A'),('BRIDGE',b'B'),('COPYTEXT',b'Hi')]:
 assert (b/(name+'.COM')).read_bytes()==(W/(name+'.COM')).read_bytes(),name
 assert out in (b/(name+'.OUT')).read_bytes(),name
 records.append('PASS DOS 3.10 '+name+': exact machine bytes, expected runtime output, and PASS')

# A separate 360 KB work disk holds the large source fixtures without duplicating them.
long=dos('LONG.ASM',';\r\n'*65536+'DB 1\r\n')
symbols=dos('SYMBOLS.ASM',''.join(f'S{i}:\n' for i in range(8192))+'DW S0,S8191\n')
large=dos('LARGE.ASM','RESB 61184\n');over=dos('OVER.ASM','RESB 61185\n')
lowmem='''CLD
MOV AX,CS
MOV ES,AX
MOV BX,1000H
MOV AH,4AH
INT 21H
JB FAILED
MOV BX,2800H
MOV AH,48H
INT 21H
JB FAILED
MOV [HOGSEG],AX
MOV AX,CS
MOV [TAILSEG],AX
MOV [FCB1SEG],AX
MOV [FCB2SEG],AX
MOV ES,AX
MOV [SAVESP],SP
MOV DX,CHILD
MOV BX,PARAMS
MOV AX,4B00H
INT 21H
MOV DX,CS
MOV DS,DX
MOV ES,DX
MOV SS,DX
MOV SP,[SAVESP]
JB FAILED
MOV AH,4DH
INT 21H
CMP AL,1
JNE FAILED
MOV AX,[HOGSEG]
MOV ES,AX
MOV AH,49H
INT 21H
JB FAILED
MOV DX,OKTEXT
MOV AH,9
INT 21H
MOV AX,4C00H
INT 21H
FAILED:
MOV AX,4C01H
INT 21H
CHILD:
DB "ASM86A.COM",0
PARAMS:
DW 0
DW TAIL
TAILSEG:
DW 0
DW 5CH
FCB1SEG:
DW 0
DW 6CH
FCB2SEG:
DW 0
TAIL:
DB 0,13
HOGSEG:
DW 0
SAVESP:
DW 0
OKTEXT:
DB "LOW MEMORY PASS",13,10,36
'''
# This diagnostic is also encoded only by the published assembler.
import sys
sys.path.insert(0,str(ROOT/'qa/asm86'))
from machine import run_assembler
hog=run_assembler((W/'ASM86A.COM').read_bytes(),lowmem);assert hog.exitcode==0,hog.output
hogfile=scratch/'LOWMEM.COM';hogfile.write_bytes(hog.files['RESULT.COM']);dos('LOWMEM.ASM',lowmem)
copies=[(W/'ASM86A.COM','ASM86A.COM'),(long,'LONG.ASM'),(symbols,'SYMBOLS.ASM'),(large,'LARGE.ASM'),(over,'OVER.ASM'),(hogfile,'LOWMEM.COM'),(dos('OLD.SAV','OLD RESULT\n'),'OLD.SAV'),(dos('SMALL.ASM','RET\n'),'SMALL.ASM')]
commands=['REN LONG.ASM SOURCE.ASM',r'A:\COMMAND /C CHECK ASM86A >LONG.LOG','COPY RESULT.COM LONG.BIN >NUL','DEL SOURCE.ASM','REN SYMBOLS.ASM SOURCE.ASM',r'A:\COMMAND /C CHECK ASM86A >SYMBOL.LOG','COPY RESULT.COM SYMBOL.BIN >NUL','DEL SOURCE.ASM','REN LARGE.ASM SOURCE.ASM',r'A:\COMMAND /C CHECK ASM86A >LARGE.LOG','COPY RESULT.COM LARGE.BIN >NUL','DEL RESULT.COM','DEL SOURCE.ASM','REN OVER.ASM SOURCE.ASM','COPY OLD.SAV RESULT.COM >NUL',r'A:\COMMAND /C CHECK ASM86A >OVER.LOG','COPY RESULT.COM KEPT.BIN >NUL','DEL SOURCE.ASM','REN SMALL.ASM SOURCE.ASM',r'A:\COMMAND /C CHECK LOWMEM >MEMORY.LOG','COPY RESULT.COM MEMKEPT.BIN >NUL']
c=vm('capacity',copies,commands,['LONG.LOG','LONG.BIN','SYMBOL.LOG','SYMBOL.BIN','LARGE.LOG','LARGE.BIN','OVER.LOG','KEPT.BIN','MEMORY.LOG','MEMKEPT.BIN'])
assert (c/'LONG.BIN').read_bytes()==b'\x01' and b'PASS' in (c/'LONG.LOG').read_bytes()
assert (c/'SYMBOL.BIN').read_bytes()==bytes.fromhex('00010001') and b'PASS' in (c/'SYMBOL.LOG').read_bytes()
assert (c/'LARGE.BIN').read_bytes()==bytes(61184) and b'PASS' in (c/'LARGE.LOG').read_bytes()
assert b'CODE 5' in (c/'OVER.LOG').read_bytes() and b'FAIL' in (c/'OVER.LOG').read_bytes() and (c/'KEPT.BIN').read_bytes()==b'OLD RESULT\r\n'
assert b'ERROR 0000000000 CODE 7' in (c/'MEMORY.LOG').read_bytes() and b'LOW MEMORY PASS' in (c/'MEMORY.LOG').read_bytes()
assert (c/'MEMKEPT.BIN').read_bytes()==b'OLD RESULT\r\n'
records += ['PASS DOS 3.10 streamed source beyond 65535 lines, all 8192 symbols, and an exact 61184-byte image','PASS DOS 3.10 image overflow reports FAIL and preserves the prior result','PASS DOS 3.10 a native parent holds 160 KiB, the child reports memory shortage, and prior output remains unchanged']
(Q/'dos-results.txt').write_text('\n'.join(records)+'\n');print('\n'.join(records))
