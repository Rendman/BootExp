"""Reconstruct every IR translator from the printed changes and inspect its archive."""
from pathlib import Path
import json,re,zipfile
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/ir86';C=ROOT/'site/content/bootstrap/ir86';D=ROOT/'site/static/downloads/ir86'
program=(ROOT/'workbench/asm86/AS07.ASM').read_text().splitlines()
for stage in json.loads((ROOT/'qa/ir86/article-patches.json').read_text()):
 text=(C/stage['page']).read_text();blocks=re.findall(r'```asm\n(.*?)\n```',text,re.S)
 for change in stage['changes']:
  a,b=change['a1'],change['a2'];assert program[a:b]==change['old'],stage['page']+' old source differs'
  for key in ['old','new','context']:
   if change[key]:assert '\n'.join(change[key]) in blocks,(stage['page'],key)
  program[a:b]=change['new']
 assert program==(W/f'IR{stage["number"]:02}.ASM').read_text().splitlines(),stage['page']+' source differs'
 assert f'CHECK IR{stage["number"]:02}' in text
assert (W/'IR86.ASM').read_bytes()==(W/'IR32.ASM').read_bytes()
import sys
sys.path.insert(0,str(ROOT/'tools'))
from ir86_runtime_text import runtime
assert (W/'RUNTIME.ASM').read_text()==runtime(30)
assert '```asm\n'+runtime(30).rstrip()+'\n```' in (C/'28-reference.md').read_text()
for name,folder in [('BOOTASM.BAS','bootasm'),('ASM86.ASM','asm86'),('AS07.ASM','asm86')]:assert (W/name).read_bytes()==(ROOT/'workbench'/folder/name).read_bytes()
pipeline=(C/'27-the-complete-pipeline.md').read_text()
assert re.search(r'```ir\n(.*?)\n```',pipeline,re.S)[1]+'\n'==(W/'COPYFILE.IR').read_text()
blocks=re.findall(r'```ir\n(.*?)\n```',(C/'29-programs.md').read_text(),re.S)
for name,block in zip(['HELLO','COUNT','BYTES','ECHOIR'],blocks):assert block+'\n'==(W/(name+'.IR')).read_text(),name+' printed example differs'
assert len(blocks)==4
files=json.loads((ROOT/'qa/ir86/package-files.json').read_text())
with zipfile.ZipFile(D/'IR86.ZIP') as z:
 assert z.namelist()==files
 for name in files:
  assert re.fullmatch('[A-Z0-9_]{1,8}\\.[A-Z0-9]{1,3}',name),name
  assert not name.endswith(('.COM','.EXE')),name
  b=(W/name).read_bytes();b.decode('ascii');assert b'\n' not in b.replace(b'\r\n',b''),name
  assert b==z.read(name)==(D/name).read_bytes(),name+' publication differs'
print(f'PASS IR86: 32 printed edits reconstruct source; five complete printed programs; {len(files)} ASCII/CRLF/8.3 archive sources; canonical bootstrap sources')
