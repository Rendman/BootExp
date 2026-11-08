"""Arrange authored editor sources as small, continuing reader checkpoints."""
from pathlib import Path
import re,json
from edit86_format import layout
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/edit86';Q=ROOT/'qa/edit86'
W.mkdir(exist_ok=True);Q.mkdir(exist_ok=True)
def dos(name,s):
 if name.endswith('.RIL'):s=layout(s)
 (W/name).write_bytes(s.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
s=(ROOT/'tools/edit86_runtime.asm').read_text()
roots=['R_VBEGIN','R_VEND','R_EBAD','R_VPOS','R_VWRITE','R_KEY','R_BMOVE','R_BLOAD','R_BREAD','R_COPY','R_VACTIVE','R_VPAGE','R_VOLDPOS','R_VOLDSHAPE','R_VCELL','R_VSEG','R_VBASE','R_KEYMAP','R_MC','R_MS','R_MO','R_DS','R_DO','R_MDH','R_MDO','R_EDOK']
positions=[s.index(x+':') for x in roots]+[len(s)]
parts={k:s[a:b].rstrip()+'\n' for k,a,b in zip(roots,positions,positions[1:])}
selected={'R_VBEGIN','R_VEND','R_EBAD','R_EDOK','R_VACTIVE','R_VPAGE','R_VOLDPOS','R_VOLDSHAPE','R_VCELL','R_VSEG','R_VBASE'}
for n in range(3,8):
 if n==4:selected|={'R_VPOS','R_VWRITE'}
 if n==5:selected|={'R_KEY','R_KEYMAP'}
 if n==6:selected|={'R_BLOAD','R_BREAD','R_COPY','R_MC','R_MS','R_MO','R_DS','R_DO'}
 if n==7:selected|={'R_BMOVE','R_MDH','R_MDO'}
 dos(f'S{n:02}.ASM',''.join(parts[k] for k in roots if k in selected))
dos('EDITRT.ASM',(W/'S07.ASM').read_text())
probes={
3:'fn main(){vbegin();if status(){return 1;}vend();return status();}\n',
4:'fn main(){vbegin();if status(){return 1;}vpos(0);vwrite("EDIT86",6);let mut bad=status();vpos(2000);if status()==0{bad=1;}vend();return bad|status();}\n',
5:'fn main(){vbegin();if status(){return 1;}vpos(0);vwrite("Press F10",9);let mut k=key();vend();return (k!=266)|status();}\n',
6:'bytes data[6];\nfn main(){let mut h=alloc(64);if status(){return 1;}blockload(h,10,"ABCDEF",6);let mut bad=status();blockread(h,10,data,6);bad=bad|status();let mut i=0;while i<6{if data[i]!=load8("ABCDEF"+i){bad=1;}i=i+1;}blockread(h,63,data,2);if status()==0{bad=1;}free(h);return bad|status();}\n',
7:'bytes data[6];\nfn main(){let mut h=alloc(64);if status(){return 1;}blockload(h,0,"ABCDEF",6);blockmove(h,0,h,1,5);let mut bad=status();blockread(h,0,data,6);bad=bad|status();let mut i=0;while i<6{if data[i]!=load8("AABCDE"+i){bad=1;}i=i+1;}blockmove(h,1,h,0,5);bad=bad|status();blockread(h,0,data,6);bad=bad|status();i=0;while i<6{if data[i]!=load8("ABCDEE"+i){bad=1;}i=i+1;}blockmove(h,63,h,0,2);if status()==0{bad=1;}free(h);return bad|status();}\n'}
for n,source in probes.items():dos(f'S{n:02}.RIL',source)
s=(ROOT/'tools/edit86.ril').read_text();a=s.index('fn main(');declarations=s[:a].splitlines()
procs={re.match(r'fn (\w+)',p)[1]:p.rstrip()+'\n' for p in re.split(r'(?m)(?=^fn )',s[a:]) if p.strip()}
INIT='store16(cap+2,4);copypos(gapend,cap);copypos(space,cap);'
LOAD=INIT+'allocate();loadfile();copypos(gap,length);'
CHECK='if reserved(){fatal("Recovery files EDIT.TMP or EDIT.BAK already exist.");}'
SCREEN='copypos(target,top);movegap(target);vbegin();if status(){fatal("EDIT86 requires an 80-column text screen.");}active=1;'
MAINS={
8:'fn main(){store16(cap,65535);add(cap,2);if (load16(cap)!=1)|(load16(cap+2)!=1){return 1;}sub(cap,3);if (load16(cap)!=65534)|(load16(cap+2)!=0){return 1;}copypos(target,cap);add(target,2);difference(work,target,cap);return !before(cap,target)|equal(cap,target)|(load16(work)!=2)|(load16(work+2)!=0);}\n',
9:'fn main(){'+INIT+'allocate();return cleanup();}\n',
10:'fn main(){'+LOAD+'let mut bad=(load16(length)!=10)|(load16(length+2)!=0);zero(target);if before(target,length){bad=bad|(peek(target)!=111);}else{bad=1;}return cleanup()|bad;}\n',
11:'fn main(){'+INIT+CHECK+'allocate();loadfile();copypos(gap,length);let mut saved=savefile();return cleanup()|!saved;}\n',
12:'fn main(){'+INIT+CHECK+'allocate();loadfile();copypos(gap,length);store16(target,5);if before(length,target){fatal("Fixture is shorter than the gap position.");}movegap(target);let mut saved=savefile();return cleanup()|!saved;}\n',
13:'fn main(){'+LOAD+'store16(target,5);linebegin(start,target);lineend(at,start);nextline(other,start);prevline(work,other);let mut bad=(load16(start)!=5)|(load16(at)!=8)|(load16(other)!=10)|(load16(work)!=5);return cleanup()|bad;}\n',
14:'fn main(){'+LOAD+'zero(start);store16(target,3);column(col,start,target);let mut bad=(load16(col)!=9)|(load16(col+2)!=0);store16(prefer,8);toward(target,start,prefer);bad=bad|(load16(target)!=2);return cleanup()|bad;}\n',
15:'fn main(){'+INIT+CHECK+'allocate();loadfile();copypos(gap,length);'+SCREEN+'refresh();let mut k=key();return cleanup()|(k!=266);}\n',
16:'fn main(){'+INIT+CHECK+'allocate();loadfile();copypos(gap,length);'+SCREEN+'while 1{refresh();let mut k=key();if status(){fatal("Keyboard service failed.");}message=0;if k==266{return cleanup();}command(k);}return 0;}\n'}
TITLES=['Teaching RILL the editor services','Binding the new intermediate operations','Taking charge of the text screen','Writing a counted screen row','Reading navigation keys','Transferring bytes between storage blocks','Moving overlapping text safely','Counting past a word boundary','Allocating the document pages','Reading a file into the pages','Saving through a temporary file','Keeping free space at the cursor','Finding physical line boundaries','Measuring columns and tab stops','Painting a window on the document','Moving the insertion position','Inserting text and line endings','Deleting text at either side','Remembering edits for undo','Finding a literal string']
WHY=[
'Keep the established compiler and add only the service names needed by a screen editor. Share the built-in lookup instead of copying its scanner.',
'Define screen positions, key events and bounded transfers in the intermediate language. Keep BIOS calls, native registers and segments inside an explicit target binding.',
'Enter and leave an existing 80-column text mode, preserving its cursor settings. A failed entry must return to DOS without leaving an active screen session.',
'Write a counted span of cells with a stable attribute. Position zero is the upper left; the last status row must not scroll the document.',
'Translate the keyboard into character values and named event numbers. The editor needs arrows and function keys without knowing BIOS scan codes.',
'Copy counted bytes between a near I/O buffer and an allocated block. Validate the complete source and destination extents before changing memory.',
'Move bytes within or between allocated blocks, including overlap. A gap buffer must preserve text when either copy direction overlaps its source.',
'Represent document positions as low and high words. A 256 KiB document needs carry, borrow and complete-position comparisons.',
'Obtain eight separately allocated 32 KiB pages. Release every successful allocation even if a later request fails.',
'Read EDIT.TXT through a 4096-byte buffer into the pages. Count every positive read, distinguish an absent file from an I/O failure, and reject excess input.',
'Write the occupied document ranges into EDIT.TMP and publish a closed file. Preserve the accepted EDIT.TXT and retain recovery files when restoration fails.',
'Move the gap to a requested logical position without changing the document. Clip each transfer at both page boundaries and copy in the safe direction.',
'Locate beginnings and endings without building a full line index. Treat CR/LF as a pair while also accepting bare CR and LF.',
'Count visual columns separately from byte positions. Expand tabs to stops eight columns apart and retain the desired column across unequal line lengths.',
'Draw twenty-four document rows and one status row. Keep a horizontal window for long lines and show control bytes without changing the stored file.',
'Connect navigation keys to the gap and window. Preserve the preferred column for vertical movement and keep the cursor visible after a scroll.',
'Insert printable characters, tabs and CR/LF at the gap. Track unsaved changes and ask before discarding them.',
'Delete one character or one complete line ending. Repaint the affected line, or the window when the line layout changes.',
'Keep a bounded ring of edit records in one extra block. Reverse insertion or deletion without copying the complete document.',
'Find literal text from the current position and repeat the search from the next byte. Search the document through logical positions, including page boundaries.'
]
records=[]
for n in range(1,8):
 records.append(dict(number=n,title=TITLES[n-1],why=WHY[n-1],kind='compiler' if n==1 else 'translator' if n==2 else 'service',source='RILLED.RIL' if n==1 else 'IRED.RIL' if n==2 else f'S{n:02}.ASM',probe=None if n<3 else f'S{n:02}.RIL'))
selected={'main'}
for n in range(8,21):
 code=dict(procs);code['main']=MAINS.get(n,procs['main'])
 if n<19:
  code['allocate']=code['allocate'].replace('    undo=alloc(16384);if status(){fatal("Not enough DOS memory for undo storage.");}return 0;','    return 0;')
  code['release']=code['release'].replace('    if undo{free(undo);if status(){bad=1;}undo=0;}return bad;','    return bad;')
  code['typing']=code['typing'].replace('    remember(1,n,0,0);','    ')
  code['erase']=code['erase'].replace('        remember(2,n,c,d);','        ')
 if n<10:code['cleanup']='fn cleanup(){return release();}\n'
 elif n==10:code['cleanup']='fn cleanup(){let mut bad=0;if inopen{close(input);if status(){bad=1;}inopen=0;}return release()|bad;}\n'
 elif n<15:code['cleanup']=code['cleanup'].replace('    if active{vend();if status(){bad=1;}active=0;}\n','')
 if n>=16:
  lines=code['command'].splitlines();lines=[line for line in lines if not (('askfind()' in line or 'findnext(1)' in line) and n<20) and not ('undone()' in line and n<19) and not (('erase(' in line) and n<18)]
  if n<17:lines=[line for line in lines if 'typing(' not in line][:-1]+['    return 0;','}']
  code['command']='\n'.join(lines)+'\n'
 while True:
  plain=re.sub(r'"(?:\\.|[^"\\])*"','""','\n'.join(code[k] for k in selected))
  refs=set(re.findall(r'\b(\w+)\s*\(',plain))&set(code)
  if refs<=selected:break
  selected|=refs
 plain=re.sub(r'"(?:\\.|[^"\\])*"','""','\n'.join(code[k] for k in selected));words=set(re.findall(r'\b\w+\b',plain))
 data=[line for line in declarations if (m:=re.match(r'(?:let mut|bytes) (\w+)',line)) and m[1] in words]
 program='// EDIT86 construction checkpoint.\n'+'\n'.join(data)+'\n'+'\n'.join(code[k] for k in procs if k in selected)
 dos(f'E{n:02}.RIL',program)
 fixture='T\tX\r\nabc\r\n' if n==14 else 'one\r\ntwo\r\n'
 dos(f'T{n:02}.TXT',fixture)
 records.append(dict(number=n,title=TITLES[n-1],why=WHY[n-1],kind='editor',source=f'E{n:02}.RIL',fixture=f'T{n:02}.TXT'))
dos('EDIT86.RIL',program)
assert [x for x in program.splitlines()[1:] if x.strip()]==[x for x in s.splitlines()[1:] if x.strip()],'final editor lost source continuity'
(Q/'checkpoints.json').write_text(json.dumps(records,indent=2)+'\n')
dos('P01.RIL','fn main(){vbegin();vend();return 0;}\n')
dos('Q01.RIL','fn main(){vpos();return 0;}\n')
dos('P02.RIL','fn main(){return 0;}\n')
dos('Q02.IR','PROC MAIN 0 0\nBMOVE\nRETURN\n')
dos('S02.ASM','')
print('Prepared editor service and continuing document checkpoints')
