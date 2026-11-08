"""Reconstruct the printed linker and inspect its source-only object collection."""
from pathlib import Path
import json,re,zipfile
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/link86';C=ROOT/'site/content/bootstrap/link86';Q=ROOT/'qa/link86';D=ROOT/'site/downloads/link86'
old=[];cases=json.loads((Q/'checkpoints.json').read_text());patches=json.loads((Q/'article-patches.json').read_text())
assert len(cases)==len(patches)==10
for c,s in zip(cases,patches):
 text=(C/s['page']).read_text();sections=re.split(r'### Edit \d+\n\n',text)[1:]
 if s['base']:assert len(sections)==len(s['changes'])
 for i,e in enumerate(s['changes']):
  a,b=e['a1'],e['a2'];assert old[a:b]==e['old'],(s['page'],'old source')
  if s['base']:
   blocks=re.findall(r'```rill\n(.*?)\n```',sections[i],re.S)
   expected=['\n'.join(e[k]).rstrip('\n') for k in ['context','old','new','after'] if e[k]]
   assert blocks==expected,(s['page'],'printed edits')
  else:assert '\n'.join(e['new']) in text
  old[a:b]=e['new']
 assert old==(W/s['source']).read_text().splitlines(),s['page']
 n=c['number'];assert f'COPY {c["source"]} SOURCE.RIL' in text
 for key,name in [('main',f'M{n:02}.OBJ'),('util',f'U{n:02}.OBJ'),('bad',f'X{n:02}.OBJ')]:
  if c[key] is not None:assert c[key].rstrip('\n') in text and (W/name).read_text()==c[key]
 assert c['binary_hex'] in text and f'{c["binary_bytes"]:05} bytes' in text
 if c['expected'] is not None:assert c['expected'] in text
 if c['error']:assert c['error'].rstrip() in text
assert (W/'LINK86.RIL').read_bytes()==(W/'L10.RIL').read_bytes()
files=json.loads((Q/'package-files.json').read_text())
assert len(files)==len(set(files))
with zipfile.ZipFile(D/'LINK86.ZIP') as z:
 assert z.namelist()==files
 for name in files:
  assert re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}',name) and not name.endswith(('.COM','.EXE'))
  raw=(W/name).read_bytes();raw.decode('ascii');assert b'\n' not in raw.replace(b'\r\n',b'')
  assert raw==z.read(name)==(D/name).read_bytes(),name
print('PASS LINK86: ten exact printed constructions, object fixtures/results, and '+str(len(files))+' ASCII/CRLF/8.3 source-only archive members')
