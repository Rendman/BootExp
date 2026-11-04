"""Prepare authored IR86 source checkpoints and manuscript facts, never COM bytes."""
from pathlib import Path
import re,json
from ir86_runtime_text import runtime,part_names,PARTS
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/ir86';Q=ROOT/'qa/ir86'
W.mkdir(parents=True,exist_ok=True);Q.mkdir(parents=True,exist_ok=True)
PROFILES=json.loads((Q/'runtime-sizes.json').read_text())
def dos(p,s):p.write_bytes((s.rstrip()+'\n').replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
def parts(text,starts):
 positions={n:text.index('\n'+n+':\n')+1 for n in starts}
 return {n:'\n'.join(l for l in text[positions[n]:positions[b]].splitlines() if l.strip() and not l.lstrip().startswith(';'))+'\n' for n,b in zip(starts,starts[1:])},positions
starts=['START','FILEBAD','OPENFILE','CLOSEFILE','WRITEOUT','GETNAME','NEXTBYTE','READLINE','SCAN','LOOK','REGISTER','VALIDNAME','VALUE','SYMBOLVALUE','DEFINE','OPERAND','MEMORY','STATEMENT','DATAITEM','FIXED','SINGLE','INTERRUPT','NEARJUMP','SHORTJUMP','FINISH','TWOOPERANDS','MOVOPERANDS','MOVREG','REGMOD','IMMEDVALUE','LOADMEM','STOREMEM','SAMEWIDTH','TIMES8','BYTEVALUE','EMITWORD','EMIT','COPYZ','TEXT','NUMBER','ERROR','PROMPT']
source=(ROOT/'workbench/asm86/ASM86.ASM').read_text();lib,pos=parts(source,starts)
lib['GETNAME']=lib['GETNAME'].replace('ASMEXT','IREXT')
lib['VALUE']=lib['VALUE'].replace('JMP SYMBOLVALUE','JMP NUMBERBAD')
lib['ZTEXT']='ZTEXT:\nLODSB\nCMP AL,0\nJE ZDONE\nMOV DL,AL\nMOV AH,2\nINT 21H\nJMP ZTEXT\nZDONE:\nRET\n'
raw=(ROOT/'tools/ir86_core.asm').read_text()
sections=re.split(r'^; @block (\w+)\n',raw,flags=re.M)
core={sections[i]:sections[i+1].strip()+'\n' for i in range(1,len(sections),2)}
core['CONTEXT']=core['CONTEXT'].replace('JNE BADIRNAME','JNE MAINBAD')+'MAINBAD:\nMOV AX,3\nJMP ERROR\n'
data=source[pos['PROMPT']:];matches=list(re.finditer(r'^([A-Z][A-Z0-9_]*):$',data,re.M))
fields={m[1]:data[m.start():matches[i+1].start() if i+1<len(matches) else len(data)].strip()+'\n' for i,m in enumerate(matches)}
def textfield(name,s):fields[name]=name+':\n'+''.join('DB '+','.join(str(x) for x in s.encode('ascii')[i:i+16])+'\n' for i in range(0,len(s),16))
textfield('PROMPT','IR source name: $');textfield('ERRMSG','IR ERROR $');textfield('IREXT','.IR\0');textfield('ASMEXT','.ASM\0');textfield('BYTEMSG',' text bytes\r\n$');textfield('SPACE',' $');textfield('CRLF','\r\n\0')
fields['FOURDIV']='FOURDIV:\nDW 1000,100,10,1\n';fields['FOUREND']='FOUREND:\n'
for name in ['NUMV','TPL','DEPTH','TARGETSIZE','DEFS','OUTLINES','BRANCHNO']:fields[name]=name+':\nDW 0\n'
for name in ['CLASS','EFFECT','INSIZE','CODE','LAST']:fields[name]=name+':\nDB 0\n'
textfield('ZEROSTART','DB 0\0');textfield('ZERONEXT',',0\0')
# The strings below are authored assembly TEXT. Only the project assembler encodes instructions.
TEMPLATES={'HEADER':'CLD\nCMP SP,0FFFEH\nJE I_ENTRY\nMOV AX,4C07H\nINT 21H\nI_ENTRY:\nJMP U_MAIN\n',
'NOP':'NOP\n','HALT':'MOV AX,4C00H\nINT 21H\n','LABEL':'U_@:\n','LIT':'MOV AX,#\n','EXIT':'MOV AH,4CH\nINT 21H\n',
'WORD':'U_@:\nDW #\n','LD':'MOV AX,[U_@]\n','ST':'MOV [U_@],AX\n','BYTE':'U_@:\nDB #\n','LDB':'MOV AL,[U_@]\nMOV AH,0\n','STB':'MOV [U_@],AL\n',
'PUSH':'PUSH AX\n','POP':'POP AX\n','ADD':'POP BX\nADD AX,BX\n','SUB':'POP BX\nSUB BX,AX\nMOV AX,BX\n',
'AND':'POP BX\nAND AX,BX\n','OR':'POP BX\nOR AX,BX\n','XOR':'POP BX\nXOR AX,BX\n',
'ADDR':'MOV AX,U_@\n','FETCH':'MOV BX,AX\nMOV AX,[BX]\n','FETCHB':'MOV BX,AX\nMOV AL,[BX]\nMOV AH,0\n',
'PUT':'POP BX\nMOV [BX],AX\n','PUTB':'POP BX\nMOV [BX],AL\n','BUFFER':'',
'JMP':'JMP U_@\n','JZ':'CMP AX,0\nJNE I?\nJMP U_@\nI?:\n','JNZ':'CMP AX,0\nJE I?\nJMP U_@\nI?:\n',
'CALL':'CALL U_@\n','RET':'RET\n','STATUS':'MOV AX,[R_STATUS]\n','PUTC':'CALL R_PUTC\n','GETC':'CALL R_GETC\n','OPEN':'CALL R_OPEN\n','CREATE':'CALL R_CREATE\n','READ':'POP DX\nPOP BX\nCALL R_READ\n','WRITE':'POP DX\nPOP BX\nCALL R_WRITE\n','CLOSE':'CALL R_CLOSE\n'}
for op,opposite in [('EQ','JNE'),('NE','JE'),('ULT','JAE'),('ULE','JA'),('UGT','JBE'),('UGE','JB'),('SLT','JGE'),('SLE','JG'),('SGT','JLE'),('SGE','JL')]:TEMPLATES[op]='POP BX\nCMP BX,AX\n'+opposite+' I?\nJMP U_@\nI?:\n'
for part in PARTS:textfield('T_RT'+part,PARTS[part]+'\n\0')
for key,value in TEMPLATES.items():textfield('T_'+key,value.replace('\n','\r\n')+'\0')
# name -> (argument class, expression/control effect, emitted machine-byte count)
OPS={'NOP':(0,0,1),'HALT':(0,5,5),'LABEL':(3,3,0),'LIT':(1,0,3),'EXIT':(0,5,4),'WORD':(5,0,2),'LD':(2,0,4),'ST':(2,0,4),'BYTE':(4,0,1),'LDB':(2,0,6),'STB':(2,0,4),'PUSH':(0,1,1),'POP':(0,2,1),'ADD':(0,2,3),'SUB':(0,2,5),'AND':(0,2,3),'OR':(0,2,3),'XOR':(0,2,3),'ADDR':(2,0,3),'FETCH':(0,0,4),'FETCHB':(0,0,6),'PUT':(0,2,3),'PUTB':(0,2,3),'BUFFER':(6,0,0),'JMP':(2,5,3),'JZ':(7,3,9),'JNZ':(7,3,9),'CALL':(2,3,3),'RET':(0,5,1),'STATUS':(0,0,4),'PUTC':(0,3,3),'GETC':(0,3,3),'OPEN':(0,3,3),'CREATE':(0,3,3),'READ':(0,6,5),'WRITE':(0,6,5),'CLOSE':(0,3,3)}
for op in ['EQ','NE','ULT','ULE','UGT','UGE','SLT','SLE','SGT','SGE']:OPS[op]=(7,4,8)

ORDER=[n for n in starts[1:-1] if n in ['FILEBAD','OPENFILE','CLOSEFILE','GETNAME','NEXTBYTE','READLINE','SCAN','LOOK','VALIDNAME','VALUE','FINISH','COPYZ','TEXT','NUMBER','ERROR']]+['ZTEXT','STATEMENT']+list(core)
fields.pop('OPTAB',None)
BASEORDER=list(fields)
READ='CALL OPENFILE\nDRIVERLINE:\nCALL READLINE\nCMP AX,0\nJE DRIVERDONE\nMOV SI,2200H\n'
CLOSE='JMP DRIVERLINE\nDRIVERDONE:\nCALL CLOSEFILE\n'
def main(level):
 s='START:\nCLD\nCMP SP,0FFFEH\nJE ROOM\nMOV AX,7\nJMP ERROR\nROOM:\nCALL GETNAME\n'
 if level>=3:s+='MOV AX,6000H\nMOV [OUTPTR],AX\n'
 if level>=16:s+=f'MOV AX,{15+PROFILES[str(level)]["bytes"]}\nMOV [TARGETSIZE],AX\n'
 if level>=17:s+=f'MOV AX,{1+PROFILES[str(level)]["definitions"]}\nMOV [DEFS],AX\n'
 if level>=5:s+='MOV SI,T_HEADER\nCALL OUTTEXT\n'
 if level==1:s+=READ+'CALL ZTEXT\nMOV DX,NEWLINE\nCALL TEXT\n'+CLOSE
 elif level==2:s+=READ+'''TRACETOKEN:
CALL SCAN
MOV AL,[2300H]
CMP AL,0
JE DRIVERLINE
MOV DL,91
MOV AH,2
INT 21H
PUSH SI
MOV SI,2300H
CALL ZTEXT
POP SI
MOV DL,93
MOV AH,2
INT 21H
MOV DX,NEWLINE
CALL TEXT
JMP TRACETOKEN
DRIVERDONE:
CALL CLOSEFILE
'''
 elif level==3:s+=READ+'CALL OUTTEXT\nMOV SI,CRLF\nCALL OUTTEXT\n'+CLOSE+'CALL WRITEOUT\n'
 else:
  s+=READ+'CALL STATEMENT\n'+CLOSE
  if level>=5:s+='MOV AL,[CODE]\nCMP AL,1\nJE MAINPRESENT\nMOV AX,3\nJMP ERROR\nMAINPRESENT:\n'
  if level>=10:s+='CALL BALANCED\n'
  s+='CALL FINISHOUTPUT\n'
  for part in part_names(level):s+='MOV SI,T_RT'+part+'\nCALL OUTTEXT\n'
  s+='CALL WRITEOUT\n'
 return s+'MOV AX,4C00H\nINT 21H\n'
def statement(level,names):
 s=f'''STATEMENT:
CALL SCAN
MOV AL,[2300H]
CMP AL,0
JNE STATWORD
RET
STATWORD:
MOV BX,OPTAB
MOV CX,{len(names)}
MOV AX,14
CALL LOOK
CMP BX,0
JNE STATFOUND
MOV AX,1
JMP ERROR
STATFOUND:
ADD BX,8
MOV AL,[BX]
MOV [CLASS],AL
INC BX
MOV AL,[BX]
MOV [EFFECT],AL
INC BX
MOV AL,[BX]
MOV [INSIZE],AL
ADD BX,2
MOV AX,[BX]
MOV [TPL],AX
MOV AL,[EFFECT]
CMP AL,5
MOV AL,0
JNE STATLAST
MOV AL,1
STATLAST:
MOV [LAST],AL
'''
 if level>=5:s+='CALL ARGUMENTS\n'
 s+='CALL FINISH\n'
 if level>=5:s+='CALL CONTEXT\n'
 if level>=10:s+='CALL FLOW\n'
 if level>=16:s+='CALL SIZEADD\n'
 if level>=17:s+='MOV AL,[CLASS]\nCMP AL,3\nJB STATNODEF\nCMP AL,6\nJA STATNODEF\nCALL NEWDEF\nSTATNODEF:\n'
 if level>=19:s+='MOV AL,[CLASS]\nCMP AL,7\nJNE STATNOBRANCH\nCALL NEWDEF\nMOV AX,[BRANCHNO]\nINC AX\nMOV [BRANCHNO],AX\nSTATNOBRANCH:\n'
 if level>=15:s+='MOV AL,[CLASS]\nCMP AL,6\nJNE STATORDINARY\nCALL ZEROBUFFER\nRET\nSTATORDINARY:\n'
 return s+'MOV SI,[TPL]\nCALL EXPAND\nRET\n'
def variants(level,names):
 result={'START':main(level)}
 if level>=4:result['STATEMENT']=statement(level,names)
 if level<17:
  s=core['EMITCHAR'];a=s.index('CMP AL,10\n');b=s.index('CHARDONE:\n',a);result['EMITCHAR']=s[:a]+s[b:]
 if level<19:
  s=core['EXPAND'];s=s.replace('CMP AL,63\nJE EXPANDBRANCH\n','');a=s.index('EXPANDBRANCH:\n');b=s.index('EXPANDDONE:\n',a);result['EXPAND']=s[:a]+s[b:]
 if level<6:
  s=result.get('EXPAND',core['EXPAND']).replace('CMP AL,35\nJE EXPANDNUMBER\n','');a=s.index('EXPANDNUMBER:\n');b=s.index('EXPANDDONE:\n',a);result['EXPAND']=s[:a]+s[b:]
 if level<5:
  s=result.get('EXPAND',core['EXPAND']).replace('CMP AL,64\nJE EXPANDNAME\n','');a=s.index('EXPANDNAME:\n');b=s.index('EXPANDDONE:\n',a);result['EXPAND']=s[:a]+s[b:]
 if level<6:result['ARGUMENTS']='ARGUMENTS:\nMOV AL,[CLASS]\nCMP AL,0\nJE ARGZERO\nCALL NAMEARG\nARGZERO:\nRET\n'
 elif level<7:result['ARGUMENTS']='ARGUMENTS:\nMOV AL,[CLASS]\nCMP AL,0\nJE ARGZERO\nCMP AL,1\nJNE ARGONE\nCALL NUMARG\nRET\nARGONE:\nCALL NAMEARG\nARGZERO:\nRET\n'
 elif level<9:
  s=core['ARGUMENTS'];a=s.index('MOV AL,[CLASS]\nCMP AL,4\nJNE ARGBUFFER',s.index('CALL NUMARG\n',s.index('ARGNAME:')));b=s.index('ARGDONE:\n',a);result['ARGUMENTS']=s[:a]+s[b:]
 elif level<15:
  s=core['ARGUMENTS'];a=s.index('ARGBUFFER:\n');b=s.index('ARGDONE:\n',a);result['ARGUMENTS']=s[:a]+s[b:];result['ARGUMENTS']=result['ARGUMENTS'].replace('JNE ARGBUFFER','JNE ARGDONE')
 if level<28:
  s=core['FLOW'].replace('CMP AL,6\nJE STACKTWO\n','');a=s.index('STACKTWO:\n');b=s.index('STACKFULL:\n',a);result['FLOW']=s[:a]+s[b:]
 if level<16:result['FINISHOUTPUT']=core['FINISHOUTPUT'].replace('MOV AL,0\nMOV [CLASS],AL\nMOV AL,5\nMOV [INSIZE],AL\nCALL SIZEADD\n','')
 return result
def render(level,names,mode=None):
 selected=part_names(level)
 for i,part in enumerate(selected):textfield('T_RT'+part,(PARTS[part]+('\n' if i+1<len(selected) else '')).replace('\n','\r\n')+'\0')
 available={**lib,**core,**variants(level,names)}
 if mode=='lookup':
  body='''CALL SCAN
MOV BX,OPTAB
MOV CX,2
MOV AX,14
CALL LOOK
CMP BX,0
JNE RECORDOK
MOV AX,1
JMP ERROR
RECORDOK:
ADD BX,10
MOV AL,[BX]
MOV AH,0
PUSH AX
CALL FINISH
POP AX
CALL NUMBER
MOV DX,NEWLINE
CALL TEXT
'''
  prefix=main(3).split('CALL OPENFILE\n',1)[0]
  available['START']=prefix+READ+body+CLOSE+'MOV AX,4C00H\nINT 21H\n'
 if mode=='names':
  available['START']=main(4)
  available['STATEMENT']=available['STATEMENT'].replace('CALL CONTEXT\n','')
 code={'START':available['START']}
 if mode=='lookup':
  for name in ['OUTTEXT','WRITEOUT']:code[name]=available[name]
 owner={}
 for k,s in available.items():
  for name in re.findall(r'^(\w+):$',s,re.M):owner[name]=k
 while True:
  joined='\n'.join(code.values());defined=set(re.findall(r'^(\w+):$',joined,re.M));refs=set(re.findall(r'\b[A-Z][A-Z0-9_]*\b',joined))
  fresh={owner[t] for t in refs-defined if t in owner}-set(code)
  if not fresh:break
  for k in fresh:code[k]=available[k]
 result='; IR86 construction source. Assemble with ASM86.\n'+code['START']
 for k in ORDER:
  if k in code:result+='\n'+code[k]
 refs=set(re.findall(r'\b[A-Z][A-Z0-9_]*\b',result));todo=[n for n in BASEORDER if n in refs]
 # Table pointers refer to templates not mentioned in executable source.
 todo+=['T_'+n for n in names if 'T_'+n not in todo]
 if level>=4:
  table='OPTAB:\n'
  for op in names:
   cls,effect,size=OPS[op];row=list(op.encode())+[0]*(8-len(op))+[cls,effect,size,0]
   table+='DB '+','.join(map(str,row))+'\nDW T_'+op+'\n'
  result+='\n'+table
 for name in dict.fromkeys(todo):
  if name in fields:result+='\n'+fields[name]
 # DIVEND and FOUREND must immediately follow their divisor arrays.
 for begin,end in [('DIVISORS','DIVEND'),('FOURDIV','FOUREND')]:
  if begin in todo and end in todo:
   result=result.replace('\n'+end+':\n','');needle=fields[begin].rstrip();result=result.replace(needle,needle+'\n'+end+':')
 return result

# Manuscript specifications are kept separate from the source formatter.
specs=json.loads((ROOT/'tools/ir86_installments.json').read_text())
names=[];manifest=[]
for spec in specs:
 number=spec['number'];level=spec['level'];names+=spec['add'].split();source=render(level,names,spec.get('mode'))
 filename=f'IR{number:02}.ASM';dos(W/filename,source)
 if spec.get('fixture') is not None:dos(W/f'T{number:02}.IR',spec['fixture'])
 if spec.get('bad') is not None:dos(W/f'X{number:02}.IR',spec['bad']['text'])
 manifest.append({**spec,'source':filename,'names':names.copy()})
dos(W/'IR86.ASM',source)
(Q/'checkpoints.json').write_text(json.dumps(manifest,indent=2)+'\n')
(Q/'language.json').write_text(json.dumps({n:{'class':OPS[n][0],'effect':OPS[n][1]} for n in names},indent=2)+'\n')
(Q/'backend-8086.json').write_text(json.dumps({'operations':{n:{'bytes':OPS[n][2],'template':TEMPLATES[n]} for n in names},'profiles':PROFILES},indent=2)+'\n')
print('Prepared IR86 construction source and language records.')
