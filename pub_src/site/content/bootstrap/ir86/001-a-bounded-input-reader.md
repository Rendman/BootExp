+++
title = "01 \u00b7 A bounded input reader"
weight = 1
description = "Read a fixed source through the inherited line reader and checked source counters."
download = "IR01.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/01-reading-an-ir-source/", "/bootstrap/ir86/037-iw-a-bounded-input-reader/"]
+++

Read a fixed source through the inherited line reader and checked source counters.

## Enter the source

Copy ASM86.ASM to IR01.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 2681

Unchanged source before the edit:

```asm
DW 15,16960,1,34464,0,10000
DW 0,1000,0,100,0,10
DW 0,1
```

Remove:

```asm

```

The following old source remains:

```asm
DIV32END:
```

### Edit at old physical position 2551

Unchanged source before the edit:

```asm
DB 0

CLEANFAIL:
```

Remove the complete old physical range 2551–2652. Its first source is:

```asm
DB 0

PREFIX:
```

Its last source is:

```asm
DB 0

REGFIELD:
```

Remove both boundaries and all source between them.

The following old source remains:

```asm
DB 0
```

### Edit at old physical position 2527

Unchanged source before the edit:

```asm
DW 0

OUTHANDLE:
```

Remove:

```asm
DW 0

ENDPC:
DW 0

SEGCODE:
```

The following old source remains:

```asm
DW 0
```

### Edit at old physical position 2514

Unchanged source before the edit:

```asm

RECOVERMSG:
DB 82,101,99,111,118,101,114,121,58,32,105,110,115,112,101,99
```

Remove:

```asm
DB 116,32,65,83,77,65,46,84,77,80,32,97,110,100,32,82
DB 69,83,85,76,84,46,66,65,75,13,10,36
```

Insert in its place:

```asm
DB 116,32,73,82,84,88,46,84,77,80,32,97,110,100,32,73
DB 82,82,69,83,46,66,65,75,13,10,36
```

The following old source remains:

```asm

RDPOS:
```

### Edit at old physical position 2510

Unchanged source before the edit:

```asm
DB 82,69,83,85,76,84,46,67,79,77,0

BAKNAME:
```

Remove:

```asm
DB 82,69,83,85,76,84,46,66,65,75,0
```

Insert in its place:

```asm
DB 73,82,82,69,83,46,66,65,75,0
```

The following old source remains:

```asm

RECOVERMSG:
```

### Edit at old physical position 2507

Unchanged source before the edit:

```asm
DB 65,83,77,65,46,84,77,80,0

RESNAME:
```

Remove:

```asm
DB 82,69,83,85,76,84,46,67,79,77,0
```

Insert in its place:

```asm
DB 82,69,83,85,76,84,46,65,83,77,0
```

The following old source remains:

```asm

BAKNAME:
```

### Edit at old physical position 2504

Unchanged source before the edit:

```asm
DB 83,79,85,82,67,69,46,65,83,77,0

TMPNAME:
```

Remove:

```asm
DB 65,83,77,65,46,84,77,80,0
```

Insert in its place:

```asm
DB 73,82,84,88,46,84,77,80,0
```

The following old source remains:

```asm

RESNAME:
```

### Edit at old physical position 2501

Unchanged source before the edit:

```asm
DB 74,67,0,0,0,0,8,114

SRCNAME:
```

Remove:

```asm
DB 83,79,85,82,67,69,46,65,83,77,0
```

Insert in its place:

```asm
DB 83,79,85,82,67,69,46,73,82,0
```

The following old source remains:

```asm

TMPNAME:
```

### Edit at old physical position 2442

Unchanged source before the edit:

```asm
ERRCODE:
DB 0
```

Remove the complete old physical range 2442–2499. Its first source is:

```asm
REGTAB:
DB 65,76,0,0
DB 67,76,0,1
```

Its last source is:

```asm
DB 83,72,82,0,0,0,10,5
DB 74,67,0,0,0,0,8,114
```

Remove both boundaries and all source between them.

The following old source remains:

```asm
SRCNAME:
DB 83,79,85,82,67,69,46,65,83,77,0
```

### Edit at old physical position 2415

Unchanged source before the edit:

```asm
CHAR:
DB 0
```

Remove:

```asm
TYPE:
DB 0

OP:
DB 0

KIND:
DB 0

WIDTH:
DB 0

REG:
DB 0

K1:
DB 0

W1:
DB 0

R1:
DB 0
```

The following old source remains:

```asm
ERRCODE:
DB 0
```

### Edit at old physical position 2396

Unchanged source before the edit:

```asm

STRIDE:
DW 0
```

Remove:

```asm

VAL:
DW 0

V1:
DW 0

PASS:
DB 1
```

The following old source remains:

```asm

ENDED:
```

### Edit at old physical position 2385

Unchanged source before the edit:

```asm
LINENO:
DW 0
```

Remove:

```asm
PC:
DW 256

SYMC:
DW 0
```

The following old source remains:

```asm
TOKLEN:
DW 0
```

### Edit at old physical position 2376

Unchanged source before the edit:

```asm

DIVISORS:
DW 10000,1000,100,10,1
```

Remove:

```asm

```

The following old source remains:

```asm
DIVEND:
```

### Edit at old physical position 2366

Unchanged source before the edit:

```asm
DB 32,98,121,116,101,115,13,10,36

ERRMSG:
```

Remove:

```asm
DB 69,82,82,79,82,32,36
```

Insert in its place:

```asm
DB 73,82,32,69,82,82,79,82,32,36
```

The following old source remains:

```asm

CODEMSG:
```

### Edit at old physical position 1879

Unchanged source before the edit:

```asm
POP AX
RET
```

