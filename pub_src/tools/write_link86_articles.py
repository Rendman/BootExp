"""Publish measured LINK86 checkpoints as one gradual construction."""
from pathlib import Path
from difflib import SequenceMatcher
import json
from publication_names import write_page
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/link86';Q=ROOT/'qa/link86';C=ROOT/'site/content/bootstrap/link86'
CASES=json.loads((Q/'checkpoints.json').read_text())
def fence(kind,s):return '```'+kind+'\n'+s.replace('\r\n','\n').rstrip('\n')+'\n```\n\n'
def front(title,weight,why,download,cover=False):
 meta=dict(title=title,weight=weight,description=why,download=download,download_group='tools/link86',reader_names=1)
 if cover:meta.update(cover=True,tool_id='LINK86',collection_key='link86')
 return '+++\n'+''.join(k+' = '+json.dumps(v)+'\n' for k,v in meta.items())+'+++\n\n'
t=front('Linking Our First Modules',10,'A RILL-written linker for two small text object modules.','LINK86.RIL',True)
t+='The RILL-written toolchain can now build another tool. LINK86 places two object modules in one DOS .COM image, resolves their public names and emits relative calls and absolute addresses. Its source is compiled with the completed RILL compiler, IR86 translator and ASM86 assembler.\n\n'
t+='Ten working stopping points build the reader, record decoder, streamed writer, publication checks, module layout, public table and relocations. The last two fixtures are complete programs: one calls a function in the other module, and one displays text exported by the other module. The object files are entered as plain ASCII; this collection does not change ASM86 or require another assembler.\n\n'
t+='Read the workbench first and keep every accepted checkpoint separately named. The [disk source collection](../../downloads/tools/link86/LINK86.ZIP) contains the RILL sources, exact text-object fixtures, viewer and checker. It supplies no prebuilt executable. The [object reference](11-reference/index.html) gives the complete small format and its limits.\n'
write_page(C/'_index.md',t)
t=front('The linker workbench',0,'Keep the RILL-built trio and preserve each linker before testing its output.','LINK86.ZIP')
t+='Begin after Rebuilding Our Tools in RILL and its matching generations. Preserve the RILL compiler as R0.COM, its translator as I0.COM and its assembler as A0.COM. Use the same DOS 3.10 hard-disk work directory, plain ASCII editor, VIEW.BAS and CHECK.BAT. Keep the preceding source collections so each builder can be recovered.\n\n'
t+='## Build a stopping point\n\nEvery Lnn.RIL is compiled through the same three tools:\n\n'+fence('dos','COPY L01.RIL SOURCE.RIL\nCHECK R0\nCOPY RESULT.IR SOURCE.IR\nCHECK I0\nCOPY RESULT.ASM SOURCE.ASM\nCHECK A0\nCOPY RESULT.COM L01.COM')
t+='Require the stated fresh OK and PASS before every following copy. RESULT.COM is also the linker output name, so preserve L01.COM before testing it. Use the same pattern for each later source. The complete source is L10.RIL, also saved as LINK86.RIL.\n\n'
t+='## Fixed object and output files\n\n| File | Use |\n|---|---|\n| MAIN.OBJ | First module; its first emitted byte loads at 0100H |\n| UTIL.OBJ | Second module, placed immediately after the first |\n| RESULT.COM | Accepted linked image |\n| LINK.TMP | Owned streamed output before publication |\n| LINK.BAK | Previous accepted image during publication |\n\nThe .OBJ extension here names our own ASCII format, not a commercial assembler object format. Mnn.OBJ and Unn.OBJ are the exact input fixtures copied to the fixed work names. Xnn.OBJ is the rejection input for MAIN.OBJ. Keep both inputs unchanged throughout a run.\n\n'
t+='Early reader checkpoints use only MAIN.OBJ and report success through CHECK.BAT. L04 recognizes the OBJ1/END envelope. L05 deliberately leaves LINK.TMP for byte inspection; delete that exercise file before another run. L06 publishes RESULT.COM. L07 and later read both modules in two passes. Unknown record types are rejected at every stopping point.\n\n'
t+='## Inspect and preserve results\n\nVIEW.BAS reports file lengths and hexadecimal bytes. Encoding fixtures are data for inspection; execute only the complete L09 and L10 linked programs. A zero-byte result is valid for inspection and is never a runnable program.\n\n'+fence('dos','ECHO N>NO.TXT')
t+='NO.TXT answers N when COMP asks whether to compare more files. Each rejection check preserves the accepted RESULT.COM as HOLD.COM and compares it afterward. CHECK must report FAIL for that input. An older output is never evidence of a new successful link. Inspect pre-existing LINK.TMP or LINK.BAK before running a publishing checkpoint; failed publication can retain recovery files.\n'
write_page(C/'00-workbench.md',t)
patches=[];old=[]
for c in CASES:
 n=c['number'];name=f'L{n:02}';page=f'{n:02}-'+['opening-an-object','refilling-input','reading-records','recognizing-records','writing-bytes','publishing-the-image','placing-two-modules','recording-public-names','relative-references','absolute-addresses'][n-1]+'.md'
 new=(W/c['source']).read_text().splitlines();t=front(f'{n:02} · '+c['title'],n,c['why'],c['source'])+c['why']+'\n\n'
 if n==2:t+='This reader test counts the eleven disk bytes in the supplied OBJ1/END fixture, including CR/LF. A mismatch returns nonzero; no display helper is added.\n\n'
 if n==3:t+='This stopping test requires exactly two physical records in its fixture. Error reports now use the owned input number, current physical record and reason code. The source buffer stores only the current record.\n\n'
 if n==8:t+='Allocate 10240 bytes for 256 forty-byte records. Bytes 0–31 hold a terminated folded name; words at 32, 34 and 36 hold its relative value, input number and pass-two seen flag. Initialize all forty bytes before inserting an entry. An offset equal to module length may name its end; a larger offset is rejected.\n\n'
 if n==9:t+='R occupies two image bytes at the current output position. Its word is target loaded address minus the loaded address just after that word, modulo 65536. MAIN has seven bytes, so VALUE in UTIL loads at 0107H. The call operand begins at 0101H and ends at 0103H: 0107H minus 0103H is 0004H.\n\n'
 if n==10:t+='A occupies two bytes and contains the target loaded address itself. MAIN has twelve bytes, placing TEXT at 010CH. The MOV DX immediate must therefore be 0C 01. The runtime of this linked example comes from its authored DOS instructions, not from the linker.\n\n'
 t+='## Enter the source\n\n';changes=[]
 if not old:t+='Create L01.RIL as plain text:\n\n'+fence('rill','\n'.join(new));changes=[dict(a1=0,a2=0,old=[],new=new,context=[],after=[])]
 else:
  t+=f'Copy L{n-1:02}.RIL to {name}.RIL. Apply these edits from the bottom of the unchanged old file upward. Physical positions are locators, not source to type. Keep all other source.\n\n'
  for i,(_,a,b,d,e) in enumerate(reversed([op for op in SequenceMatcher(None,old,new,autojunk=False).get_opcodes() if op[0]!='equal']),1):
   context=old[max(0,a-3):a];after=old[b:b+2]
   t+=f'### Edit {i}\n\n'
   if context:t+='Unchanged source immediately before the edit:\n\n'+fence('rill','\n'.join(context))
   if old[a:b]:t+=f'Remove old physical positions {a+1}–{b}:\n\n'+fence('rill','\n'.join(old[a:b]))
   else:t+=f'Insert after old physical line {a}.\n\n'
   if new[d:e]:t+=('Replace with:\n\n' if old[a:b] else 'Insert:\n\n')+fence('rill','\n'.join(new[d:e]))
   else:t+='There is no replacement source.\n\n'
   if after:t+='The following old source remains:\n\n'+fence('rill','\n'.join(after))
   changes.append(dict(a1=a,a2=b,old=old[a:b],new=new[d:e],context=context,after=after))
 t+='## Build and preserve the tool\n\n'+fence('dos',f'COPY {name}.RIL SOURCE.RIL\nCHECK R0\nCOPY RESULT.IR SOURCE.IR\nCHECK I0\nCOPY RESULT.ASM SOURCE.ASM\nCHECK A0\nCOPY RESULT.COM {name}.COM')
 t+=f'Require compiler `OK RESULT.IR {c["ir_bytes"]:010}`, translator `OK RESULT.ASM {c["assembly_bytes"]:010} text bytes`, assembler `OK RESULT.COM {c["binary_bytes"]:05} bytes`, and each PASS before the following copy. VIEW.BAS must show {name}.COM length {c["binary_bytes"]} and these first thirty-two bytes:\n\n'+fence('text',c['binary_hex'])
 t+='## Check the accepted input\n\nCreate '+f'M{n:02}.OBJ as plain ASCII:\n\n'+fence('text',c['main'])
 if c['util'] is not None:t+=f'Create U{n:02}.OBJ:\n\n'+fence('text',c['util'])
 commands=f'COPY M{n:02}.OBJ MAIN.OBJ\n'
 if c['util'] is not None:commands+=f'COPY U{n:02}.OBJ UTIL.OBJ\n'
 t+=fence('dos',commands+f'CHECK {name}')
 if c['console']:t+='Require:\n\n'+fence('text',c['console']+'PASS\n')
 else:t+='CHECK must report PASS. This checkpoint creates no linked output. Its input handling is checked by its return status; its retained executable was inspected above.\n\n'
 if c['expected'] is not None:
  raw=bytes.fromhex(c['expected']);t+=f'VIEW.BAS must show {c["output_file"]} length {len(raw)} and these complete bytes:\n\n'+fence('text',c['expected'])
  if c['program_output'] is not None:
   t+=fence('dos',f'COPY RESULT.COM TRY.COM\nCHECK TRY')+('TRY displays HI followed by CR/LF and reports PASS.\n\n' if c['program_output'] else 'TRY calls VALUE in the second module, exits with its zero result and reports PASS. It has no display routine.\n\n')
  else:t+='Inspect this data/encoding fixture; do not execute it.\n\n'
 if n==5:t+='Delete this deliberately created LINK.TMP after inspection. RESULT.COM still contains the preceding accepted file.\n\n'+fence('dos','DEL LINK.TMP')
 t+='## A rejection check\n\n'+fence('dos','COPY RESULT.COM HOLD.COM')
 if c['bad'] is not None:
  t+=f'Create X{n:02}.OBJ:\n\n'+fence('text',c['bad'])+fence('dos',f'COPY X{n:02}.OBJ MAIN.OBJ\nCHECK {name}')
 else:t+=fence('dos',f'REN MAIN.OBJ HOLD.OBJ\nCHECK {name}')+'Use an unused HOLD.OBJ name and restore it to MAIN.OBJ after the check.\n\n'
 t+='Require:\n\n'+fence('text',c['error']+'FAIL\n')+fence('dos','COMP HOLD.COM RESULT.COM <NO.TXT')+'COMP must report no differences. An unexpected PASS fails the rejection. Require a fresh successful run before preserving any new output.\n'
 if n==10:t+='\nPreserve L10.COM as LINK86.COM and L10.RIL as LINK86.RIL. The reference describes the complete accepted format.\n'
 write_page(C/page,t);patches.append(dict(number=n,page=page,base=None if n==1 else f'L{n-1:02}.RIL',source=c['source'],changes=changes));old=new
