"""Package the published IR source chain and native-produced assembly text."""
from pathlib import Path
import json,shutil,zipfile
from ir86_runtime_text import runtime
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/ir86';D=ROOT/'site/static/downloads/ir86';D.mkdir(parents=True,exist_ok=True)
def dos(name,text):(W/name).write_bytes((text.rstrip()+'\n').replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
for name,folder in [('BOOTASM.BAS','bootasm'),('ASM86.ASM','asm86'),('AS07.ASM','asm86'),('VIEW.BAS','bootasm'),('CHECK.BAT','bootasm')]:shutil.copyfile(ROOT/'workbench'/folder/name,W/name)
dos('RUNTIME.ASM',runtime(30))
dos('README.TXT','''THE BOOTSTRAP PROJECT - IR86
A practical course in small-system software

Begin with the completed BOOTASM and ASM86 collections.
Read The IR workbench before the construction installments.

BOOTASM.BAS The identical published BASIC bootstrap assembler.
ASM86.ASM   The identical published native assembler source.
AS07.ASM    The published reader used as the first source base.
IR01.ASM through IR32.ASM: complete construction checkpoints.
IR86.ASM    Completed translator, identical to IR32.ASM.
T01.IR through T32.IR: accepted input fixtures.
X01.IR through X32.IR: rejected input fixtures.
T-prefixed ASM files: expected text produced by the translator tests.
VIEW.BAS and CHECK.BAT: the unchanged published workbench helpers.
HELLO.IR, COUNT.IR, BYTES.IR, ECHOIR.IR: complete portable examples.
RUNTIME.ASM: the 8086/DOS binding fragment; do not run it alone.
COPYFILE.IR: the complete file-copy pipeline program.
Matching example ASM files were produced by the translator.

Use your own DOS and period GW-BASIC interpreter. Build ASM86 with
GWBASIC BOOTASM.BAS, requiring BASIC's OK; SYSTEM returns to DOS.
Preserve a tested ASM86.COM as ASMKEEP.COM. Run CHECK ASMKEEP and
enter IR01, for example, to build a checkpoint directly.
All IR construction checkpoints are complete executable tools.
The first diagnostics do not create an assembly file.
The T03 output is data only: inspect it and do not execute it.
Other published emitted programs are expressly complete executables.

The finished path is NAME.IR -> IR86 -> NAME.ASM -> ASM86 -> NAME.COM.
Run CHECK IR86 and enter NAME. Require OK and PASS. Run CHECK ASMKEEP
and enter NAME again; require its own OK and PASS. Only then use the
new machine file. TYPE inspects text; VIEW.BAS inspects length/bytes.
Preserve a tested translator as IRKEEP.COM and keep its source.

Names at file prompts are 1-8 letters, digits, or underscores, without
path or extension. Use ordinary disk files, not DOS devices.
Source errors leave older assembly output untouched; I/O failures
during writing may leave partial output. Require a fresh OK.

IR86 defines virtual accumulator A and sixteen-bit word semantics.
Its source does not expose processor registers or flags. Runtime
services use opaque file handles, byte streams, and normalized STATUS.
Ordinary computations do not replace that status. READ/WRITE consume
a saved handle and buffer pointer, with the count in A. Consult the
language reference and its separate target-profile section.

COPYFILE reads IN.TXT and creates or truncates OUT.TXT. Test it in
the work directory with the supplied sentence and compare the files.
It returns one on failure and can leave partial output after an I/O
error. It treats file contents as bytes, including Control-Z.

All sources are ASCII with DOS line endings and 8.3 filenames.
No preassembled executable or historical interpreter is included.
''')
files=['BOOTASM.BAS','ASM86.ASM','AS07.ASM','VIEW.BAS','CHECK.BAT','README.TXT','IR86.ASM','RUNTIME.ASM']
for c in json.loads((ROOT/'qa/ir86/checkpoints.json').read_text()):
 n=c['number'];files+=[c['source'],f'T{n:02}.IR',f'X{n:02}.IR']
 if 'console' not in c:files.append(f'T{n:02}.ASM')
for name in ['HELLO','COUNT','BYTES','ECHOIR','COPYFILE']:files.extend([name+'.IR',name+'.ASM'])
for name in files:shutil.copyfile(W/name,D/name)
archive=D/'IR86.ZIP';unchanged=False
if archive.exists():
 with zipfile.ZipFile(archive) as z:unchanged=z.namelist()==files and all(z.read(n)==(W/n).read_bytes() for n in files)
if not unchanged:
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for name in files:
   info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(W/name).read_bytes())
(ROOT/'qa/ir86/package-files.json').write_text(json.dumps(files,indent=2)+'\n')
print(f'Packaged {len(files)} IR86 source files')
