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
def program_prefix(source,level):
 if level<23:return source
 lines=source.splitlines();end=next(i for i,line in enumerate(lines) if line.startswith('R_') and line.endswith(':'))
 return '\n'.join(lines[:end])
def target_setup(case):
 text=''
 if case.get('stdin'):text+='Create KEY.TXT with `ECHO '+case['stdin']+'>KEY.TXT`. '
 for file,value in case.get('input_files',{}).items():
  if value:text+='Prepare `'+file+'` with `ECHO '+value.strip()+'>'+file+'`. '
 return text
previous=(ROOT/'workbench/asm86/AS07.ASM').read_text().splitlines();patches=[]
for case in cases:
 n=case['number'];name=f'IR{n:02}';test=f'T{n:02}';bad=f'X{n:02}';oldfile='AS07.ASM' if n==1 else f'IR{n-1:02}.ASM'
 lines=(W/case['source']).read_text().splitlines()
 text=front(f'{n:02} · '+case['title'],n,case['description'],case['source'],case.get('cartoon'))+case['why']+'\n\n## Operation and backend\n\n'+case['explain']+'\n\n## Source changes\n\n'
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
  text+=f'Run `TYPE {test}.ASM`. '+('The program prefix must be as follows; the backend runtime follows it.\n\n' if case['level']>=23 else 'Its complete text must be:\n\n')+fence('asm',program_prefix((W/(test+'.ASM')).read_text(),case['level']))
  text+=f'Assemble that generated source with `CHECK ASMKEEP`, entering `{test}`. Require `OK {case["target_bytes"]:05} bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.\n\n'
  text+=f'Run `GWBASIC VIEW.BAS`, enter `{test}.COM`, and require length **{case["target_bytes"]} bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.\n\n'
  values=case['target_hex'].split()
  if case['level']>=23:text+='This checkpoint includes the runtime fragments introduced so far. The reference lists the complete final binding. Compare the leading bytes below; the viewer must still report the full file length.\n\n';values=values[:64]
  text+=fence('text','\n'.join(' '.join(values[i:i+16]) for i in range(0,len(values),16)))
  if case.get('executable',True):
   text+=f'`{test}.COM` is a complete program. '+target_setup(case)+f'Run `CHECK {test}'+(' <KEY.TXT' if case.get('stdin') else '')+'`. '+(f'It displays `{case["output"]}` and then the checker reports PASS.' if case['output'] else 'It returns zero and the checker reports PASS.')+'\n\n'
  else:text+='This target contains data only. **Inspect it; do not execute it.**\n\n'
  for file,value in case.get('output_files',{}).items():text+=f'Inspect `{file}` with VIEW.BAS. Require length {len(value.encode())}'+(f' and byte {ord(value):02X}.' if len(value)==1 else '.')+'\n\n'
 text+='## A rejection check\n\n'+f'Enter this separate input as `{bad}.IR` using COPY CON and the same end-of-input keystroke:\n\n'+fence('ir',case['bad']['text'])
 if case['level'] in [1,3]:text+='The unbroken X line has 121 characters, exceeding the 120-character physical input bound.\n\n'
 text+=f'Run `CHECK {name}` and enter `{bad}`. Require this diagnostic and FAIL:\n\n'+fence('text',f'IR ERROR {case["bad"]["line"]:05} CODE {case["bad"]["code"]}\nFAIL')
 text+='An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.\n\n## If the result differs\n\n'
 if n<=3:text+='Check the .IR extension bytes, zero and dollar-sign terminators, and source-cursor saves. A file error is different from end of file; NEXTBYTE returns an explicit count.\n'
 elif case['level']<10:text+='Check the record stride and count, the saved template pointer, and each substitution buffer. The name and numeric token must survive FINISH. Compare the generated assembly before asking ASM86 to assemble it.\n'
 elif case['level']<19:text+='Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.\n'
 else:text+='Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.\n'
 page=case.get('page',f'{n:02}-{slug(case["title"])}.md');(C/page).write_text(text)
 patches.append(dict(number=n,page=page,base=oldfile,changes=changes));previous=lines
(Q/'article-patches.json').write_text(json.dumps(patches,indent=2)+'\n')

# The example sources were entered independently and executed by test_programs.py.
text=front('Complete portable programs',35,'Byte streams, a procedure-driven counter, and pointers to declared storage.','IR86.ZIP')
text+='These complete programs use the finished IR86 and ASM86. Save each under its indicated .IR name. Run `CHECK IRKEEP` and enter its base name; require the stated text-byte count and PASS. Then run `CHECK ASMKEEP` with the same base name and require the machine-byte count and PASS. Only then execute the new program.\n\n'
explanations={
'HELLO':('HELLO: two output bytes','PUTC writes the low byte of virtual A to the output stream. Its result is a count, so each new character is loaded explicitly. HALT returns zero. The IR source contains no physical register or operating-system service number.','Copy HELLO.IR to BADHELLO.IR and change its first PUTC to PUTC EXTRA. Translate BADHELLO with CHECK IRKEEP. Require IR ERROR 00003 CODE 1 and FAIL.'),
'COUNT':('COUNT: a procedure and an unsigned loop','DIGIT is persistent word storage. CALL passes its value in virtual A to PUTCHAR, which uses PUTC. Main reloads DIGIT after the call. ULT consumes the saved left operand and tests the updated value against 51. Every control boundary has an empty expression stack.','Copy COUNT.IR to BADCOUNT.IR and remove the PUSH immediately before LIT 51. Require IR ERROR 00013 CODE 4 and FAIL.'),
'BYTES':('BYTES: walk declared byte storage','The BYTE declarations are consecutive; TEXT2 is the zero terminator. POINTER retains a pointer formed by ADDR. FETCHB returns an unsigned byte value, and JZ stops at zero. Pointer advancement uses a byte offset within this declared sequence. No numeric address is assumed.','Copy BYTES.IR to BADBYTES.IR and change TEXT0 to 1TEXT in its first declaration. Require IR ERROR 00001 CODE 3 and FAIL.'),
'ECHOIR':('ECHOIR: copy an input byte stream','GETC returns each byte or the distinct EOF value 65535. CHARACTER saves the result before STATUS is read. The equality branch consumes its left value, so CHARACTER is reloaded before PUTC. Both services are checked. A byte value 255 is data, not EOF.','Copy ECHOIR.IR to BADECHOIR.IR and change GETC to GETC EXTRA. Require IR ERROR 00004 CODE 1 and FAIL.')}
for record in [r for r in examples if r['name']!='COPYFILE']:
 name=record['name'];heading,explain,rejection=explanations[name]
 text+='## '+heading+'\n\n'+f'Save `{name}.IR`:\n\n'+fence('ir',(W/(name+'.IR')).read_text())+explain+'\n\n'
 if name=='ECHOIR':text+='Create KEY.TXT with `ECHO IR86 echo.>KEY.TXT`, then run `CHECK ECHOIR <KEY.TXT`. It copies the line including its CR/LF.\n\n'
 command='CHECK '+name+(' <KEY.TXT' if name=='ECHOIR' else '')
 text+=f'Require `OK {name}.ASM {record["text_bytes"]:05} text bytes` from IR86, then `OK {record["binary_bytes"]:05} bytes` from ASM86. `'+command+'` displays `'+record['output'].rstrip()+'` and reports PASS.\n\n'+rejection+'\n\n'
text+='These sources use only the virtual machine and portable runtime contract. The 8086/DOS binding has the environment requirements documented separately in the reference. The pipeline installment supplies a complete file-copy example.\n'
(C/'29-programs.md').write_text(text)
print('Prepared IR86 construction articles and complete examples.')
