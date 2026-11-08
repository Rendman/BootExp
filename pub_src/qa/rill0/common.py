"""Run only the published IR translator, assembler, and their native outputs."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'qa/asm0'))
sys.path.insert(0,str(ROOT/'qa/ir86'))
from dos_machine import DosMachine,assemble
from portable_machine import Machine
W=ROOT/'workbench/rill0';Q=ROOT/'qa/rill0'
def build_ir(source,name='RILL'):
 ir=(ROOT/'workbench/ir86/IR86.COM').read_bytes()
 asm=(ROOT/'workbench/asm0/ASM86.COM').read_bytes()
 translated=DosMachine({name+'.IR':source},[name]).run(ir)
 assert translated.exitcode==0,(name,translated.output)
 assembly=translated.files[name+'.ASM']
 built=assemble(asm,assembly,name)
 assert built.exitcode==0,(name,built.output)
 return assembly,built.files[name+'.COM']
def run_compiler(source,image=None,files=None):
 given=dict(files or {})
 if source is not None:given['SOURCE.RIL']=source.encode('ascii') if isinstance(source,str) else source
 return DosMachine(given).run(image if image is not None else (W/'RILL.COM').read_bytes())
if __name__=='__main__':
 assembly,image=build_ir((W/'RILL.IR').read_bytes())
 (W/'RILL.ASM').write_bytes(assembly);(W/'RILL.COM').write_bytes(image)
 print('RILL.COM:',len(image),'bytes; assembly text:',len(assembly),'bytes')
 for source in ['fn main() { putc(72); putc(73); }','fn main() { let mut x = 48; while x < 51 { putc(x); x = x + 1; } }']:
  r=run_compiler(source,image);print(r.exitcode,r.output,r.files.get('RESULT.IR'))
