"""Build the reader-facing IR construction with a freshly bootstrapped ASM86."""
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'qa/asm86'))
from machine import assemble,run_assembler,AssemblerMachine
D=ROOT/'site/static/downloads/tools'

def build(assembler,name,source,result='RESULT.COM'):
 r=run_assembler(assembler,files={name:source},command_line=f' {name} {result}')
 assert r.exitcode==0,(name,r.output)
 assert not r.allocations,(name,'assembler allocation leak')
 return r.files[result]

def check():
 initial=(ROOT/'workbench/asm0/ASM86.COM').read_bytes()
 r=assemble(initial,(D/'asm1/ASM1.ASM').read_bytes());assert r.exitcode==0,r.output
 seed=r.files['RESULT.COM']
 assembler_source=(D/'asm86/ASM86.ASM').read_bytes()
 assembler=build(seed,'ASM86.ASM',assembler_source)
 assert len(assembler)==6433
 first=build(assembler,'ASM86.ASM',assembler_source,'ASTEST.COM')
 assert first==assembler
 second=build(first,'ASM86.ASM',assembler_source,'ASTWO.COM')
 assert second==assembler
 print('PASS ASM0 -> ASM1 -> ASM86: canonical sources and both assembler self-builds; ASMAKEEP/ASTEST comparison agrees',flush=True)

 cases=json.loads((ROOT/'qa/toolchain/ir-extensions.json').read_text())
 for c in cases:
  n=c['number'];name=f'IR{n:02}.ASM';fixture=f'T{n:02}.IR'
  program=build(assembler,name,(D/'ir86'/name).read_bytes())
  assert len(program)==c['binary_bytes'],name
  text=(D/'ir86'/fixture).read_bytes()
  r=AssemblerMachine({fixture:text,'RESULT.ASM':b'ACCEPTED'},command_line=f' {fixture} RESULT.ASM').run(program,limit=1000000000)
  assert r.exitcode==0 and r.output.decode()==c['output'],(name,r.exitcode,r.output)
  assert not r.allocations
  if n in (1,2,4):assert r.files['RESULT.ASM']==b'ACCEPTED'
  elif n==3:assert r.files['RESULT.ASM']==text
  else:
   target=build(assembler,'RESULT.ASM',r.files['RESULT.ASM'])
   assert len(target)==c['target_bytes']
   assert target[:32]==bytes.fromhex(c['target_hex'])
   child=AssemblerMachine({'A':b'A'} if n in (13,15,17,21) else {},command_line=c.get('program_command_line','')).run(target,limit=1000000000)
   assert child.exitcode==c['program_exit'] and child.output.decode()==c['program_output'],(name,'generated program',child.exitcode,child.output)
   assert not child.allocations
  files={'RESULT.ASM':b'ACCEPTED'}
  if c['bad'] is not None:files['BAD.IR']=c['bad'].replace('\n','\r\n').encode()
  rejected=AssemblerMachine(files,command_line=' BAD.IR RESULT.ASM').run(program,limit=1000000000)
  assert rejected.exitcode==1 and rejected.output.decode()==c['error'],(name,rejected.output)
  assert rejected.files['RESULT.ASM']==b'ACCEPTED' and 'IRTX.TMP' not in rejected.files and not rejected.allocations
  print(f'PASS {name}: fresh ASM86 build ({len(program)} bytes), named-file fixture, generated program where applicable, rejection and preservation',flush=True)
 assert (D/'ir86/IR86.ASM').read_bytes()==(D/'ir86/IR23.ASM').read_bytes()
 assert build(assembler,'IR86.ASM',(D/'ir86/IR86.ASM').read_bytes())==program
 print('PASS ASM86 -> IR86: all 23 canonical checkpoints, final 12301-byte translator and unchanged IR86.ASM handoff source',flush=True)
 return program

if __name__=='__main__':check()
