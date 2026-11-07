"""Arrange shared, authored IR routines for the two required compiler milestones.

These are source selections, not a parser, translator, or executable encoder.
"""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
TEXT=(ROOT/'tools/rill_bootstrap.ir').read_text()
DATA=re.findall(r'^(?:WORD|BYTE|BUFFER) .*$',TEXT,re.M)
ALIAS=TEXT[TEXT.index('LABEL IOFAIL\n'):TEXT.index('PROC ERROR')]
clean=re.sub(r'^(?:WORD|BYTE|BUFFER) .*\n','',TEXT,flags=re.M).replace(ALIAS,'')
PROCS={r.split()[0]:'PROC '+r for r in re.split(r'^PROC ',clean,flags=re.M)[1:]}

def drop_case(s,token,target,prefix='LD TOK'):
 s=s.replace(f'{prefix}\nPUSH\nLIT {token}\nCEQ\nJNZ {target}\n','')
 return s

def remove_region(s,start,end):
 a=s.index('LABEL '+start+'\n');b=s.index('LABEL '+end+'\n',a)
 return s[:a]+s[b:]

def builtin(s,allowed):
 # The intrinsic table is authored source text, not a binary image.
 pattern=r'LITS "(PUTC\\01\\0.*?)"\n'
 m=re.search(pattern,s)
 entries=m[1].split(r'\0')
 kept=[]
 for i in range(0,len(entries)-2,3):
  name,arity,body=entries[i:i+3]
  if name.lower() in allowed:kept.extend([name,arity,body])
 return s[:m.start()]+ 'LITS "'+r'\0'.join(kept)+r'\0\0'+ '"\n'+s[m.end():]

SEED_INTRINSICS={'putc','status','open','create','close','read','write','exists','delete','rename','alloc','free','get8','get16','set8','set16','load8','exit'}

def profile(level=0):
 """0: RILL0; 1..11: the successive language and service additions."""
 p=dict(PROCS)
 # The seed only implements syntax required to compile the RILL compiler.
 for token,target in [(94,'PRECTWO'),(260,'PRECFIVE')]:p['PREC']=drop_case(p['PREC'],token,target)
 p['PREC']=remove_region(p['PREC'],'PRECTWO','PRECTHREE')
 for token,target in [(94,'BINXOR'),(260,'BINSHL')]:p['BINARY']=drop_case(p['BINARY'],token,target,'LOCAL 0')
 p['BINARY']=remove_region(p['BINARY'],'BINXOR','BINAND')
 p['BINARY']=remove_region(p['BINARY'],'BINSHL','BINSHR')
 for token,target in [(45,'PRIMARYNEG'),(126,'PRIMARYNOT'),(38,'PRIMARYADDR')]:p['PRIMARY']=drop_case(p['PRIMARY'],token,target)
 p['PRIMARY']=remove_region(p['PRIMARY'],'PRIMARYNEG','PRIMARYBOOL')
 p['PRIMARY']=remove_region(p['PRIMARY'],'PRIMARYADDR','PRIMARYDONE')
 allowed={'putc','status','exit'}
 if level>=8:allowed|={'open','create','close','read','write'}
 if level>=9:allowed|={'exists','delete','rename'}
 if level>=10:allowed|={'alloc','free'}
 if level>=11:allowed|={'get8','get16','set8','set16'}
 if level>=3:allowed=allowed|{'load8'}
 p['BUILTIN']=builtin(p['BUILTIN'],allowed)
 if level<2:
  for token,target in [(124,'PRECONE'),(38,'PRECTHREE'),(261,'PRECFIVE')]:p['PREC']=drop_case(p['PREC'],token,target)
  for token,target in [(124,'BINOR'),(38,'BINAND'),(261,'BINSHR')]:p['BINARY']=drop_case(p['BINARY'],token,target,'LOCAL 0')
  for start,end in [('BINOR','BINEQ')]:p['BINARY']=remove_region(p['BINARY'],start,end)
  p['PRIMARY']=drop_case(p['PRIMARY'],33,'PRIMARYBOOL')
  p['PRIMARY']=remove_region(p['PRIMARY'],'PRIMARYBOOL','PRIMARYDONE')
 if level<1:
  for token,target in [(42,'PRECSEVEN'),(47,'PRECSEVEN'),(37,'PRECSEVEN')]:p['PREC']=drop_case(p['PREC'],token,target)
  for token,target in [(42,'BINMUL'),(47,'BINDIV'),(37,'BINMOD')]:p['BINARY']=drop_case(p['BINARY'],token,target,'LOCAL 0')
  p['BINARY']=remove_region(p['BINARY'],'BINMUL','BINEQ')
 if level<3:
  p['PRIMARY']=drop_case(p['PRIMARY'],3,'PRIMARYSTRING')
  p['PRIMARY']=remove_region(p['PRIMARY'],'PRIMARYSTRING','PRIMARYPAREN')
  p['LEX']=remove_region(p['LEX'],'LEXSTRING','LEXEOF').replace('LABEL LEXEOF\n','LABEL LEXSTRING\nJMP SYNTAX\nLABEL LEXEOF\n')
 if level==6:
  p['FUNCTION']=remove_region(p['FUNCTION'],'PARAMLOOP','PARAMDONE')
 if level in [4,5]:p['NEWGLOBAL']=p['NEWGLOBAL'].replace('LIT 512\n','LIT 511\n')
 if level<6:
  # Ordinary names resolve to an existing local or global; no implicit procedure.
  s=p['RESOLVEOPTIONAL'];a=s.index('LIT 65535\nST RECVAL\n',s.index('LABEL RESOLVEUSER'))
  b=s.index('LABEL RESOLVEGOT\n',a);p['RESOLVEOPTIONAL']=s[:a]+'JMP NAMEFAIL\n'+s[b:]
  s=p['CALLARGS'];a=s.index('LABEL ARGUSER\n');p['CALLARGS']=s[:a]+'LABEL ARGUSER\nJMP NAMEFAIL\n'
  for name in ['PRIMARY','STATEMENT']:
   s=p[name]
   if name=='PRIMARY':
    s=drop_case(s,6,'PRIMARYPARAM','LOCAL 1');s=remove_region(s,'PRIMARYPARAM','PRIMARYBUFFER')
   else:
    s=drop_case(s,6,'STPARAM','LOCAL 1');s=remove_region(s,'STPARAM','STINDEX')
   p[name]=s
  if level<5:
   p['PRIMARY']=drop_case(p['PRIMARY'],2,'PRIMARYBUFFER','LOCAL 1')
   p['PRIMARY']=remove_region(p['PRIMARY'],'PRIMARYBUFFER','PRIMARYCALL')
   p['STATEMENT']=drop_case(p['STATEMENT'],91,'STINDEX')
   p['STATEMENT']=remove_region(p['STATEMENT'],'STINDEX','STASSIGN')
   p['STATEMENT']=drop_case(p['STATEMENT'],2,'STPUTBYTE','LOCAL 1')
   p['STATEMENT']=remove_region(p['STATEMENT'],'STPUTBYTE','STFINISH')
  if level<4:
   p['PRIMARY']=drop_case(p['PRIMARY'],1,'PRIMARYGLOBAL','LOCAL 1')
   p['PRIMARY']=remove_region(p['PRIMARY'],'PRIMARYGLOBAL','PRIMARYLOCAL')
   p['STATEMENT']=drop_case(p['STATEMENT'],1,'STGLOBAL','LOCAL 1')
   p['STATEMENT']=remove_region(p['STATEMENT'],'STGLOBAL','STLOCAL')
   for name in ['RESOLVEOPTIONAL','RESOLVE']:
    s=p[name]
    a=s.index('CALL LOOKGLOBAL\n');b=s.index('LABEL RESOLVEGOT\n' if name=='RESOLVEOPTIONAL' else 'LABEL RESOLVED\n',a)
    p[name]=s[:a]+'JMP NAMEFAIL\n'+s[b:]
  # Keep the complete compiler running while each capability is added.
  s=p['MAIN'];a=s.index('LABEL TOP\n');b=s.index('LD INPUT\nCLOSE\n',a)
  header='LITS "FN"\nCALL ISWORD\nJZ SYNTAX\nCALL LEX\nLITS "MAIN"\nCALL ISWORD\nJZ SYNTAX\nCALL LEX\nLIT 40\nPUSH\nINVOKE EXPECT 1\nLIT 41\nPUSH\nINVOKE EXPECT 1\nLITS "PROC MAIN 0 16\\r\\n"\nCALL OUTSTR\nCALL BLOCK\nLD TOK\nJNZ SYNTAX\nLITS "LIT 0\\r\\nRETURN\\r\\n"\nCALL OUTSTR\n'
  top=''
  if level>=4:
   top+='LABEL TOP\nLITS "LET"\nCALL ISWORD\nJZ TOPBUFFER\nCALL GLOBALWORD\nJMP TOP\nLABEL TOPBUFFER\n'
   if level>=5:top+='LITS "BYTES"\nCALL ISWORD\nJZ TOPMAIN\nCALL GLOBALBUFFER\nJMP TOP\nLABEL TOPMAIN\n'
  p['MAIN']=s[:a]+top+header+s[b:]
 return p

