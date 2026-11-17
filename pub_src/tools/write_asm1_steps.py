"""Publish the small source edits leading from ASM0 to the named-file assembler."""
from pathlib import Path
from difflib import SequenceMatcher
import json
from asm1_steps import ROOT,BASE,STEPS
from command_files import CHECKER
from publication_names import write_page

W=ROOT/'workbench/asm1';Q=ROOT/'qa/asm1';C=ROOT/'site/content/bootstrap/asm1'

def fence(kind,text):return '```'+kind+'\n'+text.rstrip('\n')+'\n```\n\n'

EXPLANATIONS={
'A01A':'''I start with ASM0's accepted source and mark the branches that will need room as I enlarge its routines. I can make a distant condition out of two instructions that ASM0 already knows.

## What this step adds

Six existing conditional branches become an opposite short condition followed by a near JMP. The accepted instruction table stays at twenty-five records. The assembler still reads SOURCE.ASM and writes RESULT.COM.

An 8086 conditional jump has a signed byte displacement, measured from the following instruction: -128 through +127. A near JMP has a signed word displacement. In `JNE SKIP / JMP DEST / SKIP:`, equality takes the JMP to DEST; inequality skips that JMP. The near JMP occupies three bytes, so the short branch only has to skip three bytes. The condition and destination have the same meaning as the original JE DEST.

These are explicit source bridges. We are not adding a new long-conditional spelling to the assembler. The file paths use JAE to skip an error JMP when carry is clear; the short-write test uses JE to skip its error JMP when the counts agree. INPUTCLOSED and the four ZWRITEOUT labels name those nearby landing points. IMMEDWORD makes the byte-versus-word immediate choice with the same pattern. The Z labels are ordinary labels, not generated instruction forms.

Some branches already fit their present routines. We choose the wider source pattern here so later report and file-handling additions do not rely on that spare reach. No new error category or encoding routine is introduced. The opening comment identifies the construction source and emits no bytes.
''',
'A01B':'''I will need two independently saved names. Before reading the command line, I give each name a place in the assembler's data and follow the existing file calls to those places.

## What this step adds

SRCNAME replaces FNAME as the source-name label. OPENFILE loads its address into DX. RESNAME remains the address used by WRITEOUT. Both names still contain SOURCE.ASM and RESULT.COM, so this checkpoint uses fixed files and accepts no filename arguments yet.

Each record now has thirteen bytes: at most eight base characters, one dot, three extension characters, and a terminating zero. The remaining zero bytes are capacity for a later, longer selected spelling. They are not characters in the default name. DOS open/create services expect the address of the first character and stop at the zero.

The name records move after OPTAB, and OUTPTR moves beside them. Moving a variable changes the address of its storage, which the assembler resolves from its label. It does not change the word held there: 24576 is still 6000H, the start of the existing complete-image output buffer. The buffer has not moved or become a stream.

OPTAB still has twenty-five records. Its counted lookup ends before SRCNAME. The DB directives under the name labels describe ordinary data, not additional instructions in the opcode table. HANDLE remains a separate DOS handle word; these buffers hold filenames, not handles.
''',
'A01C':'''The file names are still in their default buffers. I place a temporary probe call before the assembly driver so I can check the PSP reader before allowing it to open a disk file.

## What this step adds

DOS supplies a Program Segment Prefix before the program's 0100H entry. The byte at 80H is the command-tail length, and the bytes beginning at 81H are the tail itself. The program name is not part of that tail. At entry DS and ES select this same segment. CLD makes LODSB and STOSB advance their pointers.

CMDINIT sets SI to 81H and CX to the saved length. Each consumed character decrements CX. It never searches beyond that count for a zero. A length of 127 or more is rejected; the supported DOS tail is at most 126 bytes. CMDSKIP consumes spaces and tabs between names.

CMDCOUNT counts name slots as they are begun; malformed input makes the whole parse fail. CMDPTR remembers the start of the current destination slot, while DI advances through its characters. CMDBUF contains three thirteen-byte slots. The third lets the common reader retain an extra name; the assembler's later selection routine will accept exactly two or none. A fourth name is rejected before another slot can be written.

For each name BX counts characters in the current part and DX holds that part's limit: eight for the base, then three for the extension. CMDDOT permits one dot after a nonempty base, switches the limit, and requires a nonempty extension. CMDEND writes a zero and advances the saved slot pointer by thirteen. Empty parts and a second dot fail.

CMDUP folds a through z to A through Z. CMDNUM and CMDEXTRA admit digits, underscore and hyphen in addition to letters. Quotes, paths, drive colons, switches and other characters fail. A copied name is independent of the PSP bytes; later DOS operations may reuse the default disk-transfer area in that region.

On success CMDINIT returns the count in AX. On failure it returns 65535. It changes AX, BX, CX, DX, SI, DI, flags and the command storage. It is a startup operation, called once before assembly counters are initialized; CMDCOUNT starts as zero in the loaded image. Its Z labels use the branch-bridge pattern already introduced.

## The temporary startup probe

At ROOM the driver calls CMDPROBE before initializing either pass. CMDPROBE clears LINENO, calls CMDINIT and returns DOS success only for a count of two. A malformed spelling or another count enters the existing ERROR routine with category 9. PROBEOK returns DOS status zero. The probe exits through DOS rather than returning to its caller. The original driver and source parser remain below its call, ready for reuse, but are not reached at this stopping point. No file is opened or created. This two-name expectation belongs to the probe; the next step replaces its startup call and restores the no-argument defaults without retyping the driver.

Replace CHECK.BAT so it forwards the tail to its program:

'''+fence('dos',CHECKER),
'A01D':'''The reader can retain names without touching disk. I replace the temporary probe call with file selection and connect those retained spellings to the two existing file services.

## What this step adds

CMDFILES calls CMDINIT once. Zero names keep the known SOURCE.ASM and RESULT.COM defaults. Exactly two names are copied from the first and second CMDBUF slots into SRCNAME and RESNAME with the existing COPYZ routine. Any other count, including CMDINIT's 65535 failure value, enters ERROR with category 9.

CMDMATCH compares two complete zero-terminated spellings. SI and DI advance through the names; BX and AH are scratch. AX is one for equality and zero for inequality. A shared prefix alone is not equality. Because CMDINIT folds letters before copying, differently cased spellings of the same filename compare equal.

Five comparisons reject source=result, source=temporary, source=backup, result=temporary and result=backup. TMPNAME names ASMA.TMP; BAKNAME names RESULT.BAK. Those names are reserved now for the streamed writer and publication routines that will follow. These comparisons check selected spellings; they do not inspect or create recovery files. Existing-recovery-file detection is a later stopping point.

Remove CMDPROBE and its startup call. The retained driver calls CMDFILES after its stack check and before pass counters or file services. The helper changes the working registers, so those counters are initialized afterward. OPENFILE and WRITEOUT already use the two name-buffer addresses. Both input passes still finish before output creation.

The chosen result must also differ from the running checkpoint's executable name. Keep the builder under its own saved name. Use only unquoted 8.3 names in the current directory. This checkpoint still reports just OK and the byte count; the next step adds the result spelling to that report.
''',
'A01E':'''The assembler can write the selected file, but its success line still leaves me to remember which name I supplied. I want that line to identify the result I should inspect.

## What this step adds

CMDTEXT prints a zero-terminated string addressed by SI. LODSB fetches each byte; zero returns to the caller. Each other byte goes through DL to DOS function 2. SI advances, AX and DX are scratch, and CLD at startup supplies the forward direction.

The existing TEXT routine prints dollar-terminated messages with DOS function 9. A filename buffer is zero-terminated instead, so passing it to TEXT would use the wrong stopping rule. CMDTEXT handles that representation directly without changing the message routines.

After WRITEOUT has successfully written and closed the output, it prints OKMSG, calls CMDTEXT with RESNAME, prints one space, then uses the existing NUMBER and BYTEMSG routines. The success line becomes OK, the chosen result name, and the byte count. A failed write or close still takes FILEBAD and cannot print a success line.

This changes the report, not the selected file, instruction language, or emitted program bytes. The fixture below includes zero, Control-Z and a high byte as data so its entire result is checked as bytes.
''',
'A01F':'''A handle word keeps the number DOS returned. That number alone cannot tell a later cleanup routine whether the handle is still open. I give the input file its own small state flag.

## What this step adds

INOPEN is one byte, initially zero. OPENFILE first checks that DOS function 3DH succeeded and saves the returned handle. Only then does it store one in INOPEN. A failed open leaves zero.

CLOSEFILE passes the saved handle to DOS function 3EH and checks carry. Only a successful close reaches INPUTCLOSED and stores zero. A failed close takes FILEBAD with the flag still set, rather than falsely recording that the file was closed. The handle word itself may still contain its old number after a close; INOPEN is what describes its lifetime.

This checkpoint records ownership state; it does not yet add cleanup, deletion or recovery behavior. The existing ERROR path still returns to DOS, which releases the process's handles. The later cleanup article will consume INOPEN to decide whether to attempt an explicit close. Output ownership needs its own flags when the streamed writer is introduced.

The new byte lives between BAKNAME and OUTPTR. OUTPTR still contains 6000H, and the complete-image output buffer remains in use. No opcode-table record is added here.
''',
}

