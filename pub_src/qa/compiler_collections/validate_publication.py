"""Verify separate RB/RC publications and their unchanged bootstrap handoffs."""
from pathlib import Path
import json,re,tomllib,zipfile
ROOT=Path(__file__).resolve().parents[2];C=ROOT/'site/content/bootstrap';Q=ROOT/'qa/compiler_collections';SOURCE=ROOT/'workbench/toolchain'
for group,prefix,total,family,canonical in [('rb','RB',47,'rill-seed-series','RILLBOOT.IR'),('rc','RC',43,'rill-self-series','RILL.RIL')]:
 W=ROOT/'workbench'/group;D=ROOT/'site/static/downloads'/group;files=json.loads((Q/(group+'-files.json')).read_text())
 assert len(files)==len(set(files))
 with zipfile.ZipFile(D/(prefix+'.ZIP')) as z:
  assert z.namelist()==files
  for name in files:
   assert re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}',name) and not name.endswith(('.COM','.EXE')),name
   raw=(W/name).read_bytes();raw.decode('ascii');assert b'\n' not in raw.replace(b'\r\n',b'')
   assert raw==z.read(name)==(D/name).read_bytes(),name
   if name!='README.TXT':assert raw==(SOURCE/name).read_bytes(),name
 assert (W/canonical).read_bytes()==(W/(f'{prefix}{total:02}'+Path(canonical).suffix)).read_bytes()
 assert all(not n.startswith('RC' if group=='rb' else 'RB') for n in files)
 for case in json.loads((ROOT/'qa/toolchain'/(family+'.json')).read_text()):
  n=case['number'];p=next(p for p in (C/group).glob(f'*-{group}-*.md') if tomllib.loads(p.read_text().split('+++')[1])['download']==case['source'])
  meta=tomllib.loads(p.read_text().split('+++')[1]);assert meta['weight']==n
  assert meta['aliases']==[f'/bootstrap/rill/{p.stem}/']
  assert not (C/'rill'/p.name).exists()
  assert (ROOT/'site/static/downloads/toolchain'/case['source']).read_bytes()==(W/case['source']).read_bytes()
 assert len(json.loads((ROOT/'qa/toolchain'/(family+'.json')).read_text()))==total
reference=lambda p:p.read_text().split('## Program structure',1)[1]
assert reference(C/'rb/132-the-rill-systems-language.md')==reference(C/'rc/044-reference.md')
assert len(list((C/'rill').glob('*.md')))==34
assert len(list((C/'rb').glob('*.md')))==58
assert len(list((C/'rc').glob('*.md')))==48
text=(C/'rc/048-programs.md').read_text();blocks=re.findall(r'```rill\n(.*?)\n```',text,re.S)
for i,c in enumerate(json.loads((Q/'rc-examples.json').read_text())):
 assert blocks[2*i]+'\n'==(ROOT/'workbench/rc'/(c['name']+'.RIL')).read_text()
 assert blocks[2*i+1]==c['bad']
 assert f'{c["binary_bytes"]:05} bytes' in text and c['error'] in text
assert 'download = "RILL0.IR"' in (C/'rill/_index.md').read_text()
assert 'RC01.RIL starts a new source file' in (C/'rc/000-workbench.md').read_text()
assert 'RILLBOOT.IR' in (C/'rb/033-the-systems-workbench.md').read_text()
print('PASS RB/RC: 47 seed and 43 RILL compiler articles, distinct workbenches/references/examples/archives, exact canonical sources and unchanged filenames, matching language contracts')
