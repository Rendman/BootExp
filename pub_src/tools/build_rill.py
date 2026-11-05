"""Arrange authored IR source into type-in checkpoints; never compile RILL or encode instructions."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/rill';Q=ROOT/'qa/rill'
raw=Path(__file__).with_name('rill_parts.ir').read_text()
rows=re.split(r'^; @block (\w+)\n',raw,flags=re.M)
PARTS={rows[i]:rows[i+1] for i in range(1,len(rows),2)}
def cut(block,start,end=None):
 s=PARTS[block];a=s.index('LABEL '+start+'\n');b=s.index('LABEL '+end+'\n',a) if end else len(s);return s[a:b]
def ascii_text(text):
 # Constant manuscript text represented as literal values, not executable bytes.
 b=text.encode('ascii');out=''
 for i in range(0,len(b),2):
  if i+1<len(b):out+=f'LIT {b[i]+256*b[i+1]}\nCALL PAIR\n'
  else:out+=f'LIT {b[i]}\nCALL CHAR\n'
 return out
OPEN='CALL SOURCENAME\nADDR NAMEBUF\nOPEN\nST INPUT\nSTATUS\nJNZ IOFAIL\n'
CLOSE='LD INPUT\nCLOSE\nSTATUS\nJNZ IOFAIL\n'
HEADER='''CALL NEXT
CALL LEX
LIT 32974
CALL EXPECT
LIT 14
ST WANTTAIL
LIT 46121
CALL EXPECT
LIT 40
CALL EXPECT
LIT 41
CALL EXPECT
LIT 123
CALL EXPECT
'''
EMPTY='LIT 125\nCALL EXPECT\nLIT 0\nCALL EXPECT\n'
CONCHAR='''LABEL CHAR
PUTC
STATUS
JZ CHARDONE
LIT 4
EXIT
LABEL CHARDONE
RET
'''
def factor(level):
 pre=PARTS['FACTOR'].split('LD TOK\n',1)[0]
 if level<18:dispatch='LD TOK\nPUSH\nLIT 65535\nNE SYNTAX\n'
 else:
  dispatch='LD TOK\nPUSH\nLIT 65535\nEQ FACTORNUM\n'
  if level>=20:dispatch+='LD TOK\nPUSH\nLIT 40\nEQ FACTORPAREN\n'
  if level>=21:dispatch+='LD TOK\nPUSH\nLIT 45\nEQ FACTORMINUS\n'
  if level>=22:dispatch+='LD TOK\nPUSH\nLIT 40116\nEQ FACTORSERVICE\nLD TOK\nPUSH\nLIT 52865\nEQ FACTORSERVICE\n'
  dispatch+='CALL USEVAR\n'+PARTS['FACTOR'].split('CALL USEVAR\n',1)[1].split('LABEL FACTORNUM\n',1)[0]
 s=pre+dispatch+cut('FACTOR','FACTORNUM','FACTORPAREN')
 if level>=20:s+=cut('FACTOR','FACTORPAREN','FACTORMINUS')
 if level>=21:s+=cut('FACTOR','FACTORMINUS','FACTORSERVICE')
 if level>=22:s+=cut('FACTOR','FACTORSERVICE','FACTORDONE')
 return s+cut('FACTOR','FACTORDONE')
def statement(level):
 s='LABEL STATEMENT\n'
 for at,tok,label in [(17,49844,'PUTSTAT'),(23,38665,'EXITSTAT'),(25,33062,'IFSTAT'),(29,56585,'WHILESTAT')]:
  if level>=at:s+=f'LD TOK\nPUSH\nLIT {tok}\nEQ {label}\n'
 if level>=18:s+='CALL USEVAR\n'+PARTS['STATEMENT'].split('CALL USEVAR\n',1)[1].split('LABEL PUTSTAT\n',1)[0]
 else:s+='JMP SYNTAX\n'
 s+=cut('STATEMENT','PUTSTAT','EXITSTAT')
 if level>=23:s+=cut('STATEMENT','EXITSTAT')
 return s

def condition(level):
 if level>=28:return PARTS['CONDITION']
 prefix='LABEL CONDITION\nST BRANCH\nCALL EXPR\n'
 value=cut('CONDITION','VALUECOND')
 if level<27:return prefix+value
 checks='LD TOK\nPUSH\nLIT 200\nEQ RELATION\nLD TOK\nPUSH\nLIT 201\nNE VALUECOND\n'
 relation=cut('CONDITION','RELATION','CONDNE')
 relation=relation[:relation.index('CALL RESTORE\n')]+'''CALL RESTORE
PUSH
LIT 200
EQ CONDNE
'''+ascii_text('EQ B')+'JMP CONDTARGET\n'
 return prefix+checks+relation+cut('CONDITION','CONDNE','CONDEQ')+value

def driver(level):
 if level==1:return 'LABEL MAIN\nLIT 72\nPUTC\nLIT 73\nPUTC\nHALT\n'
 if level==2:return 'LABEL MAIN\nLIT 72\nCALL CHAR\nLIT 73\nCALL CHAR\nHALT\n'
 if level==3:return 'LABEL MAIN\nLIT 256\nST STEP\nLIT 16712\nCALL DIVIDE\nLD COUNT\nCALL CHAR\nHALT\n'
 if level==4:return 'LABEL MAIN\n'+ascii_text('HI\r\n')+'HALT\n'
 if level==5:return 'LABEL MAIN\nLIT 65535\nCALL NUMBER\nCALL NEWLINE\nHALT\n'
 if level==6:return 'LABEL MAIN\nGETC\nPUSH\nLIT 65\nNE SYNTAX\n'+ascii_text('OK\r\n')+'HALT\n'
 if level==7:return '''LABEL MAIN
CALL SOURCENAME
ADDR NAMEBUF
ST TOKENVAL
LABEL NAMEDISPLAY
LD TOKENVAL
FETCHB
JZ NAMEDONE
CALL CHAR
LD TOKENVAL
PUSH
LIT 1
ADD
ST TOKENVAL
JMP NAMEDISPLAY
LABEL NAMEDONE
CALL NEWLINE
HALT
'''
 if level==8:return 'LABEL MAIN\n'+OPEN+CLOSE+ascii_text('OK\r\n')+'HALT\n'
 if level==9:return 'LABEL MAIN\n'+OPEN+'''CALL NEXT
LABEL DISPLAY
LD CH
JZ DISPLAYDONE
CALL CHAR
CALL NEXT
JMP DISPLAY
LABEL DISPLAYDONE
'''+CLOSE+'HALT\n'
 if level in [10,11,12]:
  s='LABEL MAIN\n'+OPEN+'CALL NEXT\nCALL LEX\nLABEL SHOWTOKEN\nLD TOK\nJZ TOKENDONE\n'
  if level==11:s+='PUSH\nLIT 65535\nNE SHOWVALUE\nLD TOKENVAL\nJMP TOKENPRINT\nLABEL SHOWVALUE\nLD TOK\nLABEL TOKENPRINT\n'
  s+='CALL NUMBER\n'
  if level==12:s+='LIT 58\nCALL CHAR\nLD SUFFIX\nCALL NUMBER\n'
  return s+'LIT 32\nCALL CHAR\nCALL LEX\nJMP SHOWTOKEN\nLABEL TOKENDONE\nCALL NEWLINE\n'+CLOSE+'HALT\n'
 if level in [13,14]:
  s='LABEL MAIN\n'+OPEN+HEADER+EMPTY+CLOSE
  if level==13:return s+ascii_text('OK\r\n')+'HALT\n'
  return s+'LIT 1\nST DEST\n'+ascii_text('LABEL MAIN\r\nHALT\r\n')+'''LIT 0
ST DEST
ST TOKENVAL
'''+ascii_text('BUFFER ')+'''LD OUTCOUNT
CALL NUMBER
CALL NEWLINE
LABEL SHOWBUFFER
LD TOKENVAL
PUSH
LD OUTCOUNT
UGE BUFFERDONE
ADDR OUTBUF
PUSH
LD TOKENVAL
ADD
FETCHB
CALL CHAR
LD TOKENVAL
PUSH
LIT 1
ADD
ST TOKENVAL
JMP SHOWBUFFER
LABEL BUFFERDONE
HALT
'''
 s=PARTS['DRIVER']
 if level<16:
  a=s.index('LABEL DECLLOOP\n');b=s.index('LABEL DECLDONE\n',a)+len('LABEL DECLDONE\n');s=s[:a]+s[b:]
 if level<17:s=s.replace('CALL BODY\n',EMPTY.split('LIT 0\n')[0])
 if level==24:s=s.replace('CALL BODY\n','CALL NEWLABEL\nCALL DEFLABEL\nCALL BODY\n')
 return s

def source(level):
 selected={};body=driver(level)
 if level>=2:selected['CHAR']=PARTS['CHAR'] if level>=14 else CONCHAR
 for name,at in [('DIVIDE',3),('PAIR',4),('NUMBER',5),('ERROR',6),('NAMETEXT',7),('NEXT',9),('LEX',10),('COMMENT',10),('SCANNUM',11),('SCANWORD',12),('EXPECT',13),('WRITEFILE',15),('VARADDRESS',16),('DECLARE',16),('SAVE',18),('EXPRESSION',17),('FACTOR',17),('BODY',17),('STATEMENT',17),('LABELS',24),('CONDITION',25),('IFSTAT',25),('WHILESTAT',29)]:
  if level>=at:selected[name]=PARTS[name]
 if 7<=level<15:selected['NAMETEXT']=cut('NAMETEXT','NAMEWORD','RESULTNAME')
 if 10<=level<12:
  s=selected['LEX'];a=s.index('LD CH\nPUSH\nLIT 97\n');b=s.index('LABEL PUNCT\n',a);s=s[:a]+s[b:]
  if level==10:
   a=s.index('LD CH\nPUSH\nLIT 48\n');b=s.index('LABEL LETTERTEST\n',a);s=s[:a]+s[b:]
  selected['LEX']=s
 if level>=17:
  selected['FACTOR']=factor(level)
  selected['STATEMENT']=statement(level)
  if level<19:selected['EXPRESSION']='LABEL EXPR\nCALL FACTOR\nRET\n'
 if level>=25:
  selected['CONDITION']=condition(level)
  if level<26:selected['IFSTAT']='''LABEL IFSTAT
CALL LEX
CALL NEWLABEL
CALL SAVE
CALL CONDITION
CALL BLOCK
CALL RESTORE
CALL DEFLABEL
RET
'''
 used=set(re.findall(r'\b[A-Z][A-Z0-9_]*\b',body+'\n'+''.join(selected.values())))
 if level>=14:used.update(['OUTBUF','OUT1','OUT2','OUT3'])
 data=''
 for block in ['DATA','FILENAMES']:
  lines=[line for line in PARTS[block].splitlines() if line.split()[1] in used]
  if lines:data+='; '+block+'\n'+'\n'.join(lines)+'\n'
 s=data+'; Driver\n'+body
 for name in PARTS:
  if name in selected:s+='; '+name+'\n'+selected[name]
 return s

def dos(path,text):path.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
if __name__=='__main__':
 specs=json.loads(Path(__file__).with_name('rill_installments.json').read_text());manifest=[]
 W.mkdir(exist_ok=True);Q.mkdir(exist_ok=True)
 for spec in specs:
  n=spec['number'];name=f'R{n:02}';dos(W/(name+'.IR'),source(n))
  if n>=6 and n!=7:dos(W/f'T{n:02}.RIL',spec.get('fixture',''))
  suffix='IR' if spec['bad']['kind']=='ir' else 'RIL'
  dos(W/f'X{n:02}.{suffix}',spec['bad'].get('source',''))
  manifest.append({**spec,'source':name+'.IR'})
 dos(W/'RILL.IR',source(29))
 (Q/'checkpoints.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Prepared authored IR source checkpoints; no RILL parsing or executable generation.')
