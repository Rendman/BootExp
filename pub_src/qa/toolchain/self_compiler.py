from common import *
seed=(W/'RILLBOOT.COM').read_bytes();source=(W/'RILL.RIL').read_bytes();records=[]
for generation in range(3):
 r=run(seed,source,'RIL');print(generation,'compile',r.exitcode,bytes(r.output),flush=True)
 if r.exitcode:
  (Q/'compiler-rejection.txt').write_bytes(r.output);raise AssertionError(r.output)
 text=r.files['RESULT.IR'];(W/f'RILL{generation}.IR').write_bytes(text)
 a,image=ir(text);(W/f'RILL{generation}.ASM').write_bytes(a);(W/f'RILL{generation}.COM').write_bytes(image)
 print(generation,'native',len(text),len(a),len(image),flush=True)
 if generation:assert image==seed,'self-build differs'
 seed=image
 records.append(f'PASS RILL generation {generation}: {len(text)} IR bytes, {len(image)} native bytes')
(W/'RILL.COM').write_bytes(seed);(Q/'self-compiler-results.txt').write_text('\n'.join(records)+'\n')
