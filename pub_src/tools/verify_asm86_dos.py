"""Run BASIC-produced ASM86 and its two generations under DOS 3.10.
Historical DOS files stay in local QA; they are never packaged for readers.
"""
from pathlib import Path
import subprocess,shutil,socket,time
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa/asm86';W=ROOT/'workbench/asm86'
boot=Q/'boot.img';disk=Q/'work.img';scratch=Q/'dos';scratch.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'qa/dos-original.img',boot)
subprocess.run(['mformat','-C','-f','360','-i',str(disk),'::'],check=True)
def copy(path,dest=None,image=disk):subprocess.run(['mcopy','-o','-i',str(image),str(path),'::'+(dest or path.name)],check=True)
def dos(name,text):
 p=scratch/name;p.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'));return p
for name in ['ASM86.COM','ASM86.ASM']:copy(W/name)
copy(W/'ASM86.ASM','SELF.ASM');copy(W/'ASM86.ASM','AGAIN.ASM')
copy(ROOT/'workbench/bootasm/CHECK.BAT')
for name in ['SELF','AGAIN']:copy(dos(name+'.IN',name+'\n'))
copy(dos('NO.IN','N\n'))
copy(dos('BAD.IN','BAD\n'));copy(dos('BAD.ASM','MOV AX,AL\n'))
cmds=['ECHO OFF','B:',r'A:\COMMAND /C CHECK ASM86 <SELF.IN >SELF.LOG',r'A:\COMMAND /C CHECK SELF <AGAIN.IN >AGAIN.LOG',r'A:\COMP ASM86.COM SELF.COM <NO.IN >CMP1.LOG',r'A:\COMP SELF.COM AGAIN.COM <NO.IN >CMP2.LOG',r'A:\COMMAND /C CHECK ASM86 <BAD.IN >BAD.LOG','ECHO DONE >DONE.TXT']
copy(dos('AUTOEXEC.BAT','\n'.join(cmds)+'\n'),image=boot)
monitor='/tmp/bootexp-asm86-monitor.sock'
Path(monitor).unlink(missing_ok=True)
p=subprocess.Popen(['qemu-system-i386','-machine','pc','-m','16M','-drive',f'file={boot},format=raw,if=floppy,index=0','-drive',f'file={disk},format=raw,if=floppy,index=1','-boot','a','-display','none','-monitor','unix:'+monitor+',server=on,wait=off','-serial','none','-no-reboot'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
try:
 for attempt in range(240):
  done=subprocess.run(['mtype','-i',str(disk),'::DONE.TXT'],capture_output=True)
  if done.returncode==0:break
  if p.poll() is not None:raise RuntimeError(p.stderr.read().decode())
  time.sleep(.5)
 else:raise RuntimeError('DOS test did not finish within 120 seconds')
 s=socket.socket(socket.AF_UNIX);s.connect(monitor);s.sendall(b'quit\n');s.close();p.wait(timeout=10)
 for name in ['SELF.COM','AGAIN.COM','SELF.LOG','AGAIN.LOG','CMP1.LOG','CMP2.LOG','BAD.LOG']:
  subprocess.run(['mcopy','-o','-i',str(disk),'::'+name,str(scratch/name)],check=True)
 expected=(W/'ASM86.COM').read_bytes()
 assert (scratch/'SELF.COM').read_bytes()==expected
 assert (scratch/'AGAIN.COM').read_bytes()==expected
 for name in ['SELF.LOG','AGAIN.LOG']:
  raw=(scratch/name).read_bytes();assert f'OK {len(expected):05} bytes'.encode() in raw and b'PASS' in raw,(name,raw)
 assert b'ERROR 00001 CODE 1' in (scratch/'BAD.LOG').read_bytes() and b'FAIL' in (scratch/'BAD.LOG').read_bytes()
 for name in ['CMP1.LOG','CMP2.LOG']:assert b'Files compare ok' in (scratch/name).read_bytes(),(name,(scratch/name).read_bytes())
 (Q/'dos-results.txt').write_text('PASS DOS 3.10: BASIC-produced ASM86 builds SELF.COM; SELF builds AGAIN.COM; both match every byte of the first executable.\nPASS DOS COMP: both generations report Files compare ok.\nPASS DOS CHECK: successful builds report PASS; unequal register widths report ERROR 00001 CODE 1 and FAIL.\n')
 print((Q/'dos-results.txt').read_text())
finally:
 if p.poll() is None:p.terminate();p.wait(timeout=10)