def patch(previous,lines):
 changes=[];text='Apply these edits from the bottom of the old file upward. Physical positions locate the old source; the context identifies the exact edit. Keep all other source.\n\n'
 for i,(_,a,b,c,d) in enumerate(reversed([x for x in SequenceMatcher(None,previous,lines,autojunk=False).get_opcodes() if x[0]!='equal']),1):
  before=previous[max(0,a-3):a];after=previous[b:b+2];old=previous[a:b];new=lines[c:d]
  text+=f'### Change {i}\n\n'
  if before:text+='Unchanged source immediately before the edit:\n\n'+fence('asm','\n'.join(before))
  if old:text+=f'Remove old physical positions {a+1}–{b}:\n\n'+fence('asm','\n'.join(old))
  else:text+=f'Insert after old physical line {a}.\n\n'
  if new:text+=('Replace with:\n\n' if old else 'Insert:\n\n')+fence('asm','\n'.join(new))
  else:text+='There is no replacement source.\n\n'
  if after:text+='The following old source stays in place:\n\n'+fence('asm','\n'.join(after))
  changes.append(dict(a1=a,a2=b,old=old,new=new,context=before,after=after))
 return text,changes

def publish():
 facts=json.loads((Q/'intro.json').read_text());previous=BASE.splitlines();oldfile='ASM0.ASM';patches=[]
 for index,s in enumerate(facts,1):
  name=s['id'];lines=(W/(name+'.ASM')).read_text().splitlines()
  meta=dict(title=f'{index:02} · '+s['title'],weight=index,description=s['description'],download=name+'.ASM',download_group='tools/asm1',reader_names=1,command_examples='literal')
  t='+++\n'+''.join(k+' = '+json.dumps(v)+'\n' for k,v in meta.items())+'+++\n\n'+EXPLANATIONS[name]+'\n\n## Enter the source\n\n'
  t+=f'Copy {oldfile} to {name}.ASM. '
  edits,changes=patch(previous,lines);t+=edits
  t+='## Build this stopping point\n\n'+fence('dos',f'COPY {name}.ASM SOURCE.ASM\nCHECK ASMKEEP\nCOPY RESULT.COM {name}.COM')
  t+=f'Require the preceding ASM0 to report `OK {s["binary_bytes"]:05} bytes` and CHECK to report PASS before preserving the result. VIEW.BAS must show {name}.COM length {s["binary_bytes"]} bytes. Keep the source and executable together.\n\n'
  t+='## Check the addition\n\n'
  if s['mode']=='probe':
   t+=fence('dos','CHECK A01C in.asm out.com')+'Require PASS and no program text before it. The names need not exist: this driver makes no file calls. Repeat with tabs between the names; require PASS.\n\n'
   t+='Try `CHECK A01C ONLY.ASM`, then `CHECK A01C A..ASM OUT.COM`. Each must report `ERROR 00000 CODE 9` and FAIL. The first checks the probe count; the second checks the spelling. There is no result file to inspect and no display helper to add.\n\n'
  else:
   fixture='T'+name[1:]+'.ASM';result=s.get('result','RESULT.COM')
   t+='Create '+fixture+':\n\n'+fence('asm',s['fixture'])
   commands=(f'COPY {fixture} SOURCE.ASM\nCHECK {name}' if s['mode']=='fixed' else f'CHECK {name} {fixture} {result}')
   t+=fence('dos',commands)
   report=f'OK {result} {s["target_bytes"]:05} bytes' if name in ['A01E','A01F'] else f'OK {s["target_bytes"]:05} bytes'
   t+='Require:\n\n'+fence('text',report+'\nPASS')
   t+=f'VIEW.BAS must show {result} length {s["target_bytes"]} bytes and these complete contents:\n\n'+fence('text',s['target_hex'])
   t+='The file is an encoding check; inspect it rather than executing it.\n\n'
  if name=='A01D':t+='Run `CHECK A01D T01D.ASM`, then `CHECK A01D T01D.ASM t01d.asm`. Each must report `ERROR 00000 CODE 9` and FAIL before a file is opened. Preserve CHOSEN.COM. With no arguments, A01D still assembles SOURCE.ASM to RESULT.COM.\n\n'
  if name=='A01F':
   t+='The open-state flag is internal, so also inspect the bytes retained in A01F.COM. Count file offsets from zero; a COM file offset is its loaded offset minus 0100H. VIEW.BAS prints sixteen bytes on each complete row.\n\n'
   t+='| File offset | Expected bytes | Meaning |\n|---|---|---|\n'
   for key,meaning in [('open','Load AL with one and store it in INOPEN'),('close','Load AL with zero and store it in INOPEN')]:
    t+=f'| {s[key+"_offset"]:04X}H | `{s[key+"_hex"]}` | {meaning} |\n'
   t+=f'\nIn both stores, the final two bytes are the low and high bytes of INOPEN\'s loaded address, {s["flag_address"]:04X}H. These are the assembler\'s own retained instructions, not a temporary printing routine.\n\n'
  nextpage=facts[index]['page'] if index<len(facts) else '01-fixed-work-files.md'
  nexttitle=facts[index]['title'] if index<len(facts) else 'Adding XOR to the Arithmetic Table'
  t+=f'Continue with [{nexttitle}](../{Path(nextpage).stem}/index.html).\n'
  write_page(C/s['page'],t)
  patches.append(dict(source=name+'.ASM',base=oldfile,page=s['page'],chapter=index,changes=changes))
  previous=lines;oldfile=name+'.ASM'
 (Q/'intro-patches.json').write_text(json.dumps(patches,indent=2)+'\n')
 print('Published six focused ASM1 steps before the separate XOR lesson')

if __name__=='__main__':publish()
