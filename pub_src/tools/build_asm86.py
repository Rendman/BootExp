"""Publish authored assembly fragments as gradual, complete type-in checkpoints.
This prepares source text and articles; only BOOTASM or ASM86 emits COM bytes.
"""
from pathlib import Path
import re,json,difflib,sys
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'workbench/asm0';CONTENT=ROOT/'site/content/bootstrap/asm0'
WORK.mkdir(parents=True,exist_ok=True);CONTENT.mkdir(parents=True,exist_ok=True)
TEMPLATE=(ROOT/'tools/asm86_template.asm').read_text()
STARTS=['START','FILEBAD','OPENFILE','CLOSEFILE','WRITEOUT','NEXTBYTE','READLINE','SCAN','LOOK','REGISTER','VALIDNAME','VALUE','SYMBOLVALUE','DEFINE','OPERAND','MEMORY','STATEMENT','DATAITEM','FIXED','SINGLE','INTERRUPT','NEARJUMP','SHORTJUMP','FINISH','TWOOPERANDS','MOVOPERANDS','MOVREG','REGMOD','IMMEDVALUE','LOADMEM','STOREMEM','SAMEWIDTH','TIMES8','BYTEVALUE','EMITWORD','EMIT','COPYZ','TEXT','NUMBER','ERROR','OKMSG']
positions={name:TEMPLATE.index('\n'+name+':\n')+1 for name in STARTS}
BLOCK={name:TEMPLATE[positions[name]:positions[nextname]].strip()+'\n' for name,nextname in zip(STARTS,STARTS[1:])}
# Strip surrounding explanatory comments from each source fragment.
for name,code in list(BLOCK.items()):
 BLOCK[name]='\n'.join(line for line in code.splitlines() if line.strip() and not line.lstrip().startswith(';'))+'\n'
BLOCK['ZTEXT']='''ZTEXT:
LODSB
CMP AL,0
JE ZDONE
MOV DL,AL
MOV AH,2
INT 21H
JMP ZTEXT
ZDONE:
RET
'''
ORDER=STARTS[1:-1]+['ZTEXT']
data=TEMPLATE[positions['OKMSG']:]
matches=list(re.finditer(r'^([A-Z][A-Z0-9_]*):$',data,re.M))
FIELDS={m.group(1):data[m.start():matches[i+1].start() if i+1<len(matches) else len(data)].strip()+'\n' for i,m in enumerate(matches)}
FIELDORDER=list(FIELDS)
FIELDS['HELLOMSG']='HELLOMSG:\nDB 65,83,77,48,13,10,36\n'
FIELDS['READYMSG']='READYMSG:\nDB 82,69,65,68,89,13,10,36\n'
FIELDS['OPENMSG']='OPENMSG:\nDB 79,112,101,110,101,100,13,10,36\n'
FIELDS['BUFFERMSG']='BUFFERMSG:\nDB 66,117,102,102,101,114,101,100,32,36\n'
FIELDORDER+=['HELLOMSG','READYMSG','OPENMSG','BUFFERMSG']
records=[]
for line in FIELDS['OPTAB'].splitlines()[1:]:
 if line.startswith('DB '):
  row=[int(v) for v in line[3:].split(',')]
  name=bytes(row[:6]).split(b'\0')[0].decode('ascii')
  records.append((name,row,line))

