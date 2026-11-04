"""Build every published assembly checkpoint by executing BOOTASM.BAS."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from bootstrap import basic_build,WORK,ROOT
import json
def build(name):
 image=WORK/(name+'.COM');expected=image.read_bytes();image.unlink()
 log=basic_build(name)
 assert 'OK '+name+'.COM' in log,(name,log)
 assert image.read_bytes()==expected,name+' BASIC and native output differ'
 return f'PASS {name}: BASIC and native output match every byte ({len(expected)} bytes)'
if __name__=='__main__':
 names=[Path(c['source']).stem for c in json.loads((ROOT/'qa/asm86/checkpoints.json').read_text())]
 with ProcessPoolExecutor(max_workers=4) as pool:results=list(pool.map(build,names))
 (ROOT/'qa/asm86/basic-results.txt').write_text('\n'.join(results)+'\n')
 print('\n'.join(results))
