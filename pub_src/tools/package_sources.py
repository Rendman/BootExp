"""Prepare only the reader's source collection; exclude execution artifacts."""
from pathlib import Path
import json,shutil,zipfile,re
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/bootasm';D=ROOT/'site/static/downloads/bootasm'
def dos(p,text):p.write_bytes((text.rstrip()+'\n').replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
page=ROOT/'site/content/bootstrap/bootasm/00-workbench.md'
checker=re.search(r'```dos\n(ECHO OFF\n.*?)\n```',page.read_text(),re.S).group(1)
dos(W/'CHECK.BAT',checker)
examples=ROOT/'site/content/bootstrap/bootasm/20-programs.md'
blocks=re.findall(r'```asm\n(.*?)\n```',examples.read_text(),re.S)
for name,block in zip(['HELLO','COPYBYTE','FAIL'],blocks):dos(W/(name+'.ASM'),block)
dos(W/'README.TXT','''THE BOOTSTRAP PROJECT - BOOTASM
A practical course in small-system software

Read the BOOTASM collection in order, beginning with The workbench.

BYTE.BAS    The first one-byte exercise.
VIEW.BAS    A file-length and hexadecimal byte viewer.
BA02.BAS through BA18.BAS: complete saved construction checkpoints.
BOOTASM.BAS The completed assembler; the same program as BA18.BAS.
CHECK.BAT   Runs a complete COM program and prints PASS or FAIL.
T02.ASM through T18.ASM: installment acceptance fixtures.
X02.ASM through X18.ASM: installment rejection fixtures.
HELLO.ASM, COPYBYTE.ASM, FAIL.ASM: complete example programs.

Use your own DOS and GW-BASIC interpreter. The workbench instructions
call the interpreter GWBASIC; use the name supplied on your own disk.
Run GWBASIC BOOTASM.BAS, then enter a source base name without an
extension. Require an OK report before treating output as new.
Save a tested copy of BOOTASM.BAS as BOOTKEEP.BAS before changing it.

Inspect encoding and data fixtures with VIEW.BAS. Do not execute them.
Only T09, T10, T17, T18 and the three complete examples are intended
as executable programs. CHECK FAIL must report FAIL: that example
returns a deliberately nonzero status.

Source is ASCII with DOS line endings and short filenames. BASIC line
numbers belong to the source. There are no preassembled programs in
this collection. Empty assembly output is valid for inspection only.
''')
files=['BYTE.BAS','VIEW.BAS','BOOTASM.BAS','CHECK.BAT','README.TXT','HELLO.ASM','COPYBYTE.ASM','FAIL.ASM']
for stage in json.loads((ROOT/'qa/checkpoints.json').read_text()):
 i=stage['number'];files.extend([stage['source'],f'T{i:02}.ASM',f'X{i:02}.ASM'])
for name in files:shutil.copyfile(W/name,D/name)
archive=D/'BOOTASM.ZIP'
unchanged=False
if archive.exists():
 with zipfile.ZipFile(archive) as z:unchanged=z.namelist()==files and all(z.read(name)==(W/name).read_bytes() for name in files)
if not unchanged:
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for name in files:
   info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,(W/name).read_bytes())
print(f'Packaged {len(files)} source files')
import runpy
runpy.run_path(str(ROOT/'tools/package_asm86.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tools/package_asma0.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tools/package_asm86a.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tools/package_ir86.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tools/package_rill.py'),run_name='__main__')

runpy.run_path(str(ROOT/'tools/package_toolchain.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tools/package_compiler_collections.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tools/package_reader_names.py'),run_name='__main__')
