"""Print exact bottom-up source edits and native-measured stopping tests."""
from publication_names import write_page
from pathlib import Path
from difflib import SequenceMatcher
import json,re
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/asm86a';Q=ROOT/'qa/asm86a';C=ROOT/'site/content/bootstrap/asm86a';C.mkdir(parents=True,exist_ok=True)
cases=json.loads((Q/'checkpoints.json').read_text());examples=json.loads((Q/'examples.json').read_text())
def fence(kind,s):return '```'+kind+'\n'+s.rstrip('\n')+'\n```\n\n'
def front(title,weight,description,download,cartoon=None):
 s='+++\n'+f'title = {json.dumps(title)}\nweight = {weight}\ndescription = {json.dumps(description)}\ndownload = "{download}"\n'
 if cartoon:s+=f'cartoon = "{cartoon}"\n'
 return s+'+++\n\n'
def slug(s):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
previous=(ROOT/'workbench/asm86/ASM86.ASM').read_text().splitlines();patches=[]
for case in cases:
 n=case['number'];collection='asma0' if n<=12 else 'asm86a';chapter=n if n<=12 else n-12;C=ROOT/'site/content/bootstrap'/collection;C.mkdir(parents=True,exist_ok=True);name=f'A{n:02}';oldfile='ASM86.ASM' if n==1 else 'ASMA0.ASM' if n==13 else f'A{n-1:02}.ASM';lines=(W/(name+'.ASM')).read_text().splitlines();page=f'{n:02}-{slug(case["title"])}.md'
 t=front(f'{chapter:02} · '+case['title'],chapter,case['description'],name+'.ASM',case.get('cartoon'))+case['why']+'\n\n## The working parts\n\n'+case['explain']+'\n\n## Enter the source\n\n'
 if n<=12:
  t=t.replace('+++\n\n',f'aliases = [\"/bootstrap/asm86a/{page[:-3]}/\"]\n+++\n\n',1)
  (ROOT/'site/content/bootstrap/asm86a'/page).unlink(missing_ok=True)
 t+=f'Copy `{oldfile}` to `{name}.ASM`. '
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
  t+=f'Run `CHECK ASMKEEP`, enter `{name}` at `Source name:`, and require `OK {case["binary_bytes"]:05} bytes` and PASS. This uses the preceding published ASM86, not the new checkpoint. It creates {name}.COM.\n\n'
 else:
  t+=fence('dos',f'COPY {name}.ASM SOURCE.ASM\nCHECK ASMA0')+f'Require `OK RESULT.COM {case["binary_bytes"]:05} bytes` and PASS. Preserve this executable before using its fixed output name:\n\n'+fence('dos',f'COPY RESULT.COM {name}.COM')
 t+=f'VIEW.BAS must report {name}.COM length {case["binary_bytes"]} bytes. Keep that executable and source together.\n\n## Acceptance check\n\n'
 if case.get('fixture_ref'):
  alias=case['fixture_ref'];t+=fence('dos',f'COPY {name}.ASM {alias}\nCOPY {name}.COM {Path(alias).stem}.COM\nCOPY {alias} SOURCE.ASM')
 else:
  t+=f'Create T{n:02}.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:\n\n'+fence('asm' if n not in range(3,7) else 'text',case['fixture'].replace('\r\n','\n'))+fence('dos',f'COPY T{n:02}.ASM SOURCE.ASM')
 t+=fence('dos',f'CHECK {name}')+'Require:\n\n'+fence('text',case.get('prefix','').replace('\r\n','\n')+f'OK {case.get("output_file","RESULT.COM")} {case["target_bytes"]:05} bytes\nPASS')
 target=case.get('output_file','RESULT.COM');shown=case['target_hex'].split()[:32]
 t+=f'In VIEW.BAS, inspect {target}. Require length **{case["target_bytes"]} bytes** and '+('these complete contents' if case['target_bytes']<=32 else 'these first thirty-two bytes')+':\n\n'+fence('text',' '.join(shown))
 if case.get('self_build'):
  alias='ASMA0' if n==12 else 'ASM86A'
  t+='Compare the first self-produced executable with the preserved original, then use that new generation to assemble the same source once more:\n\n'+fence('dos',f'ECHO N>NO.TXT\nCOMP {alias}.COM RESULT.COM <NO.TXT\nCOPY RESULT.COM GEN1.COM\nCHECK GEN1\nCOMP {alias}.COM RESULT.COM <NO.TXT')
  t+=f'Both COMP comparisons must report no differences. GEN1 must report `OK RESULT.COM {case["binary_bytes"]:05} bytes` and PASS. COMP may ask whether to compare more files; NO.TXT answers N. Keep the original {alias}.COM separately.\n\n'
  if n==12:t+='Continue with the separate [ASM86A collection](../../asm86a/index.html). For its construction builds, ASMA0.COM is the preceding builder. ASMKEEP.COM remains the original ASM86. Their filename interfaces differ; do not overwrite one with the other.\n\n'
  else:t+=fence('dos','COPY ASM86A.COM ASMAKEEP.COM')+'ASMAKEEP.COM is the preserved fixed-file assembler. ASMKEEP.COM still names the original prompted ASM86.\n\n'
 else:t+='The byte inspection is the stopping check for this encoding exercise. Keep the result as data.\n\n'
 t+='## A rejection check\n\n';bad=case['bad']
 if n in [3,4,5]:t+='After inspecting the successful copy, delete ASMA.TMP. It belongs to this copy exercise.\n\n'
 if bad['kind']=='source':
  t+=f'Create X{n:02}.ASM with this separate source:\n\n'+fence('asm',bad['text'])+fence('dos',f'COPY X{n:02}.ASM SOURCE.ASM\nCHECK {name}')
 elif bad['kind']=='missing':t+=fence('dos',f'REN SOURCE.ASM HOLD.ASM\nCHECK {name}')+'Choose an unused HOLD.ASM name before renaming. Restore HOLD.ASM to SOURCE.ASM afterward.\n\n'
 else:t+=fence('dos',f'ECHO RECOVERY>ASMA.TMP\nCHECK {name}')+'TYPE ASMA.TMP afterward: its RECOVERY text must be unchanged. After inspection, delete this deliberately created test file.\n\n'
 t+='Require:\n\n'+fence('text',case.get('prefix','').replace('\r\n','\n')+f'ERROR {bad["line"]:0{10 if n>=19 else 5}} CODE {bad["code"]}\nFAIL')
 if n==3:t+='This early writer creates an empty ASMA.TMP before discovering the missing source. Inspect it and delete it before another run. RESULT.COM must be unchanged.\n\n'
 elif n in [4,5]:t+='The pre-existing RESULT.COM must remain unchanged. A missing-source failure must remove only the temporary file this run owned.\n\n'
 else:t+='The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.\n\n'
 if n in [9,17]:
  limit=2048 if n==9 else 8192
  t+='## Fill the symbol table\n\nEnter SYMS.BAS as a source-text exercise:\n\n'+fence('basic',(W/'SYMS.BAS').read_text().replace('10 N=8192',f'10 N={limit}'))
  t+=f'Run GWBASIC SYMS.BAS, require SOURCE.ASM READY, and use SYSTEM to return to DOS. BASIC closes the text file with its normal source Control-Z marker. Run CHECK {name}. Require `OK RESULT.COM 00004 bytes` and PASS. VIEW.BAS must show `00 01 00 01`: all definitions have value 0100H because none emits bytes. This file is data, not an executable.\n\n'
  t+=f'Keep a copy of that result. Change BASIC line 10 to `10 N={limit+1}` and RUN again. CHECK {name} must report `ERROR {limit+1:05} CODE 5` and FAIL, preserving the four-byte result. Restore the stated accepted N before another run. The BASIC program creates assembly source, never executable bytes.\n\n'
 if n==19:
  t+='## A long source, a small result\n\nEnter LONGSRC.BAS:\n\n'+fence('basic',(W/'LONGSRC.BAS').read_text())
  t+='Run it in BASIC, require SOURCE.ASM READY, and return to DOS with SYSTEM. Its closed text file includes BASIC\'s ordinary source Control-Z. CHECK A19 must report `OK RESULT.COM 00001 bytes` and PASS. VIEW.BAS must show exactly `01`. The comments exceed a word-sized physical-line count while the output stays small; do not execute this data.\n\nChange BASIC line 50 to `50 PRINT #1,"UNKNOWN"`, RUN again, and return to DOS. CHECK A19 must report `ERROR 0000065537 CODE 1` and FAIL. The one-byte accepted RESULT.COM must remain unchanged. Restore the original line 50 before another run.\n\n'
 if n==23:
  t+='## Reach the image boundary\n\nMake LIMIT.ASM containing `RESB 61184`. Copy it to SOURCE.ASM and run CHECK A23. Require `OK RESULT.COM 61184 bytes` and PASS. VIEW.BAS must show length 61184 and zero bytes. This is storage data, never a runnable program. Preserve it; change the count to 61185 and repeat. Require `ERROR 0000000001 CODE 5` and FAIL, with the previous result unchanged. The target limit is independent of the assembler\'s output-block size.\n\n'
 t+='An unexpected PASS fails this rejection test.\n\n## If the result differs\n\n'
 if n<13:t+='Check the fixed name bytes, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.\n'
 elif n<20:t+='Check ES at helper exits, the saved page segment and offset, record padding, and the complete spelling comparison. Check carry after every DOS memory call. A successful allocation does not initialize its contents.\n'
 elif n<25:t+='Check saved expression values across EMIT, the unresolved-reference flag, and fixed statement lengths in both passes. Quoted text bypasses mnemonic folding. A reserve count must be checked before multiplication or output.\n'
 else:t+='Check descriptor width, segment selection, ModR/M bits, displacement order, and registers changed by EMIT. Use the printed bytes to distinguish a parser mistake from an encoding mistake. Keep the branch size the same in both passes.\n'
 write_page((C/page),t);patches.append(dict(number=n,chapter=chapter,collection=collection,page=page,base=oldfile,changes=changes));previous=lines
