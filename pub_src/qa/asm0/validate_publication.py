"""Reconstruct source from printed edits and check every packaged file."""
from pathlib import Path
import json,re,zipfile
import runpy
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/asm0';C=ROOT/'site/content/bootstrap/asm0';D=ROOT/'site/downloads/asm0'
checks=runpy.run_path(str(ROOT/'qa/asm1/validate_steps.py'))
program=[]
for stage in json.loads((ROOT/'qa/asm0/article-patches.json').read_text()):
 text=(C/stage['page']).read_text()
 blocks=re.findall(r'```asm\n(.*?)\n```',text,re.S)
 if stage['number']==1:
  assert blocks[0].splitlines()==stage['changes'][0]['new']
  program=blocks[0].splitlines()
 else:
  # Notes and blank lines must not act as source coordinates.
  varied=['; Reader note','']
  for line in program:varied+=['  '+line,'']
  program=checks['apply_label_edits'](varied,stage,text)
 expected=(W/f'AS{stage["number"]:02}.ASM').read_text().splitlines()
 assert checks['code'](program)==checks['code'](expected),(stage['page'],'printed edits do not reconstruct source')
 assert f'CHECK AS{stage["number"]:02}' in text
assert (W/'ASM86.ASM').read_bytes()==(W/'AS28.ASM').read_bytes()
assert (W/'BOOTASM.BAS').read_bytes()==(ROOT/'workbench/bootasm/BOOTASM.BAS').read_bytes()
files=json.loads((ROOT/'qa/asm0/package-files.json').read_text())
with zipfile.ZipFile(D/'ASM86.ZIP') as z:
 assert z.namelist()==files,'archive manifest differs'
 for name in files:
  assert re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}',name),name
  assert not name.endswith(('.COM','.EXE')),name
  b=(W/name).read_bytes();b.decode('ascii')
  assert b'\n' not in b.replace(b'\r\n',b''),name+' non-DOS line endings'
  assert z.read(name)==b==(D/name).read_bytes(),name+' archive/source/download differ'
for n in [0,30,31,32]:assert len(list(C.glob(f'{n:02}-*.md')))==1
print(f'PASS ASM86: all 28 printed edits reconstruct exact source; {len(files)} source-only archive files match ASCII/CRLF/8.3 downloads')
