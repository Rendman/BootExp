"""Publish the editor's measured source additions and its DOS workbench."""
from pathlib import Path
from difflib import SequenceMatcher
import json,re
from publication_names import write_page
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/edit86';Q=ROOT/'qa/edit86';C=ROOT/'site/content/bootstrap/edit86'
C.mkdir(exist_ok=True);cases=json.loads((Q/'checkpoints.json').read_text());patches=[]
def fence(kind,s):return '```'+kind+'\n'+s.replace('\r\n','\n').rstrip('\n')+'\n```\n\n'
def front(title,weight,why,download,cover=False):
 meta=dict(title=title,weight=weight,description=why,download=download,download_group='tools/edit86',reader_names=1)
 if cover:meta.update(cover=True,tool_id='EDIT86',collection_key='edit86')
 return '+++\n'+''.join(k+' = '+json.dumps(v)+'\n' for k,v in meta.items())+'+++\n\n'
def patch(base,new,kind,source):
 old=base.splitlines();lines=new.splitlines();changes=[];text=''
 if not old:
  text+='Create '+source+' as plain ASCII:\n\n'+fence(kind,new)
  changes=[dict(a1=0,a2=0,old=[],new=lines,context=[],after=[])]
 else:
  text+='Keep the unchanged source. Apply these edits from the bottom of the old file upward; physical positions locate text and are not source to type.\n\n'
  for index,(_,a,b,d,e) in enumerate(reversed([x for x in SequenceMatcher(None,old,lines,autojunk=False).get_opcodes() if x[0]!='equal']),1):
   context=old[max(0,a-2):a];after=old[b:b+2];text+=f'### Edit {index}\n\n'
   if context:text+='Unchanged source immediately before the edit:\n\n'+fence(kind,'\n'.join(context))
   if old[a:b]:text+=f'Remove old physical positions {a+1}–{b}:\n\n'+fence(kind,'\n'.join(old[a:b]))
   else:text+=f'Insert after old physical line {a}.\n\n'
   if lines[d:e]:text+=('Replace with:\n\n' if old[a:b] else 'Insert:\n\n')+fence(kind,'\n'.join(lines[d:e]))
   else:text+='There is no replacement source.\n\n'
   if after:text+='The following old source remains:\n\n'+fence(kind,'\n'.join(after))
   changes.append(dict(a1=a,a2=b,old=old[a:b],new=lines[d:e],context=context,after=after))
 return text,changes

def buildcommands(source,name,c='RILLED',i='IRED'):
 return fence('dos',f'COPY {source} SOURCE.RIL\nCHECK {c}\nCOPY RESULT.IR SOURCE.IR\nCHECK {i}\nCOPY RESULT.ASM SOURCE.ASM\nCHECK A0\nCOPY RESULT.COM {name}.COM')
def measured(case,name):
 return f'Require compiler `OK RESULT.IR {case["ir_bytes"]:010}`, translator `OK RESULT.ASM {case["assembly_bytes"]:010} text bytes`, assembler `OK RESULT.COM {case["binary_bytes"]:05} bytes`, and each PASS before the following copy. VIEW.BAS must report {name}.COM length {case["binary_bytes"]} bytes, beginning with:\n\n'+fence('text',case['binary_hex'])

