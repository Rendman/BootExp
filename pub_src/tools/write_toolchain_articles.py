"""Render exact source edits and results measured by the published native tools."""
from pathlib import Path
from difflib import SequenceMatcher
import re,json
from compiler_publication import publish
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'workbench/toolchain';Q=ROOT/'qa/toolchain';BASE=ROOT/'site/content/bootstrap'
def front(title,weight,description,download):return '+++\n'+f'title = {json.dumps(title)}\nweight = {weight}\ndescription = {json.dumps(description)}\ndownload = "{download}"\ndownload_group = "toolchain"\n'+'+++\n\n'
def fence(kind,s):return '```'+kind+'\n'+s.replace('\r\n','\n').rstrip('\n')+'\n```\n\n'
def slug(s):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
HELP={
'PRINT':'A is a pointer to terminated bytes. Save the pointer in a local slot before PUTC changes A. A zero byte ends the walk; it is not written.',
'PRINTNUM':'Save the value, current decimal place, and output digit separately. Repeated subtraction chooses one digit at each place. Formatting cannot borrow a parser work cell that remains live across a call.',
'PRINT32':'Treat the two words as one unsigned count. Divide the high word by ten, then carry its remainder through the low word one bit at a time. Store the remainders and display them in reverse order, including leading zeroes.',
'ERROR':'An error category is an explicit parameter. Input, output, temporary ownership, and backup state have separate meanings. Cleanup may close or delete owned files, but an older accepted RESULT.IR is not scratch storage.',
'FAIL':'An error category is an explicit parameter. Close owned handles, retain recovery files when restoration fails, and exit nonzero. No ordinary parse routine returns a successful result after this path.',
'LETTER':'Accept an underscore or a letter in either ASCII case. The scanner performs case folding when saving a name; character recognition alone does not modify the source byte.',
'DIGIT':'The decimal range is exactly ASCII 48 through 57. Punctuation next to a digit is not another numeric digit.',
'NEXT':'INPOS and INLEN describe an already-read block. Refill only after consuming it. A short positive read is data, not EOF. Check STATUS before using a count. Control-Z ends source text; the byte services used by a compiled program still preserve that value.',
'LEX':'Keep source position, token kind, numeric value, and complete spelling distinct. Save temporary values in local slots across NEXT calls. Paired punctuation is recognized before returning a single character; comments consume source without manufacturing a token.',
'EXPECT':'Compare the current token before advancing. On success, leave the following token ready; a caller must not advance once more accidentally.',
'ISWORD':'Check the token class and every character through the zero terminator. A keyword prefix is insufficient: FN and FNN are different spellings.',
'SETIDENT':'Copy an explicit terminated spelling into IDENT. This is a table-test helper as well as a way to ask for a required entry without depending on the current source token.',
'TWORD':'An offset is meaningful only together with the TABLE block handle. GET16 reads the canonical low-byte-first word after validating its extent.',
'TBYTE':'Use the same opaque block with a byte offset. GET8 returns a zero-extended byte; it does not reveal a segment selector or native address.',
'WRITEFIELD':'Pass the record offset and word value explicitly. SET16 performs a checked two-byte access. The caller chooses a field offset within its own record.',
'RECORDFIELDS':'Kind, value or slot, and lexical level are distinct word fields. Store them explicitly after initializing a record rather than relying on new memory containing zeroes.',
'RECORD':'Initialize the entire forty-byte record, copy the complete spelling, then write the explicit fields. The global region begins at zero in TABLE; the local region begins at byte offset 20480.',
'NEWGLOBAL':'Append one global or procedure record, bounded by 512 entries. The record offset remains stable even after scanning changes IDENT.',
'NEWLOCAL':'Append a record in the separate local-name region. Its slot number and lexical level are explicit fields. The region has room for parameters and live local bindings, not a second global namespace.',
'FIND':'Search entries from the end toward the beginning and compare complete spellings. This selects the innermost active binding. Return 65535 for absence; offset zero is a valid found record.',
'LOOKGLOBAL':'Restrict FIND to the active global entries. A local shadow must not change how a procedure definition is found.',
'RESOLVE':'Search active local bindings first, then globals. Save the found offset separately from kind and value fields; recursive parsing can replace the shared search result.',
'FLUSH':'Write only a nonempty output block. Check STATUS and the exact returned count before clearing OUTLEN. A zero-count DOS write is never used to flush or truncate the file.',
'OUTCHAR':'Append one byte, advance the checked low/high output count, and flush a full 4096-byte block. The output belongs to this assembly, not to the input refill buffer.',
'OUTSTR':'Walk a terminated template while preserving its pointer. Normalize a bare LF in an IR template to CR/LF while retaining existing CR/LF. Quoted source escapes are still printable backslash spellings at this point.',
'OUTNUM':'Emit a fixed decimal word spelling through OUTCHAR. It uses the same checked output path as instruction names and delimiters.',
'NEWLINE':'End an emitted IR record with carriage return and line feed. A record terminator and a zero byte ending an in-memory string have different jobs.',
'NEWLABEL':'Advance a checked word counter. The counter supplies names, not physical code addresses.',
'LABELDEF':'Emit LABEL, the reserved B_ prefix, and the saved number. Every definition ends with a record terminator.',
'LABELJUMP':'Emit a saved label number as an operand after the caller has selected the branch operation. Preserve that target across formatting calls.',
'OUTNAME':'Read the spelling from its stable symbol record. Parsing another argument must not silently change the name being emitted.',
'BUILTIN':'A terminated spelling selects an intrinsic record containing an arity and IR text. Compare the whole name. A failed match advances past both fields before considering another entry.',
'RESOLVEOPTIONAL':'A call can precede its procedure definition. Record its name and required arity as a pending procedure; final acceptance rejects any definition that never arrives. Ordinary undeclared variable use remains an error.',
'PREC':'Return a precedence number, with zero for a nonoperator. Multiplication binds more tightly than addition; word comparisons and bit operators occupy explicitly defined lower levels.',
'BINARY':'Emit the selected IR operation after the right expression is complete. This routine translates an operation; it does not evaluate the user program during compilation.',
'EXPR':'Save the pending operator and precedence in local slots. Emit PUSH for the left operand, recurse at one higher minimum precedence for the right, then emit the operation. A bounded recursion counter prevents uncontrolled nesting.',
'PRIMARY':'A primary can emit a literal, string pointer, binding, addressed slot, indexed byte, or call. Parentheses recurse through EXPR. Save binding metadata before scanning a nested expression, which can change the shared search fields.',
'CALLARGS':'Evaluate arguments from left to right and save each emitted result. Check the complete argument count against the intrinsic or procedure record. INVOKE consumes precisely those words and preserves older expression operands.',
'GLOBALWORD':'A global mutable word has a literal initializer and a stable V_ name. Reject duplicates before emitting its declaration.',
'GLOBALBUFFER':'Declare a nonempty global byte extent. The buffer is materialized in the COM image. Extra allocated blocks are a different service and are not pointers into this declaration.',
'DECLARE':'Allocate a local slot and record its lexical level. Mark it unavailable during its own initializer, then publish the binding after acceptance. Save its slot across recursive expression parsing.',
'BLOCK':'Save the active local-name count and next local slot at entry. Restore both at the closing brace. This permits a nested binding to shadow an outer one without permanently consuming its name or slot.',
'STATEMENT':'Keep assignment destinations, false targets, and loop targets in local slots. An if/else join and a while back edge meet with no expression temporaries. Parse every statement even after an explicit return.',
'FUNCTION':'Record the procedure name before scanning parameters, verify any earlier call arity, and create parameter bindings. PROC reserves the bounded local frame. Every normal fall-through ends with return value zero.',
'MAIN':'Open the fixed source, stream accepted IR through an owned temporary file, and verify all pending procedures. Require an argument-free main. Publish only after parsing, source close, flush, and output close succeed.'}
def helper(c):return HELP.get(c.get('key','').upper(),'Keep the input fields, result, and scratch state explicit. Use the saved descriptor and checked stream interfaces rather than retaining a complete source or output image.')
def patches(old,new,kind,oldname):
 t='';changes=[]
 for i,(_,a,b,c,d) in enumerate(reversed([op for op in SequenceMatcher(None,old,new,autojunk=False).get_opcodes() if op[0]!='equal']),1):
  before=old[max(0,a-3):a];after=old[b:b+2];removed=old[a:b];added=new[c:d]
  t+=f'### Edit {i}\n\n'
  if before:t+='Unchanged source immediately before the edit:\n\n'+fence(kind,'\n'.join(before))
  if removed:t+=f'Remove this source at old physical positions {a+1}–{b} in {oldname}:\n\n'+fence(kind,'\n'.join(removed))
  else:t+=f'Insert after old physical line {a}.\n\n'
  if added:t+=('Replace it with:\n\n' if removed else 'Insert:\n\n')+fence(kind,'\n'.join(added))
  else:t+='There is no replacement source.\n\n'
  if after:t+='The following old source remains in place:\n\n'+fence(kind,'\n'.join(after))
  changes.append(dict(a1=a,a2=b,old=removed,new=added,context=before,after=after))
 return t,changes
