"""Authored 8086 command-tail routines and shared publication conventions.

These helpers arrange assembly source; the project assemblers emit its bytes.
"""
from pathlib import Path
import re
import json
from functools import lru_cache

ROOT=Path(__file__).resolve().parents[1]
FC_BINARY=r'C:\DOS\FC.EXE /B'

def binary_comparisons(text):
 return text.replace('FC /B',FC_BINARY)
PARSER='''CMDINIT:
MOV SI,81H
MOV DI,CMDBUF
MOV [CMDPTR],DI
MOV AL,[80H]
MOV AH,0
MOV CX,AX
CMP CX,127
JAE CMDBAD
CMDSKIP:
CMP CX,0
JE CMDDONE
LODSB
DEC CX
CMP AL,32
JE CMDSKIP
CMP AL,9
JE CMDSKIP
MOV BX,[CMDCOUNT]
CMP BX,3
JAE CMDBAD
INC BX
MOV [CMDCOUNT],BX
MOV BX,0
MOV DX,8
CMDCHAR:
CMP AL,46
JE CMDDOT
CMP AL,97
JB CMDUP
CMP AL,122
JA CMDUP
SUB AL,32
CMDUP:
CMP AL,65
JB CMDNUM
CMP AL,90
JBE CMDPUT
CMDNUM:
CMP AL,48
JB CMDEXTRA
CMP AL,57
JBE CMDPUT
CMDEXTRA:
CMP AL,95
JE CMDPUT
CMP AL,45
JNE CMDBAD
CMDPUT:
INC BX
CMP BX,DX
JA CMDBAD
STOSB
JMP CMDNEXT
CMDDOT:
CMP DX,8
JNE CMDBAD
CMP BX,0
JE CMDBAD
MOV DX,3
MOV BX,0
STOSB
CMDNEXT:
CMP CX,0
JE CMDEND
LODSB
DEC CX
CMP AL,32
JE CMDEND
CMP AL,9
JNE CMDCHAR
CMDEND:
CMP BX,0
JE CMDBAD
MOV AL,0
STOSB
MOV DI,[CMDPTR]
ADD DI,13
MOV [CMDPTR],DI
JMP CMDSKIP
CMDDONE:
MOV AX,[CMDCOUNT]
RET
CMDBAD:
MOV AX,65535
RET
'''
DATA='''CMDCOUNT:
DW 0
CMDPTR:
DW 0
CMDBUF:
DB 0,0,0,0,0,0,0,0,0,0,0,0,0
DB 0,0,0,0,0,0,0,0,0,0,0,0,0
DB 0,0,0,0,0,0,0,0,0,0,0,0,0
'''
TEXT='''CMDTEXT:
LODSB
CMP AL,0
JE CMDTEXTEND
MOV DL,AL
MOV AH,2
INT 21H
JMP CMDTEXT
CMDTEXTEND:
RET
'''
MATCH='''CMDMATCH:
LODSB
MOV BX,DI
MOV AH,[BX]
CMP AL,AH
JNE CMDNO
INC DI
CMP AL,0
JNE CMDMATCH
MOV AX,1
RET
CMDNO:
MOV AX,0
RET
'''

def native(code,fields,output='RESNAME',report=True):
 """Install the same startup parser in native assembler/translator sources."""
 code=dict(code);fields=dict(fields)
 code['CMDINIT']=PARSER
 code['CMDMATCH']=MATCH
 for part in re.split(r'(?m)(?=^CMD\w+:)',DATA):
  if part.strip():fields[part.split(':',1)[0]]=part
 for name in ['SRCNAME','RESNAME']:
  # Maximum 8.3 plus NUL, including when the default spelling is shorter.
  if name in fields:
   values=[int(x) for row in fields[name].splitlines()[1:] for x in row[3:].split(',')]
   fields[name]=name+':\nDB '+','.join(map(str,values+[0]*(13-len(values))))+'\n'
 setup='''CMDFILES:
CALL CMDINIT
CMP AX,0
JE CMDREADY
CMP AX,2
JNE CMDFAIL
MOV SI,CMDBUF
MOV DI,SRCNAME
CALL COPYZ
MOV SI,CMDBUF
ADD SI,13
MOV DI,RESNAME
CALL COPYZ
'''
 for left,right in [('SRCNAME','RESNAME'),('SRCNAME','TMPNAME'),('SRCNAME','BAKNAME'),('RESNAME','TMPNAME'),('RESNAME','BAKNAME')]:
  setup+=f'MOV SI,{left}\nMOV DI,{right}\nCALL CMDMATCH\nCMP AX,0\nJNE CMDFAIL\n'
 setup+='CMDREADY:\nRET\nCMDFAIL:\nMOV AX,9\nJMP ERROR\n'
 code['CMDFILES']=setup
 # Startup runs before any file, memory, or other DOS service.
 start=code['START']
 if 'ROOM:\n' in start:start=start.replace('ROOM:\n','ROOM:\nCALL CMDFILES\n',1)
 else:
  assert 'JNE NEAR MEMORYBAD\n' in start
  start=start.replace('JNE NEAR MEMORYBAD\n','JNE NEAR MEMORYBAD\nCALL CMDFILES\n',1)
 code['START']=start
 if report:
  code['CMDTEXT']=TEXT
  for key in code:
   code[key]=code[key].replace('MOV DX,OKMSG\nCALL TEXT\n',f'MOV DX,OKMSG\nCALL TEXT\nMOV SI,{output}\nCALL CMDTEXT\nMOV DL,32\nMOV AH,2\nINT 21H\n')
  fields['OKMSG']='OKMSG:\nDB 79,75,32,36\n'
 return code,fields

