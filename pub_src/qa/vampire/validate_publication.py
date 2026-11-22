"""Reconstruct the actual printed adventure edits and validate source archives."""
from pathlib import Path
import json,re,sys,tomllib,zipfile

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from vampire_lessons import RECIPES,expand
W=ROOT/'workbench/vampire';Q=ROOT/'qa/vampire';C=ROOT/'site/content/bootstrap/vampire'
def lines(s):return [line for line in s.splitlines() if line.strip()]
old=[]
cases=json.loads((Q/'checkpoints.json').read_text())
patches=json.loads((Q/'article-patches.json').read_text())
assert len(cases)==len(patches)==26
for case,patch in zip(cases,patches):
    text=(C/patch['page']).read_text();n=case['number']
    printed='\n'.join(lines(text))
    for change in patch['changes']:
        kind=change['kind'];new=change['new']
        assert '\n'.join(new) in printed,(n,'unprinted source')
        if kind=='initial':old=list(new)
        elif kind=='insert':
            assert old.count(change['anchor'])==1
            at=old.index(change['anchor']);old[at:at]=new
            assert change['anchor'] in text
        elif kind=='append':old+=new
        else:
            prior=change['old'];assert '\n'.join(prior) in printed
            at=[i for i in range(len(old)) if old[i:i+len(prior)]==prior]
            assert len(at)==1,(n,'ambiguous printed locator')
            old[at[0]:at[0]+len(prior)]=new
    assert old==lines((W/case['source']).read_text()),(n,'reconstructed source')
    assert f'VMAKE V{n:02}' in text and str(case['binary_bytes']) in text.replace(',','')
    for report in case['reports']:assert report.strip() in text
    for expected in case['expected']+case['alternate_expected']:assert expected in text
    assert 'physical line' not in text and 'source lines' not in text
assert (W/'VAMPIRE.RIL').read_bytes()==(W/'V26.RIL').read_bytes()
cover=tomllib.loads((C/'_index.md').read_text().split('+++')[1]);assert cover['optional']
for name in RECIPES:assert (W/name).read_text()==expand(name),name
assert (W/'WIN.TXT').read_bytes().endswith(b'STAKES\r\n')
files=json.loads((Q/'package-files.json').read_text())
for area in ['site/downloads/vampire','site/static/downloads/tools/vampire']:
    d=ROOT/area
    with zipfile.ZipFile(d/'VAMPIRE.ZIP') as z:
        assert z.namelist()==files
        for name in files:
            assert re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}',name),name
            assert not name.endswith(('.COM','.EXE','.ASM','.IR'))
            raw=(W/name).read_bytes();raw.decode('ascii')
            assert b'\n' not in raw.replace(b'\r\n',b'')
            assert raw==z.read(name)==(d/name).read_bytes(),name
text=f'PASS optional adventure: 26 exact uniquely anchored printed constructions; command fixtures; optional navigation; {len(files)} ASCII/CRLF/8.3 source-only archive members'
print(text);(Q/'publication-results.txt').write_text(text+'\n')
