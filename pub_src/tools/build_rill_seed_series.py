"""Arrange authored IR routines into independently executable compiler checkpoints."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/toolchain';Q=ROOT/'qa/toolchain'
text=(ROOT/'tools/rill_bootstrap.ir').read_text();data='\n'.join(re.findall(r'^(?:WORD|BYTE|BUFFER) .*$',text,re.M))+'\n'
alias=text[text.index('LABEL IOFAIL\n'):text.index('PROC ERROR')]
clean=re.sub(r'^(?:WORD|BYTE|BUFFER) .*\n','',text,flags=re.M);clean=clean.replace(alias,'')
rows=re.split(r'^PROC ',clean,flags=re.M);procs={r.split()[0]:'PROC '+r for r in rows[1:]}
argcs={n:int(b.splitlines()[0].split()[2]) for n,b in procs.items()}
# Each tuple is an authored driver/fixture, not a host-language translation.
def formatnum(body):return body+'CALL PRINTNUM\nLIT 0\nRETURN\n'
setup='LIT 22000\nALLOC\nST TABLE\n'
record='LITS "ABC"\nCALL SETIDENT\nLIT 1\nST RECTYPE\nLIT 12345\nST RECVAL\nLIT 0\nST RECLEVEL\nLIT 0\nPUSH\nINVOKE RECORD 1\nLIT 1\nST GLOBALS\n'
openinput='LITS "SOURCE.RIL"\nOPEN\nST INPUT\nSTATUS\nJNZ IOFAIL\nCALL NEXT\nCALL LEX\n'
openout='LITS "RILL.TMP"\nCREATE\nST OUTPUT\nSTATUS\nJNZ IOFAIL\nLIT 1\nST OWN\n'
finishout='CALL FLUSH\nLD OUTPUT\nCLOSE\nLIT 0\nST OUTPUT\nST OWN\nLITS "OK RILL.TMP\\r\\n"\nCALL PRINT\nLIT 0\nRETURN\n'
exprdriver=setup+record+openout+openinput+'LIT 1\nPUSH\nINVOKE EXPR 1\nLD TOK\nJNZ SYNTAX\n'+finishout
entries=[]
def add(key,title,body,expected='',fixture=None,bad=None,code=None,fragment=None,complete=False,variant=None,boundary=None):
 entries.append(dict(key=key,title=title,body=body,expected=expected,fixture=fixture,bad=bad,code=code,fragment=fragment,complete=complete,variant=variant,boundary=boundary))
add('PRINT','A terminated text pointer','LITS "HI"\nCALL PRINT\nLIT 0\nRETURN\n','HI')
add('PRINTNUM','A visible word value',formatnum('LIT 65535\n'),'65535')
add('PRINT32','Counting beyond one word','LIT 1\nPUSH\nLIT 1\nPUSH\nINVOKE PRINT32 2\nLIT 0\nRETURN\n','0000065537')
add('ERROR','One terminal error path','LITS "READY"\nCALL PRINT\nLIT 0\nRETURN\n','READY')
add('LETTER','Identifier characters',formatnum('LIT 95\nPUSH\nINVOKE LETTER 1\n'),'00001')
add('DIGIT','Decimal characters',formatnum('LIT 57\nPUSH\nINVOKE DIGIT 1\n'),'00001')
add('NEXT','A bounded source refill','LITS "SOURCE.RIL"\nOPEN\nST INPUT\nSTATUS\nJNZ IOFAIL\nCALL NEXT\nLD CH\nCALL PRINTNUM\nLIT 0\nRETURN\n','00065','A',None,1)
add('LEX','Punctuation and paired operators',openinput+'LD TOK\nCALL PRINTNUM\nLIT 0\nRETURN\n','00256','==',None,1,variant='punctuation')
add('LEX','Complete identifier spelling',openinput+'ADDR IDENT\nCALL PRINT\nLIT 0\nRETURN\n','HELLO','hello',None,1,variant='names')
add('LEX','Checked decimal words',openinput+'LD VALUE\nCALL PRINTNUM\nLIT 0\nRETURN\n','65535','65535','65536',3,variant='numbers')
add('LEX','Quoted source text',openinput+'ADDR STRING\nCALL PRINT\nLIT 0\nRETURN\n','"Hi"','"Hi"','"open',2,variant='full')
add('EXPECT','Consume an exact token',openinput+'LIT 43\nPUSH\nINVOKE EXPECT 1\nLITS "OK"\nCALL PRINT\nLIT 0\nRETURN\n','OK','+','-',2)
add('ISWORD','Compare the whole keyword',openinput+'LITS "FN"\nCALL ISWORD\nCALL PRINTNUM\nLIT 0\nRETURN\n','00001','fn',None,1)
add('SETIDENT','Save an explicit spelling','LITS "ABC"\nCALL SETIDENT\nADDR IDENT\nCALL PRINT\nLIT 0\nRETURN\n','ABC')
add('TWORD','Word fields in an opaque block',setup+'LD TABLE\nPUSH\nLIT 100\nPUSH\nLIT 4660\nSET16\n'+formatnum('LIT 100\nCALL TWORD\n'),'04660')
add('TBYTE','Byte fields in an opaque block',setup+'LD TABLE\nPUSH\nLIT 100\nPUSH\nLIT 4660\nSET16\n'+formatnum('LIT 100\nCALL TBYTE\n'),'00052')
add('WRITEFIELD','Write one explicit record field',setup+'LIT 100\nPUSH\nLIT 4660\nPUSH\nINVOKE WRITEFIELD 2\n'+formatnum('LIT 100\nCALL TWORD\n'),'04660')
add('RECORD','Initialize a complete symbol',setup+record+formatnum('LIT 34\nCALL TWORD\n'),'12345')
add('NEWGLOBAL','Add a global definition',setup+'LITS "ABC"\nCALL SETIDENT\nLIT 12345\nST RECVAL\nLIT 1\nCALL NEWGLOBAL\n'+formatnum('LIT 34\nCALL TWORD\n'),'12345')
add('NEWLOCAL','A separate local-name region',setup+'LITS "ABC"\nCALL SETIDENT\nLIT 7\nST RECVAL\nLIT 5\nCALL NEWLOCAL\n'+formatnum('LIT 20514\nCALL TWORD\n'),'00007')
add('FIND','Search exact names from the inside out',setup+record+'LIT 0\nPUSH\nLIT 1\nPUSH\nINVOKE FIND 2\n'+formatnum('LD RECVAL\n'),'12345')
add('LOOKGLOBAL','The global namespace',setup+record+'CALL LOOKGLOBAL\n'+formatnum('LD RECVAL\n'),'12345')
add('RESOLVE','Resolve a current binding',setup+record+'CALL RESOLVE\n'+formatnum('LD RECVAL\n'),'12345')
add('FLUSH','Write a nonempty output block',openout+'ADDR OUTBUF\nPUSH\nLIT 65\nPUTB\nLIT 1\nST OUTLEN\n'+finishout,'OK RILL.TMP\r\n',fragment='A')
add('OUTCHAR','Append one streamed byte',openout+'LIT 65\nCALL OUTCHAR\n'+finishout,'OK RILL.TMP\r\n',fragment='A')
add('OUTSTR','Append a text template',openout+'LITS "HI"\nCALL OUTSTR\n'+finishout,'OK RILL.TMP\r\n',fragment='HI')
add('OUTNUM','Print an IR operand',openout+'LIT 12345\nCALL OUTNUM\n'+finishout,'OK RILL.TMP\r\n',fragment='12345')
add('NEWLINE','Terminate an emitted record',openout+'CALL NEWLINE\n'+finishout,'OK RILL.TMP\r\n',fragment='\r\n')
add('NEWLABEL','Allocate a source label number',formatnum('CALL NEWLABEL\n'),'00001')
add('LABELDEF','Define one compiler label',openout+'LIT 7\nCALL LABELDEF\n'+finishout,'OK RILL.TMP\r\n',fragment='LABEL B_00007\r\n')
add('LABELJUMP','Emit a label operand',openout+'LIT 7\nCALL LABELJUMP\n'+finishout,'OK RILL.TMP\r\n',fragment=' B_00007\r\n')
add('OUTNAME','Emit a saved symbol spelling',setup+record+openout+'LIT 0\nCALL OUTNAME\n'+finishout,'OK RILL.TMP\r\n',fragment='ABC')
add('BUILTIN','A table of portable services','LITS "PUTC"\nCALL SETIDENT\nCALL BUILTIN\n'+formatnum('LD RECVAL\n'),'00001')
add('RESOLVEOPTIONAL','Call names and forward declarations',setup+record+'CALL RESOLVEOPTIONAL\n'+formatnum('LD RECTYPE\n'),'00001')
add('PREC','Operator precedence',openinput+'CALL PREC\nCALL PRINTNUM\nLIT 0\nRETURN\n','00007','*',None,1)
add('BINARY','Emit a word operation',openout+'LIT 43\nCALL BINARY\n'+finishout,'OK RILL.TMP\r\n',fragment='ADD\r\n')
add('EXPR','Precedence with a numeric primary',exprdriver,'OK RILL.TMP\r\n','1+2*3','(1)',2,fragment='LIT 00001\r\nPUSH\r\nLIT 00002\r\nPUSH\r\nLIT 00003\r\nMUL\r\nADD\r\n',variant='numeric')
add('PRIMARY','Parentheses, strings, and unary values',exprdriver,'OK RILL.TMP\r\n','-(1+2)','ABC',4,fragment='LIT 00001\r\nPUSH\r\nLIT 00002\r\nADD\r\nNEG\r\n',variant='values')
add('PRIMARY','Variables and addressed storage',exprdriver,'OK RILL.TMP\r\n','ABC+1','UNKNOWN',4,fragment='LD V_ABC\r\nPUSH\r\nLIT 00001\r\nADD\r\n',variant='full')
add('CALLARGS','Nested argument expressions',exprdriver,'OK RILL.TMP\r\n','putc(65)','get8(1)',4,fragment='LIT 00065\r\nPUSH\r\nPOP\r\nPUTC\r\n')
add('GLOBALWORD','A global word declaration',setup+openout+openinput+'CALL GLOBALWORD\n'+finishout,'OK RILL.TMP\r\n','let mut abc=65;','let abc=65;',2,fragment='WORD V_ABC 00065\r\n')
add('GLOBALBUFFER','A global byte extent',setup+openout+openinput+'CALL GLOBALBUFFER\n'+finishout,'OK RILL.TMP\r\n','bytes abc[8];','bytes abc[0];',5,fragment='BUFFER V_ABC 00008\r\n')
add('DECLARE','A local slot and initializer',setup+openout+openinput+'LIT 1\nST LEVEL\nCALL DECLARE\n'+finishout,'OK RILL.TMP\r\n','let mut x=7;','let mut x=x;',4,fragment='LIT 00007\r\nSETLOCAL 00000\r\n')
add('BLOCK','Enter and leave a lexical scope',setup+openout+openinput+'CALL BLOCK\n'+finishout,'OK RILL.TMP\r\n','{}','{putc(65);}',2,fragment='')
add('STATEMENT','Statements and structured branches',setup+openout+openinput+'LITS "PROC MAIN 0 16\\r\\n"\nCALL OUTSTR\nCALL BLOCK\nLITS "LIT 0\\r\\nRETURN\\r\\n"\nCALL OUTSTR\n'+finishout,'OK RILL.TMP\r\n','{let mut x=65;while x<67{putc(x);x=x+1;}}','{putc();}',4,complete=True)
add('FUNCTION','A named procedure definition',setup+openout+openinput+'CALL FUNCTION\nLITS "PROC MAIN 0 0\\r\\nINVOKE F_MAIN 0\\r\\nRETURN\\r\\n"\nCALL OUTSTR\n'+finishout,'OK RILL.TMP\r\n','fn main(){putc(65);return 0;}','fn main(a,a){}',4,complete=True)
add('MAIN','The complete streamed compiler',None,'','fn main(){putc(72);putc(73);return 0;}','fn main(){return 65536;}',3,complete=True)

def lexer(mode):
 b=procs['LEX'];a=b.index('LABEL LEXNAME\n');n=b.index('LABEL LEXNUMBER\n');q=b.index('LABEL LEXSTRING\n');end=b.index('LABEL LEXEOF\n')
 name=b[a:n] if mode in ['names','numbers','full'] else 'LABEL LEXNAME\nJMP SYNTAX\n'
 number=b[n:q] if mode in ['numbers','full'] else 'LABEL LEXNUMBER\nJMP SYNTAX\n'
 string=b[q:end] if mode=='full' else 'LABEL LEXSTRING\nJMP SYNTAX\n'
 return b[:a]+name+number+string+b[end:]
def primary(mode):
 if mode=='numeric':return 'PROC PRIMARY 0 0\nLD TOK\nPUSH\nLIT 2\nCNE\nJNZ SYNTAX\nLITS "LIT "\nCALL OUTSTR\nLD VALUE\nCALL OUTNUM\nCALL NEWLINE\nCALL LEX\nLIT 0\nRETURN\n'
 b=procs['PRIMARY']
 if mode=='values':
  a=b.index('CALL RESOLVEOPTIONAL\n');end=b.index('LABEL PRIMARYNUM\n');b=b[:a]+'JMP NAMEFAIL\n'+b[end:]
 return b

from compiler_checks import refine
refine(entries,'ir')

def build():
 current={};cases=[]
 for n,e in enumerate(entries,1):
  key=e['key']
  if key=='LEX':current[key]=lexer(e['variant'])
  elif key=='EXPR':current[key]=procs[key];current['PRIMARY']=primary('numeric')
  elif key=='PRIMARY':current[key]=primary(e['variant'])
  else:current[key]=procs[key]
  if key=='MAIN':program=text
  else:
   body=dict(current);body['MAIN']='PROC MAIN 0 0\n'+e['body']
   refs=set(re.findall(r'^(?:CALL|INVOKE) (\w+)',alias+'\n'.join(body.values()),re.M))
   for name in refs-set(body):
    if name not in argcs:raise ValueError(name)
    body[name]=f'PROC {name} {argcs[name]} 0\nLIT 2\nPUSH\nINVOKE ERROR 1\nLIT 0\nRETURN\n' if name!='ERROR' else 'PROC ERROR 1 0\nLIT 1\nEXIT\n'
   program=data+'\n'+body['MAIN']+'\n'+'\n'.join((alias+'\n' if k=='ERROR' else '')+body[k] for k in procs if k!='MAIN' and k in body)
  source=f'RB{n:02}.IR';(W/source).write_bytes(program.replace('\n','\r\n').encode('ascii'))
  if e['fixture'] is not None:(W/f'TRB{n:02}.RIL').write_bytes((e['fixture']+'\r\n').encode())
  if e['bad'] is not None:(W/f'XRB{n:02}.RIL').write_bytes((e['bad']+'\r\n').encode())
  cases.append({**e,'number':n,'source':source})
 (Q/'rill-seed-series.json').write_text(json.dumps(cases,indent=2)+'\n');print('Prepared',len(cases),'IR-written compiler checkpoints')
if __name__=='__main__':build()
