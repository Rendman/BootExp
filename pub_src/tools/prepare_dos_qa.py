"""Decode a public historical reference disk; work only on our QA copy."""
from pathlib import Path
import json,struct,subprocess
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa'
j=json.loads((Q/'dos310.json').read_text())
raw=bytearray()
for cylinder in j['diskData']:
 for head in cylinder:
  for sector in sorted(head,key=lambda s:s['s']):
   words=sector.get('d',[0]);count=sector['l']//4
   words=words+[words[-1]]*(count-len(words))
   raw.extend(b''.join(struct.pack('<I',n&0xffffffff) for n in words))
image=Q/'dos-test.img';image.write_bytes(raw)
listing=subprocess.check_output(['mdir','-b','-i',str(image),'::']).decode()
keep={'IBMBIO.COM','IBMDOS.COM','COMMAND.COM','BASICA.EXE'}
for name in listing.splitlines():
 base=name.rsplit('/',1)[-1]
 if base.upper() not in keep:
  subprocess.run(['mattrib','-i',str(image),'-r','-s','-h','::'+base],capture_output=True)
  subprocess.run(['mdel','-i',str(image),'::'+base],check=True,capture_output=True)
# All project input/output on a separate 360 KB data disk, preserving boot disk space.
data=Q/'work-test.img'
subprocess.run(['mformat','-C','-f','360','-i',str(data),'::'],check=True)
W=ROOT/'workbench/bootasm'
for file in W.iterdir():
 if (file.name in {'BYTE.BAS','VIEW.BAS','BOOTASM.BAS'} or (file.stem.startswith('T') and file.stem[1:].isdigit() and file.suffix=='.ASM') or (file.stem.startswith('BA') and file.stem[2:].isdigit())):
  subprocess.run(['mcopy','-i',str(data),str(file),'::'+file.name],check=True,capture_output=True)
commands=['ECHO OFF','VER > DOSVER.TXT']
# First run the original interpreter with every published checkpoint fixture.
for stage in json.loads((Q/'checkpoints.json').read_text()):
 i=stage['number'];name=f'T{i:02}'
 (Q/'INPUT.TXT').write_bytes((name+'\r\nSYSTEM\r\n').encode())
 subprocess.run(['mcopy','-i',str(data),str(Q/'INPUT.TXT'),f'::{name}.IN'],check=True)
 commands.append(f'A:\\BASICA {stage["source"]} <{name}.IN >{name}.LOG')
commands.extend(['ECHO DONE > DONE.TXT','GOTO STOP',':STOP','GOTO STOP'])
(Q/'AUTOEXEC.BAT').write_bytes(('B:\r\n'+'\r\n'.join(commands)+'\r\n').encode())
subprocess.run(['mcopy','-o','-i',str(image),str(Q/'AUTOEXEC.BAT'),'::AUTOEXEC.BAT'],check=True)
print(image,data)
