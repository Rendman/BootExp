from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'qa/asm86a'))
from machine import AssemblerMachine,run_assembler
W=ROOT/'workbench/toolchain';Q=ROOT/'qa/toolchain'
def run(image,source=None,kind='IR',files=None,limit=2_000_000_000):
 f=dict(files or {})
 if source is not None:f['SOURCE.'+kind]=source.encode('ascii') if isinstance(source,str) else source
 return AssemblerMachine(f).run(image,limit=limit)
def asm(source):
 r=run_assembler((ROOT/'workbench/asm86a/ASM86A.COM').read_bytes(),source)
 if r.exitcode:
  (Q/'failed-source.asm').write_bytes(source.encode() if isinstance(source,str) else source)
  raise AssertionError(bytes(r.output))
 return r.files['RESULT.COM']
def ir(source,translator=None):
 r=run(translator or (ROOT/'workbench/ir86/IRWIDE.COM').read_bytes(),source)
 assert r.exitcode==0,bytes(r.output)
 return r.files['RESULT.ASM'],asm(r.files['RESULT.ASM'])
if __name__=='__main__':
 image=asm((ROOT/'workbench/ir86/IRWIDE.ASM').read_bytes());(ROOT/'workbench/ir86/IRWIDE.COM').write_bytes(image)
 print('IRWIDE',len(image))
 a,b=ir('PROC MAIN 0 0\nLIT 72\nPUTC\nLIT 73\nPUTC\nLIT 0\nRETURN\n');r=run(b);assert r.exitcode==0 and r.output==b'HI',(r.exitcode,r.output);print('PASS streaming procedure test')
