"""Package reader source only, including exact article examples and fixtures."""
from pathlib import Path
import json,re,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/asm86';D=ROOT/'site/static/downloads/asm86'
D.mkdir(parents=True,exist_ok=True)
def dos(name,text):(W/name).write_bytes((text.rstrip()+'\n').replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
for name in ['VIEW.BAS','CHECK.BAT']:shutil.copyfile(ROOT/'workbench/bootasm'/name,W/name)
source=(ROOT/'workbench/bootasm/BOOTASM.BAS').read_text()
source=source.replace('22 DIM SY$(127), SV(127)','22 DIM SY$(255), SV(255)').replace('7030 IF SC=128 THEN','7030 IF SC=256 THEN')
dos('BAWIDE.BAS',source)
examples=ROOT/'site/content/bootstrap/asm86/32-programs.md'
blocks=re.findall(r'```asm\n(.*?)\n```',examples.read_text(),re.S)
for name,block in zip(['HELLO','MEMORY','COUNT'],blocks):dos(name+'.ASM',block)
dos('README.TXT','''THE BOOTSTRAP PROJECT - ASM86
A practical course in small-system software

Begin with the completed BOOTASM collection and its BASIC workbench.
Read The assembly workbench before the construction installments.

BAWIDE.BAS  BOOTASM with the printed symbol-table changes.
AS01.ASM through AS29.ASM: complete saved construction checkpoints.
ASM86.ASM   Completed native assembler, identical to AS29.ASM.
VIEW.BAS    The unchanged BOOTASM length and hexadecimal byte viewer.
CHECK.BAT   The unchanged immediate DOS status checker.
T04.ASM through T29.ASM: checkpoint input fixtures.
X07.ASM through X29.ASM: source rejection fixtures where applicable.
HELLO.ASM, MEMORY.ASM, COUNT.ASM: three complete example programs.

Use your own DOS and period GW-BASIC interpreter. GWBASIC is the name
used in the articles; substitute the actual name on your disk.
GWBASIC BAWIDE.BAS builds a checkpoint. Enter AS01, for example.
Require BASIC's OK and byte count; SYSTEM returns to DOS.
CHECK AS01 executes that complete checkpoint and prints PASS or FAIL.
Keep BOOTKEEP.BAS and a tested BASIC-built ASMKEEP.COM separately.

AS01 through AS29 are complete executable tools or diagnostics.
Their output fixtures are usually data or encoding exercises: inspect
with VIEW.BAS, including file length. Do not execute those outputs.
Only T25, T28, T29, and the three example programs are expressly
complete output programs. The rejection cases must report FAIL.

Run CHECK ASM86 and enter a plain 1-8-character source base name.
Use ordinary disk names, not DOS devices such as CON or NUL.
Source errors leave an older output unchanged. Require a fresh OK
before use; an I/O error during writing can leave a partial file.
The native tool requires a full 64 KB segment and entry SP=FFFEH.
Its limits are 8192 output bytes, 4000 lines, 120 characters per line,
16 characters per token/name, and 256 labels. See the reference.

All source is ASCII with DOS line endings and 8.3 filenames.
This collection contains no preassembled programs or interpreter.
''')
files=['BAWIDE.BAS','ASM86.ASM','VIEW.BAS','CHECK.BAT','README.TXT','HELLO.ASM','MEMORY.ASM','COUNT.ASM']
for case in json.loads((ROOT/'qa/asm86/checkpoints.json').read_text()):
 n=case['number'];files.append(case['source'])
 if case['fixture'] is not None:files.append(f'T{n:02}.ASM')
 if case['bad'] and case['bad']['kind']=='source':files.append(f'X{n:02}.ASM')
for name in files:shutil.copyfile(W/name,D/name)
archive=D/'ASM86.ZIP'
unchanged=False
if archive.exists():
 with zipfile.ZipFile(archive) as z:unchanged=z.namelist()==files and all(z.read(name)==(W/name).read_bytes() for name in files)
if not unchanged:
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for name in files:
   info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,(W/name).read_bytes())
(ROOT/'qa/asm86/package-files.json').write_text(json.dumps(files,indent=2)+'\n')
print(f'Packaged {len(files)} ASM86 source files')
