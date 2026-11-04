"""Build published IR translators with ASM86, then run their generated programs."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/ir86';Q=ROOT/'qa/ir86'
sys.path.insert(0,str(ROOT/'qa/asm86'))
from dos_machine import DosMachine,assemble
ASM=(ROOT/'workbench/asm86/ASM86.COM').read_bytes()
cases=json.loads((Q/'checkpoints.json').read_text());results=[]
def check(test,message):
 if not test:raise AssertionError(message)
def symbols(machine):
 raw=bytes(machine.cpu.mem_read(machine.base+0x3000,5120));result={}
 for i in range(256):
  row=raw[i*20:i*20+20];name=row[:17].split(b'\0')[0]
  if not name:break
  result[name.decode('ascii')]=int.from_bytes(row[18:20],'little')
 return result
for case in cases:
 n=case['number'];level=case['level'];name=f'IR{n:02}';test=f'T{n:02}';bad=f'X{n:02}'
 source=(W/case['source']).read_bytes()
 check(all(len(s)<=120 for s in source.splitlines()),name+' physical line too long')
 built=assemble(ASM,source,name)
 if built.exitcode:
  (Q/'build-symbols.json').write_text(json.dumps(symbols(built),indent=2))
  raise AssertionError(f'{name} build: {built.output!r}')
 image=built.files[name+'.COM'];(W/(name+'.COM')).write_bytes(image)
 mapping=symbols(built)
 files={test+'.IR':(W/(test+'.IR')).read_bytes(),test+'.ASM':b'OLD TEXT'}
 run=DosMachine(files,[test]).run(image)
 check(run.exitcode==0,f'{name} acceptance: {run.output!r}')
 console=run.output.decode('ascii').replace('\r\r\n','\r\n')
 prefix='IR source name: '+test+'\r\n'
 case['binary_bytes']=len(image)
 if 'console' in case:
  check(console==prefix+case['console'],f'{name} diagnostic {console!r}')
  check(run.files[test+'.ASM']==b'OLD TEXT',name+' diagnostic wrote an output')
 else:
  target=run.files[test+'.ASM'];target.decode('ascii')
  check(b'\n' not in target.replace(b'\r\n',b''),name+' output is not CRLF')
  check(console==prefix+f'OK {test}.ASM {len(target):05} text bytes\r\n',f'{name} success text {console!r}')
  if 'assembly' in case:check(target.decode()==case['assembly'],f'{name} exact copied text')
  (W/(test+'.ASM')).write_bytes(target)
  program=assemble(ASM,target,test)
  check(program.exitcode==0,f'{name} generated assembly: {program.output!r}\n{target.decode()}')
  code=program.files[test+'.COM'];(W/(test+'.COM')).write_bytes(code)
  case.update(text_bytes=len(target),target_bytes=len(code),target_hex=code.hex(' ').upper())
  if level>=16:
   demand=int.from_bytes(run.cpu.mem_read(run.base+mapping['TARGETSIZE'],2),'little')
   check(demand==len(code),f'{name} target accounting {demand} != {len(code)}')
  if case.get('executable',True):
   child=DosMachine().run(code)
   check(child.exitcode==case['exit'] and child.output.decode('ascii')==case['output'],f'{name} generated runtime: {child.output!r}, status {child.exitcode}')
  else:check(code==b'A',name+' data fixture differs')
 rejected=DosMachine({bad+'.IR':(W/(bad+'.IR')).read_bytes(),bad+'.ASM':b'OLD TEXT'},[bad]).run(image)
 b=case['bad'];diagnostic=f'IR ERROR {b["line"]:05} CODE {b["code"]}'.encode()
 check(rejected.exitcode==1 and diagnostic in rejected.output,f'{name} rejection: {rejected.output!r}; expected {diagnostic!r}')
 check(rejected.files[bad+'.ASM']==b'OLD TEXT',name+' rejection changed old output')
 results.append(f'PASS {name}: ASM86 build; accepted input; exact visible result; rejection preserves output'+('; generated target assembles and runs' if case.get('executable',True) and 'console' not in case else ''))
 print(results[-1],flush=True)
(W/'IR86.COM').write_bytes((W/f'IR{len(cases):02}.COM').read_bytes())
check((W/'IR86.ASM').read_bytes()==(W/f'IR{len(cases):02}.ASM').read_bytes(),'Final source differs')
(Q/'checkpoints.json').write_text(json.dumps(cases,indent=2)+'\n')
(Q/'checkpoint-results.txt').write_text('\n'.join(results)+'\n')
print('PASS: every IR86 construction checkpoint')