def dos(path,text):path.write_bytes((text.rstrip()+'\n').replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
def tokens(text):
 return set(re.findall(r'\b[A-Z][A-Z0-9_]*\b','\n'.join(line.split(';',1)[0] for line in text.splitlines())))
def driver(body,*,memory=True):
 s='START:\nCLD\n'
 if memory:s+='CMP SP,0FFFEH\nJE ROOM\nMOV AX,7\nJMP ERROR\nROOM:\n'
 return s+body.strip()+'\nGOOD:\nMOV AX,4C00H\nINT 21H\n'
READLOOP='''CALL OPENFILE
DRIVERLINE:
CALL READLINE
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
'''
CLOSELOOP='''JMP DRIVERLINE
DRIVERDONE:
CALL CLOSEFILE
'''
def value_driver(action,*,write=False,buffer=False):
 init=''
 if buffer:init='MOV AL,2\nMOV [PASS],AL\nMOV AX,100H\nMOV [PC],AX\nMOV AX,6000H\nMOV [OUTPTR],AX\n'
 body=init+READLOOP+'CALL SCAN\nCALL VALUE\n'+action+'\n'+CLOSELOOP
 if write:body+='CALL WRITEOUT\n'
 elif buffer:body+='MOV DX,BUFFERMSG\nCALL TEXT\nMOV AX,[PC]\nSUB AX,100H\nCALL NUMBER\nMOV DX,BYTEMSG\nCALL TEXT\n'
 return driver(body)

def assembler_main(two=False,symbols=False):
 s=BLOCK['START']
 if not symbols:s=s.replace('MOV AX,0\nMOV [SYMC],AX\nMOV AX,3000H\nMOV [SYMNEXT],AX\n','')
 if not two:
  s=s.replace('MOV AL,1\nMOV [PASS],AL','MOV AL,2\nMOV [PASS],AL')
  s=s.replace('MOV AL,[PASS]\nADD AL,1\nMOV [PASS],AL\nCMP AL,3\nJB PASSSTART\n','')
 return s

def statement(names,labels=False):
 prefix='''STATEMENT:
CALL SCAN
MOV AL,[2300H]
CMP AL,0
JNE STWORD
RET
STWORD:
'''
 if labels:prefix+='''AFTERWORD:
LODSB
CMP AL,32
JE AFTERWORD
CMP AL,58
JNE INSTRUCTION
CALL DEFINE
CALL FINISH
RET
INSTRUCTION:
DEC SI
'''
 prefix+=f'''MOV BX,OPTAB
MOV CX,{len(names)}
MOV AX,8
CALL LOOK
CMP BX,0
JNE STOPFOUND
MOV AX,1
JMP ERROR
STOPFOUND:
ADD BX,6
MOV AL,[BX]
MOV [TYPE],AL
INC BX
MOV AL,[BX]
MOV [OP],AL
MOV AL,[TYPE]
'''
 types={row[1][6] for row in records if row[0] in names}
 for typ,handler in [(1,'DATAITEM'),(2,'FIXED'),(5,'SINGLE'),(6,'INTERRUPT'),(7,'NEARJUMP'),(8,'SHORTJUMP')]:
  if typ in types:prefix+=f'CMP AL,{typ}\nJNE STNEXT{typ}\nCALL {handler}\nRET\nSTNEXT{typ}:\n'
 if types & {3,4}:prefix+='CALL TWOOPERANDS\nCALL FINISH\nRET\n'
 else:prefix+='JMP SYNTAXBAD\n'
 prefix+='SYNTAXBAD:\nMOV AX,1\nJMP ERROR\n'
 return prefix

def numeric(hexadecimal=False,reserved=False,symbolic=False):
 s=BLOCK['VALUE']
 if not symbolic:
  alternative='JMP NUMBERBAD\n'
  if reserved:alternative='CALL REGISTER\nCMP AX,0FFFFH\nJNE RESERVEDNUM\nJMP NUMBERBAD\nRESERVEDNUM:\nMOV AX,3\nJMP ERROR\n'
  s=s.replace('JMP SYMBOLVALUE\n',alternative)
 if not hexadecimal:
  start=s.index('MOV BX,DI\n');end=s.index('NUMBERSTART:\n',start)
  s=s[:start]+'MOV BP,10\n'+s[end:]
  s=s.replace('CMP AL,9\nJBE DIGITOK\nSUB AL,7\nCMP AL,10\nJB NUMBERBAD\nCMP AL,15\nJA NUMBERBAD', 'CMP AL,9\nJA NUMBERBAD')
  s=s.replace('CMP BP,16\nJE HEXDIGIT\n','')
  start=s.index('JMP ADDDIGIT\n');end=s.index('ADDDIGIT:\n',start)
  s=s[:start]+s[end:]
 return s

def operand(memory=False):
 s=BLOCK['OPERAND']
 if not memory:s=s.replace('MOV AL,[2300H]\nCMP AL,91\nJE MEMORY\n','')
 return s

def two_operands(math=False,memory=False):
 s=BLOCK['TWOOPERANDS']
 if not memory:s=s.replace('MOV AX,[VAL]\nMOV [V1],AX\n','')
 if not math:
  start=s.index('MOV AL,[TYPE]\n');end=s.index('TWOBAD:\n',start)
  s=s[:start]+'JMP MOVOPERANDS\n'+s[end:]
 return s

def mov_operands(copies=False,memory=False):
 s=BLOCK['MOVOPERANDS']
 if not memory:
  s=s.replace('CMP AL,2\nJNE MOVDESTREG\nJMP STOREMEM\nMOVDESTREG:\n','')
  s=s.replace('CMP AL,2\nJE LOADMEM\n','CMP AL,3\nJNE TWOBAD\n')
 if not copies:s=s.replace('CMP AL,1\nJE MOVREG\n','')
 return s

def data_items(words=False):
 s=BLOCK['DATAITEM']
 if not words:
  a=s.index('MOV DL,[OP]\n');b=s.index('DATASEP:\n',a)
  s=s[:a]+'CALL BYTEVALUE\n'+s[b:]
 return s

def define(spelling=False):
 if not spelling:return BLOCK['DEFINE']
 return '''DEFINE:
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
JE SPELLGOOD
MOV AX,3
JMP ERROR
SPELLGOOD:
RET
'''

STAGES=[]
def add(title,description,why,explain,main,*,names=(),variants=None,fixture=None,payload='',image=None,bad=None,executable=None,cartoon=None):
 STAGES.append(dict(title=title,description=description,why=why,explain=explain,main=main,names=list(names),variants=variants or {},fixture=fixture,payload=payload,image=image,bad=bad,executable=executable,cartoon=cartoon))
add('A message from assembly','A short DOS program, built with the BASIC assembler.',
'The BASIC construction gave us an assembler. Our first assembly-language program will use it to display a message and return to DOS.',
'''The source uses the same MOV, CALL, RET, and INT forms accepted by BOOTASM. DX receives the offset of HELLOMSG. DOS function 09H displays its bytes until it reaches the dollar-sign code 36; the 13 and 10 move the cursor to the next line. The dollar sign is a terminator, not part of the displayed message.

TEXT is a small subroutine with DX as its input. It changes AH and the flags DOS leaves behind; DOS may also return a value in AL. It does not save AX, because the caller has no AX value to retain. CALL pushes a two-byte return offset and RET takes it back. GOOD then uses function 4CH with a zero return code.

The labels name offsets beginning at 0100H. Neither ORG nor a segment directive is needed or accepted. Each DB item is an ASCII character code, and the BASIC assembler writes the machine bytes without a file header.''',
 driver('MOV DX,HELLOMSG\nCALL TEXT',memory=False),payload='ASM0\r\n')
add('Numbers in the report','Display an unsigned word without a divide instruction.',
'An assembly-language tool needs to report counts. We shall print an unsigned word as five decimal digits using repeated subtraction.',
'''NUMBER takes its value in AX and preserves every word register. The five PUSH instructions save AX, BX, CX, DX, and SI; the POP instructions restore them in reverse order. DI and BP are not touched. The routine uses ten stack bytes for its saved registers, in addition to its return address.

CX holds the amount still to be displayed. SI points at a table of word divisors: 10000, 1000, 100, 10, and 1. BX copies that pointer because our assembler accepts a word load through BX. For each divisor, AL begins with the code for 0. Repeated subtraction advances the digit until CX is smaller than the divisor.

Function 02H displays the character in DL. The arithmetic remainder stays in CX, because DOS may change AL. All five places are printed, including leading zeroes; this makes the routine small and keeps zero unambiguous. The tests show the low bound, a middle value, and the largest unsigned word. DIVEND names the byte just after the divisor table and emits no data.''',
 driver('MOV AX,0\nCALL NUMBER\nMOV DX,NEWLINE\nCALL TEXT\nMOV AX,1000\nCALL NUMBER\nMOV DX,NEWLINE\nCALL TEXT\nMOV AX,65535\nCALL NUMBER\nMOV DX,NEWLINE\nCALL TEXT',memory=False),payload='00000\r\n01000\r\n65535\r\n')
add('A clear failure report','A source line, an error code, and a DOS failure status.',
'A tool must make failure visible. We shall add one exit which reports a line number and a reason code, and establish the memory required by this workbench.',
'''ERROR takes a small reason code in AX. It saves AL in ERRCODE before displaying any text, then prints ERROR, the five-digit LINENO value, and CODE followed by the reason digit. It finishes with DOS function 4CH and return code one. DOS closes the process's files on termination.

The line number is zero when no source line has been read. Codes 1 through 7 distinguish syntax, values, symbols, range, capacity, file input/output, and memory respectively; the full reference gives their exact use. NUMBER preserves AX and its other saved registers, while TEXT may change AX. Saving the reason first is therefore necessary.

The entry check requires SP=FFFEH, the normal stack pointer for a .COM program given a full 64 KB segment. Our working buffers will use fixed offsets within that segment. Refusing a smaller segment is simpler than relocating all those buffers. Code 7 is a real workbench limit, not a claim that every DOS program needs 64 KB.

To exercise the rejection exit on an otherwise roomy machine, save a separate copy as SMALL.ASM and insert MOV SP,8000H immediately before CMP SP,0FFFEH. This leaves ample stack space for the report but deliberately fails the entry check. Build SMALL with BOOTASM and run CHECK SMALL: it must display ERROR 00000 CODE 7 and FAIL. Keep the normal checkpoint unchanged.''',
 driver('MOV DX,READYMSG\nCALL TEXT'),payload='READY\r\n',bad={'kind':'stack','line':0,'code':7})
add('Opening and closing a file','Let DOS return a handle, and check carry immediately.',
'A filename is useful only if DOS can open it. We shall open an existing source file for input and close its handle before returning.',
'''FNAME contains the zero-terminated name SOURCE.ASM. Use COPY to select a source before running the assembler; no console input is read. OPENFILE passes FNAME in DS:DX to DOS function 3DH with AL=0 for read-only access. On success AX is the handle, a small number which DOS uses to identify the open file. HANDLE retains it. The carry flag reports an error; JAE takes the carry-clear success path, while the near jump reaches FILEBAD on failure.

CLOSEFILE loads the saved handle into BX and uses function 3EH. Its carry result is checked before another operation can replace it. FILEBAD selects code 6 and reaches the common report. Neither routine returns after an error.

OPENFILE changes AX, DX, the flags, and HANDLE. CLOSEFILE uses BX and AH and changes the flags DOS returns. They do not read or interpret file contents. This checkpoint reports Opened only after both calls succeed. The missing-file test is useful: the existence of a filename in memory is not evidence that a disk file was opened.''',
 driver('CALL OPENFILE\nCALL CLOSEFILE\nMOV DX,OPENMSG\nCALL TEXT'),fixture='DB 65\r\n',payload='Opened\r\n',bad={'kind':'missing','line':0,'code':6})
add('Reading one byte','A handle-based read distinguishes data from end of file.',
'We shall read the source a byte at a time and display exactly the bytes read. This isolates file input from parsing.',
'''NEXTBYTE requests one byte with DOS function 3FH: BX is HANDLE, CX is one, and DS:DX points at CHAR. Carry indicates a file error. With carry clear, AX is the number of bytes read: one for a character, zero for end of file. CHAR is meaningful only when AX is one.

The routine changes AX, BX, CX, DX, and flags. It preserves the index registers, which lets a line-building loop keep its destination pointer while requesting another byte. A failed read selects code 6.

The driver checks AX before copying CHAR to DL for display. Function 02H may change AL, but the next read returns a new count. CLOSEFILE runs after the zero count. Reading one byte per DOS call is deliberately simple and can be slow on a long source file; it avoids a second buffered-input mechanism while the parser is being constructed.

At this checkpoint no case conversion or comment handling is performed. The source is displayed as text, not executed. A zero-byte input produces no copied characters and still returns successfully.''',
 driver('CALL OPENFILE\nDUMPBYTE:\nCALL NEXTBYTE\nCMP AX,0\nJE DUMPEND\nMOV DL,[CHAR]\nMOV AH,2\nINT 21H\nJMP DUMPBYTE\nDUMPEND:\nCALL CLOSEFILE'),fixture='Abc\r\n',payload='Abc\r\n',bad={'kind':'missing','line':0,'code':6})
add('Physical source lines','Bound each line and handle CR, LF, and the last line at EOF.',
'A parser needs complete source lines. We shall collect a line in a fixed buffer and return an explicit end-of-file indication.',
'''READLINE stores text at 2200H, followed by a zero byte. DI is the next free destination; BP counts physical characters. AX=1 means a line is ready and AX=0 means there is no more source. The routine changes the ordinary working registers and the ENDED, SKIPLF, and LINENO fields.

A carriage return finishes a line and sets SKIPLF. A following line feed is consumed without creating a second empty line. A bare line feed also finishes a line. Control-Z and a zero-byte read set ENDED. If characters preceded that ending, they form one last line; otherwise the routine returns zero immediately.

Tabs become spaces and lowercase ASCII letters become uppercase. Other control bytes and bytes above 126 are rejected as file/text errors. Comments still occupy physical buffer space; their semicolon is interpreted by the token reader, not discarded here.

The limit is 120 physical characters per line and 4,000 physical lines per input. The extra zero byte fits in the reserved buffer. READFAIL advances the report to the line which could not be completed. Once a complete line has been accepted, LINENO is its one-based physical line number.

The diagnostic driver prints each completed line with ZTEXT. It is a text reader, not an assembler. Blank lines are visible as blank display lines, and a final line without CR/LF is still displayed once.''',
 driver(READLOOP+'MOV SI,2200H\nCALL ZTEXT\nMOV DX,NEWLINE\nCALL TEXT\n'+CLOSELOOP),fixture='one\r\ntwo\r\n',payload='ONE\r\nTWO\r\n',bad={'kind':'source','text':'X'*121+'\r\n','line':1,'code':5})
add('Taking the line apart','Words and punctuation become bounded tokens.',
'We shall give the parser one word or punctuation mark at a time, while retaining a cursor into the current line.',
'''SCAN takes SI as the current position in the zero-terminated line. It skips spaces and returns one token at 2300H, a zero byte after it, and its length in TOKLEN. SI remains at the next separator or at the end marker. A zero token length means end of statement. The routine changes AX and DI as well as SI and TOKLEN.

Comma, colon, and square brackets are single-character tokens. A punctuation mark encountered after a word is put back by decrementing SI so the next call can return it separately. A semicolon means the rest of the line is a comment. Neither a zero byte nor a semicolon is consumed past the statement's end, so another call still sees an empty token.

A token may contain at most sixteen characters. The bound is checked before storing another character; its terminating zero occupies the seventeenth byte. This limit is independent of the 120-character physical-line limit. Quoted strings are not recognized.

The driver displays each token between brackets. It saves SI while ZTEXT walks the token buffer, then restores the line cursor. Without that saved cursor, the next SCAN would continue inside the token instead of the source line. This test separates token boundaries from their eventual meaning.''',
 driver(READLOOP+'''TRACETOKEN:
CALL SCAN
MOV AL,[2300H]
CMP AL,0
JE DRIVERLINE
MOV DL,91
MOV AH,2
INT 21H
PUSH SI
MOV SI,2300H
CALL ZTEXT
POP SI
MOV DL,93
MOV AH,2
INT 21H
MOV DX,NEWLINE
CALL TEXT
JMP TRACETOKEN
DRIVERDONE:
CALL CLOSEFILE
'''),fixture='db 1,2 ; a note\r\n',payload='[DB]\r\n[1]\r\n[,]\r\n[2]\r\n',bad={'kind':'source','text':'ABCDEFGHIJKLMNOPQ\r\n','line':1,'code':1})
add('Looking up a table entry','Compare a token with fixed-size records.',
'Instruction names and register names belong in small tables. We shall write one search routine and test it with two records.',
'''LOOK takes BX as the first record, CX as the record count, and AX as the record size in bytes. Each record begins with a zero-terminated name. It returns the matching record's address in BX, or zero if no record matches. It preserves SI, the source cursor, and changes AX, BX, CX, DX, DI, BP, STRIDE, and flags.

BP retains the current record's base while DI walks its name. The token is compared from its beginning for every candidate. Both names must reach zero together, so DB cannot match a longer prefix. On a mismatch the saved stride advances BP to the next record and the count is reduced.

The demonstration table uses eight-byte records: six bytes for a short name and its zero padding, then a class byte and a parameter byte. DB's parameter is zero; DW's is one. This is a table test, not yet a parser for either directive. The driver prints the parameter after a successful lookup and rejects an absent name.

The search count is checked before reading a record, including a count of zero. The routine uses two stack bytes for its saved SI, in addition to its return address. Keeping the stride in STRIDE is safe here because LOOK does not call itself or another LOOK while a search is active.''',
 driver(READLOOP+'''CALL SCAN
MOV BX,OPTAB
MOV CX,2
MOV AX,8
CALL LOOK
CMP BX,0
JNE TRACEFOUND
MOV AX,1
JMP ERROR
TRACEFOUND:
ADD BX,7
MOV AL,[BX]
MOV AH,0
PUSH AX
CALL FINISH
POP AX
CALL NUMBER
MOV DX,NEWLINE
CALL TEXT
'''+CLOSELOOP),names=['DB','DW'],fixture='DB\r\nDW\r\n',payload='00000\r\n00001\r\n',bad={'kind':'source','text':'UNKNOWN\r\n','line':1,'code':1},cartoon='asm86-postroom.png')
NUMACTION='PUSH AX\nCALL FINISH\nPOP AX\nCALL NUMBER\nMOV DX,NEWLINE\nCALL TEXT'
add('Unsigned decimal values','Check every digit before multiplying the accumulated value.',
'A token of decimal digits must become a word without accepting a sign, an expression, or an overflow.',
'''VALUE takes the token at 2300H and returns its unsigned value in AX. It preserves the source cursor SI by saving it on the stack. The numeric work uses CX as the accumulated value, DX as the next digit, and DI as the end of the token. AX, BX, CX, DX, DI, BP, and flags are scratch state.

Each character must lie between the codes for 0 and 9. Before multiplying, the accumulated value must be below 6553, or exactly 6553 with a final digit no greater than five. That check admits 65535 and rejects the next value before arithmetic can wrap.

Multiplication by ten is eight times the old value plus twice the old value. ADD performs those doublings with instructions BOOTASM already accepts. This keeps the routine's implementation vocabulary small; it does not imply the CPU lacks a multiply instruction.

The diagnostic driver reads one number per line. It saves AX while FINISH checks that no extra token follows, then prints the result. Empty values, malformed digits, and overflow select code 2. Only decimal numbers are accepted by this checkpoint.''',
 value_driver(NUMACTION),variants={'VALUE':numeric()},fixture='42\r\n65535\r\n',payload='00042\r\n65535\r\n',bad={'kind':'source','text':'65536\r\n','line':1,'code':2})
add('Hexadecimal values','A final H selects base sixteen; a leading digit keeps names distinct.',
'We shall extend VALUE to recognize hexadecimal while retaining the same unsigned-word result and overflow checks.',
'''The final character is examined before the digit loop. H selects base sixteen and is excluded from the digits to be read. Otherwise BP remains ten. A value must still begin with a decimal digit: write 0FFH, not FFH.

Characters A through F become values ten through fifteen. The digit must be smaller than the selected base, so a letter in a decimal token is rejected. Before a hexadecimal step, CX must be no greater than 4095. Four doublings then multiply it by sixteen, and the checked digit is added.

VALUE's input, result, preserved SI, and scratch registers are unchanged. No BASIC-style prefixes, signed literals, character constants, or expression arithmetic are added. A hexadecimal word is simply another way to write a number from zero through 65535.''',
 value_driver(NUMACTION),variants={'VALUE':numeric(True)},fixture='0FFH\r\n1234H\r\n',payload='00255\r\n04660\r\n',bad={'kind':'source','text':'0GH\r\n','line':1,'code':2})
add('Collecting output bytes','Count loaded offsets while retaining bytes in a separate buffer.',
'We shall collect byte values in memory before opening any output file. An invalid source must not be mistaken for a new program.',
'''PC begins at 0100H, the loaded address of the first .COM byte. OUTPTR begins at 6000H, the location of the output buffer in the assembler's own segment. These are different addresses with different purposes. Every emitted byte advances both by one.

EMIT takes the byte in AL and preserves AX and BX. On pass two it stores the byte at OUTPTR; on pass one it only counts. The current driver sets PASS to two. The 2100H limit on PC allows 8192 output bytes and refuses the next byte before storing beyond the buffer.

BYTEVALUE takes a full value in AX. Values above 255 select code 4; otherwise it enters EMIT. The caller therefore cannot accidentally truncate a word into a byte. EMIT selects code 5 if the image is full. Its nested PUSH instructions use four stack bytes in addition to the call's return address.

This checkpoint accepts one numeric byte value per line, checks the end of each statement, and reports the count collected. It writes no .COM file yet. The distinction lets us test conversion and capacity without disk-output behavior.''',
 value_driver('CALL BYTEVALUE\nCALL FINISH',buffer=True),variants={'VALUE':numeric(True)},fixture='65\r\n66\r\n',payload='Buffered 00002 bytes\r\n',bad={'kind':'source','text':'256\r\n','line':1,'code':4})
add('Writing the image','Create the output only after every source line succeeds.',
'The byte buffer is ready to become a file. We shall create a fresh .COM image and check both the write count and the close.',
'''WRITEOUT passes the fixed RESULT.COM name at RESNAME to DOS function 3CH. CX=0 requests an ordinary file. Creation truncates an existing file exactly; there is no BASIC sequential-file end marker or .COM header.

The returned handle goes in BX. For function 40H, CX is PC minus 0100H and DS:DX points to the buffer at 6000H. Carry reports a write error; with carry clear AX must equal the requested count. A short write is an error even though carry was clear. The final close is checked as well.

Only a completed write and close produce OK followed by the five-digit byte count. WRITEOUT changes working registers; it returns to the driver's successful termination. A zero-byte image creates a genuine empty file, which is valid for inspection but not execution.

Input errors leave an older output untouched because creation has not occurred. A disk error after creation can leave an empty or partial output; require a fresh OK report. The source is still one numeric byte per line at this checkpoint.''',
 value_driver('CALL BYTEVALUE\nCALL FINISH',buffer=True,write=True),variants={'VALUE':numeric(True)},fixture='65\r\n66\r\n',image='41 42',bad={'kind':'source','text':'256\r\n','line':1,'code':4})
add('The DB directive','Look up a mnemonic, then read its comma-separated byte values.',
'We shall replace the one-number-per-line input with an assembly statement: DB followed by one or more byte values.',
'''STATEMENT takes SI at the beginning of a cleaned line. An empty token is an empty statement. Otherwise LOOK searches OPTAB, now containing the DB record. The record supplies TYPE, which selects the handler, and OP, its small parameter. The record count is an explicit part of the search.

A conditional branch reaches a nearby test label; CALL reaches the handler without the short branch's distance limit. The handler returns through STATEMENT to the source loop. This dispatcher changes the parser's working registers and TYPE and OP.

DATAITEM scans a value, converts it, and sends it through BYTEVALUE. It then scans either a comma, which requests another value, or the empty token at the end of the statement. A trailing comma requests a missing value and is rejected. Comments and spaces are handled by the existing reader and scanner.

The first complete byte statement can now hold a row of data. Unknown mnemonics and unexpected separators select syntax code 1. The output remains buffered until the source succeeds.''',
 assembler_main(),names=['DB'],variants={'VALUE':numeric(True),'STATEMENT':statement(['DB']),'DATAITEM':data_items()},fixture='DB 41H,42H,43H\r\n',image='41 42 43',bad={'kind':'source','text':'NOPE 1\r\n','line':1,'code':1})
add('The DW directive','A word is two bytes, low byte first.',
'DW adds a word-sized data item without changing the meaning of DB or the value reader.',
'''OPTAB gains the DW record, with class one and parameter one. DATAITEM uses that parameter to choose BYTEVALUE or EMITWORD. The dispatcher still calls the same data handler.

EMITWORD takes AX, saves it, emits AL, copies AH into AL, emits the high byte, and restores AX. EMIT itself preserves AX, so the high byte survives the first call. The routine changes PC and OUTPTR, and uses two additional stack bytes for its saved word.

The order is little-endian: 1234H becomes 34 12. No alignment byte is inserted between adjacent directives. DW permits 65535; DB still rejects a value above 255. The native assembler's buffer can hold 8192 bytes, but each item must fit its selected width.''',
 assembler_main(),names=['DB','DW'],variants={'VALUE':numeric(True),'STATEMENT':statement(['DB','DW']),'DATAITEM':data_items(True)},fixture='DW 1234H,65535\r\nDB 0\r\n',image='34 12 FF FF 00',bad={'kind':'source','text':'DB 256\r\n','line':1,'code':4})
add('Reading the source twice','Reopen the source and reproduce the same instruction positions.',
'We shall count the source on pass one and collect its bytes on pass two, while all values are still numeric.',
'''PASS begins at one. PASSSTART resets PC, OUTPTR, LINENO, ENDED, and SKIPLF before reopening the source. A closed input handle is not reused as though its file position had reset; OPENFILE obtains a fresh handle.

EMIT already knows the pass convention. It performs range and capacity checks in either pass, but only pass two writes the output buffer. Every accepted form has a fixed length, so both passes must advance PC in the same way.

After a successful close, PASS is increased. A value below three repeats the source; otherwise the completed buffer is written. Only one output file and one OK report are produced. Do not edit a source while the assembler is processing it.

The visible byte check is deliberately unchanged. Reading twice must not duplicate the data or append an old file tail.''',
 assembler_main(two=True),names=['DB','DW'],variants={'VALUE':numeric(True),'STATEMENT':statement(['DB','DW']),'DATAITEM':data_items(True)},fixture='DW 1234H\r\nDB 65\r\n',image='34 12 41',bad={'kind':'source','text':'DW 65536\r\n','line':1,'code':2})
# Shared assembly-language features grow from here; each specification is cumulative.
FEATURES=['DB','DW']
def spec(*,labels=False,stored=False,reserved=True,symbolic=False,copies=False,memory=False,math=False):
 variants={'VALUE':numeric(True,reserved,symbolic),'STATEMENT':statement(FEATURES,labels),'DATAITEM':data_items(True)}
 if labels:variants['DEFINE']=define(spelling=not stored)
 if 'MOV' in FEATURES:
  variants.update(OPERAND=operand(memory),TWOOPERANDS=two_operands(math,memory),MOVOPERANDS=mov_operands(copies,memory))
 return dict(main=assembler_main(True,stored),names=FEATURES.copy(),variants=variants)
add('Recognizing register names','A four-byte dictionary distinguishes registers from values.',
'Register names must be recognizable before they can be used as operands or rejected as labels. We shall add their small dictionary to the token lookup.',
'''REGTAB contains sixteen four-byte records: two name characters, a zero, and an encoding number. Codes zero through seven denote byte registers AL, CL, DL, BL, AH, CH, DH, and BH. Codes eight through fifteen denote word registers AX, CX, DX, BX, SP, BP, SI, and DI.

REGISTER calls LOOK with that table and stride four. On a match it returns the code in AX; on a miss it returns FFFFH. It preserves SI through LOOK and changes the lookup scratch registers. Zero is a real code for AL, so FFFFH is the unambiguous miss result.

For this checkpoint, a recognized register in a data value is rejected with symbol code 3; another nonnumeric token remains a value error. Registers are not data constants. This exercises the dictionary without yet claiming support for MOV or other register instructions.''',
 **spec(reserved=True),fixture='DB 65\r\n',image='41',bad={'kind':'source','text':'DW AX\r\n','line':1,'code':3})
add('Checking a label line','Accept a standalone name and reject malformed or reserved spellings.',
'A label has a syntax of its own. We shall recognize that syntax before giving definitions storage in a symbol table.',
'''After the first token, STATEMENT looks past spaces for a colon. A colon selects DEFINE; otherwise the cursor is put back at the first operand character and mnemonic lookup proceeds normally. FINISH requires the label to occupy the statement by itself. A comment may follow it.

VALIDNAME accepts one through sixteen characters: letters, digits, and underscores, with a letter or underscore first. SCAN already enforces the length. The routine preserves SI and changes AL, flags, and the lookup scratch state used by REGISTER. Register names are reserved.

At this stopping point DEFINE checks spelling and returns without storing an address. Label lines emit no bytes, but labels are not yet accepted as values and duplicate definitions are not detected. Keeping that distinction explicit makes the spelling and statement-boundary checks observable on their own.''',
 **spec(labels=True,reserved=True),fixture='START:\r\nDB 65\r\n',image='41',bad={'kind':'source','text':'1BAD:\r\nDB 0\r\n','line':1,'code':3})
add('Recording an address','Store up to 256 names in fixed twenty-byte records.',
'We shall retain each valid definition with the loaded offset of its next byte, and check the same position on the second pass.',
'''SYMC counts the records in use and SYMNEXT points at the next free slot, initially 3000H. A symbol record occupies twenty bytes: seventeen bytes for a name and zero terminator, one padding byte, and a word value at offset eighteen. The table's 256 records occupy 3000H through 43FFH.

DEFINE validates the token, refuses a register name, and searches the existing records. On pass one a match is a duplicate error. Otherwise COPYZ writes the name, PC supplies the word value, SYMNEXT advances by twenty, and SYMC advances by one. A full table selects capacity code 5 before another record is written.

Pass two does not enter definitions again. It requires each name to exist and its retained value to equal the current PC. This detects an inconsistent definition rather than silently changing the table. SYMC and SYMNEXT are initialized once, outside PASSSTART, so the first-pass table survives reopening the source.

Only names and their addresses are being recorded here; data operands remain numeric. The byte result demonstrates that definitions themselves occupy no space. A repeated definition must now be rejected.''',
 **spec(labels=True,stored=True,reserved=True),fixture='START:\r\nDB 65\r\nEND:\r\n',image='41',bad={'kind':'source','text':'AGAIN:\r\nDB 1\r\nAGAIN:\r\n','line':3,'code':3})
add('Using a named value','Resolve forward references on the collecting pass.',
'A saved address can replace a hand-counted number. We shall let VALUE use a label, including one defined farther down the source.',
'''A token beginning with a decimal digit remains a number. Other tokens enter SYMBOLVALUE, which validates the name, rejects register names, and searches the symbol table. A match returns the word at record offset eighteen in AX.

An unknown name returns zero only during pass one. The width of every statement is fixed, so that placeholder changes no positions. On pass two an unknown name is a symbol error, code 3. The output file has not been opened at that point.

VALUE still preserves SI. The symbol path may change the lookup scratch registers, including BX, CX, DX, DI, and BP. A caller must not keep a live loop count in those registers without saving it.

Our test emits a word before the byte it names. TEXT therefore has loaded offset 0102H. A named address is an ordinary unsigned value: DW can hold it, while DB rejects a value above 255. Expressions such as TEXT+1 remain outside the language.''',
 **spec(labels=True,stored=True,symbolic=True),fixture='DW TEXT\r\nTEXT:\r\nDB 65\r\n',image='02 01 41',bad={'kind':'source','text':'DW MISSING\r\n','line':1,'code':3})
FEATURES+=['RET','CLD','LODSB','STOSB']
add('Fixed instruction bytes','Five no-operand mnemonics use the same table dispatcher.',
'We shall add machine instructions whose complete encodings are one fixed byte each.',
'''The new OPTAB records have class two and carry their opcode in the parameter byte. FIXED sends that byte through EMIT, then calls FINISH to reject an extra operand.

RET is the near return C3H. CLD is FCH and selects increasing indexes for string instructions. LODSB, ACH, loads AL from DS:SI and adjusts SI; STOSB, AAH, stores AL at ES:DI and adjusts DI. Their direction depends on the direction flag. They are plain, single instructions; no repeat prefix is accepted.

FIXED changes AL, PC, OUTPTR, and the scanner scratch state. It receives its opcode through OP and its argument cursor through SI. These encodings do not make the fixture safe to execute: its stack and index registers have not been prepared. Inspect the bytes only.''',
 **spec(labels=True,stored=True,symbolic=True),fixture='RET\r\nCLD\r\nLODSB\r\nSTOSB\r\n',image='C3 FC AC AA',bad={'kind':'source','text':'RET 1\r\n','line':1,'code':1})
FEATURES+=['MOV']
add('A register and an immediate','Determine MOV size from its destination register.',
'We shall add MOV with a register destination and a numeric or named immediate value.',
'''OPERAND scans one operand and tries REGISTER first. A register code supplies its number, REG, and width, WIDTH: zero for byte or one for word. KIND=1 identifies a register. A token which is not a register is read through VALUE and stored in VAL with KIND=3. The source cursor SI remains just after the operand.

TWOOPERANDS saves the first kind, width, and register in K1, W1, and R1. It then requires a comma and reads the second operand into the ordinary result fields. Those saved fields prevent the second lookup from destroying the destination description.

For this form, MOVOPERANDS requires a register first and an immediate second. The opcode is B0H plus the byte register number, or B8H plus the word register number. TIMES8 supplies the width contribution with three doublings. IMMEDVALUE reads VAL and chooses BYTEVALUE or EMITWORD from W1.

The routine changes the operand fields, parser scratch registers, and output state. A byte destination rejects values above 255. Register-to-register MOV is not accepted at this checkpoint. The source uses the same small instruction vocabulary as the routines it constructs; no extra assembler is involved.''',
 **spec(labels=True,stored=True,symbolic=True),fixture='MOV AL,41H\r\nMOV AX,1234H\r\n',image='B0 41 B8 34 12',bad={'kind':'source','text':'MOV AL,256\r\n','line':1,'code':4})
add('Two register operands','Put destination and source numbers into ModR/M.',
'We shall let MOV copy between registers of equal width, using the saved first operand and the newly read second operand.',
'''KIND=1 for the second operand selects MOVREG. SAMEWIDTH compares W1 with WIDTH and selects syntax code 1 if a byte and a word register were mixed. No extension or truncation rule is implied.

The opcode is 8AH for byte registers and 8BH for word registers. REGMOD constructs the second byte: 192 for mode 11, eight times the destination number R1 for bits 5-3, and the source number REG for bits 2-0. Thus MOV AX,BX is 8B C3.

TIMES8 changes only AL and flags. SAMEWIDTH changes AL, DL, and flags; the caller reloads the value needed for encoding afterward. EMIT preserves AX and BX, so emitting the opcode does not destroy the saved operand fields. As before, MOV itself does not change arithmetic flags when the assembled program runs.''',
 **spec(labels=True,stored=True,symbolic=True,copies=True),fixture='MOV AX,BX\r\nMOV DL,AL\r\nMOV CH,BH\r\n',image='8B C3 8A D0 8A EF',bad={'kind':'source','text':'MOV AX,AL\r\n','line':1,'code':1})
FEATURES+=['INC','DEC','PUSH','POP']
add('Single-register families','Increment, decrement, save, and restore a word register.',
'Four instruction families use the same register-number calculation and one-byte output.',
'''The class-five records carry bases 40H, 48H, 50H, and 58H for INC, DEC, PUSH, and POP. SINGLE reads a register and accepts only codes eight through fifteen, the word-register half of REGTAB. Subtracting eight recovers the processor's register number.

INC and DEC change a word by one with wraparound and preserve carry. PUSH subtracts two from SP and stores a word at SS:SP. POP reads a word and advances SP; neither instruction changes arithmetic flags. Every ordinary saved word must be balanced before a return.

SINGLE changes the scanner and lookup scratch registers, AL, output state, and flags used by the assembler. FINISH refuses a second operand. Byte INC/DEC, memory forms, and immediate PUSH are excluded. PUSH SP has the original 8086/8088 behavior of storing the decremented SP; avoid it in ordinary saved-register code. POP SP also changes the stack pointer itself.''',
 **spec(labels=True,stored=True,symbolic=True,copies=True),fixture='INC BX\r\nDEC CX\r\nPUSH AX\r\nPOP DX\r\n',image='43 49 50 5A',bad={'kind':'source','text':'INC AL\r\n','line':1,'code':1})
FEATURES+=['INT']
add('Assembling a DOS request','Emit CDH and a checked interrupt number.',
'A source program can now prepare registers. We shall add INT so a complete assembled program can display a character and terminate through DOS.',
'''INTERRUPT reads one value, saves AX while it emits CDH, then passes the restored value through BYTEVALUE. That bound check is essential: the interrupt number occupies one byte. FINISH rejects another token.

In the test, DL holds Z and AH holds function 02H. INT 21H displays the character. Loading AX with 4C00H then requests function 4CH with a zero return code in AL. The source is a complete executable, unlike the earlier encoding fixtures.

INTERRUPT changes VALUE's scratch registers, AX, PC, OUTPTR, and flags. Its temporary saved AX costs two stack bytes. The interrupt instruction itself causes the processor to save flags, CS, and IP while the service runs; the caller must use the documented DOS register interface, not treat a software interrupt as an ordinary subroutine.''',
 **spec(labels=True,stored=True,symbolic=True,copies=True),fixture='MOV DL,5AH\r\nMOV AH,2\r\nINT 21H\r\nMOV AX,4C00H\r\nINT 21H\r\n',image='B2 5A B4 02 CD 21 B8 00 4C CD 21',executable='Z',bad={'kind':'source','text':'INT 256\r\n','line':1,'code':4})
FEATURES+=['ADD','OR','AND','SUB','CMP']
add('Arithmetic and comparisons','Select a group number, register form, or full-width immediate.',
'Five related instruction families can share the operand reader and much of their encoding work.',
'''The class-four parameters are the processor's group numbers: ADD=0, OR=1, AND=4, SUB=5, and CMP=7. They are not a consecutive numbering invented by this assembler.

TWOOPERANDS requires a register destination. For a register source, SAMEWIDTH checks the widths and the opcode is eight times OP plus two plus W1. REGMOD supplies the ordinary two-register ModR/M byte.

For an immediate source, the opcode is 80H for a byte or 81H for a word. ModR/M is 192 plus eight times OP plus the destination register. IMMEDVALUE emits the full selected width. The shorter sign-extended 83H form is deliberately omitted, keeping instruction sizes independent of a value's eventual address.

ADD and SUB store their arithmetic result; CMP sets subtraction flags without storing it. AND and OR operate on corresponding bits. The assembled operations affect flags; the parser and encoding helpers also use flags internally, so the assembler saves state in fields rather than depending on a comparison across a helper call. Memory arithmetic and signed literal syntax remain excluded.''',
 **spec(labels=True,stored=True,symbolic=True,copies=True,math=True),fixture='ADD AX,BX\r\nSUB CX,1\r\nCMP AL,41H\r\nAND AL,0DFH\r\nOR BL,20H\r\n',image='03 C3 81 E9 01 00 80 F8 41 80 E0 DF 80 CB 20',bad={'kind':'source','text':'ADD AX,AL\r\n','line':1,'code':1})
add('Moving through memory','Use BX or one direct offset; let the register determine width.',
'We shall add bracketed MOV operands without adding an expression parser or the processor\'s entire addressing vocabulary.',
'''An opening bracket selects MEMORY. The inner token BX selects r/m=7; every other inner token is a value or label and selects r/m=6 with a direct word offset. A closing bracket is required. KIND=2 identifies memory, REG holds that r/m number, and VAL holds the direct offset when needed.

The first operand's value is now saved in V1 as well. For a load into a register, LOADMEM uses opcode 8AH or 8BH and ModR/M equal to eight times R1 plus the memory r/m number. A direct offset follows only for r/m=6.

For a store, STOREMEM requires a register source, uses 88H or 89H, and puts that register number in the middle field. V1 supplies a direct destination offset. The memory operand has no width of its own; the register on the other side supplies it.

These routines change the operand fields, VALUE and lookup scratch state, AL and DL, and output state. EMIT preserves DX, so the r/m number in DL survives while the instruction bytes are emitted. Memory-to-memory and immediate-to-memory MOV are rejected. Segment overrides, [SI], [BP], and indexed combinations are omitted to keep the grammar and record of instruction lengths small. The processor supports more than this source language accepts.''',
 **spec(labels=True,stored=True,symbolic=True,copies=True,memory=True,math=True),fixture='MOV AL,[BX]\r\nMOV [BX],AL\r\nMOV AX,[200H]\r\nMOV [200H],AX\r\n',image='8A 07 88 07 8B 06 00 02 89 06 00 02',bad={'kind':'source','text':'MOV [BX],1\r\n','line':1,'code':1})
FEATURES+=['CALL','JMP']
add('Near calls and jumps','Subtract the address after the three-byte instruction.',
'We shall assemble control transfers which remain in the current code segment, including a forward call to a named routine.',
'''Class seven carries E8H for CALL or E9H for JMP. NEARJUMP reads the destination, subtracts PC plus three, and emits the opcode and a word displacement. The 8086/8088 subtraction already wraps into the unsigned sixteen-bit pattern needed for a backward transfer.

CALL pushes the offset of the following instruction. RET takes that offset back from the stack; a routine must restore its own saved words first. JMP pushes nothing. Neither transfer changes arithmetic flags by itself, although a called routine may do so.

NEARJUMP preserves the computed displacement on the stack while emitting the opcode. It changes VALUE's scratch state, AX, DX, PC, OUTPTR, and flags. Every accepted near transfer is three bytes. Far calls, indirect transfers, and automatic short-JMP selection are omitted because this workbench uses one .COM segment and fixed instruction sizes.

The complete test calls SAY, which displays C, then returns to the termination code. SAY begins five bytes beyond the return address, so the CALL displacement is 0005H.''',
 **spec(labels=True,stored=True,symbolic=True,copies=True,memory=True,math=True),fixture='CALL SAY\r\nMOV AX,4C00H\r\nINT 21H\r\nSAY:\r\nMOV DL,43H\r\nMOV AH,2\r\nINT 21H\r\nRET\r\n',image='E8 05 00 B8 00 4C CD 21 B2 43 B4 02 CD 21 C3',executable='C',bad={'kind':'source','text':'CALL LOST\r\n','line':1,'code':3})
FEATURES+=['JB','JAE','JE','JNE','JBE','JA']
add('Short conditional branches','A signed byte selects a nearby path from the flags.',
'A comparison needs a way to select a path. We shall add the six short conditions and reject a destination outside their signed-byte reach.',
'''Class eight carries the condition opcode: 72H through 77H for unsigned comparisons. JE and JNE test equality for either interpretation. The reference gives the flag expressions for every accepted spelling.

SHORTJUMP subtracts PC plus two from the target. Pass one accepts a placeholder for an unknown name. Pass two accepts unsigned word results 0000H through 007FH or FF80H through FFFFH, the bit patterns for displacements zero through 127 or minus 128 through minus one. Any other result selects range code 4.

Only AL is emitted as the displacement byte. AX is saved while the opcode is emitted, then restored. VALUE's scratch registers, AX, DX, PC, OUTPTR, and flags may change. There is no silent widening or processor upgrade.

A distant conditional transfer must be written as the opposite nearby condition around a three-byte near JMP. That pattern is also visible in the assembler's own source wherever a shared error exit is farther away than a short branch can reach. A CALL can reach a handler without asking a conditional branch to span the whole handler.

The complete test displays 0, 1, and 2. CMP DL,33H sets the flags for JB; no flag-changing instruction lies between that comparison and its branch.''',
 **spec(labels=True,stored=True,symbolic=True,copies=True,memory=True,math=True),fixture='MOV DL,30H\r\nAGAIN:\r\nMOV AH,2\r\nINT 21H\r\nINC DX\r\nCMP DL,33H\r\nJB AGAIN\r\nMOV AX,4C00H\r\nINT 21H\r\n',image='B2 30 B4 02 CD 21 42 80 FA 33 72 F6 B8 00 4C CD 21',executable='012',bad={'kind':'source','text':'JE 400H\r\n','line':1,'code':4},cartoon='asm86-signals.png')

def render(stage):
 variants=stage['variants'];code={'START':stage['main']}
 owner={}
 for key,value in {**BLOCK,**variants}.items():
  for label in re.findall(r'^([A-Z][A-Z0-9_]*):$',value,re.M):owner[label]=key
 while True:
  refs=tokens('\n'.join(code.values()));defined=set(re.findall(r'^([A-Z][A-Z0-9_]*):$','\n'.join(code.values()),re.M))
  needed={owner[name] for name in refs-defined if name in owner and owner[name]!='START'}
  fresh=needed-set(code)
  if not fresh:break
  for key in fresh:code[key]=variants.get(key,BLOCK[key])
 source='; ASM86 construction checkpoint. Plain BOOTASM source.\n'+code['START']
 for key in ORDER:
  if key in code:source+='\n'+code[key]
 refs=tokens(source)
 for key in FIELDORDER:
  if key not in refs:continue
  if key=='OPTAB':
   rows=[line for name,row,line in records if name in stage['names']]
   assert len(rows)==len(stage['names']),(stage['title'],rows)
   source+='\nOPTAB:\n'+'\n'.join(rows)+'\n'
  else:source+='\n'+FIELDS[key]
 return source

manifest=[];previous=''
for number,stage in enumerate(STAGES,1):
 source=render(stage);filename=f'AS{number:02}.ASM'
 dos(WORK/filename,source)
 if stage['fixture'] is not None:dos(WORK/f'T{number:02}.ASM',stage['fixture'])
 if stage['bad'] and stage['bad']['kind']=='source':dos(WORK/f'X{number:02}.ASM',stage['bad']['text'])
 record={key:value for key,value in stage.items() if key not in ['main','variants']}
 record.update(number=number,source=filename,lines=len(source.splitlines()))
 manifest.append(record);previous=source
assert len(STAGES)==28
# The final checkpoint is the complete reader-facing source.
dos(WORK/'ASM86.ASM',previous)
(ROOT/'qa/asm0/checkpoints.json').write_text(json.dumps(manifest,indent=2))
print(f'Prepared {len(STAGES)} source checkpoints; final source {len(previous.splitlines())} lines.')