def runtime():
 return PARSER+'''R_ARGC:
MOV AX,[CMDCOUNT]
JMP R_OK
R_ARG:
CMP AX,1
JB R_ARGBAD
MOV BX,[CMDCOUNT]
CMP AX,BX
JA R_ARGBAD
MOV BX,CMDBUF
R_ARGNEXT:
DEC AX
JE R_ARGDONE
ADD BX,13
JMP R_ARGNEXT
R_ARGDONE:
MOV AX,BX
JMP R_OK
R_ARGBAD:
MOV AX,0
JMP R_ERROR
'''+DATA

CHECKER='''ECHO OFF
IF "%1"=="" GOTO USAGE
IF NOT EXIST %1.COM GOTO MISSING
%1 %2 %3 %4 %5 %6 %7 %8 %9
IF ERRORLEVEL 1 GOTO FAIL
ECHO.
ECHO PASS
GOTO END
:FAIL
ECHO.
ECHO FAIL
GOTO END
:MISSING
ECHO Missing program
GOTO END
:USAGE
ECHO Use CHECK name [filenames]
:END
'''

def checker(folder):
 (Path(folder)/'CHECK.BAT').write_bytes(CHECKER.replace('\n','\r\n').encode('ascii'))

def rill_helpers(count=2,tmp='RILL.TMP',bak='RILL.BAK'):
 """Authored portable filename selection; physical PSP access stays in ARG."""
 checks=[]
 for i in range(1,count+1):
  for j in range(i+1,count+1):checks.append(f'filesame(arg({i}),arg({j}))')
  for name in (tmp,bak):checks.append(f'filesame(arg({i}),"{name}")')
 return '''fn filearg(n,fallback){
    let mut count=argc();
    if count==0{return fallback;}
    if count!='''+str(count)+'''{exit(1);}
    if '''+'|'.join(checks)+'''{exit(1);}
    return arg(n);
}
fn filesame(a,b){
    let mut i=0;
    while load8(a+i)==load8(b+i){
        if load8(a+i)==0{return 1;}i=i+1;
    }
    return 0;
}
'''

IR_HELPERS='''PROC FILEARG 2 2
ARGC
JZ FILEDEFAULT
PUSH
LIT 2
CNE
JNZ FILEBADARGS
LIT 1
ARG
SETLOCAL 0
LIT 2
ARG
SETLOCAL 1
LOCAL 0
PUSH
LOCAL 1
PUSH
INVOKE FILESAME 2
JNZ FILEBADARGS
LOCAL 0
PUSH
LITS "RILL.TMP"
PUSH
INVOKE FILESAME 2
JNZ FILEBADARGS
LOCAL 0
PUSH
LITS "RILL.BAK"
PUSH
INVOKE FILESAME 2
JNZ FILEBADARGS
LOCAL 1
PUSH
LITS "RILL.TMP"
PUSH
INVOKE FILESAME 2
JNZ FILEBADARGS
LOCAL 1
PUSH
LITS "RILL.BAK"
PUSH
INVOKE FILESAME 2
JNZ FILEBADARGS
PARAM 0
ARG
RETURN
LABEL FILEDEFAULT
PARAM 1
RETURN
LABEL FILEBADARGS
LIT 1
EXIT
PROC FILESAME 2 1
LABEL FILECOMPARE
PARAM 0
FETCHB
SETLOCAL 0
LOCAL 0
PUSH
PARAM 1
FETCHB
CNE
JNZ FILENOSAME
LOCAL 0
JZ FILEISSAME
PARAM 0
PUSH
LIT 1
ADD
PUSH
PARAM 1
PUSH
LIT 1
ADD
PUSH
INVOKE FILESAME 2
RETURN
LABEL FILEISSAME
LIT 1
RETURN
LABEL FILENOSAME
LIT 0
RETURN
'''

