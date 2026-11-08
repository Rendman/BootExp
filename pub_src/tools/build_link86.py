"""Arrange authored RILL procedures as the first LINK86 construction."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/link86';Q=ROOT/'qa/link86'
for p in [W,Q]:p.mkdir(parents=True,exist_ok=True)
source=(ROOT/'tools/link86.ril').read_text()
a=source.index('fn main(');declarations=source[:a].splitlines()
parts=re.split(r'(?m)(?=^fn )',source[a:]);procs={re.match(r'fn (\w+)',p)[1]:p.rstrip()+'\n' for p in parts if p.strip()}
def dos(name,s):(W/name).write_bytes(s.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
EMPTY='OBJ1\nEND\n'
LITERAL='OBJ1\nB B8 00 4C CD 21\nEND\n'
RELMAIN='OBJ1\nB E8\nR VALUE\nB B4 4C CD 21\nEND\n'
RELUTIL='OBJ1\nP VALUE 0000\nB 33 C0 C3\nEND\n'
ABSMAIN='OBJ1\nB BA\nA TEXT\nB B4 09 CD 21 B8 00 4C CD 21\nEND\n'
ABSUTIL='OBJ1\nP TEXT 0000\nB 48 49 0D 0A 24\nEND\n'
SIMPLEFAIL='fn fail(code){if inopen{close(input);}exit(1);return 0;}\n'
SINGLEOPEN='fn openunit(){input=open("MAIN.OBJ");if status(){fail(6);}inopen=1;return 0;}\n'
NOSYMBOLS=procs['main'].replace('    table=alloc(10240);if status(){fail(6);}\n','').replace('            modulecheck(size);\n','')
a=NOSYMBOLS.index('    unit=0;line=0;let mut i=0;');b=NOSYMBOLS.index('    commit();',a)
NOSYMBOLS=NOSYMBOLS[:a]+'    unit=0;line=0;finishout();\n'+NOSYMBOLS[b:]
RELREF=procs['reference'].replace('fn reference(kind)','fn reference()').replace('        if kind==82{value=value-(256+pc+2);}', '        value=value-(256+pc+2);')
# main bodies are complete retained tool/diagnostic entry points, never byte encoders.
MAINS={
1:'fn main(){openunit();closein();return 0;}\n',
2:'fn main(){openunit();let mut count=0;while nextbyte()!=65535{count=count+1;}closein();return count!=11;}\n',
3:'fn main(){openunit();let mut count=0;while readline(){count=count+1;}closein();return count!=2;}\n',
4:'fn main(){openunit();records();closein();return 0;}\n',
5:'fn main(){preflight();pass=2;openunit();createout();records();closein();finishout();print("OK LINK.TMP ");number(pc);print(" bytes\\r\\n");return 0;}\n',
6:'fn main(){preflight();pass=2;openunit();createout();records();closein();unit=0;line=0;finishout();commit();report();return 0;}\n',
7:NOSYMBOLS,
}
TITLES=['Opening the first object','Refilling a bounded input block','Reading one physical record','Recognizing the object envelope','Writing literal bytes','Publishing the accepted image','Placing two modules','Recording public names','Calling into another module','Taking an address from another module']
WHY=[
'Open MAIN.OBJ read-only and close its owned handle. Fixed work files keep console parsing out of the linker.',
'Read through a 1024-byte block and consume every positive read before refilling. Zero count is EOF; Control-Z ends object text.',
'Bound a physical record to 120 characters, count its line, and accept ordinary DOS text endings without retaining the complete object.',
'Recognize OBJ1 and END, including blank lines and semicolon comments. Reject unknown records instead of silently copying malformed text.',
'Decode up to sixteen hexadecimal bytes in a B record and stream them to an owned LINK.TMP. Inspect that file before deleting it.',
'Publish a closed temporary file as RESULT.COM, retaining the accepted image on source rejection and recovery files after a failed restoration.',
'Place MAIN.OBJ first and UTIL.OBJ second. Count both modules on pass one, then reopen them and stream the same layout on pass two.',
'Record complete public spellings and module-relative offsets in initialized forty-byte records. Check duplicates, extents and pass agreement.',
'Resolve R records into near-relative words while streaming. A saved definition supplies the target even when the defining module follows the caller.',
'Resolve A records into loaded word addresses. Keep relative displacements and absolute addresses distinct even though each occupies two output bytes.',
]
records=[]
for n,title in enumerate(TITLES,1):
 code=dict(procs);code['main']=MAINS.get(n,procs['main'])
 if n==1:code['openunit']=SINGLEOPEN
 if n<=2:code['fail']=SIMPLEFAIL
 elif n<5:code['fail']='fn fail(code){if inopen{close(input);inopen=0;}print("LINK ERROR ");number(unit);putc(32);number(line);print(" CODE ");number(code);print("\\r\\n");exit(1);return 0;}\n'
 elif n<8:code['fail']=procs['fail'].replace('    if table{free(table);table=0;}\n','')
 if n==5:code['preflight']='fn preflight(){if exists("LINK.TMP"){fail(8);}if status(){fail(6);}return 0;}\n'
 branches=[]
 if n>=5:branches.append(('B','bytesrecord();'))
 if n>=8:branches.append(('P','definition();'))
 if n>=9:branches.append(('R','reference();' if n==9 else 'reference(82);'))
 if n>=10:branches.append(('A','reference(65);'))
 dispatch='fail(1);'
 for name,body in reversed(branches):dispatch='if same("'+name+'"){'+body+'}else{'+dispatch+'}'
 start=code['records'].index('                    if same("B")');end=code['records'].index('\n                }',start)
 code['records']=code['records'][:start]+'                    '+dispatch+code['records'][end:]
 if n==9:code['reference']=RELREF
 selected={'main'}
 while True:
  plain=re.sub(r'"(?:\\.|[^"\\])*"','""','\n'.join(code[k] for k in selected))
  refs=set(re.findall(r'\b(\w+)\s*\(',plain))&set(code)
  if refs<=selected:break
  selected|=refs
 plain=re.sub(r'"(?:\\.|[^"\\])*"','""','\n'.join(code[k] for k in selected))
 words=set(re.findall(r'\b\w+\b',plain))
 data=[line for line in declarations if (m:=re.match(r'(?:let mut|bytes) (\w+)',line)) and m[1] in words]
 program='// LINK86 construction checkpoint.\n'+'\n'.join(data)+'\n'+'\n'.join(code[k] for k in procs if k in selected)
 name=f'L{n:02}.RIL';dos(name,program)
 main=EMPTY if n<=4 else LITERAL
 util=None if n<=6 else EMPTY
 expected=None if n<=4 else 'B8 00 4C CD 21'
 if n==7:util='OBJ1\nB 41 42\nEND\n';expected+=' 41 42'
 if n==8:util='OBJ1\nP LETTER 0000\nB 41\nEND\n';expected+=' 41'
 if n==9:main=RELMAIN;util=RELUTIL;expected='E8 04 00 B4 4C CD 21 33 C0 C3'
 if n==10:main=ABSMAIN;util=ABSUTIL;expected='BA 0C 01 B4 09 CD 21 B8 00 4C CD 21 48 49 0D 0A 24'
 if n<=2:bad=None;badcode=None
 elif n==3:bad='X'*121+'\n';badcode=5
 elif n==4:bad='OBJ2\nEND\n';badcode=1
 elif n==5:bad='OBJ1\nB 0G\nEND\n';badcode=2
 elif n==6:bad='OBJ1\nB 90\nEND\nB 90\n';badcode=1
 elif n==7:bad='OBJ1\nB 90\n';badcode=1
 elif n==8:bad='OBJ1\nP SAME 0000\nP SAME 0000\nEND\n';badcode=3
 elif n==9:bad=RELMAIN.replace('R VALUE','R LOST');badcode=3
 else:bad=ABSMAIN.replace('A TEXT','A LOST');badcode=3
 dos(f'M{n:02}.OBJ',main)
 if util is not None:dos(f'U{n:02}.OBJ',util)
 if bad is not None:dos(f'X{n:02}.OBJ',bad)
 records.append(dict(number=n,title=title,why=WHY[n-1],source=name,main=main,util=util,bad=bad,code=badcode,expected=expected,output_file=None if n<=4 else 'LINK.TMP' if n==5 else 'RESULT.COM',program_output='' if n==9 else 'HI\r\n' if n==10 else None))
dos('LINK86.RIL',(W/'L10.RIL').read_text())
(Q/'checkpoints.json').write_text(json.dumps(records,indent=2)+'\n')
print('Prepared ten authored LINK86 checkpoints; final source',len(program.splitlines()),'lines')
