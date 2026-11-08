"""Package the RILL-written compiler; package_ladder supplies RILL0/RILLBOOT."""
from project_paths import directory_name
from pathlib import Path
import json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'workbench/toolchain';Q=ROOT/'qa/compilers';Q.mkdir(parents=True,exist_ok=True)
for collection,family,last,canonical in [('rc','rill-self-series',43,'RILL.RIL')]:
 W=ROOT/'workbench'/directory_name(collection);D=ROOT/'site/downloads'/directory_name(collection)
 for p in [W,D]:p.mkdir(parents=True,exist_ok=True)
 files=['ASM86A.ASM','IRWIDE.ASM','RILLBOOT.IR','VIEW.BAS','CHECK.BAT','README.TXT']
 if collection=='rc':files+=['RILL.RIL','IR86.RIL','ASM86A.RIL','TMAKE.BAT','TLOCAL.RIL','XLOCAL.RIL','TSCOPE.RIL']
 prefix=collection.upper()
 for c in json.loads((ROOT/'qa/toolchain'/(family+'.json')).read_text()):
  files.append(c['source']);n=c['number']
  if c.get('fixture') is not None:files.append(f'T{prefix}{n:02}.RIL')
  if c.get('bad') is not None:files.append(f'X{prefix}{n:02}.RIL')
 examples=json.loads((ROOT/'qa/toolchain/examples.json').read_text())
 if collection=='rc':examples=[c for c in examples if c['name'] in ['ERECUR','EHEAP','ECOPY']]
 files += [c['name']+'.RIL' for c in examples]
 text=f'''THE BOOTSTRAP PROJECT - {prefix}
A practical course in small-system software

The compiler construction: RILL0 -> RB compiler seed -> RC.
The preceding native ladder is BOOTASM -> ASM86 -> ASMA0 -> ASM86A
-> streaming IR86. Use the same DOS 3.10 and period BASIC workbench.
All files here are ASCII/CRLF/8.3 source. No executable is supplied.

ASM86A.ASM and IRWIDE.ASM: unchanged native prerequisite sources.
Preserve their tested executables as ASMAKEEP.COM and IWKEEP.COM.
VIEW.BAS and CHECK.BAT: unchanged inspection and status helpers.
{prefix}01 through {prefix}{last:02}: complete construction checkpoint sources.
T-prefixed and X-prefixed RIL files: exact acceptance/rejection inputs.
{canonical}: complete compiler source, identical to RC43.RIL.
Early checkpoints are executable helper diagnostics. An emitted text
fragment is inspected as text; it is not a complete compiler result.
Require each fresh OK and PASS before copying the next result.

'''
 text+='''Begin with the completed RB collection and its RILLBOOT.COM.
RILLBOOT.IR is its unchanged source, built with IWKEEP and ASMAKEEP.
Compile RC sources with RILLBOOT, then IWKEEP and ASMAKEEP.
RC43 already supports 64 locals. Preserve its seed-built executable
as RBOOT.COM and its source as RILL.RIL. RBOOT compiles that same
source to establish R0 using the RILL compiler's own 64-slot frames.
R0 compiles that same source to R1, then R1 to R2; both match R0 exactly.
TLOCAL.RIL, XLOCAL.RIL and TSCOPE.RIL check local/frame bounds and reuse.
ERECUR.RIL, EHEAP.RIL and ECOPY.RIL are complete compiler examples.
IR86.RIL and ASM86A.RIL are the translator and assembler in RILL.
TMAKE.BAT builds all three tools and both closed-loop generations.
The complete TOOLCHN.ZIP also contains earlier continuation sources.
'''
 text+='''
Use fixed SOURCE.RIL/RESULT.IR, SOURCE.IR/RESULT.ASM and
SOURCE.ASM/RESULT.COM files in a hard-disk directory. Keep each builder
separately named. Inspect existing temporary/backup files before a run.
Source rejection preserves accepted output; failed publication can
leave recovery files. Require a new successful status before using it.
The complete RILL language has 24-character folded names, 512 global
or procedure symbols, sixteen parameters and sixty-four live local words, lexical
scopes, recursive calls, byte buffers, strings and opaque file/block
services. RILLBOOT accepts the subset used to implement that compiler.
Consult each compiler's own reference for accepted syntax and bounds.
'''
 (W/'README.TXT').write_bytes(text.replace('\n','\r\n').encode('ascii'))
 for name in files:
  if name!='README.TXT':shutil.copyfile(SOURCE/name,W/name)
  shutil.copyfile(W/name,D/name)
 archive=D/(prefix+'.ZIP');same=False
 if archive.exists():
  with zipfile.ZipFile(archive) as z:same=z.namelist()==files and all(z.read(n)==(W/n).read_bytes() for n in files)
 if not same:
  with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
   for name in files:
    info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(W/name).read_bytes())
 (Q/(collection+'-files.json')).write_text(json.dumps(files,indent=2)+'\n');print(f'Packaged {len(files)} {prefix} source files')
