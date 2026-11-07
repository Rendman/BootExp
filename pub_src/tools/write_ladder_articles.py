"""Publish the continuing native translator and compiler constructions."""
from pathlib import Path
from difflib import SequenceMatcher
import json,re,tomllib
from publication_names import ROOT,SERIES,filename,HELP_TITLES
from compiler_profiles import profile,render
C=ROOT/'site/content/bootstrap';Q=ROOT/'qa/toolchain';W=ROOT/'workbench/toolchain'
def fence(k,s):return '```'+k+'\n'+s.replace('\r\n','\n').rstrip('\n')+'\n```\n\n'
def slug(s):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
def front(group,title,weight,description,download,aliases=(),cover=False):
 meta=dict(title=title,weight=weight,description=description,download=download,download_group='tools/'+SERIES[group][0].lower(),reader_names=1)
 if cover:meta.update(cover=True,tool_id=SERIES[group][0],collection_key=group)
 if aliases:meta['aliases']=list(aliases)
 return '+++\n'+''.join(k+' = '+json.dumps(v)+'\n' for k,v in meta.items())+'+++\n\n'
def edits(old,new,condense=False):
 changes=[];t=''
 if not old:return fence('ir','\n'.join(new)),[dict(a1=0,a2=0,old=[],new=new)]
 for tag,a,b,c,d in reversed(SequenceMatcher(None,old,new,autojunk=False).get_opcodes()):
  if tag=='equal':continue
  before=old[max(0,a-3):a];after=old[b:b+2]
  t+=f'### Edit at old physical position {a+1}\n\n'
  if before:t+='Unchanged source before the edit:\n\n'+fence('source','\n'.join(before))
  bounded=condense and b-a>30
  if a!=b:
   if bounded:t+=f'Remove the complete old physical range {a+1}–{b}. Its first source is:\n\n'+fence('source','\n'.join(old[a:a+3]))+'Its last source is:\n\n'+fence('source','\n'.join(old[b-3:b]))+'Remove both boundaries and all source between them.\n\n'
   else:t+='Remove:\n\n'+fence('source','\n'.join(old[a:b]))
  if c!=d:t+='Insert in its place:\n\n'+fence('source','\n'.join(new[c:d]))
  if after:t+='The following old source remains:\n\n'+fence('source','\n'.join(after))
  changes.append(dict(a1=a,a2=b,old=old[a:b],new=new[c:d],context=before,after=after,old_display='bounds' if bounded else 'full'))
 return t,changes

GUIDES={
 'ir86':('ASM86 builds every saved source in this collection. The translator always reads SOURCE.IR and writes RESULT.ASM. Preserve the completed translator as IRKEEP.COM; make the identical IWKEEP.COM copy used by later workbenches.','IR86.ASM','IR86.ZIP'),
 'rill':('Begin with the completed ASM86 and native IR86 workbenches. Every compiler checkpoint is written in IR86. Translate SOURCE.IR with IRKEEP, copy accepted RESULT.ASM to SOURCE.ASM, then assemble with ASMAKEEP. The finished RILL0 reads SOURCE.RIL and publishes RESULT.IR.','RILL0.IR','RILL0.ZIP'),
 'rb':('Begin with the completed RILL0. Copy RILL0.IR to RB01.IR and continue editing its working compiler. Use IRKEEP and ASMAKEEP for every build. Each saved compiler accepts the earlier language while gaining one capability.','RILLBOOT.IR','RILLBOOT.ZIP')}
