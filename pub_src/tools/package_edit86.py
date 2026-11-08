"""Package only the editor's ASCII sources, target binding and reader fixtures."""
from pathlib import Path
import json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/edit86';D=ROOT/'site/static/downloads/edit86';D.mkdir(parents=True,exist_ok=True)
for name in ['VIEW.BAS','CHECK.BAT']:shutil.copyfile(ROOT/'workbench/bootasm'/name,W/name)
text='''THE BOOTSTRAP PROJECT - EDIT86
Building Our Screen Editor

Begin after the completed RILL-written toolchain. Preserve its R0.COM,
I0.COM and A0.COM and their matching RILL.RIL/IR86.RIL/ASM86.RIL sources.
Use the workbench and articles for the exact edits and build reports.
No compiler, translator, assembler or editor executable is supplied.

Build RILLED.RIL with R0/I0/A0 and save RESULT.COM as RILLED.COM.
Build IRED.RIL with R0/I0/A0 and save RESULT.COM as IRED.COM.
The new compiler and translator retain the established languages and
add only editor services. IRED reads EDITRT.ASM from its work directory
and appends that authored target binding to its assembly output.
S02.ASM is empty. S03.ASM through S07.ASM are continuing binding stages.
S03.RIL through S07.RIL are small service checks, not editor versions.
P01/Q01 check the compiler; P02/Q02 check the translator. P01.IR is
compiler-produced text for exact inspection, not machine code.

Use RILLED, IRED and A0 for E08.RIL through E20.RIL. Copy S07.ASM to
EDITRT.ASM before translating them. Copy each source to SOURCE.RIL,
require the fresh compiler OK and CHECK PASS, copy RESULT.IR to
SOURCE.IR, require translator OK and PASS, copy RESULT.ASM to
SOURCE.ASM, require assembler OK and PASS, then preserve RESULT.COM
under its checkpoint name. Never trust a stale result after failure.
E20.RIL and EDIT86.RIL are identical. Preserve E20.COM as EDIT86.COM.

Early document checks use DOS status and byte comparisons, without
extra display routines. T10.TXT through T20.TXT are CR/LF fixtures;
T14 has a literal tab. The final source grows the same paired-position,
page, reader, writer and gap routines into the full screen editor.
Use VIEW.BAS for lengths and bytes; CHECK.BAT makes status visible.

EDIT86 edits fixed EDIT.TXT. Select a source with COPY, preserve a
separately named accepted original, edit/save, then copy back only
after Saved and a clean exit. Navigation changes memory only. The
whole document and its insertion gap share eight 32768-byte blocks.
Files up to 262144 bytes are accepted; a full buffer needs a deletion
before insertion. There is no imposed line length or line count.
A separate 16384-byte ring retains the newest 2048 edits, with no redo.
The main 64 KiB plus text and undo requests total 336 KiB, before DOS,
environment and memory control overhead. All requests are checked.
Use the reference 640 KiB machine and an 80-column mode 3 or 7 screen.

Arrows/Home/End/Page Up/Page Down navigate. F6/F7 select document
start/end. Enter inserts CR/LF, Tab inserts a literal tab. Delete and
Backspace keep CR/LF paired. F2 (Control-S) saves, F3 finds literal
case-sensitive text up to 64 printable characters, F5 finds next,
F4 (Control-Z) undoes, F10 (Control-Q) quits. Unsaved quit asks S to
save, Q to discard or Escape to cancel. Search does not wrap.
Control/high bytes display as dots but round-trip unchanged. Long
lines scroll horizontally and may be slow; they are not truncated.

EDIT.TMP and EDIT.BAK are reserved recovery names. Existing copies
block entry/saving. Save writes and closes the temporary, backs up
the old document, publishes the temporary, then removes the backup.
A failed publication attempts restoration. Failed restoration or
backup deletion retains recovery material. Inspect and copy it to
safe names before retrying. This is not a power-loss guarantee.
A clean quit after deliberate discard does not imply a prior save.

All members are source-only ASCII with DOS CR/LF and 8.3 filenames.
Keep the earlier source collections to reproduce every builder.
'''
(W/'README.TXT').write_bytes(text.replace('\n','\r\n').encode('ascii'))
files=['EDIT86.RIL','RILLED.RIL','IRED.RIL','EDITRT.ASM','VIEW.BAS','CHECK.BAT','README.TXT','P01.RIL','P01.IR','Q01.RIL','P02.RIL','Q02.IR','S02.ASM']
for c in json.loads((ROOT/'qa/edit86/checkpoints.json').read_text()):
 n=c['number']
 if n<3:continue
 files.append(c['source'])
 if n<8:files.append(c['probe'])
 elif n>=10:files.append(c['fixture'])
for name in files:shutil.copyfile(W/name,D/name)
archive=D/'EDIT86.ZIP';same=False
if archive.exists():
 with zipfile.ZipFile(archive) as z:same=z.namelist()==files and all(z.read(n)==(W/n).read_bytes() for n in files)
if not same:
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for name in files:
   info=zipfile.ZipInfo(name,(1986,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(W/name).read_bytes())
for p in D.iterdir():
 if p.name not in set(files)|{'EDIT86.ZIP'}:p.unlink()
(ROOT/'qa/edit86/package-files.json').write_text(json.dumps(files,indent=2)+'\n')
print('Packaged',len(files),'EDIT86 source files')
