"""Check the focused ASM1 construction and final handoff in a private DOS disk."""
from pathlib import Path
import json,subprocess,tempfile,shutil,time
ROOT=Path(__file__).resolve().parents[1]
W=ROOT/'workbench/asm1';Q=ROOT/'qa/asm1'
steps=json.loads((Q/'intro.json').read_text())
scratch=Path(tempfile.mkdtemp(prefix='bootexp-asm1-'))
boot=scratch/'boot.img';disk=scratch/'work.img'
shutil.copyfile(ROOT/'qa/dos-original.img',boot)
subprocess.run(['mformat','-C','-f','360','-i',str(disk),'::'],check=True)
def copy(path,name=None,image=disk):
 subprocess.run(['mcopy','-o','-i',str(image),str(path),'::'+(name or path.name)],check=True)
def dos(name,text):
 p=scratch/name;p.write_bytes(text.replace('\n','\r\n').encode('ascii'));return p
copy(ROOT/'workbench/asm0/ASM86.COM','ASMKEEP.COM');copy(W/'CHECK.BAT')
commands=['ECHO OFF','B:'];expected={}
for s in steps:
 name=s['id'];copy(W/(name+'.ASM'))
 commands += [f'COPY {name}.ASM SOURCE.ASM >NUL',f'A:\\COMMAND /C CHECK ASMKEEP >B{name[1:]}.LOG',f'COPY RESULT.COM {name}.COM >NUL']
 expected[name+'.COM']=(W/(name+'.COM')).read_bytes()
 if s['mode']=='probe':
  commands += ['A:\\COMMAND /C CHECK A01C in.asm out.com >T01C.LOG','A:\\COMMAND /C CHECK A01C ONLY.ASM >X01C.LOG']
 else:
  fixture='T'+name[1:]+'.ASM';copy(W/fixture)
  if s['mode']=='fixed':commands += [f'COPY {fixture} SOURCE.ASM >NUL',f'A:\\COMMAND /C CHECK {name} >T{name[1:]}.LOG']
  else:commands += [f'A:\\COMMAND /C CHECK {name} {fixture} {s["result"]} >T{name[1:]}.LOG']
  result=s.get('result','RESULT.COM');saved=name+'.BIN'
  commands.append(f'COPY {result} {saved} >NUL');expected[saved]=bytes.fromhex(s['expected'])
copy(W/'A01.ASM');copy(W/'T01.ASM')
commands += ['COPY A01.ASM SOURCE.ASM >NUL','A:\\COMMAND /C CHECK ASMKEEP >B01.LOG','COPY RESULT.COM A01.COM >NUL','A:\\COMMAND /C CHECK A01 T01.ASM XOR.COM >T01.LOG']
expected['A01.COM']=(ROOT/'workbench/asm86/A01.COM').read_bytes()
expected['XOR.COM']=bytes.fromhex('32C033C380F08081F03412')
segment_cases=[c for c in json.loads((ROOT/'qa/asm86/checkpoints.json').read_text()) if c['number'] in (10,11)]
segment_success=[];segment_failure=[]
for c in segment_cases:
 n=c['number'];name=f'A{n:02}'
 for source in [name+'.ASM',f'T{n:02}.ASM',f'X{n:02}.ASM']:copy(W/source)
 commands += [f'COPY {name}.ASM SOURCE.ASM >NUL',f'A:\\COMMAND /C CHECK ASMKEEP >B{n:02}.LOG',f'COPY RESULT.COM {name}.COM >NUL',f'A:\\COMMAND /C CHECK {name} T{n:02}.ASM RESULT.COM >T{n:02}.LOG',f'COPY RESULT.COM R{n:02}.BIN >NUL']
 expected[name+'.COM']=(ROOT/'workbench/asm86'/(name+'.COM')).read_bytes()
 expected[f'R{n:02}.BIN']=bytes.fromhex(c['expected']);segment_success += [f'B{n:02}',f'T{n:02}']
 for i,bad in enumerate([c['bad'],*c.get('extra_rejections',[])]):
  stem=f'X{n:02}'+('' if i==0 else chr(64+i))
  if i:copy(dos(stem+'.ASM',bad['text']))
  commands += [f'A:\\COMMAND /C CHECK {name} {stem}.ASM RESULT.COM >{stem}.LOG',f'COPY RESULT.COM K{stem[1:]}.BIN >NUL']
  expected[f'K{stem[1:]}.BIN']=bytes.fromhex(c['expected'])
  segment_failure.append((stem,bad['line'],bad['code']))
copy(W/'ASMA0.ASM','ASM1.ASM')
commands += ['COPY ASM1.ASM SOURCE.ASM >NUL','A:\\COMMAND /C CHECK ASMKEEP >SEED.LOG','COPY RESULT.COM ASM1.COM >NUL','A:\\COMMAND /C CHECK ASM1 ASM1.ASM SELF.COM >SELF.LOG','A:\\COMMAND /C CHECK SELF ASM1.ASM AGAIN.COM >AGAIN.LOG','ECHO DONE >DONE.TXT']
for name in ['ASM1.COM','SELF.COM','AGAIN.COM']:expected[name]=(ROOT/'workbench/asm86/ASMA0.COM').read_bytes()
copy(dos('AUTOEXEC.BAT','\n'.join(commands)+'\n'),image=boot)
p=subprocess.Popen(['qemu-system-i386','-machine','pc','-m','16M','-drive',f'file={boot},format=raw,if=floppy,index=0','-drive',f'file={disk},format=raw,if=floppy,index=1','-boot','a','-display','none','-monitor','stdio','-serial','none','-no-reboot'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
try:
 for _ in range(360):
  if subprocess.run(['mtype','-i',str(disk),'::DONE.TXT'],capture_output=True).returncode==0:break
  if p.poll() is not None:raise RuntimeError(p.stderr.read().decode())
  time.sleep(.5)
 else:raise RuntimeError('DOS stopping-point checks did not finish')
 p.stdin.write(b'quit\n');p.stdin.flush();p.wait(timeout=10)
 def read(name):return subprocess.run(['mtype','-i',str(disk),'::'+name],capture_output=True,check=True).stdout
 for name,data in expected.items():assert read(name)==data,name
 for name in ['B01A','B01B','B01C','B01D','B01E','B01F','T01A','T01B','T01C','T01D','T01E','T01F','B01','T01','SEED','SELF','AGAIN',*segment_success]:
  log=read(name+'.LOG');assert b'PASS' in log and b'FAIL' not in log,(name,log)
 rejected=read('X01C.LOG');assert b'ERROR 00000 CODE 9' in rejected and b'FAIL' in rejected,rejected
 for name,line,code in segment_failure:
  log=read(name+'.LOG');assert f'ERROR {line:05} CODE {code}'.encode() in log and b'FAIL' in log and b'PASS' not in log,(name,log)
 report='PASS DOS 3.10: ASM0 builds all six focused ASM1 checkpoints and the separate XOR step; all byte/status fixtures agree.\nPASS DOS 3.10: ASM0 builds the final ASM1; two self-built generations reproduce every byte of its established executable.\n'
 report+='PASS DOS 3.10 A10: four segment sources, three legal destinations, forbidden CS destination and both byte-register rejections.\nPASS DOS 3.10 A11: ES-prefixed byte/word loads/stores, cleared prefixes on ordinary accesses and rejected DS/CS/SS overrides; every rejection preserves the accepted bytes.\n'
 (Q/'intro-dos-results.txt').write_text(report);print(report,end='')
finally:
 if p.poll() is None:p.terminate();p.wait(timeout=10)
