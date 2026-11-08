"""Publish current tool names and retain established source filenames and URLs."""
from pathlib import Path
import json,re,tomllib
from project_paths import directory_name,collection_key
ROOT=Path(__file__).resolve().parents[1];CONTENT=ROOT/'site/content/bootstrap'
SERIES={
 'bootasm':('BOOTASM','Our First Assembler'),
 'asm86':('ASM0','An Assembler That Builds Itself'),
 'asma0':('ASM1','Building a Streaming Assembler'),
 'asm86a':('ASM86','Extending the 8086 Assembler'),
 'ir86':('IR86','Building an Intermediate Language'),
 'rill':('RILL0','Our First Compiler'),
 'rb':('RILLBOOT','A Compiler for Writing Tools'),
 'rc':('RILL','A Compiler Written in Its Own Language'),
 'toolchain':('TOOLCHAIN','Rebuilding Our Tools in RILL'),
 'link86':('LINK86','Linking Our First Modules'),
 'edit86':('EDIT86','Building Our Screen Editor')}
WORDS={'ASM86':'ASM0','ASMA0':'ASM1','ASM86A':'ASM86','RB':'RILLBOOT','RC':'RILL'}
TOKEN=re.compile(r'\b(?:RILL\.(?:IR|ASM|COM|ZIP)|ASM86A|ASMA0|ASM86|RB|RC)\b')
def names(s):return TOKEN.sub(lambda m:'RILL0'+m[0][4:] if m[0].startswith('RILL.') else WORDS[m[0]],s)
def filename(name):
 stem,sep,ext=name.partition('.')
 if stem=='RILL' and ext in ['IR','ASM','COM','ZIP']:stem='RILL0'
 else:stem=WORDS.get(stem,stem)
 return stem+sep+ext
def reader_text(group,original,text):
 """Give each canonical archive instructions for its current collection."""
 if group=='edit86':return text
 newline='\r\n' if '\r\n' in text else '\n'
 text=names(text.replace('\r\n','\n'))
 if original=='README.TXT':
  text=text.replace('first RILL -> RILLBOOT','RILL0 -> RILLBOOT')
  if group=='rc':
   text=text.replace('IR86.RIL and ASM86.RIL are the translator and assembler in RILL.\nTMAKE.BAT builds all three tools and both closed-loop generations.\nThe complete TOOLCHN.ZIP also contains earlier continuation sources.',
    'After both compiler self-builds match, continue with Rebuilding Our\nTools in RILL. Its TOOLCHN.ZIP supplies IR86.RIL, ASM86.RIL, and\nTMAKE.BAT for the complete three-tool builds and comparisons.')
 return text.replace('\n',newline)

HELP_TITLES={
 'PRINT':'Printing a String','PRINTNUM':'Printing a Number','PRINT32':'Counting Beyond 65535',
 'ERROR':'Reporting an Error','FAIL':'Reporting an Error','LETTER':'Recognizing Identifier Characters','DIGIT':'Recognizing Decimal Digits',
 'NEXT':'Reading a File in Blocks','EXPECT':'Consuming the Required Token','ISWORD':'Recognizing a Complete Keyword','SETIDENT':'Copying a Name',
 'TWORD':'Reading a Word from Allocated Storage','TBYTE':'Reading a Byte from Allocated Storage','WRITEFIELD':'Writing a Symbol Field','RECORDFIELDS':'Storing a Symbol\'s Meaning',
 'RECORD':'Recording a Name and Its Meaning','NEWGLOBAL':'Adding a Global Name','NEWLOCAL':'Adding a Local Name','FIND':'Finding a Name in the Table','LOOKGLOBAL':'Finding a Global Name','RESOLVE':'Finding the Visible Binding',
 'FLUSH':'Writing a Buffered Block','OUTCHAR':'Adding a Byte to the Output','OUTSTR':'Writing Text Through the Buffer','OUTNUM':'Writing a Numeric Operand','NEWLINE':'Ending a Line of Generated Code',
 'NEWLABEL':'Giving Each Branch a Unique Name','LABELDEF':'Defining a Branch Destination','LABELJUMP':'Naming a Branch Destination','OUTNAME':'Writing a Stored Name',
 'BUILTIN':'Recognizing Built-in Services','RESOLVEOPTIONAL':'Remembering Calls Before Their Definitions','PREC':'Making Multiplication Come First','BINARY':'Translating an Arithmetic Operation','EXPR':'Translating an Expression',
 'CALLARGS':'Keeping Values Across a Procedure Call','GLOBALWORD':'Compiling a Global Variable','GLOBALBUFFER':'Compiling a Byte Buffer','DECLARE':'Initializing a Local Variable','BLOCK':'Remembering Which Names Are Visible',
 'STATEMENT':'Compiling Assignments and Branches','FUNCTION':'Compiling a Procedure','MAIN':'Compiling a Complete Program'}
TITLES={
 'asma0/02-reading-an-input-block.md':'Reading a File in Blocks',
 'asma0/03-writing-an-output-block.md':'Copying a File in Small Blocks',
 'asm86a/13-allocating-auxiliary-workspace.md':'Getting More Memory from DOS',
 'asm86a/21-small-value-expressions.md':'Calculating Addresses and Counts'}