Remove the complete old physical range 1879–2364. Its first source is:

```asm
ATOM:
MOV AL,[0CC00H]
CMP AL,48
```

Its last source is:

```asm
BYTEMSG:
DB 32,98,121,116,101,115,13,10,36
```

Remove both boundaries and all source between them.

The following old source remains:

```asm
ERRMSG:
DB 69,82,82,79,82,32,36
```

### Edit at old physical position 1869

Unchanged source before the edit:

```asm
INT 21H
ADD SI,4
CMP SI,DIV32END
```

Remove:

```asm
JAE ZNUMBER323
JMP N32PLACE
ZNUMBER323:
```

Insert in its place:

```asm
JB NEAR N32PLACE
```

The following old source remains:

```asm
POP SI
POP DX
```

### Edit at old physical position 1851

Unchanged source before the edit:

```asm
MOV DX,[D32LO]
SUB AX,DX
MOV [N32LO],AX
```

Remove:

```asm
JAE N32NOBORROW
```

Insert in its place:

```asm
JAE NEAR N32NOBORROW
```

The following old source remains:

```asm
MOV AX,[N32HI]
DEC AX
```

### Edit at old physical position 1843

Unchanged source before the edit:

```asm
MOV AX,[N32LO]
MOV DX,[D32LO]
CMP AX,DX
```

Remove:

```asm
JAE ZNUMBER322
JMP N32DIGIT
ZNUMBER322:
```

Insert in its place:

```asm
JB NEAR N32DIGIT
```

The following old source remains:

```asm
N32TAKE:
MOV AX,[N32LO]
```

### Edit at old physical position 1836

Unchanged source before the edit:

```asm
MOV AX,[N32HI]
MOV DX,[D32HI]
CMP AX,DX
```

Remove:

```asm
JAE ZNUMBER321
JMP N32DIGIT
ZNUMBER321:
JA N32TAKE
```

Insert in its place:

```asm
JB NEAR N32DIGIT
JA NEAR N32TAKE
```

The following old source remains:

```asm
MOV AX,[N32LO]
MOV DX,[D32LO]
```

### Edit at old physical position 1804

Unchanged source before the edit:

```asm
JNE INPUTLOW
MOV AX,[INBYTEHI]
CMP AX,0FFFFH
```

Remove:

```asm
JE COUNTFULL
```

Insert in its place:

```asm
JE NEAR COUNTFULL
```

The following old source remains:

```asm
INC AX
MOV [INBYTEHI],AX
```

### Edit at old physical position 1801

Unchanged source before the edit:

```asm
COUNTINPUT:
MOV AX,[INBYTES]
CMP AX,0FFFFH
```

Remove:

```asm
JNE INPUTLOW
```

Insert in its place:

```asm
JNE NEAR INPUTLOW
```

The following old source remains:

```asm
MOV AX,[INBYTEHI]
CMP AX,0FFFFH
```

### Edit at old physical position 1784

Unchanged source before the edit:

```asm
JNE LINELOW
MOV AX,[LINEHI]
CMP AX,0FFFFH
```

Remove:

```asm
JE COUNTFULL
```

Insert in its place:

```asm
JE NEAR COUNTFULL
```

The following old source remains:

```asm
INC AX
MOV [LINEHI],AX
```

### Edit at old physical position 1781

Unchanged source before the edit:

```asm
COUNTLINE:
MOV AX,[LINENO]
CMP AX,0FFFFH
```

Remove:

```asm
JNE LINELOW
```

Insert in its place:

```asm
JNE NEAR LINELOW
```

The following old source remains:

```asm
MOV AX,[LINEHI]
CMP AX,0FFFFH
```

### Edit at old physical position 1563

Unchanged source before the edit:

```asm
MOV AL,1
MOV [CLEANFAIL],AL
CLEANEND:
```

Remove the complete old physical range 1563–1775. Its first source is:

```asm
CALL MEMFREE
RET
```

Its last source is:

```asm
MOV BX,[BUCKET]
MOV AX,[SYMID]
MOV ES:[BX],AX
```

Remove both boundaries and all source between them.

The following old source remains:

```asm
RET
```

### Edit at old physical position 1559

Unchanged source before the edit:

```asm
MOV DX,TMPNAME
MOV AH,41H
INT 21H
```

Remove:

```asm
JAE CLEANEND
```

Insert in its place:

```asm
JAE NEAR CLEANEND
```

The following old source remains:

```asm
MOV AL,1
MOV [CLEANFAIL],AL
```

### Edit at old physical position 1555

Unchanged source before the edit:

```asm
JE CLEANEND
MOV AL,[KEEPFILES]
CMP AL,0
```

Remove:

```asm
JNE CLEANEND
```

Insert in its place:

```asm
JNE NEAR CLEANEND
```

The following old source remains:

```asm
MOV DX,TMPNAME
MOV AH,41H
```

### Edit at old physical position 1552

Unchanged source before the edit:

```asm
CLEANTEMP:
MOV AL,[OWNTMP]
CMP AL,0
```

Remove:

```asm
JE CLEANEND
```

Insert in its place:

```asm
JE NEAR CLEANEND
```

The following old source remains:

```asm
MOV AL,[KEEPFILES]
CMP AL,0
```

### Edit at old physical position 1546

Unchanged source before the edit:

```asm
MOV BX,[OUTHANDLE]
MOV AH,3EH
INT 21H
```

Remove:

```asm
JAE CLEANTEMP
```

Insert in its place:

```asm
JAE NEAR CLEANTEMP
```

The following old source remains:

```asm
MOV AL,1
MOV [CLEANFAIL],AL
```

### Edit at old physical position 1542

Unchanged source before the edit:

