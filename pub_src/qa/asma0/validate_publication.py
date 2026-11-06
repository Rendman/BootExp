"""Check the separate seed collection, its source boundary, and independent disk archive."""
from pathlib import Path
import json,re,tomllib,zipfile
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/asma0';C=ROOT/'site/content/bootstrap/asma0';Q=ROOT/'qa/asma0';D=ROOT/'site/static/downloads/asma0'
manifest=json.loads((Q/'package-files.json').read_text())
with zipfile.ZipFile(D/'ASMA0.ZIP') as z:
 assert z.namelist()==manifest
 for name in manifest:
  assert re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}',name),name
  assert not name.endswith(('.COM','.EXE'))
  raw=(W/name).read_bytes();raw.decode('ascii');assert b'\n' not in raw.replace(b'\r\n',b'')
  assert raw==z.read(name)==(D/name).read_bytes(),name
assert (W/'ASMA0.ASM').read_bytes()==(W/'A12.ASM').read_bytes()==(ROOT/'workbench/asm86a/ASMA0.ASM').read_bytes()
for n in range(1,13):
 assert (W/f'A{n:02}.ASM').read_bytes()==(ROOT/f'workbench/asm86a/A{n:02}.ASM').read_bytes()
 p=next(C.glob(f'{n:02}-*.md'));meta=tomllib.loads(p.read_text().split('+++')[1])
 assert meta['weight']==n and meta['title'].startswith(f'{n:02} ')
 assert meta['aliases']==[f'/bootstrap/asm86a/{p.stem}/']
 assert meta['download']==f'A{n:02}.ASM'
 assert (ROOT/'site/static/downloads/asm86a'/f'A{n:02}.ASM').read_bytes()==(W/f'A{n:02}.ASM').read_bytes(),'legacy source link'
text=(C/'14-programs.md').read_text();blocks=re.findall(r'```asm\n(.*?)\n```',text,re.S);examples=json.loads((Q/'examples.json').read_text())
assert len(blocks)==len(examples)==3
for c,b in zip(examples,blocks):
 assert b+'\n'==(W/(c['name']+'.ASM')).read_text()
 assert f'{c["binary_bytes"]:05} bytes' in text
 assert f'ERROR {c["bad_line"]:05} CODE {c["bad_code"]}' in text
assert '10 N=2048' in (W/'SYMS.BAS').read_text()
assert not any(re.fullmatch(r'A(?:1[3-9]|[2-4][0-9])\.ASM',n) for n in manifest)
full=json.loads((ROOT/'qa/asm86a/package-files.json').read_text())
assert 'ASMA0.ASM' in full and 'A12.ASM' in full
assert not any(f'A{n:02}.ASM' in full for n in range(1,12))
assert all(f'A{n:02}.ASM' in full for n in range(13,41))
for n in range(13,41):
 p=next((C.parent/'asm86a').glob(f'{n:02}-*.md'));meta=tomllib.loads(p.read_text().split('+++')[1]);assert meta['weight']==n-12 and meta['title'].startswith(f'{n-12:02} ')
assert 'Copy `ASM1.ASM` to `A13.ASM`' in next((C.parent/'asm86a').glob('13-*.md')).read_text()
print(f'PASS ASMA0: 12 articles, independent reference/programs, {len(manifest)} source-only files, canonical seed and A13 handoff, separate archives and legacy source links')