for group,family in [('rb','rill-seed-series'),('rc','rill-self-series')]:
 for case in json.loads((ROOT/'qa/toolchain'/(family+'.json')).read_text()):
  key=case['key'].upper();n=case['number'];offset=33 if group=='rb' else 88
  slug=re.sub('[^a-z0-9]+','-',case['title'].lower()).strip('-')
  title=HELP_TITLES.get(key,case['title'])
  if key=='LEX':title={'punctuation':'Reading Punctuation and Paired Operators','names':'Reading Names Without Losing Letters','numbers':'Reading Decimal Values','full':'Reading Quoted Text'}.get(case.get('variant'),'Reading Tokens')
  if key=='PRIMARY':title={'values':'Reading Parentheses, Strings, and Unary Values','full':'Reading Variables and Addresses'}.get(case.get('variant'),'Reading Values, Addresses, and Names')
  TITLES[f'{group}/{offset+n:03}-{group}-{slug}.md']=title

def prepare(path,text):
 """Rename prose/commands without changing any printed implementation or expected bytes."""
 path=Path(path);rel=path.relative_to(CONTENT);group=collection_key(rel.parts[0])
 if group not in SERIES:return text
 front,body=text.split('+++',2)[1:];meta=tomllib.loads(front)
 if meta.get('reader_names')==1:return text
 tool,title=SERIES[group]
 oldgroup=meta.get('download_group',group);oldsource=meta.get('checkpoint',meta.get('download'))
 # Source/data listings and observed program output remain byte-exact.
 chunks=re.split(r'(```.*?```)',body,flags=re.S)
 for i,chunk in enumerate(chunks):
  if not chunk.startswith('```'):chunks[i]=names(chunk)
  elif chunk.startswith('```dos\n') or (chunk.startswith('```text\n') and 'GW-BASIC' in chunk):chunks[i]=names(chunk)
 body=''.join(chunks)
 body=body.replace('IR86 → RILL → RILLBOOT → RILL','IR86 → RILL0 → RILLBOOT → RILL')
 body=re.sub(r'BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL(?=\*\*|[.\n])','BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL',body)
 body=re.sub(r'downloads/([a-z0-9]+)/',lambda m:'downloads/tools/'+('toolchain' if m[1]=='toolchain' else SERIES[m[1]][0].lower())+'/' if m[1] in SERIES or m[1]=='toolchain' else m[0],body)
 if group=='rill':
  body=re.sub(r'(?m)(CHECK )RILL(?=\s|$)',r'\1RILL0',body)
  body=re.sub(r'(enter |enter `)RILL(?=`|[., ])',r'\1RILL0',body)
 body=re.sub(r'Together they require \d+ BASIC lines; type and test them as two separate programs\.', 'Type and test them as two separate programs.',body)
 body=re.sub(r'(complete |separate )\d+-line (program|viewer)',r'\1\2',body)
 if path.name=='_index.md':newtitle=title
 else:
  heading=TITLES.get((Path(group)/Path(*rel.parts[1:])).as_posix())
  newtitle=(f'{meta.get("weight",0):02} · '+heading) if heading else names(meta['title'])
 front=re.sub(r'(?m)^title = .*$',lambda _: 'title = '+json.dumps(newtitle),front,count=1)
 if 'description' in meta:front=re.sub(r'(?m)^description = .*$',lambda _:'description = '+json.dumps(names(meta['description'])),front,count=1)
 if oldsource:
  key='checkpoint' if 'checkpoint' in meta else 'download'
  front=re.sub(r'(?m)^'+key+r' = .*$',lambda _:key+' = '+json.dumps(filename(oldsource)),front,count=1)
  publicgroup='toolchain' if oldgroup=='toolchain' else group
  canonical='toolchain' if publicgroup=='toolchain' else SERIES[publicgroup][0].lower()
  if 'download_group' in meta:front=re.sub(r'(?m)^download_group = .*$',f'download_group = "tools/{canonical}"',front,count=1)
  else:front+=f'download_group = "tools/{canonical}"\n'
 front+='reader_names = 1\n'
 if path.name=='_index.md':front+=f'tool_id = "{tool}"\ncollection_key = "{group}"\n'
 return '+++'+front+'+++'+body

def write_page(path,text):
 path=Path(path);text=prepare(path,text)
 group=collection_key(path.relative_to(CONTENT).parts[0])
 if directory_name(group)!=group:
  front,body=text.split('+++',2)[1:]
  url='/bootstrap/'+group+'/'+('' if path.name=='_index.md' else path.stem+'/')
  if re.search(r'(?m)^url = ',front):front=re.sub(r'(?m)^url = .*$',lambda _:'url = '+json.dumps(url),front)
  else:front+='url = '+json.dumps(url)+'\n'
  text='+++'+front+'+++'+body
 if path.name=='_index.md' and group in SERIES:
  from series_overviews import with_overview
  text=with_overview(group,text)
 path.write_text(text)

if __name__=='__main__':
 for p in CONTENT.rglob('*.md'):write_page(p,p.read_text())
 print('Applied reader names and article titles; preserved publication routes and source blocks')
