"""Build and self-rebuild the RILL toolchain under an actual DOS 3.10 kernel."""
from pathlib import Path
import subprocess,shutil,time,socket,struct
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa/toolchain';W=ROOT/'workbench/toolchain';scratch=Q/'dos';scratch.mkdir(exist_ok=True)
boot=Q/'boot.img';disk=Q/'work.img';shutil.copyfile(ROOT/'qa/dos-original.img',boot)
# A private hard disk matches the course workbench; source files exceed one floppy.
with disk.open('wb') as f:f.truncate(16*1024*1024)
subprocess.run(['sfdisk',str(disk)],input=b'label: dos\nunit: sectors\n\nstart=63, size=32697, type=04\n',stdout=subprocess.DEVNULL,check=True)
volume=str(disk)+'@@32256'
subprocess.run(['mformat','-i',volume,'-h','16','-s','63','-T','32697','-H','63','-c','4','::'],check=True)
def copy(p,name=None,image=volume):subprocess.run(['mcopy','-o','-i',image,str(p),'::'+(name or p.name)],check=True)
def dos(name,s):p=scratch/name;p.write_bytes(s.replace('\n','\r\n').encode('ascii'));return p
copy(ROOT/'workbench/bootasm/CHECK.BAT')
copy(W/'TMAKE.BAT')
for p,name in [(ROOT/'workbench/asm86a/ASM86A.COM','ASMAKEEP.COM'),(ROOT/'workbench/ir86/IRWIDE.ASM','IRWIDE.ASM'),(ROOT/'workbench/rill/RILLBOOT.IR','RILLBOOT.IR'),(ROOT/'workbench/rill/RILL.IR','RILL.IR'),(W/'TSMALL.RIL','TSMALL.RIL')]+[(W/(n+'.RIL'),n+'.RIL') for n in ['RILL','IR86','ASM86A']]:copy(p,name)
copy(W/'RC43.RIL')
commands=['C:',r'A:\COMMAND /C TMAKE >TMAKE.LOG']
copy(dos('HI.RIL','fn main(){putc(72);putc(73);return 0;}\n'))
commands += ['COPY HI.RIL SOURCE.RIL >NUL',r'A:\COMMAND /C CHECK R2 >HI.CMP','COPY RESULT.IR SOURCE.IR >NUL',r'A:\COMMAND /C CHECK I2 >HI.TRN','COPY RESULT.ASM SOURCE.ASM >NUL',r'A:\COMMAND /C CHECK A2 >HI.BLD','COPY RESULT.COM HI.COM >NUL',r'A:\COMMAND /C CHECK HI >HI.OUT','ECHO DONE >DONE.TXT']
copy(dos('CONFIG.SYS','FILES=30\n'),image=str(boot));copy(dos('AUTOEXEC.BAT','ECHO OFF\n'+'\n'.join(commands)+'\n'),image=str(boot))
monitor='/tmp/bootexp-rill-tools.sock';Path(monitor).unlink(missing_ok=True)
p=subprocess.Popen(['qemu-system-i386','-machine','pc','-m','16M','-drive',f'file={boot},format=raw,if=floppy,index=0','-drive',f'file={disk},format=raw,if=ide,index=0','-boot','a','-display','none','-monitor','unix:'+monitor+',server=on,wait=off','-serial','none','-no-reboot'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
try:
 for n in range(1200):
  if subprocess.run(['mtype','-i',volume,'::DONE.TXT'],capture_output=True).returncode==0:break
  if p.poll() is not None:raise RuntimeError(p.stderr.read().decode())
  time.sleep(.5)
 else:raise RuntimeError('DOS toolchain did not finish within ten minutes')
 s=socket.socket(socket.AF_UNIX);s.connect(monitor);s.sendall(b'quit\n');s.close();p.wait(timeout=10)
 logs=[]
 buildlog=subprocess.check_output(['mtype','-i',volume,'::TMAKE.LOG']);(scratch/'TMAKE.LOG').write_bytes(buildlog)
 assert buildlog.count(b'PASS ')==10 and b'FAIL' not in buildlog,buildlog
 initial=subprocess.check_output(['mtype','-i',volume,'::RC43.COM'])
 assert initial==subprocess.check_output(['mtype','-i',volume,'::RSELF.COM'])==(W/'RC43.COM').read_bytes()
 logs.append('PASS DOS 3.10 RC43 self-build before the 64-local extension')
 for stem,name in [('R','RILL'),('I','IR86'),('A','ASM86A')]:
  for gen in [0,1,2]:
   data=subprocess.check_output(['mtype','-i',volume,'::'+stem+str(gen)+'.COM']);assert data==(W/(name+'.COM')).read_bytes(),(stem,gen,'different executable')
   logs.append(f'PASS DOS 3.10 {name} generation {gen}: compiler, translator, assembler, and exact executable')
 text=subprocess.check_output(['mtype','-i',volume,'::HI.OUT']);assert b'HI' in text and b'PASS' in text,text
 logs.append('PASS DOS 3.10 generation-two RILL -> generation-two IR86 -> generation-two ASM86A -> HI')
 (Q/'dos-results.txt').write_text('\n'.join(logs)+'\n');print('\n'.join(logs))
finally:
 if p.poll() is None:p.terminate();p.wait(timeout=10)