allpatches=[]
for family,collection,offset,prefix,language in [('ir-extensions','ir86',36,'IW','asm'),('rill-seed-series','rb',33,'RB','ir'),('rill-self-series','rc',88,'RC','rill')]:
 cases=json.loads((Q/(family+'.json')).read_text());old=(ROOT/'workbench/asm86a/ASM86A.ASM').read_text().splitlines() if prefix=='IW' else [];oldname='ASM86A.ASM' if old else None
 for c in cases:
  n=c['number'];name=f'{prefix}{n:02}';weight=offset+n;page=f'{weight:03}-{prefix.lower()}-{slug(c["title"])}.md';source=(W/c['source']).read_text().splitlines()
  description=c.get('why') or helper(c).split('. ')[0]+'.'
  t=front(f'{name} · '+c['title'],weight if prefix=='IW' else n,description,c['source'])
  t+=description+'\n\n## The working parts\n\n'+(helper(c) if prefix!='IW' else c['why']+' The assembly routines use the inherited bounded reader and owned-file cleanup. The operation table supplies argument class, stack action, and an authored target template. Native encodings belong to this backend; the IR operation retains its abstract meaning.')+'\n\n'
  if prefix in ['RB','RC']:t+='The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.\n\n'
  if prefix in ['RB','RC'] and c.get('key','').upper()=='BLOCK':t=t.replace('+++\n\n','cartoon = \"rill-drawers.png\"\n+++\n\n',1)
  t+='## Enter the source\n\n'
  if oldname:t+=f'Copy {oldname} to {c["source"]}. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.\n\n'
  else:t+=f'Create {c["source"]} as plain text. This is its complete source:\n\n'
  if oldname:
   edit,changes=patches(old,source,language,oldname);t+=edit
  else:
   t+=fence(language,'\n'.join(source));changes=[dict(a1=0,a2=0,old=[],new=source,context=[],after=[])]
  t+='## Build this stopping point\n\n'
  if prefix=='IW':
   t+=fence('dos',f'COPY {c["source"]} SOURCE.ASM\nCHECK ASMAKEEP')+f'Require `OK RESULT.COM {c["binary_bytes"]:05} bytes` and PASS, then save it:\n\n'+fence('dos',f'COPY RESULT.COM {name}.COM')
  else:
   if prefix=='RC':
    t+=fence('dos',f'COPY {c["source"]} SOURCE.RIL\nCHECK RILLBOOT')+f'Require `OK RESULT.IR {c["ir_bytes"]:010}` and PASS. Copy RESULT.IR to SOURCE.IR.\n\n'
   else:t+=fence('dos',f'COPY {c["source"]} SOURCE.IR')
   t+=fence('dos','CHECK IWKEEP\nCOPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP')+f'Require IR86 `OK RESULT.ASM {c["assembly_bytes"]:010} text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM {c["binary_bytes"]:05} bytes` and PASS before saving:\n\n'+fence('dos',f'COPY RESULT.COM {name}.COM')
  t+=f'VIEW.BAS must report {name}.COM length {c["binary_bytes"]} bytes. Keep this executable and its source together.\n\n## Acceptance check\n\n'
  fixture=c.get('fixture')
  if fixture is not None:
   fn=f'T{name}.'+('IR' if prefix=='IW' else 'RIL');kind='text' if prefix=='IW' and n<5 else 'ir' if prefix=='IW' else 'rill'
   t+=f'Create {fn} with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:\n\n'+fence(kind,fixture)
   t+=fence('dos',f'COPY {fn} SOURCE.'+('IR' if prefix=='IW' else 'RIL'))
  t+=fence('dos',f'CHECK {name}')+'Require, apart from command echo and the checker\'s separator:\n\n'+fence('text',c.get('output',c.get('console','')).replace('\r\n','\n')+'PASS\n')
  if prefix=='IW':
   if n==3:t+='VIEW.BAS must show RESULT.ASM length 5 and bytes `41 42 43 0D 0A`. This is copied data; do not execute or assemble it.\n\n'
   elif n>=5:
    t+=fence('dos','COPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP')+f'Require `OK RESULT.COM {c["target_bytes"]:05} bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length {c["target_bytes"]} and these '+('first thirty-two bytes' if c['target_bytes']>32 else 'complete bytes')+':\n\n'+fence('text',c['target_hex'])
    if n in [13,15,17,21]:t+='First create the ordinary input file A with `ECHO A>A`. Its declared filename is the word 65 followed by its zero high byte. '
    if n==12:t+='Create KEY.TXT with `ECHO A>KEY.TXT` and run CHECK TRY <KEY.TXT. '
    else:t+='Run CHECK TRY. '
    if c['program_exit']:t+=f'It deliberately returns {c["program_exit"]}; the checker reports FAIL. This verifies the program\'s explicit exit value.\n\n'
    elif c['program_output']:t+='It displays `'+c['program_output']+'` and reports PASS.\n\n'
    else:t+='It returns zero and the checker reports PASS.\n\n'
   if n==23:t+=fence('dos','COPY IW23.COM IRWIDE.COM\nCOPY IRWIDE.COM IWKEEP.COM')+'Preserve IWKEEP as the fixed-file translator. The earlier IRKEEP retains its source-name prompt. IRWIDE.ASM and IW23.ASM are identical.\n\n'
  elif 'result' in c:
   resultname='RESULT.IR' if c['key'].upper()=='MAIN' else 'RILL.TMP'
   t+=f'TYPE {resultname}. Its complete text is:\n\n'+fence('ir',c['result'])
   t+=f'VIEW.BAS must show length {c["result_bytes"]} bytes. '+('For an empty fragment, length zero is the expected visible result. ' if c['result_bytes']==0 else '')
   if c['complete']:
    t+='This is a complete program. Copy it to SOURCE.IR, run CHECK IWKEEP, copy the accepted RESULT.ASM to SOURCE.ASM, and run CHECK ASMAKEEP. Require OK and PASS at both steps. '
    t+=f'VIEW.BAS must report RESULT.COM length {c["program_bytes"]}. Copy that file to TRY.COM; CHECK TRY displays `{c["program_output"]}` and reports PASS.\n\n'
   else:t+='This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.\n\n'
   if resultname=='RILL.TMP':t+='After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.\n\n'
  t+='## A rejection or boundary check\n\n'
  if prefix=='IW':
   if c.get('bad'):
    fn=f'X{name}.IR';(W/fn).write_bytes(c['bad'].replace('\n','\r\n').encode());t+=f'Create {fn}:\n\n'+fence('ir',c['bad'])+fence('dos',f'COPY {fn} SOURCE.IR\nCHECK {name}')
   else:t+=f'Rename SOURCE.IR to an unused HOLD.IR, then run CHECK {name}. Restore the source after the test.\n\n'
   t+='Require:\n\n'+fence('text',c['error']+'FAIL\n')+'The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.\n\n'
  elif c.get('code'):
   if c['bad'] is not None:
    fn=f'X{name}.RIL';t+=f'Create {fn}:\n\n'+fence('rill',c['bad'])+fence('dos',f'COPY {fn} SOURCE.RIL\nCHECK {name}')
   else:t+=f'Rename SOURCE.RIL to an unused HOLD.RIL and run CHECK {name}. Restore the source afterward.\n\n'
   t+='Require:\n\n'+fence('text',c['error']+'FAIL\n')+'An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.\n\n'
  elif prefix=='RB':
   t+='Check a representable-word boundary in the preceding translator. Create BAD.IR:\n\n'+fence('ir','PROC MAIN 0 0\nLIT 65536\nRETURN')+fence('dos','COPY BAD.IR SOURCE.IR\nCHECK IWKEEP')+'Require `IR ERROR 0000000002 CODE 2` and FAIL. The accepted RESULT.ASM must remain unchanged. The diagnostic cannot be built from an out-of-range word.\n\n'
  else:
   t+='Check the same word boundary in the compiler seed. Create BAD.RIL:\n\n'+fence('rill','fn main(){return 65536;}')+fence('dos','COPY BAD.RIL SOURCE.RIL\nCHECK RILLBOOT')+'Require `ERROR 0000000001 CODE 00003` and FAIL, preserving the accepted RESULT.IR. An unexpected PASS fails this check.\n\n'
  t+='## If the result differs\n\nCheck the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper\'s local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.\n'
  if prefix=='RB' and c['key']=='MAIN':t+='\nPreserve RB47.COM as RILLBOOT.COM and RB47.IR as RILLBOOT.IR. This compiler seed was built entirely through the native IR86 and ASM86A tools. Continue with the complete programs in this collection, then the separate [RC collection](../../rc/index.html).\n'
  if prefix=='RC' and c['key']=='main':t+='\nPreserve RC43.COM as R0.COM and RC43.RIL as RILL.RIL. The same source is the input for the two compiler self-build comparisons.\n'
  publish(collection,page,t)
  allpatches.append(dict(family=family,number=n,collection=collection,page=page,base=oldname,kind=language,changes=changes,source=c['source']))
  old=source;oldname=c['source']
