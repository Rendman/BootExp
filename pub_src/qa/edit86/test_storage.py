"""Check service boundaries, bounded undo and actual workbench source round trips."""
import zipfile,json
from services import ROOT,W,Q,TOOLS,build
from editor_machine import EditorMachine,key
image=(W/'EDIT86.COM').read_bytes();logs=[]
def passed(s):logs.append('PASS '+s);print(logs[-1],flush=True)
def execute(text,events):
 r=EditorMachine({'EDIT.TXT':text},keys=[key(k) for k in events]).run(image,limit=2000000000)
 assert r.exitcode==0 and not r.allocations and not r.keys,(r.exitcode,r.output)
 assert r.files['EDIT.TXT']==text
 return r
# The exact delivered source archive is the input corpus, not a model of text.
largest=0;members=0
for archive in sorted((ROOT/'site/static/downloads/tools').glob('*/*.ZIP')):
 with zipfile.ZipFile(archive) as z:
  for info in z.infolist():assert info.file_size<=262144;members+=1;largest=max(largest,info.file_size)
  name=max(z.infolist(),key=lambda v:v.file_size).filename
  execute(z.read(name),[271,270,265,266])
passed(f'largest source from every collection round-trips byte-for-byte; all {members} archive members fit; largest {largest} bytes')
ir,asm,assembler=build((TOOLS/'ASM86A.RIL').read_bytes())
assert assembler==(TOOLS/'ASM86A.COM').read_bytes()
_,editor_asm,extended_ir=build((W/'IRED.RIL').read_bytes(),(W/'RILLED.COM').read_bytes(),(W/'IRED.COM').read_bytes())
assert extended_ir==(W/'IRED.COM').read_bytes()
asm=max([asm,editor_asm],key=len)
execute(asm,[271,270,265,266])
passed(f'actual {len(asm)}-byte generated toolchain assembly edits/saves beyond 64 KiB')
events=([ord('x'),8]*1024)+[ord('x')]+[267]*2049+[265,266]
r=EditorMachine({'EDIT.TXT':b''},keys=[key(k) for k in events]).run(image,limit=2000000000)
assert r.exitcode==0 and r.files['EDIT.TXT']==b'x' and not r.allocations
assert any(b'No earlier edit remains' in screen for screen in r.screen_log[-3:])
passed('2048-record undo ring overwrites only the oldest edit and refuses an extra undo')
r=EditorMachine({},keys=[ord('x'),key(265),key(266)]).run(image)
assert r.exitcode==0 and r.files=={'EDIT.TXT':b'x'} and not r.allocations
def inject(machine):machine.files['EDIT.TMP']=b'RECOVERY';return key(265)
r=EditorMachine({'EDIT.TXT':b'old'},keys=[ord('!'),inject,key(266),ord('q')]).run(image)
assert r.exitcode==0 and r.files=={'EDIT.TXT':b'old','EDIT.TMP':b'RECOVERY'}
passed('new-document creation and recovery-name recheck immediately before saving')
r=EditorMachine({'EDIT.TXT':b'A'*65537},keys=[key(271),ord('!'),key(265),key(266)]).run(image,limit=2000000000)
assert r.exitcode==0 and r.files['EDIT.TXT']==b'A'*65537+b'!' and not r.allocations
passed('long-line visual columns and horizontal scroll beyond 65535 cells without truncation')
source=b'''bytes data[6];
fn main(){
 let mut h=alloc(64);let mut j=alloc(64);let mut bad=status();
 blockload(h,0,"ABCDEF",6);bad=bad|status();blockload(j,0,"XXXXXX",6);bad=bad|status();
 blockload(h,0,65535,2);if status()==0{bad=1;}
 blockmove(h,0,j,63,2);if status()==0{bad=1;}
 blockread(j,0,data,6);bad=bad|status();let mut n=0;while n<6{if data[n]!=88{bad=1;}n=n+1;}
 blockmove(h,0,j,0,6);bad=bad|status();blockread(j,0,data,6);bad=bad|status();
 n=0;while n<6{if data[n]!=load8("ABCDEF"+n){bad=1;}n=n+1;}
 blockread(h,0,65535,2);if status()==0{bad=1;}
 blockread(h,64,data,0);if status()==0{bad=1;}
 free(h);bad=bad|status();free(j);bad=bad|status();
 vbegin();bad=bad|status();vpos(1999);vwrite("AB",2);if status()==0{bad=1;}
 vpos(0);vwrite(65535,2);if status()==0{bad=1;}
 n=256;while n<272{if key()!=n{bad=1;}n=n+1;}
 if key()!=265{bad=1;}if key()!=266{bad=1;}if key()!=267{bad=1;}
 vend();return bad|status();
}
'''
_,_,probe=build(source,(W/'RILLED.COM').read_bytes(),(W/'IRED.COM').read_bytes())
r=EditorMachine(keys=[key(n) for n in range(256,272)]+[19,17,26]).run(probe)
assert r.exitcode==0 and not r.allocations and not r.keys,(r.exitcode,r.output)
passed('complete key map/control aliases, cross-block copying, rejected destination extents and near-address wraps')
assert (W/'E20.COM').read_bytes()==image
passed('formatted reader source and authored editor produce identical executable bytes')
(Q/'storage-results.txt').write_text('\n'.join(logs)+'\n')
