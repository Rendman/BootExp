"""Reconstruct every new checkpoint from its actual printed source edits."""
from pathlib import Path
import json,re,zipfile,tomllib
ROOT=Path(__file__).resolve().parents[2];W=ROOT/'workbench/toolchain';Q=ROOT/'qa/toolchain';C=ROOT/'site/content/bootstrap';D=ROOT/'site/static/downloads/toolchain'
programs={'ir-extensions':(ROOT/'workbench/asm86a/ASM86A.ASM').read_text().splitlines(),'rill-seed-series':[],'rill-self-series':[]};counts={k:0 for k in programs}
for stage in json.loads((Q/'article-patches.json').read_text()):
 family=stage['family'];program=programs[family];text=(C/stage['collection']/stage['page']).read_text();kind=stage['kind'];sections=re.split(r'### Edit \d+\n',text)[1:]
 if stage['base'] is None:
  blocks=re.findall('```'+kind+r'\n(.*?)\n```',text,re.S);assert blocks[0].splitlines()==stage['changes'][0]['new'];sections=[text]
 for i,ch in enumerate(stage['changes']):
  a,b=ch['a1'],ch['a2'];assert program[a:b]==ch['old'],(stage['page'],'old context')
  blocks=re.findall('```'+kind+r'\n(.*?)\n```',sections[i],re.S)
  expected=['\n'.join(ch[k]).rstrip('\n') for k in ['context','old','new','after'] if ch[k]]
  assert blocks[:len(expected)]==expected,(stage['page'],'printed blocks')
  program[a:b]=ch['new']
 assert program==(W/stage['source']).read_text().splitlines(),(stage['page'],'source reconstruction')
 assert 'PASS' in text,(stage['page'],'visible checks')
 assert f'CHECK {Path(stage["source"]).stem}' in text,(stage['page'],'execution command')
 counts[family]+=1
assert counts=={'ir-extensions':23,'rill-seed-series':47,'rill-self-series':43},counts
for a,b in [('IW23.ASM','IRWIDE.ASM'),('RB47.IR','RILLBOOT.IR'),('RC43.RIL','RILL.RIL')]:assert (W/a).read_bytes()==(W/b).read_bytes(),(a,b,'canonical handoff')
for name,group in [('BOOTASM.BAS','bootasm'),('ASM86.ASM','asm86'),('ASMA0.ASM','asma0'),('ASM86A.ASM','asm86a'),('VIEW.BAS','bootasm'),('CHECK.BAT','bootasm'),('IRWIDE.ASM','ir86'),('RILLBOOT.IR','rill')]:assert (W/name).read_bytes()==(ROOT/'workbench'/group/name).read_bytes(),name
for name,group,page in [('IR86','toolchain','01-ir86-in-rill.md'),('ASM86A','toolchain','02-asm86-in-rill.md')]:
 blocks=re.findall(r'```rill\n(.*?)\n```',(C/group/page).read_text(),re.S)
 strip=lambda s:[r for r in s.splitlines() if r.strip()]
 assert strip('\n'.join(blocks))==strip((W/(name+'.RIL')).read_text()),name+' source notebook'
for c in json.loads((Q/'examples.json').read_text()):
 p=next((C/'rb').glob('*-'+re.sub('[^a-z0-9]+','-',c['title'].lower()).strip('-')+'.md'))
 blocks=re.findall(r'```rill\n(.*?)\n```',p.read_text(),re.S);assert blocks[0]+'\n'==(W/(c['name']+'.RIL')).read_text()
 assert blocks[1]==c['bad'],c['name']+' printed rejection'
 text=p.read_text();assert f'{c["binary_bytes"]:05} bytes' in text and c['error'] in text,c['name']+' measured reports'
files=json.loads((Q/'package-files.json').read_text())
with zipfile.ZipFile(D/'TOOLCHN.ZIP') as z:
 assert z.namelist()==files and len(files)==len(set(files))
 for name in files:
  assert re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}',name),name
  assert not name.endswith(('.COM','.EXE')),name
  raw=(W/name).read_bytes();raw.decode('ascii');assert b'\n' not in raw.replace(b'\r\n',b''),name
  assert raw==z.read(name)==(D/name).read_bytes(),name+' source/download/archive'
for family in counts:
 for c in json.loads((Q/(family+'.json')).read_text()):
  assert c['source'] in files
  prefix={'ir-extensions':'IW','rill-seed-series':'RB','rill-self-series':'RC'}[family];ext='IR' if prefix=='IW' else 'RIL';n=c['number']
  if c.get('fixture') is not None:assert f'T{prefix}{n:02}.'+ext in files
  if c.get('bad') is not None:assert f'X{prefix}{n:02}.'+ext in files
import sys
sys.path.insert(0,str(ROOT/'tools'))
from publication_names import names
pipeline=(C/'toolchain/03-building-the-toolchain.md').read_text();assert re.search(r'```dos\n(ECHO OFF\n.*?)\n```',pipeline,re.S)[1]+'\n'==names((W/'TMAKE.BAT').read_text())
# The RILL ports can only be introduced after the compiler self-builds.
expected={'00-workbench.md':0,'01-ir86-in-rill.md':1,'02-asm86-in-rill.md':2,'03-building-the-toolchain.md':3,'04-comparing-generations.md':4}
assert len(list((C/'toolchain').glob('*.md')))==6
for page,weight in expected.items():assert tomllib.loads((C/'toolchain'/page).read_text().split('+++')[1])['weight']==weight
assert tomllib.loads((C/'toolchain/_index.md').read_text().split('+++')[1])['weight']>tomllib.loads((C/'rc/_index.md').read_text().split('+++')[1])['weight']
assert 'download = "IRWIDE.ASM"' in (C/'ir86/_index.md').read_text()
assert (C/'rc/133-the-compiler-self-build.md').exists()
assert not (C/'ir86/061-ir86-in-rill.md').exists()
assert not any((C/'rc'/p).exists() for p in ['134-asm86a-in-rill.md','135-the-complete-toolchain.md'])
for page,routes in {
 '01-ir86-in-rill.md':['/bootstrap/ir86/061-ir86-in-rill/'],
 '02-asm86-in-rill.md':['/bootstrap/rc/134-asm86a-in-rill/','/bootstrap/rill/134-asm86a-in-rill/'],
 '03-building-the-toolchain.md':['/bootstrap/rc/135-the-complete-toolchain/','/bootstrap/rill/135-the-complete-toolchain/']}.items():
 assert tomllib.loads((C/'toolchain'/page).read_text().split('+++')[1])['aliases']==routes
compare=(C/'toolchain/04-comparing-generations.md').read_text()
for tool in ['A','I','R']:
 for generation in [1,2]:assert f'COMP {tool}0.COM {tool}{generation}.COM <NO.TXT' in compare
assert 'CHECK R2' in compare and 'CHECK I2' in compare and 'CHECK A2' in compare
packages=json.loads((ROOT/'qa/reader-packages.json').read_text())
for name in ['IR86.RIL','ASM86.RIL','TMAKE.BAT']:
 assert name in packages['toolchain']['files'] and name not in packages['rill']['files']
print(f'PASS toolchain: 23 native IR + 47 IR-compiler + 43 RILL-compiler printed edits reconstruct exact sources; complete port notebooks, examples, handoffs, and {len(files)} ASCII/CRLF/8.3 archive sources agree')
