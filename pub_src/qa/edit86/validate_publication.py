"""Reconstruct the printed editor/service edits and check the source-only archive."""
from pathlib import Path
import json,re,zipfile
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/edit86';Q=ROOT/'qa/edit86';C=ROOT/'site/content/bootstrap/edit86';D=ROOT/'site/downloads/edit86'
cases=json.loads((Q/'checkpoints.json').read_text());patches=json.loads((Q/'article-patches.json').read_text());assert len(cases)==len(patches)==20
for c,s in zip(cases,patches):
 n=c['number'];text=(C/s['page']).read_text();base=[]
 if s['base']:base=((ROOT/'workbench/toolchain' if n<3 else W)/s['base']).read_text().splitlines()
 sections=re.split(r'### Edit \d+\n\n',text)[1:]
 if s['base']:assert len(sections)==len(s['changes'])
 for index,e in enumerate(s['changes']):
  a,b=e['a1'],e['a2'];assert base[a:b]==e['old'],(n,'old source')
  if s['base']:
   blocks=re.findall('```'+s['kind']+r'\n(.*?)\n```',sections[index].split('\n## ',1)[0],re.S)
   expected=['\n'.join(e[k]).rstrip('\n') for k in ['context','old','new','after'] if e[k]]
   assert blocks==expected,(n,'printed edit')
  else:assert '\n'.join(e['new']) in text
  base[a:b]=e['new']
 assert base==(W/s['source']).read_text().splitlines(),(n,'reconstruction')
 assert c['binary_hex'] in text and f'{c["binary_bytes"]:05} bytes' in text
 if c.get('probe'):assert (W/c['probe']).read_text().rstrip() in text
 if n>=10:assert (W/c['fixture']).read_text().rstrip() in text
assert (W/'E20.RIL').read_bytes()==(W/'EDIT86.RIL').read_bytes()
for name in ['P01.RIL','P01.IR','Q01.RIL']:
 assert (W/name).read_text().rstrip() in (C/patches[0]['page']).read_text()
for name in ['P02.RIL','Q02.IR']:assert (W/name).read_text().rstrip() in (C/patches[1]['page']).read_text()
assert (W/'EDITRT.ASM').read_bytes()==(W/'S07.ASM').read_bytes()
files=json.loads((Q/'package-files.json').read_text());assert len(files)==len(set(files))
with zipfile.ZipFile(D/'EDIT86.ZIP') as z:
 assert z.namelist()==files
 for name in files:
  assert re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}',name) and not name.endswith(('.COM','.EXE'))
  raw=(W/name).read_bytes();raw.decode('ascii');assert b'\n' not in raw.replace(b'\r\n',b'')
  assert raw==z.read(name)==(D/name).read_bytes(),name
for p in C.glob('*.md'):
 text=p.read_text();assert not re.search(r'\b\d+ (?:required )?(?:BASIC |source )?lines?\b',text,re.I),p
print('PASS EDIT86: twenty exact service/editor constructions and '+str(len(files))+' ASCII/CRLF/8.3 source-only archive members')