```asm
CLEANOUTPUT:
MOV AL,[OUTOPEN]
CMP AL,0
```

Remove:

```asm
JE CLEANTEMP
```

Insert in its place:

```asm
JE NEAR CLEANTEMP
```

The following old source remains:

```asm
MOV BX,[OUTHANDLE]
MOV AH,3EH
```

### Edit at old physical position 1536

Unchanged source before the edit:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

Remove:

```asm
JAE CLEANOUTPUT
```

Insert in its place:

```asm
JAE NEAR CLEANOUTPUT
```

The following old source remains:

```asm
MOV AL,1
MOV [CLEANFAIL],AL
```

### Edit at old physical position 1532

Unchanged source before the edit:

```asm
CLEANUP:
MOV AL,[INOPEN]
CMP AL,0
```

Remove:

```asm
JE CLEANOUTPUT
```

Insert in its place:

```asm
JE NEAR CLEANOUTPUT
```

The following old source remains:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
```

### Edit at old physical position 1521

Unchanged source before the edit:

```asm
MOV DX,BAKNAME
MOV AH,41H
INT 21H
```

Remove:

```asm
JAE BACKREMOVED
```

Insert in its place:

```asm
JAE NEAR BACKREMOVED
```

The following old source remains:

```asm
JMP FILEBAD
BACKREMOVED:
```

### Edit at old physical position 1517

Unchanged source before the edit:

```asm
MOV [OWNTMP],AL
MOV AL,[HAVEBAK]
CMP AL,0
```

Remove:

```asm
JE COMMITDONE
```

Insert in its place:

```asm
JE NEAR COMMITDONE
```

The following old source remains:

```asm
MOV DX,BAKNAME
MOV AH,41H
```

### Edit at old physical position 1503

Unchanged source before the edit:

```asm
MOV DI,RESNAME
MOV AH,56H
INT 21H
```

Remove:

```asm
JAE RESTORED
```

Insert in its place:

```asm
JAE NEAR RESTORED
```

The following old source remains:

```asm
MOV AL,1
MOV [KEEPFILES],AL
```

### Edit at old physical position 1498

Unchanged source before the edit:

```asm
ZCOMMIT1:
MOV AL,[HAVEBAK]
CMP AL,0
```

Remove:

```asm
JE PUBLISHFAIL
```

Insert in its place:

```asm
JE NEAR PUBLISHFAIL
```

The following old source remains:

```asm
MOV DX,BAKNAME
MOV DI,RESNAME
```

### Edit at old physical position 1493

Unchanged source before the edit:

```asm
MOV DI,RESNAME
MOV AH,56H
INT 21H
```

Remove:

```asm
JB ZCOMMIT1
JMP PUBLISHED
ZCOMMIT1:
```

Insert in its place:

```asm
JAE NEAR PUBLISHED
```

The following old source remains:

```asm
MOV AL,[HAVEBAK]
CMP AL,0
```

### Edit at old physical position 1483

Unchanged source before the edit:

```asm
MOV DI,BAKNAME
MOV AH,56H
INT 21H
```

Remove:

```asm
JAE BACKEDUP
```

Insert in its place:

```asm
JAE NEAR BACKEDUP
```

The following old source remains:

```asm
JMP FILEBAD
BACKEDUP:
```

### Edit at old physical position 1478

Unchanged source before the edit:

```asm
MOV DX,RESNAME
CALL EXISTS
CMP AX,0
```

Remove:

```asm
JE PUBLISH
```

Insert in its place:

```asm
JE NEAR PUBLISH
```

The following old source remains:

```asm
MOV DX,RESNAME
MOV DI,BAKNAME
```

### Edit at old physical position 1467

Unchanged source before the edit:

```asm
MOV DX,BAKNAME
CALL EXISTS
CMP AX,0
```

Remove:

```asm
JE PREFLIGHTOK
```

Insert in its place:

```asm
JE NEAR PREFLIGHTOK
```

The following old source remains:

```asm
NAMEBUSY:
MOV AX,8
```

### Edit at old physical position 1463

Unchanged source before the edit:

```asm
MOV DX,TMPNAME
CALL EXISTS
CMP AX,0
```

Remove:

```asm
JNE NAMEBUSY
```

Insert in its place:

```asm
JNE NEAR NAMEBUSY
```

The following old source remains:

```asm
MOV DX,BAKNAME
CALL EXISTS
```

### Edit at old physical position 1451

Unchanged source before the edit:

```asm
MOV BX,AX
MOV AH,3EH
INT 21H
```

Remove:

```asm
JAE EXISTSCLOSED
```

Insert in its place:

```asm
JAE NEAR EXISTSCLOSED
```

The following old source remains:

```asm
JMP FILEBAD
EXISTSCLOSED:
```

### Edit at old physical position 1445

Unchanged source before the edit:

```asm
INT 21H
JAE FILEEXISTS
CMP AX,2
```

Remove:

```asm
JE FILENONE
```

Insert in its place:

```asm
JE NEAR FILENONE
```

The following old source remains:

```asm
JMP FILEBAD
FILEEXISTS:
```

### Edit at old physical position 1443

Unchanged source before the edit:

```asm
EXISTS:
MOV AX,3D00H
INT 21H
```

Remove:

```asm
JAE FILEEXISTS
```

Insert in its place:

```asm
JAE NEAR FILEEXISTS
```

The following old source remains:

```asm
CMP AX,2
JE FILENONE
```

### Edit at old physical position 1388

Unchanged source before the edit:

```asm
MOV AX,4C01H
INT 21H
```

Remove the complete old physical range 1388–1439. Its first source is:

```asm
CREATEOUT:
MOV DX,TMPNAME
MOV CX,0
```

Its last source is:

```asm
POP AX
RET
```

Remove both boundaries and all source between them.

The following old source remains:

```asm
EXISTS:
MOV AX,3D00H
```

### Edit at old physical position 1381

Unchanged source before the edit:

```asm
MOV DL,[HAVEBAK]
OR AL,DL
CMP AL,0
```

Remove:

```asm
JE ERROREXIT
```

Insert in its place:

```asm
JE NEAR ERROREXIT
```

The following old source remains:

```asm
MOV DX,RECOVERMSG
CALL TEXT
```

### Edit at old physical position 1350

Unchanged source before the edit:

```asm
INT 21H
ADD SI,2
CMP SI,DIVEND
```

Remove:

```asm
JB NEXTPLACE
```

Insert in its place:

```asm
JB NEAR NEXTPLACE
```

The following old source remains:

```asm
POP SI
POP DX
```

### Edit at old physical position 1340

Unchanged source before the edit:

```asm
MOV AL,48
SUBTRACT:
CMP CX,DX
```

Remove:

```asm
JB PRINTDIGIT
```

Insert in its place:

```asm
JB NEAR PRINTDIGIT
```

The following old source remains:

```asm
SUB CX,DX
ADD AL,1
```

### Edit at old physical position 1318

Unchanged source before the edit:

```asm
LODSB
STOSB
CMP AL,0
```

Remove:

```asm
JNE COPYZ
```

Insert in its place:

```asm
JNE NEAR COPYZ
```

The following old source remains:

```asm
RET
```

### Edit at old physical position 1114

Unchanged source before the edit:

```asm
MOV AX,1
JMP ERROR
FINISHED:
```

Remove the complete old physical range 1114–1311. Its first source is:

```asm
RET

