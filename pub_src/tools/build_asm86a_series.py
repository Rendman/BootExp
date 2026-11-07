"""Lay out authored assembly milestones for the ASM86A type-in collection."""
from pathlib import Path
import json,re
from build_asm86a import ROOT,W,Q,LIB,fields,SEED,STARTS,seed_source,full_source,fit_source_branches,fieldtext,dos

def rewrite(code,mapping):
 pattern=re.compile(r'(?<![A-Z0-9_])('+'|'.join(re.escape(k) for k in mapping)+r')(?![A-Z0-9_])')
 return {k:pattern.sub(lambda m:mapping[m[0]],v) for k,v in code.items()}
def dispatch(code,table,equ=False):
 kinds={int(v.split(',')[-2]) for v in table.splitlines()[1:] if v.startswith('DB ')}
 if equ:
  pre=full_source(True,fit=False)[0]['STATEMENT'].split('MOV BX,OPTAB\n',1)[0]
  tail=full_source(True,fit=False)[0]['STATEMENT'].split('SYNTAXBAD:\n',1)[1]
  tail='SYNTAXBAD:\n'+tail
 else:
  pre=code['STATEMENT'].split('MOV BX,OPTAB\n',1)[0]
  tail='SYNTAXBAD:\nMOV AX,1\nJMP ERROR\n'
 n=len([v for v in table.splitlines() if v.startswith('DB ')])
 out=pre+f'MOV BX,OPTAB\nMOV CX,{n}\nMOV AX,8\nCALL LOOK\nCMP BX,0\nJE SYNTAXBAD\nADD BX,6\nMOV AL,[BX]\nMOV [TYPE],AL\nINC BX\nMOV AL,[BX]\nMOV [OP],AL\nMOV AL,[TYPE]\n'
 for cls,target in [(1,'DATAITEM'),(2,'FIXED'),(5,'SINGLE'),(6,'INTERRUPT'),(7,'NEARJUMP'),(8,'SHORTJUMP'),(9,'GROUP'),(10,'SHIFT'),(12,'RESERVE'),(13,'REPEAT'),(14,'RETURNOP')]:
  if cls in kinds:out+=f'CMP AL,{cls}\nJNE DISPATCH{cls}\nCALL {target}\nRET\nDISPATCH{cls}:\n'
 out+='CALL TWOOPERANDS\nCALL FINISH\nRET\n'+tail
 return out

def assemble_source(code,f,fit=False,roots=()):
 if fit:code=fit_source_branches(code)
 owners={label:k for k,v in code.items() for label in re.findall(r'^([A-Z][A-Z0-9_]*):$',v,re.M)}
 selected={'START',*roots}
 while True:
  refs=set(re.findall(r'\b[A-Z][A-Z0-9_]*\b','\n'.join(code[k] for k in selected)))
  needed={owners[r] for r in refs if r in owners}
  if needed<=selected:break
  selected|=needed
 order=['START']+[k for k in STARTS[1:-1] if k in selected]+[k for k in code if k not in STARTS and k in selected]
 s='; ASM86A construction checkpoint.\n'+'\n'.join(code[k] for k in order)
 refs=set(re.findall(r'\b[A-Z][A-Z0-9_]*\b',s))
 # Allocation descriptors are a contiguous group; HASHSEG follows eight page words.
 if 'MEMSEGS' in refs:refs.add('HASHSEG')
 for k,v in f.items():
  if k in refs:s+='\n'+v
 return s

