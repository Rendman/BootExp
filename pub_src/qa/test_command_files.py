"""Execute PSP-selected filenames through every file-using construction family."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qa/toolchain'))
from common import run,AssemblerMachine
reports=[]
def passed(message):reports.append(message);print(message,flush=True)

def reject(image,tail,files):
 r=run(image,files=files,command_line=tail)
 assert r.exitcode!=0,(tail,r.output)
 assert r.files==files,(tail,'files changed',r.files)
 assert not r.handles and not r.allocations,(tail,'resources retained')

asm=ROOT/'workbench/asm86'
for n in [c['number'] for c in json.loads((ROOT/'qa/asm86/checkpoints.json').read_text())]:
 image=(asm/f'A{n:02}.COM').read_bytes()
 data=b'ABC\r\n' if 3<=n<=6 else b'DB 65,66\r\n'
 r=run(image,files={'IN.ASM':data,'OUT.COM':b'OLD'},command_line='\t in.asm  out.com  ')
 assert r.exitcode==0,(n,r.output)
 target='ASMA.TMP' if 3<=n<=5 else 'OUT.COM'
 assert r.files[target]==(data if 3<=n<=6 else b'AB'),(n,r.files)
 assert 'SOURCE.ASM' not in r.files and 'RESULT.COM' not in r.files
for image in [(asm/'ASMA0.COM').read_bytes(),(asm/'ASM86A.COM').read_bytes()]:
 for tail in ['ONLY.ASM','A.ASM B.COM EXTRA.TXT','TOOLONGNM.ASM O.COM','A.LONG O.COM','A..ASM O.COM','A.ASM A.ASM','a.asm A.ASM','ASMA.TMP O.COM','A.ASM RESULT.BAK','"A.ASM" O.COM','DIR/A.ASM O.COM','A.ASM O.COM FOUR X']:
  reject(image,tail,{'A.ASM':b'DB 1\r\n','O.COM':b'OLD','ASMA.TMP':b'KEEP'})

ir=ROOT/'workbench/ir86'
for n in range(1,24):
 image=(ROOT/'workbench/toolchain'/f'IW{n:02}.COM').read_bytes()
 data=(ir/f'T{n:02}.IR').read_bytes()
 r=run(image,files={'IN.IR':data,'OUT.ASM':b'OLD'},command_line='IN.IR OUT.ASM')
 assert r.exitcode==0,(n,r.output)
 if n>=3 and n!=4:assert r.files['OUT.ASM']!=b'OLD'
 assert 'SOURCE.IR' not in r.files and 'RESULT.ASM' not in r.files

for family,folder,prefix in [('rill-initial-series','rill0','R'),('rill-seed-series','toolchain','RB'),('rill-self-series','toolchain','RC')]:
 for c in json.loads((ROOT/'qa/toolchain'/(family+'.json')).read_text()):
  if c.get('fixture') is None and c.get('fragment') is None:continue
  image=(ROOT/'workbench'/folder/f'{prefix}{c["number"]:02}.COM').read_bytes()
  r=run(image,files={'IN.RIL':(c.get('fixture') or '').encode(),'OUT.IR':b'OLD'},command_line='IN.RIL OUT.IR')
  assert r.exitcode==c.get('accept_exit',0),(family,c['number'],r.output)
  if c.get('fragment') is not None:assert r.files['OUT.IR']==c['fragment'].encode(),(family,c['number'],r.files)
  if c['key'].upper()=='MAIN':assert b'OK OUT.IR ' in r.output
  assert 'SOURCE.RIL' not in r.files and 'RESULT.IR' not in r.files

tools=ROOT/'workbench/toolchain'
for name,source,dest,text in [('RILL','IN.RIL','OUT.IR','fn main(){return 0;}'),('IR86','IN.IR','OUT.ASM','PROC MAIN 0 0\nLIT 0\nRETURN\n'),('ASM86A','IN.ASM','OUT.COM','DB 65,66\n')]:
 image=(tools/(name+'.COM')).read_bytes()
 r=run(image,files={source:text.encode(),dest:b'OLD'},command_line=source+' '+dest)
 assert r.exitcode==0 and r.files[dest]!=b'OLD' and ('OK '+dest+' ').encode() in r.output,(name,r.output)
 for tail in [source,source+' '+source,source+' '+dest+' EXTRA']:
  reject(image,tail,{source:text.encode(),dest:b'OLD'})
from portable import Machine
ir_source='PROC MAIN 0 0\nARGC\nPUSH\nLIT 2\nCNE\nJNZ BAD\nLIT 2\nARG\nFETCHB\nRETURN\nLABEL BAD\nLIT 1\nRETURN\n'
for base in (0x2000,0x4000):
 p=Machine(arguments=('ONE.ASM','TWO.COM'),data_base=base).run(ir_source)
 assert p.exitcode==ord('T')
 p=Machine(arguments=('ONE.ASM',),data_base=base).run('PROC MAIN 0 0\nLIT 2\nARG\nSTATUS\nRETURN\n')
 assert p.exitcode==1
passed('PASS PSP filenames: all native assembler/IR stages, compiler file stages, and RILL-written trio; malformed tails and collision preservation')

if (ROOT/'workbench/link86/LINK86.COM').exists():
 folder=ROOT/'workbench/link86'
 for n in range(1,11):
  image=(folder/f'L{n:02}.COM').read_bytes()
  c=json.loads((ROOT/'qa/link86/checkpoints.json').read_text())[n-1]
  files={'ONE.OBJ':(folder/f'M{n:02}.OBJ').read_bytes(),'TWO.OBJ':(folder/f'U{n:02}.OBJ').read_bytes() if c['util'] is not None else b'OBJ1\r\nEND\r\n','OUT.COM':b'OLD'}
  r=run(image,files=files,command_line='ONE.OBJ TWO.OBJ OUT.COM')
  assert r.exitcode==0,(n,r.output)
  if c['expected'] is not None:assert r.files['LINK.TMP' if n==5 else 'OUT.COM']==bytes.fromhex(c['expected'])
  assert 'MAIN.OBJ' not in r.files and 'UTIL.OBJ' not in r.files and 'RESULT.COM' not in r.files
 passed('PASS LINK86: all stages read PSP-selected modules and publish the selected result')

if (ROOT/'workbench/edit86/EDIT86.COM').exists():
 sys.path.insert(0,str(ROOT/'qa/edit86'))
 from editor_machine import EditorMachine,key
 image=(ROOT/'workbench/edit86/EDIT86.COM').read_bytes()
 r=EditorMachine({'TEST.ASM':b'original'},keys=[key(ord('!')),key(265),key(266)],command_line='TEST.ASM').run(image,limit=2_000_000_000)
 assert r.exitcode==0 and r.files['TEST.ASM']==b'!original' and 'EDIT.TXT' not in r.files,r.output
 assert any(b'TEST.ASM' in row for row in r.screen_log)
 assert not r.allocations
 reject(image,'EDIT.TMP',{'EDIT.TMP':b'KEEP'})
 translator=(ROOT/'workbench/edit86/IRED.COM').read_bytes()
 binding=(ROOT/'workbench/edit86/EDITRT.ASM').read_bytes()
 r=run(translator,files={'IN.IR':b'PROC MAIN 0 0\nLIT 0\nRETURN\n','BIND.ASM':binding},command_line='IN.IR OUT.ASM BIND.ASM')
 assert r.exitcode==0 and r.files['OUT.ASM'].endswith(binding),r.output
 passed('PASS EDIT86: selected source is displayed, edited and saved directly; recovery names are refused')
(ROOT/'qa/command-file-results.txt').write_text('\n'.join(reports)+'\n')
