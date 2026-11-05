"""Render exact IR edits and native-measured RILL checkpoint results into the manuscript."""
from pathlib import Path
from difflib import SequenceMatcher
import json,re
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/rill';Q=ROOT/'qa/rill';C=ROOT/'site/content/bootstrap/rill'
cases=json.loads((Q/'checkpoints.json').read_text());examples=json.loads((Q/'examples.json').read_text())
def fence(kind,text):return '```'+kind+'\n'+text.rstrip('\n')+'\n```\n\n'
def slug(s):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
def front(title,weight,description,download,cartoon=None):
 t='+++\n'+f'title = {json.dumps(title)}\nweight = {weight}\ndescription = {json.dumps(description)}\ndownload = "{download}"\n'
 if cartoon:t+=f'cartoon = "{cartoon}"\n'
 return t+'+++\n\n'
previous=[];patches=[]
for case in cases:
 n=case['number'];name=f'R{n:02}';oldfile=f'R{n-1:02}.IR';lines=(W/case['source']).read_text().splitlines()
 page=f'{n:02}-{slug(case["title"])}.md'
 t=front(f'{n:02} · '+case['title'],n,case['description'],case['source'],case.get('cartoon'))+case['why']+'\n\n## The working parts\n\n'+case['explain']+'\n\n## Enter the source\n\n'
 if n==1:t+='Create R01.IR as plain IR text. This is the complete new source:\n\n'+fence('ir','\n'.join(lines))
 else:t+=f'Copy `{oldfile}` to `{name}.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.\n\n'
 changes=[]
 for i,(_,a,b,c,d) in enumerate(reversed([o for o in SequenceMatcher(None,previous,lines,autojunk=False).get_opcodes() if o[0]!='equal']),1):
  before=previous[max(0,a-3):a];old=previous[a:b];new=lines[c:d];labels=[v for v in previous[:a] if v.startswith('LABEL ')]
  if n>1:
   t+=f'### Change {i}: '+('following `'+labels[-1]+'`' if labels else 'in the declarations')+'\n\n'
   if before:t+='Unchanged source immediately before the edit:\n\n'+fence('ir','\n'.join(before))
   if old:t+=f'Remove these exact old lines (physical positions {a+1}–{b} in `{oldfile}`):\n\n'+fence('ir','\n'.join(old))
   else:t+=f'Insert after old physical line {a}, before the following old line.\n\n'
   if new:t+=('Put this source in their place:\n\n' if old else 'Insert this source:\n\n')+fence('ir','\n'.join(new))
   else:t+='No replacement source is needed.\n\n'
  changes.append(dict(a1=a,a2=b,old=old,new=new,context=before))
 t+='## Build the stopping point\n\n'+fence('dos','CHECK IRKEEP')
 t+=f'Enter `{name}` at `IR source name:`. Require `OK {name}.ASM {case["assembly_bytes"]:05} text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `{name}` at `Source name:`, and require `OK {case["binary_bytes"]:05} bytes` and PASS. Save the source and executable before testing.\n\n'
 t+='## Acceptance check\n\n'
 if n>=6 and n!=7:
  if case['fixture']:
   t+=f'Create `T{n:02}.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:\n\n'+fence('rill' if n>=13 else 'text',case['fixture'].replace('\r\n','\n'))
  else:t+=f'Create an empty `T{n:02}.RIL` using `COPY CON T{n:02}.RIL` and Ctrl-Z then Enter. VIEW.BAS must report length zero.\n\n'
  if case.get('stdin'):t+=f'Run `CHECK {name} <T{n:02}.RIL`. This is diagnostic byte input, not a RILL program.\n\n'
  else:t+=f'Run `COPY T{n:02}.RIL SOURCE.RIL`, then `CHECK {name}`.\n\n'
 else:t+=f'Run `CHECK {name}`. This checkpoint does not read SOURCE.RIL.\n\n'
 if n<15:
  t+='Apart from DOS command echo and the checker\'s separating blank line, require:\n\n'+fence('text',case['output'].replace('\r\n','\n')+'PASS\n')
  t+='This is a diagnostic stopping point. It does not create RESULT.IR.\n\n'
 else:
  t+='Require:\n\n'+fence('text',f'OK RESULT.IR {case["text_bytes"]:05}\nPASS')
  t+='Run `TYPE RESULT.IR`. Its complete contents must be:\n\n'+fence('ir',(W/f'T{n:02}.IR').read_text())
  t+=f'Copy RESULT.IR to T{n:02}.IR. Translate it with CHECK IRKEEP, entering T{n:02}; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK {case["target_bytes"]:05} bytes` and PASS.\n\n'
  t+=f'VIEW.BAS must report T{n:02}.COM length **{case["target_bytes"]} bytes**. These are its first sixteen bytes, not its complete contents:\n\n'+fence('text',' '.join(case['target_hex'].split()[:16]))
  if case.get('program_stdin'):t+=f'Create KEY.TXT with `ECHO {case["program_stdin"]}>KEY.TXT`. '
  t+=f'Run `CHECK T{n:02}'+(' <KEY.TXT' if case.get('program_stdin') else '')+'`. '
  if case.get('program_exit',0):t+=f'It deliberately returns status {case["program_exit"]}; the checker must report FAIL. This is the intended executable result.\n\n'
  elif case['program_output']:t+='It displays `'+case['program_output']+'` and the checker reports PASS.\n\n'
  else:t+='It returns zero and the checker reports PASS.\n\n'
 t+='## A rejection check\n\n';bad=case['bad']
 if bad['kind']=='ir':
  t+='The program has no source-language reader at this stopping point. Check an IR transcription error independently: create BAD.IR with this text:\n\n'+fence('ir',bad['source'])
  t+='Run CHECK IRKEEP and enter BAD. Require:\n\n'+fence('text',f'IR ERROR {bad["line"]:05} CODE {bad["code"]}\nFAIL')
  t+='The unwanted operand must prevent BAD.ASM from being created. If an older BAD.ASM exists, it must remain unchanged.\n\n'
 elif bad['kind']=='missing':
  t+=f'Rename SOURCE.RIL to HOLD.RIL, run CHECK {name}, and require:\n\n'+fence('text',f'ERROR {bad["line"]:05} CODE {bad["code"]:05}\nFAIL')
  t+='Restore HOLD.RIL to SOURCE.RIL afterward. A missing source is not successful empty input.\n\n'
 else:
  if n==9:t+='Create X09.RIL with COPY CON: press Ctrl-A once, then Ctrl-Z and Enter. VIEW.BAS must show leading byte 01. This deliberately invalid source byte is not a printed RILL token.\n\n'
  else:t+=f'Create X{n:02}.RIL with this separate test:\n\n'+fence('rill' if n>=13 else 'text',bad['source'].replace('\r\n','\n'))
  if case.get('stdin'):t+=f'Run `CHECK {name} <X{n:02}.RIL`. '
  else:t+=f'Copy X{n:02}.RIL to SOURCE.RIL, then run CHECK {name}. '
  t+='Require:\n\n'+fence('text',f'ERROR {bad["line"]:05} CODE {bad["code"]:05}\nFAIL')
  if n>=15:t+='Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.\n\n'
 t+='An unexpected PASS is a failed rejection test.\n\n## If the result differs\n\n'
 if n<6:t+='Check the IR literal values, operand order, and empty expression boundaries. Translate and assemble afresh; an older COM file can otherwise conceal a source error.\n'
 elif n<13:t+='Check each service STATUS immediately, the current-byte advance, and any shared work cell needed across a call. Compare token values with the printed result before changing the parser.\n'
 elif n<24:t+='Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.\n'
 else:t+='Check the order in which targets enter and leave FRAMES. Compare the false relation and label names in RESULT.IR. A branch must consume its saved expression operand before reaching an IR control boundary.\n'
 (C/page).write_text(t);patches.append(dict(number=n,page=page,base=oldfile if n>1 else None,changes=changes));previous=lines
