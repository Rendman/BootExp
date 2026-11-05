"""Verify the IR-written RILL compiler and complete programs under local DOS 3.10."""
from pathlib import Path
import subprocess,shutil,socket,time,json
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa/rill';W=ROOT/'workbench/rill'
boot=Q/'boot.img';disk=Q/'work.img';scratch=Q/'dos';scratch.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'qa/dos-original.img',boot)
subprocess.run(['mformat','-C','-f','360','-i',str(disk),'::'],check=True)
def copy(p,dest=None,image=disk):subprocess.run(['mcopy','-o','-i',str(image),str(p),'::'+(dest or p.name)],check=True)
def dos(name,text):
 p=scratch/name;p.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'));return p
for folder,name,target in [('asm86','ASM86.COM','ASMKEEP.COM'),('ir86','IR86.COM','IRKEEP.COM'),('bootasm','CHECK.BAT','CHECK.BAT')]:copy(ROOT/'workbench'/folder/name,target)
copy(W/'RILL.IR');copy(dos('RILL.IN','RILL\n'));copy(dos('CONFIG.SYS','FILES=30\n'),image=boot)
copy(dos('KEY.TXT','RILL echo.\n'))
names=['HELLO','COUNT','CHOICE','RLECHO']
commands=['ECHO OFF','B:',r'A:\COMMAND /C CHECK IRKEEP <RILL.IN >RILL.TRN',r'A:\COMMAND /C CHECK ASMKEEP <RILL.IN >RILL.BLD']
for n in names:
 copy(W/(n+'.RIL'));copy(dos(n+'.IN',n+'\n'))
 commands += [f'COPY {n}.RIL SOURCE.RIL >NUL',fr'A:\COMMAND /C CHECK RILL >{n}.CMP',f'COPY RESULT.IR {n}.IR >NUL',fr'A:\COMMAND /C CHECK IRKEEP <{n}.IN >{n}.TRN',fr'A:\COMMAND /C CHECK ASMKEEP <{n}.IN >{n}.BLD',fr'A:\COMMAND /C CHECK {n}'+(' <KEY.TXT' if n=='RLECHO' else '')+f' >{n}.OUT']
copy(dos('BAD.RIL','fn main(){putc(65536);}\n'));copy(dos('OLD.IR','OLD RESULT\n'))
binary=scratch/'ALL.BIN';binary.write_bytes(bytes(range(256)));copy(binary)
commands += ['COPY BAD.RIL SOURCE.RIL >NUL','COPY OLD.IR RESULT.IR >NUL',r'A:\COMMAND /C CHECK RILL >BAD.LOG','COPY RESULT.IR KEPT.IR >NUL','DEL SOURCE.RIL',r'A:\COMMAND /C CHECK RILL >MISSING.LOG',r'A:\COMMAND /C CHECK RLECHO <ALL.BIN >ECHO.BIN','ECHO DONE >DONE.TXT']
copy(dos('AUTOEXEC.BAT','\n'.join(commands)+'\n'),image=boot)
monitor='/tmp/bootexp-rill-monitor.sock';Path(monitor).unlink(missing_ok=True)
p=subprocess.Popen(['qemu-system-i386','-machine','pc','-m','16M','-drive',f'file={boot},format=raw,if=floppy,index=0','-drive',f'file={disk},format=raw,if=floppy,index=1','-boot','a','-display','none','-monitor','unix:'+monitor+',server=on,wait=off','-serial','none','-no-reboot'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
try:
 for attempt in range(240):
  done=subprocess.run(['mtype','-i',str(disk),'::DONE.TXT'],capture_output=True)
  if done.returncode==0:break
  if p.poll() is not None:raise RuntimeError(p.stderr.read().decode())
  time.sleep(.5)
 else:raise RuntimeError('DOS RILL pipeline did not finish within 120 seconds')
 s=socket.socket(socket.AF_UNIX);s.connect(monitor);s.sendall(b'quit\n');s.close();p.wait(timeout=10)
 outputs=['RILL.ASM','RILL.COM','RILL.TRN','RILL.BLD','BAD.LOG','MISSING.LOG','KEPT.IR','ECHO.BIN']+[n+ext for n in names for ext in ['.IR','.ASM','.COM','.CMP','.TRN','.BLD','.OUT']]
 for name in outputs:subprocess.run(['mcopy','-o','-i',str(disk),'::'+name,str(scratch/name)],check=True)
 for ext in ['.ASM','.COM']:assert (scratch/('RILL'+ext)).read_bytes()==(W/('RILL'+ext)).read_bytes(),'DOS-built compiler differs '+ext
 for ext in ['.TRN','.BLD']:assert b'PASS' in (scratch/('RILL'+ext)).read_bytes()
 records=['PASS DOS 3.10 IR86 and ASM86 build RILL directly; assembly and executable match the bootstrap-built compiler']
 expected={'HELLO':b'HI','COUNT':b'012','CHOICE':b'U!','RLECHO':b'RILL echo.\r\n'}
 for n in names:
  for ext in ['.IR','.ASM','.COM']:assert (scratch/(n+ext)).read_bytes()==(W/(n+ext)).read_bytes(),(n,ext,'DOS differs')
  for ext in ['.CMP','.TRN','.BLD','.OUT']:assert b'PASS' in (scratch/(n+ext)).read_bytes(),(n,ext,'missing PASS')
  assert expected[n] in (scratch/(n+'.OUT')).read_bytes(),n+' output differs'
  records.append('PASS DOS 3.10 '+n+': RILL -> IR -> assembly -> COM, expected output and PASS')
 assert b'ERROR 00001 CODE 00003' in (scratch/'BAD.LOG').read_bytes() and b'FAIL' in (scratch/'BAD.LOG').read_bytes()
 assert (scratch/'KEPT.IR').read_bytes()==b'OLD RESULT\r\n'
 assert b'ERROR 00001 CODE 00001' in (scratch/'MISSING.LOG').read_bytes() and b'FAIL' in (scratch/'MISSING.LOG').read_bytes()
 assert (scratch/'ECHO.BIN').read_bytes()==b'\r\nB>ECHO OFF\r\n'+bytes(range(256))+b'\r\nPASS\r\n\r\n'
 records+=['PASS DOS rejection and missing input report exact diagnostics and FAIL; rejected source preserves the older IR file','PASS DOS compiled RILL byte-stream program preserves all 256 byte values and reports PASS']
 text='\n'.join(records)+'\n';(Q/'dos-results.txt').write_text(text);print(text)
finally:
 if p.poll() is None:p.terminate();p.wait(timeout=10)