TWOOPERANDS:
```

Its last source is:

```asm
MOV [PC],BX
POP BX
POP AX
```

Remove both boundaries and all source between them.

The following old source remains:

```asm
RET
```

### Edit at old physical position 1110

Unchanged source before the edit:

```asm
CALL SCAN
MOV AL,[0CC00H]
CMP AL,0
```

Remove:

```asm
JE FINISHED
```

Insert in its place:

```asm
JE NEAR FINISHED
```

The following old source remains:

```asm
MOV AX,1
JMP ERROR
```

### Edit at old physical position 524

Unchanged source before the edit:

```asm
VALUEBAD:
MOV AX,3
JMP ERROR
```

Remove the complete old physical range 524–1104. Its first source is:

```asm

DEFINE:
CALL VALIDNAME
```

Its last source is:

```asm
POP AX
CALL EMIT
JMP FINISH
```

Remove both boundaries and all source between them.

The following old source remains:

```asm

FINISH:
```

### Edit at old physical position 426

Unchanged source before the edit:

```asm
POP SI
POP AX
RET
```

Remove the complete old physical range 426–522. Its first source is:

```asm
EXPRESSIONADD:
POP AX
CALL SCAN
```

Its last source is:

```asm
RET
VALUEBAD:
MOV AX,3
```

Remove both boundaries and all source between them.

Insert in its place:

```asm
NUMBERBAD:
MOV AX,2
```

The following old source remains:

```asm
JMP ERROR
```

### Edit at old physical position 424

Unchanged source before the edit:

```asm
CMP AL,45
JE EXPRESSIONSUB
POP SI
```

Remove:

```asm
POP AX
```

The following old source remains:

```asm
RET
EXPRESSIONADD:
```

### Edit at old physical position 417

Unchanged source before the edit:

```asm
EXPRESSIONLOOP:
PUSH AX
PUSH SI
```

Remove:

```asm
CALL SCAN
MOV AL,[0CC00H]
CMP AL,43
JE EXPRESSIONADD
CMP AL,45
JE EXPRESSIONSUB
```

Insert in its place:

```asm
MOV SI,0CC00H
MOV DI,[TOKLEN]
ADD DI,0CC00H
MOV BX,DI
DEC BX
MOV AL,[BX]
MOV BP,10
CMP AL,72
JNE NEAR NUMBERSTART
MOV BP,16
DEC DI
NUMBERSTART:
CMP SI,DI
JE NEAR NUMBERBAD
MOV CX,0
DIGIT:
LODSB
SUB AL,48
CMP AL,9
JBE NEAR DIGITOK
SUB AL,7
CMP AL,10
JB NEAR NUMBERBAD
CMP AL,15
JA NEAR NUMBERBAD
DIGITOK:
MOV AH,0
MOV DX,AX
CMP DX,BP
JAE NEAR NUMBERBAD
CMP BP,16
JE NEAR HEXDIGIT
CMP CX,6553
JA NEAR NUMBERBAD
JB NEAR DECDIGIT
CMP DX,5
JA NEAR NUMBERBAD
DECDIGIT:
MOV AX,CX
ADD CX,CX
ADD AX,AX
ADD AX,AX
ADD AX,AX
ADD CX,AX
JMP ADDDIGIT
HEXDIGIT:
CMP CX,4095
JA NEAR NUMBERBAD
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADDDIGIT:
ADD CX,DX
CMP SI,DI
JB NEAR DIGIT
MOV AX,CX
```

The following old source remains:

```asm
POP SI
POP AX
```

### Edit at old physical position 412

Unchanged source before the edit:

```asm
MOV AX,3
JMP ERROR
```

Remove:

```asm
VALUE:
CALL FACTOR
EXPRESSIONLOOP:
PUSH AX
```

Insert in its place:

```asm
ATOM:
MOV AL,[0CC00H]
CMP AL,48
JB NEAR WORDVALUE
CMP AL,57
JBE NEAR LITERAL
WORDVALUE:
JMP NUMBERBAD
LITERAL:
```

The following old source remains:

```asm
PUSH SI
CALL SCAN
```

### Edit at old physical position 403

Unchanged source before the edit:

```asm
CMP AL,65
JB SYMBOLBAD
CMP AL,90
```

Remove:

```asm
JBE NAMEVALID
```

Insert in its place:

```asm
JBE NEAR NAMEVALID
```

The following old source remains:

```asm
JMP SYMBOLBAD
NAMEVALIDEND:
```

### Edit at old physical position 401

Unchanged source before the edit:

```asm
CMP AL,57
JBE NAMEVALID
CMP AL,65
```

Remove:

```asm
JB SYMBOLBAD
```

Insert in its place:

```asm
JB NEAR SYMBOLBAD
```

The following old source remains:

```asm
CMP AL,90
JBE NAMEVALID
```

### Edit at old physical position 399

Unchanged source before the edit:

```asm
CMP AL,48
JB SYMBOLBAD
CMP AL,57
```

Remove:

```asm
JBE NAMEVALID
```

Insert in its place:

```asm
JBE NEAR NAMEVALID
```

The following old source remains:

```asm
CMP AL,65
JB SYMBOLBAD
```

### Edit at old physical position 397

Unchanged source before the edit:

```asm
CMP AL,95
JE NAMEVALID
CMP AL,48
```

Remove:

```asm
JB SYMBOLBAD
```

Insert in its place:

```asm
JB NEAR SYMBOLBAD
```

The following old source remains:

```asm
CMP AL,57
JBE NAMEVALID
```

### Edit at old physical position 395

Unchanged source before the edit:

```asm
CMP AL,0
JE NAMEVALIDEND
CMP AL,95
```

Remove:

```asm
JE NAMEVALID
```

Insert in its place:

```asm
JE NEAR NAMEVALID
```

The following old source remains:

```asm
CMP AL,48
JB SYMBOLBAD
```

### Edit at old physical position 393

Unchanged source before the edit:

```asm
NAMEVALID:
LODSB
CMP AL,0
```

Remove:

```asm
JE NAMEVALIDEND
```

Insert in its place:

```asm
JE NEAR NAMEVALIDEND
```

The following old source remains:

```asm
CMP AL,95
JE NAMEVALID
```

### Edit at old physical position 387

Unchanged source before the edit:

```asm
JMP SYMBOLBAD
ZVALIDNAM1:
CMP AL,90
```

Remove:

```asm
JBE ZVALIDNAM2
JMP SYMBOLBAD
ZVALIDNAM2:
```

Insert in its place:

```asm
JA NEAR SYMBOLBAD
```

The following old source remains:

```asm
NAMEVALID:
LODSB
```

### Edit at old physical position 383

Unchanged source before the edit:

```asm
CMP AL,95
JE NAMEVALID
CMP AL,65
```

Remove:

```asm
JAE ZVALIDNAM1
JMP SYMBOLBAD
ZVALIDNAM1:
```

Insert in its place:

```asm
JB NEAR SYMBOLBAD
```

The following old source remains:

```asm
CMP AL,90
JBE ZVALIDNAM2
```

### Edit at old physical position 381

Unchanged source before the edit:

```asm
MOV SI,0CC00H
LODSB
CMP AL,95
```

Remove:

```asm
JE NAMEVALID
```

Insert in its place:

```asm
JE NEAR NAMEVALID
```

The following old source remains:

```asm
CMP AL,65
JAE ZVALIDNAM1
```

### Edit at old physical position 374

Unchanged source before the edit:

```asm
VALIDNAME:
MOV AX,[TOKLEN]
CMP AX,31
```

Remove:

```asm
JBE NAMELIMIT
```

Insert in its place:

```asm
JBE NEAR NAMELIMIT
```

The following old source remains:

```asm
JMP SYMBOLBAD
NAMELIMIT:
```

### Edit at old physical position 356

Unchanged source before the edit:

```asm
POP SI
RET
```

Remove:

```asm
REGISTER:
MOV BX,REGTAB
MOV CX,20
MOV AX,4
CALL LOOK
CMP BX,0
JE NOREGISTER
ADD BX,3
MOV AL,[BX]
MOV AH,0
RET
NOREGISTER:
MOV AX,0FFFFH
RET
```

The following old source remains:

```asm
VALIDNAME:
MOV AX,[TOKLEN]
```

### Edit at old physical position 339

Unchanged source before the edit:

```asm
CMP AL,DL
JNE LOOKSTEP
CMP AL,0
```

Remove:

```asm
JE LOOKFOUND
```

Insert in its place:

```asm
JE NEAR LOOKFOUND
```

The following old source remains:

```asm
INC DI
JMP LOOKCHAR
```

### Edit at old physical position 337

Unchanged source before the edit:

```asm
MOV BX,DI
MOV DL,[BX]
CMP AL,DL
```

Remove:

```asm
JNE LOOKSTEP
```

Insert in its place:

```asm
JNE NEAR LOOKSTEP
```

The following old source remains:

```asm
CMP AL,0
JE LOOKFOUND
```

### Edit at old physical position 327

Unchanged source before the edit:

```asm
MOV BP,BX
LOOKNEXT:
CMP CX,0
```

Remove:

```asm
JNE ZLOOK1
JMP LOOKMISS
ZLOOK1:
```

Insert in its place:

```asm
JE NEAR LOOKMISS
```

The following old source remains:

```asm
MOV DI,BP
MOV SI,0CC00H
```

### Edit at old physical position 316

Unchanged source before the edit:

```asm
CMP AL,41
JE SEPARATORRET
CMP AL,34
```

Remove:

```asm
JE SEPARATORRET
```

Insert in its place:

```asm
JE NEAR SEPARATORRET
```

The following old source remains:

```asm
MOV AH,0
SEPARATORRET:
```

### Edit at old physical position 314

Unchanged source before the edit:

```asm
CMP AL,40
JE SEPARATORRET
CMP AL,41
```

Remove:

```asm
JE SEPARATORRET
```

Insert in its place:

```asm
JE NEAR SEPARATORRET
```

The following old source remains:

```asm
CMP AL,34
JE SEPARATORRET
```

### Edit at old physical position 312

Unchanged source before the edit:

```asm
CMP AL,45
JE SEPARATORRET
CMP AL,40
```

Remove:

```asm
JE SEPARATORRET
```

Insert in its place:

```asm
JE NEAR SEPARATORRET
```

The following old source remains:

```asm
CMP AL,41
JE SEPARATORRET
```

### Edit at old physical position 310

Unchanged source before the edit:

```asm
CMP AL,43
JE SEPARATORRET
CMP AL,45
```

Remove:

```asm
JE SEPARATORRET
```

Insert in its place:

```asm
JE NEAR SEPARATORRET
```

The following old source remains:

```asm
CMP AL,40
JE SEPARATORRET
```

### Edit at old physical position 308

Unchanged source before the edit:

```asm
CMP AL,93
JE SEPARATORRET
CMP AL,43
```

Remove:

```asm
JE SEPARATORRET
```

Insert in its place:

```asm
JE NEAR SEPARATORRET
```

The following old source remains:

```asm
CMP AL,45
JE SEPARATORRET
```

### Edit at old physical position 306

Unchanged source before the edit:

```asm
CMP AL,91
JE SEPARATORRET
CMP AL,93
```

Remove:

```asm
JE SEPARATORRET
```

Insert in its place:

```asm
JE NEAR SEPARATORRET
```

The following old source remains:

```asm
CMP AL,43
JE SEPARATORRET
```

### Edit at old physical position 304

Unchanged source before the edit:

```asm
CMP AL,58
JE SEPARATORRET
CMP AL,91
```

Remove:

```asm
JE SEPARATORRET
```

Insert in its place:

```asm
JE NEAR SEPARATORRET
```

The following old source remains:

```asm
CMP AL,93
JE SEPARATORRET
```

### Edit at old physical position 302

Unchanged source before the edit:

```asm
JMP SEPARATORRET
ZSCAN4:
CMP AL,58
```

Remove:

```asm
JE SEPARATORRET
```

Insert in its place:

```asm
JE NEAR SEPARATORRET
```

The following old source remains:

```asm
CMP AL,91
JE SEPARATORRET
```

### Edit at old physical position 298

Unchanged source before the edit:

```asm
SEPARATOR:
MOV AH,1
CMP AL,44
```

Remove:

```asm
JNE ZSCAN4
JMP SEPARATORRET
ZSCAN4:
```

Insert in its place:

```asm
JE NEAR SEPARATORRET
```

The following old source remains:

```asm
CMP AL,58
JE SEPARATORRET
```

### Edit at old physical position 291

Unchanged source before the edit:

```asm
CMP AL,97
JB TOKENKEPT
CMP AL,122
```

Remove:

```asm
JA TOKENKEPT
```

Insert in its place:

```asm
JA NEAR TOKENKEPT
```

The following old source remains:

```asm
SUB AL,32
TOKENKEPT:
```

### Edit at old physical position 289

Unchanged source before the edit:

```asm
JMP ERROR
TOKENCHAR:
CMP AL,97
```

Remove:

```asm
JB TOKENKEPT
```

Insert in its place:

```asm
JB NEAR TOKENKEPT
```

The following old source remains:

```asm
CMP AL,122
JA TOKENKEPT
```

### Edit at old physical position 268

Unchanged source before the edit:

```asm
CMP AH,1
JE SCANBACK
CMP DI,0CC3FH
```

Remove:

```asm
JAE TOKENBAD
```

Insert in its place:

```asm
JAE NEAR TOKENBAD
```

The following old source remains:

```asm
CALL TOKENCHAR
STOSB
```

### Edit at old physical position 266

Unchanged source before the edit:

```asm
JE SCANBACK
CALL SEPARATOR
CMP AH,1
```

Remove:

```asm
JE SCANBACK
```

Insert in its place:

```asm
JE NEAR SCANBACK
```

The following old source remains:

```asm
CMP DI,0CC3FH
JAE TOKENBAD
```

### Edit at old physical position 263

Unchanged source before the edit:

```asm
CMP AL,9
JE SCANBACK
CMP AL,59
```

Remove:

```asm
JE SCANBACK
```

Insert in its place:

```asm
JE NEAR SCANBACK
```

The following old source remains:

```asm
CALL SEPARATOR
CMP AH,1
```

### Edit at old physical position 261

Unchanged source before the edit:

```asm
CMP AL,32
JE SCANBACK
CMP AL,9
```

Remove:

```asm
JE SCANBACK
```

Insert in its place:

```asm
JE NEAR SCANBACK
```

The following old source remains:

```asm
CMP AL,59
JE SCANBACK
```

### Edit at old physical position 259

Unchanged source before the edit:

```asm
CMP AL,0
JE SCANBACK
CMP AL,32
```

Remove:

```asm
JE SCANBACK
```

Insert in its place:

```asm
JE NEAR SCANBACK
```

The following old source remains:

```asm
CMP AL,9
JE SCANBACK
```

### Edit at old physical position 257

Unchanged source before the edit:

```asm
SCANMORE:
LODSB
CMP AL,0
```

Remove:

```asm
JE SCANBACK
```

Insert in its place:

```asm
JE NEAR SCANBACK
```

The following old source remains:

```asm
CMP AL,32
JE SCANBACK
```

### Edit at old physical position 251

Unchanged source before the edit:

```asm
STOSB
CALL SEPARATOR
CMP AH,1
```

Remove:

```asm
JNE ZSCAN3
JMP SCANDONE
ZSCAN3:
```

Insert in its place:

```asm
JE NEAR SCANDONE
```

The following old source remains:

```asm
SCANMORE:
LODSB
```

### Edit at old physical position 244

Unchanged source before the edit:

```asm
JMP SCANEND
ZSCAN1:
CMP AL,59
```

Remove:

```asm
JNE ZSCAN2
JMP SCANEND
ZSCAN2:
```

Insert in its place:

```asm
JE NEAR SCANEND
```

The following old source remains:

```asm
CALL TOKENCHAR
STOSB
```

### Edit at old physical position 240

Unchanged source before the edit:

```asm
CMP AL,9
JE SCANSPACE
CMP AL,0
```

Remove:

```asm
JNE ZSCAN1
JMP SCANEND
ZSCAN1:
```

Insert in its place:

```asm
JE NEAR SCANEND
```

The following old source remains:

```asm
CMP AL,59
JNE ZSCAN2
```

### Edit at old physical position 238

Unchanged source before the edit:

```asm
CMP AL,32
JE SCANSPACE
CMP AL,9
```

Remove:

```asm
JE SCANSPACE
```

Insert in its place:

```asm
JE NEAR SCANSPACE
```

The following old source remains:

```asm
CMP AL,0
JNE ZSCAN1
```

### Edit at old physical position 236

Unchanged source before the edit:

```asm
SCANSPACE:
LODSB
CMP AL,32
```

Remove:

```asm
JE SCANSPACE
```

Insert in its place:

```asm
JE NEAR SCANSPACE
```

The following old source remains:

```asm
CMP AL,9
JE SCANSPACE
```

### Edit at old physical position 210

Unchanged source before the edit:

```asm
MOV AL,1
MOV [ENDED],AL
CMP BP,0
```

Remove:

```asm
JE EMPTYEND
```

Insert in its place:

```asm
JE NEAR EMPTYEND
```

The following old source remains:

```asm
LINEEND:
MOV AL,0
```

### Edit at old physical position 198

Unchanged source before the edit:

```asm
LINEFEED:
MOV AL,[SKIPLF]
CMP AL,0
```

Remove:

```asm
JE LINEEND
```

Insert in its place:

```asm
JE NEAR LINEEND
```

The following old source remains:

```asm
MOV AL,0
MOV [SKIPLF],AL
```

### Edit at old physical position 188

Unchanged source before the edit:

```asm
JMP READBAD
ZREADLINE6:
CMP AL,126
```

Remove:

```asm
JBE ZREADLINE7
JMP READBAD
ZREADLINE7:
```

Insert in its place:

```asm
JA NEAR READBAD
```

The following old source remains:

```asm
KEEPCHAR:
STOSB
```

### Edit at old physical position 184

Unchanged source before the edit:

```asm
CMP AL,9
JE KEEPCHAR
CMP AL,32
```

Remove:

```asm
JAE ZREADLINE6
JMP READBAD
ZREADLINE6:
```

Insert in its place:

```asm
JB NEAR READBAD
```

The following old source remains:

```asm
CMP AL,126
JBE ZREADLINE7
```

### Edit at old physical position 182

Unchanged source before the edit:

```asm
JMP READFULL
ZREADLINE5:
CMP AL,9
```

Remove:

```asm
JE KEEPCHAR
```

Insert in its place:

```asm
JE NEAR KEEPCHAR
```

The following old source remains:

```asm
CMP AL,32
JAE ZREADLINE6
```

### Edit at old physical position 178

Unchanged source before the edit:

```asm
JMP ENDFILE
ZREADLINE4:
CMP BP,1023
```

Remove:

```asm
JB ZREADLINE5
JMP READFULL
ZREADLINE5:
```

Insert in its place:

```asm
JAE NEAR READFULL
```

The following old source remains:

```asm
CMP AL,9
JE KEEPCHAR
```

### Edit at old physical position 174

Unchanged source before the edit:

```asm
JMP CARRIAGE
ZREADLINE3:
CMP AL,26
```

Remove:

```asm
JNE ZREADLINE4
JMP ENDFILE
ZREADLINE4:
```

Insert in its place:

```asm
JE NEAR ENDFILE
```

The following old source remains:

```asm
CMP BP,1023
JB ZREADLINE5
```

### Edit at old physical position 170

Unchanged source before the edit:

```asm
MOV AH,0
MOV [SKIPLF],AH
CMP AL,13
```

Remove:

```asm
JNE ZREADLINE3
JMP CARRIAGE
ZREADLINE3:
```

Insert in its place:

```asm
JE NEAR CARRIAGE
```

The following old source remains:

```asm
CMP AL,26
JNE ZREADLINE4
```

### Edit at old physical position 164

Unchanged source before the edit:

```asm
ZREADLINE1:
MOV AL,[CHAR]
CMP AL,10
```

Remove:

```asm
JNE ZREADLINE2
JMP LINEFEED
ZREADLINE2:
```

Insert in its place:

```asm
JE NEAR LINEFEED
```

The following old source remains:

```asm
MOV AH,0
MOV [SKIPLF],AH
```

### Edit at old physical position 159

Unchanged source before the edit:

```asm
READCHAR:
CALL NEXTBYTE
CMP AX,0
```

Remove:

```asm
JNE ZREADLINE1
JMP ENDFILE
ZREADLINE1:
```

Insert in its place:

```asm
JE NEAR ENDFILE
```

The following old source remains:

```asm
MOV AL,[CHAR]
CMP AL,10
```

### Edit at old physical position 153

Unchanged source before the edit:

```asm
MOV BP,0
MOV AL,[ENDED]
CMP AL,0
```

Remove:

```asm
JE READCHAR
```

Insert in its place:

```asm
JE NEAR READCHAR
```

The following old source remains:

```asm
MOV AX,0
RET
```

### Edit at old physical position 132

Unchanged source before the edit:

```asm
MOV DX,0
MOV [RDPOS],DX
CMP AX,0
```

Remove:

```asm
JE BUFFEREND
```

Insert in its place:

```asm
JE NEAR BUFFEREND
```

The following old source remains:

```asm
BUFFERBYTE:
MOV BX,[RDPOS]
```

### Edit at old physical position 125

Unchanged source before the edit:

```asm
MOV CX,4096
MOV AH,3FH
INT 21H
```

Remove:

```asm
JAE REFILLED
```

Insert in its place:

```asm
JAE NEAR REFILLED
```

The following old source remains:

```asm
JMP FILEBAD
REFILLED:
```

### Edit at old physical position 119

Unchanged source before the edit:

```asm
MOV AX,[RDPOS]
MOV DX,[RDLEN]
CMP AX,DX
```

Remove:

```asm
JB BUFFERBYTE
```

Insert in its place:

```asm
JB NEAR BUFFERBYTE
```

The following old source remains:

```asm
MOV BX,[HANDLE]
MOV DX,0D000H
```

### Edit at old physical position 115

Unchanged source before the edit:

```asm
MOV [INOPEN],AL
RET
```

Insert in its place:

```asm
CREATEOUT:
MOV DX,TMPNAME
MOV CX,0
MOV AH,3CH
INT 21H
JAE NEAR OUTPUTOPEN
JMP FILEBAD
OUTPUTOPEN:
MOV [OUTHANDLE],AX
MOV AL,1
MOV [OUTOPEN],AL
MOV [OWNTMP],AL
RET
CLOSEOUT:
MOV BX,[OUTHANDLE]
MOV AH,3EH
INT 21H
JAE NEAR OUTPUTCLOSED
JMP FILEBAD
OUTPUTCLOSED:
MOV AL,0
MOV [OUTOPEN],AL
RET

