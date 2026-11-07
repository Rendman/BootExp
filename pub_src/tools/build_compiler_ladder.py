"""Build one continuing IR-written compiler manuscript from shared authored routines."""
from pathlib import Path
import json,re
from copy import deepcopy
from compiler_profiles import ROOT,PROCS,ALIAS,profile,render,main_record_profile
import compiler_lessons as lessons
W=ROOT/'workbench/toolchain';Q=ROOT/'qa/toolchain';R=ROOT/'workbench/rill'
def dos(p,s):p.write_bytes(s.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))

def build():
 p=profile(0);needed=set(re.findall(r'^PROC (\w+)',render(p),re.M))|{'SETIDENT'};entries=[]
 for old in lessons.entries:
  e=deepcopy(old);key=e['key']
  if key not in needed or key=='LEX' and e['variant']=='full':continue
  if key=='PRIMARY' and e['variant']=='values':
   e.update(title='Parenthesized values',fixture='(1+2)',fragment='LIT 00001\r\nPUSH\r\nLIT 00002\r\nADD\r\n')
  if key=='PREC':
   e.update(fixture='+',title='Addition and comparison precedence',check_value=6)
   e['body']=e['body'].replace('LIT 7\nCNE\nRETURN','LIT 6\nCNE\nRETURN')
  if key=='EXPR':
   e.update(fixture='1+2-3',fragment='LIT 00001\r\nPUSH\r\nLIT 00002\r\nADD\r\nPUSH\r\nLIT 00003\r\nSUB\r\n')
  if key in ['RESOLVEOPTIONAL','PRIMARY'] and (key!='PRIMARY' or e['variant']=='full'):
   e['body']=e['body'].replace(lessons.record,lessons.record.replace('LIT 1\nST RECTYPE','LIT 5\nST RECTYPE').replace('LIT 12345\nST RECVAL','LIT 0\nST RECVAL').replace('LIT 0\nPUSH\nINVOKE RECORD 1','LIT 20480\nPUSH\nINVOKE RECORD 1').replace('ST GLOBALS','ST LOCALCOUNT'))
  if key=='PRIMARY' and e['variant']=='full':e.update(fragment='LOCAL 00000\r\nPUSH\r\nLIT 00001\r\nADD\r\n',title='Reading a local binding')
  if key=='RESOLVEOPTIONAL':
   e.update(check_value=5,title='Finding a local or builtin')
   e['body']=e['body'].replace('LIT 1\nCNE\nRETURN','LIT 5\nCNE\nRETURN')
  if key=='MAIN':e.update(title='The first complete compiler',body=None)
  entries.append(e)
 current={};cases=[]
 for n,e in enumerate(entries,1):
  key=e['key']
  if key=='LEX':
   current[key]=lessons.lexer(e['variant'])
  elif key=='EXPR':current[key]=p[key];current['PRIMARY']=lessons.primary('numeric')
  elif key=='PRIMARY':
   b=p[key]
   if e['variant']=='values':
    a=b.index('CALL RESOLVEOPTIONAL\n');end=b.index('LABEL PRIMARYNUM\n');b=b[:a]+'JMP NAMEFAIL\n'+b[end:]
   current[key]=b
  else:current[key]=p[key]
  if key=='MAIN':program=render(p,extra=('SETIDENT',))
  else:
   body=dict(current);body['MAIN']='PROC MAIN 0 0\n'+e['body']
   # Later routines fail explicitly until their own construction installment.
   refs=set(re.findall(r'^(?:CALL|INVOKE) (\w+)',ALIAS+'\n'.join(body.values()),re.M))
   for name in refs-set(body):
    argc=int(PROCS[name].splitlines()[0].split()[2])
    body[name]=f'PROC {name} {argc} 0\nLIT 2\nPUSH\nINVOKE ERROR 1\nLIT 0\nRETURN\n' if name!='ERROR' else 'PROC ERROR 1 0\nLIT 1\nEXIT\n'
   program=render(body,extra=tuple(current))
  source=f'R{n:02}.IR';dos(R/source,program)
  if e['fixture'] is not None:dos(R/f'T{n:02}.RIL',e['fixture']+'\n')
  if e['bad'] is not None:dos(R/f'X{n:02}.RIL',e['bad']+'\n')
  cases.append({**e,'number':n,'source':source})
 dos(R/'RILL.IR',render(p,extra=('SETIDENT',)))
 (Q/'rill-initial-series.json').write_text(json.dumps(cases,indent=2)+'\n')
 # Each continuation remains a complete compiler for the preceding subset.
 fixtures=[('Multiply, divide, and remainder','fn main(){putc(13*5);}', 'A'),
 ('Word masks and comparison values','fn main(){putc((130>>1)|0);}', 'A'),
 ('Quoted text and byte loads','fn main(){putc(load8("A"));}', 'A'),
 ('Global mutable words','let mut x=65;fn main(){putc(x);}', 'A'),
 ('Global byte buffers','bytes b[2];fn main(){b[0]=65;putc(b[0]);}', 'A'),
 ('Recording the main procedure','fn main(){putc(65);}', 'A'),
 ('Named procedures','fn main(){putc(value());}fn value(){return 65;}', 'A'),
 ('Parameters and recursion','fn main(){putc(twice(32)+1);}fn twice(x){return x*2;}', 'A'),
 ('Counted file services','fn main(){putc(65);}', 'A'),
 ('Publishing accepted files','fn main(){putc(65);}', 'A'),
 ('Allocated workspace','fn main(){let mut h=alloc(100);free(h);return status();}', ''),
 ('Checked workspace access','fn main(){let mut h=alloc(100);set8(h,0,65);putc(get8(h,0));free(h);return 0;}', 'A')]
 explanations=[
 'Add unsigned multiply, quotient, and remainder to the existing precedence parser. The IR runtime rejects a zero divisor; word products wrap.',
 'Add masks, logical right shift, and logical negation. Comparison values are zero or one. These are the bit operations used in the compiler source.',
 'Keep quoted source bytes separate from folded names. Compile a string pointer and read its bytes through load8; no printing operation is hidden in a literal.',
 'Add global mutable words with literal initializers. Reuse the initialized symbol records and resolve a visible local before a global.',
 'Add global byte buffers and indexed reads and stores. The program owns its index bounds; allocated blocks use a different checked interface.',
 'Give main an initialized procedure record and emit its body through FUNCTION. Its entry wrapper invokes that body with zero arguments; the accepted one-main language remains intact.',
 'Record named zero-argument procedures and pending calls. Final acceptance rejects an undefined procedure; main must exist and take no arguments.',
 'Add parameter records and verify call arity. Parameters and local words belong to each call, so recursive procedures preserve their callers.',
 'Add opaque file handles and counted reads and writes. Check service status and exact write progress; a short positive read still contains data.',
 'Add existence, deletion, and rename for recoverable publication. Temporary ownership and the previous accepted result remain distinct states.',
 'Allocate workspace through an opaque block handle. A block is separate from ordinary pointers into the program image; check status before using it.',
 'Access allocated blocks through checked byte offsets. A canonical word needs two valid bytes; the symbol record layout stays unchanged.'
 ]
 seed=[]
 for n,(title,fixture,output) in enumerate(fixtures,1):
  level=n if n<6 else n-1
  files={};result_file=None;result_data=None
  if level==8:
   fixture=next(c['source'] for c in json.loads((ROOT/'tools/toolchain_examples.json').read_text()) if c['name']=='ECOPY')
   files={'IN.TXT':'A short copy.\r\n'};result_file='OUT.TXT';result_data=files['IN.TXT'];output=''
  if level==9:
   fixture='bytes b[1];\nfn main(){\n b[0]=65;\n delete("OLD.TXT");if status(){return 1;}\n let mut h=create("TEMP.TXT");if status(){return 1;}\n if write(h,b,1)!=1{return 1;}\n close(h);if status(){return 1;}\n rename("TEMP.TXT","OLD.TXT");if status(){return 1;}\n if exists("TEMP.TXT"){return 1;}\n return exists("OLD.TXT")!=1;\n}'
   files={'OLD.TXT':'old\r\n'};result_file='OLD.TXT';result_data='A';output=''
  if level==11:
   fixture='fn main(){\n let mut h=alloc(100);if status(){return 1;}\n set16(h,98,4660);if status(){free(h);return 1;}\n let mut n=get16(h,98);\n set8(h,0,65);putc(get8(h,0));\n free(h);return n!=4660;\n}'
  source=f'RB{n:02}.IR';dos(W/source,render(main_record_profile() if n==6 else profile(level),extra=('SETIDENT',)));dos(W/f'TRB{n:02}.RIL',fixture+'\n')
  bad='fn main(){putc(65536);}'
  dos(W/f'XRB{n:02}.RIL',bad+'\n')
  seed.append(dict(number=n,key='MAIN',title=title,source=source,fixture=fixture,bad=bad,code=3,complete=True,expected='',fragment=None,program_output=output,why=explanations[n-1],files=files,result_file=result_file,result_data=result_data))

 dos(R/'RILLBOOT.IR',render(profile(11)));dos(W/'RILLBOOT.IR',render(profile(11)))
 (Q/'rill-seed-series.json').write_text(json.dumps(seed,indent=2)+'\n')
 print('Prepared',len(cases),'RILL0 checkpoints and',len(seed),'continuing RILLBOOT checkpoints')
if __name__=='__main__':build()