def ir_filenames(s,fragment=False):
 s=s.replace('LITS "SOURCE.RIL"\nOPEN', 'LIT 1\nPUSH\nLITS "SOURCE.RIL"\nPUSH\nINVOKE FILEARG 2\nOPEN')
 s=re.sub(r'LITS "RESULT.IR"\n(?!PUSH\nINVOKE FILEARG 2\n)', 'LIT 2\nPUSH\nLITS "RESULT.IR"\nPUSH\nINVOKE FILEARG 2\n',s)
 if fragment:s=s.replace('LITS "RILL.TMP"\nCREATE','LIT 2\nPUSH\nLITS "RILL.TMP"\nPUSH\nINVOKE FILEARG 2\nCREATE')
 return s

def rill_filenames(s,src,dest):
 s=s.replace('"'+src+'"','filearg(1,"'+src+'")')
 s=s.replace('"'+dest+'"','filearg(2,"'+dest+'")')
 # Keep the natural report accurate when a caller selected another result.
 s=s.replace('"OK '+dest+' "','"OK ");print(filearg(2,"'+dest+'"));print(" "')
 return s

def tool_kind(name,group=''):
 name=name.upper()
 if name in {'ASM1','ASMA0','ASM86','ASM86A','ASMAKEEP','A0','A1','A2'} or re.fullmatch(r'A\d\d',name):return 'ASM'
 if name in {'IR86','IRKEEP','IWKEEP','IRWIDE','IRED','I0','I1','I2'} or re.fullmatch(r'(?:IR|IW)\d\d',name):return 'IR'
 if name in {'RILL','RILL0','RILLBOOT','RBOOT','RILLED','R0','R1','R2'} or re.fullmatch(r'(?:R|RB|RC)\d\d',name):return 'RIL'
 if name=='GEN1' and group in {'asma0','asm86a','asm1','asm86'}:return 'ASM'
 if name=='LINK86' or re.fullmatch(r'L\d\d',name):return 'OBJ'
 if name=='EDIT86' or re.fullmatch(r'E(?:1\d|20)',name):return 'TXT'
 return None

@lru_cache(None)
def file_checkpoint(name):
 m=re.fullmatch(r'(R|RB|RC)(\d\d)',name.upper())
 if not m:return True
 family={'R':'rill-initial-series','RB':'rill-seed-series','RC':'rill-self-series'}[m[1]]
 case=next(c for c in json.loads((ROOT/'qa/toolchain'/(family+'.json')).read_text()) if c['number']==int(m[2]))
 return case.get('fixture') is not None or case.get('fragment') is not None or case['key'].upper()=='MAIN'

def command_text(text,group='',batch=False):
 """Use named PSP inputs in DOS examples; leave implementation listings intact."""
 sources={'ASM':'SOURCE.ASM','IR':'SOURCE.IR','RIL':'SOURCE.RIL','OBJ':'MAIN.OBJ','UTIL':'UTIL.OBJ','TXT':'EDIT.TXT'}
 outputs={'ASM':'RESULT.COM','IR':'RESULT.ASM','RIL':'RESULT.IR'}
 in_dos=batch;lines=text.splitlines(keepends=True);out=[]
 for i,line in enumerate(lines):
  plain=line.rstrip('\r\n');end=line[len(plain):]
  if not batch and plain.startswith('```'):
   in_dos=plain=='```dos';out.append(line);continue
  if not in_dos:out.append(line);continue
  m=re.fullmatch(r'COPY (\S+) (SOURCE\.(ASM|IR|RIL)|MAIN\.OBJ|UTIL\.OBJ|EDIT\.TXT)(?: >NUL)?',plain,re.I)
  if m:
   key=m[3].upper() if m[3] else {'MAIN.OBJ':'OBJ','UTIL.OBJ':'UTIL','EDIT.TXT':'TXT'}[m[2].upper()]
   sources[key]=m[1]
   # ASM0's bootstrap input stays fixed. Its COPY is still needed.
   following=''.join(lines[i+1:i+8])
   if key=='ASM' and re.search(r'(?:CHECK ASMKEEP|GWBASIC)',following,re.I):out.append(line)
   continue
  m=re.fullmatch(r'(CHECK )?([A-Z][A-Z0-9]*)(\s*)',plain,re.I)
  if m and file_checkpoint(m[2]) and (kind:=tool_kind(m[2],group)):
   if kind in outputs:
    plain=plain.rstrip()+' '+sources[kind]+' '+outputs[kind]
    if m[2].upper()=='IRED':plain+=' EDITRT.ASM'
   elif kind=='OBJ':plain=plain.rstrip()+' '+sources['OBJ']+' '+sources['UTIL']+' RESULT.COM'
   else:plain=plain.rstrip()+' '+sources['TXT']
  for ext in ('ASM','IR','RIL'):
   if plain.upper().startswith('REN SOURCE.'+ext+' '):plain=plain.replace('SOURCE.'+ext,sources[ext])
   if plain.upper().startswith('REN HOLD.') and plain.upper().endswith(' SOURCE.'+ext):plain=plain[:-len('SOURCE.'+ext)]+sources[ext]
  if plain.upper().startswith(('FC /B ',FC_BINARY.upper()+' ','TYPE ','COPY ')) and 'EDIT.TXT' in plain:
   plain=plain.replace('EDIT.TXT',sources['TXT'])
   words=plain.split()
   if len(words)==3 and words[0].upper()=='COPY' and words[1].upper()==words[2].upper():continue
  out.append(plain+end)
 return re.sub(r'```dos\n\s*```\n*','', ''.join(out)) if not batch else ''.join(out)

