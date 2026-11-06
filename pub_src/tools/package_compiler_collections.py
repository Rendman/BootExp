"""Package the IR-written and RILL-written compiler constructions separately."""
from pathlib import Path
import json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'workbench/toolchain';Q=ROOT/'qa/compiler_collections';Q.mkdir(parents=True,exist_ok=True)
for collection,family,last,canonical in [('rb','rill-seed-series',47,'RILLBOOT.IR'),('rc','rill-self-series',43,'RILL.RIL')]:
 W=ROOT/'workbench'/collection;D=ROOT/'site/static/downloads'/collection
 for p in [W,D]:p.mkdir(parents=True,exist_ok=True)
 files=['ASM86A.ASM','IRWIDE.ASM','RILLBOOT.IR','VIEW.BAS','CHECK.BAT','README.TXT']
 if collection=='rc':files+=['RILL.RIL','IR86.RIL','ASM86A.RIL','TMAKE.BAT']
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

The compiler construction: first RILL -> RB compiler seed -> RC.
The preceding native ladder is BOOTASM -> ASM86 -> ASMA0 -> ASM86A
-> streaming IR86. Use the same DOS 3.10 and period BASIC workbench.
All files here are ASCII/CRLF/8.3 source. No executable is supplied.

ASM86A.ASM and IRWIDE.ASM: unchanged native prerequisite sources.
Preserve their tested executables as ASMAKEEP.COM and IWKEEP.COM.
VIEW.BAS and CHECK.BAT: unchanged inspection and status helpers.
{prefix}01 through {prefix}{last:02}: complete construction checkpoint sources.
T-prefixed and X-prefixed RIL files: exact acceptance/rejection inputs.
{canonical}: complete compiler source, identical to the final checkpoint.
Early checkpoints are executable helper diagnostics. An emitted text
fragment is inspected as text; it is not a complete compiler result.
Require each fresh OK and PASS before copying the next result.

'''
 if collection=='rb':
  text+='''RB sources are IR, built with IWKEEP and ASMAKEEP. At the final
checkpoint preserve RB47.COM as RILLBOOT.COM and RB47.IR as RILLBOOT.IR.
The eight E-prefixed RIL programs use that completed compiler seed.
RILLBOOT reads SOURCE.RIL and streams RESULT.IR via RILL.TMP/RILL.BAK.
Copy accepted RESULT.IR to SOURCE.IR for IWKEEP; copy its accepted
RESULT.ASM to SOURCE.ASM for ASMAKEEP. Preserve every accepted output.
The separate RC collection expresses this same compiler in RILL.
'''
 else:
  text+='''Begin with the completed RB collection and its RILLBOOT.COM.
RILLBOOT.IR is its unchanged source, built with IWKEEP and ASMAKEEP.
Compile RC sources with RILLBOOT, then IWKEEP and ASMAKEEP.
Preserve RC43.COM as R0.COM and RC43.RIL as RILL.RIL. R0 compiles
that same source to R1, then R1 to R2; both must match R0 exactly.
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
The shared systems language has 24-character folded names, 512 global
or procedure symbols, sixteen parameters and live local words, lexical
scopes, recursive calls, byte buffers, strings and opaque file/block
services. Consult the exact language reference for all bounds.
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
