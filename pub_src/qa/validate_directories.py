"""Check production directories, reader-name mappings and owned download sets."""
from pathlib import Path
import json,re,sys,tomllib,zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from publication_names import SERIES
from project_paths import directory_name

def check():
 manifest=json.loads((ROOT/'qa/reader-packages.json').read_text())
 expected_readers={tool.lower() for tool,_ in SERIES.values()}
 assert set(manifest)==expected_readers,'Reader manifest disagrees with the collection map'
 checks=[
  (ROOT,{'site','workbench','tools','qa'}),
  (ROOT/'workbench',expected_readers),
  (ROOT/'site/content/bootstrap',expected_readers),
  (ROOT/'site/downloads',expected_readers),
  (ROOT/'site/static/downloads',{'tools'}),
  (ROOT/'site/static/downloads/tools',expected_readers),
  (ROOT/'qa',(expected_readers-{'rillboot','rill'})|{'compilers'}),
 ]
 for base,expected in checks:
  ignored={'__pycache__'}|({'.venv'} if base==ROOT else set())
  actual={p.name for p in base.iterdir() if p.is_dir() and p.name not in ignored}
  assert actual==expected,(str(base),'missing',sorted(expected-actual),'unexpected',sorted(actual-expected))
 config=tomllib.loads((ROOT/'site/hugo.toml').read_text())
 mounts={m['source']:m['target'] for m in config['module']['mounts']}
 for key in SERIES:
  assert mounts['downloads/'+directory_name(key)]=='static/downloads/'+key,(key,'download URL mount')
 assert (ROOT/'site'/config['publishDir']).resolve()==ROOT.parent/'public','Hugo must publish to root public/'
 for wrong in [ROOT/'public',ROOT/'pub_src',ROOT/'site/public']:
  assert not wrong.exists(),f'Misplaced generated directory: {wrong}'

 # The seed's former direct URLs and the old complete-source icons remain
 # supported. Everything else in each download directory belongs to its ZIP.
 seed_files=set(json.loads((ROOT/'qa/asm1/package-files.json').read_text()))-{'README.TXT'}
 legacy_aliases={'asm86a':seed_files,'ir86':{'IR86.RIL','IRWIDE.ASM'},'rill':{'RILL.RIL','RILLBOOT.IR'}}
 canonical_aliases={'ir86':{'IR86.RIL','IRWIDE.ASM'}}
 for canonical,m in manifest.items():
  group=m['legacy_group'];legacy=ROOT/'site/downloads'/directory_name(group)
  assert SERIES[group][0].lower()==canonical,(group,canonical,'directory map')
  with zipfile.ZipFile(legacy/m['legacy_archive']) as z:
   members=set(z.namelist())
   allowed=members|{m['legacy_archive']}|legacy_aliases.get(group,set())
   actual={p.name for p in legacy.iterdir()}
   assert actual==allowed,(group,'legacy download files',sorted(actual^allowed))
   for name in members:
    assert (ROOT/'workbench'/directory_name(group)/name).is_file(),(group,name,'missing workbench source')
   for name in allowed-members-{m['legacy_archive']}:
    owner='asma0' if group=='asm86a' else 'toolchain'
    assert (legacy/name).read_bytes()==(ROOT/'workbench'/directory_name(owner)/name).read_bytes(),(group,name,'compatibility source')
  dest=ROOT/'site/static/downloads/tools'/canonical
  allowed=set(m['files'])|{m['archive']}|canonical_aliases.get(canonical,set())
  actual={p.name for p in dest.iterdir()}
  assert actual==allowed,(canonical,'reader download files',sorted(actual^allowed))
  for name in canonical_aliases.get(canonical,set()):
   assert (dest/name).read_bytes()==(ROOT/'workbench/toolchain'/name).read_bytes(),(canonical,name,'compatibility source')

 # The shared workbench also feeds the separate seed archive, including its
 # assembly listings. They must survive toolchain packaging unchanged.
 seed=set(json.loads((ROOT/'qa/compilers/rb-files.json').read_text()))
 for name in seed-{'README.TXT'}:
  assert (ROOT/'workbench/toolchain'/name).read_bytes()==(ROOT/'workbench/rillboot'/name).read_bytes(),(name,'shared RILLBOOT source')
 for area in ['workbench/rillboot','workbench/toolchain','site/downloads/toolchain']:
  active=seed if area=='workbench/rillboot' else set(json.loads((ROOT/'qa/toolchain/package-files.json').read_text()))
  if area=='workbench/toolchain':active|=seed
  for p in (ROOT/area).iterdir():
   if re.fullmatch(r'(?:T|X)?RB\d+\.(?:IR|RIL|ASM)',p.name):
    assert p.name in active,(str(p),'obsolete compiler-seed file')
 text=f'PASS directory layout: four production areas; {len(SERIES)} matching collection/workbench/reader mappings; exact download sets and compatibility sources; shared compiler-seed inputs; root public/ output; no obsolete seed stages'
 print(text)
 (ROOT/'qa/directory-results.txt').write_text(text+'\n')

if __name__=='__main__':check()
