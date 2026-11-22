"""Print exact bottom-up source edits and native-measured stopping tests."""
from project_paths import directory_name
from publication_names import write_page
from pathlib import Path
from difflib import SequenceMatcher
from assembly_edits import source_note
from assembler_article_notes import ASM1_NOTES
from assembler_stream_checks import exercise
import json,re,tomllib
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/asm86';Q=ROOT/'qa/asm86';C=ROOT/'site/content/bootstrap/asm86';C.mkdir(parents=True,exist_ok=True)
cases=json.loads((Q/'checkpoints.json').read_text());examples=json.loads((Q/'examples.json').read_text())
SEED_STORY_OPENINGS={
 1:"I have followed the names from the PSP to the file services and into the success report. Now I turn to the arithmetic table. The next assembler will hash names, and I need to account for the XOR instruction it will use.",
 2:"I follow the source reader in my notebook: it asks DOS for one byte, then asks again for the next. I want to collect a small block at once and let the reader hand those bytes to the parser one at a time. The parser should still receive the same characters in the same order.",
 3:"The output buffer still has to hold every byte of the assembled program. I want to write a block when it fills and reuse that space. I'll first try the writer by copying a few characters from one file to another, with the parser left out of the path.",
 4:"The copy writer creates its temporary file before opening the source. If that open fails, an empty file remains. I need to keep track of which handles are open and which file this run created, so the error routine can clean up after itself.",
 5:"I have given the temporary file a fixed name, but finding that name on disk does not tell me where it came from. It might be left from an interrupted run. I want the program to stop and let me inspect it before creating anything under the same name.",
 6:"The copied bytes are safely in a closed temporary file. I want to give that file the result name while keeping a way back if a rename fails. I write the three filenames in my notebook and follow where the accepted copy would be after each DOS call.",
 7:"I have checked the writer with copied characters. Now I can put the parser back in the path and send it assembly source again. Pass one will count the instruction bytes; pass two will feed them to the block writer as they are made.",
 8:"I look at the comments and labels in my source: much of what I type never becomes an instruction byte. The block reader can keep going through a long file, but its line counter still stops at 4000. I'll extend that counter's permitted range while keeping a check against wraparound.",
 9:"With the whole-image output buffer gone, I can give more room to names. I redraw the memory sketch before moving anything, marking the line, token, two file blocks, symbol records and stack. Each needs its own part of the segment.",
 10:"My memory sketch still fits inside one segment. Reading the segment-register MOV forms in the processor manual shows me how another program could select storage elsewhere. I'll teach ASM1 to encode those forms using instructions ASM0 already accepts.",
 11:"Selecting a segment register is only part of addressing storage elsewhere. A memory instruction must also use that segment. I'll add the explicit `ES:` spelling and follow the extra prefix byte into the output, keeping the ordinary offset and width rules in place.",
 12:"I save the accepted source as ASM1.ASM and keep the copy ASM0 built. I've changed how the assembler reads, writes and uses its workspace. I want the same evidence I required of ASM0: two self-built copies that match the preserved executable byte for byte.",
}
SEED_STORY_AFTER_CHECKS={
 3:"The viewer shows `41 42 43 0D 0A`, matching the characters and line ending I put in the source file. I can trace this small copy through the reader, the output block and DOS before involving instruction encoding again.",
 7:"The instruction bytes match the earlier result. I trace them from the parser through EMIT to the disk file; they no longer accumulate in a buffer for the whole program. I can erase that buffer from the memory sketch.",
 12:"I put the matching generations beside the ASM0-built copy, still under its own name. Looking back at the memory sketch, I can account for the space I have reused and the file routines doing the work. ASM1 can reproduce itself with that arrangement.",
}
LARGER_STORY_OPENINGS={
 13:"ASM1 can encode segment-register moves and ES memory accesses. Now I have a use for them in the assembler itself. I turn to the DOS memory calls in the manual: before moving the names out of the main segment, I need to obtain their storage and be able to return it, even if a later allocation fails.",
 14:"My memory sketch now has boxes outside the main segment. A record number must lead me to both the right box and the right place inside it. I'll check the last record slot in the last page before trusting that calculation with any source names.",
 15:"DOS has given me storage, but it has not promised what bytes are already there. I sketch one complete symbol record in the notebook and mark what every field should contain. The writer must establish all of it, including the unused name bytes.",
 16:"I can put a name in a record. Finding it again means choosing which records to examine. A bucket number will narrow the search, but I still need to read every letter before deciding that a stored name is the one in the source.",
 17:"The page helpers have passed their small checks while the old symbol table has continued doing the assembly. Now I can connect the new table to definitions and operands. I'll leave the file buffers where they are while I check that change.",
 18:"The names have moved out of the main segment. I spread the memory sketch across another notebook page and give the code, line, token, file blocks and stack their marked ranges. There is room to retain longer spellings and read longer source lines, provided every copy stays within its boundary.",
 19:"The source reader can refill its block as often as needed, but a word-sized count still ends at 65535. Comments count as source lines too, even though they add no program bytes. I work through the carry from the low word into a second word before changing the counters and their printed report.",
 20:"I can still recognize the greeting among its decimal ASCII values, but I would rather type the words I mean. Quotation marks can tell the assembler where the text begins and ends. Inside them, a lowercase letter or a semicolon must survive exactly as I typed it.",
 21:"A label gives me an address, but I often need a place a little beyond it or the distance between two labels. I want to leave that relationship visible in the source. I'll begin with addition, subtraction and parentheses, keeping track of values that are not known on the first pass.",
 22:"I have started writing relationships between values in the source. A repeated count deserves a name of its own too. That name must have the same value on both passes, and defining it should leave the next instruction's address alone.",
 23:"Drawing a working area in the notebook is easy; spelling it as a long row of zeroes is tedious. I'll give a byte or word count to a storage directive. The assembler must still write those zeroes into the file and check that the area fits the program image.",
 25:"The MOV paths already need to remember an address, a width and sometimes a segment prefix. I keep finding those same questions in the notes for each operand. I'll collect the answers into one description while retaining the address forms I can already check.",
 27:"The processor manual gives each legal memory-register combination a ModR/M code. I copy that small table into the notebook and work through how an address reaches its code. The parser still supplies only a direct address or BX here; the mapping can be put in place without changing that vocabulary yet.",
 29:"I draw the stack after CALL and PUSH BP, marking the return address, the argument above it and a local word below BP. Addresses such as `[BP+4]` and `[BP-2]` would let the source follow that drawing. I'll extend the memory parser and trace the argument through a small routine.",
 30:"So far, writing a value into memory has meant putting it through a register first. With the address description available, I can teach MOV to store an immediate value directly. The source will have to say BYTE or WORD so the assembler knows how much to write.",
 32:"I mark a byte inside a table in the notebook. Sometimes I need that byte; sometimes I need its address to pass to a routine. LEA supplies the offset calculation without reading the stored byte. I'll keep those two jobs distinct as I add its encoding.",
 37:"The shift forms in the processor manual have a restriction worth keeping beside the listing: the count is one or it comes from CL. I'll accept those forms explicitly. A convenient-looking spelling must not make the assembler emit an instruction my 8088 cannot execute.",
 40:"I put the completed source beside the copy built by ASM1. The memory sketch now includes allocated pages, and the instruction notes cover far more operand forms than when I began. The builder is still the preserved seed. I'll ask the larger assembler to reproduce that executable, then let its copy repeat the job.",
}
LARGER_STORY_AFTER_CHECKS={
 17:"The two bytes `00 01` give HERE its expected address. This time the definition and the operand have met through the allocated table. The page helpers are doing the assembler's ordinary work now.",
 20:"The viewer shows lowercase letters and the semicolon among the message bytes. Those characters used to need separate numeric entries. I can read the sentence in the source and still account for every byte in the file.",
 40:"I keep the seed-built copy beside the two matching generations. Its file is still a single COM program; the extra symbol pages are workspace it obtains when it runs. I can follow how ASM1 made the first copy and how that copy made the next.",
}
STORY_OPENINGS={**SEED_STORY_OPENINGS,**LARGER_STORY_OPENINGS}
STORY_AFTER_CHECKS={**SEED_STORY_AFTER_CHECKS,**LARGER_STORY_AFTER_CHECKS}
def fence(kind,s):return '```'+kind+'\n'+s.rstrip('\n')+'\n```\n\n'
def front(title,weight,description,download,cartoon=None):
 s='+++\n'+f'title = {json.dumps(title)}\nweight = {weight}\ndescription = {json.dumps(description)}\ndownload = "{download}"\n'
 if cartoon:s+=f'cartoon = "{cartoon}"\n'
 return s+'+++\n\n'