FLUSH:
PUSH AX
PUSH BX
PUSH CX
PUSH DX
MOV CX,[OUTCNT]
CMP CX,0
JE NEAR FLUSHDONE
MOV BX,[OUTHANDLE]
MOV DX,0E000H
MOV AH,40H
INT 21H
JAE NEAR FLUSHCOUNT
JMP FILEBAD
FLUSHCOUNT:
CMP AX,CX
JE NEAR FLUSHGOOD
JMP FILEBAD
FLUSHGOOD:
MOV AX,0
MOV [OUTCNT],AX
FLUSHDONE:
POP DX
POP CX
POP BX
POP AX
RET
```

The following old source remains:

```asm
NEXTBYTE:
MOV AX,[RDPOS]
```

### Edit at old physical position 108

Unchanged source before the edit:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

Remove:

```asm
JAE INPUTCLOSED
```

Insert in its place:

```asm
JAE NEAR INPUTCLOSED
```

The following old source remains:

```asm
JMP FILEBAD
INPUTCLOSED:
```

### Edit at old physical position 96

Unchanged source before the edit:

```asm
MOV DX,SRCNAME
MOV AX,3D00H
INT 21H
```

Remove:

```asm
JAE INPUTOPEN
```

Insert in its place:

```asm
JAE NEAR INPUTOPEN
```

The following old source remains:

```asm
JMP FILEBAD
INPUTOPEN:
```

### Edit at old physical position 8

Unchanged source before the edit:

```asm
JE ROOM
MOV AX,7
JMP ERROR
```

Remove the complete old physical range 8–86. Its first source is:

```asm
ROOM:
CALL MEMINIT
CALL PREFLIGHT
```

Its last source is:

```asm
GOOD:
MOV AX,4C00H
INT 21H
```

Remove both boundaries and all source between them.

The following old source remains:

```asm

