"""Check the adventure on DOS 3.10, including real CON keyboard input."""
from pathlib import Path
import shutil,subprocess,time

ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa/vampire';W=ROOT/'workbench/vampire'
scratch=Q/'dos';scratch.mkdir(exist_ok=True)
boot=Q/'boot.img';disk=Q/'work.img'
shutil.copyfile(ROOT/'qa/dos-original.img',boot)
subprocess.run(['mformat','-C','-f','360','-i',str(disk),'::'],check=True)
def copy(path,image=disk):subprocess.run(['mcopy','-o','-i',str(image),str(path),'::'+path.name],check=True)
def get(name):return subprocess.check_output(['mtype','-i',str(disk),'::'+name])
def exists(name):return subprocess.run(['mtype','-i',str(disk),'::'+name],capture_output=True).returncode==0
for name in ['VAMPIRE.COM','WIN.TXT']:copy(W/name)
batch=scratch/'AUTOEXEC.BAT'
batch.write_bytes(('ECHO OFF\r\nB:\r\nVAMPIRE WIN.TXT >WIN.LOG\r\n'
                  'IF ERRORLEVEL 1 ECHO FAIL >FAIL.TXT\r\n'
                  'ECHO READY >READY.TXT\r\nVAMPIRE >KEY.LOG\r\n'
                  'IF ERRORLEVEL 1 ECHO FAIL >>FAIL.TXT\r\nECHO READY >EOFREADY.TXT\r\n'
                  'VAMPIRE >EOF.LOG\r\nIF ERRORLEVEL 1 ECHO FAIL >>FAIL.TXT\r\n'
                  'ECHO DONE >DONE.TXT\r\n').encode('ascii'))
copy(batch,boot)
p=subprocess.Popen(['qemu-system-i386','-machine','pc','-m','16M',
    '-drive',f'file={boot},format=raw,if=floppy,index=0',
    '-drive',f'file={disk},format=raw,if=floppy,index=1',
    '-boot','a','-display','none','-monitor','stdio','-serial','none','-no-reboot'],
    stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
try:
    def waitfor(name):
        for _ in range(100):
            if exists(name):return
            if p.poll() is not None:raise RuntimeError(p.stderr.read().decode())
            time.sleep(.25)
        raise RuntimeError('DOS did not reach '+name)
    waitfor('READY.TXT');time.sleep(.5)
    for ch in 'read the sign\nquit\n':
        key={' ':'spc','\n':'ret'}.get(ch,ch)
        p.stdin.write(('sendkey '+key+' 20\n').encode());p.stdin.flush();time.sleep(.08)
    waitfor('EOFREADY.TXT');time.sleep(.25)
    p.stdin.write(b'sendkey ctrl-z 20\n');p.stdin.flush();time.sleep(.15)
    p.stdin.write(b'sendkey ret 20\n');p.stdin.flush()
    waitfor('DONE.TXT')
    p.stdin.write(b'quit\n');p.stdin.flush();p.wait(timeout=10)
    # COMMAND opens redirection before IF, even when its condition is false.
    assert not get('FAIL.TXT').strip()
    win=get('WIN.LOG');key=get('KEY.LOG');eof=get('EOF.LOG')
    assert b'Congratulations! You have killed Dracula.' in win and b'Time:' in win
    assert b'The sign reads: Dracula wakes at midnight.' in key and b'Goodbye.' in key,key
    assert b'End of commands.' in eof,eof
    for name,raw in [('WIN.LOG',win),('KEY.LOG',key),('EOF.LOG',eof)]: (scratch/name).write_bytes(raw)
    result='PASS DOS 3.10: PSP-selected WIN.TXT completes the adventure; DOS CON reads keyboard READ THE SIGN and QUIT; Control-Z ends console input; all return zero'
    print(result);(Q/'dos-results.txt').write_text(result+'\n')
finally:
    if p.poll() is None:p.terminate();p.wait(timeout=10)