t=front('Building Our Screen Editor',11,'A RILL-written screen editor with a paged document, recoverable saves and bounded undo.','EDIT86.RIL',True)
t+='We can build our tools with RILL. EDIT86 gives that workbench a screen editor of its own: a window on a plain source file, an insertion position, navigation, search and a way to reverse a mistaken edit. It follows the RILL-written toolchain and LINK86 on the bootstrap ladder.\n\n'
t+='The executable remains a DOS .COM program. Its text lives in eight separately allocated pages rather than in the code segment. The complete 256 KiB buffer holds both the file and its free insertion gap. Moving around changes memory; disk writes happen only when Save is requested. A bounded undo ring uses one more block.\n\n'
t+='The construction begins with preserved copies of the compiler and translator. We add counted screen writes, key events and checked bulk transfers, then grow one editor source through file loading, safe saving, a movable gap, line boundaries, a window, navigation and editing. Native screen and segment details remain in the target binding.\n\n'
t+='Begin with the workbench. The [source collection](../../downloads/tools/edit86/EDIT86.ZIP) contains every stopping point, the service extensions, plain text fixtures and the established inspection helpers. No executable is supplied. The complete source is EDIT86.RIL; the reference gives its memory budget and working limits.\n'
write_page(C/'_index.md',t)
t=front('The editor workbench',0,'Preserve the established trio and give the editor its own work directory.','EDIT86.ZIP')
t+='Begin after Rebuilding Our Tools in RILL and its matching generations. Keep the compiler R0.COM, translator I0.COM and assembler A0.COM unchanged. Make an editor work directory on the hard disk, with these builders, CHECK.BAT, VIEW.BAS and a plain ASCII editor. Use the DOS 3.10 workbench and an 80-column text display.\n\n'
t+='## The service builders\n\nCopy the exact RILL.RIL and IR86.RIL from the toolchain collection. The first two articles extend those sources as RILLED.RIL and IRED.RIL. Build each with R0, I0 and A0, preserving the new executables as RILLED.COM and IRED.COM. They accept the established language plus the editor operations. The earlier builders remain available.\n\n'
t+='IRED appends an explicitly authored EDITRT.ASM target binding after the established runtime. Keep that file beside SOURCE.IR. S02.ASM is empty; S03.ASM through S07.ASM are complete saved stages of the binding. Copy the stated stage to EDITRT.ASM before translating its probe. The complete editor uses S07.ASM, also supplied as EDITRT.ASM. This is source read by our translator and assembler, not a prebuilt machine-code library.\n\n'
t+='## One build pattern\n\n'+buildcommands('E08.RIL','E08')
t+='Require every fresh OK report and PASS before the following COPY. Preserve each accepted executable under its checkpoint name. RILLED emits SOURCE.IR input for IRED; IRED emits ordinary assembly input for A0. The resulting native instructions come from A0. E20.RIL and EDIT86.RIL are the same completed editor source.\n\n'
t+='## Select a document\n\n'+fence('dos','COPY T15.TXT EDIT.TXT\nCHECK E15')
t+='Fixed names keep filename parsing out of this editor. EDIT.TXT is the document; EDIT.TMP and EDIT.BAK are reserved save/recovery names. Copy a source into EDIT.TXT, edit it, and copy it back only after a successful save and a clean return to DOS. Keep a separately named accepted source until the edited source has passed its own build and tests.\n\n'
t+='Do not run two editor instances in the same work directory or change these files while an instance is active. Inspect a pre-existing EDIT.TMP or EDIT.BAK before removing it. A recovery file may be the only copy of a failed save.\n\n'
t+='## Inspect results\n\nUse CHECK immediately so a silent return is visibly PASS or FAIL. Use VIEW.BAS for the reported length and hexadecimal bytes. COMP compares a round trip against its preserved original:\n\n'+fence('dos','ECHO N>NO.TXT\nCOMP EDIT.TXT T15.TXT <NO.TXT')
t+='NO.TXT answers N to COMP\'s request for another comparison. The screen services need the physical text screen and keyboard; redirecting ordinary DOS output does not supply key events or capture the screen. F10 leaves a screen probe or editor. After editing is introduced, Escape cancels the unsaved-changes question.\n\n'
t+='## Memory before entry\n\nThe finished editor retains a 64 KiB main DOS block, obtains eight 32 KiB text blocks and one 16 KiB undo block. That is 336 KiB plus the DOS environment, memory-control records and resident system software. Use the reference 640 KiB machine; total installed RAM alone does not guarantee enough free DOS memory. Every allocation is checked. A failed startup frees the blocks it obtained and returns FAIL without saving the document.\n'
write_page(C/'00-workbench.md',t)