reference='''LINK86 reads MAIN.OBJ and UTIL.OBJ in that order and writes one DOS .COM image. The format is our own ASCII object text. It contains authored bytes and relocation records; it is not compatible with commercial OBJ files.

## Records

| Record | Meaning |
|---|---|
| OBJ1 | Required first nonblank, noncomment record |
| B hh ... | Emit one through sixteen hexadecimal byte pairs |
| P name hhhh | Export a module-relative offset, exactly four hexadecimal digits |
| R name | Emit target minus the address after this two-byte operand, modulo 65536 |
| A name | Emit the target's absolute loaded word address |
| END | Required final record; only blank lines/comments may follow |

Fields are separated by spaces or tabs. A semicolon ends the meaningful part of a physical record. Names and record spellings are folded to uppercase; hexadecimal digits accept either case. Each B item has exactly two digits. Numeric fields have no H suffix, signs or expressions. P's offset is independent of the record's position and may be written before its bytes. R and A each occupy two bytes at their own record position; there is no separate patch-offset field or addend.

Names begin with a letter or underscore and continue with letters, digits or underscores, at most 31 characters. Public names are unique across both modules. References may precede definitions and may name a public in the same module. An unexported location is not a linker symbol. The format has no private-name records, implicit imports, alignment, sections, short/far relocations, library search or entry-selection directive.

## Layout and passes

MAIN begins at loaded offset 0100H. UTIL begins immediately after MAIN's emitted bytes. Public offsets are relative to their owning module, never loaded addresses. They must be between zero and that module's length, inclusive; an end label is a position, not an extra allocated byte. Programs remain responsible for live storage and valid executable entry bytes.

Pass one validates records, counts the layout and stores public definitions. Pass two reopens both inputs, verifies public values, owners and occurrences, verifies module lengths, and resolves references into streamed output. Keep the inputs unchanged. Same-sized edits to byte records or references are not all detected; this is not a general file identity check.

Words are emitted low byte first. A near relative word is ordinary sixteen-bit displacement arithmetic in this one code segment. There is no check that a symbol denotes executable instructions rather than data. The two complete acceptance programs supply their own DOS exit/output instructions; LINK86 adds no runtime or executable header.

## Limits

| Resource | Bound |
|---|---|
| Input modules | Two fixed files: MAIN.OBJ, then UTIL.OBJ |
| Emitted image | 61184 bytes, loaded at 0100H through EFFFH |
| Public definitions | 256, stored in a checked 10240-byte allocated block |
| Name spelling | 31 characters, compared in full |
| Physical record | 120 characters, including comments and whitespace |
| Physical records | At most 65535 per input per pass |
| B record | One through sixteen byte pairs |
| File buffers | 1024 bytes each; no complete object or image buffer |

The upper 4 KiB remains the generated program's stack reservation. A zero-byte output is valid for inspection only. Allocated symbol storage does not enlarge the target code segment. The linker itself is built by the established RILL toolchain, whose normal DOS entry and stack guard apply.

Object text accepts CR/LF, bare CR or LF and a final unterminated record. Control-Z ends input text. Other control bytes except tab and high bytes are rejected. B records can materialize every byte value, including zero, FF and 1A.

## Files, reports and failures

Existing LINK.TMP or LINK.BAK blocks a publishing run. Create the temporary file only after a successful layout pass. Flush and close it, release allocated symbol storage, then rename the previous RESULT.COM to LINK.BAK, rename LINK.TMP to RESULT.COM, and delete the backup. A failed second rename attempts restoration. Failed restoration or backup deletion can leave recovery files; inspect them before another run. DOS rename is not atomic replacement. Source rejection preserves the accepted result and removes only this run's owned temporary output.

A completed link prints `OK RESULT.COM nnnnn bytes` and returns zero. Failures print `LINK ERROR uuuuu lllll CODE ccccc` and return one. Input numbers one and two identify MAIN and UTIL; zero identifies global setup/publication. The line is the current physical record, or zero before reading. At a record-count overflow, the counter retains 65535. L01/L02 use return status only; L05 deliberately reports and leaves LINK.TMP for inspection.

| Code | Meaning |
|---|---|
| 1 | Malformed header/record, source byte or missing END |
| 2 | Invalid byte/word hexadecimal spelling |
| 3 | Invalid, duplicate or undefined public name |
| 4 | Public offset outside its module |
| 5 | Record, name, symbol, byte-record or image capacity |
| 6 | File, allocation, transfer or publication failure |
| 7 | Definitions or module layout differ between passes |
| 8 | Reserved temporary/backup name already exists |

Require the fresh success report and PASS before copying or executing output. A failure report never authorizes use of an older RESULT.COM.
'''
write_page(C/'11-reference.md',front('The object and linker reference',11,'The complete text format, layout arithmetic, limits and publication contract.','LINK86.RIL')+reference)
(Q/'article-patches.json').write_text(json.dumps(patches,indent=2)+'\n')
print('Published LINK86 workbench, ten construction lessons and object reference')
