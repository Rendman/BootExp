"""Reconstruct the required printed construction and verify source-only delivery."""
from pathlib import Path
import json,re,sys,tomllib,zipfile
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'site/content/bootstrap';Q=ROOT/'qa/toolchain'
sys.path.insert(0,str(ROOT/'tools'))
from publication_names import filename

def check():
 patches=json.loads((Q/'ladder-article-patches.json').read_text())
 previous={};counts={}
 for stage in patches:
  family=stage['family'];group=stage['collection'];folder=ROOT/stage['folder'];n=stage['number'];text=(C/group/stage['page']).read_text()
  if family not in previous:
   if group=='ir86':base=(ROOT/'workbench/asm86a/ASM86A.ASM').read_text().splitlines();assert stage['base']=='ASM86.ASM'
   elif group=='rb':base=(ROOT/'workbench/rill/RILL.IR').read_text().splitlines();assert stage['base']=='RILL0.IR'
   else:base=[];assert stage['base'] is None
  else:base=previous[family]
  sections=re.split(r'### Edit at old physical position \d+\n\n',text)[1:]
  if base:assert len(sections)==len(stage['changes']),(group,n,'edit count')
  else:
   block=re.search(r'```ir\n(.*?)\n```',text,re.S);assert block and block[1].splitlines()==stage['changes'][0]['new']
  for i,e in enumerate(stage['changes']):
   a,b=e['a1'],e['a2'];assert base[a:b]==e['old'],(group,n,'base differs')
   if sections:
    blocks=re.findall(r'```(?:ir|asm)\n(.*?)\n```',sections[i],re.S)
    pieces=([e.get('context',[]),e['old'][:3],e['old'][-3:],e['new'],e.get('after',[])] if e.get('old_display')=='bounds' else [e.get(k,[]) for k in ['context','old','new','after']])
    expected=['\n'.join(part).rstrip('\n') for part in pieces if part]
    assert blocks[:len(expected)]==expected,(group,n,'printed source differs')
   base[a:b]=e['new']
  assert base==(folder/stage['source']).read_text().splitlines(),(group,n,'reconstruction')
  assert 'PASS' in text and 'VIEW.BAS' in text
  previous[family]=list(base);counts[family]=counts.get(family,0)+1
 assert counts=={f:len(json.loads((Q/(f+'.json')).read_text())) for f in counts}
 assert (ROOT/'workbench/ir86/IR86.ASM').read_bytes()==(ROOT/'workbench/ir86/IRWIDE.ASM').read_bytes()
 assert (ROOT/'workbench/rill/RILL.IR').read_text().splitlines()==previous['rill-initial-series']
 assert (ROOT/'workbench/rill/RILLBOOT.IR').read_text().splitlines()==previous['rill-seed-series']
 # The RILL-written compiler still has its own exact construction.
 old=[];selfpatches=json.loads((Q/'article-patches.json').read_text())
 assert len(selfpatches)==len(json.loads((Q/'rill-self-series.json').read_text()))==43
 for s in selfpatches:
  assert s['family']=='rill-self-series'
  text=(C/'rc'/s['page']).read_text()
  sections=re.split(r'### Edit \d+\n\n',text)[1:]
  if s['base']:assert len(sections)==len(s['changes'])
  for i,e in enumerate(s['changes']):
   a,b=e['a1'],e['a2'];assert old[a:b]==e['old']
   if s['base']:
    blocks=re.findall(r'```rill\n(.*?)\n```',sections[i],re.S)
    pieces=([e.get('context',[]),e['old'][:3],e['old'][-3:],e['new'],e.get('after',[])] if e.get('old_display')=='bounds' else [e.get(k,[]) for k in ['context','old','new','after']])
    expected=['\n'.join(part).rstrip('\n') for part in pieces if part]
    assert blocks[:len(expected)]==expected
   else:assert '\n'.join(e['new']) in text
   old[a:b]=e['new']
  assert old==(ROOT/'workbench/toolchain'/s['source']).read_text().splitlines()
 assert old==(ROOT/'workbench/toolchain/RILL.RIL').read_text().splitlines()
 # Reconstruct the local-capacity exercises from their printed instructions.
 complete=(C/'rc'/selfpatches[-1]['page']).read_text()
 blocks=re.findall(r'```rill\n(.*?)\n```',complete,re.S)
 local=next(b for b in blocks if b.startswith('fn check('))+'\n'
 work=ROOT/'workbench/toolchain'
 assert local==(work/'TLOCAL.RIL').read_text()
 assert local.replace('return (a0!=0)','let mut extra=0;\nreturn (a0!=0)')==(work/'XLOCAL.RIL').read_text()
 rows='\n'.join(local.splitlines()[1:9])
 skeleton=next(b for b in blocks if b.startswith('let mut result=0;'))
 scope=re.sub(r'// Copy (?:the|the same) eight declaration lines here\.',lambda _:rows,skeleton)
 assert re.sub(r'\s+','',scope)==re.sub(r'\s+','',(work/'TSCOPE.RIL').read_text())
 # Both later port notebooks reproduce their exact authored source by routine.
 for name,page in [('IR86','01-ir86-in-rill.md'),('ASM86A','02-asm86-in-rill.md')]:
  text=(C/'toolchain'/page).read_text();part=text.split('## Complete source, by routine\n\n')[1].split('## Complete build\n\n')[0]
  blocks=re.findall(r'```rill\n(.*?)\n```',part,re.S)
  expected=re.split(r'(?m)(?=^fn )',(ROOT/'workbench/toolchain'/(name+'.RIL')).read_text())
  assert blocks==[p.rstrip('\n') for p in expected],name
 batch=(ROOT/'workbench/toolchain/TMAKE.BAT').read_text()
 page=(C/'toolchain/03-building-the-toolchain.md').read_text()
 # Reader naming changes only filenames and prose, never implementation listings.
 from publication_names import reader_text
 assert reader_text('toolchain','TMAKE.BAT',batch).strip() in page
 compare=(C/'toolchain/04-comparing-generations.md').read_text()
 for stem in ['A','I','R']:
  for gen in [1,2]:assert f'COMP {stem}0.COM {stem}{gen}.COM' in compare
 # Every legacy archive is independently checked against its source snapshot.
 specs=[('ir86','IR86.ZIP','ir86','ir86/package-files.json'),('rill','RILL.ZIP','rill','rill/package-files.json'),('rb','RB.ZIP','rb','compiler_collections/rb-files.json'),('rc','RC.ZIP','rc','compiler_collections/rc-files.json'),('toolchain','TOOLCHN.ZIP','toolchain','toolchain/package-files.json')]
 for group,archive,work,manifest in specs:
  files=json.loads((ROOT/'qa'/manifest).read_text());dest=ROOT/'site/static/downloads'/group
  with zipfile.ZipFile(dest/archive) as z:
   assert z.namelist()==files,(group,'archive members')
   for name in files:
    assert re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}',name),name
    assert not name.endswith(('.COM','.EXE'))
    raw=(ROOT/'workbench'/work/name).read_bytes();raw.decode('ascii')
    assert b'\n' not in raw.replace(b'\r\n',b''),(group,name,'line endings')
    assert z.read(name)==raw==(dest/name).read_bytes(),(group,name,'source differs')
 print('PASS required native IR, continuing RILL0/RILLBOOT, all RILL compiler edits, exact port notebooks, rebuild commands, and source archives')
if __name__=='__main__':check()
