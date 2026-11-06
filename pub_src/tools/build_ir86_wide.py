"""Arrange authored translator assembly and target templates; no host instruction encoder."""
from pathlib import Path
import re,json
from build_asm86a import full_source,blocks,fieldtext,dos,ROOT,W as AW
from ir86_runtime_text import PARTS,part_names
W=ROOT/'workbench/ir86';Q=ROOT/'qa/toolchain';Q.mkdir(exist_ok=True)
# (argument class, stack action, authored assembly text)
OPS={}
def op(name,cls,delta,text):OPS[name]=(cls,delta,text)
op('NOP',0,0,'NOP\n');op('HALT',0,4,'MOV AX,4C00H\nINT 21H\n');op('EXIT',0,4,'MOV AH,4CH\nINT 21H\n')
op('LABEL',2,0,'U_@:\n');op('LIT',1,0,'MOV AX,#\n');op('ADDR',2,0,'MOV AX,U_@\n')
for name,form in [('WORD','DW'),('BYTE','DB'),('BUFFER','RESB')]:op(name,3,4,'U_@:\n'+form+' #\n')
for name,text in {'LD':'MOV AX,[U_@]\n','ST':'MOV [U_@],AX\n','LDB':'MOV AL,[U_@]\nMOV AH,0\n','STB':'MOV [U_@],AL\n'}.items():op(name,2,0,text)
for name,text in {'FETCH':'MOV BX,AX\nMOV AX,[BX]\n','FETCHB':'MOV BX,AX\nMOV AL,[BX]\nMOV AH,0\n','NEG':'NEG AX\n','NOT':'NOT AX\n'}.items():op(name,0,0,text)
op('PUSH',0,1,'PUSH AX\n');op('POP',0,2,'POP AX\n');op('PUT',0,2,'POP BX\nMOV [BX],AX\n');op('PUTB',0,2,'POP BX\nMOV [BX],AL\n')
for name in ['ADD','AND','OR','XOR']:op(name,0,2,'POP BX\n'+name+' AX,BX\n')
op('SUB',0,2,'POP BX\nSUB BX,AX\nMOV AX,BX\n');op('MUL',0,2,'POP BX\nMUL BX\n')
for name in ['DIV','MOD']:op(name,0,2,'MOV BX,AX\nPOP AX\nCMP BX,0\nJE NEAR R_STACKFAIL\nXOR DX,DX\nDIV BX\n'+('MOV AX,DX\n' if name=='MOD' else ''))
for name in ['SHL','SHR']:op(name,0,2,'MOV CX,AX\nAND CX,15\nPOP AX\n'+name+' AX,CL\n')
conditions={'EQ':'JNE','NE':'JE','ULT':'JAE','ULE':'JA','UGT':'JBE','UGE':'JB','SLT':'JGE','SLE':'JG','SGT':'JLE','SGE':'JL'}
for name,inv in conditions.items():
 op(name,2,2,'POP BX\nCMP BX,AX\n'+inv+' $+5\nJMP U_@\n')
 op('C'+name,0,2,'POP BX\nCMP BX,AX\nMOV AX,0\n'+inv+' $+3\nINC AX\n')