def seed_stage(n):
 code,f,_=seed_source(True)
 for key,value in fields.items():
  if key not in f:f[key]=value
 if n<9:
  code=rewrite(code,{'4000H':'2200H','4080H':'2300H','4082H':'2302H','4090H':'2310H','5000H':'3000H','4200H':'5000H','4600H':'6000H'})
  code['DEFINE']=code['DEFINE'].replace('CMP AX,2048','CMP AX,256')
 if n<8:code['READLINE']=LIB['READLINE']
 if n<10:
  for key in ['OPERAND','TWOOPERANDS','MOVOPERANDS','LOADMEM','STOREMEM','REGISTER']:code[key]=LIB[key]
  for key in ['GETNAME']:code.pop(key,None)
  f['REGTAB']=fields['REGTAB']
  # Adapt the unchanged parser to whichever line/token memory map is active.
  mapping={'2200H':'4000H','2300H':'4080H','2302H':'4082H','2310H':'4090H'} if n>=9 else {}
  for key in ['OPERAND','TWOOPERANDS','MOVOPERANDS','LOADMEM','STOREMEM','REGISTER']:
   if mapping:code[key]=rewrite({key:code[key]},mapping)[key]
 if n==10:
  seg=code['SEGOPERAND'];a=seg.index('POP AX\n');b=seg.index('SEGREGISTER:\n');code['SEGOPERAND']=seg[:a]+'POP AX\nJMP TWOBAD\n'+seg[b:]
 if n<=2:
  start=LIB['START'].replace('CALL GETNAME\n','')
  if n==2:start=start.replace('MOV [LINENO],AX\n','MOV [LINENO],AX\nMOV [RDPOS],AX\nMOV [RDLEN],AX\n')
  code['START']=start
  code['EMIT']=LIB['EMIT'];code['ERROR']=LIB['ERROR'].split('PROMPT:\n')[0]
  if n==1:code['NEXTBYTE']=LIB['NEXTBYTE']
  out=LIB['WRITEOUT'];a=out.index('MOV DX,FNAME\n');out='WRITEOUT:\n'+out[a:];out=out.replace('MOV DX,FNAME','MOV DX,RESNAME');code['WRITEOUT']=out
 if 3<=n<=6:
  before='CALL PREFLIGHT\n' if n>=5 else ''
  code['START']='''START:
CLD
CMP SP,0FFFEH
JE ROOM
MOV AX,7
JMP ERROR
ROOM:
'''+before+'''MOV AX,0
MOV [RDPOS],AX
MOV [RDLEN],AX
MOV [OUTCNT],AX
MOV [LINENO],AX
MOV AX,100H
MOV [PC],AX
MOV AL,2
MOV [PASS],AL
CALL CREATEOUT
CALL OPENFILE
COPYBYTE:
CALL NEXTBYTE
CMP AX,0
JE COPYDONE
MOV AL,[CHAR]
CALL EMIT
JMP COPYBYTE
COPYDONE:
CALL CLOSEFILE
CALL FLUSH
CALL CLOSEOUT
'''+('CALL COMMIT\n' if n>=6 else '')+'''MOV DX,OKMSG
CALL TEXT
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
MOV AX,4C00H
INT 21H
'''
  if n<6:f['OKMSG']=fieldtext('OKMSG','OK ASMA.TMP $')
 if n==3:code['ERROR']=LIB['ERROR'].split('PROMPT:\n')[0]
 if n<9:
  # Variants restored from the original reader use the original addresses.
  for key in ['OPERAND','TWOOPERANDS','MOVOPERANDS','LOADMEM','STOREMEM','REGISTER']:
   code[key]=rewrite({key:code[key]},{'4080H':'2300H','4082H':'2302H'})[key]
 if n<9:code['START']=code['START'].replace('MOV AX,5000H\nMOV [SYMNEXT],AX','MOV AX,3000H\nMOV [SYMNEXT],AX')
 if n<=2:code['WRITEOUT']=fit_source_branches(code)['WRITEOUT']
 return assemble_source(code,f,roots=('STATEMENT','READLINE') if 3<=n<=6 else ())

