"""Self-build RC43 before using it to build the 64-local continuation."""
from common import *
import json

records=[]
seed=(W/'RILLBOOT.COM').read_bytes()
initial=(W/'RC43.RIL').read_bytes()
for generation in range(3):
 r=run(seed,initial,'RIL');assert r.exitcode==0,r.output
 a,image=ir(r.files['RESULT.IR'])
 if generation:assert image==seed,'initial self-build differs'
 seed=image
 (W/'RC43.COM').write_bytes(image)
 records.append(f'PASS RC43 generation {generation}: {len(image)} identical native bytes')
 print(records[-1],flush=True)
initial_bytes=len(seed)

source=(W/'RILL.RIL').read_bytes()
assert source==(W/'RC44.RIL').read_bytes()
for generation in range(4):
 r=run(seed,source,'RIL');assert r.exitcode==0,r.output
 text=r.files['RESULT.IR'];a,image=ir(text)
 stem='RC44BOOT' if generation==0 else f'RILL{generation-1}'
 if generation:
  (W/(stem+'.IR')).write_bytes(text);(W/(stem+'.ASM')).write_bytes(a)
 (W/(stem+'.COM')).write_bytes(image)
 if generation>1:assert image==seed,'extended self-build differs'
 if generation==0:extension=dict(initial_compiler_bytes=initial_bytes,boot_binary_bytes=len(image),boot_ir_bytes=len(text),boot_assembly_bytes=len(a))
 if generation==1:extension.update(binary_bytes=len(image),ir_bytes=len(text),assembly_bytes=len(a))
 seed=image
 records.append(f'PASS RC44 '+('predecessor build' if generation==0 else f'generation {generation-1}')+f': {len(text)} IR bytes, {len(image)} native bytes'+('; identical to previous generation' if generation>1 else ''))
 print(records[-1],flush=True)
(W/'RC44.COM').write_bytes(seed)
(W/'RILL.COM').write_bytes(seed)
(Q/'local-capacity.json').write_text(json.dumps(extension,indent=2)+'\n')
(Q/'self-compiler-results.txt').write_text('\n'.join(records)+'\n')
