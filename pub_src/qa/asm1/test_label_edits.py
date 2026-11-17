"""Follow the published label locators and build the results with ASM0."""
from pathlib import Path
import sys,json,runpy
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'qa/asm86'))
from machine import assemble
checks=runpy.run_path(str(ROOT/'qa/asm1/validate_steps.py'))
apply=checks['apply_label_edits'];code=checks['code']
intro=json.loads((ROOT/'qa/asm1/intro-patches.json').read_text())
later=[s for s in json.loads((ROOT/'qa/asm86/article-patches.json').read_text()) if s['collection']=='asma0']
stages=[(s,'asm1',s['source']) for s in intro]+[(s,'asm86',f'A{s["number"]:02}.ASM') for s in later]
program=(ROOT/'workbench/asm0/ASM86.ASM').read_text().splitlines()
builder=(ROOT/'workbench/asm0/ASM86.COM').read_bytes();records=[]
for stage,folder,source in stages:
 # Vary indentation, notes and blank lines. These must not act as coordinates.
 formatted=[]
 for i,line in enumerate(program):
  if i%9==0:formatted+=['','; Workbench note']
  formatted.append('  '+line)
 text=(ROOT/'site/content/bootstrap/asm1'/stage['page']).read_text()
 program=apply(formatted,stage,text)
 canonical=ROOT/'workbench'/folder/source
 assert program==code(canonical.read_text().splitlines()),source
 built=assemble(builder,'\r\n'.join(program)+'\r\n')
 assert built.exitcode==0,(source,built.output)
 assert built.files['RESULT.COM']==canonical.with_suffix('.COM').read_bytes(),(source,'machine bytes differ')
 result='PASS '+source+': label-only edits with different spacing/notes; ASM0 reproduces the established executable'
 records.append(result);print(result,flush=True)
(ROOT/'qa/asm1/label-edit-results.txt').write_text('\n'.join(records)+'\n')
print('PASS all 18 ASM1 checkpoints reconstructed without line positions and assembled byte-for-byte')