def full_stage(n):
 core,cf,_=full_source(True,profile='core',fit=False)
 whole,wf,_=full_source(True,fit=False)
 # Native memory/record helpers are introduced while retaining the seed grammar.
 if n<=16:
  code,f,_=seed_source(True)
  for k in ['MEMINIT','MEMFREE']:code[k]=core[k]
  for k,v in cf.items():
   if k not in f:f[k]=v
  code['START']=code['START'].replace('CALL PREFLIGHT','CALL MEMINIT\nCALL EARLYTEST\nCALL PREFLIGHT').replace('CALL COMMIT\n','CALL COMMIT\nCALL MEMFREE\n')
  code['CLEANUP']=code['CLEANUP'].replace('CLEANEND:\nRET','CLEANEND:\nCALL MEMFREE\nRET')
  test='EARLYTEST:\n'
  if n==13:
   code['START']=code['START'].replace('CALL EARLYTEST\n','')
  if n>=14:
   code['SYMPTR']=core['SYMPTR']
   if n==14:test+='MOV AX,8192\nCALL SYMPTR\nMOV AX,42\nMOV ES:[BX],AX\nMOV AX,ES:[BX]\nMOV DX,CS\nMOV ES,DX\nCMP AX,42\nJE EARLYPASS\nMOV AX,7\nJMP ERROR\nEARLYPASS:\nRET\n'
  if n>=15:
   code['RECORDWRITE']=core['RECORDWRITE'].replace('0CC00H','4080H')
   test+='PUSH SI\nMOV SI,TESTNAME\nMOV DI,4080H\nCALL COPYZ\nPOP SI\n'
   if n==16:
    code['SYMLOOK']=core['SYMLOOK'].replace('0CC00H','4080H');test+='CALL SYMLOOK\n'
   test+='MOV AX,8192\nMOV [SYMID],AX\nMOV AX,12345\nMOV [DEFVALUE],AX\nMOV AX,0\nMOV [DEFTYPE],AX\nMOV [HEADID],AX\nMOV [BUCKET],AX\n'
   if n==16:
    # Recover the real bucket, rather than the zero used by the record-store diagnostic.
    test+='CALL SYMLOOK\nMOV AX,8192\nMOV [SYMID],AX\n'
   test+='MOV AX,[SYMID]\nCALL RECORDWRITE\n'
   if n==16:test+='CALL SYMLOOK\nMOV AX,[SYMID]\nCALL SYMPTR\n'
   else:test+='MOV AX,8192\nCALL SYMPTR\n'
   test+='ADD BX,32\nMOV AX,ES:[BX]\nMOV DX,CS\nMOV ES,DX\nCMP AX,12345\nJE EARLYPASS\nMOV AX,7\nJMP ERROR\nEARLYPASS:\nRET\n'
   f['TESTNAME']=fieldtext('TESTNAME','PAGED\0')
  if n>=14:code['EARLYTEST']=test
  return assemble_source(code,f,True)
 code,f=core,dict(wf)
 if n==17:
  code=rewrite(code,{'0C800H':'4000H','0CC00H':'4080H','0CC02H':'4082H','0CC3FH':'4090H','0D000H':'4200H','0E000H':'4600H'})
  code['READLINE']=code['READLINE'].replace('CMP BP,1023','CMP BP,120')
  for key in ['NEXTBYTE','EMIT']:code[key]=code[key].replace('4096','1024')
 if n>=19:
  for key in ['COUNTLINE','COUNTINPUT','NUMBER32']:code[key]=whole[key]
  code['START']=whole['START']
  code['NEXTBYTE']=whole['NEXTBYTE']
  reader=code['READLINE'];a=reader.index('MOV AX,[LINENO]\n',reader.index('LINEEND:'));b=reader.index('MOV AX,1\n',a);reader=reader[:a]+'CALL COUNTLINE\n'+reader[b:]
  a=reader.index('READFAIL:\n')+len('READFAIL:\n');b=reader.index('JMP ERROR\n',a);reader=reader[:a]+'PUSH AX\nCALL COUNTLINE\nPOP AX\n'+reader[b:];code['READLINE']=reader
  code['ERROR']=whole['ERROR']
 if n>=20:
  code['READLINE']=whole['READLINE']
  for key in ['SCAN','DATAITEM']:code[key]=whole[key]
 if n>=21:
  for key in ['VALUE','ATOM','BYTEVALUE']:code[key]=whole[key]
 if n>=23:code['RESERVE']=whole['RESERVE']
 if n>=24:code['SHORTJUMP']=whole['SHORTJUMP']
 if n>=25:
  code['RMHELPERS']=whole['RMHELPERS']
  code['MEMORY']=code['MEMORY'].replace('MEMORY:\n','MEMORY:\nMOV AL,0\nMOV [MOD],AL\n').replace('MEMORYOK:\nRET','MEMORYOK:\nMOV AL,255\nMOV [WIDTH],AL\nRET')
  code['TWOOPERANDS']=code['TWOOPERANDS'].replace('MOV [R1],AL\n','MOV [R1],AL\nMOV AL,[MOD]\nMOV [M1],AL\n')
  # The copied descriptors now supply the existing load/store encodings.
  code['LOADMEM']=code['LOADMEM'].replace('LOADMEM:\n','LOADMEM:\nCALL RMCURRENT\n').replace('[REG]','[RMREG]').replace('[VAL]','[RMDISP]')
  code['STOREMEM']=code['STOREMEM'].replace('STOREOK:\n','STOREOK:\nCALL RMFIRST\n').replace('[R1]','[RMREG]').replace('[V1]','[RMDISP]')
 if n>=26:
  for key in ['ENCODE','WIDTHHELPERS','EMITIMM']:code[key]=whole[key]
  code['LOADMEM']='''LOADMEM:
CALL RMCURRENT
MOV AL,[W1]
CALL CHECKWIDTH
MOV AL,[R1]
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
ADD AL,138
MOV [ENCOP],AL
JMP ENCODE
'''
  code['STOREMEM']='''STOREMEM:
MOV AL,[KIND]
CMP AL,1
JNE TWOBAD
CALL RMFIRST
MOV AL,[WIDTH]
CALL CHECKWIDTH
MOV AL,[REG]
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
ADD AL,136
MOV [ENCOP],AL
JMP ENCODE
'''
  code['OPERAND']=code['OPERAND'].replace('OPERAND:\n','OPERAND:\nMOV AL,255\nMOV [EXWIDTH],AL\n')
 if n>=27:
  code['MEMMAP']=whole['MEMMAP']
  code['MEMORY']='''MEMORY:
MOV AX,0
MOV [MEMDISP],AX
MOV [ADDRMASK],AL
MOV [MEMHAD],AL
CALL SCAN
MOV AX,[0CC00H]
CMP AX,5842H
JNE SIMPLEMEMVAL
MOV AL,[0CC02H]
CMP AL,0
JNE SIMPLEMEMVAL
MOV AL,1
MOV [ADDRMASK],AL
JMP SIMPLEMEMEND
SIMPLEMEMVAL:
CALL VALUE
MOV [MEMDISP],AX
MOV AL,1
MOV [MEMHAD],AL
SIMPLEMEMEND:
CALL SCAN
MOV AL,[0CC00H]
CMP AL,93
JNE TWOBAD
JMP MEMFINISH
'''
 if n>=28:code['OPERAND']=whole['OPERAND']
 if n>=29:code['MEMORY']=whole['MEMORY']
 if n>=30:code['MOVOPERANDS']=whole['MOVOPERANDS']
 if n>=31:
  code['TWOOPERANDS']=whole['TWOOPERANDS']
  if n<32:code['TWOOPERANDS']=code['TWOOPERANDS'].replace('CMP AL,11\nJE LEAOP\n','')
  code['MATHOPERANDS']=whole['MATHOPERANDS']
 if n>=32:code['LEAOP']=whole['LEAOP']
 if n>=33:code['NEARJUMP']=whole['NEARJUMP']
 if n>=34:code['RETURNOP']=whole['RETURNOP']
 if n>=35:code['GROUP']=whole['GROUP']
 if n>=37:
  code['SHIFT']=whole['SHIFT']
 if n>=39:code['REPEAT']=whole['REPEAT']
 allowed={'DB','DW','NOP','RET','CLD','LODSB','STOSB','MOV','ADD','OR','AND','SUB','XOR','CMP','INC','DEC','PUSH','POP','INT','CALL','JMP','JB','JAE','JE','JNE','JBE','JA','JL','JGE','JLE','JG'}
 for at,names in [(23,'RESB RESW'),(24,'JZ JNZ JC JNC'),(31,'ADC SBB TEST'),(32,'LEA'),(35,'NEG NOT'),(36,'MUL DIV IMUL IDIV'),(37,'SHL SHR SAR'),(38,'SAL ROL ROR RCL RCR'),(39,'LODSW STOSW MOVSB MOVSW REP')]:
  if n>=at:allowed.update(names.split())
 rows=[]
 for line in wf['OPTAB'].splitlines()[1:]:
  row=[int(b) for b in line[3:].split(',')];name=bytes(row[:6]).split(b'\0')[0].decode()
  if name in allowed:
   if name=='RET' and n<34:line='DB 82,69,84,0,0,0,2,195'
   rows.append(line)
 f['OPTAB']='OPTAB:\n'+'\n'.join(rows)+'\n'
 code['STATEMENT']=dispatch(code,f['OPTAB'],equ=n>=22)
 return assemble_source(code,f,True)

def source(n):return seed_stage(n) if n<=12 else full_stage(n)
def build_all():
 cases=[c for c in json.loads((ROOT/'tools/asm86a_installments.json').read_text()) if c['number'] not in [34,35,38,39]]
 for c in cases:
  n=c['number'];dos(W/f'A{n:02}.ASM',source(n))
  if c.get('fixture') is not None:dos(W/f'T{n:02}.ASM',c['fixture'])
  if c.get('bad',{}).get('kind')=='source':dos(W/f'X{n:02}.ASM',c['bad']['text'])
 dos(W/'ASMA0.ASM',source(12));dos(W/'ASM86A.ASM',source(40))
 (Q/'checkpoints.json').write_text(json.dumps(cases,indent=2)+'\n')
 print('Prepared ASM86A manuscript source checkpoints, never executable bytes')

if __name__=='__main__':build_all()
