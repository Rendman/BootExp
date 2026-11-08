"""Run every native checkpoint and prove two self-assembly generations."""
from pathlib import Path
import json,sys
from dos_machine import DosMachine,assemble
ROOT=Path(__file__).resolve().parents[2];WORK=ROOT/'workbench/asm86';QA=ROOT/'qa/asm86'
CASES=json.loads((QA/'checkpoints.json').read_text())
RESULT=[]
seed=(WORK/'ASM86.COM').read_bytes()
def check(condition,message):
 if not condition:raise AssertionError(message)
def run_case(case,image):
 number=case['number'];stem=f'T{number:02}'
 files={};inputs=[]
 if case['fixture'] is not None:
  files['SOURCE.ASM']=(WORK/(stem+'.ASM')).read_bytes()
 result=DosMachine(files,inputs).run(image)
 check(result.exitcode==0,f'{case["source"]} accepted test failed: {result.output!r}')
 prefix=''
 if case['image'] is not None:
  expected=bytes.fromhex(case['image'])
  check(result.files.get('RESULT.COM')==expected,f'{case["source"]}: encoded bytes {result.files.get("RESULT.COM")} != {expected}')
  payload=f'OK {len(expected):05} bytes\r\n'
  if case['executable'] is not None:
   child=DosMachine().run(expected)
   check(child.exitcode==0 and child.output.decode('ascii')==case['executable'],f'{case["source"]}: child program output')
 else:payload=case['payload'].replace('{stem}',stem)
 check(result.output.decode('ascii').replace('\r\r\n','\r\n')==prefix+payload,f'{case["source"]}: console {result.output!r} != {(prefix+payload)!r}')
 bad=case['bad']
 if bad:
  name=f'X{number:02}'
  kwargs={};inputs=[];files={'RESULT.COM':b'OLD OUTPUT'}
  if bad['kind']=='source':files['SOURCE.ASM']=bad['text'].encode('ascii')
  elif bad['kind']=='console':inputs=[bad['input']]
  elif bad['kind']=='stack':inputs=[];kwargs['sp']=0x8000
  elif bad['kind']=='missing':pass
  else:raise AssertionError(bad)
  rejected=DosMachine(files,inputs,**kwargs).run(image)
  check(rejected.exitcode==1,f'{case["source"]}: expected rejection, got {rejected.output!r}')
  diagnostic=f'ERROR {bad["line"]:05} CODE {bad["code"]}'
  check(diagnostic in rejected.output.decode('ascii'),f'{case["source"]}: expected {diagnostic}, got {rejected.output!r}')
  check(rejected.files['RESULT.COM']==b'OLD OUTPUT',f'{case["source"]}: failed input changed old output')
 return result
for case in CASES:
 name=Path(case['source']).stem
 source=(WORK/case['source']).read_bytes()
 check(all(len(line)<=120 for line in source.splitlines()),f'{name}: overlong source line')
 built=assemble(seed,source,name)
 check(built.exitcode==0,f'{name} build: {built.output!r}')
 image=built.files['RESULT.COM'];(WORK/(name+'.COM')).write_bytes(image)
 run_case(case,image)
 case['binary_bytes']=len(image)
 RESULT.append(f'PASS {name}: {len(image)} bytes; visible checkpoint result'+('; rejection and old-output preservation' if case['bad'] else ''))
 print(RESULT[-1],flush=True)
final=(WORK/'AS28.COM').read_bytes();source=(WORK/'ASM86.ASM').read_bytes()
first=assemble(final,source,'SELF')
check(first.exitcode==0 and first.files['RESULT.COM']==final,f'First self-assembly differs: {first.output!r}')
second=assemble(first.files['RESULT.COM'],source,'AGAIN')
check(second.exitcode==0 and second.files['RESULT.COM']==final,f'Second self-assembly differs: {second.output!r}')
check(final==seed,'BASIC-produced first ASM86 differs from self-assembled image')
(WORK/'ASM86.COM').write_bytes(final)
(WORK/'SELF.COM').write_bytes(first.files['RESULT.COM'])
(WORK/'AGAIN.COM').write_bytes(second.files['RESULT.COM'])
RESULT.append('PASS: two self-assembly generations match every byte of the first native executable')
print(RESULT[-1],flush=True)
(QA/'checkpoints.json').write_text(json.dumps(CASES,indent=2))
(QA/'checkpoint-results.txt').write_text('\n'.join(RESULT)+'\n')
print('PASS: all checkpoint and self-assembly checks')
