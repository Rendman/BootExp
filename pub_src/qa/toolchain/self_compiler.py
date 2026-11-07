"""Establish RILL's own frame convention before comparing self-builds."""
from common import *
import json

source=(W/'RILL.RIL').read_bytes()
assert source==(W/'RC43.RIL').read_bytes()
seed=(W/'RILLBOOT.COM').read_bytes();records=[];facts={}
for generation in range(4):
 r=run(seed,source,'RIL');assert r.exitcode==0,r.output
 text=r.files['RESULT.IR'];a,image=ir(text)
 if generation==0:
  (W/'RC43.COM').write_bytes(image)
  facts.update(boot_binary_bytes=len(image),boot_ir_bytes=len(text),boot_assembly_bytes=len(a))
 else:
  stem=f'RILL{generation-1}'
  (W/(stem+'.IR')).write_bytes(text);(W/(stem+'.ASM')).write_bytes(a);(W/(stem+'.COM')).write_bytes(image)
  if generation>1:assert image==seed,'self-build differs'
  else:facts.update(binary_bytes=len(image),ir_bytes=len(text),assembly_bytes=len(a))
 seed=image
 records.append(('PASS RILLBOOT -> RC43' if generation==0 else f'PASS RILL generation {generation-1}')+f': {len(text)} IR bytes, {len(image)} native bytes'+('; identical to previous generation' if generation>1 else ''))
 print(records[-1],flush=True)
(W/'RILL.COM').write_bytes(seed)
(Q/'local-capacity.json').write_text(json.dumps(facts,indent=2)+'\n')
(Q/'self-compiler-results.txt').write_text('\n'.join(records)+'\n')
