"""Package the seed collection without introducing another executable producer."""
from pathlib import Path
import json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/asma0';D=ROOT/'site/static/downloads/asma0';Q=ROOT/'qa/asma0'
for p in [W,D,Q]:p.mkdir(parents=True,exist_ok=True)
for name,group in [('BOOTASM.BAS','bootasm'),('ASM86.ASM','asm86'),('VIEW.BAS','bootasm'),('CHECK.BAT','bootasm'),('ASMA0.ASM','asm86a')]:shutil.copyfile(ROOT/'workbench'/group/name,W/name)
syms=(ROOT/'workbench/asm86a/SYMS.BAS').read_text().replace('10 N=8192','10 N=2048');(W/'SYMS.BAS').write_bytes(syms.replace('\n','\r\n').encode('ascii'))
files=['BOOTASM.BAS','ASM86.ASM','ASMA0.ASM','VIEW.BAS','CHECK.BAT','SYMS.BAS','README.TXT']
for c in json.loads((ROOT/'qa/asm86a/checkpoints.json').read_text()):
 n=c['number']
 if n>12:continue
 names=[f'A{n:02}.ASM']
 if c.get('fixture') is not None:names.append(f'T{n:02}.ASM')
 if c['bad']['kind']=='source':names.append(f'X{n:02}.ASM')
 for name in names:shutil.copyfile(ROOT/'workbench/asm86a'/name,W/name)
 files+=names
for name in ['HELLO','MEMORY','COUNT']:shutil.copyfile(ROOT/'workbench/asm86'/(name+'.ASM'),W/(name+'.ASM'));files.append(name+'.ASM')
readme='''THE BOOTSTRAP PROJECT - ASMA0
A practical course in small-system software

The ladder: BOOTASM -> ASM86 -> ASMA0 -> ASM86A -> IR86 -> RILL.
ASMA0 is the streaming seed collection, built directly by ASM86.
Read its workbench, construction articles, reference, and programs.

BOOTASM.BAS and ASM86.ASM: unchanged preceding bootstrap sources.
A01.ASM through A12.ASM: complete seed construction checkpoints.
ASMA0.ASM: complete seed, identical to A12.ASM.
Tnn.ASM and Xnn.ASM: exact acceptance/rejection inputs where applicable.
VIEW.BAS and CHECK.BAT: unchanged inspection and DOS status helpers.
SYMS.BAS: source-text generator for the 2048-definition exercise.
HELLO.ASM, MEMORY.ASM, COUNT.ASM: complete executable examples.

Use your own DOS 3.10 and period GW-BASIC interpreter; note its banner.
Build ASM86 from BOOTASM.BAS. Preserve it as ASMKEEP.COM.
CHECK ASMKEEP prompts for A01 through A12 without an extension.
Require OK and PASS at every build. Preserve each source/executable.
A03 through A06 copy data; inspect that output, never execute it.
Only fixtures expressly identified as complete programs may be run.

ASMA0.COM is 3342 bytes. Compare both self-assembly generations with
its ASM86-built original. The seed uses fixed SOURCE.ASM/RESULT.COM,
1024-byte input/output blocks, 2048 symbols, sixteen-character names,
120-character physical lines, and at most 65535 lines per pass.
It runs in one full 64 KB segment and allocates no extra symbol pages.
Output is streamed, with at most 61184 bytes in the chosen COM profile.
Inspect ASMA.TMP and RESULT.BAK recovery files before another full run.
Source rejection preserves the accepted RESULT.COM. Require fresh OK.

The separate ASM86A collection begins by copying this verified
ASMA0.ASM to A13.ASM. Keep the tested ASMA0.COM as its builder.
All members are ASCII/CRLF/8.3 source. No executable or interpreter
is supplied in this source collection.
'''
(W/'README.TXT').write_bytes(readme.replace('\n','\r\n').encode())
for name in files:shutil.copyfile(W/name,D/name)
archive=D/'ASMA0.ZIP';same=False
if archive.exists():
 with zipfile.ZipFile(archive) as z:same=z.namelist()==files and all(z.read(n)==(W/n).read_bytes() for n in files)
if not same:
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for name in files:
   info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(W/name).read_bytes())
(Q/'package-files.json').write_text(json.dumps(files,indent=2)+'\n');print(f'Packaged {len(files)} ASMA0 source files')
