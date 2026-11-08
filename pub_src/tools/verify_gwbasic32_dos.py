"""Run the actual GW-BASIC 3.20 binary against the published bootstrap source.

Only private QA copies of DOS/media are written. No historical executable or
emulator-generated disk belongs to a reader source collection.
"""
from pathlib import Path
import argparse,json,re,shutil,socket,subprocess,time,tempfile,hashlib
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa/bootasm';W=ROOT/'workbench/bootasm'
PRIVATE=Q/'gwbasic32';PRIVATE.mkdir(parents=True,exist_ok=True)
INTERPRETER=PRIVATE/'GWBASIC.EXE'

def command(args,**kwargs):return subprocess.run(args,check=True,capture_output=True,**kwargs)
def dos(text):return text.replace('\r\n','\n').replace('\n','\r\n').encode('ascii')
def get(image,name):return subprocess.check_output(['mtype','-i',str(image),'::TEST/'+name],stderr=subprocess.DEVNULL)

def session(label,files,commands,timeout=180,capture_banner=False):
 directory=PRIVATE/label;directory.mkdir(exist_ok=True)
 boot=directory/'boot.img';data=directory/'work.img'
 shutil.copyfile(ROOT/'qa/dos-original.img',boot)
 # Retain the boot records, system files and command interpreter on our copy.
 listing=subprocess.check_output(['mdir','-b','-i',str(boot),'::']).decode().splitlines()
 for name in listing:
  base=name.rsplit('/',1)[-1]
  if base.upper() not in {'IBMBIO.COM','IBMDOS.COM','COMMAND.COM'}:
   subprocess.run(['mattrib','-i',str(boot),'-r','-s','-h','::'+base],capture_output=True)
   command(['mdel','-i',str(boot),'::'+base])
 command(['mcopy','-o','-i',str(boot),str(INTERPRETER),'::GWBASIC.EXE'])
 command(['mformat','-C','-f','360','-i',str(data),'::'])
 command(['mmd','-i',str(data),'::TEST'])
 files=dict(files);files['QUIT.IN']=b'SYSTEM\r\n'
 for name,raw in files.items():
  p=directory/name;p.write_bytes(raw)
  command(['mcopy','-o','-i',str(data),str(p),'::TEST/'+name])
 auto=directory/'AUTOEXEC.BAT';auto.write_bytes(dos('ECHO OFF\nB:\nCD \\TEST\nVER >DOSVER.TXT\n'+'\n'.join(commands)+'\nECHO DONE >B:\\DONE.TXT\n'))
 command(['mcopy','-o','-i',str(boot),str(auto),'::AUTOEXEC.BAT'])
 monitor_directory=tempfile.TemporaryDirectory(prefix='bootexp-gw32-')
 monitor=Path(monitor_directory.name)/'monitor.sock'
 process=subprocess.Popen(['qemu-system-i386','-machine','pc','-m','16M','-drive',f'file={boot},format=raw,if=floppy,index=0','-drive',f'file={data},format=raw,if=floppy,index=1','-boot','a','-display','none','-monitor','unix:'+str(monitor)+',server=on,wait=off','-serial','none','-no-reboot'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 try:
  if capture_banner:
   deadline=time.monotonic()+30
   while not monitor.exists():
    if process.poll() is not None:raise RuntimeError(process.stderr.read().decode())
    if time.monotonic()>deadline:raise RuntimeError('QEMU monitor did not open')
    time.sleep(.05)
   observer=socket.socket(socket.AF_UNIX);observer.settimeout(2);observer.connect(str(monitor))
   def receive():
    raw=b''
    while b'(qemu)' not in raw:raw+=observer.recv(4096)
    return raw
   receive()
   def observe(cmd):observer.sendall(cmd.encode()+b'\n');return receive()
   screen=directory/'screen.bin'
   while time.monotonic()<deadline:
    observe(f'pmemsave 0xb8000 4000 "{screen}"')
    raw=screen.read_bytes()[::2]
    text='\n'.join(raw[i:i+80].decode('cp437').rstrip() for i in range(0,2000,80))
    if re.search(r'GW-BASIC\s+3\.20\b',text) and 'Ok' in text:break
    time.sleep(.1)
   else:raise RuntimeError('Expected original GW-BASIC 3.20 startup banner; screen:\n'+text)
   (Q/'gwbasic32-version.txt').write_text(text+'\n')
   time.sleep(.5)
   for k in ['s','y','s','t','e','m','ret']:
    observe('sendkey '+k+' 30');time.sleep(.12)
   observer.close()
  end=time.monotonic()+timeout
  while time.monotonic()<end:
   if process.poll() is not None:raise RuntimeError(process.stderr.read().decode())
   if subprocess.run(['mtype','-i',str(data),'::DONE.TXT'],capture_output=True).returncode==0:break
   time.sleep(.25)
  else:
   observer=socket.socket(socket.AF_UNIX);observer.settimeout(2);observer.connect(str(monitor))
   reply=b''
   while b'(qemu)' not in reply:reply+=observer.recv(4096)
   screen=directory/'timeout.bin';observer.sendall(f'pmemsave 0xb8000 4000 "{screen}"\n'.encode())
   reply=b''
   while b'(qemu)' not in reply:reply+=observer.recv(4096)
   observer.close();raw=screen.read_bytes()[::2]
   print('\n'.join(raw[i:i+80].decode('cp437').rstrip() for i in range(0,2000,80)),flush=True)
   raise RuntimeError(f'{label}: DOS did not complete within {timeout} seconds; inspect {data}')
  connection=socket.socket(socket.AF_UNIX);connection.connect(str(monitor));connection.sendall(b'quit\n');connection.close();process.wait(timeout=10)
  return data
 finally:
  if process.poll() is None:process.terminate();process.wait(timeout=10)
  monitor_directory.cleanup()

def invoke(source,log,input='QUIT.IN'):
 return f'A:\\GWBASIC {source} <{input} >{log}'

SMOKE='''10 ON ERROR GOTO 900
20 PRINT "GW32 FILE PROBE"
30 OPEN "O", #1, "PROBE.TXT"
40 PRINT #1, "OK"
50 CLOSE #1
60 OPEN "I", #1, "PROBE.TXT"
70 LINE INPUT #1, T$
80 CLOSE #1
90 IF T$<>"OK" THEN PRINT "PROBE FAIL": END
100 OPEN "R", #1, "PROBE.BIN", 1
110 FIELD #1, 1 AS B$
120 LSET B$=CHR$(65)
130 PUT #1, 1
140 CLOSE
150 PRINT "PROBE PASS"
160 END
900 PRINT "PROBE BASIC ERROR"; ERR; "AT"; ERL
910 CLOSE: END
'''

def smoke():
 image=session('smoke',{'SMOKE.BAS':dos(SMOKE)},['A:\\GWBASIC',invoke('SMOKE.BAS','SMOKE.LOG')],timeout=45,capture_banner=True)
 log=get(image,'SMOKE.LOG');(Q/'gwbasic32-smoke.txt').write_bytes(log)
 banner=(Q/'gwbasic32-version.txt').read_text()
 print(banner+log.decode('cp437'),flush=True)
 assert re.search(r'GW-BASIC\s+3\.20\b',banner), 'Interpreter banner is not GW-BASIC 3.20'
 assert b'PROBE PASS' in log and b'PROBE BASIC ERROR' not in log, 'Original interpreter file probe failed'
 assert get(image,'PROBE.BIN')==b'A'
 return banner,get(image,'DOSVER.TXT').decode('cp437')

def checkpoints():
 cases=json.loads((ROOT/'qa/checkpoints.json').read_text())
 files={'CHECK.BAT':(W/'CHECK.BAT').read_bytes()};commands=[]
 for c in cases:
  n=c['number'];good=c['fixture']+'.ASM';bad=f'X{n:02}.ASM'
  for name in [c['source'],good,bad]:files[name]=(W/name).read_bytes()
  commands += [f'COPY {good} SOURCE.ASM >NUL',invoke(c['source'],f'A{n:02}.LOG'),f'COPY RESULT.COM A{n:02}.COM >NUL',f'COPY {bad} SOURCE.ASM >NUL',invoke(c['source'],f'X{n:02}.LOG'),f'COPY RESULT.COM X{n:02}.COM >NUL']
  if c['run'] is not None:commands.append(f'A:\\COMMAND /C CHECK A{n:02} >R{n:02}.LOG')
 image=session('checkpoints',files,commands)
 results=[]
 for c in cases:
  n=c['number'];expected=bytes.fromhex(c['expected']);good=get(image,f'A{n:02}.LOG');bad=get(image,f'X{n:02}.LOG')
  assert b'OK RESULT.COM' in good and b'BASIC error' not in good,(c['source'],good)
  assert get(image,f'A{n:02}.COM')==expected,(n,'accepted bytes differ')
  assert c['diagnostic'].encode() in bad and b'OK ' not in bad,(n,bad)
  assert get(image,f'X{n:02}.COM')==expected,(n,'rejection changed accepted output')
  if c['run'] is not None:
   runtime=get(image,f'R{n:02}.LOG');assert b'PASS' in runtime and b'FAIL' not in runtime and c['run'].encode() in runtime,(n,runtime)
  results.append({'source':c['source'],'bytes':len(expected),'exact_bytes':True,'rejection':c['diagnostic'],'accepted_output_preserved':True,'executed':c['run'] is not None})
  print('PASS original GW-BASIC 3.20',c['source'],'bytes, rejection and preservation',flush=True)
 return results

def boundaries():
 # These are authored source fixtures and expected bytes, not a host encoder.
 valid=[
  ('EMPTY','',b''),('WORDS','DB 0,255\nDW 0,32768,65535',bytes.fromhex('00 FF 00 00 00 80 FF FF')),
  ('FIXED','RET\nCLD\nLODSB\nSTOSB',bytes.fromhex('C3 FC AC AA')),
  ('MEMORY','MOV BX,DATA\nMOV AL,[BX]\nMOV [DATA],AX\nDATA:\nDW 0',bytes.fromhex('BB 09 01 8A 07 89 06 09 01 00 00')),
  ('NEAR','HERE:\nCALL THERE\nJMP HERE\nTHERE:\nRET',bytes.fromhex('E8 03 00 E9 FA FF C3')),
  ('JPLUS','JE 181H',bytes.fromhex('74 7F')),
  ('JMINUS','\n'.join(['DB '+','.join(['0']*32)]*3+['DB '+','.join(['0']*30),'JE 100H']),bytes(126)+bytes.fromhex('74 80')),
  ('FULL','\n'.join(['DB '+','.join(['0']*32)]*128),bytes(4096)),
  ('SYMBOLS','\n'.join(f'L{i}:\nDB 0' for i in range(256)),bytes(256)),
  ('LINES','\n'.join([';']*2000),b''),
  ('LOWER',' ; note\n\tmov al,0ffh ; note',bytes.fromhex('B0 FF')),
 ]
 invalid=[
  ('BIGBYTE','DB 256','Byte out of range'),('BIGWORD','DW 65536','Number too large'),
  ('BADHEX','DB 12ZH','Bad number'),('DUP','A:\nA:','Duplicate label'),
  ('UNDEF','DW MISSING','Undefined label'),('REGNAME','AX:\nDB 0','Reserved label'),
  ('MISMATCH','MOV AX,AL','Register sizes differ'),('MEMIMM','MOV [BX],1','Register required'),
  ('NEWCPU','PUSHA','Unknown instruction'),('JTOOFAR','JE 182H','Branch out of range'),
  ('OVERFLOW','\n'.join(['DB '+','.join(['0']*32)]*128+['DB 0']),'Program too large'),
  ('MANYLAB','\n'.join(f'L{i}:' for i in range(257)),'Too many labels'),
  ('MANYLINE','\n'.join([';']*2001),'Too many source lines'),
  ('LONG',';'+'x'*120,'Source line too long'),('TRAIL','DB 1,','Missing value'),
 ]
 files={'BOOTASM.BAS':(W/'BOOTASM.BAS').read_bytes(),'HOLD.COM':b'UNCHANGED','VIEW.BAS':(W/'VIEW.BAS').read_bytes(),'BYTE.BAS':(W/'BYTE.BAS').read_bytes(),'CHECK.BAT':(W/'CHECK.BAT').read_bytes()};commands=[]
 for number,(name,text,expected) in enumerate(valid,1):
  fixture=f'V{number:02}.ASM';files[fixture]=dos(text+'\n')
  # DOS COPY does not retain an empty file; REN preserves a valid zero-byte
  # assembly result for the byte viewer and host-side inspection.
  commands += [f'COPY {fixture} SOURCE.ASM >NUL',invoke('BOOTASM.BAS',f'V{number:02}.LOG'),f'REN RESULT.COM V{number:02}.COM']
 for number,(name,text,diagnostic) in enumerate(invalid,1):
  fixture=f'X{number:02}.ASM';files[fixture]=dos(text+'\n')
  commands += [f'COPY HOLD.COM RESULT.COM >NUL',f'COPY {fixture} SOURCE.ASM >NUL',invoke('BOOTASM.BAS',f'X{number:02}.LOG'),f'COPY RESULT.COM X{number:02}.COM >NUL']
 # Truncation must remove a prior longer file, including the empty case.
 files['SHORT.ASM']=b'DB 9\r\n';commands += ['COPY HOLD.COM RESULT.COM >NUL','COPY SHORT.ASM SOURCE.ASM >NUL',invoke('BOOTASM.BAS','SHORT.LOG'),'COPY RESULT.COM SHORT.COM >NUL']
 for n,value in enumerate(['0','65','255','256','-1']):
  files[f'B{n}.IN']=dos(value+'\nSYSTEM\n');commands += [invoke('BYTE.BAS',f'B{n}.LOG',f'B{n}.IN'),f'COPY BYTE.COM B{n}.COM >NUL']
 for name,target in [('EMPTY','V01.COM'),('BYTES','V02.COM'),('MISSING','MISSING.COM')]:
  files[name+'.IN']=dos(target+'\nSYSTEM\n');commands.append(invoke('VIEW.BAS',name+'.LOG',name+'.IN'))
 for name in ['HELLO','COPYBYTE','FAIL']:
  files[name+'.ASM']=(W/(name+'.ASM')).read_bytes()
  commands += [f'COPY {name}.ASM SOURCE.ASM >NUL',invoke('BOOTASM.BAS',name+'.BLD'),f'COPY RESULT.COM {name}.COM >NUL',f'A:\\COMMAND /C CHECK {name} >{name}.LOG']
 image=session('boundaries',files,commands)
 results=[]
 for n,(name,text,expected) in enumerate(valid,1):
  log=get(image,f'V{n:02}.LOG');assert b'OK RESULT.COM' in log,(name,log)
  assert get(image,f'V{n:02}.COM')==expected,(name,'bytes differ')
  results.append({'case':name,'accepted':True,'bytes':len(expected)})
 for n,(name,text,diagnostic) in enumerate(invalid,1):
  log=get(image,f'X{n:02}.LOG');assert diagnostic.encode() in log and b'OK ' not in log,(name,log)
  assert get(image,f'X{n:02}.COM')==b'UNCHANGED',(name,'output changed')
  results.append({'case':name,'accepted':False,'diagnostic':diagnostic,'accepted_output_preserved':True})
 assert get(image,'SHORT.COM')==b'\x09'
 for n,value in enumerate([0,65,255,255,255]):assert get(image,f'B{n}.COM')==bytes([value]),n
 for n in [3,4]:assert b'Bad byte' in get(image,f'B{n}.LOG')
 assert b'Length: 0' in get(image,'EMPTY.LOG')
 assert b'00 FF 00 00 00 80 FF FF' in get(image,'BYTES.LOG')
 assert b'Cannot read file' in get(image,'MISSING.LOG')
 assert subprocess.run(['mtype','-i',str(image),'::TEST/MISSING.COM'],capture_output=True).returncode!=0
 for name,expected,output,success in [
  ('HELLO','BA 0C 01 B4 09 CD 21 B8 00 4C CD 21 48 45 4C 4C 4F 0D 0A 24',b'HELLO\r\n',True),
  ('COPYBYTE','BB 16 01 8A 07 88 06 17 01 8A 16 17 01 B4 02 CD 21 B8 00 4C CD 21 4D 00',b'M',True),
  ('FAIL','B8 01 4C CD 21',b'',False)]:
  assert get(image,name+'.COM')==bytes.fromhex(expected),name
  runtime=get(image,name+'.LOG');assert output in runtime and (b'PASS' if success else b'FAIL') in runtime,(name,runtime)
 print('PASS original GW-BASIC 3.20: limits, branches, truncation, BYTE/VIEW and complete examples',flush=True)
 return {'cases':results,'truncation':True,'byte_writer':True,'viewer':True,'complete_programs':['HELLO','COPYBYTE','FAIL']}

def asm0():
 work=ROOT/'workbench/asm0';cases=json.loads((ROOT/'qa/asm0/checkpoints.json').read_text())
 files={'BOOTASM.BAS':(W/'BOOTASM.BAS').read_bytes(),'CHECK.BAT':(W/'CHECK.BAT').read_bytes()};commands=[]
 for c in cases:
  name=c['source'];stem=Path(name).stem;files[name]=(work/name).read_bytes()
  commands += [f'COPY {name} SOURCE.ASM >NUL',invoke('BOOTASM.BAS',stem+'.LOG'),f'COPY RESULT.COM {stem}.COM >NUL']
 commands += ['COPY RESULT.COM ASM0.COM >NUL',r'A:\COMMAND /C CHECK ASM0 >SELF1.LOG','COPY RESULT.COM SELF1.COM >NUL',r'A:\COMMAND /C CHECK SELF1 >SELF2.LOG','COPY RESULT.COM SELF2.COM >NUL']
 image=session('asm0',files,commands)
 results=[]
 for c in cases:
  stem=Path(c['source']).stem;log=get(image,stem+'.LOG');actual=get(image,stem+'.COM');expected=(work/(stem+'.COM')).read_bytes()
  assert b'OK RESULT.COM' in log and b'BASIC error' not in log,(stem,log)
  assert actual==expected,(stem,'GW-BASIC and retained project output differ')
  results.append({'source':c['source'],'bytes':len(actual),'exact_bytes':True})
 baseline=get(image,'ASM0.COM')
 for n in [1,2]:
  assert get(image,f'SELF{n}.COM')==baseline,(n,'ASM0 self-build differs')
  log=get(image,f'SELF{n}.LOG');assert f'OK {len(baseline):05} bytes'.encode() in log and b'PASS' in log and b'FAIL' not in log,(n,log)
 print('PASS original GW-BASIC 3.20: all 28 ASM0 builds and two exact native self-builds',flush=True)
 return results,len(baseline)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--smoke-only',action='store_true');parser.add_argument('--interpreter',type=Path);args=parser.parse_args()
 source_disk=ROOT.parent/'vm/Software/Microsoft MS-DOS 3.20 (1986) (5.25-360k)/disk02.img'
 if args.interpreter:
  if args.interpreter.resolve()!=INTERPRETER.resolve():shutil.copyfile(args.interpreter,INTERPRETER)
 elif source_disk.is_file():command(['mcopy','-o','-i',str(source_disk),'::GWBASIC.EXE',str(INTERPRETER)])
 assert INTERPRETER.is_file(),'Supply the original GW-BASIC 3.20 executable with --interpreter'
 banner,version=smoke()
 if not args.smoke_only:
  records=checkpoints();limits=boundaries();construction,size=asm0()
  report={'interpreter':'Microsoft GW-BASIC 3.20','startup_banner':banner.splitlines()[:4],'interpreter_bytes':INTERPRETER.stat().st_size,'interpreter_sha256':hashlib.sha256(INTERPRETER.read_bytes()).hexdigest(),'dos':version.strip(),'machine':'QEMU PC/SeaBIOS, 640 KiB conventional memory','published_basic_sources_changed':False,'basic_checkpoints':records,'boundaries':limits,'asm0_construction':construction,'asm0_bytes':size,'asm0_matching_self_builds':2,'passed':True}
  (Q/'gwbasic32-results.json').write_text(json.dumps(report,indent=2)+'\n')
  print('PASS GW-BASIC 3.20 compatibility: unchanged BOOTASM, all construction stages and ASM0 handoff',flush=True)
