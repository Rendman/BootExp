"""Reconstruct compiler checkpoints from printed source and inspect source-only publication."""
from pathlib import Path
import re,json,zipfile
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/rill';C=ROOT/'site/content/bootstrap/rill';D=ROOT/'site/static/downloads/rill';Q=ROOT/'qa/rill'
program=[];stages=json.loads((Q/'article-patches.json').read_text())
assert len(stages)==29
for stage in stages:
 text=(C/stage['page']).read_text();blocks=re.findall(r'```ir\n(.*?)\n```',text,re.S)
 for change in stage['changes']:
  a,b=change['a1'],change['a2'];assert program[a:b]==change['old'],stage['page']+' old source differs'
  for key in ['old','new','context']:
   if change[key]:assert '\n'.join(change[key]) in blocks,(stage['page'],key)
  program[a:b]=change['new']
 assert program==(W/f'R{stage["number"]:02}.IR').read_text().splitlines(),stage['page']+' reconstructed source differs'
 assert f'CHECK R{stage["number"]:02}' in text
 for forbidden in ['required IR lines','This block contains','small, testable addition']:assert forbidden not in text
assert (W/'RILL.IR').read_bytes()==(W/'R29.IR').read_bytes()
assert (W/'RILL.ASM').read_bytes()==(W/'R29.ASM').read_bytes()
# Authored source arrangement is the complete implementation, not another compiler.
strip=lambda s:[v for line in s.splitlines() if (v:=line.split(';',1)[0].strip())]
assert strip((ROOT/'tools/rill_parts.ir').read_text())==strip((W/'RILL.IR').read_text())
for name,folder in [('BOOTASM.BAS','bootasm'),('ASM86.ASM','asm86'),('IR86.ASM','ir86'),('CHECK.BAT','bootasm'),('VIEW.BAS','bootasm')]:assert (W/name).read_bytes()==(ROOT/'workbench'/folder/name).read_bytes()
blocks=re.findall(r'```rill\n(.*?)\n```',(C/'32-programs.md').read_text(),re.S)
assert len(blocks)==4
for name,block in zip(['HELLO','COUNT','CHOICE','RLECHO'],blocks):assert block+'\n'==(W/(name+'.RIL')).read_text(),name+' printed program differs'
pipeline=(C/'30-the-complete-pipeline.md').read_text()
assert re.search(r'```rill\n(.*?)\n```',pipeline,re.S)[1]+'\n'==(W/'COUNT.RIL').read_text()
assert re.search(r'```ir\n(.*?)\n```',pipeline,re.S)[1]+'\n'==(W/'COUNT.IR').read_text()
files=json.loads((Q/'package-files.json').read_text())
with zipfile.ZipFile(D/'RILL.ZIP') as z:
 assert z.namelist()==files
 for name in files:
  assert re.fullmatch('[A-Z0-9_]{1,8}\\.[A-Z0-9]{1,3}',name),name
  assert not name.endswith(('.COM','.EXE')),name
  raw=(W/name).read_bytes();raw.decode('ascii');assert b'\n' not in raw.replace(b'\r\n',b''),name
  assert raw==z.read(name)==(D/name).read_bytes(),name+' archive/download differs'
for name in ['rill-tails.png','rill-drawers.png','rill-paths.png']:assert (ROOT/'site/static/images'/name).is_file(),name
print(f'PASS RILL: 29 printed edits reconstruct exact IR sources; four printed programs and pipeline; {len(files)} ASCII/CRLF/8.3 source-only archive files; canonical bootstrap sources')
