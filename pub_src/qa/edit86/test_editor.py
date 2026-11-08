"""Execute EDIT86's real 8086 image, including its BIOS and DOS boundaries."""
from pathlib import Path
import json,sys
from services import ROOT,W,Q,build
from editor_machine import EditorMachine,key
from unicorn.x86_const import *

ir,asm,image=build((ROOT/'tools/edit86.ril').read_bytes(),(W/'RILLED.COM').read_bytes(),(W/'IRED.COM').read_bytes())
(W/'EDIT86.COM').write_bytes(image)
(Q/'editor-facts.json').write_text(json.dumps(dict(ir_bytes=len(ir),assembly_bytes=len(asm),binary_bytes=len(image),binary_hex=image[:32].hex(' ').upper()),indent=2)+'\n')
logs=[]
def passed(s):logs.append('PASS '+s);print(logs[-1],flush=True)
def execute(text=b'',events=(266,),files=None,cls=EditorMachine,**kwargs):
 f={'EDIT.TXT':text};f.update(files or {})
 r=cls(f,keys=[key(e) if isinstance(e,int) else e for e in events],**kwargs).run(image,limit=2000000000)
 assert r.exitcode==0,(r.exitcode,r.output)
 assert not r.allocations,('allocation leak',r.allocations)
 assert not r.keys,('unused events',r.keys)
 return r
def edited(text,events,expected,**kwargs):
 r=execute(text,events+[265,266],**kwargs)
 assert r.files['EDIT.TXT']==expected,(text[:80],events,r.files['EDIT.TXT'][:100],expected[:100])
 assert 'EDIT.TMP' not in r.files and 'EDIT.BAK' not in r.files,r.files.keys()
 return r

r=execute(b'hello\r\nworld\r\n');assert r.screen_log[0][:5]==b'hello' and r.screen_log[0][80:85]==b'world'
assert len([o for o in r.operations if o[0]=='allocate'])==9
r=execute(b'\tABC\x00\x1a\xff\r\n',mode=7);assert r.screen_log[0][:14]==b'        ABC...'
passed('color/monochrome screen, literal control-byte display, nine checked allocations and release')
for text in [b'',b'ABC',b'a\rb\nc\r\nd',bytes(range(256)),b'\t'*100+b'x'*200+b'\nlast']:
 edited(text,[],text)
edited(b'ABC',[ord('x'),ord('y'),256,264,13,9,ord('Z'),8],b'x\r\n\tABC')
edited(b'A\r\nB\nC\rD',[257,257,8,267,257,264,267],b'A\r\nB\nC\rD')
edited(b'abcdef',[271,8,8,267,267,270,264,267],b'abcdef')
passed('lossless saves, insertion, CR/LF pairs, bare endings, deletion and single-edit undo')
edited(b'123456789\nxx\nabcdefghij',[261,259,259,ord('!')],b'123456789\nxx\nabcdefghi!j')
edited(b'A\tB\n1234567890',[261,259,ord('!')],b'A\tB\n123456789!0')
edited(b'A\nB\nC',[271,258,260,ord('!')],b'A\n!B\nC')
r=edited(b'\n'.join(f'row{i:02}'.encode() for i in range(60)),[263,262,271,270],b'\n'.join(f'row{i:02}'.encode() for i in range(60)))
assert r.screen_log[1][:5]==b'row01',r.screen_log[1][:80]
r=edited(b'X'*200,[261,ord('!')],b'X'*200+b'!');assert r.cursor==0 # restored original BIOS cursor on exit
passed('preferred visual column, tabs, Home/End, document ends, paging, vertical/horizontal viewport')
events=[268]+list(b'needle')+[13,ord('!'),269,ord('?')]
edited(b'needle first\nneedle last',events,b'!needle first\n?needle last')
edited(b'abc',[268,ord('x'),27,ord('!')],b'!abc')
r=execute(b'original',[ord('!'),266,27,266,ord('q')]);assert r.files['EDIT.TXT']==b'original'
r=execute(b'original',[ord('!'),266,ord('s')]);assert r.files['EDIT.TXT']==b'!original'
passed('literal search/find-next, search cancel, quit cancel/discard/save')

# DOS may return short positive reads; page fills must not cross allocations.
class ShortRead(EditorMachine):
 def interrupt(self,c,num,unused):
  if num==0x21 and c.reg_read(UC_X86_REG_AH)==0x3f:c.reg_write(UC_X86_REG_CX,min(c.reg_read(UC_X86_REG_CX),997))
  super().interrupt(c,num,unused)
