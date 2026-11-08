"""Check canonical names, exact source aliases, and artifact-based reader tests."""
from pathlib import Path
import json,re,sys,tomllib,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from publication_names import SERIES,names,filename,reader_text
C=ROOT/'site/content/bootstrap';D=ROOT/'site/static/downloads/tools'
manifest=json.loads((ROOT/'qa/reader-packages.json').read_text());count=0
assert set(manifest)=={'bootasm','asm0','asm1','asm86','ir86','rill0','rillboot','rill','toolchain','link86'}
for group,m in manifest.items():
 with zipfile.ZipFile(D/group/m['archive']) as z,zipfile.ZipFile(ROOT/'site/static/downloads'/m['legacy_group']/m['legacy_archive']) as old:
  assert z.namelist()==list(m['files'])
  for new,original in m['files'].items():
   assert filename(original)==new and re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}',new)
   assert not new.endswith(('.COM','.EXE'))
   expected=old.read(original)
   if original in ['README.TXT','TMAKE.BAT']:expected=reader_text(m['legacy_group'],original,expected.decode()).encode()
   assert expected==z.read(new)==(D/group/new).read_bytes(),(group,new)
   expected.decode('ascii');assert b'\n' not in expected.replace(b'\r\n',b''),(group,new)
   count+=1
for group,(tool,title) in SERIES.items():
 meta=tomllib.loads((C/group/'_index.md').read_text().split('+++')[1])
 assert meta['title']==title and meta['tool_id']==tool and meta['collection_key']==group
 assert meta['download_group']=='tools/'+tool.lower()
 assert (D/tool.lower()/meta['download']).exists()
for family,group in [('rill-initial-series','rill'),('rill-seed-series','rb'),('rill-self-series','rc')]:
 cases=json.loads((ROOT/'qa/toolchain'/(family+'.json')).read_text())
 for c in cases:
  page=next(p for p in (C/group).glob('*.md') if tomllib.loads(p.read_text().split('+++')[1]).get('download')==c['source'])
  text=page.read_text();assert 'preceding-language word boundary' not in text and 'Check a representable-word boundary' not in text
  if c.get('check_value') is not None:assert c['console']=='' and 'adds no display routine' in text
  if 'result' in c and not c['complete']:
   raw=c['result'].encode();assert f'length {len(raw)} bytes' in text
   if raw:
    block=re.search(r'(?:The complete bytes must be:|these complete bytes:)\n\n```text\n(.*?)\n```',text,re.S)
    assert block and bytes.fromhex(block[1])==raw,(page,'fragment inspection')
   else:assert 'empty file' in text
  if c.get('accept_exit'):assert c['console']=='ERROR 0000000001 CODE 00002\r\n' and ('FAIL is the intended status' in text or 'the intended result' in text)
batch=(D/'toolchain/TMAKE.BAT').read_text()
for name in re.findall(r'(?m)^COPY (\S+) SOURCE\.',batch):
 if not name.startswith('RESULT.'):assert (D/'toolchain'/name).exists(),name
assert 'COPY ASM86.RIL SOURCE.RIL' in batch
commands=batch.splitlines()
for name,builder in [('RILL','RILLBOOT'),('IR86','R0'),('ASM86','R0')]:
 i=commands.index(f'COPY {name}.RIL SOURCE.RIL >NUL');assert commands[i+1]==builder,(name,'minimum seed handoff')
assert commands.count('RILLBOOT')==1
assert 'COPY RESULT.COM RBOOT.COM >NUL' in commands
assert commands.count('RBOOT')==1
assert commands.count('COPY RILL.RIL SOURCE.RIL >NUL')==4
assert 'RC44' not in batch and 'RSELF' not in batch
print(f'PASS reader publication: {len(manifest)} named series; {count} canonical source members; all compiler stopping checks use natural reports, status assertions or exact file bytes; batch prerequisites resolve')
