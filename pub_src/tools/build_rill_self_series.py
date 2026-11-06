"""Select authored RILL procedures and authored diagnostics into buildable source steps."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/toolchain';Q=ROOT/'qa/toolchain'
s=(ROOT/'tools/rill_self.ril').read_text();start=s.index('fn main(');data=s[:start];pieces=re.split(r'(?m)(?=^fn )',s[start:]);procs={re.match(r'fn (\w+)',p)[1]:p for p in pieces if p.strip()};args={n:re.match(r'fn \w+\(([^)]*)\)',p)[1].split(',') for n,p in procs.items()};args={n:[a.strip() for a in v if a.strip()] for n,v in args.items()}
entries=[]
def add(key,title,body,expected='',fixture=None,bad=None,code=None,fragment=None,complete=False):entries.append(dict(key=key,title=title,body=body,expected=expected,fixture=fixture,bad=bad,code=code,fragment=fragment,complete=complete))
setup='table=alloc(22000);'
record='setident("ABC");rectype=1;recval=12345;reclevel=0;record(0);globals=1;'
opened='output=create("RILL.TMP");own=1;'
read='input=open("SOURCE.RIL");if status(){fail(1);}next();lex();'
closed='flush();close(output);output=0;own=0;print("OK RILL.TMP\\r\\n");return 0;'
exprdriver=setup+record+opened+read+'expr(1);if tok!=0{fail(2);}'+closed
add('print','Read a text pointer in RILL','print("HI");return 0;','HI')
add('printnum','Word formatting with local state','printnum(65535);return 0;','65535')
add('print32','Portable paired-word counting','print32(1,1);return 0;','0000065537')
add('fail','One checked failure path','print("READY");return 0;','READY')
add('letter','Character classification','printnum(letter(95));return 0;','00001')
add('digit','A decimal character test','printnum(digit(57));return 0;','00001')
add('next','Refill source bytes in RILL','input=open("SOURCE.RIL");if status(){fail(1);}next();printnum(ch);return 0;','00065','A',None,1)
add('lex','Tokens with saved local state',read+'printnum(value);return 0;','65535','65535','65536',3)
add('expect','Consume a required token',read+'expect(43);print("OK");return 0;','OK','+','-',2)
add('isword','Whole-keyword recognition',read+'printnum(isword("FN"));return 0;','00001','fn',None,1)
add('setident','Copy an identifier explicitly','setident("ABC");print(ident);return 0;','ABC')
add('tword','A word in an opaque block',setup+'set16(table,100,4660);printnum(tword(100));return 0;','04660')
add('tbyte','A byte in an opaque block',setup+'set16(table,100,4660);printnum(tbyte(100));return 0;','00052')
add('find','Search records by complete spelling',setup+'setident("ABC");printnum(find(0,0));return 0;','65535')
add('recordfields','Store explicit record fields',setup+'rectype=1;recval=12345;reclevel=0;recordfields(0);printnum(tword(34));return 0;','12345')
add('record','Initialize every record byte',setup+record+'printnum(tword(34));return 0;','12345')
add('newglobal','Append a global record',setup+'setident("ABC");recval=12345;newglobal(1);printnum(tword(34));return 0;','12345')
add('newlocal','A scoped local record',setup+'setident("ABC");recval=7;newlocal(5);printnum(tword(20514));return 0;','00007')
add('lookglobal','Select the global namespace',setup+record+'lookglobal();printnum(recval);return 0;','12345')
add('resolve','Choose the innermost binding',setup+record+'resolve();printnum(recval);return 0;','12345')
add('flush','Flush a bounded text block',opened+'outbuf[0]=65;outlen=1;'+closed,'OK RILL.TMP\r\n',fragment='A')
add('outchar','Append an output byte',opened+'outchar(65);'+closed,'OK RILL.TMP\r\n',fragment='A')
add('outstr','Append a template string',opened+'outstr("HI");'+closed,'OK RILL.TMP\r\n',fragment='HI')
add('outnum','An emitted word operand',opened+'outnum(12345);'+closed,'OK RILL.TMP\r\n',fragment='12345')
add('newline','Terminate an output record',opened+'newline();'+closed,'OK RILL.TMP\r\n',fragment='\r\n')
add('newlabel','A label counter in RILL','printnum(newlabel());return 0;','00001')
add('labeldef','Emit a branch definition',opened+'labeldef(7);'+closed,'OK RILL.TMP\r\n',fragment='LABEL B_00007\r\n')
add('labeljump','Emit a branch operand',opened+'labeljump(7);'+closed,'OK RILL.TMP\r\n',fragment=' B_00007\r\n')
add('outname','Emit the stored spelling',setup+record+opened+'outname(0);'+closed,'OK RILL.TMP\r\n',fragment='ABC')
add('builtin','Recognize portable intrinsics','setident("PUTC");builtin();printnum(recval);return 0;','00001')
add('resolveoptional','Record a call before its definition',setup+record+'resolveoptional();printnum(rectype);return 0;','00001')
add('prec','A precedence table in RILL',read+'printnum(prec());return 0;','00007','*',None,1)
add('binary','Select an IR word operation',opened+'binary(43);'+closed,'OK RILL.TMP\r\n',fragment='ADD\r\n')
add('expr','Precedence climbing in RILL',exprdriver,'OK RILL.TMP\r\n','1+2*3','(1)',2,fragment='LIT 00001\r\nPUSH\r\nLIT 00002\r\nPUSH\r\nLIT 00003\r\nMUL\r\nADD\r\n')
add('primary','Values, addresses, and names',exprdriver,'OK RILL.TMP\r\n','ABC+1','UNKNOWN',4,fragment='LD V_ABC\r\nPUSH\r\nLIT 00001\r\nADD\r\n')
add('callargs','Calls inside expressions',exprdriver,'OK RILL.TMP\r\n','putc(65)','get8(1)',4,fragment='LIT 00065\r\nPUSH\r\nPOP\r\nPUTC\r\n')
add('globalword','Compile a global word',setup+opened+read+'globalword();'+closed,'OK RILL.TMP\r\n','let mut abc=65;','let abc=65;',2,fragment='WORD V_ABC 00065\r\n')
add('globalbuffer','Compile a byte extent',setup+opened+read+'globalbuffer();'+closed,'OK RILL.TMP\r\n','bytes abc[8];','bytes abc[0];',5,fragment='BUFFER V_ABC 00008\r\n')
add('declare','Initialize a scoped slot',setup+opened+read+'level=1;declare();'+closed,'OK RILL.TMP\r\n','let mut x=7;','let mut x=x;',4,fragment='LIT 00007\r\nSETLOCAL 00000\r\n')
add('block','Scope entry and restoration',setup+opened+read+'block();'+closed,'OK RILL.TMP\r\n','{}','{putc(65);}',2,fragment='')
add('statement','Structured statements in RILL',setup+opened+read+'outstr("PROC MAIN 0 16\\r\\n");block();outstr("LIT 0\\r\\nRETURN\\r\\n");'+closed,'OK RILL.TMP\r\n','{let mut x=65;while x<67{putc(x);x=x+1;}}','{putc();}',4,complete=True)
add('function','Compile a complete procedure',setup+opened+read+'function();outstr("PROC MAIN 0 0\\r\\nINVOKE F_MAIN 0\\r\\nRETURN\\r\\n");'+closed,'OK RILL.TMP\r\n','fn main(){putc(65);return 0;}','fn main(a,a){}',4,complete=True)
add('main','The compiler compiles its own language',None,'','fn main(){putc(72);putc(73);return 0;}','fn main(){return 65536;}',3,complete=True)

from compiler_checks import refine
refine(entries,'rill')

def build():
 current={};cases=[]
 for n,e in enumerate(entries,1):
  key=e['key'];current[key]=procs[key]
  if key=='lex':current['lexkind']=procs['lexkind']
  if key=='expr':current['primary']='fn primary(){if tok!=2{fail(2);}outstr("LIT ");outnum(value);newline();lex();return 0;}\n'
  if key=='main':program=s
  else:
   body=dict(current);body['main']='fn main(){'+e['body']+'}\n'
   text='\n'.join(body.values());plain=re.sub(r'"(?:\\.|[^"\\])*"','""',text)
   refs=set(re.findall(r'\b([a-z_][a-z_0-9]*)\s*\(',plain))&set(procs)
   for name in refs-set(body):body[name]='fn '+name+'('+','.join(args[name])+'){'+('exit(1);' if name=='fail' else 'fail(2);')+'return 0;}\n'
   if any('fail(2)' in b for k,b in body.items() if k not in current) and 'fail' not in body:body['fail']='fn fail(code){exit(1);return 0;}\n'
   program=data+'\n'+body['main']+'\n'+'\n'.join(body[k] for k in procs if k!='main' and k in body)
  source=f'RC{n:02}.RIL';(W/source).write_bytes(program.replace('\n','\r\n').encode('ascii'))
  if e['fixture'] is not None:(W/f'TRC{n:02}.RIL').write_bytes((e['fixture']+'\r\n').encode())
  if e['bad'] is not None:(W/f'XRC{n:02}.RIL').write_bytes((e['bad']+'\r\n').encode())
  cases.append({**e,'number':n,'source':source})
 (Q/'rill-self-series.json').write_text(json.dumps(cases,indent=2)+'\n');print('Prepared',len(cases),'RILL-written compiler checkpoints')
if __name__=='__main__':build()