text=(b'abcd\r\n'*12000)+b'last'
edited(text,[271,ord('!'),270,ord('?'),267],text+b'!',cls=ShortRead)
# Cross both the 32 KiB page and 64 KiB word boundaries, and save a live middle gap.
text=b'0123456789\n'*13000
edited(text,[271,8,ord('!'),270,ord('?'),267,263,ord('@'),267],text[:-1]+b'!')
text=b'A'*32766+b'needle\n'+b'B\n'*20000
edited(text,[268]+list(b'needle')+[13,ord('!')],text[:32766]+b'!'+text[32766:])
passed('short reads, page-spanning search and gap transfers, source larger than 128 KiB, live-gap save')
text=(b'line\r\n'*(262144//6+1))[:262144]
edited(text,[ord('!'),271,8,ord('!')],text[:-1]+b'!')
r=EditorMachine({'EDIT.TXT':text+b'X'},keys=[]).run(image,limit=2000000000)
assert r.exitcode==1 and r.files['EDIT.TXT']==text+b'X' and not r.allocations and b'exceeds' in r.output
passed('exact 256 KiB capacity, refused growth, deletion/replacement, oversized input preserves original')

for reserved in ['EDIT.TMP','EDIT.BAK']:
 r=EditorMachine({'EDIT.TXT':b'old',reserved:b'RECOVERY'}).run(image)
 assert r.exitcode==1 and r.files[reserved]==b'RECOVERY' and r.files['EDIT.TXT']==b'old' and not r.allocations
class Fault(EditorMachine):
 which=None
 def interrupt(self,c,num,unused):
  ah=c.reg_read(UC_X86_REG_AH)
  if num==0x21 and ah==self.which and (ah!=0x40 or c.reg_read(UC_X86_REG_BX)>2):
   c.reg_write(UC_X86_REG_AX,0 if ah==0x40 else 5);self.carry(ah!=0x40);return
  super().interrupt(c,num,unused)
for function in [0x3c,0x40,0x56]:
 class F(Fault):which=function
 r=execute(b'old',[ord('!'),265,266,ord('q')],cls=F)
 assert r.files['EDIT.TXT']==b'old' and 'EDIT.TMP' not in r.files and 'EDIT.BAK' not in r.files
for function in [0x3d,0x3f]:
 class F(Fault):which=function
 r=F({'EDIT.TXT':b'old'}).run(image);assert r.exitcode==1 and not r.allocations and r.files['EDIT.TXT']==b'old'
class LowMemory(EditorMachine):
 def interrupt(self,c,num,unused):
  if num==0x21 and c.reg_read(UC_X86_REG_AH)==0x48 and len(self.allocations)==3:
   c.reg_write(UC_X86_REG_AX,8);self.carry(True);return
  super().interrupt(c,num,unused)
r=LowMemory({'EDIT.TXT':b'old'}).run(image);assert r.exitcode==1 and not r.allocations and not r.keys
r=EditorMachine({'EDIT.TXT':b'old'},mode=1).run(image);assert r.exitcode==1 and not r.allocations
passed('reserved recovery names, read/create/short-write/rename failures, partial allocation cleanup, screen rejection')

class Recovery(EditorMachine):
 restore=False;delete_backup=False
 def interrupt(self,c,num,unused):
  ah=c.reg_read(UC_X86_REG_AH)
  if num==0x21 and ah in [0x56,0x41]:
   name=self.filename(c.reg_read(UC_X86_REG_DS)*16+c.reg_read(UC_X86_REG_DX))
   if (ah==0x56 and not self.delete_backup and (name=='EDIT.TMP' or self.restore and name=='EDIT.BAK')) or (ah==0x41 and self.delete_backup and name=='EDIT.BAK'):
    c.reg_write(UC_X86_REG_AX,5);self.carry(True);return
  super().interrupt(c,num,unused)
r=execute(b'old',[ord('!'),265,266,ord('q')],cls=Recovery);assert r.files['EDIT.TXT']==b'old' and 'EDIT.TMP' not in r.files
class Restore(Recovery):restore=True
r=Restore({'EDIT.TXT':b'old'},keys=[ord('!'),key(265),key(266),ord('q')]).run(image)
assert r.exitcode==1 and r.files['EDIT.BAK']==b'old' and r.files['EDIT.TMP']==b'!old' and 'EDIT.TXT' not in r.files and not r.allocations
class DeleteBackup(Recovery):delete_backup=True
r=DeleteBackup({'EDIT.TXT':b'old'},keys=[ord('!'),key(265),key(266),ord('q')]).run(image)
assert r.exitcode==1 and r.files['EDIT.BAK']==b'old' and r.files['EDIT.TXT']==b'!old' and not r.allocations
passed('backup restoration and explicit retained recovery files when restoration or backup removal fails')
(Q/'test-results.txt').write_text('\n'.join(logs)+'\n')
