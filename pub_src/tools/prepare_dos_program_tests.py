"""Run only complete BASIC-produced programs under the DOS reference system."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa';W=ROOT/'workbench/bootasm'
image=Q/'work-test.img';boot=Q/'dos-test.img'
names=['T09','T10','T17','T18','HELLO','COPYBYTE','FAIL']
for name in names:
 subprocess.run(['mcopy','-o','-i',str(image),str(W/(name+'.COM')),'::'+name+'.COM'],check=True)
subprocess.run(['mcopy','-o','-i',str(image),str(W/'CHECK.BAT'),'::CHECK.BAT'],check=True)
cmds=['ECHO OFF','B:']+[f'A:\\COMMAND /C CHECK {name} >{name}.OUT' for name in names]+['ECHO DONE >RUNDONE.TXT']
p=Q/'RUNEXEC.BAT';p.write_bytes(('\r\n'.join(cmds)+'\r\n').encode())
subprocess.run(['mcopy','-o','-i',str(boot),str(p),'::AUTOEXEC.BAT'],check=True)
