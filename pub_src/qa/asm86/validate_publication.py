"""Reconstruct all printed edits and verify the complete source-only publication."""
from pathlib import Path
import json,re,zipfile
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/asm86';Q=ROOT/'qa/asm86';C=ROOT/'site/content/bootstrap/asm86';D=ROOT/'site/downloads/asm86'
import sys
sys.path.insert(0,str(ROOT/'tools'))
from project_paths import directory_name
program=(ROOT/'workbench/asm0/ASM86.ASM').read_text().splitlines();cases=json.loads((Q/'checkpoints.json').read_text())
for stage,case in zip(json.loads((Q/'article-patches.json').read_text()),cases):
 n=stage['number'];collection=stage['collection'];chapter=stage['chapter'];text=(C.parent/directory_name(collection)/stage['page']).read_text();
 assert collection==('asma0' if n<=12 else 'asm86a') and chapter==(n if n<=12 else 1+[c['number'] for c in cases if c['number']>12].index(n))
 if n==13:assert stage['base']=='ASMA0.ASM'
 sections=re.split(r'### Change \d+[^\n]*\n',text)[1:]
 assert len(sections)==len(stage['changes']),(n,'printed edit count')
 for section,change in zip(sections,stage['changes']):
  blocks=re.findall(r'```asm\n(.*?)\n```',section,re.S);a,b=change['a1'],change['a2']
  assert program[a:b]==change['old'],(n,'old source')
  expected=['\n'.join(change[k]).rstrip('\n') for k in ['context','old','new','after'] if change[k]]
  assert blocks[:len(expected)]==expected,(n,'printed source/context differs')
  program[a:b]=change['new']
 assert program==(W/f'A{n:02}.ASM').read_text().splitlines(),(n,'printed reconstruction')
 assert f'CHECK A{n:02}' in text and 'FAIL' in text and 'PASS' in text,(n,'visible checks')
 assert f'{case["binary_bytes"]:05} bytes' in text,(n,'build count')
 if case.get('fixture') is not None:
  blocks=re.findall(r'```(?:asm|text)\n(.*?)\n```',text,re.S)
  assert case['fixture'].replace('\r\n','\n').rstrip('\n') in blocks,(n,'acceptance source')
  assert (W/f'T{n:02}.ASM').read_text()==case['fixture'].replace('\r\n','\n'),(n,'fixture source')
 if case['bad']['kind']=='source':
  assert case['bad']['text'].rstrip('\n') in re.findall(r'```asm\n(.*?)\n```',text,re.S),(n,'rejection source')
 assert not re.search(r'\b(?:contains|requires)\s+\*?\*?\d+\s+(?:required\s+)?(?:BASIC|source|assembly)?\s*lines',text,re.I),(n,'editorial line announcement')
assert (W/'ASMA0.ASM').read_bytes()==(W/'A12.ASM').read_bytes()
assert (W/'ASM86A.ASM').read_bytes()==(W/'A40.ASM').read_bytes()
for name,group in [('BOOTASM.BAS','bootasm'),('VIEW.BAS','bootasm'),('CHECK.BAT','bootasm'),('ASM86.ASM','asm86')]:assert (W/name).read_bytes()==(ROOT/'workbench'/directory_name(group)/name).read_bytes(),name
files=json.loads((Q/'package-files.json').read_text())
with zipfile.ZipFile(D/'ASM86A.ZIP') as z:
 assert z.namelist()==files
 for name in files:
  assert re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}',name),name
  assert not name.endswith(('.COM','.EXE')),name
  data=(W/name).read_bytes();data.decode('ascii')
  assert b'\n' not in data.replace(b'\r\n',b''),name
  assert z.read(name)==data==(D/name).read_bytes(),name
text=(C/'43-programs.md').read_text();blocks=re.findall(r'```asm\n(.*?)\n```',text,re.S)
for r,b in zip(json.loads((Q/'examples.json').read_text()),blocks):assert b+'\n'==(W/(r['name']+'.ASM')).read_text(),r['name']
for n,name in [(9,'SYMS'),(17,'SYMS'),(19,'LONGSRC')]:
 p=next((C.parent/directory_name('asma0' if n<=12 else 'asm86a')).glob(f'{n:02}-*.md'));blocks=re.findall(r'```basic\n(.*?)\n```',p.read_text(),re.S)
 expected=(W/(name+'.BAS')).read_text().replace('10 N=8192','10 N=2048') if n==9 else (W/(name+'.BAS')).read_text()
 assert blocks==[expected.rstrip('\n')],(n,'BASIC text generator')
 assert len(blocks[0].splitlines())<=50
for img in ['press','cloakroom','bridge']:assert (ROOT/f'site/static/images/asm86a-{img}.png').is_file()
assert len(list(C.glob('*.md')))==29
assert len(list((C.parent/'asm1').glob('*.md')))==16
for n in [0,41,42,43]:assert len(list(C.glob(f'{n:02}-*.md')))==1
assert 'BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL' in (C/'_index.md').read_text()
print(f'PASS ASMA0/ASM86A: all 12 seed and 24 larger-assembler printed edits reconstruct exact source; {len(files)} source-only archive files match ASCII/CRLF/8.3 downloads; fixtures, programs, text generators, and assets agree')