NOTES={
1:'The old built-in table remains intact. `findbuiltin(p)` performs the same complete-token match and argument setup for either table. An unsuccessful first lookup leaves the current source token available for the editor table. Each record names a source spelling, an arity and an IR sequence. The POP before a multi-argument operation places the final argument in A; the preceding arguments remain on the expression stack. This changes neither ordinary user procedures nor the language\'s frame bounds.',
2:'The new operations have no physical-register operands. VPOS takes a cell number in A; VWRITE consumes one saved value and A. BLOAD and BREAD consume three saved values plus A; BMOVE consumes four plus A. Delta values 6 and 5 describe those latter stack effects. Check depth before subtracting it. `editorruntime` reads EDITRT.ASM after source translation has finished, so it may reuse inbuf. It copies every positive read through outchar; it neither assembles text nor supplies instruction bytes. A missing binding aborts publication.',
3:'R_VBEGIN queries the current BIOS mode and accepts only 80-column modes 3 and 7. It remembers the active display page, cursor position and cursor shape, clears the working screen and marks the session active. R_VEND clears that screen and restores the saved cursor state. It does not restore the old screen contents. The common success and failure exits restore DS and ES to the main segment. BIOS calls preserve BP explicitly because the generated procedure frames depend on it.',
4:'A cell number is row times 80 plus column. R_VPOS checks the range 0–1999, divides by 80 and asks the BIOS to position the hardware cursor. R_VWRITE treats bytes as literal cells, with attribute 7; it does not interpret carriage return, tab or line feed. Validate the near span and the complete cell extent before writing. The binding privately selects B800H for color text or B000H for monochrome and adds the active page base. Keeping these addresses here leaves them out of the editor language. Direct cell writes also avoid scrolling when the last cell is written.',
5:'Normal characters retain their byte values. Extended keys are translated through R_KEYMAP into event values beginning at 256. Unrecognized extended keys return zero and do nothing. Control-S, Control-Q and Control-Z also select Save, Quit and Undo. Save, Find, Undo and Quit therefore reach the editor as ordinary word values; no BIOS scan number appears in the RILL source. KEY requires an active screen session and waits for one event.',
6:'BLOAD copies from a near buffer into a checked block; BREAD copies in the other direction. The private words remember both segment/offset pairs and the count while R_BLOCKPTR validates the allocated extent. A near transfer that wraps its sixteen-bit address is rejected. R_COPY selects a backward copy only when a destination follows its source within the same overlapping block; otherwise it copies forward. Every exit restores the segment state expected by generated code. The probe checks actual recovered bytes and an invalid extent through status, without a display helper.',
7:'BMOVE receives source handle, source offset, destination handle, destination offset and count. Resolve both opaque handles with R_BLOCKPTR before touching the destination. The checked descriptor values are private to the binding; the source program keeps only handles. The shared copy handles both directions. The probe first produces AABCDE by moving five overlapping bytes to the right, then ABCDEE by moving them left. A rejected source extent must not turn into a partial copy.',
8:'Each position occupies four near bytes: the low word at its address and the high word two bytes after it. `add` and `sub` accept a word-sized distance and propagate one carry or borrow. `difference` subtracts complete positions; `before` compares high words first. No physical address is represented by these pairs. The stopping test crosses 65535 in both directions, checks a difference of two and returns a status. No console output is part of this arithmetic.',
9:'`pages` holds eight opaque allocation handles. The main block is reduced to 64 KiB by the established allocator before its first DOS request. Each request asks for 32768 bytes, keeping offsets within a word. Store a successful handle immediately so cleanup can find it if the next allocation fails. `release` frees only recorded handles, clears them and remembers a failed release. The fatal path uses that same cleanup. Text bytes need no initial clearing because no byte is read before it becomes occupied document storage.',
10:'Loading fills the prefix of the pages. The gap is initially at the file end: gap equals length, gapend equals capacity, and space equals capacity minus length. `handle` divides a position into a page number and a 0–32767 offset. `peek` adds space for logical bytes at or after the gap. It is called only for positions strictly below length. The reader clips a refill at its current page boundary as well as 4096 bytes, so short positive DOS reads cannot make the next transfer cross a page. At full capacity it probes for one more input byte: EOF is accepted, another byte is rejected.',
11:'`writepart` streams an occupied physical range through io, clipping both at 4096 bytes and at a page boundary. Saving writes [0,gap) and [gapend,capacity), never the free bytes between them. `savefile` refuses pre-existing recovery names, creates its own temporary file, writes and closes it, then backs up the old document before renaming the temporary file. If that rename fails, it attempts restoration. `own` identifies our temporary file; `keep` protects recovery material after an unsuccessful restoration or backup deletion. Abort and cleanup remove only owned, unprotected temporary output. A successful save clears dirty; a failed save leaves the editor open.',
12:'The logical insertion position is gap. The corresponding free interval in physical storage is [gap,gapend), whose size is space. Moving right copies bytes after the gap into its beginning. Moving left copies bytes before it into its end. Choose a chunk no larger than the remaining distance or either page remainder. Left moves work from the end; right moves from the start. The block primitive handles overlap within an individual chunk. A zero-sized gap needs only new position words. Moving the gap changes no document length and creates no disk writes.',
13:'A line ends before CR or LF; nextline consumes CR/LF together and accepts either byte alone. linebegin scans backward to the byte after a terminator. prevline steps over the preceding terminator before finding that line\'s beginning. Empty lines and a final unterminated line need no special stored records. The routines use logical positions and `peek`, so page boundaries and the gap do not change their meaning. Their position arguments may alias as shown; probe is private scratch for the backward scans.',
14:'A column is a visual distance, not a file offset. Ordinary bytes occupy one cell; a tab occupies 8 minus the current column modulo 8. Keep columns as paired words too, because an unusually long line may exceed 65535 cells. `toward` walks a line until another character would pass the wanted column or until a terminator. It stops before a tab that would overshoot. The fixture contains a literal tab between T and X: X begins in column eight, and the position after X has column nine.',
15:'`paintrow` initializes an eighty-byte row, expands tabs into spaces, and substitutes a dot for other controls and high bytes. The underlying text is unchanged. `top` names the first displayed line; `scroll` is the first visible visual column. `refresh` keeps the insertion position within twenty-four rows and eighty columns, then puts the status on row twenty-four. It remembers the previous top and horizontal origin, repainting the whole window when either changes. `layout`, `allrows` and `onerow` distinguish line-layout work from a changed row. The returned hardware cursor is always in a document row.',
16:'The loop refreshes, reads one event and dispatches it through small returning branches. Left and right cross a CR/LF pair as one line ending. Home and End stay on the line; F6 and F7 select document start and end. Up/down preserve a preferred visual column, while Page Up/Down repeat line movement twenty-four times. A nonvertical command ends that preference. Moving across a terminator requests a new layout; ordinary motion within a line needs only cursor placement. Navigation leaves dirty clear and makes no file writes.',
17:'An insertion consumes one byte of space, advances gap and length, and leaves gapend unchanged. Enter inserts CR then LF as one action, after checking room for both. A refused insertion changes neither text nor dirty. An ordinary character marks one row for paint; a new line marks the window and layout. `confirm` asks about unsaved changes: S saves and quits only if saving succeeds, Q discards memory changes, and Escape returns to editing. This conservative flag records that an edit occurred; it does not compare the entire document with disk.',
18:'Forward deletion removes bytes at gap by advancing gapend and reducing length. Backspace first moves the gap to the character on its left, then uses the same deletion. rightcount and leftcount keep CR/LF pairs together while accepting a lone terminator. Do nothing at either document boundary. Read the removed bytes before extending the gap; they still belong to the document until then. A deleted terminator changes line layout, while a plain deleted byte changes only its row.',
19:'Allocate a separate 16384-byte undo block only now. Each eight-byte record holds kind, count, a paired logical position and up to two deleted bytes. uhead selects the next slot; ucount retains at most 2048 edits. On overflow the oldest record is replaced. Remember an insertion before consuming space and a deletion before discarding its bytes. Undo moves the gap to the saved position, removes an inserted span or restores deleted bytes, and conservatively marks the document dirty. There is no redo and no saved copy of the whole document.',
20:'The query accepts up to sixty-four printable characters and Escape cancels it. Enter installs a nonempty literal needle. findnext compares bytes through logical positions, checking length before each read; it can match across a page boundary. F3 begins at the insertion position, while F5 begins one byte later. A found match moves the gap to its first byte and requests layout. Matching is case-sensitive and does not wrap from EOF. Searching changes neither text nor undo records.'
}
old_runtime='';old_editor=''
for case in cases:
 n=case['number'];slug=re.sub('[^a-z0-9]+','-',case['title'].lower()).strip('-');page=f'{n:02}-{slug}.md'
 t=front(f'{n:02} · '+case['title'],n,case['why'],case['source'])+case['why']+'\n\n'+NOTES[n]+'\n\n## Enter the source\n\n'
 source=(W/case['source']).read_text();kind='asm' if 3<=n<=7 else 'rill'
 if n==1:
  base=(ROOT/'workbench/toolchain/RILL.RIL').read_text();t+='Copy the exact toolchain RILL.RIL to RILLED.RIL.\n\n'
 elif n==2:
  base=(ROOT/'workbench/toolchain/IR86.RIL').read_text();t+='Copy the exact toolchain IR86.RIL to IRED.RIL.\n\n'
 elif n<8:
  base=old_runtime;t+=f'Copy S{n-1:02}.ASM to S{n:02}.ASM.\n\n' if base else ''
 else:
  base=old_editor;t+=f'Copy E{n-1:02}.RIL to E{n:02}.RIL.\n\n' if base else ''
 listing,changes=patch(base,source,kind,case['source']);t+=listing
 patches.append(dict(page=page,source=case['source'],base='RILL.RIL' if n==1 else 'IR86.RIL' if n==2 else f'S{n-1:02}.ASM' if 4<=n<=7 else f'E{n-1:02}.RIL' if n>8 else None,kind=kind,changes=changes))
 if 3<=n<=7:
  t+='## The service probe\n\nCreate '+case['probe']+' as plain text:\n\n'+fence('rill',(W/case['probe']).read_text())
  t+=fence('dos',f'COPY {case["source"]} EDITRT.ASM')+buildcommands(case['probe'],f'S{n:02}')+measured(case,f'S{n:02}')
  t+='Run '+f'`CHECK S{n:02}`. '+('The screen clears; the cursor state is restored and CHECK reports PASS.' if n==3 else 'EDIT86 appears in the upper left; the deliberately invalid position is detected, then CHECK reports PASS.' if n==4 else 'Press F10 at the prompt. CHECK must report PASS; a different key deliberately returns FAIL.' if n==5 else 'The exact copied bytes and the rejected extent are checked through status. CHECK must report PASS; no display helper is added.')+'\n\n'
  if n==3:t+='An unsupported mode returns FAIL before the session becomes active. Use an 80-column mode 3 or monochrome mode 7 screen.\n\n'
  if n==4:t+='The request for cell 2000 must fail; the final valid cell is 1999. The probe remembers that status before VEND replaces it.\n\n'
  if n in [6,7]:t+='The invalid transfer starts at offset 63 of a sixty-four-byte block and requests two bytes. It must fail before changing destination memory. Every allocated probe block is freed.\n\n'
  old_runtime=source
 elif n<3:
  name='RILLED' if n==1 else 'IRED';t+='## Build and preserve the builder\n\n'+buildcommands(case['source'],name,'R0','I0')+measured(case,name)
  if n==1:
   t+='Create P01.RIL:\n\n'+fence('rill',(W/'P01.RIL').read_text())+fence('dos','COPY P01.RIL SOURCE.RIL\nCHECK RILLED\nTYPE RESULT.IR')
   t+='Require PASS and exactly this intermediate source:\n\n'+fence('text',(W/'P01.IR').read_text())
   t+='Create Q01.RIL for a wrong-arity check:\n\n'+fence('rill',(W/'Q01.RIL').read_text())+fence('dos','COPY Q01.RIL SOURCE.RIL\nCHECK RILLED')+'Require FAIL; VPOS needs one argument. No native screen code is needed to inspect these compiler results.\n\n'
  else:
   t+='Create the empty S02.ASM binding with `COPY NUL S02.ASM`, then copy it to EDITRT.ASM. Create P02.RIL:\n\n'+fence('rill',(W/'P02.RIL').read_text())
   t+='Build P02.RIL with RILLED, IRED and A0 using the workbench pattern, preserving P02.COM. `CHECK P02` must report PASS. This program uses only the established runtime, so the binding can be empty.\n\n'
   t+='Create Q02.IR:\n\n'+fence('text',(W/'Q02.IR').read_text())+fence('dos','COPY Q02.IR SOURCE.IR\nCHECK IRED')+'Require FAIL with CODE 00004: BMOVE has no four saved arguments. Keep all binding files as ASCII assembly source. A missing EDITRT.ASM is an I/O error and cannot publish a new RESULT.ASM.\n\n'
 else:
  name=f'E{n:02}';t+='## Build and preserve the program\n\n'
  if n==8:t+='Use the completed S07.ASM binding throughout the editor construction:\n\n'+fence('dos','COPY S07.ASM EDITRT.ASM')
  t+=buildcommands(case['source'],name)+measured(case,name)
  if n>=10:
   fixture=(W/case['fixture']).read_text();t+='## The document fixture\n\nCreate '+case['fixture']+' with CR/LF after each displayed line'+(' and a literal tab between T and X' if n==14 else '')+':\n\n'+fence('text',fixture)
   t+=fence('dos',f'COPY {case["fixture"]} EDIT.TXT\nCHECK {name}')
  else:t+='## Check the stopping point\n\n'+fence('dos',f'CHECK {name}')
  checks={
8:'CHECK must report PASS. The arithmetic crosses the low-word boundary, borrows back and checks complete ordering and subtraction. A mistake in carry or borrow must return FAIL rather than merely wrap the low word.',
9:'CHECK must report PASS after obtaining and freeing all eight text pages. In an environment with too little free DOS memory, require FAIL and the allocation diagnostic; previously obtained pages are released. Do not reduce the document capacity silently to hide an allocation failure.',
10:'Require PASS. The diagnostic expects ten file bytes and the first byte 6F. It makes no output file. Copy `123` without a line ending over EDIT.TXT and repeat: require FAIL. Restore the fixture before continuing. A missing file is an empty new document in the retained reader, but this diagnostic intentionally rejects a length other than ten.',
11:'Require PASS and an unchanged document. Compare EDIT.TXT with T11.TXT using COMP. For rejection, create EDIT.TMP containing HOLD, run CHECK E11 and require FAIL with the recovery-file diagnostic. TYPE EDIT.TMP must still show HOLD and COMP must still find the document unchanged. Inspect and remove only that exercise recovery file before continuing.',
12:'Require PASS and an unchanged document by COMP against T12.TXT. The gap has moved to logical position five, but saving must still reproduce all ten bytes. Try a three-byte document: require FAIL with the shorter-than-gap diagnostic and preserve those input bytes. Restore the fixture.',
13:'Require PASS. The beginning, end and following-line positions must be five, eight and ten, and stepping back must recover five. Repeat with an empty document: require FAIL, since these diagnostic positions deliberately describe the supplied two-line fixture. The line routines themselves accept empty documents.',
14:'Require PASS: the position after T, tab and X is visual column nine, and reaching column eight stops before X at byte position two. Repeat with T13.TXT in EDIT.TXT: require FAIL because that file does not contain the tab fixture. No file is saved by either run.',
15:'The screen must show one on the first row, two on the next and the help line on the last row. Press F10; CHECK must report PASS. COMP must still find EDIT.TXT identical to T15.TXT. An empty document displays blank document rows and leaves with PASS. A different exit key deliberately returns FAIL in this screen-only stopping test.',
16:'Try arrows, Home, End, Page Up, Page Down, F6 and F7. The insertion cursor must remain in the document window. F2 saves an unchanged file. F10 returns CHECK PASS; COMP against T16.TXT must show no difference. At the first byte, Left does nothing; at EOF, Right does nothing.',
17:'Type ! at the beginning. The status gains an asterisk. Press F10, then Escape: the document must remain open. Press F2, then F10; require CHECK PASS. VIEW.BAS must report eleven bytes, exactly `21 6F 6E 65 0D 0A 74 77 6F 0D 0A`. On a separate run, type a character then F10 and Q: the accepted disk file must stay unchanged.',
18:'Press Delete at the first byte, type !, then F2 and F10. Require PASS and exactly ten file bytes: `21 6E 65 0D 0A 74 77 6F 0D 0A`. Restore T18.TXT. End then Right crosses CR/LF as one action; Backspace there removes the whole pair. At document start Backspace must do nothing.',
19:'Press Delete, type !, then F4 twice. Save with F2 and leave with F10. Require CHECK PASS and COMP equality with T19.TXT. Another F4 reports that no earlier edit remains. Undoing a line ending restores both CR and LF; navigation alone never creates an undo record.',
20:'Press F3, type two and press Enter. The cursor must move to the second line. Type !, then F2 and F10. Require CHECK PASS and eleven bytes: `6F 6E 65 0D 0A 21 74 77 6F 0D 0A`. Restore T20.TXT; search for absent text and require the not-found message with no document change. Escape cancels a partly entered query. F5 repeats from the byte after the current position.'}
  t+=checks[n]+'\n\n'
  if n==20:t+='Preserve E20.COM as EDIT86.COM. EDIT86.RIL is the same source as E20.RIL. Keep RILLED.RIL, IRED.RIL and EDITRT.ASM with it so the editor can be rebuilt from the established trio.\n\n'
  old_editor=source
 t+='## If the check disagrees\n\n'+('Check the table spelling, argument counts and exact insertion points. Keep the earlier builder executable so a rejected source cannot strand the workbench.' if n<3 else 'Check the saved binding stage and the stated build reports first. A runtime-label error means the matching EDITRT.ASM was not beside the translator. Compare the registers and extent checks before changing the test.' if n<8 else 'Check the exact fixture and the freshly preserved executable first. For position errors, compare both words and the gap/space invariant. For file errors, inspect recovery names and keep the accepted input before another run.')+'\n'
 write_page(C/page,t)