def publication(group,text,path=None):
 if group in {'bootasm','asm86'}:return text  # metadata key asm86 is ASM0
 # Early construction probes deliberately precede the completed PSP interface.
 # Their examples already spell out the interface of that precise checkpoint.
 if 'command_examples = "literal"' in text.split('+++',2)[1]:return text
 if path is not None and (path.stem in {'00-workbench','000-workbench'} or path.stem.endswith('reference')) and '## Command-line filenames' not in text:
  tool={'asma0':'ASM1','asm86a':'ASM86','ir86':'IR86','rill':'RILL0','rb':'RILLBOOT','rc':'RILL','toolchain':'RILL','link86':'LINK86','edit86':'EDIT86'}[group]
  if group=='link86':usage='CHECK LINK86 FIRST.OBJ SECOND.OBJ OUTPUT.COM';defaults='MAIN.OBJ, UTIL.OBJ and RESULT.COM';reserved='LINK.TMP and LINK.BAK'
  elif group=='edit86':usage='CHECK EDIT86 INPUT.RIL';defaults='EDIT.TXT';reserved='EDIT.TMP and EDIT.BAK'
  else:
   kind='ASM' if group in {'asma0','asm86a'} else 'IR' if group=='ir86' else 'RIL'
   dest={'ASM':'COM','IR':'ASM','RIL':'IR'}[kind]
   usage=f'CHECK {tool} INPUT.{kind} OUTPUT.{dest}'
   defaults=f'SOURCE.{kind} and RESULT.{dest}'
   reserved='ASMA.TMP and RESULT.BAK' if kind=='ASM' else 'IRTX.TMP and IRRES.BAK' if kind=='IR' else 'RILL.TMP and RILL.BAK'
  section='## Command-line filenames\n\n```dos\n'+usage+'\n```\n\n'
  section+='DOS supplies the names in the PSP command tail. The native entry binding copies them into owned zero-terminated storage before file services. '
  if group not in {'asma0','asm86a'}:section+='The language-level interface supplies argument counts and ordinary string pointers through portable services. '
  section+='CHECK.BAT forwards the arguments and reports status immediately. No arguments select '+defaults+'. Use unquoted 8.3 disk names in the current directory: letters, digits, underscore and hyphen, with an optional extension. Paths, switches, excess arguments and overlong names are rejected. Keep selected files distinct from each other and from '+reserved+'. Those temporary/backup names remain reserved.\n\n'
  if group=='edit86':section+='The selected document is opened and saved under the same name. Keep a separately named accepted source while editing; the status row shows the selected name.\n\n'
  else:section+='Success reports the selected result name. Rejected source preserves that accepted result; recovery rules apply to the selected name. Early diagnostic writers may deliberately retain a temporary file for inspection, as stated in their lesson.\n\n'
  head,body=text.split('+++',2)[1:]
  opening,separator,rest=body.strip().partition('\n\n')
  text='+++'+head+'+++\n\n'+opening+'\n\n'+section+rest+'\n'
 return command_text(text,group)

def package(folder):
 folder=Path(folder);checker(folder)
 p=folder/'README.TXT'
 if p.exists():
  text=p.read_text()
  text=text.replace('uses fixed','defaults to').replace('Use fixed SOURCE.','Default work names are SOURCE.')
  text=re.sub(r'(?m)^VIEW\.BAS and CHECK\.BAT[^\n]*','VIEW.BAS inspects bytes; CHECK.BAT forwards filename arguments.',text)
  text+='\nCOMMAND-LINE FILENAMES\n'
  text+='From ASM1 onward, supply input and output filenames on the command\nline: CHECK tool INPUT.EXT OUTPUT.EXT. No arguments select the\ndefault work names. Use unquoted 8.3 filenames in the current directory;\npaths and switches are not accepted. Input, output, temporary and backup\nnames must be distinct. LINK86 takes two object names then the result;\nEDIT86 takes one document name and saves that same document.\n'
  text=binary_comparisons(text)
  p.write_bytes(text.replace('\n','\r\n').encode('ascii'))
