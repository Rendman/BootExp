"""Execute the published BASIC to build ASM86; no outside assembler is used."""
from pathlib import Path
import io,sys,json,tempfile,shutil
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/python'))
sys.path.insert(0,str(ROOT/'tools/python-pcbasic207'))
import pcbasic
WORK=ROOT/'workbench/asm0'
def basic_build(stem='ASM86'):
 assert (WORK/'BOOTASM.BAS').read_bytes()==(ROOT/'workbench/bootasm/BOOTASM.BAS').read_bytes(), 'Bootstrap source differs between collections'
 out=io.BytesIO()
 with tempfile.TemporaryDirectory() as directory:
  target=Path(directory)
  shutil.copyfile(WORK/'BOOTASM.BAS',target/'BOOTASM.BAS')
  shutil.copyfile(WORK/(stem+'.ASM'),target/'SOURCE.ASM')
  with pcbasic.Session(input_streams=io.BytesIO(),output_streams=out,devices={'A':str(target)},current_device='A:') as session:
   session.execute('LOAD "BOOTASM.BAS"')
   session.execute('RUN')
   log=out.getvalue().decode('ascii',errors='replace')
   symbols={}
   count=int(session.get_variable('SC!'))
   names=session.get_variable('SY$()')
   values=session.get_variable('SV!()')
   for i in range(count):
    symbols[names[i].decode('ascii')]=int(values[i])
   (ROOT/'qa/asm0'/('basic-'+stem+'-symbols.json')).write_text(json.dumps(symbols,indent=2))
  if (target/'RESULT.COM').exists():shutil.copyfile(target/'RESULT.COM',WORK/(stem+'.COM'))
 (ROOT/'qa/asm0'/('basic-'+stem+'.log')).write_text(log)
 print(log,flush=True)
 return log
if __name__=='__main__':
 log=basic_build(sys.argv[1] if len(sys.argv)>1 else 'ASM86')
 if 'OK ' not in log:
  raise SystemExit(1)