(Q/'article-patches.json').write_text(json.dumps(patches,indent=2)+'\n')
reference='''EDIT86 edits one fixed document, EDIT.TXT. An absent file starts an empty document; a failed inspection or read is an error. Saving an empty document creates a genuine zero-byte file. No byte is treated as a text EOF marker: 1A, NUL and high bytes round-trip unchanged.

## Keys

| Key | Action |
|---|---|
| Printable ASCII, Tab | Insert the character or a literal tab |
| Enter | Insert CR/LF together |
| Backspace, Delete | Remove text on the left or right; CR/LF stays paired |
| Arrows | Move the insertion position; up/down retain a preferred visual column |
| Home, End | Beginning/end of the physical line |
| Page Up, Page Down | Move twenty-four physical lines |
| F6, F7 | Document start/end |
| F2 or Control-S | Save EDIT.TXT |
| F3 | Enter a literal, case-sensitive search; Enter accepts, Escape cancels |
| F5 | Find the next occurrence, starting one byte later; no wrap |
| F4 or Control-Z | Undo one retained edit |
| F10 or Control-Q | Quit; S saves, Q discards, Escape cancels when dirty |

Tabs use eight-column stops. Other control and high bytes display as dots but retain their exact values. Long lines scroll horizontally; they do not wrap into extra screen rows. CR/LF, lone CR, lone LF and a final unterminated line are accepted. Newly entered line endings are CR/LF. There is no line-length or line-count table bound. Very long lines and distant searches require scans and can be slow on an 8088.

## Document representation

Positions are unsigned pairs of words, low word first. Capacity is (0000H,0004H), or 262144 bytes. Logical text has length bytes. Physical text occupies [0,gap) and [gapend,capacity); the interval [gap,gapend) is free. Thus gapend minus gap equals space, and length plus space equals capacity. gap is also the insertion position. Logical positions below gap map directly; positions at or after it add space. End positions may equal capacity, but byte access is restricted to positions below length.

The physical page number is high-word times two plus bit fifteen of the low word. The page offset is the low word AND 32767. Eight opaque block handles identify the pages. A handle is never a segment or a near pointer. A checked bulk move clips at both source and destination page ends; the helper handles overlap within each chunk.

A full 256 KiB file is accepted, but it has no free insertion room. Delete before inserting. Enter requires two free bytes and is refused as a whole if only one remains. Refused edits create no undo record. The editor keeps the complete document in RAM; navigation neither pages text to disk nor silently saves it.

## Memory budget

| Storage | Amount | Reason |
|---|---|---|
| Main DOS block | 64 KiB | PSP, near code/static data, ordinary buffers and stack |
| Document | 8 times 32 KiB | 256 KiB shared by occupied text and gap |
| Undo | 16 KiB | 2048 records of eight bytes |
| Requested program blocks | 336 KiB | Main block plus nine auxiliary blocks |
| Additional conventional memory | Depends on DOS environment | Environment, DOS control records, resident software and fragmentation |

The main image remains below the 61184-byte profile bound; the upper 4 KiB remains its guarded stack. Auxiliary memory enlarges data capacity, not near-code reach. The existing sixteen-slot allocator has seven unused slots. No full line index, second document copy or disk cache is allocated. A startup failure frees acquired blocks and returns nonzero. Installed RAM is not the same as available DOS memory.

Undo stores kind and count bytes, low/high logical position words and two deleted bytes. It retains the newest 2048 successful insert/delete actions, including paired line endings. New edits overwrite the oldest retained record. There is no redo. Saving does not clear the ring. Undo conservatively marks dirty even when it happens to restore saved text.

## Screen and key services

These are extensions in RILLED and IRED, not changes required by the preceding bootstrap tools. Every service sets persistent status: zero on success, nonzero on failure. STATUS itself leaves that state unchanged; save it before another service replaces it.

| RILL call | Meaning |
|---|---|
| vbegin(), vend() | Enter/leave a screen session; preserve cursor settings, clear the working screen |
| vpos(cell) | Position the cursor at cell 0 through 1999 |
| vwrite(pointer,count) | Write literal consecutive cells with the normal attribute; never scroll |
| key() | Wait for a character/event word; zero denotes an unrecognized extended key |
| blockload(block,offset,pointer,count) | Near buffer to checked allocated block |
| blockread(block,offset,pointer,count) | Checked allocated block to near buffer |
| blockmove(source,sourceOffset,dest,destOffset,count) | Checked overlap-safe transfer between blocks |

Near pointers must name valid program storage for the complete count. Wrapping a near address is rejected. Both allocated extents are validated before a move. An offset must be strictly below the allocation size, including on a zero-count transfer; counts must fit the remaining extent. Copies set no terminator. Main-segment state is restored on success and failure.

VWRITE checks its screen extent; it advances the internal cell position but leaves hardware cursor placement to VPOS. It writes literal byte values; the editor supplies tab expansion and control substitution. Screen calls and KEY require a successful VBEGIN. The 8086 binding accepts BIOS text modes 3 and 7 with eighty columns and twenty-five rows. It uses the active page, a fixed normal attribute, BIOS cursor/key services and private text-video addresses. It does not switch modes, preserve old screen contents, resize the screen or implement terminal escape sequences.

| Event | Value |
|---|---|
| Left, Right, Up, Down | 256, 257, 258, 259 |
| Home, End, Page Up, Page Down | 260, 261, 262, 263 |
| Delete, Save, Quit, Undo | 264, 265, 266, 267 |
| Find, Next, Document start, Document end | 268, 269, 270, 271 |

The IR names are VBEGIN, VEND, VPOS, VWRITE, KEY, BLOAD, BREAD and BMOVE. Multi-argument operations take their final argument in A and consume the earlier arguments from the expression stack in source order. VWRITE consumes one saved word; BLOAD/BREAD consume three; BMOVE consumes four. Their result is zero except KEY's event. STATUS gives the service outcome. No physical registers, native handles or video addresses appear in this IR interface.

## Saving and recovery

Existing EDIT.TMP or EDIT.BAK blocks entry and saving. Saving needs enough free disk space for a complete temporary document alongside the accepted file. Use the hard-disk workbench for large sources. After the complete text is written to EDIT.TMP and that handle is closed, an existing EDIT.TXT is renamed EDIT.BAK, the temporary is renamed EDIT.TXT and the backup is deleted. A failed publication attempts restoration. DOS renaming is not atomic replacement, and this is not a power-loss guarantee.

Ordinary failed saves leave the accepted document intact and keep dirty set. Failed restoration retains EDIT.TMP and EDIT.BAK for inspection, possibly with no EDIT.TXT. Failed backup removal retains the new EDIT.TXT and old EDIT.BAK. Cleanup protects retained recovery material, prints a warning and returns FAIL. Do not retry blindly or delete either copy before inspecting it. Copy a selected recovery file to a separately named safe file first.

The normal return is zero. Startup, fatal service or cleanup failure returns one; screen/file diagnostics identify the failing operation. A rejected edit or failed recoverable save leaves the editor running with a status-line explanation. CHECK reports the final DOS status, while the on-screen Saved message confirms an accepted save. A clean quit does not prove a prior failed save succeeded: a deliberate discard also returns zero.

There are no filename prompts, command-line options, multiple documents, selection, clipboard, replace, redo, syntax coloring, automatic writes or disk-backed document pages. The fixed names and bounded records keep this first editor within the existing language and memory profile.
'''
write_page(C/'21-reference.md',front('The editor and service reference',21,'Keys, logical positions, memory, native binding and save recovery.','EDIT86.RIL')+reference)
t=front('Editing a workbench source',22,'Use the editor on the actual source formats and preserve an accepted source.','EDIT86.RIL')
t+='Use EDIT86 in a separate hard-disk directory. Keep EDIT86.COM, its source, the service builders and their binding together. Select a source with COPY:\n\n'+fence('dos','COPY IR86.RIL HOLD.RIL\nCOPY IR86.RIL EDIT.TXT\nCHECK EDIT86')
t+='Try F3 to find a routine name, F5 for another occurrence, and F6/F7 for document ends. On this first pass, make no changes; press F2 then F10. Require Saved on screen and CHECK PASS. Compare the complete file:\n\n'+fence('dos','COMP EDIT.TXT HOLD.RIL <NO.TXT')
t+='Require no difference, then inspect its length with VIEW.BAS. Repeat with a .BAS, .ASM and .IR source selected under the same EDIT.TXT name. This checks source round trips rather than adding a new display program. A source larger than 65535 bytes is still one document. The total occupied bytes must not exceed 262144, and a full document needs a deletion before growth.\n\n'
t+='For an actual edit, keep HOLD.RIL, change the working document, save with F2 and leave with F10. Copy it back only after the Saved report:\n\n'+fence('dos','COPY EDIT.TXT IR86.RIL')
t+='Build and test that changed source with the existing toolchain before replacing an accepted tool executable. Keep the old source and executable until that check passes. EDIT86 edits bytes; it does not validate RILL syntax or assemble source for you.\n\n'
t+='To test rejection without risking a source, preserve EDIT.TXT, create a small EDIT.TMP containing HOLD, and run CHECK EDIT86. Require FAIL with the recovery-file diagnostic. Inspect both files to confirm they were preserved. Remove only the deliberate exercise file after that check.\n'
write_page(C/'22-editing-a-workbench-source.md',t)
print('Published editor workbench, twenty construction lessons, reference and source exercise')