for name,inv in [('JZ','JNE'),('JNZ','JE')]:op(name,2,4,'CMP AX,0\n'+inv+' $+5\nJMP U_@\n')
op('JMP',2,4,'JMP U_@\n');op('CALL',2,0,'CALL U_@\n');op('RET',0,4,'RET\n')
op('PROC',4,0,'U_@:\nPUSH BP\nMOV BP,SP\nSUB SP,#\nCMP SP,0F000H\nJB NEAR R_STACKFAIL\n')
op('RETURN',0,4,'MOV SP,BP\nPOP BP\nRET\n')
op('INVOKE',5,0,'CALL U_@\nADD SP,#\n')
op('LOCAL',1,0,'MOV AX,[BP-#]\n');op('SETLOCAL',1,0,'MOV [BP-#],AX\n');op('LADDR',1,0,'LEA AX,[BP-#]\n');op('PARAM',1,0,'MOV AX,[BP+#]\n')
op('SETPARAM',1,0,'MOV [BP+#],AX\n');op('PADDR',1,0,'LEA AX,[BP+#]\n')
op('LITS',6,0,'')
for name in ['PUTC','GETC','OPEN','CREATE','CLOSE']:op(name,0,0,'CALL R_'+name+'\n')
op('STATUS',0,0,'MOV AX,[R_STATUS]\n')
for name in ['READ','WRITE']:op(name,0,3,'POP DX\nPOP BX\nCALL R_'+name+'\n')
for name in ['DELETE','EXISTS','ALLOC','FREEBLOCK']:op(name,0,0,'CALL R_'+name+'\n')
op('RENAME',0,2,'POP DX\nCALL R_RENAME\n')
for name,width in [('GET8',1),('GET16',2)]:op(name,0,2,f'POP BX\nMOV CX,{width}\nCALL R_GETMEM\n')
for name,width in [('SET8',1),('SET16',2)]:op(name,0,3,f'POP DX\nPOP BX\nMOV CX,{width}\nCALL R_SETMEM\n')
HEADER='CLD\nCMP SP,0FFFEH\nJNE NEAR R_STACKFAIL\nCALL U_MAIN\nMOV AH,4CH\nINT 21H\n'
def near(s):return re.sub(r'^(J(?:B|AE|E|NE|BE|A|L|GE|LE|G|C|NC)) ([A-Z_][A-Z0-9_]*)$',r'\1 NEAR \2',s,flags=re.M)
RUNTIME=near('\n'.join(PARTS[n] for n in part_names(32))+'\n'+(ROOT/'tools/ir86_wide_runtime.asm').read_text())
LITS='MOV AX,S_?\nJMP I_?\nS_?:\nDB '
LITSEND='0\nI_?:\n'
def source(ops=None,runtime=None,driver=None,frames=True,strings=True):
 prune=ops is not None or driver is not None
 ops=OPS if ops is None else ops
 runtime=RUNTIME if runtime is None else runtime
 code,f,order=full_source(True,fit=False)
 selected=['FILEBAD','OPENFILE','CLOSEFILE','CREATEOUT','FLUSH','NEXTBYTE','READLINE','SCAN','LOOK','VALIDNAME','ATOM','FINISH','COPYZ','TEXT','NUMBER','ERROR','EXISTS','COMMIT','CLEANUP','COUNTLINE','COUNTINPUT','NUMBER32']
 code={k:code[k] for k in selected}
 code['ATOM']=code['ATOM'].replace('JMP SYMBOLVALUE','JMP NUMBERBAD')
 code['CLEANUP']=code['CLEANUP'].replace('CALL MEMFREE\n','')
 code.update(blocks(ROOT/'tools/ir86_wide.asm'))
 if driver is not None:code['START']=driver
 statement=code['STATEMENT']
 if not frames:
  statement=statement.replace('CMP AL,4\nJE STATPROC\n','').replace('CMP AL,5\nJE STATINVOKE\n','')
  a=statement.index('STATPROC:\n');b=statement.index('STATSTRING:\n',a);statement=statement[:a]+statement[b:]
  a=statement.index('STATLOCAL:\n');b=statement.index('STATFLOW:\n',a);statement=statement[:a]+'STATLOCAL:\n'+statement[b:]
 if not strings:statement=statement.replace('CMP AL,6\nJE STATSTRING\n','').replace('STATSTRING:\nCALL STRINGOUT\nRET\n','')
 code['STATEMENT']=statement

 code['STATEMENT']=code['STATEMENT'].replace('MOV AX,14','MOV AX,16').replace('ADD BX,8','ADD BX,10').replace('MOV CX,OPCOUNT',f'MOV CX,{len(ops)}')
 for name,text in [('SRCNAME','SOURCE.IR\0'),('RESNAME','RESULT.ASM\0'),('TMPNAME','IRTX.TMP\0'),('BAKNAME','IRRES.BAK\0'),('ERRMSG','IR ERROR $'),('OKMSG','OK RESULT.ASM $'),('BYTEMSG',' text bytes\r\n$'),('RECOVERMSG','Recovery: inspect IRTX.TMP and IRRES.BAK\r\n$')]:f[name]=fieldtext(name,text)
 for n in ['TOTALLO','TOTALHI','NUMV','TPL','DEPTH','PARAMS','LOCALS','STRID']:f[n]=n+':\nDW 0\n'
 for n in ['IRCLASS','IRDELTA']:f[n]=n+':\nDB 0\n'
 f['IRNAME']='IRNAME:\nRESB 32\n'
 for name,text in [('HEADER',HEADER),('RUNTIME',runtime),('LITS',LITS),('LITSEND',LITSEND),('STRINGNEXT','\nDB ')]+[(n,r[2]) for n,r in OPS.items() if n!='LITS']:f['T_'+name]=fieldtext('T_'+name,text.replace('\n','\r\n')+'\0')
 f['IRTAB']='IRTAB:\n'+''.join('DB '+','.join(str(b) for b in n.encode().ljust(10,b'\0')+bytes([c,d,0,0]))+'\nDW T_'+n+'\n' for n,(c,d,t) in ops.items())
 owners={n:k for k,v in code.items() for n in re.findall(r'^([A-Z][A-Z0-9_]*):$',v,re.M)}
 used={'START'} if prune else set(code)
 while True:
  refs=set(re.findall(r'\b[A-Z][A-Z0-9_]*\b','\n'.join(code[k] for k in used)))
  needed={owners[r] for r in refs if r in owners}
  if needed<=used:break
  used|=needed
 s=near(code['START']+'\n'+'\n'.join(v for k,v in code.items() if k!='START' and k in used))
 refs=set(re.findall(r'\b[A-Z][A-Z0-9_]*\b',s))
 if 'IRTAB' in refs:refs|={'T_'+n for n in ops}
 for k,v in f.items():
  if k in refs:s+='\n'+v
 # Preserve adjacency of divisor tables and their sentinel labels.
 for begin,end in [('DIVISORS','DIVEND'),('DIV32','DIV32END')]:
  if begin in refs:
   s=s.replace('\n'+end+':\n','');s=s.replace(f[begin].rstrip(),f[begin].rstrip()+'\n'+end+':')
 return '; IR86 streaming native translator. Built with ASM86A.\n'+s
if __name__=='__main__':
 dos(W/'IRWIDE.ASM',source())
 (Q/'wide-ops.json').write_text(json.dumps(OPS,indent=2)+'\n')
 print('Prepared authored IR86 streaming source and target templates')