(Q/'article-patches.json').write_text(json.dumps(patches,indent=2)+'\n')
# A complete pipeline whose counts come from actual native tools.
count=next(r for r in examples if r['name']=='COUNT')
t=front('30 · The complete RILL pipeline',30,'Carry a structured counter through IR and assembly to a working program.','RILL.IR')
t+='The compiler source is IR86, and its result is IR86. Keep both translations visible while making a complete program. Begin with the tested R29.COM and preserve the working compiler:\n\n'+fence('dos','COPY R29.COM RILL.COM\nCOPY RILL.COM RLKEEP.COM')
t+='RILL.COM must have length 5173 bytes in VIEW.BAS. Keep RILL.IR, IRKEEP.COM, ASMKEEP.COM, CHECK.BAT, and their sources.\n\n## Enter a complete program\n\nSave this as COUNT.RIL:\n\n'+fence('rill',(W/'COUNT.RIL').read_text())
t+='x is a mutable unsigned word. The condition is evaluated at the loop entrance on every iteration. Each successful pass prints the low byte of x, then advances x by one. The body has no declarations or hidden parameter frame.\n\n'+fence('dos','COPY COUNT.RIL SOURCE.RIL\nCHECK RLKEEP')
t+=f'Require `OK RESULT.IR {count["text_bytes"]:05}` and PASS. TYPE RESULT.IR must show:\n\n'+fence('ir',(W/'COUNT.IR').read_text())
t+='The WORD declaration precedes MAIN. The condition emits UGE to leave the loop when x is not less than 51. PUSH and ADD implement the update; both loop edges have an empty expression stack. B00001 and B00002 are generated names, not physical addresses.\n\n## Translate and assemble\n\n'+fence('dos','COPY RESULT.IR COUNT.IR\nCHECK IRKEEP')
t+=f'Enter COUNT. Require `OK COUNT.ASM {count["assembly_bytes"]:05} text bytes` and PASS. Run CHECK ASMKEEP, enter COUNT, and require `OK {count["binary_bytes"]:05} bytes` and PASS. VIEW.BAS must report COUNT.COM length {count["binary_bytes"]} bytes. Its first sixteen hexadecimal bytes are:\n\n'+fence('text',(W/'COUNT.COM').read_bytes()[:16].hex(' ').upper())
t+='Only after all three tools succeed, run CHECK COUNT. It displays `012` and reports PASS. The saved IR is sufficient input for another conforming backend; the source program makes no native register or DOS call assumptions.\n\n## Observe a rejected program\n\nCopy COUNT.RIL to BADCOUNT.RIL and remove the semicolon from `x = x + 1;`. Copy BADCOUNT.RIL to SOURCE.RIL and run CHECK RLKEEP. Require ERROR 00006 CODE 00002 and FAIL. The closing brace is the token at which the missing semicolon is detected. TYPE RESULT.IR must still show the accepted counter above.\n\nRestore COUNT.RIL as SOURCE.RIL before another successful build. An unexpected PASS fails the rejection check. If the result differs, inspect RESULT.IR first, then COUNT.ASM; do not execute an older COUNT.COM after any build step fails.\n'
(C/'30-the-complete-pipeline.md').write_text(t)
# Short complete programs, each with a relevant exact rejection.
t=front('Complete RILL programs',32,'Byte output, a mutable counter, unsigned choice, and a checked byte-stream echo.','RILL.ZIP')
t+='These programs use the completed compiler. For each NAME.RIL, copy it to SOURCE.RIL and run CHECK RLKEEP. Require the compiler count and PASS; copy RESULT.IR to NAME.IR. Run CHECK IRKEEP and CHECK ASMKEEP, entering NAME at each prompt, requiring both OK reports and PASS before executing NAME.COM.\n\n'
explain={
'HELLO':('Two output bytes','Each putc statement writes one ASCII byte. There are no string literals, so each character is explicit. The normal end returns zero.','Change its first `putc` to `putcat`. Require ERROR 00002 CODE 00002 and FAIL.'),
'COUNT':('A mutable counter','The declaration reserves x before MAIN. The unsigned condition is false at 51, and addition wraps as a word. The displayed 012 shows three completed iterations.','Remove the declaration of x. Require ERROR 00002 CODE 00004 and FAIL.'),
'CHOICE':('Unsigned choice','The word 65535 is greater than one in unsigned order. The first branch prints U; equality then prints an exclamation mark. There is no implicit signed interpretation.','Change the initializer 65535 to 65536. Require ERROR 00002 CODE 00003 and FAIL.'),
'RLECHO':('A checked byte stream','c saves the input before status() is read. EOF is 65535 with success status; it exits zero. Every ordinary byte, including 255, is written and output status checked. A failed input or output exits one.','Change `getc()` to `getc(1)`. Require ERROR 00004 CODE 00002 and FAIL.')}
for r in examples:
 name=r['name'];heading,description,reject=explain[name]
 t+='## '+name+': '+heading+'\n\nSave '+name+'.RIL:\n\n'+fence('rill',(W/(name+'.RIL')).read_text())+description+'\n\n'
 t+=f'Require compiler `OK RESULT.IR {r["text_bytes"]:05}`, IR86 `OK {name}.ASM {r["assembly_bytes"]:05} text bytes`, and ASM86 `OK {r["binary_bytes"]:05} bytes`, each followed by PASS.\n\n'
 if name=='RLECHO':t+='Create KEY.TXT with `ECHO RILL echo.>KEY.TXT`. Run `CHECK RLECHO <KEY.TXT`; it displays `RILL echo.` with CR/LF and reports PASS. An empty input file produces no text and still reports PASS. The compiler source reader\'s Control-Z convention does not apply to this program\'s byte input.\n\n'
 else:t+='CHECK '+name+' displays `'+r['output']+'` and reports PASS.\n\n'
 t+='For a separate rejection, copy the source to BAD.RIL. '+reject+' Copy that changed file to SOURCE.RIL and run CHECK RLKEEP. An unexpected PASS is a failed rejection. The older RESULT.IR must remain unchanged. Restore the accepted source before building again.\n\n'
(C/'32-programs.md').write_text(t)
print('Rendered RILL construction, pipeline, and complete-program articles.')