EXPLAIN={
 'PRINT':'Walk zero-terminated text, preserving its pointer across a byte output call. This display routine remains part of the compiler diagnostics.',
 'PRINTNUM':'Keep the value and decimal place in separate local slots. Emit the decimal digits without borrowing a parser work cell.',
 'PRINT32':'Report a count as two words without requiring a wider machine value. Divide the pair by ten and display its saved digits.',
 'ERROR':'Close owned handles and free owned workspace before reporting the line and error category. Retain recovery files if restoring accepted output fails.',
 'NEXT':'Refill the input block only after consuming its valid bytes. A short positive read still contains data; zero is EOF. Keep checked source-line counts separately.',
 'LEX':'Keep the token kind, numeric value, and complete spelling separate. Fold identifiers while preserving source text. Reject decimal overflow before a word wraps.',
 'RECORD':'Initialize a forty-byte symbol record, copy its complete spelling, and write its kind, value, and lexical level explicitly.',
 'FIND':'Search complete spellings from the innermost live binding outward. Offset zero is valid; 65535 represents absence.',
 'RESOLVEOPTIONAL':'Recognize a builtin or an existing local binding. RILL0 rejects an unknown name.',
 'PREC':'Return a precedence for an accepted operator and zero for a nonoperator. RILL0 starts with addition, subtraction, and unsigned comparisons.',
 'PRIMARY':'Compile a numeric value, parenthesized expression, local binding, or accepted builtin call. Keep the binding metadata in local slots across nested parsing.',
 'EXPR':'Compile the left primary, save its value, and recurse at a higher minimum precedence for the right operand. Check recursion depth before nesting.',
 'STATEMENT':'Compile assignments, local declarations, if/else, and while with saved branch destinations. Every branch boundary has an empty expression stack.',
 'MAIN':'Open the fixed source and stream generated text through an owned temporary file. Publish it only after the full source, final flush, and both closes succeed.'}
