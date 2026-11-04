"""Lay out authored IR explanations, exact source edits, and native-produced results."""
from pathlib import Path
from difflib import SequenceMatcher
import json,re
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/ir86';Q=ROOT/'qa/ir86';C=ROOT/'site/content/bootstrap/ir86'
C.mkdir(parents=True,exist_ok=True)
cases=json.loads((Q/'checkpoints.json').read_text());examples=json.loads((Q/'examples.json').read_text())
def fence(kind,text,keep=False):return '```'+kind+'\n'+(text if keep else text.rstrip('\n'))+'\n```\n\n'
def slug(s):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
def front(title,weight,desc,download,cartoon=None):
 s='+++\n'+f'title = {json.dumps(title)}\nweight = {weight}\ndescription = {json.dumps(desc)}\ndownload = "{download}"\n'
 if cartoon:s+=f'cartoon = "{cartoon}"\n'
 return s+'+++\n\n'
previous=(ROOT/'workbench/asm86/AS07.ASM').read_text().splitlines();patches=[]
for case in cases:
 n=case['number'];name=f'IR{n:02}';test=f'T{n:02}';bad=f'X{n:02}';oldfile='AS07.ASM' if n==1 else f'IR{n-1:02}.ASM'
 lines=(W/case['source']).read_text().splitlines()
 text=front(f'{n:02} · '+case['title'],n,case['description'],case['source'],case.get('cartoon'))+case['why']+'\n\n## How it works\n\n'+case['explain']+'\n\n## Source changes\n\n'
 text+=f'Copy `{oldfile}` to `{name}.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.\n\n'
 if n==4:text+='LOOK and FINISH are the routines already entered in the ASM86 collection. Their complete added blocks below may be copied from AS09.ASM; compare the printed source when placing them here.\n\n'
 if case['level']==6:text+='VALUE is the unsigned numeric reader from the published ASM86 source, with a nonnumeric token directed to NUMBERBAD. Copy its routine block if convenient, then compare the complete addition below. It accepts numeric tokens only in this translator.\n\n'
 changes=[]
 for i,(tag,a1,a2,b1,b2) in enumerate(reversed([op for op in SequenceMatcher(None,previous,lines,autojunk=False).get_opcodes() if op[0]!='equal']),1):
  old=previous[a1:a2];new=lines[b1:b2];context=previous[max(0,a1-3):a1];labels=[v for v in previous[:a1] if re.fullmatch('[A-Z][A-Z0-9_]*:',v)]
  where=f'following `{labels[-1]}`' if labels else 'at the beginning'
  text+=f'### Change {i}: {where}\n\n'
  if context:text+='Unchanged code immediately before the edit:\n\n'+fence('asm','\n'.join(context),True)
  if old:text+=f'Remove these exact old lines (physical positions {a1+1}–{a2} in `{oldfile}`):\n\n'+fence('asm','\n'.join(old),True)
  else:text+=f'Insert after old physical line {a1}, before the following old line.\n\n'
  if new:text+=('Put this source in their place:\n\n' if old else 'Insert this source:\n\n')+fence('asm','\n'.join(new),True)
  else:text+='No replacement source is needed.\n\n'
  changes.append(dict(a1=a1,a2=a2,old=old,new=new,context=context))
 text+='## Build the checkpoint\n\n'+fence('dos','CHECK ASMKEEP')
 text+=f'Enter `{name}` at ASM86\'s `Source name:` prompt. Require `OK {case["binary_bytes"]:05} bytes` followed by PASS. This builds `{name}.COM` directly with the completed assembler. Save the source and executable before running the test.\n\n'
 text+=f'Create `{test}.IR` with `COPY CON {test}.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.\n\n'+fence('ir',case['fixture'])
 text+=fence('dos','CHECK '+name)+f'Enter `{test}` at `IR source name:`. Apart from DOS echo and the checker\'s separating blank line, require:\n\n'
 if 'console' in case:
  text+=fence('text','IR source name: '+test+'\n'+case['console'].replace('\r\n','\n')+'PASS')
  text+='This diagnostic creates no assembly file. Its displayed text is the test result.\n\n'
 else:
  text+=fence('text',f'IR source name: {test}\nOK {test}.ASM {case["text_bytes"]:05} text bytes\nPASS')
  text+=f'Run `TYPE {test}.ASM`. Its complete text must be:\n\n'+fence('asm',(W/(test+'.ASM')).read_text())
  text+=f'Assemble that generated source with `CHECK ASMKEEP`, entering `{test}`. Require `OK {case["target_bytes"]:05} bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.\n\n'
  text+=f'Run `GWBASIC VIEW.BAS`, enter `{test}.COM`, and require length **{case["target_bytes"]} bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.\n\n'
  values=case['target_hex'].split();text+=fence('text','\n'.join(' '.join(values[i:i+16]) for i in range(0,len(values),16)))
  if case.get('executable',True):
   text+=f'`{test}.COM` is a complete program. Run `CHECK {test}`. '+(f'It displays `{case["output"]}` and then the checker reports PASS.' if case['output'] else 'It returns zero and the checker reports PASS.')+'\n\n'
  else:text+='This target contains data only. **Inspect it; do not execute it.**\n\n'
 text+='## A rejection check\n\n'+f'Enter this separate input as `{bad}.IR` using COPY CON and the same end-of-input keystroke:\n\n'+fence('ir',case['bad']['text'])
 if case['level'] in [1,3]:text+='The unbroken X line has 121 characters, exceeding the 120-character physical input bound.\n\n'
 text+=f'Run `CHECK {name}` and enter `{bad}`. Require this diagnostic and FAIL:\n\n'+fence('text',f'IR ERROR {case["bad"]["line"]:05} CODE {case["bad"]["code"]}\nFAIL')
 text+='An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.\n\n## If the result differs\n\n'
 if n<=3:text+='Check the .IR extension bytes, zero and dollar-sign terminators, and source-cursor saves. A file error is different from end of file; NEXTBYTE returns an explicit count.\n'
 elif case['level']<10:text+='Check the record stride and count, the saved template pointer, and each substitution buffer. The name and numeric token must survive FINISH. Compare the generated assembly before asking ASM86 to assemble it.\n'
 elif case['level']<19:text+='Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.\n'
 else:text+='Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. A DOS carry branch must immediately follow DOS apart from empty or comment lines.\n'
 page=f'{n:02}-{slug(case["title"])}.md';(C/page).write_text(text)
 patches.append(dict(number=n,page=page,base=oldfile,changes=changes));previous=lines
