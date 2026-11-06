"""Check the seed/compiler handoff and examples through both published builders."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'qa/toolchain'))
from common import run,ir,W
Q=ROOT/'qa/compiler_collections';records=[];logs=[]
for c in json.loads((ROOT/'qa/toolchain/examples.json').read_text()):
 outputs=[]
 for name in ['RILLBOOT','RILL']:
  r=run((W/(name+'.COM')).read_bytes(),c['source'],'RIL');assert r.exitcode==0,(name,c['name'],r.output)
  text=r.files['RESULT.IR'];assembly,image=ir(text);n=run(image,files={k:v.encode() for k,v in c.get('files',{}).items()})
  assert n.exitcode==0 and n.output==c['output'].encode(),(name,c['name'],n.output)
  if c.get('result_file'):assert n.files[c['result_file']]==c['files']['IN.TXT'].encode()
  bad=run((W/(name+'.COM')).read_bytes(),c['bad'],'RIL',{'RESULT.IR':text})
  assert bad.exitcode==1 and bad.output.decode().strip()==c['error'] and bad.files['RESULT.IR']==text
  outputs.append((text,assembly,image))
 assert outputs[0]==outputs[1],c['name']
 text,assembly,image=outputs[1]
 assert (len(text),len(assembly),len(image))==(c['ir_bytes'],c['assembly_bytes'],c['binary_bytes']),c['name']
 if c['name'] in ['ERECUR','EHEAP','ECOPY']:records.append(c)
 logs.append('PASS '+c['name']+': RB/RC identical IR, assembly and executable; exact runtime/file output, rejection and preservation')
source=(W/'RILL.RIL').read_bytes();compiled=run((W/'RILLBOOT.COM').read_bytes(),source,'RIL');assert compiled.exitcode==0
_,image=ir(compiled.files['RESULT.IR']);assert image==(W/'RILL.COM').read_bytes()
for _ in range(2):
 r=run(image,source,'RIL');assert r.exitcode==0;_,again=ir(r.files['RESULT.IR']);assert again==image;image=again
logs.append('PASS RB-to-RC handoff: seed builds canonical RILL, two self-builds reproduce 26625 bytes')
(Q/'rc-examples.json').write_text(json.dumps(records,indent=2)+'\n');(Q/'example-results.txt').write_text('\n'.join(logs)+'\n');print('\n'.join(logs))