patches=[]
for group,family,folder,prefix in [('ir86','ir-extensions',ROOT/'workbench/ir86','IR'),('rill','rill-initial-series',ROOT/'workbench/rill','R'),('rb','rill-seed-series',W,'RB')]:
 cases=json.loads((Q/(family+'.json')).read_text());dest=C/group
 # Preserve all prior routes as direct aliases to the corresponding working part.
 oldpages=[]
 for p in dest.glob('*.md'):
  if p.name=='_index.md':continue
  meta=tomllib.loads(p.read_text().split('+++')[1]);oldpages.append((p,meta))
 alias_for={n:[] for n in range(len(cases)+3)}
 for p,m in oldpages:
  if m.get('weight',0)==0:target=0
  elif 'reference' in p.stem or p.stem.endswith(('-contract','-systems-language')):target=len(cases)+1
  elif group=='ir86' and re.match(r'0?(3[7-9]|[45][0-9]|60)-iw',p.stem):target=min(len(cases),max(1,m.get('weight',37)-36))
  else:target=min(len(cases),max(1,m.get('weight',1)))
  for route in ['/bootstrap/'+group+'/'+p.stem+'/']+m.get('aliases',[]):
   stem=Path(route.strip('/')).name
   destination=len(cases)+1 if 'reference' in stem or stem.endswith(('-contract','-systems-language')) else 1 if stem=='01-a-program-in-the-intermediate-language' else target
   alias_for[destination].append(route)
  p.unlink()
 source,download,archive=GUIDES[group]
 cover=front(group,SERIES[group][1],list(SERIES).index(group)+1,source,download,cover=True)
 if group=='ir86':body='This collection builds one native translator from a bounded reader through procedure frames, strings, file streams, and allocated workspace. The first small translator grows into the translator that builds the compiler. ASM86 assembles every stage.\n\nThe language defines word values, a virtual accumulator, an expression stack, byte addresses, and opaque service handles. The 8086 instructions appear in the backend templates and DOS binding; they are not part of the IR program interface.'
 elif group=='rill':body='Build a small compiler in the processor-independent IR language. Its scanner, record layout, local bindings, streamed emitter, and parser are the working parts that RILLBOOT extends. The first language has one fn main(), mutable local words, + and -, unsigned comparisons, assignments, if/else, while, putc, status, exit, and return.'
 else:body='Continue the completed RILL0 source. Add word arithmetic, masks, strings, global storage, procedures, and the file and workspace services needed to compile the RILL compiler. Every continuation remains a working compiler for its preceding subset. The seed deliberately omits XOR, left shift, unary minus, bitwise complement, explicit address-of, and unused intrinsic wrappers; RILL adds the operations needed by the later tool sources.'
 (dest/'_index.md').write_text(cover+body+'\n\nRead the workbench first. The [source collection](../../downloads/tools/'+SERIES[group][0].lower()+'/'+archive+') contains plain source and test files.\n')
 work='000-workbench.md';routes=sorted(set(alias_for[0])-{'/bootstrap/'+group+'/000-workbench/'})
 text=front(group,'The '+SERIES[group][0]+' workbench',0,source,archive,routes)+source+'\n\nKeep VIEW.BAS and CHECK.BAT from the BOOTASM workbench. Work in an ordinary DOS hard-disk directory. Fixed names avoid adding a filename parser to each tool. Require a fresh OK and PASS before copying an output into the next stage.\n\n'
 if group=='ir86':text+=fence('dos','COPY IR01.ASM SOURCE.ASM\nCHECK ASMAKEEP\nCOPY RESULT.COM IR01.COM')
 else:text+=fence('dos','COPY '+cases[0]['source']+' SOURCE.IR\nCHECK IRKEEP\nCOPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP\nCOPY RESULT.COM '+prefix+'01.COM')
 text+='An early stopping point may produce a fragment rather than a complete program. Inspect its length and bytes with VIEW.BAS; execute it only when the article gives a complete program. Recovery names protect an interrupted publication: inspect them before trying again.\n'
 (dest/work).write_text(text)
 old=(ROOT/'workbench/asm86a/ASM86A.ASM').read_text().splitlines() if group=='ir86' else (ROOT/'workbench/rill/RILL.IR').read_text().splitlines() if group=='rb' else []
 oldname='ASM86.ASM' if group=='ir86' else 'RILL0.IR' if group=='rb' else None
 for c in cases:
  if group=='rill' and c['key'] not in ['LEX','PRIMARY','PREC','RESOLVEOPTIONAL','MAIN']:c['title']=HELP_TITLES.get(c['key'],c['title'])
  n=c['number'];name=f'{prefix}{n:02}';src=f'{name}.ASM' if group=='ir86' else c['source'];new=(folder/src).read_text().splitlines();page=f'{n:03}-{slug(c["title"])}.md'
  route='/bootstrap/'+group+'/'+Path(page).stem+'/'
  aliases=sorted(set(alias_for[n])-{route});description=c.get('why') or EXPLAIN.get(c.get('key'),'Build '+c['title'].lower()+'.').split('. ')[0]+'.'
  text=front(group,f'{n:02} · '+c['title'],n,description,src,aliases)
  explanation=description if group=='rb' else EXPLAIN.get(c.get('key'),description)
  if group=='rill' and c['key']=='LEX':explanation={'punctuation':'Skip whitespace and line comments, and recognize punctuation and paired operators. Identifier, number, and string paths still reject input in this checkpoint.', 'names':'Copy each complete identifier into IDENT, fold its letters to uppercase, and enforce the 24-character bound. Punctuation remains available; numeric and quoted tokens still reject input.', 'numbers':'Accumulate decimal VALUE only after checking that the next digit fits a word. TOK identifies a number; CH retains the first following character. Names and punctuation keep their earlier behavior; strings are still rejected.'}[c['variant']]
  if group=='rill' and c['key']=='PRIMARY':explanation='Compile numeric literals and parenthesized expressions through the existing EXPR routine. Name and call paths are still rejected.' if c['variant']=='values' else 'Resolve a local binding or builtin name and save its metadata before scanning further. Numeric and parenthesized primaries remain available. Argument parsing still reaches the rejecting CALLARGS stub in this checkpoint.'
  text+=explanation+'\n\n'
  if group=='rb':text+='Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.\n\n'
  text+='## Enter the source\n\n'
  if oldname:text+=f'Copy {oldname} to {src}. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.\n\n'
  else:text+='Create '+src+' as plain text:\n\n'
  edit,changes=edits(old,new,condense=group=='ir86' and n==1);text+=edit.replace('```source','```asm' if group=='ir86' else '```ir')
  text+='## Build and check\n\n'
  if group=='ir86':text+=fence('dos',f'COPY {src} SOURCE.ASM\nCHECK ASMAKEEP')
  else:text+=fence('dos',f'COPY {src} SOURCE.IR\nCHECK IRKEEP\nCOPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP')
  text+=f'Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM {c["binary_bytes"]:05} bytes`. Save RESULT.COM as {name}.COM. VIEW.BAS must show length {c["binary_bytes"]}.\n\n'
  if c.get('fixture') is not None:
   fixture=f'T{n:02}.IR' if group=='ir86' else f'T{n:02}.RIL' if group=='rill' else f'TRB{n:02}.RIL'
   text+='Create '+fixture+':\n\n'+fence('ir' if group=='ir86' and n>=5 else 'text' if group=='ir86' else 'rill',c['fixture'])
   text+=fence('dos',f'COPY {fixture} SOURCE.'+('IR' if group=='ir86' else 'RIL'))
  text+=fence('dos','CHECK '+name)
  output=c.get('output',c.get('console',''))
  if output:text+='Require:\n\n'+fence('text',output+('FAIL' if c.get('accept_exit') else 'PASS'))
  else:text+='Require '+('FAIL' if c.get('accept_exit') else 'PASS')+'.\n\n'
  if c.get('check_value') is not None:text+='The driver compares the result with '+str(c['check_value'])+' and returns nonzero on a mismatch; it adds no display routine.\n\n'
  if c.get('accept_exit'):text+='The error routine deliberately exits nonzero; its diagnostic and FAIL are the intended result.\n\n'
  if group=='ir86' and n==3:text+='Inspect RESULT.ASM with VIEW.BAS: length 5, bytes `41 42 43 0D 0A`. This copied data is not a program.\n\n'
  elif group=='ir86' and n>=5:
   text+=fence('dos','COPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP')+f'Require OK and PASS. VIEW.BAS must show RESULT.COM length {c["target_bytes"]} and these leading bytes:\n\n'+fence('text',c['target_hex'])
   text+='Copy it to TRY.COM. '
   if n in [13,15,17,21]:text+='First create A with `ECHO A>A`. '
   text+='CHECK TRY '+(f'displays `{c["program_output"]}` and ' if c['program_output'] else '')+('reports PASS.' if not c['program_exit'] else f'reports FAIL because the test returns {c["program_exit"]}.')+'\n\n'
  elif 'result' in c:
   result='RESULT.IR' if c['key']=='MAIN' else 'RILL.TMP';raw=c['result'].encode()
   text+=f'Inspect {result} with VIEW.BAS. Require length {len(raw)} bytes and '+('these complete bytes:\n\n'+fence('text','\n'.join(raw[i:i+16].hex(' ').upper() for i in range(0,len(raw),16))) if raw else 'an empty file.\n\n')
   if c['complete']:
    text+='This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. '
    
    for path,data in c.get('files',{}).items():text+='First create '+path+' with `ECHO '+data.rstrip('\r\n')+'>'+path+'`.\n\n'
    text+=f'VIEW.BAS must report length {c["program_bytes"]}. CHECK TRY '+(f'displays `{c["program_output"]}` and ' if c['program_output'] else '')+'reports PASS.\n\n'
    if c.get('result_file'):text+='Inspect '+c['result_file']+' with VIEW.BAS: require length '+str(len(c['result_data']))+' and bytes `'+c['result_data'].encode().hex(' ').upper()+'`.\n\n'
   else:text+='This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.\n\n'
  if group=='ir86' or c.get('code'):
   text+='## Check the new boundary\n\n'
   if c.get('bad') is not None:
    text+='Use this separate rejected source:\n\n'+fence('ir' if group=='ir86' else 'rill',c['bad'])+'Copy it to SOURCE.'+('IR' if group=='ir86' else 'RIL')+' and run CHECK '+name+'. '
   else:text+='Temporarily rename SOURCE.'+('IR' if group=='ir86' else 'RIL')+' to HOLD.TXT and run CHECK '+name+'. Restore the source afterward. '
   text+='Require:\n\n'+fence('text',c['error']+'FAIL')+'An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.\n\n'
  if n==len(cases):
   if group=='ir86':text+=fence('dos',f'COPY {name}.COM IRKEEP.COM\nCOPY IRKEEP.COM IWKEEP.COM')+'IR86.ASM and this final source are identical. Continue with [RILL0](../../rill/index.html).\n'
   elif group=='rill':text+=fence('dos',f'COPY {name}.COM RLKEEP.COM')+'RILL0.IR is this final source. Continue by editing it in [RILLBOOT](../../rb/index.html).\n'
   else:text+=fence('dos',f'COPY {name}.COM RILLBOOT.COM')+'RILLBOOT.IR is this final source. Continue with the [compiler written in RILL](../../rc/index.html).\n'
  (dest/page).write_text(text);patches.append(dict(family=family,number=n,collection=group,page=page,base=oldname,kind='asm' if group=='ir86' else 'ir',source=src,folder=str(folder.relative_to(ROOT)),changes=changes));old=new;oldname=src
 # Exact minimal contract, separate from the target implementation.
 aliases=sorted(set(alias_for[len(cases)+1]+alias_for[len(cases)+2]) - {'/bootstrap/'+group+'/900-language-reference/'})
 text=front(group,SERIES[group][0]+' language reference',900,'The accepted language and its bounded implementation.',download,aliases)
 if group=='ir86':
  from build_ir86_wide import OPS
  table='| Operation | Argument class | Stack action |\n|---|---:|---:|\n'
  for name,(cls,delta,_) in OPS.items():table+=f'| `{name}` | {cls} | {delta} |\n'
  text+=(ROOT/'tools/ir86_reference.md').read_text().replace('<!-- OPERATION_TABLE -->',table.rstrip())

 else:
  text+='Words range from 0 through 65535; arithmetic wraps and ordering is unsigned. Names begin with a letter or underscore, continue with letters, digits, or underscores, and are folded to uppercase with complete spelling, up to 24 characters. Source uses decimal word literals, ASCII text, // comments ending at LF or EOF, and brace-enclosed bodies. Use DOS CR/LF disk text. Local bindings use `let mut name=expression;`, assignment, lexical braces, `if`/`else`, `while`, and `return expression;`. Expressions have parentheses, +, -, and unsigned comparisons. Addition/subtraction bind more tightly than comparisons; each level associates left to right. Zero is false and any nonzero word is true. return; and normal fall-through return zero. Each expression and block has a checked nesting limit of sixteen. At most sixteen local word slots are live in a procedure.\n\n'
  if group=='rill':text+='There is exactly one argument-free `fn main(){...}`. Its builtin calls are putc(value), status(), and exit(value). No strings, globals, user procedures, multiply, divide, bit operators, or byte-input intrinsic are accepted. RILLBOOT adds the syntax needed to compile the compiler while retaining these implementations.\n'
  else:text+='RILLBOOT adds `*`, `/`, `%`, `&`, `|`, `>>`, logical `!`, zero-terminated string literals and escapes, global mutable words with literal initializers, global `bytes name[size];` buffers, indexed bytes, procedure parameters, and recursive calls. Calls evaluate arguments from left to right. Declarations may occur after calls; final acceptance rejects an undefined procedure or inconsistent arity. The table has 512 global/procedure records and 32 active local records. Each procedure has at most sixteen parameters and sixteen live local words.\n\nBuiltin calls are putc, status, exit, load8, open, create, close, read, write, exists, delete, rename, alloc, free, get8, get16, set8, and set16. The first three and load8 take respectively 1, 0, 1, and 1 arguments; file read/write and block stores take 3; rename and block loads take 2; other services take 1. Handles are opaque. read returns zero at EOF; a failure can also return zero, so check status immediately. A short positive read contains data; require exact write progress. File transfers preserve all byte values, including Control-Z. The native binding supplies eight file slots and sixteen allocated-block slots.\n\nRILLBOOT omits ^, <<, unary -, ~, explicit address-of, getc, load16, store8, and store16 because the compiler source does not need them. The RILL-written compiler adds the operators and pointer wrappers required by its tool successors.\n'
  text+='\nBoth milestones use the same 40-byte symbol record layout, 4096-byte file blocks, checked two-word text counters, scanner, parser state, and RILL.TMP/RILL.BAK publication. Source rejection preserves an accepted RESULT.IR; a failed publication may leave recovery files.\n'
 (dest/'900-language-reference.md').write_text(text)
(Q/'ladder-article-patches.json').write_text(json.dumps(patches,indent=2)+'\n')
print('Published continuing IR86, RILL0 and RILLBOOT constructions')
