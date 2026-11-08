"""Lay out the authored explanations and exact source edits for publication."""
from publication_names import write_page
from pathlib import Path
from difflib import SequenceMatcher
import json,re,tomllib
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'workbench/asm0';CONTENT=ROOT/'site/content/bootstrap/asm0'
CASES=json.loads((ROOT/'qa/asm0/checkpoints.json').read_text())
def fence(kind,text,keep=False):return '```'+kind+'\n'+(text if keep else text.rstrip('\n'))+'\n```\n\n'
def slug(title):return re.sub('[^a-z0-9]+','-',title.lower()).strip('-')
def front(title,weight,description,download,cartoon=None):
 s='+++\n'+f'title = {json.dumps(title)}\nweight = {weight}\ndescription = {json.dumps(description)}\ndownload = "{download}"\n'
 if cartoon:s+=f'cartoon = "{cartoon}"\n'
 return s+'+++\n\n'
def view(name,raw):
 return (f'Inspect `{name}.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `{name}.COM`, and require a length of **{len(raw)} bytes** with these hexadecimal bytes:\n\n'
         +fence('text',' '.join(f'{b:02X}' for b in raw))+'Use `SYSTEM` to return to DOS.\n\n')
# Keep earlier construction addresses as aliases when removing a whole lesson.
oldpages={}
for p in CONTENT.glob('*.md'):
 if not re.match(r'^\d\d-',p.name):continue
 meta=tomllib.loads(p.read_text().split('+++')[1])
 if re.fullmatch(r'AS\d\d\.ASM',meta.get('download','')):
  key=p.stem[3:];key='opening-and-closing-a-file' if key=='choosing-the-source-name' else key
  oldpages.setdefault(key,[]).extend(['/bootstrap/asm86/'+p.stem+'/']+meta.get('aliases',[]))
  p.unlink()
previous=[];patches=[]
for case in CASES:
 n=case['number'];name=f'AS{n:02}';test=f'T{n:02}';source=(WORK/case['source']).read_text();lines=source.splitlines()
 text=front(f'{n:02} · '+case['title'],n,case['description'],case['source'],case['cartoon'])+case['why']+'\n\n'
 text+='## How it works\n\n'+case['explain']+'\n\n## Source changes\n\n'
 changes=[]
 if n==1:
  text+='Enter this complete source as `AS01.ASM`. The labels and instruction lines are actual source; there are no printed margin numbers.\n\n'+fence('asm',source)
  changes=[dict(tag='insert',a1=0,a2=0,old=[],new=lines,context=[])]
 else:
  text+=f'Copy `AS{n-1:02}.ASM` to `{name}.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.\n\n'
  ops=[op for op in SequenceMatcher(None,previous,lines,autojunk=False).get_opcodes() if op[0]!='equal']
  for i,(tag,a1,a2,b1,b2) in enumerate(reversed(ops),1):
   old=previous[a1:a2];new=lines[b1:b2];context=previous[max(0,a1-3):a1]
   labels=[s for s in previous[:a1] if re.fullmatch('[A-Z][A-Z0-9_]*:',s)]
   location=f'following `{labels[-1]}`' if labels else 'at the beginning'
   text+=f'### Change {i}: {location}\n\n'
   if context:text+='Unchanged code immediately before this edit:\n\n'+fence('asm','\n'.join(context),keep=True)
   if old:text+=f'Remove these exact old lines (physical lines {a1+1}–{a2} of `AS{n-1:02}.ASM`):\n\n'+fence('asm','\n'.join(old),keep=True)
   else:text+=f'Insert after old physical line {a1}, before the following old line.\n\n'
   if new:text+=('Put this source in their place:\n\n' if old else 'Insert this source:\n\n')+fence('asm','\n'.join(new),keep=True)
   else:text+='No replacement lines are needed.\n\n'
   changes.append(dict(tag=tag,a1=a1,a2=a2,old=old,new=new,context=context))
 text+='## Build and stop\n\n'
 text+=f'Use the BASIC assembler prepared in the workbench guide:\n\n'+fence('dos',f'COPY {name}.ASM SOURCE.ASM\nGWBASIC BOOTASM.BAS')
 text+=f'Require `OK RESULT.COM {case["binary_bytes"]} bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM {name}.COM`. Save this source and executable as a working stopping point.\n\n'
 if case['fixture'] is not None:
  text+=f'Use `COPY CON {test}.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:\n\n'+fence('asm',case['fixture'].replace('\r\n','\n'))
 if case['fixture'] is not None:text+=fence('dos',f'COPY {test}.ASM SOURCE.ASM')
 text+=fence('dos','CHECK '+name)
 payload=(f'OK {len(bytes.fromhex(case["image"])):05} bytes\r\n' if case['image'] is not None else case['payload'].replace('{stem}',test))
 console=payload
 text+='The display, apart from DOS command echo and the checker\'s separating blank line, is:\n\n'+fence('text',console.replace('\r\n','\n')+'PASS\n')
 if case['image'] is not None:
  text+=view('RESULT',bytes.fromhex(case['image']))
  if case['executable'] is not None:
   text+=f'`RESULT.COM` is also a complete executable. Preserve it with `COPY RESULT.COM {test}.COM`, then run `CHECK {test}`. It displays `{case["executable"]}` followed by the checker\'s blank line and `PASS`.\n\n'
  else:text+='This file is an encoding or data fixture. **Inspect it; do not execute it.**\n\n'
 if case['bad']:
  bad=case['bad'];x=f'X{n:02}'
  text+='## A rejection check\n\n'
  if bad['kind']=='source':
   text+=f'Enter this separate file as `{x}.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:\n\n'+fence('asm',bad['text'].replace('\r\n','\n'))
   if n==6:text+='The test line contains exactly 121 X characters. Count carefully: 120 is allowed.\n\n'
   text+=fence('dos',f'COPY {x}.ASM SOURCE.ASM\nCHECK {name}')
  elif bad['kind']=='missing':text+=fence('dos',f'REN SOURCE.ASM HOLD.ASM\nCHECK {name}')+'Use an unused HOLD.ASM name and restore it to SOURCE.ASM after the test.\n\n'
  elif bad['kind']=='console':text+=f'Run `CHECK {name}` and enter `{bad["input"]}` as the base name. The dot is forbidden.\n\n'
  elif bad['kind']=='stack':text+='Use the separate SMALL.ASM experiment described above; build it with BOOTASM, then run `CHECK SMALL`.\n\n'
  text+='Require this diagnostic followed by the checker\'s `FAIL`:\n\n'+fence('text',f'ERROR {bad["line"]:05} CODE {bad["code"]}\nFAIL')
  text+='`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.\n\n'
 text+='## If the result differs\n\n'
 if n<4:text+='Check the decimal character bytes, the dollar-sign terminators, and the order of saved registers. A RET must match a CALL; the top-level exit uses DOS function 4CH.\n'
 else:text+='Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.\n'
 filename=f'{n:02}-{slug(case["title"])}.md'
 routes=sorted(set(oldpages.get(slug(case['title']),[]))-{'/bootstrap/asm86/'+Path(filename).stem+'/'})
 if routes:text=text.replace('+++\n\n','aliases = '+json.dumps(routes)+'\n+++\n\n',1)
 write_page(CONTENT/filename,text)
 patches.append(dict(number=n,page=filename,changes=changes))
 previous=lines
(ROOT/'qa/asm0/article-patches.json').write_text(json.dumps(patches,indent=2)+'\n')
print('Prepared 28 construction articles and their exact printed-edit record.')
