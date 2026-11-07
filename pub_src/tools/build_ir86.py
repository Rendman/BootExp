"""Arrange the single required native IR86 construction; never encode instructions."""
from pathlib import Path
import json,shutil
from build_ir86_extensions import build,ROOT,OPS

def main():
 build();W=ROOT/'workbench/ir86';T=ROOT/'workbench/toolchain';Q=ROOT/'qa/ir86'
 cases=json.loads((ROOT/'qa/toolchain/ir-extensions.json').read_text())
 for c in cases:
  n=c['number'];shutil.copyfile(T/c['source'],W/f'IR{n:02}.ASM')
  shutil.copyfile(T/f'TIW{n:02}.IR',W/f'T{n:02}.IR')
  c['source']=f'IR{n:02}.ASM'
 shutil.copyfile(W/f'IR{len(cases):02}.ASM',W/'IR86.ASM')
 shutil.copyfile(W/'IR86.ASM',W/'IRWIDE.ASM')
 (Q/'checkpoints.json').write_text(json.dumps(cases,indent=2)+'\n')
 (Q/'language.json').write_text(json.dumps(OPS,indent=2)+'\n')
 print('Prepared one native IR86 construction and its retained complete source')
if __name__=='__main__':main()
