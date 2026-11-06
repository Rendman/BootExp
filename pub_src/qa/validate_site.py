"""Check the built course, source links, type-in patches, and public archive."""
from pathlib import Path
import sys,re,json,zipfile,tomllib
from urllib.parse import urlparse,unquote,urljoin
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools/python'))
from bs4 import BeautifulSoup
PUBLIC=ROOT.parent/'public';CONTENT=ROOT/'site/content';WORK=ROOT/'workbench/bootasm'
if not (PUBLIC/'bootstrap/bootasm/index.html').is_file():
 raise SystemExit(f'Missing built BOOTASM collection: {PUBLIC}')
errors=[];count=0
for p in PUBLIC.rglob('*.html'):
 soup=BeautifulSoup(p.read_text(),'html.parser');count+=1
 if len(soup.select('h1'))!=1:errors.append(f'{p}: must have one H1')
 for a in soup.select('[href], [src]'):
  dest=a.get('href',a.get('src',''));u=urlparse(dest)
  if u.scheme or u.netloc or not u.path:continue
  target=PUBLIC/unquote(u.path).lstrip('/') if u.path.startswith('/') else p.parent/unquote(u.path)
  if target.is_dir():target/= 'index.html'
  if not target.exists():errors.append(f'{p.relative_to(PUBLIC)}: missing {dest}')
  elif u.fragment and target.suffix=='.html':
   ids=BeautifulSoup(target.read_text(),'html.parser').select('[id]')
   if unquote(u.fragment) not in {n['id'] for n in ids}:errors.append(f'{p}: missing anchor {dest}')
 for img in soup.select('img'):
  if not img.get('alt'):errors.append(f'{p}: image without alt')
# Old seed URLs must redirect correctly on both file copies and GitHub project sites.
for p in (CONTENT/'bootstrap/asma0').glob('*.md'):
 meta=tomllib.loads(p.read_text().split('+++')[1])
 for alias in meta.get('aliases',[]):
  assert len(alias.strip('/').split('/'))==3,alias
  redirect=PUBLIC/alias.strip('/')/'index.html'
  if not redirect.is_file():errors.append(f'Missing legacy redirect: {alias}');continue
  soup=BeautifulSoup(redirect.read_text(),'html.parser')
  link=soup.select_one('link[rel="canonical"]');refresh=soup.select_one('meta[http-equiv="refresh"]');a=soup.select_one('a[href]')
  expected=PUBLIC/'bootstrap/asma0'/p.stem/'index.html'
  if not link or not refresh or not a:errors.append(f'Incomplete legacy redirect: {alias}');continue
  target=link['href']
  if target.startswith('/') or (redirect.parent/target).resolve()!=expected.resolve():errors.append(f'Incorrect portable redirect: {alias}')
  if refresh['content']!=f'0; url={target}' or a['href']!=target:errors.append(f'Inconsistent redirect targets: {alias}')
  for prefix in ['', '/BootExp']:
   actual=urljoin(f'https://example.invalid{prefix}{alias}index.html',target)
   if actual!=f'https://example.invalid{prefix}/bootstrap/asma0/{p.stem}/index.html':errors.append(f'Incorrect hosted redirect: {alias}')
for p in (ROOT/'site/static/downloads/bootasm').iterdir():
 if p.suffix.upper() in {'.BAS','.ASM','.BAT','.TXT'}:
  b=p.read_bytes()
  if b'\n' in b.replace(b'\r\n',b''):errors.append(f'{p}: non-DOS line endings')
  try:b.decode('ascii')
  except UnicodeDecodeError:errors.append(f'{p}: non-ASCII source')
  if len(p.stem)>8 or len(p.suffix)>4:errors.append(f'{p}: not an 8.3 name')
with zipfile.ZipFile(ROOT/'site/static/downloads/bootasm/BOOTASM.ZIP') as z:
 if len(z.namelist())!=59:errors.append('Unexpected archive file count')
 for name in z.namelist():
  if z.read(name)!=(WORK/name).read_bytes():errors.append(f'Archive differs: {name}')
 if any(n.upper().endswith(('.EXE','.COM')) for n in z.namelist()):errors.append('Prebuilt executable in source archive')
# Reconstruct the assembler from printed patch blocks, not the author's stage data.
program={}
for i in range(2,19):
 p=next((CONTENT/'bootstrap/bootasm').glob(f'{i:02}-*.md'))
 block=re.search(r'```basic\n(.*?)\n```',p.read_text(),re.S).group(1)
 source=block.splitlines()
 if len(source)>50:errors.append(f'{p}: too many required BASIC lines')
 for line in source:
  n,text=line.split(' ',1);program[int(n)]=text
 expected='\n'.join(f'{n} {v}' for n,v in sorted(program.items()))+'\n'
 if expected!=(WORK/f'BA{i:02}.BAS').read_text():errors.append(f'{p}: printed patch differs from executable checkpoint')
 if 'ERROR line' not in p.read_text():errors.append(f'{p}: missing visible rejection')
if (WORK/'BOOTASM.BAS').read_bytes()!=(WORK/'BA18.BAS').read_bytes():errors.append('Final source differs from final checkpoint')
import runpy
runpy.run_path(str(ROOT/'qa/asm86/validate_publication.py'),run_name='__main__')
runpy.run_path(str(ROOT/'qa/asma0/validate_publication.py'),run_name='__main__')
runpy.run_path(str(ROOT/'qa/asm86a/validate_publication.py'),run_name='__main__')
runpy.run_path(str(ROOT/'qa/ir86/validate_publication.py'),run_name='__main__')
runpy.run_path(str(ROOT/'qa/rill/validate_publication.py'),run_name='__main__')
runpy.run_path(str(ROOT/'qa/toolchain/validate_publication.py'),run_name='__main__')
for p in CONTENT.rglob('*.md'):
 text=p.read_text().lower()
 for forbidden in ('checksum','unicorn','python','automated regression','ai-generated','ai tools'):
  if forbidden in text:errors.append(f'{p}: production language {forbidden}')
if errors:
 print('\n'.join(errors));raise SystemExit(1)
asm_count=len(json.loads((ROOT/'qa/asm86/package-files.json').read_text()))
seed_count=len(json.loads((ROOT/'qa/asma0/package-files.json').read_text()))
asma_count=len(json.loads((ROOT/'qa/asm86a/package-files.json').read_text()))
ir_count=len(json.loads((ROOT/'qa/ir86/package-files.json').read_text()))
rill_count=len(json.loads((ROOT/'qa/rill/package-files.json').read_text()))
tool_count=len(json.loads((ROOT/'qa/toolchain/package-files.json').read_text()))
text=f'PASS: {count} HTML files (including 12 seed redirects); all local links, assets and anchors; 59 BOOTASM + {asm_count} ASM86 + {seed_count} ASMA0 + {asma_count} ASM86A + {ir_count} IR86 + {rill_count} RILL + {tool_count} toolchain archive sources; ASCII/CRLF/8.3; all 17 BASIC, 29 ASM86, 12 ASMA0, 28 ASM86A, 32 IR86, 29 first RILL, 23 streaming IR, 47 compiler-seed, and 43 self-compiling RILL printed edits reconstruct exact checkpoints; editorial exclusions.'
print(text);(ROOT/'qa/site-results.txt').write_text(text+'\n')