(Q/'article-patches.json').write_text(json.dumps(patches,indent=2)+'\n')
# Whole-program examples and their measured rejection edits.
t=front('31 · Complete assembly programs',31,'Strings, a stack frame, a distant conditional, and repeated byte movement.','ASM86A.ZIP')
t+='Use the completed ASMAKEEP.COM. For each NAME.ASM below, copy it to SOURCE.ASM and run CHECK ASMAKEEP. Require OK and PASS before copying RESULT.COM to NAME.COM. Inspect it with VIEW.BAS before running CHECK NAME.\n\n'
notes={'HELLO':'DOS function 40H writes a counted string. Both carry and the returned count are checked. Quoted data preserves the mixed case; CR and LF are explicit bytes.', 'FRAME':'CALL pushes the return address; PUSH BP saves the caller frame. BP+4 addresses the word argument. BP-2 is a local word after SUB SP,2. Restoring SP and BP precedes RET 2, which releases the argument. BP-based memory defaults to SS.', 'BRIDGE':'The nonzero word takes JNE NEAR across a zero-filled region. The opposite short branch skips E9 and its word displacement when the condition is false. The intervening bytes are never executed.', 'COPYTEXT':'A COM program begins with DS and ES selecting the program segment. CLD makes movement advance. REP MOVSB copies two bytes, then the output loop prints the copy. REP consumes CX; the output loop loads its own count.'}
for r in examples:
 name=r['name'];t+='## '+name+'\n\n'+fence('asm',(W/(name+'.ASM')).read_text())+notes[name]+'\n\n'
 t+=f'Require `OK RESULT.COM {r["binary_bytes"]:05} bytes` and PASS. VIEW.BAS must report length {r["binary_bytes"]} and these first thirty-two bytes:\n\n'+fence('text',r['hex'])
 t+=f'After saving RESULT.COM as {name}.COM, CHECK {name} displays '+json.dumps(r['output'])+' and reports PASS. Here `\\r\\n` means carriage return followed by line feed.\n\n'
 t+='For a separate rejection, copy the source to BAD.ASM. Replace `'+r['bad_before']+'` with `'+r['bad_after']+'`. Copy BAD.ASM to SOURCE.ASM and run CHECK ASMAKEEP. Require '+f'`ERROR {r["bad_line"]:010} CODE {r["bad_code"]}` and FAIL. The accepted RESULT.COM must remain unchanged; an unexpected PASS fails the check. Restore the accepted source before rebuilding.\n\n'
write_page((C/'43-programs.md'),t)
print('Rendered 12 ASMA0 and 28 ASM86A checkpoints and the complete ASM86A programs.')
