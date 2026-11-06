"""Rebuild all three tools twice using only their RILL implementations."""
from common import *
import json,time
names=['ASM86A','IR86','RILL'];images={n:(W/(n+'.COM')).read_bytes() for n in names};logs=[]
for generation in [1,2]:
 produced={}
 for name in names:
  start=time.monotonic();r=run(images['RILL'],(W/(name+'.RIL')).read_bytes(),'RIL');assert r.exitcode==0,(generation,name,'compile',r.output)
  r=run(images['IR86'],r.files['RESULT.IR']);assert r.exitcode==0,(generation,name,'translate',r.output)
  a=r.files['RESULT.ASM'];r=run(images['ASM86A'],a,'ASM');assert r.exitcode==0,(generation,name,'assemble',r.output)
  image=r.files['RESULT.COM'];assert image==images[name],(generation,name,'different executable',len(image),len(images[name]))
  (W/f'{name}{generation}.COM').write_bytes(image);produced[name]=image
  line=f'PASS generation {generation} {name}: RILL -> RILL-written IR86 -> RILL-written ASM86A; {len(image)} identical bytes'
  print(line,round(time.monotonic()-start,2),flush=True);logs.append(line)
 images=produced
(Q/'rebuild-results.txt').write_text('\n'.join(logs)+'\n')
(Q/'self-build-facts.json').write_text(json.dumps({n:len(b) for n,b in images.items()},indent=2)+'\n')
