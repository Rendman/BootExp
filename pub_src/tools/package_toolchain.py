"""Package the authored bootstrap and self-hosting sources without executables."""
from project_paths import directory_name
from pathlib import Path
import shutil,json,zipfile,re
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/toolchain';D=ROOT/'site/downloads/toolchain';D.mkdir(parents=True,exist_ok=True)
def dos(name,s):(W/name).write_bytes(s.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
for name,group in [('BOOTASM.BAS','bootasm'),('VIEW.BAS','bootasm'),('CHECK.BAT','bootasm'),('ASM86.ASM','asm86'),('ASMA0.ASM','asma0'),('ASM86A.ASM','asm86a'),('IRWIDE.ASM','ir86'),('RILLBOOT.IR','rill'),('RILL.IR','rill')]:shutil.copyfile(ROOT/'workbench'/directory_name(group)/name,W/name)
commands=['ECHO OFF','IF NOT EXIST ASMAKEEP.COM GOTO MISSING','COPY IRWIDE.ASM SOURCE.ASM >NUL','ASMAKEEP','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.COM IRWIDE.COM >NUL','COPY RILLBOOT.IR SOURCE.IR >NUL','IRWIDE','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.ASM SOURCE.ASM >NUL','ASMAKEEP','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.COM RILLBOOT.COM >NUL']
# Preserve the first complete compiler as a required construction milestone.
dos('TSMALL.RIL','fn main(){putc(72);putc(73);return 0;}\n')
insert=commands.index('COPY RILLBOOT.IR SOURCE.IR >NUL')
commands[insert:insert]=['COPY RILL.IR SOURCE.IR >NUL','IRWIDE','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.ASM SOURCE.ASM >NUL','ASMAKEEP','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.COM RILL0.COM >NUL','COPY TSMALL.RIL SOURCE.RIL >NUL','RILL0','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.IR SOURCE.IR >NUL','IRWIDE','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.ASM SOURCE.ASM >NUL','ASMAKEEP','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.COM STEST.COM >NUL','STEST','IF ERRORLEVEL 1 GOTO FAILED','ECHO PASS RILL0 PROGRAM']
commands += ['COPY RILL.RIL SOURCE.RIL >NUL','RILLBOOT','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.IR SOURCE.IR >NUL','IRWIDE','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.ASM SOURCE.ASM >NUL','ASMAKEEP','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.COM RBOOT.COM >NUL']
for name,stem in [('RILL','R'),('IR86','I'),('ASM86A','A')]:
 commands += [f'COPY {name}.RIL SOURCE.RIL >NUL','RBOOT' if name=='RILL' else 'R0','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.IR SOURCE.IR >NUL','IRWIDE','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.ASM SOURCE.ASM >NUL','ASMAKEEP','IF ERRORLEVEL 1 GOTO FAILED',f'COPY RESULT.COM {stem}0.COM >NUL',f'ECHO PASS {name} INITIAL BUILD']
for gen in [1,2]:
 for name,stem in [('RILL','R'),('IR86','I'),('ASM86A','A')]:
  commands += [f'COPY {name}.RIL SOURCE.RIL >NUL',f'R{gen-1}','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.IR SOURCE.IR >NUL',f'I{gen-1}','IF ERRORLEVEL 1 GOTO FAILED','COPY RESULT.ASM SOURCE.ASM >NUL',f'A{gen-1}','IF ERRORLEVEL 1 GOTO FAILED',f'COPY RESULT.COM {stem}{gen}.COM >NUL',f'ECHO PASS {name} GENERATION {gen}']
commands += ['ECHO BUILDS COMPLETE - COMPARE THE GENERATIONS','GOTO END',':MISSING','ECHO MISSING TESTED ASMAKEEP.COM','GOTO END',':FAILED','ECHO FAIL - STOP AT THE FIRST TOOL ERROR',':END']
dos('TMAKE.BAT','\n'.join(commands)+'\n')
native_bytes=next(c['binary_bytes'] for c in json.loads((ROOT/'qa/asm86/checkpoints.json').read_text()) if c['number']==40)
dos('README.TXT',f'''THE BOOTSTRAP PROJECT - THE TOOLCHAIN IN RILL
A practical course in small-system software

The ladder is BOOTASM -> ASM86 -> ASMA0 -> ASM86A -> streaming IR86
-> RILL0 -> IR-written RILLBOOT seed -> RILL-written compiler, translator,
and assembler -> two matching rebuild generations of all three tools.

BOOTASM.BAS and ASM86.ASM are the unchanged published foundation.
ASMA0.ASM and ASM86A.ASM are the unchanged native assembler milestones.
IRWIDE.ASM is the streaming native IR86 bootstrap translator.
RILLBOOT.IR is the compiler seed, authored in processor-neutral IR86.
RILL.RIL, IR86.RIL, ASM86A.RIL implement the three tools in RILL.
TMAKE.BAT rebuilds the native translator, RILL0 and its HI program,
then the compiler seed. RILLBOOT builds the completed RC43 compiler
as RBOOT. RBOOT compiles the same source with 64-slot frames to
establish R0;
R0 then builds the RILL-written translator and assembler. It
then rebuilds each tool twice using only the RILL implementations.
VIEW.BAS and CHECK.BAT are the unchanged workbench helpers.
IW01.ASM through IW23.ASM: identical aliases of IR01 through IR23.
RILL.IR: the completed first compiler, continued by RB01 through RB12.
RC01.RIL through RC43.RIL: the compiler written in RILL.
RILL.RIL: identical to the completed RC43.RIL, with 64 local slots.
TLOCAL.RIL, XLOCAL.RIL, TSCOPE.RIL: local/frame boundary exercises.
T-prefixed inputs and X-prefixed rejection cases accompany those tools.
The named example RIL/IR files accompany the interface articles.

Use your own DOS 3.10 and its period BASIC interpreter. Begin with the
completed ASM86A workbench: ASMAKEEP.COM must be the tested {native_bytes}-byte
native assembler. Keep it and the sources on a separate labeled disk.
TMAKE deliberately preserves that builder. Do not start from a supplied
binary: none is present. Use a hard-disk working directory, with enough
space for source files, generated IR/assembly, and preserved executables.
The full course archive need not fit a single 360 KB floppy.

TMAKE checks each tool status immediately. Its PASS markers identify
the RILL0 program and completed initial/rebuild tool pipelines.
A nonzero tool status immediately stops the batch with FAIL. Stop at
that first error; old output never proves a new successful translation.
A0.COM/I0.COM/R0.COM are the first RILL-written assembler/IR/compiler.
A1/I1/R1 and A2/I2/R2 are the next two generations.
ECHO N>NO.TXT answers COMP's compare-more-files question. Compare
A0.COM A1.COM, A0.COM A2.COM, I0.COM I1.COM, I0.COM I2.COM,
R0.COM R1.COM, and R0.COM R2.COM, each with COMP and <NO.TXT.
Every comparison must report no differences. Byte equality and fresh
successful builds are separate checks.

RILL reads SOURCE.RIL and publishes RESULT.IR using RILL.TMP/RILL.BAK.
IR86 reads SOURCE.IR and publishes RESULT.ASM using IRTX.TMP/IRRES.BAK.
ASM86A reads SOURCE.ASM and publishes RESULT.COM using ASMA.TMP and
RESULT.BAK. Existing recovery names prevent a new run; inspect them.
Each tool streams bounded blocks and preserves old output on source
rejection. A failed publication can leave recovery files. Require OK
and immediate status success before copying any result.

The RILL implementations require no outside compiler, assembler,
linker, embedded project executable, or physical-register escape.
IR words are sixteen bits; storage is byte-addressed. File and extra
memory-block handles are opaque. Procedures, local state, arguments,
word expressions, and quoted strings suffice to write the tools.
The target remains a COM image with at most 61184 emitted bytes.
The assembler retains 8192 symbols using separately allocated pages.
RILL supports 512 global/function symbols, 24-character folded names,
16 parameters, 64 simultaneously live local words, and block/expression
nesting of at most 16. Byte buffers are global; use allocated blocks for
larger tables. This is a bounded systems language, without
ownership checking or a claim of memory safety. Consult the references.

Every archive member is ASCII source with DOS line endings and an
8.3 name. No preassembled executable or historical interpreter is here.
''')
files=['BOOTASM.BAS','ASM86.ASM','ASMA0.ASM','ASM86A.ASM','IRWIDE.ASM','RILLBOOT.IR','RILL.RIL','IR86.RIL','ASM86A.RIL','VIEW.BAS','CHECK.BAT','TMAKE.BAT','README.TXT','RILL.IR','TSMALL.RIL','TLOCAL.RIL','XLOCAL.RIL','TSCOPE.RIL']
files+=sorted(p.name for p in W.glob('E*.RIL'))+sorted(p.name for p in W.glob('E*.IR'))
for family,prefix,ext in [('ir-extensions','IW','IR'),('rill-seed-series','RB','RIL'),('rill-self-series','RC','RIL')]:
 for c in json.loads((ROOT/'qa/toolchain'/(family+'.json')).read_text()):
  files.append(c['source']);n=c['number']
  if c.get('fixture') is not None:files.append(f'T{prefix}{n:02}.'+ext)
  if c.get('bad') is not None:files.append(f'X{prefix}{n:02}.'+ext)

for name in files:shutil.copyfile(W/name,D/name)
# These directories own generated publication files. Retire compiler-seed
# checkpoints absent from the active construction, keeping other work files.
seed_files=set(json.loads((ROOT/'qa/compilers/rb-files.json').read_text()))
shared_files=set(files)|seed_files
for stale in W.iterdir():
 if stale.is_file() and re.fullmatch(r'(?:T|X)?RB\d+\.(?:IR|RIL|ASM)',stale.name) and stale.name not in shared_files:stale.unlink()
for stale in D.iterdir():
 if stale.is_file() and stale.name not in set(files)|{'TOOLCHN.ZIP'}:stale.unlink()
archive=D/'TOOLCHN.ZIP';same=False
if archive.exists():
 with zipfile.ZipFile(archive) as z:same=z.namelist()==files and all(z.read(n)==(W/n).read_bytes() for n in files)
if not same:
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for name in files:
   info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(W/name).read_bytes())
(ROOT/'qa/toolchain/package-files.json').write_text(json.dumps(files,indent=2)+'\n')
# Keep complete-source icons useful at the parent tool collection level.
for group,name in [('ir86','IR86.RIL'),('ir86','IRWIDE.ASM'),('rill','RILL.RIL'),('rill','RILLBOOT.IR')]:shutil.copyfile(W/name,ROOT/'site/downloads'/directory_name(group)/name)
print(f'Packaged {len(files)} toolchain source files')