def slug(s):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
from write_asm1_steps import publish as publish_intro
publish_intro()
previous=(ROOT/'workbench/asm1/A01F.ASM').read_text().splitlines();patches=[];previous_number=None
chapters={c['number']:i for i,c in enumerate([r for r in cases if r['number']>12],1)}
for case in cases:
 n=case['number'];collection='asma0' if n<=12 else 'asm86a';chapter=n+6 if n<=12 else chapters[n];C=ROOT/'site/content/bootstrap'/directory_name(collection);C.mkdir(parents=True,exist_ok=True);name=f'A{n:02}';oldfile='A01F.ASM' if n==1 else 'ASMA0.ASM' if n==13 else f'A{previous_number:02}.ASM';lines=(W/(name+'.ASM')).read_text().splitlines();page='01-fixed-work-files.md' if n==1 else f'{n:02}-{slug(case["title"])}.md'
 t=front(f'{chapter:02} · '+case['title'],chapter,case['description'],name+'.ASM',case.get('cartoon'))+STORY_OPENINGS.get(n,case['why'])+'\n\n'
 if n<=12:t+=source_note(oldfile,name+'.ASM','ASMKEEP.COM')
 t+='## The working parts\n\n'+case['explain']+'\n\n## Enter the source\n\n'
 if n<=12:
  t=t.replace('+++\n\n',f'aliases = [\"/bootstrap/asm86a/{page[:-3]}/\"]\n+++\n\n',1)
  (ROOT/'site/content/bootstrap/asm86'/page).unlink(missing_ok=True)
 t+=f'Copy `{oldfile}` to `{name}.ASM`. '
 if n<=12:
  from assembly_edits import patch as label_patch
  printed,changes=label_patch(previous,lines)
  t+=printed
 else:
  edits=[o for o in SequenceMatcher(None,previous,lines,autojunk=False).get_opcodes() if o[0]!='equal'];changes=[]
  if edits:t+='Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.\n\n'
  else:t+='The tested source is retained without edits. This stopping point proves the executable handoff.\n\n'
  for i,(_,a,b,c,d) in enumerate(reversed(edits),1):
   before=previous[max(0,a-3):a];after=previous[b:b+2];old=previous[a:b];new=lines[c:d];labels=[v for v in previous[:a] if v.endswith(':')]
   t+=f'### Change {i}'+(' near `'+labels[-1]+'`' if labels else ' at the entry')+'\n\n'
   if before:t+='Unchanged source immediately before this edit:\n\n'+fence('asm','\n'.join(before))
   if old:t+=f'Remove this exact source at old physical positions {a+1}–{b}:\n\n'+fence('asm','\n'.join(old))
   else:t+=f'Insert after old physical line {a}.\n\n'
   if new:t+=('Replace it with:\n\n' if old else 'Insert:\n\n')+fence('asm','\n'.join(new))
   else:t+='There is no replacement source.\n\n'
   if after:t+='The following old source stays in place:\n\n'+fence('asm','\n'.join(after))
   changes.append(dict(a1=a,a2=b,old=old,new=new,context=before,after=after))
 t+='## Build the stopping point\n\n'
 if n<=12:
  t+=f'Copy `{name}.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK {case["binary_bytes"]:05} bytes` and PASS. This uses the preceding published ASM86, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM {name}.COM`.\n\n'
 else:
  t+=fence('dos',f'COPY {name}.ASM SOURCE.ASM\nCHECK ASMA0')+f'Require `OK RESULT.COM {case["binary_bytes"]:05} bytes` and PASS. Preserve this executable before using its fixed output name:\n\n'+fence('dos',f'COPY RESULT.COM {name}.COM')
 if n>12:t+=f'VIEW.BAS must report {name}.COM length {case["binary_bytes"]} bytes. '
 t+='Keep that executable and source together.\n\n'
 if n in (13,14,15):
  from asm86_memory_checks import article as memory_article
  t+=memory_article(n)
 t+=('## Ordinary assembly regression check\n\n' if n in (13,14,15) else '## Acceptance check\n\n')
 if case.get('fixture_ref'):
  alias=case['fixture_ref'];t+=fence('dos',f'COPY {name}.ASM {alias}\nCOPY {name}.COM {Path(alias).stem}.COM\nCOPY {alias} SOURCE.ASM')
 else:
  repeated={4:3,5:3,6:3,7:2,8:2,9:2}
  if n in repeated:
   t+=f'Reuse the earlier input unchanged:\n\n'+fence('dos',f'COPY T{repeated[n]:02}.ASM T{n:02}.ASM\nCOPY T{n:02}.ASM SOURCE.ASM')
  else:
   t+=f'Create T{n:02}.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:\n\n'+fence('asm' if n not in range(3,7) else 'text',case['fixture'].replace('\r\n','\n'))+fence('dos',f'COPY T{n:02}.ASM SOURCE.ASM')
 t+=fence('dos',f'CHECK {name}')+'Require:\n\n'+fence('text',case.get('prefix','').replace('\r\n','\n')+f'OK {case.get("output_file","RESULT.COM")} {case["target_bytes"]:05} bytes\nPASS')
 target=case.get('output_file','RESULT.COM');shown=case['target_hex'].split()[:32]
 t+=f'In VIEW.BAS, inspect {target}. Require length **{case["target_bytes"]} bytes** and '+('these complete contents' if case['target_bytes']<=32 else 'these first thirty-two bytes')+':\n\n'+fence('text',' '.join(shown))
 if case.get('inspection_rows'):
  t+=case['inspection_note']+'\n\n| Source instruction | Emitted bytes |\n|---|---|\n'
  t+=''.join(f'| `{source}` | `{encoded}` |\n' for source,encoded in case['inspection_rows'])+'\n'
  t+='This fixture is an encoding fragment, not a complete DOS program. Inspect its bytes; do not run RESULT.COM.\n\n'
 if case.get('self_build'):
  alias='ASMA0' if n==12 else 'ASM86A'
  t+='Compare the first self-produced executable with the preserved original, then use that new generation to assemble the same source once more:\n\n'+fence('dos',f'FC /B {alias}.COM RESULT.COM\nCOPY RESULT.COM GEN1.COM\nCHECK GEN1\nFC /B {alias}.COM RESULT.COM')
  t+=f'Both FC comparisons must report no differences. GEN1 must report `OK RESULT.COM {case["binary_bytes"]:05} bytes` and PASS. Keep the original {alias}.COM separately.\n\n'
  if n in STORY_AFTER_CHECKS:t+=STORY_AFTER_CHECKS[n]+'\n\n'
  if n==12:t+='Continue with the separate [ASM86A collection](../../asm86a/index.html). For its construction builds, ASMA0.COM is the preceding builder. ASMKEEP.COM remains the original ASM86. ASM1 accepts PSP filenames; ASM0 keeps its fixed work files. Preserve each builder under its own name.\n\n'
  else:t+=fence('dos','COPY ASM86A.COM ASMAKEEP.COM')+'ASMAKEEP.COM is the preserved command-line assembler. ASMKEEP.COM still names the original ASM86.\n\n'
 else:
  if not case.get('inspection_rows'):
   if n>12:t+='The byte inspection is the stopping check for this encoding exercise. Keep the result as data.\n\n'
   else:t+=('These are the copied text bytes, including their line ending. Inspect the result as data.\n\n' if n in range(3,7) else 'The byte inspection checks the accepted result. Keep it as data.\n\n')
  if n in STORY_AFTER_CHECKS:t+=STORY_AFTER_CHECKS[n]+'\n\n'
 t+=exercise(n)
 if n not in (2,8):
  t+='## A rejection check\n\n';bad=case['bad']
  if n in [3,4,5]:t+='After inspecting the successful copy, delete ASMA.TMP. It belongs to this copy exercise.\n\n'
  if bad['kind']=='source':
   t+=f'Create X{n:02}.ASM with this separate source:\n\n'+fence('asm',bad['text'])+fence('dos',f'COPY X{n:02}.ASM SOURCE.ASM\nCHECK {name}')
  elif bad['kind']=='missing':t+=fence('dos',f'REN SOURCE.ASM HOLD.ASM\nCHECK {name}')+'Choose an unused HOLD.ASM name before renaming. Restore HOLD.ASM to the selected fixture name afterward.\n\n'
  else:t+=fence('dos',f'ECHO RECOVERY>ASMA.TMP\nCHECK {name}')+'TYPE ASMA.TMP afterward: its RECOVERY text must be unchanged. After inspection, delete this deliberately created test file.\n\n'
  t+='Require:\n\n'+fence('text',case.get('prefix','').replace('\r\n','\n')+f'ERROR {bad["line"]:0{10 if n>=19 else 5}} CODE {bad["code"]}\nFAIL')
  if n==3:t+='This early writer creates an empty ASMA.TMP before discovering the missing source. Inspect it and delete it before another run. RESULT.COM must be unchanged.\n\n'
  elif n==4:t+='The pre-existing RESULT.COM must remain unchanged. A missing-source failure must remove only the temporary file this run owned.\n\n'
  elif n==5:t+='PREFLIGHT must leave both the pre-existing RESULT.COM and the unowned ASMA.TMP unchanged. No output file should be created or removed by this rejected run.\n\n'
  else:t+='The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with FC /B if in doubt. Require a fresh OK before using any output.\n\n'
 if case.get('extra_rejections'):
  t+=case['rejection_note']+'\n\n'
  for extra in case['extra_rejections']:t+=fence('asm',extra['text'])
 if n in [9,17]:
  limit=2048 if n==9 else 8192
  t+='## Fill the symbol table\n\nEnter SYMS.BAS as a source-text exercise:\n\n'+fence('basic',(W/'SYMS.BAS').read_text().replace('10 N=8192',f'10 N={limit}'))
  t+=f'Run GWBASIC SYMS.BAS, require SOURCE.ASM READY, and use SYSTEM to return to DOS. BASIC closes the text file with its normal source Control-Z marker. Run CHECK {name} SOURCE.ASM RESULT.COM. Require `OK RESULT.COM 00004 bytes` and PASS. VIEW.BAS must show `00 01 00 01`: all definitions have value 0100H because none emits bytes. This file is data, not an executable.\n\n'
  t+=f'Keep a copy of that result. Change BASIC line 10 to `10 N={limit+1}` and RUN again. CHECK {name} SOURCE.ASM RESULT.COM must report `ERROR {limit+1:05} CODE 5` and FAIL, preserving the four-byte result. Restore the stated accepted N before another run. The BASIC program creates assembly source, never executable bytes.\n\n'
 if n==19:
  t+='## A long source, a small result\n\nEnter LONGSRC.BAS:\n\n'+fence('basic',(W/'LONGSRC.BAS').read_text())
  t+='Run it in BASIC, require SOURCE.ASM READY, and return to DOS with SYSTEM. Its closed text file includes BASIC\'s ordinary source Control-Z. CHECK A19 SOURCE.ASM RESULT.COM must report `OK RESULT.COM 00001 bytes` and PASS. VIEW.BAS must show exactly `01`. The comments exceed a word-sized physical-line count while the output stays small; do not execute this data.\n\nChange BASIC line 50 to `50 PRINT #1,"UNKNOWN"`, RUN again, and return to DOS. CHECK A19 SOURCE.ASM RESULT.COM must report `ERROR 0000065537 CODE 1` and FAIL. The one-byte accepted RESULT.COM must remain unchanged. Restore the original line 50 before another run.\n\n'
 if n==23:
  t+='## Reach the image boundary\n\nMake LIMIT.ASM containing `RESB 61184`. Run CHECK A23 LIMIT.ASM RESULT.COM. Require `OK RESULT.COM 61184 bytes` and PASS. VIEW.BAS must show length 61184 and zero bytes. This is storage data, never a runnable program. Preserve it; change the count to 61185 and repeat. Require `ERROR 0000000001 CODE 5` and FAIL, with the previous result unchanged. The target limit is independent of the assembler\'s output-block size.\n\n'
 t+='An unexpected PASS fails this rejection test.\n\n## If the result differs\n\n'
 if n in ASM1_NOTES:t+=ASM1_NOTES[n]+'\n'
 elif n==10:t+='Check the four appended REGTAB records, the register kind and width, and SEGMOV\'s 8CH/8EH choice. The segment number belongs in the ModR/M register field; the ordinary word-register number belongs in its r/m field. The colon lookahead must restore SI for a standalone segment operand.\n'
 elif n==11:t+='Check SEGOPERAND\'s saved cursor and ES-only selector, PREFIX for the current operand, and P1 for the first operand. OPERAND must clear PREFIX on each new operand; a store must use saved P1. A spare 26H on an ordinary access reveals a prefix that was not cleared.\n'
 elif n<20:t+='Check ES at helper exits, the saved page segment and offset, record padding, and the complete spelling comparison. Check carry after every DOS memory call. A successful allocation does not initialize its contents.\n'
 elif n<25:t+='Check saved expression values across EMIT, the unresolved-reference flag, and fixed statement lengths in both passes. Quoted text bypasses mnemonic folding. A reserve count must be checked before multiplication or output.\n'
 else:t+='Check descriptor width, segment selection, ModR/M bits, displacement order, and registers changed by EMIT. Use the printed bytes to distinguish a parser mistake from an encoding mistake. Keep the branch size the same in both passes.\n'
 # Keep a single article per retained source and preserve earlier route names.
 routes=[]
 removed={36:[34,35],37:[38,39]}.get(n,[])
 old_specs=json.loads((ROOT/'tools/asm86a_installments.json').read_text())
 for missing in removed:
  old_case=next(c for c in old_specs if c['number']==missing)
  routes.append('/bootstrap/asm86a/'+f'{missing:02}-'+slug(old_case['title'])+'/')
 for oldpage in [p for number in [n,*removed] for p in C.glob(f'{number:02}-*.md')]:
  metadata=tomllib.loads(oldpage.read_text().split('+++')[1]);routes+=metadata.get('aliases',[])
  if oldpage.name!=page:
   routes.append('/bootstrap/'+collection+'/'+oldpage.stem+'/');oldpage.unlink()
 if routes:
  frontmeta=tomllib.loads(t.split('+++')[1]);routes+=frontmeta.get('aliases',[])
  routes=sorted(set(routes)-{'/bootstrap/'+collection+'/'+page[:-3]+'/'})
  t=re.sub(r'^aliases = .*\n','',t,flags=re.M)
  t=t.replace('+++\n\n','aliases = '+json.dumps(routes)+'\n+++\n\n',1)
 write_page((C/page),t);patches.append(dict(number=n,chapter=chapter,collection=collection,page=page,base=oldfile,changes=changes,edit_style='labels' if n<=12 else 'positions'));previous=lines;previous_number=n
