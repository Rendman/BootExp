"""Check the built course, source links, type-in patches, and public archive."""
from pathlib import Path
import sys,re,json,zipfile
from urllib.parse import urlparse,unquote
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
for p in CONTENT.rglob('*.md'):
 text=p.read_text().lower()
 for forbidden in ('checksum','unicorn','python','automated regression','ai-generated','ai tools'):
  if forbidden in text:errors.append(f'{p}: production language {forbidden}')
if errors:
 print('\n'.join(errors));raise SystemExit(1)
asm_count=len(json.loads((ROOT/'qa/asm86/package-files.json').read_text()))
text=f'PASS: {count} HTML pages; all local links, assets and anchors; 59 BOOTASM + {asm_count} ASM86 archive sources; ASCII/CRLF/8.3; all 17 BASIC and 29 assembly printed edits reconstruct exact checkpoints; editorial exclusions.'
print(text);(ROOT/'qa/site-results.txt').write_text(text+'\n')
