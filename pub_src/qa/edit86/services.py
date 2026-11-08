"""Bootstrap the published editor services with the existing self-hosted trio."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'qa/toolchain'))
from common import run,W as TOOLS
W=ROOT/'workbench/edit86';Q=ROOT/'qa/edit86'
RUNTIME={'EDITRT.ASM':(W/'EDITRT.ASM').read_bytes()}
def build(source,compiler=None,translator=None,runtime=None):
 c=compiler or (TOOLS/'RILL.COM').read_bytes();i=translator or (TOOLS/'IR86.COM').read_bytes()
 r=run(c,source,'RIL');assert r.exitcode==0,r.output
 ir=r.files['RESULT.IR'];r=run(i,ir,files=RUNTIME if runtime is None else {'EDITRT.ASM':runtime});assert r.exitcode==0,r.output
 asm=r.files['RESULT.ASM'];r=run((TOOLS/'ASM86A.COM').read_bytes(),asm,'ASM');assert r.exitcode==0,r.output
 return ir,asm,r.files['RESULT.COM']
if __name__=='__main__':
 facts={}
 for name in ['RILLED','IRED']:
  ir,asm,image=build((W/(name+'.RIL')).read_bytes());(W/(name+'B.COM')).write_bytes(image)
  facts[name]={'bootstrap_ir_bytes':len(ir),'bootstrap_assembly_bytes':len(asm),'bootstrap_binary_bytes':len(image)}
  print(name,'bootstrap',len(image),flush=True)
 c=(W/'RILLEDB.COM').read_bytes();i=(W/'IREDB.COM').read_bytes()
 for generation in range(3):
  nc=build((W/'RILLED.RIL').read_bytes(),c,i);ni=build((W/'IRED.RIL').read_bytes(),c,i)
  if generation:assert nc[2]==c and ni[2]==i,'editor-service rebuild differs'
  c=nc[2];i=ni[2]
  print('PASS service generation',generation,len(c),len(i),flush=True)
 (W/'RILLED.COM').write_bytes(c);(W/'IRED.COM').write_bytes(i)
 for name,result in [('RILLED',nc),('IRED',ni)]:
  facts[name].update(ir_bytes=len(result[0]),assembly_bytes=len(result[1]),binary_bytes=len(result[2]))
 (Q/'platform-facts.json').write_text(json.dumps(facts,indent=2)+'\n')
