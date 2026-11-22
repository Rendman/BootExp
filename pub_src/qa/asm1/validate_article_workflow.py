"""Check reader numbering, source locators, and the executable-name handoff."""
from pathlib import Path
import re,tomllib

ROOT=Path(__file__).resolve().parents[2]
CONTENT=ROOT/'site/content/bootstrap'
for group,last in [('asm0',31),('asm1',20)]:
 pages=[]
 for page in (CONTENT/group).glob('*.md'):
  if page.name=='_index.md':continue
  text=page.read_text();meta=tomllib.loads(text.split('+++')[1])
  pages.append((meta['weight'],page,text,meta))
 pages.sort()
 assert [weight for weight,*_ in pages]==list(range(last+1)),group
 for weight,page,text,meta in pages:
  if weight:assert meta['title'].startswith(f'{weight:02} · '),(page,'article number')
  else:assert not re.match(r'^\d',meta['title']),(page,'unnumbered workbench')
  changes=[int(n) for n in re.findall(r'^### Change (\d+)',text,re.M)]
  assert changes==list(range(1,len(changes)+1)),(page,'edit order')
  prose=re.sub(r'```.*?```','',text,flags=re.S)
  assert not re.search(r'\b1 bytes\b|physical positions|old physical line',prose),(page,'editorial leftover')
  if meta['download'].startswith(('AS','A0','A1')) and page.name not in {'00-workbench.md','13-reference.md','31-reference.md','32-programs.md','14-programs.md'}:
   assert '**Starting source:**' in text and '**Save as:**' in text and '**Build with:**' in text,(page,'source note')
 print(f'PASS {group}: consecutive article numbers, separate source names, label edits and clean units',flush=True)

# Follow the self-build article's actual commands, rather than assuming that
# a working-name executable was installed somewhere outside the instructions.
text=(CONTENT/'asm0/30-self-assembly.md').read_text()
available={'RESULT.COM'}
for block in re.findall(r'```dos\n(.*?)\n```',text,re.S):
 for line in block.splitlines():
  if line.startswith('COPY '):
   _,src,dst=line.split()
   if src.endswith('.COM'):assert src in available,('copy uses missing executable',line)
   if dst.endswith('.COM'):available.add(dst)
  elif line.startswith('CHECK '):assert line.split()[1]+'.COM' in available,('run uses missing executable',line)
assert 'ASM0.COM' in available,'Self-build never saves the working assembler'
assert text.index('COPY SELF.COM ASM0.COM')>text.index('FC.EXE /B SELF.COM AGAIN.COM')
print('PASS ASM0: verified native generation is saved as ASM0.COM for the reference, examples and ASM1 workbench',flush=True)

reader=(CONTENT/'asm1/02-reading-an-input-block.md').read_text()
helper=re.search(r'```basic\n(10 N=1024.*?)\n```',reader,re.S)[1]+'\n'
assert helper==(ROOT/'workbench/asm1/STREAM.BAS').read_text()
lines=helper.replace('N=1024','N=4000').replace('"DB 65"','";"')
assert lines==(ROOT/'workbench/asm1/LINES.BAS').read_text()
assert 'SAVE "LINES.BAS",A' in (CONTENT/'asm1/08-a-longer-source-count.md').read_text()
assert 'A missing-source' not in (CONTENT/'asm1/05-protecting-recovery-names.md').read_text()
assert 'plus the XOR forms' in (CONTENT/'asm1/07-streaming-the-two-assembly-passes.md').read_text()
print('PASS ASM1: published generator matches disk sources; saved BASIC variants and current capabilities agree',flush=True)
