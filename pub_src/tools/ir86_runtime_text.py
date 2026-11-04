"""Select authored assembly-text fragments for the DOS runtime profile."""
from pathlib import Path
import re
SOURCE=Path(__file__).with_name('ir86_runtime.asm').read_text()
pieces=re.split(r'^; @part (\w+)\n',SOURCE,flags=re.M)
PARTS={pieces[i]:pieces[i+1].strip()+'\n' for i in range(1,len(pieces),2)}
def part_names(level):
 names=[]
 if level>=24:names+=['RESULT','PUTC']
 if level>=25:names+=['GETC']
 if level>=26:names+=['OPEN']
 if level>=27:names+=['CREATE']
 if level>=26:names+=['FILE']
 if level>=28:names+=['FIND','READ']
 if level>=29:names+=['WRITE']
 if level>=30:names+=['CLOSE']
 if level>=23:names+=['STATUS']
 if level>=24:names+=['BYTE']
 if level>=26:names+=['FILEDATA']
 if level>=28:names+=['TRANSFERDATA']
 return names
def runtime(level):
 return '\n'.join(PARTS[n] for n in part_names(level))
