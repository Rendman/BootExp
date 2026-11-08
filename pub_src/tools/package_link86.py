"""Source-only LINK86 checkpoints and hand-entered object fixtures."""
from pathlib import Path
import json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/link86';D=ROOT/'site/static/downloads/link86';D.mkdir(parents=True,exist_ok=True)
for name in ['VIEW.BAS','CHECK.BAT']:shutil.copyfile(ROOT/'workbench/bootasm'/name,W/name)
text='''THE BOOTSTRAP PROJECT - LINK86
Linking Our First Modules

Begin after the RILL-written toolchain and its matching rebuilds.
Preserve R0.COM, I0.COM, A0.COM and their exact source collections.
No compiler, translator, assembler or prebuilt executable is supplied here.
Compile L01.RIL through L10.RIL with R0, translate with I0, assemble
with A0, requiring fresh OK and PASS before every following copy.
LINK86.RIL is identical to L10.RIL.

The first checkpoints open and read MAIN.OBJ; their status is the check.
L04 accepts the OBJ1/END envelope. L05 writes LINK.TMP for inspection;
delete that deliberate exercise output before continuing. L06 publishes
RESULT.COM. L07 places MAIN.OBJ then UTIL.OBJ in two passes. L08 adds
public names, L09 relative words, and L10 absolute addresses.
Mnn.OBJ and Unn.OBJ are the exact accepted MAIN/UTIL input fixtures.
Xnn.OBJ are rejection inputs copied over MAIN.OBJ. Inputs are plain
ASCII object text, not preassembled binary files or a standard OBJ format.
Only the L09/L10 linked acceptance images are designated runnable tests.
All other output bytes are inspected with VIEW.BAS.

The complete linker reads MAIN.OBJ and UTIL.OBJ and writes RESULT.COM.
OBJ1 starts each object; END ends its records. B contains 1-16 two-digit
hexadecimal bytes. P name hhhh defines a module-relative hex word
position. R name emits a near-relative word; A name emits an absolute
loaded address. Blank lines and semicolon comments are accepted.
Names are folded ASCII, at most 31 characters. Object records contain
at most 120 characters. There are 256 public names, at most 65535
physical records per input, 1024-byte I/O blocks, and 61184 output bytes.
No addends, library search, short/far fixups, EXE files or assembler
object-output mode are included. The two input files stay unchanged
throughout both passes; same-sized byte edits are not all detectable.

Existing LINK.TMP/LINK.BAK prevents a publishing run. Source rejection
preserves an accepted RESULT.COM; publication failure can retain recovery
files. Inspect them before another run. Status zero and the fresh OK
report are required before preserving or executing any linked image.
L01/L02 report failure through exit status only. Later errors print the
input number, physical record and reason code described in the reference.

All archive members are ASCII/CRLF/8.3 sources. Keep the preceding
source archives so the builders remain reproducible.
'''
(W/'README.TXT').write_bytes(text.replace('\n','\r\n').encode('ascii'))
files=['LINK86.RIL','VIEW.BAS','CHECK.BAT','README.TXT']
for c in json.loads((ROOT/'qa/link86/checkpoints.json').read_text()):
 n=c['number'];files += [c['source'],f'M{n:02}.OBJ']
 if c['util'] is not None:files.append(f'U{n:02}.OBJ')
 if c['bad'] is not None:files.append(f'X{n:02}.OBJ')
for name in files:shutil.copyfile(W/name,D/name)
archive=D/'LINK86.ZIP'
same=False
if archive.exists():
 with zipfile.ZipFile(archive) as z:same=z.namelist()==files and all(z.read(n)==(W/n).read_bytes() for n in files)
if not same:
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for name in files:
   info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(W/name).read_bytes())
(ROOT/'qa/link86/package-files.json').write_text(json.dumps(files,indent=2)+'\n')
print('Packaged',len(files),'LINK86 source files')
