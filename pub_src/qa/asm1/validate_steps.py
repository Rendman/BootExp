"""Reconstruct the focused opening sources from the reader's printed edits."""
from pathlib import Path
import json,re,tomllib
ROOT=Path(__file__).resolve().parents[2]

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
  sections=re.split(r'### Change \d+\n\n',text)[1:]
  assert len(sections)==len(stage['changes'])
  for section,e in zip(sections,stage['changes']):
   a,b=e['a1'],e['a2'];assert previous[a:b]==e['old'],(page,'old source')
   blocks=re.findall(r'```asm\n(.*?)\n```',section,re.S)
   expected=['\n'.join(e[k]).rstrip('\n') for k in ['context','old','new','after'] if e[k]]
   assert blocks[:len(expected)]==expected,(page,'printed edit')
   previous[a:b]=e['new']
  assert previous==(ROOT/'workbench/asm1'/stage['source']).read_text().splitlines()
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
 print('PASS six focused ASM1 articles reconstruct exact sources with checkpoint-specific byte/status checks')
 return previous

if __name__=='__main__':reconstruct()
