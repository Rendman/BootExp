"""Run the published ASM86 -> IR86 -> program pipeline under local DOS 3.10."""
from pathlib import Path
import subprocess,shutil,socket,time,json
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa/ir86';W=ROOT/'workbench/ir86'
boot=Q/'boot.img';disk=Q/'work.img';scratch=Q/'dos';scratch.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'qa/dos-original.img',boot)
subprocess.run(['mformat','-C','-f','360','-i',str(disk),'::'],check=True)
def copy(p,dest=None,image=disk):subprocess.run(['mcopy','-o','-i',str(image),str(p),'::'+(dest or p.name)],check=True)
def dos(name,text):
 p=scratch/name;p.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'));return p
copy(ROOT/'workbench/asm86/ASM86.COM');copy(ROOT/'workbench/bootasm/CHECK.BAT')
copy(W/'IR86.ASM');copy(W/'IR86.COM','IRKEEP.COM')
copy(dos('IR86.IN','IR86\n'))
names=['HELLO','COUNT','BYTES','ECHOIR','COPYFILE']
commands=['ECHO OFF','B:',r'A:\COMMAND /C CHECK ASM86 <IR86.IN >BUILD.LOG']
for n in names:
 copy(W/(n+'.IR'));copy(dos(n+'.IN',n+'\n'))
 commands += [fr'A:\COMMAND /C CHECK IR86 <{n}.IN >{n}.TRN',fr'A:\COMMAND /C CHECK ASM86 <{n}.IN >{n}.BLD',fr'A:\COMMAND /C CHECK {n}'+(' <KEY.TXT' if n=='ECHOIR' else '')+f' >{n}.OUT']
copy(dos('IN.TXT','An IR86 file copy.\n'));copy(dos('KEY.TXT','IR86 echo.\n'))
copy(dos('CONFIG.SYS','FILES=30\n'),image=boot)
binary=scratch/'BIN.TXT';binary.write_bytes(bytes(range(256)));copy(binary)
copy(dos('BAD.IR','LABEL MAIN\nPOP\n'));copy(dos('BAD.IN','BAD\n'));copy(dos('BAD.ASM','OLD ASSEMBLY\n'))
commands += [r'A:\COMMAND /C CHECK IR86 <BAD.IN >BAD.LOG','REN IN.TXT HOLD.TXT',r'A:\COMMAND /C CHECK COPYFILE >MISSING.OUT','REN HOLD.TXT IN.TXT','REN OUT.TXT TEXT.TXT','REN IN.TXT TEXTIN.TXT','REN BIN.TXT IN.TXT',r'A:\COMMAND /C CHECK COPYFILE >BINARY.OUT',r'A:\COMMAND /C CHECK ECHOIR <IN.TXT >ECHOIR.BIN','ECHO DONE >DONE.TXT']
copy(dos('AUTOEXEC.BAT','\n'.join(commands)+'\n'),image=boot)
monitor='/tmp/bootexp-ir86-monitor.sock';Path(monitor).unlink(missing_ok=True)
p=subprocess.Popen(['qemu-system-i386','-machine','pc','-m','16M','-drive',f'file={boot},format=raw,if=floppy,index=0','-drive',f'file={disk},format=raw,if=floppy,index=1','-boot','a','-display','none','-monitor','unix:'+monitor+',server=on,wait=off','-serial','none','-no-reboot'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
try:
 for attempt in range(240):
  done=subprocess.run(['mtype','-i',str(disk),'::DONE.TXT'],capture_output=True)
  if done.returncode==0:break
  if p.poll() is not None:raise RuntimeError(p.stderr.read().decode())
  time.sleep(.5)
 else:raise RuntimeError('DOS IR pipeline did not finish within 120 seconds')
 s=socket.socket(socket.AF_UNIX);s.connect(monitor);s.sendall(b'quit\n');s.close();p.wait(timeout=10)
 outputs=['IR86.COM','BUILD.LOG','IN.TXT','OUT.TXT','TEXT.TXT','TEXTIN.TXT','BAD.LOG','BAD.ASM','MISSING.OUT','BINARY.OUT','ECHOIR.BIN']+[n+ext for n in names for ext in ['.ASM','.COM','.TRN','.BLD','.OUT']]
 for name in outputs:subprocess.run(['mcopy','-o','-i',str(disk),'::'+name,str(scratch/name)],check=True)
 assert (scratch/'IR86.COM').read_bytes()==(W/'IR86.COM').read_bytes(),'DOS-built translator differs'
 assert f'OK {len((W/"IR86.COM").read_bytes()):05} bytes'.encode() in (scratch/'BUILD.LOG').read_bytes() and b'PASS' in (scratch/'BUILD.LOG').read_bytes()
 records=[]
 expected={'HELLO':b'HI','COUNT':b'012','BYTES':b'OK','ECHOIR':b'IR86 echo.\r\n','COPYFILE':b''}
 for n in names:
  assert (scratch/(n+'.ASM')).read_bytes()==(W/(n+'.ASM')).read_bytes(),n+' target text differs'
  assert (scratch/(n+'.COM')).read_bytes()==(W/(n+'.COM')).read_bytes(),n+' target bytes differ'
  for ext in ['.TRN','.BLD','.OUT']:assert b'PASS' in (scratch/(n+ext)).read_bytes(),(n,ext)
  if expected[n]:assert expected[n] in (scratch/(n+'.OUT')).read_bytes(),n+' display differs'
  records.append('PASS DOS 3.10 '+n+': native IR translation, native ASM86 assembly, expected runtime and PASS status')
 assert (scratch/'OUT.TXT').read_bytes()==(scratch/'IN.TXT').read_bytes(),'DOS copied file differs'
 assert (scratch/'OUT.TXT').read_bytes()==bytes(range(256)),'DOS binary copy differs'
 assert bytes(range(256)) in (scratch/'ECHOIR.BIN').read_bytes(),'DOS byte stream differs'
 assert b'PASS' in (scratch/'ECHOIR.BIN').read_bytes()
 assert (scratch/'TEXT.TXT').read_bytes()==(scratch/'TEXTIN.TXT').read_bytes()==b'An IR86 file copy.\r\n'
 assert b'FAIL' in (scratch/'MISSING.OUT').read_bytes() and b'PASS' in (scratch/'BINARY.OUT').read_bytes()
 assert b'IR ERROR 00002 CODE 4' in (scratch/'BAD.LOG').read_bytes() and b'FAIL' in (scratch/'BAD.LOG').read_bytes()
 assert (scratch/'BAD.ASM').read_bytes()==b'OLD ASSEMBLY\r\n'
 records.insert(0,'PASS DOS 3.10 ASM86 builds IR86.COM matching every byte of the bootstrap-built translator')
 records+=['PASS DOS file and stream bindings preserve text and all 256 byte values; missing input reports FAIL','PASS DOS IR rejection reports exact diagnostic, FAIL, and preserves old assembly output']
 text='\n'.join(records)+'\n';(Q/'dos-results.txt').write_text(text);print(text)
finally:
 if p.poll() is None:p.terminate();p.wait(timeout=10)