(Q/'article-patches.json').write_text(json.dumps(allpatches,indent=2)+'\n')
# Each new language capability has a short, complete program and a concrete rejection.
for i,c in enumerate(json.loads((Q/'examples.json').read_text()),81):
 t=front(c['title'],i-32,c['why'],c['name']+'.RIL')+c['why']+'\n\nSave '+c['name']+'.RIL:\n\n'+fence('rill',c['source'])
 t+=fence('dos',f'COPY {c["name"]}.RIL SOURCE.RIL\nCHECK RILLBOOT\nCOPY RESULT.IR SOURCE.IR\nCHECK IWKEEP\nCOPY RESULT.ASM SOURCE.ASM\nCHECK ASMAKEEP')
 t+=f'Require `OK RESULT.IR {c["ir_bytes"]:010}`, translator `OK RESULT.ASM {c["assembly_bytes"]:010} text bytes`, and assembler `OK RESULT.COM {c["binary_bytes"]:05} bytes`, each with PASS **before** the following copy. VIEW.BAS must show result length {c["binary_bytes"]} and these first thirty-two bytes:\n\n'+fence('text',c['hex'])
 t+=f'Copy RESULT.COM to {c["name"]}.COM. '
 if c.get('files'):t+='Create IN.TXT with `ECHO A short copy.>IN.TXT`. '
 t+='CHECK '+c['name']+' '+('displays '+json.dumps(c['output'])+' and ' if c['output'] else '')+'reports PASS. '
 if c.get('result_file'):t+='COMP IN.TXT OUT.TXT must report no differences; answer N to its compare-more-files question. Empty and binary input are valid too. A missing IN.TXT must report FAIL before creating OUT.TXT. '
 t+='Here `\\r\\n` means carriage return and line feed.\n\nFor a separate source rejection, create BAD.RIL:\n\n'+fence('rill',c['bad'])+fence('dos','COPY BAD.RIL SOURCE.RIL\nCHECK RILLBOOT')+'Require:\n\n'+fence('text',c['error']+'\nFAIL')+'The older RESULT.IR must remain unchanged. An unexpected PASS fails the rejection check. Restore the accepted source before another build.\n'
 publish('rb',f'{i:03}-{slug(c["title"])}.md',t)
print('Rendered native IR, compiler seed, RILL compiler, and complete language examples')
