"""Package ASCII/CRLF/8.3 reader sources, never executable artifacts."""
from pathlib import Path
import json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/asm86a';D=ROOT/'site/static/downloads/asm86a';D.mkdir(parents=True,exist_ok=True)
for name in ['BOOTASM.BAS','VIEW.BAS','CHECK.BAT']:shutil.copyfile(ROOT/'workbench/bootasm'/name,W/name)
shutil.copyfile(ROOT/'workbench/asm86/ASM86.ASM',W/'ASM86.ASM')
readme='''THE BOOTSTRAP PROJECT - ASM86A
A practical course in small-system software

The bootstrap ladder: BOOTASM -> ASM86 -> ASM86A -> IR86 -> RILL.
ASMA0 is the seed milestone within the ASM86A construction.
Read the workbench, then the construction articles in order.

BOOTASM.BAS  Completed BASIC foundation, unchanged.
ASM86.ASM    Preceding native assembler, unchanged.
ASMA0.ASM    Seed, identical to A12.ASM; built directly with ASM86.
ASM86A.ASM   Complete assembler, identical to A40.ASM; built by ASMA0.
A01.ASM through A40.ASM: complete construction checkpoints.
Tnn.ASM and Xnn.ASM: acceptance and rejection inputs where applicable.
VIEW.BAS and CHECK.BAT: unchanged viewer and immediate DOS checker.
HELLO.ASM, FRAME.ASM, BRIDGE.ASM, COPYTEXT.ASM: complete programs.
LONGSRC.BAS and SYMS.BAS: BASIC generators of source text only.

Use your own DOS 3.10 and period GW-BASIC interpreter. Note its banner.
Build ASM86 with BOOTASM.BAS; preserve it as ASMKEEP.COM.
CHECK ASMKEEP prompts for a source base name: A01 through A12.
The seed is 3342 bytes. Prove both self-assembly generations.
Keep the tested ASMA0.COM to build A13 through A40.

For a fixed-file build: COPY A13.ASM SOURCE.ASM; CHECK ASMA0.
Require OK and PASS, then COPY RESULT.COM A13.COM before testing.
The complete ASM86A is 6422 bytes; preserve it as ASMAKEEP.COM.
It has no filename prompt. ASMKEEP remains the original ASM86.
SOURCE.ASM is reopened for two passes and must remain unchanged.
RESULT.COM is the published output; ASMA.TMP and RESULT.BAK are
reserved recovery names. Inspect existing recovery files before use.
Require a fresh OK and PASS before using any result.

A03 through A06 are byte-copy diagnostics. Inspect their data output;
do not execute it. Most other output fixtures are also encoding data.
Only outputs explicitly called complete programs may be executed.
A12 and A40 acceptance inputs are their canonical self-build sources.

The seed streams 1024-byte blocks with 2048 symbols in one segment.
The complete tool streams 4096-byte blocks and allocates 8192 records
in eight symbol pages plus a hash block: 392 KiB including its main
segment, before DOS/environment/allocation overhead. Names may have
31 characters. Physical lines have at most 1023 characters. Output
has at most 61184 bytes in the chosen single-segment COM profile.
Its source language is a selected 8086 subset, not all Intel syntax.
Consult the reference for exact forms, limits, and recovery behavior.

All packaged files are source, ASCII, DOS line endings, and 8.3 names.
No preassembled program, DOS copy, or BASIC interpreter is included.
'''
(W/'README.TXT').write_bytes(readme.replace('\n','\r\n').encode('ascii'))
files=['BOOTASM.BAS','ASM86.ASM','ASMA0.ASM','ASM86A.ASM','VIEW.BAS','CHECK.BAT','README.TXT','LONGSRC.BAS','SYMS.BAS']
for c in json.loads((ROOT/'qa/asm86a/checkpoints.json').read_text()):
 n=c['number'];files.append(f'A{n:02}.ASM')
 if c.get('fixture') is not None:files.append(f'T{n:02}.ASM')
 if c['bad']['kind']=='source':files.append(f'X{n:02}.ASM')
files+=['HELLO.ASM','FRAME.ASM','BRIDGE.ASM','COPYTEXT.ASM']
for name in files:shutil.copyfile(W/name,D/name)
archive=D/'ASM86A.ZIP';same=False
if archive.exists():
 with zipfile.ZipFile(archive) as z:same=z.namelist()==files and all(z.read(n)==(W/n).read_bytes() for n in files)
if not same:
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for name in files:
   info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(W/name).read_bytes())
(ROOT/'qa/asm86a/package-files.json').write_text(json.dumps(files,indent=2)+'\n');print(f'Packaged {len(files)} ASM86A source files')
