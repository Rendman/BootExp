"""Arrange authored assembly into bootstrap checkpoints; never encode an instruction."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/asm86a';Q=ROOT/'qa/asm86a'
BASE=(ROOT/'workbench/asm86/ASM86.ASM').read_text()
STARTS=['START','FILEBAD','OPENFILE','CLOSEFILE','WRITEOUT','GETNAME','NEXTBYTE','READLINE','SCAN','LOOK','REGISTER','VALIDNAME','VALUE','SYMBOLVALUE','DEFINE','OPERAND','MEMORY','STATEMENT','DATAITEM','FIXED','SINGLE','INTERRUPT','NEARJUMP','SHORTJUMP','FINISH','TWOOPERANDS','MOVOPERANDS','MOVREG','REGMOD','IMMEDVALUE','LOADMEM','STOREMEM','SAMEWIDTH','TIMES8','BYTEVALUE','EMITWORD','EMIT','COPYZ','TEXT','NUMBER','ERROR','OKMSG']
pos={k:BASE.index(k+':\n') for k in STARTS}
LIB={k:BASE[pos[k]:pos[v]].strip()+'\n' for k,v in zip(STARTS,STARTS[1:])}
for k in LIB:LIB[k]='\n'.join(l for l in LIB[k].splitlines() if l and not l.startswith(';'))+'\n'
data=BASE[pos['OKMSG']:];fields={};matches=list(re.finditer(r'^([A-Z][A-Z0-9_]*):$',data,re.M))
for i,m in enumerate(matches):fields[m[1]]=data[m.start():matches[i+1].start() if i+1<len(matches) else len(data)].strip()+'\n'
def blocks(path):
 parts=re.split(r'^; @block (\w+)\n',path.read_text(),flags=re.M)
 return {parts[i]:parts[i+1].strip()+'\n' for i in range(1,len(parts),2)}
SEED=blocks(ROOT/'tools/asm86a_seed.asm')
def fieldtext(name,text):
 data=text.encode();return name+':\n'+''.join('DB '+','.join(str(b) for b in data[i:i+16])+'\n' for i in range(0,len(data),16))
def seed_source(parts=False):
 code=dict(LIB);code.update(SEED)
 for k in ['GETNAME','WRITEOUT']:code.pop(k,None)
 # The seed has its own fixed memory map.
 for k,s in list(code.items()):
  if k in SEED:continue
  for old,new in [('2200H','4000H'),('2300H','4080H'),('2302H','4082H'),('2310H','4090H'),('3000H','5000H')]:s=s.replace(old,new)
  code[k]=s
 code['READLINE']=code['READLINE'].replace('CMP AX,4000\nJA READFULL','CMP AX,0\nJNE LINECOUNTSAFE\nMOV AX,5\nJMP ERROR\nLINECOUNTSAFE:')
 code['READLINE']=code['READLINE'].replace('MOV DX,[LINENO]\nINC DX\n','MOV DX,[LINENO]\nCMP DX,0FFFFH\nJE READLIMIT\nINC DX\nREADLIMIT:\n')
 code['DEFINE']=code['DEFINE'].replace('CMP AX,256\n','CMP AX,2048\n')
 code['REGISTER']=code['REGISTER'].replace('MOV CX,16\n','MOV CX,20\n')
 code['OPERAND']=code['OPERAND'].replace('CALL SCAN\n','MOV AL,0\nMOV [PREFIX],AL\nCALL SCAN\n',1).replace('JE IMMEDIATE\n','JE IMMEDIATE\nCMP AX,16\nJB NORMALREGISTER\nJMP SEGOPERAND\nNORMALREGISTER:\n',1)
 code['TWOOPERANDS']=code['TWOOPERANDS'].replace('MOV [R1],AL\n','MOV [R1],AL\nMOV AL,[PREFIX]\nMOV [P1],AL\n')
 code['MOVOPERANDS']=code['MOVOPERANDS'].replace('MOVOPERANDS:\n','MOVOPERANDS:\nMOV AL,[K1]\nCMP AL,4\nJNE MOVNOTSEG\nJMP SEGMOV\nMOVNOTSEG:\nMOV AL,[KIND]\nCMP AL,4\nJNE MOVNOTSRC\nJMP SEGMOV\nMOVNOTSRC:\n')
 code['LOADMEM']=code['LOADMEM'].replace('LOADMEM:\n','LOADMEM:\nMOV AL,[PREFIX]\nCMP AL,0\nJE LOADPREFIX\nCALL EMIT\nLOADPREFIX:\n')
 code['STOREMEM']=code['STOREMEM'].replace('STOREOK:\n','STOREOK:\nMOV AL,[P1]\nCMP AL,0\nJE STOREPREFIX\nCALL EMIT\nSTOREPREFIX:\n')
 code['IMMEDVALUE']=code['IMMEDVALUE'].replace('JE BYTEVALUE\n','JNE IMMEDWORD\nJMP BYTEVALUE\nIMMEDWORD:\n')
 f=dict(fields)
 for k in ['EXTP','FNAME','COMEXT','ASMEXT','OUTPTR']:f.pop(k,None)
 f['OKMSG']=fieldtext('OKMSG','OK RESULT.COM $')
 for k,t in [('SRCNAME','SOURCE.ASM\0'),('TMPNAME','ASMA.TMP\0'),('RESNAME','RESULT.COM\0'),('BAKNAME','RESULT.BAK\0'),('RECOVERMSG','Recovery: inspect ASMA.TMP and RESULT.BAK\r\n$')]:f[k]=fieldtext(k,t)
 for k in ['RDPOS','RDLEN','OUTCNT','OUTHANDLE','ENDPC','SEGCODE']:f[k]=k+':\nDW 0\n'
 for k in ['INOPEN','OUTOPEN','OWNTMP','HAVEBAK','KEEPFILES','CLEANFAIL','PREFIX','P1']:f[k]=k+':\nDB 0\n'
 f['REGTAB']+='DB 69,83,0,16\nDB 67,83,0,17\nDB 83,83,0,18\nDB 68,83,0,19\n'
 order=['START']+[k for k in STARTS[1:-1] if k in code]+[k for k in SEED if k not in STARTS]
 if parts:return code,f,order
 return '; ASMA0: fixed-file streaming bootstrap assembler.\n'+'\n'.join(code[k] for k in order)+'\n'+'\n'.join(f.values())
def fit_source_branches(code):
 # Author explicit opposite-condition/near-JMP source for distant local labels.
 # This produces assembly text only; the published assembler alone encodes it.
 opposite={'JE':'JNE','JNE':'JE','JB':'JAE','JAE':'JB','JA':'JBE','JBE':'JA','JL':'JGE','JGE':'JL','JG':'JLE','JLE':'JG'}
 order=[k for k in STARTS[:-1] if k in code]+[k for k in code if k not in STARTS]
 base={};all_labels={};cursor=0
 for key in order:
  base[key]=cursor
  for i,line in enumerate(code[key].splitlines()):
   if re.fullmatch('[A-Z][A-Z0-9_]*:',line):all_labels[line[:-1]]=cursor+i
  cursor+=len(code[key].splitlines())
 result={}
 for key,text in code.items():
  lines=text.splitlines();local={v[:-1]:i for i,v in enumerate(lines) if v.endswith(':')};out=[];counter=0
  for i,line in enumerate(lines):
   words=line.split()
   if len(words)==2 and words[0] in opposite and words[1] in all_labels and abs(all_labels[words[1]]-(base[key]+i))>16:
    counter+=1;label='Z'+key[:8]+str(counter)
    out.extend([opposite[words[0]]+' '+label,'JMP '+words[1],label+':'])
   else:out.append(line)
  result[key]='\n'.join(out)+'\n'
 return result
def full_source(parts=False,profile="full",fit=True):
 code,f,order=seed_source(True)
 for k,s in list(code.items()):
  for old,new in [('4000H','0C800H'),('4080H','0CC00H'),('4082H','0CC02H'),('4090H','0CC3FH'),('4200H','0D000H'),('4600H','0E000H')]:s=s.replace(old,new)
  if k in ['EMIT','NEXTBYTE']:s=s.replace('1024','4096')
  if k=='READLINE':s=s.replace('CMP BP,120','CMP BP,1023')
  code[k]=s
 code.update(blocks(ROOT/'tools/asm86a_memory.asm'))
 code['START']=code['START'].replace('CALL PREFLIGHT','CALL MEMINIT\nCALL PREFLIGHT').replace('MOV AX,5000H\nMOV [SYMNEXT],AX\n','')
 code['START']=code['START'].replace('MOV [OUTCNT],AX\n','MOV [OUTCNT],AX\nMOV [DEFSEEN],AX\n')
 code['START']=code['START'].replace('PASSVALID:\n','PASSVALID:\nMOV AX,[DEFSEEN]\nMOV DX,[SYMC]\nCMP AX,DX\nJE DEFINITIONCOUNT\nMOV AX,3\nJMP ERROR\nDEFINITIONCOUNT:\n')
 code['START']=code['START'].replace('CALL COMMIT\n','CALL COMMIT\nCALL MEMFREE\nMOV AL,[CLEANFAIL]\nCMP AL,0\nJE FINALCLEAN\nMOV AX,7\nJMP ERROR\nFINALCLEAN:\n')
 code['CLEANUP']=code['CLEANUP'].replace('CLEANEND:\nRET','CLEANEND:\nCALL MEMFREE\nRET')
 code['STATEMENT']=code['STATEMENT'].replace('CALL DEFINE\n','MOV AX,[PC]\nMOV [DEFVALUE],AX\nMOV AX,0\nMOV [DEFTYPE],AX\nCALL DEFINE\n')
 code['VALIDNAME']=code['VALIDNAME'].replace('VALIDNAME:\n','VALIDNAME:\nMOV AX,[TOKLEN]\nCMP AX,31\nJBE NAMELIMIT\nJMP SYMBOLBAD\nNAMELIMIT:\n')
 f.pop('SYMNEXT',None)
 for k in ['MEMNEXT','MEMCOUNT','RECORDPTR','BUCKET','HEADID','SYMID','DEFVALUE','DEFTYPE','DEFSEEN']:f[k]=k+':\nDW 0\n'
 f['MEMSEGS']='MEMSEGS:\nDW 0,0,0,0,0,0,0,0\n';f['HASHSEG']='HASHSEG:\nDW 0\n'
 f['UNRESOLVED']='UNRESOLVED:\nDB 0\n'
 if profile=='core':
  if fit:code=fit_source_branches(code)
  order=[k for k in order if k in code]+[k for k in code if k not in order]
  if parts:return code,f,order
  return '; ASM86A capacity core.\n'+'\n'.join(code[k] for k in order)+'\n'+'\n'.join(f.values())
 # Full language remains implemented in the seed's accepted source vocabulary.
 oldvalue=code['VALUE'].replace('VALUE:\n','ATOM:\n',1)
 language=blocks(ROOT/'tools/asm86a_language.asm')
 for k in ['MOVREG','REGMOD','IMMEDVALUE','LOADMEM','STOREMEM','SAMEWIDTH','SEGOPERAND','SEGMOV']:code.pop(k,None)
 code.update(language);code['ATOM']=oldvalue
 # Preserve source bytes; only the scanner folds identifiers outside strings.
 reader=code['READLINE']
 reader=reader.replace('JE TABCHAR','JE KEEPCHAR')
 a=reader.index('CMP AL,97\n');b=reader.index('KEEPCHAR:\n',a)
 reader=reader[:a]+reader[b:]
 code['READLINE']=reader
 rows=fields['OPTAB'].splitlines()[1:]
 def row(name,kind,parameter):return 'DB '+','.join(str(b) for b in name.encode().ljust(6,b'\0')+bytes([kind,parameter]))
 rows=[row('RET',14,195) if v.startswith('DB 82,69,84,') else v for v in rows]
 additional=[('RESB',12,0),('RESW',12,1),('LEA',11,0),('ADC',4,2),('SBB',4,3),('TEST',15,0),('NEG',9,3),('NOT',9,2),('MUL',9,4),('IMUL',9,5),('DIV',9,6),('IDIV',9,7),('SHL',10,4),('SAL',10,4),('SHR',10,5),('SAR',10,7),('ROL',10,0),('ROR',10,1),('RCL',10,2),('RCR',10,3),('LODSW',2,173),('STOSW',2,171),('MOVSB',2,164),('MOVSW',2,165),('REP',13,243),('JZ',8,116),('JNZ',8,117),('JC',8,114),('JNC',8,115)]
 rows.extend(row(*r) for r in additional)
 f['OPTAB']='OPTAB:\n'+'\n'.join(rows)+'\n'
 code['STATEMENT']=code['STATEMENT'].replace('MOV CX,31\n',f'MOV CX,{len(rows)}\n')
 f['STRINGTAB']='STRINGTAB:\n'+'\n'.join(row(n,2,v) for n,v in [('MOVSB',164),('MOVSW',165),('STOSB',170),('STOSW',171),('LODSB',172),('LODSW',173)])+'\n'
 for k in ['EXPRDEPTH','NAMELEN','MEMDISP','RMDISP','IMMVAL','BRDEST']:f[k]=k+':\nDW 0\n'
 for k in ['EXWIDTH','MOD','ADDRMASK','MEMHAD','MEMSIGN','M1','RMKIND','RMREG','RMWIDTH','RMMOD','RMPREFIX','ENCWIDTH','ENCOP','REGFIELD','STRINGOP']:f[k]=k+':\nDB 0\n'
 code.update(blocks(ROOT/'tools/asm86a_counts.asm'))
 code['START']=code['START'].replace('MOV [LINENO],AX\n','MOV [LINENO],AX\nMOV [LINEHI],AX\nMOV [INBYTES],AX\nMOV [INBYTEHI],AX\n')
 reader=code['READLINE']
 a=reader.index('MOV AX,[LINENO]\n',reader.index('LINEEND:'));b=reader.index('MOV AX,1\n',a)
 reader=reader[:a]+'CALL COUNTLINE\n'+reader[b:]
 a=reader.index('READFAIL:\n')+len('READFAIL:\n');b=reader.index('JMP ERROR\n',a)
 reader=reader[:a]+'PUSH AX\nCALL COUNTLINE\nPOP AX\n'+reader[b:]
 code['READLINE']=reader
 code['NEXTBYTE']=code['NEXTBYTE'].replace('MOV [RDPOS],AX\nMOV AX,1\n','MOV [RDPOS],AX\nCALL COUNTINPUT\nMOV AX,1\n')
 code['ERROR']=code['ERROR'].replace('MOV AX,[LINENO]\nCALL NUMBER\n','MOV AX,[LINENO]\nMOV DX,[LINEHI]\nCALL NUMBER32\n')
 for k in ['LINEHI','INBYTES','INBYTEHI','N32LO','N32HI','D32LO','D32HI']:f[k]=k+':\nDW 0\n'
 divisors=[]
 for value in [10**n for n in range(9,-1,-1)]:divisors.extend([value//65536,value%65536])
 f['DIV32']='DIV32:\n'+''.join('DW '+','.join(str(n) for n in divisors[i:i+6])+'\n' for i in range(0,len(divisors),6))
 f['DIV32END']='DIV32END:\n'
 if fit:code=fit_source_branches(code)
 order=[k for k in order if k in code]+[k for k in code if k not in order]
 if parts:return code,f,order
 return '; ASM86A: allocated symbols and streamed assembly.\n'+'\n'.join(code[k] for k in order)+'\n'+'\n'.join(f.values())
def dos(path,text):path.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
if __name__=='__main__':
 from build_asm86a_series import build_all
 build_all()