FILEBAD:
```

### Edit at old physical position 5

Unchanged source before the edit:

```asm
START:
CLD
CMP SP,0FFFEH
```

Remove:

```asm
JE ROOM
```

Insert in its place:

```asm
JNE NEAR MEMORYBAD
CALL OPENFILE
READNEXT:
CALL READLINE
CMP AX,0
JE NEAR READDONE
MOV SI,0C800H
SHOWBYTE:
LODSB
CMP AL,0
JE NEAR SHOWEND
MOV DL,AL
MOV AH,2
INT 21H
JMP SHOWBYTE
SHOWEND:
MOV DX,NEWLINE
CALL TEXT
JMP READNEXT
READDONE:
CALL CLOSEFILE
MOV AX,4C00H
INT 21H
MEMORYBAD:
```

The following old source remains:

```asm
MOV AX,7
JMP ERROR
```

### Edit at old physical position 1

Remove:

```asm
; ASM86A construction checkpoint.
```

Insert in its place:

```asm
; IR86 streaming native translator. Built with ASM86A.
```

The following old source remains:

```asm
START:
CLD
```

## Build and check

```dos
COPY IR01.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 02042 bytes`. Save RESULT.COM as IR01.COM. VIEW.BAS must show length 2042.

Create T01.IR:

```text
ABC
```

```dos
COPY T01.IR SOURCE.IR
```

```dos
CHECK IR01
```

Require:

```text
ABC
PASS
```

## Check the new boundary

Temporarily rename SOURCE.IR to HOLD.TXT and run CHECK IR01. Restore the source afterward. Require:

```text
IR ERROR 0000000000 CODE 6
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