def main_record_profile():
 """Keep the one-main language while making main an ordinary procedure record."""
 p=profile(5)
 p['NEWGLOBAL']=PROCS['NEWGLOBAL']
 p['FUNCTION']=profile(6)['FUNCTION'].replace('CALL LEX\n','',1)
 s=p['MAIN'];a=s.index('CALL LEX\nLITS "MAIN"');b=s.index('LD INPUT\nCLOSE\n',a)
 s=s[:a]+'CALL LEX\nLITS "MAIN"\nCALL ISWORD\nJZ SYNTAX\nCALL FUNCTION\nLD TOK\nJNZ SYNTAX\nLITS "PROC MAIN 0 0\\r\\nINVOKE F_MAIN 0\\r\\nRETURN\\r\\n"\nCALL OUTSTR\n'+s[b:]
 p['MAIN']=s
 return p

def render(procs,roots=('MAIN',),extra=()):
 """Retain only routines and fields referenced by this working stage."""
 p=dict(procs);used=set(roots)|set(extra)
 owners={n:k for k,v in p.items() for n in re.findall(r'^(?:LABEL|PROC) (\w+)',v,re.M)}
 # Error aliases are entries into ERROR, not independent routines.
 owners.update({n:'ERROR' for n in re.findall(r'^LABEL (\w+)',ALIAS,re.M)})
 while True:
  joined='\n'.join(p[k] for k in used)+(ALIAS if 'ERROR' in used else '')
  refs=set(re.findall(r'^(?:CALL|INVOKE|JMP|JZ|JNZ) (\w+)',joined,re.M))
  missing=refs-set(owners)
  if missing:raise ValueError(('undefined routine',missing))
  needed={owners[n] for n in refs}
  if needed<=used:break
  used|=needed
 code='\n'.join((ALIAS if k=='ERROR' else '')+p[k] for k in PROCS if k in used)
 refs=set(re.findall(r'\b[A-Z][A-Z0-9_]*\b',code))
 data='\n'.join(line for line in DATA if line.split()[1] in refs)
 return '; RILL compiler construction. Portable IR source.\n'+data+'\n'+code
