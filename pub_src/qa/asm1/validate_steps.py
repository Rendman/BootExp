"""Reconstruct the focused opening sources from the reader's printed edits."""
from pathlib import Path
import json,re,tomllib
ROOT=Path(__file__).resolve().parents[2]

def code(lines):
 return [line.strip() for line in lines if line.strip() and not line.lstrip().startswith(';')]

def apply_label_edits(program,stage,text):
 """Follow the printed label and locator, without using numeric edit indices."""
 program=code(program)
 sections=re.split(r'### Change \d+[^\n]*\n\n',text)[1:]
 assert len(sections)==len(stage['changes']),(stage['page'],'edit count')
 for section,e in zip(sections,stage['changes']):
  label=e['anchor']+':'
  assert f'Find the unique label `{label}`' in section,(stage['page'],'missing label instruction')
  assert program.count(label)==1,(stage['page'],'ambiguous label',label)
  blocks=re.findall(r'```asm\n(.*?)\n```',section,re.S)
  keys=(['landmark'] if e['placement']=='before_label' else ['context'])+['old','new']
  keys=[key for key in keys if e[key]]
  expected=['\n'.join(e[key]) for key in keys]
  assert blocks[:len(expected)]==expected,(stage['page'],'printed edit differs')
  printed={key:code(block.splitlines()) for key,block in zip(keys,blocks)}
  at=program.index(label)
  if e['placement']=='after_context':
   context=printed['context']
   assert context[0]==label and program[at:at+len(context)]==context,(stage['page'],'locator differs')
   at+=len(context)
  elif e['placement']=='before_label':assert printed['landmark']==[label]
  else:assert e['placement']=='at_label'
  old=printed.get('old',[]);new=printed.get('new',[])
  assert program[at:at+len(old)]==old,(stage['page'],'old source differs')
  if e.get('end_anchor'):assert program[at+len(old)]==e['end_anchor']+':'
  program[at:at+len(old)]=new
 # The editing instructions must be usable without margin or physical lines.
 editing=text.split('## Enter the source\n\n')[1].split('## Build')[0]
 assert not re.search(r'physical (?:positions?|lines?)|old physical|old line \d|positions \d',editing,re.I)
 return program

def reconstruct():
 previous=(ROOT/'workbench/asm0/ASM86.ASM').read_text().splitlines()
 facts=json.loads((ROOT/'qa/asm1/intro.json').read_text())
 patches=json.loads((ROOT/'qa/asm1/intro-patches.json').read_text())
 assert len(facts)==len(patches)==6
 for index,(s,stage) in enumerate(zip(facts,patches),1):
  page=ROOT/'site/content/bootstrap/asm1'/stage['page'];text=page.read_text()
  meta=tomllib.loads(text.split('+++')[1])
  assert meta['weight']==index and meta['title'].startswith(f'{index:02} ')
  assert meta['download']==stage['source']==s['id']+'.ASM'
  # Extra notes and spacing deliberately change physical positions, as they
  # may in WordPerfect. Label-based instructions must still resolve exactly.
  previous=['; Workbench note','']+previous
  previous=apply_label_edits(previous,stage,text)
  assert previous==code((ROOT/'workbench/asm1'/stage['source']).read_text().splitlines())
  assert f'OK {s["binary_bytes"]:05} bytes' in text and 'VIEW.BAS' in text
  if s['mode']=='probe':
   assert 'CHECK A01C in.asm out.com' in text and 'ERROR 00000 CODE 9' in text
  else:
   assert s['fixture'].rstrip('\n') in re.findall(r'```asm\n(.*?)\n```',text,re.S)
   assert s['target_hex'] in text
  if s['mode']=='fixed':
   assert f'COPY T{s["id"][1:]}.ASM SOURCE.ASM\nCHECK {s["id"]}\n' in text
  if s['id']=='A01F':
   for key in ['open','close']:assert s[key+'_hex'] in text and f'{s[key+"_offset"]:04X}H' in text
 print('PASS six ASM1 opening articles reconstruct from unique labels despite different comments and spacing')
 return (ROOT/'workbench/asm1'/patches[-1]['source']).read_text().splitlines()

if __name__=='__main__':reconstruct()
