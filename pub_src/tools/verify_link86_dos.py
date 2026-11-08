"""Execute the RILL-built linker and its two linked programs under DOS 3.10."""
from pathlib import Path
import subprocess,shutil,socket,time
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa/link86';W=ROOT/'workbench/link86';scratch=Q/'dos';scratch.mkdir(exist_ok=True)
boot=Q/'boot.img';disk=Q/'work.img';shutil.copyfile(ROOT/'qa/dos-original.img',boot)
subprocess.run(['mformat','-C','-f','360','-i',str(disk),'::'],check=True)
def copy(p,image=disk):subprocess.run(['mcopy','-o','-i',str(image),str(p),'::'+p.name],check=True)
def dos(name,s):p=scratch/name;p.write_bytes(s.replace('\n','\r\n').encode('ascii'));return p
for name in ['LINK86.COM','M09.OBJ','U09.OBJ','M10.OBJ','U10.OBJ','X09.OBJ']:copy(W/name)
copy(ROOT/'workbench/bootasm/CHECK.BAT')
cmds=['ECHO OFF','B:','COPY M09.OBJ MAIN.OBJ >NUL','COPY U09.OBJ UTIL.OBJ >NUL',r'A:\COMMAND /C CHECK LINK86 >REL.LOG','COPY RESULT.COM REL.COM >NUL',r'A:\COMMAND /C CHECK REL >REL.RUN','COPY M10.OBJ MAIN.OBJ >NUL','COPY U10.OBJ UTIL.OBJ >NUL',r'A:\COMMAND /C CHECK LINK86 >ABS.LOG','COPY RESULT.COM ABS.COM >NUL',r'A:\COMMAND /C CHECK ABS >ABS.RUN','COPY X09.OBJ MAIN.OBJ >NUL','COPY U09.OBJ UTIL.OBJ >NUL',r'A:\COMMAND /C CHECK LINK86 >BAD.LOG','ECHO DONE >DONE.TXT']
copy(dos('AUTOEXEC.BAT','\n'.join(cmds)+'\n'),boot)
monitor='/tmp/bootexp-link86.sock';Path(monitor).unlink(missing_ok=True)
p=subprocess.Popen(['qemu-system-i386','-machine','pc','-m','16M','-drive',f'file={boot},format=raw,if=floppy,index=0','-drive',f'file={disk},format=raw,if=floppy,index=1','-boot','a','-display','none','-monitor','unix:'+monitor+',server=on,wait=off','-serial','none','-no-reboot'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
try:
 for _ in range(240):
  if subprocess.run(['mtype','-i',str(disk),'::DONE.TXT'],capture_output=True).returncode==0:break
  if p.poll() is not None:raise RuntimeError(p.stderr.read().decode())
  time.sleep(.5)
 else:raise RuntimeError('DOS linker check did not finish within 120 seconds')
 s=socket.socket(socket.AF_UNIX);s.connect(monitor);s.sendall(b'quit\n');s.close();p.wait(timeout=10)
 def get(name):return subprocess.check_output(['mtype','-i',str(disk),'::'+name])
 relative=bytes.fromhex('E8 04 00 B4 4C CD 21 33 C0 C3');absolute=bytes.fromhex('BA 0C 01 B4 09 CD 21 B8 00 4C CD 21 48 49 0D 0A 24')
 assert get('REL.COM')==relative and get('ABS.COM')==get('RESULT.COM')==absolute
 for name,size in [('REL.LOG',10),('ABS.LOG',17)]:
  raw=get(name);assert f'OK RESULT.COM {size:05} bytes'.encode() in raw and b'PASS' in raw and b'FAIL' not in raw,(name,raw)
 assert b'PASS' in get('REL.RUN') and b'HI\r\n' in get('ABS.RUN') and b'PASS' in get('ABS.RUN')
 raw=get('BAD.LOG');assert b'CODE 00003' in raw and b'FAIL' in raw and b'OK ' not in raw,raw
 logs=['PASS DOS 3.10: LINK86 emits the exact cross-module call image; linked program returns zero','PASS DOS 3.10: LINK86 resolves exported text; linked program displays HI and returns zero','PASS DOS 3.10: unresolved reference reports failure and preserves the accepted image']
 (Q/'dos-results.txt').write_text('\n'.join(logs)+'\n');print('\n'.join(logs))
finally:
 if p.poll() is None:p.terminate();p.wait(timeout=10)