(Q/'article-patches.json').write_text(json.dumps(patches,indent=2)+'\n')

# The example sources were entered independently and executed by test_programs.py.
text=front('Three complete programs',29,'Console output, a procedure-driven counter, and a byte-pointer loop.','IR86.ZIP')
text+='These complete programs use the finished IR86 and ASM86. Save each under its indicated .IR name. Run `CHECK IRKEEP` and enter its base name; require the stated text-byte count and PASS. Then run `CHECK ASMKEEP` with the same base name and require the machine-byte count and PASS. Only then execute the new program.\n\n'
explanations={
'HELLO':('HELLO: two console characters','TODX supplies each character code to DOS function 02H. LIT 200H sets AH to two; DOS displays DL. The second character is prepared after the first DOS call because result registers may have changed. HALT returns zero.','Copy HELLO.IR to BADHELLO.IR and change its first TODX to TODX EXTRA. Translate BADHELLO with CHECK IRKEEP. Require IR ERROR 00003 CODE 1 and FAIL.'),
'COUNT':('COUNT: a procedure and an unsigned loop','DIGIT is named word storage. CALL passes its value in AX to PUTCHAR, whose TODX and DOS sequence displays it. After the call, main reloads DIGIT rather than depending on AX. The comparison consumes the saved left word and branches while the updated digit is less than 51. The expression stack is empty at every label, call, and transfer.','Copy COUNT.IR to BADCOUNT.IR and remove the PUSH immediately before LIT 51. Translate BADCOUNT with CHECK IRKEEP. ULT then has no left operand: require IR ERROR 00013 CODE 4 and FAIL.'),
'BYTES':('BYTES: walk a zero-terminated message','The BYTE declarations are consecutive, and TEXT2 is the zero terminator. POINTER retains an offset. FETCHB converts one byte to an unsigned word; JZ stops at its terminator. Pointer addition happens after DOS and the updated offset is stored before the loop transfers. The word POINTER itself is separate storage, not a second copy of the text.','Copy BYTES.IR to BADBYTES.IR and change TEXT0 to 1TEXT in the first BYTE declaration. Translate BADBYTES with CHECK IRKEEP. Require IR ERROR 00001 CODE 3 and FAIL.')}
for record in examples[:3]:
 name=record['name'];heading,explain,rejection=explanations[name]
 text+='## '+heading+'\n\n'+f'Save `{name}.IR`:\n\n'+fence('ir',(W/(name+'.IR')).read_text())+explain+'\n\n'
 text+=f'Require `OK {name}.ASM {record["text_bytes"]:05} text bytes` from IR86, then `OK {record["binary_bytes"]:05} bytes` from ASM86. `CHECK {name}` displays `{record["output"]}` and reports PASS.\n\n'+rejection+'\n\n'
text+='All three programs require the full-segment entry arrangement documented in the reference. They leave DS, ES, and SS at their DOS entry values and rely only on the accepted 8086/8088 instruction forms. The file-copy program in the pipeline installment is a separate example of handle-based input and output.\n'
(C/'29-programs.md').write_text(text)
print('Prepared IR86 construction articles and complete examples.')
