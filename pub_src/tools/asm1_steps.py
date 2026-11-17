"""Arrange the small, separately explained steps that lead to A01.ASM.

Only the published ASM0 assembler encodes the resulting assembly sources.
"""
from pathlib import Path
import json,re
from build_asm86a_series import seed_stage
from build_asm86a import BASE,dos

ROOT=Path(__file__).resolve().parents[1]
W=ROOT/'workbench/asm1'
Q=ROOT/'qa/asm1'
ROW='DB 88,79,82,0,0,0,4,6\n'
REPORT='MOV SI,RESNAME\nCALL CMDTEXT\nMOV DL,32\nMOV AH,2\nINT 21H\n'
STEPS=[
 dict(id='A01A',page='01a-reaching-error-handlers.md',title='Giving Conditional Branches Room',description='Use explicit short skips and near jumps before the routines grow.',
      fixture='JNE SKIP\nJMP DEST\nSKIP:\nDB 0\nDEST:\nRET\n',expected='7503E9010000C3',mode='fixed'),
 dict(id='A01B',page='01b-storing-file-names.md',title='Making Room for File Names',description='Give each selected filename its own terminated buffer and explain the data layout.',
      fixture='DB 1,2,3,4\n',expected='01020304',mode='fixed'),
 dict(id='A01C',page='01c-reading-the-command-tail.md',title='Reading Names from the PSP',description='Read a bounded tail, validate 8.3 spellings and keep independent copies.',mode='probe'),
 dict(id='A01D',page='01d-selecting-the-work-files.md',title='Selecting the Source and Result',description='Connect the saved names to file services and reject collisions before opening files.',
      fixture='DW 1234H\n',expected='3412',mode='selected',result='CHOSEN.COM'),
 dict(id='A01E',page='01e-reporting-the-result-name.md',title='Naming the Result in the Report',description='Print the selected result through a small zero-terminated string routine.',
      fixture='DB 65,0,26,255\n',expected='41001AFF',mode='selected',result='REPORT.COM'),
 dict(id='A01F',page='01f-remembering-an-open-input.md',title='Remembering an Open Input File',description='Distinguish a live input handle from a closed handle for the coming cleanup routine.',
      fixture='RET\n',expected='C3',mode='selected',result='CLOSED.COM'),
]

def remove(source,old):
 assert source.count(old)==1,(old,source.count(old))
 return source.replace(old,'',1)

def routine(source,first,last):
 return source[source.index(first+':\n'):source.index(last+':\n')]

def sources():
 # Work backward from the established endpoint. Each subtraction removes one
 # authored feature, keeping all later assembler executables byte-identical.
 final=seed_stage(1)
 f=remove(final,ROW).replace('MOV CX,26\nMOV AX,8\nCALL LOOK','MOV CX,25\nMOV AX,8\nCALL LOOK',1)
 e=remove(remove(remove(f,'MOV AL,1\nMOV [INOPEN],AL\n'),'MOV AL,0\nMOV [INOPEN],AL\n'),'INOPEN:\nDB 0\n\n')
 d=remove(e,REPORT)
 d=remove(d,routine(d,'CMDTEXT','OKMSG'))
 b=remove(d,routine(d,'CMDINIT','OKMSG'))
 b=remove(b,'CALL CMDFILES\n')
 command_data=b[b.index('CMDCOUNT:\n'):]
 b=remove(b,command_data)
 for field in ['TMPNAME','BAKNAME']:
  b=re.sub(r'(?m)^'+field+r':\nDB [^\n]*\n\n','',b,count=1)
 c=b.replace('OKMSG:\n',routine(f,'CMDINIT','CMDMATCH')+'OKMSG:\n',1)+command_data
 probe='''CMDPROBE:
MOV AX,0
MOV [LINENO],AX
CALL CMDINIT
CMP AX,2
JE PROBEOK
MOV AX,9
JMP ERROR
PROBEOK:
MOV AX,4C00H
INT 21H

'''
 c=c.replace('ROOM:\n','ROOM:\nCALL CMDPROBE\n',1)
 c=c.replace('CMDINIT:\n',probe+'CMDINIT:\n',1)
 # Restore the old filename declarations and OUTPTR location for the branch
 # step. The following storage step alone performs those data-layout edits.
 a=b
 for field in ['SRCNAME','RESNAME','OUTPTR']:
  a=re.sub(r'(?m)^'+field+r':\n(?:DB|DW) [^\n]*\n\n?','',a,count=1)
 a=a.replace('MOV DX,SRCNAME\n','MOV DX,FNAME\n',1)
 original_names=routine(BASE,'FNAME','HANDLE')
 a=a.replace('HANDLE:\n',original_names+'HANDLE:\n',1)
 a=a.replace('PC:\nDW 256\n','PC:\nDW 256\n\nOUTPTR:\nDW 24576\n',1)
 return dict(zip([s['id'] for s in STEPS],[a,b,c,d,e,f]))

def prepare():
 W.mkdir(exist_ok=True);Q.mkdir(exist_ok=True)
 manuscripts=sources()
 for step in STEPS:
  name=step['id'];dos(W/(name+'.ASM'),manuscripts[name])
  if 'fixture' in step:dos(W/('T'+name[1:]+'.ASM'),step['fixture'])
 print('Prepared six focused ASM1 sources; the A01 endpoint is retained')

if __name__=='__main__':prepare()