(Q/'article-patches.json').write_text(json.dumps(patches,indent=2)+'\n')
# Whole-program examples and their measured rejection edits.
t=front('27 · Complete assembly programs',27,'Strings, a stack frame, a distant conditional, and explicit byte movement.','ASM86A.ZIP')
t+='I return to a greeting, this time with its words in quotation marks and its length calculated from the labels. Beside it I keep a stack drawing for the procedure call and trace a conditional jump across a longer gap. These small programs let me follow the new source forms all the way to their results.\n\n'
t+='Use the completed ASMAKEEP.COM. For each NAME.ASM below, run CHECK ASMAKEEP NAME.ASM RESULT.COM. Require OK and PASS before copying RESULT.COM to NAME.COM. Inspect it with VIEW.BAS before running CHECK NAME.\n\n'
notes={'HELLO':'DOS function 40H writes a counted string. Both carry and the returned count are checked. Quoted data preserves the mixed case; CR and LF are explicit bytes.', 'FRAME':'CALL pushes the return address; PUSH BP saves the caller frame. BP+4 addresses the word argument. BP-2 is a local word after SUB SP,2. Restoring SP and BP precedes RET. The caller releases its argument with ADD SP,2. BP-based memory defaults to SS.', 'BRIDGE':'The nonzero word takes JNE NEAR across a zero-filled region. The opposite short branch skips E9 and its word displacement when the condition is false. The intervening bytes are never executed.', 'COPYTEXT':'A COM program begins with DS and ES selecting the program segment. CLD makes movement advance. The LODSB/STOSB loop copies two bytes, then the output loop prints the copy. The copy loop consumes CX; the output loop loads its own count.'}
for r in examples:
 name=r['name'];t+='## '+name+'\n\n'+fence('asm',(W/(name+'.ASM')).read_text())+notes[name]+'\n\n'
 t+=f'Require `OK RESULT.COM {r["binary_bytes"]:05} bytes` and PASS. VIEW.BAS must report length {r["binary_bytes"]} and these first thirty-two bytes:\n\n'+fence('text',r['hex'])
 t+=f'After saving RESULT.COM as {name}.COM, CHECK {name} displays '+json.dumps(r['output'])+' and reports PASS. Here `\\r\\n` means carriage return followed by line feed.\n\n'
 t+='For a separate rejection, copy the source to BAD.ASM. Replace `'+r['bad_before']+'` with `'+r['bad_after']+'`. Run CHECK ASMAKEEP BAD.ASM RESULT.COM. Require '+f'`ERROR {r["bad_line"]:010} CODE {r["bad_code"]}` and FAIL. The accepted RESULT.COM must remain unchanged; an unexpected PASS fails the check. Restore the accepted source before rebuilding.\n\n'
write_page((C/'43-programs.md'),t)
print('Rendered 18 ASM1 and 24 ASM86 checkpoints and the complete ASM86 programs.')
