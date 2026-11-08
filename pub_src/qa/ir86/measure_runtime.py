"""Measure backend runtime code with the published ASM86, not a host encoder."""
from pathlib import Path
import json,sys,re
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'qa/asm0'));sys.path.insert(0,str(ROOT/'tools'))
from dos_machine import assemble
from ir86_runtime_text import runtime
asm=(ROOT/'workbench/asm0/ASM86.COM').read_bytes();profiles={}
for level in range(1,31):
 text=runtime(level)
 if text:
  source='JMP R_DONE\n'+text+'\nR_DONE:\nRET\n'
  built=assemble(asm,source,'RTSIZE')
  assert built.exitcode==0,(level,built.output,source)
  size=len(built.files['RTSIZE.COM'])-4
 else:size=0
 profiles[level]=dict(bytes=size,definitions=len(re.findall(r'^\w+:$',text,re.M)))
(ROOT/'qa/ir86/runtime-sizes.json').write_text(json.dumps(profiles,indent=2)+'\n')
print('PASS runtime sizes measured by ASM86:',profiles[30])
