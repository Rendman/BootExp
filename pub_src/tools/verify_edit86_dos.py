"""Exercise the actual RILL-built editor on DOS 3.10 and BIOS text video."""
from pathlib import Path
import subprocess,shutil,socket,time
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa/edit86';W=ROOT/'workbench/edit86';scratch=Q/'dos';scratch.mkdir(exist_ok=True)
boot=Q/'boot.img';disk=Q/'work.img';shutil.copyfile(ROOT/'qa/dos-original.img',boot)
subprocess.run(['mformat','-C','-f','360','-i',str(disk),'::'],check=True)
def copy(p,image=disk):subprocess.run(['mcopy','-o','-i',str(image),str(p),'::'+p.name],check=True)
def dos(name,s):p=scratch/name;p.write_bytes(s.replace('\n','\r\n').encode('ascii'));return p
original=b''.join(f'row{i:05} document text\r\n'.encode() for i in range(3500))
p=scratch/'LARGE.TXT';p.write_bytes(original);copy(p)
copy(W/'EDIT86.COM');copy(ROOT/'workbench/bootasm/CHECK.BAT')
copy(dos('AUTOEXEC.BAT','ECHO OFF\nB:\nCOPY LARGE.TXT EDIT.TXT >NUL\nA:\\COMMAND /C CHECK EDIT86 >EDIT.LOG\nECHO DONE >DONE.TXT\n'),boot)
monitor='/tmp/bootexp-edit86.sock';Path(monitor).unlink(missing_ok=True)
process=subprocess.Popen(['qemu-system-i386','-machine','pc','-m','16M','-drive',f'file={boot},format=raw,if=floppy,index=0','-drive',f'file={disk},format=raw,if=floppy,index=1','-boot','a','-display','none','-monitor','unix:'+monitor+',server=on,wait=off','-serial','none','-no-reboot'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
try:
 for _ in range(100):
  if Path(monitor).exists():break
  time.sleep(.1)
 connection=socket.socket(socket.AF_UNIX);connection.settimeout(2);connection.connect(monitor)
 def receive():
  raw=b''
  while b'(qemu)' not in raw:raw+=connection.recv(4096)
  return raw
 receive()
 def command(s):connection.sendall(s.encode()+b'\n');return receive()
 def screen():
  target=scratch/'screen.bin';reply=command(f'pmemsave 0xb8000 4000 "{target}"')
  if not target.exists():raise RuntimeError(reply.decode(errors='replace'))
  return target.read_bytes()[::2]
 def waitfor(test,label):
  for _ in range(240):
   if test():return
   if process.poll() is not None:raise RuntimeError(process.stderr.read().decode())
   time.sleep(.25)
  raise RuntimeError('DOS editor timed out: '+label)
 waitfor(lambda:b'EDIT86 EDIT.TXT' in screen(),'initial document screen')
 initial=screen();assert initial[:8]==b'row00000'
 command('sendkey f7');time.sleep(.3)
 command('sendkey shift-1');time.sleep(.3)
 command('sendkey f2')
 waitfor(lambda:b'Saved EDIT.TXT.' in screen(),'saved document')
 saved=screen();assert b'!' in saved[:1920]
 command('sendkey f10')
 waitfor(lambda:subprocess.run(['mtype','-i',str(disk),'::DONE.TXT'],capture_output=True).returncode==0,'return to DOS')
 connection.sendall(b'quit\n');process.wait(timeout=10)
 def get(name):return subprocess.check_output(['mtype','-i',str(disk),'::'+name])
 assert get('EDIT.TXT')==original+b'!'
 log=get('EDIT.LOG');assert b'PASS' in log and b'FAIL' not in log,log
 lines=[f'PASS DOS 3.10: load {len(original)} bytes and paint the BIOS text screen', 'PASS DOS 3.10: move to document end beyond 64 KiB, insert, save, and verify every resulting byte', 'PASS DOS 3.10: return to DOS with CHECK PASS after releasing text and undo blocks']
 (Q/'dos-results.txt').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
finally:
 if process.poll() is None:process.terminate();process.wait(timeout=10)
