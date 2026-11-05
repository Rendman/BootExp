+++
title = "13 \u00b7 Allocating auxiliary workspace"
weight = 13
description = "Shrink the main allocation and request owned DOS work blocks."
download = "A13.ASM"
+++

A full symbol table should not compete with resident code for the same segment.

## The working parts

MEMINIT checks the owned main segment, retains 1000H paragraphs with DOS function 4AH, allocates eight A00H-paragraph pages and one 200H-paragraph bucket block, and clears every bucket head. Returned segments are saved in MEMSEGS; HASHSEG follows the eight page words.

MEMFREE releases recorded allocations and restores ES to the main segment. Partial-allocation failure uses the same cleanup. The assembler still uses its seed symbol table in this checkpoint; MEMORY READY confirms the auxiliary setup completed before normal assembly.

## Enter the source

Copy `A12.ASM` to `A13.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `P1:`

Unchanged source immediately before this edit:

```asm

P1:
DB 0
```

Insert after old physical line 1463.

Insert:

```asm

MEMNEXT:
DW 0

MEMCOUNT:
DW 0

MEMSEGS:
DW 0,0,0,0,0,0,0,0

HASHSEG:
DW 0

READYMSG:
DB 77,69,77,79,82,89,32,82,69,65,68,89,13,10,36
```

### Change 2 near `SEGBAD:`

Unchanged source immediately before this edit:

```asm
RET
SEGBAD:
JMP TWOBAD
```

Insert after old physical line 1263.

Insert:

```asm

MEMINIT:
MOV AX,[2]
MOV DX,CS
SUB AX,DX
CMP AX,1000H
JAE MEMOWNED
JMP MEMBAD
MEMOWNED:
MOV AX,CS
MOV ES,AX
MOV BX,1000H
MOV AH,4AH
INT 21H
JAE MEMSHRUNK
JMP MEMBAD
MEMSHRUNK:
MOV AX,MEMSEGS
MOV [MEMNEXT],AX
MOV CX,8
MEMALLOCLOOP:
PUSH CX
MOV BX,0A00H
CALL ALLOCBLOCK
POP CX
DEC CX
JNE MEMALLOCLOOP
MOV BX,200H
CALL ALLOCBLOCK
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,0
MOV CX,4096
MOV AX,0
MEMCLEAR:
MOV ES:[BX],AX
ADD BX,2
DEC CX
JNE MEMCLEAR
MOV AX,CS
MOV ES,AX
RET
ALLOCBLOCK:
MOV AH,48H
INT 21H
JAE ALLOCATED
JMP MEMBAD
ALLOCATED:
MOV BX,[MEMNEXT]
MOV [BX],AX
ADD BX,2
MOV [MEMNEXT],BX
MOV AX,[MEMCOUNT]
INC AX
MOV [MEMCOUNT],AX
RET
MEMBAD:
MOV AX,7
JMP ERROR

MEMFREE:
MOV DI,MEMSEGS
MOV BP,[MEMCOUNT]
MEMFREELOOP:
CMP BP,0
JNE ZMEMFREE1
JMP MEMFREED
ZMEMFREE1:
MOV BX,DI
MOV AX,[BX]
CMP AX,0
JE MEMFREENEXT
MOV ES,AX
MOV AH,49H
INT 21H
JAE MEMFREEOK
MOV AL,1
MOV [CLEANFAIL],AL
JMP MEMFREENEXT
MEMFREEOK:
MOV BX,DI
MOV AX,0
MOV [BX],AX
MEMFREENEXT:
ADD DI,2
DEC BP
JMP MEMFREELOOP
MEMFREED:
MOV AX,CS
MOV ES,AX
RET

EARLYTEST:
MOV DX,READYMSG
CALL TEXT
RET
```

The following old source stays in place:

```asm

OKMSG:
```

### Change 3 near `SEGMOV:`

Unchanged source immediately before this edit:

```asm
JNE SEGBAD
MOV AL,[WIDTH]
CMP AL,1
```

Remove this exact source at old physical positions 1238–1238:

```asm
JNE SEGBAD
```

Replace it with:

```asm
JE ZSEGMOV3
JMP SEGBAD
ZSEGMOV3:
```

The following old source stays in place:

```asm
MOV AL,142
CALL EMIT
```

### Change 4 near `SEGMOV:`

Unchanged source immediately before this edit:

```asm
JE SEGBAD
MOV AL,[KIND]
CMP AL,1
```

Remove this exact source at old physical positions 1235–1235:

```asm
JNE SEGBAD
```

Replace it with:

```asm
JE ZSEGMOV2
JMP SEGBAD
ZSEGMOV2:
```

The following old source stays in place:

```asm
MOV AL,[WIDTH]
CMP AL,1
```

### Change 5 near `SEGMOV:`

Unchanged source immediately before this edit:

```asm
JNE SEGLOAD
MOV AL,[R1]
CMP AL,1
```

Remove this exact source at old physical positions 1232–1232:

```asm
JE SEGBAD
```

Replace it with:

```asm
JNE ZSEGMOV1
JMP SEGBAD
ZSEGMOV1:
```

The following old source stays in place:

```asm
MOV AL,[KIND]
CMP AL,1
```

### Change 6 near `SEGOPERAND:`

Unchanged source immediately before this edit:

```asm
CALL SCAN
MOV AL,[4080H]
CMP AL,58
```

Remove this exact source at old physical positions 1198–1198:

```asm
JNE SEGREGISTER
```

Replace it with:

```asm
JE ZSEGOPERA1
JMP SEGREGISTER
ZSEGOPERA1:
```

The following old source stays in place:

```asm
POP AX
MOV AX,[SEGCODE]
```

### Change 7 near `CLEANEND:`

Unchanged source immediately before this edit:

```asm
MOV AL,1
MOV [CLEANFAIL],AL
CLEANEND:
```

Insert after old physical line 1189.

Insert:

```asm
CALL MEMFREE
```

The following old source stays in place:

```asm
RET
```

### Change 8 near `PUBLISH:`

Unchanged source immediately before this edit:

```asm
MOV DI,RESNAME
MOV AH,56H
INT 21H
```

Remove this exact source at old physical positions 1122–1122:

```asm
JAE PUBLISHED
```

Replace it with:

```asm
JB ZCOMMIT1
JMP PUBLISHED
ZCOMMIT1:
```

The following old source stays in place:

```asm
MOV AL,[HAVEBAK]
CMP AL,0
```

### Change 9 near `MOVDESTREG:`

Unchanged source immediately before this edit:

```asm
CMP AL,1
JE MOVREG
CMP AL,2
```

Remove this exact source at old physical positions 803–803:

```asm
JE LOADMEM
```

Replace it with:

```asm
JNE ZMOVOPERA2
JMP LOADMEM
ZMOVOPERA2:
```

The following old source stays in place:

```asm
MOV AL,[W1]
CALL TIMES8
```

### Change 10 near `MOVDESTREG:`

Unchanged source immediately before this edit:

```asm
JMP STOREMEM
MOVDESTREG:
CMP AL,1
```

Remove this exact source at old physical positions 798–798:

```asm
JNE TWOBAD
```

Replace it with:

```asm
JE ZMOVOPERA1
JMP TWOBAD
ZMOVOPERA1:
```

The following old source stays in place:

```asm
MOV AL,[KIND]
CMP AL,1
```

### Change 11 near `TWOOPERANDS:`

Unchanged source immediately before this edit:

```asm
CMP AL,1
JE MATHREG
CMP AL,3
```

Remove this exact source at old physical positions 757–757:

```asm
JNE TWOBAD
```

Replace it with:

```asm
JE ZTWOOPERA4
JMP TWOBAD
ZTWOOPERA4:
```

The following old source stays in place:

```asm
MOV AL,[W1]
ADD AL,128
```

### Change 12 near `TWOOPERANDS:`

Unchanged source immediately before this edit:

```asm
JE MOVOPERANDS
MOV AL,[K1]
CMP AL,1
```

Remove this exact source at old physical positions 752–752:

```asm
JNE TWOBAD
```

Replace it with:

```asm
JE ZTWOOPERA3
JMP TWOBAD
ZTWOOPERA3:
```

The following old source stays in place:

```asm
MOV AL,[KIND]
CMP AL,1
```

### Change 13 near `TWOOPERANDS:`

Unchanged source immediately before this edit:

```asm
CALL OPERAND
MOV AL,[TYPE]
CMP AL,3
```

Remove this exact source at old physical positions 749–749:

```asm
JE MOVOPERANDS
```

Replace it with:

```asm
JNE ZTWOOPERA2
JMP MOVOPERANDS
ZTWOOPERA2:
```

The following old source stays in place:

```asm
MOV AL,[K1]
CMP AL,1
```

### Change 14 near `TWOOPERANDS:`

Unchanged source immediately before this edit:

```asm
CALL SCAN
MOV AL,[4080H]
CMP AL,44
```

Remove this exact source at old physical positions 745–745:

```asm
JNE TWOBAD
```

Replace it with:

```asm
JE ZTWOOPERA1
JMP TWOBAD
ZTWOOPERA1:
```

The following old source stays in place:

```asm
CALL OPERAND
MOV AL,[TYPE]
```

### Change 15 near `SINGLE:`

Unchanged source immediately before this edit:

```asm
CMP AX,8
JB SYNTAXBAD
CMP AX,15
```

Remove this exact source at old physical positions 663–663:

```asm
JA SYNTAXBAD
```

Replace it with:

```asm
JBE ZSINGLE2
JMP SYNTAXBAD
ZSINGLE2:
```

The following old source stays in place:

```asm
SUB AL,8
MOV DL,[OP]
```

### Change 16 near `SINGLE:`

Unchanged source immediately before this edit:

```asm
CALL SCAN
CALL REGISTER
CMP AX,8
```

Remove this exact source at old physical positions 661–661:

```asm
JB SYNTAXBAD
```

Replace it with:

```asm
JAE ZSINGLE1
JMP SYNTAXBAD
ZSINGLE1:
```

The following old source stays in place:

```asm
CMP AX,15
JA SYNTAXBAD
```

### Change 17 near `DATASEP:`

Unchanged source immediately before this edit:

```asm
CMP AL,44
JE DATAITEM
CMP AL,0
```

Remove this exact source at old physical positions 648–648:

```asm
JNE SYNTAXBAD
```

Replace it with:

```asm
JE ZDATAITEM1
JMP SYNTAXBAD
ZDATAITEM1:
```

The following old source stays in place:

```asm
RET
```

### Change 18 near `OPERAND:`

Unchanged source immediately before this edit:

```asm
JE MEMORY
CALL REGISTER
CMP AX,0FFFFH
```

Remove this exact source at old physical positions 509–509:

```asm
JE IMMEDIATE
```

Replace it with:

```asm
JNE ZOPERAND2
JMP IMMEDIATE
ZOPERAND2:
```

The following old source stays in place:

```asm
CMP AX,16
JB NORMALREGISTER
```

### Change 19 near `OPERAND:`

Unchanged source immediately before this edit:

```asm
CALL SCAN
MOV AL,[4080H]
CMP AL,91
```

Remove this exact source at old physical positions 506–506:

```asm
JE MEMORY
```

Replace it with:

```asm
JNE ZOPERAND1
JMP MEMORY
ZOPERAND1:
```

The following old source stays in place:

```asm
CALL REGISTER
CMP AX,0FFFFH
```

### Change 20 near `DEFINE:`

Unchanged source immediately before this edit:

```asm
JNE DEFINEBAD
MOV AX,[SYMC]
CMP AX,2048
```

Remove this exact source at old physical positions 465–465:

```asm
JAE TABLEFULL
```

Replace it with:

```asm
JB ZDEFINE4
JMP TABLEFULL
ZDEFINE4:
```

The following old source stays in place:

```asm
MOV DI,[SYMNEXT]
PUSH SI
```

### Change 21 near `DEFINE:`

Unchanged source immediately before this edit:

```asm
CMP AL,1
JNE CHECKDEFINE
CMP BX,0
```

Remove this exact source at old physical positions 462–462:

```asm
JNE DEFINEBAD
```

Replace it with:

```asm
JE ZDEFINE3
JMP DEFINEBAD
ZDEFINE3:
```

The following old source stays in place:

```asm
MOV AX,[SYMC]
CMP AX,2048
```

### Change 22 near `DEFINE:`

Unchanged source immediately before this edit:

```asm
CALL LOOK
MOV AL,[PASS]
CMP AL,1
```

Remove this exact source at old physical positions 460–460:

```asm
JNE CHECKDEFINE
```

Replace it with:

```asm
JE ZDEFINE2
JMP CHECKDEFINE
ZDEFINE2:
```

The following old source stays in place:

```asm
CMP BX,0
JNE DEFINEBAD
```

### Change 23 near `DEFINE:`

Unchanged source immediately before this edit:

```asm
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
```

Remove this exact source at old physical positions 453–453:

```asm
JNE DEFINEBAD
```

Replace it with:

```asm
JE ZDEFINE1
JMP DEFINEBAD
ZDEFINE1:
```

The following old source stays in place:

```asm
MOV BX,5000H
MOV CX,[SYMC]
```

### Change 24 near `ADDDIGIT:`

Unchanged source immediately before this edit:

```asm
ADDDIGIT:
ADD CX,DX
CMP SI,DI
```

Remove this exact source at old physical positions 417–417:

```asm
JB DIGIT
```

Replace it with:

```asm
JAE ZVALUE7
JMP DIGIT
ZVALUE7:
```

The following old source stays in place:

```asm
MOV AX,CX
POP SI
```

### Change 25 near `DIGITOK:`

Unchanged source immediately before this edit:

```asm
JA NUMBERBAD
JB DECDIGIT
CMP DX,5
```

Remove this exact source at old physical positions 398–398:

```asm
JA NUMBERBAD
```

Replace it with:

```asm
JBE ZVALUE6
JMP NUMBERBAD
ZVALUE6:
```

The following old source stays in place:

```asm
DECDIGIT:
MOV AX,CX
```

### Change 26 near `DIGITOK:`

Unchanged source immediately before this edit:

```asm
CMP BP,16
JE HEXDIGIT
CMP CX,6553
```

Remove this exact source at old physical positions 395–395:

```asm
JA NUMBERBAD
```

Replace it with:

```asm
JBE ZVALUE5
JMP NUMBERBAD
ZVALUE5:
```

The following old source stays in place:

```asm
JB DECDIGIT
CMP DX,5
```

### Change 27 near `DIGITOK:`

Unchanged source immediately before this edit:

```asm
MOV AH,0
MOV DX,AX
CMP DX,BP
```

Remove this exact source at old physical positions 391–391:

```asm
JAE NUMBERBAD
```

Replace it with:

```asm
JB ZVALUE4
JMP NUMBERBAD
ZVALUE4:
```

The following old source stays in place:

```asm
CMP BP,16
JE HEXDIGIT
```

### Change 28 near `DIGIT:`

Unchanged source immediately before this edit:

```asm
CMP AL,10
JB NUMBERBAD
CMP AL,15
```

Remove this exact source at old physical positions 386–386:

```asm
JA NUMBERBAD
```

Replace it with:

```asm
JBE ZVALUE3
JMP NUMBERBAD
ZVALUE3:
```

The following old source stays in place:

```asm
DIGITOK:
MOV AH,0
```

### Change 29 near `DIGIT:`

Unchanged source immediately before this edit:

```asm
JBE DIGITOK
SUB AL,7
CMP AL,10
```

Remove this exact source at old physical positions 384–384:

```asm
JB NUMBERBAD
```

Replace it with:

```asm
JAE ZVALUE2
JMP NUMBERBAD
ZVALUE2:
```

The following old source stays in place:

```asm
CMP AL,15
JA NUMBERBAD
```

### Change 30 near `NUMBERSTART:`

Unchanged source immediately before this edit:

```asm
DEC DI
NUMBERSTART:
CMP SI,DI
```

Remove this exact source at old physical positions 375–375:

```asm
JE NUMBERBAD
```

Replace it with:

```asm
JNE ZVALUE1
JMP NUMBERBAD
ZVALUE1:
```

The following old source stays in place:

```asm
MOV CX,0
DIGIT:
```

### Change 31 near `VALIDNAME:`

Unchanged source immediately before this edit:

```asm
CMP AL,65
JB SYMBOLBAD
CMP AL,90
```

Remove this exact source at old physical positions 329–329:

```asm
JA SYMBOLBAD
```

Replace it with:

```asm
JBE ZVALIDNAM2
JMP SYMBOLBAD
ZVALIDNAM2:
```

The following old source stays in place:

```asm
NAMEVALID:
LODSB
```

### Change 32 near `VALIDNAME:`

Unchanged source immediately before this edit:

```asm
CMP AL,95
JE NAMEVALID
CMP AL,65
```

Remove this exact source at old physical positions 327–327:

```asm
JB SYMBOLBAD
```

Replace it with:

```asm
JAE ZVALIDNAM1
JMP SYMBOLBAD
ZVALIDNAM1:
```

The following old source stays in place:

```asm
CMP AL,90
JA SYMBOLBAD
```

### Change 33 near `LOOKNEXT:`

Unchanged source immediately before this edit:

```asm
MOV BP,BX
LOOKNEXT:
CMP CX,0
```

Remove this exact source at old physical positions 278–278:

```asm
JE LOOKMISS
```

Replace it with:

```asm
JNE ZLOOK1
JMP LOOKMISS
ZLOOK1:
```

The following old source stays in place:

```asm
MOV DI,BP
MOV SI,4080H
```

### Change 34 near `SCANMORE:`

Unchanged source immediately before this edit:

```asm
SCANMORE:
LODSB
CMP AL,0
```

Remove this exact source at old physical positions 239–239:

```asm
JE SCANBACK
```

Replace it with:

```asm
JNE ZSCAN7
JMP SCANBACK
ZSCAN7:
```

The following old source stays in place:

```asm
CMP AL,32
JE SCANBACK
```

### Change 35 near `SCANSPACE:`

Unchanged source immediately before this edit:

```asm
CMP AL,91
JE SCANDONE
CMP AL,93
```

Remove this exact source at old physical positions 235–235:

```asm
JE SCANDONE
```

Replace it with:

```asm
JNE ZSCAN6
JMP SCANDONE
ZSCAN6:
```

The following old source stays in place:

```asm
SCANMORE:
LODSB
```

### Change 36 near `SCANSPACE:`

Unchanged source immediately before this edit:

```asm
CMP AL,58
JE SCANDONE
CMP AL,91
```

Remove this exact source at old physical positions 233–233:

```asm
JE SCANDONE
```

Replace it with:

```asm
JNE ZSCAN5
JMP SCANDONE
ZSCAN5:
```

The following old source stays in place:

```asm
CMP AL,93
JE SCANDONE
```

### Change 37 near `SCANSPACE:`

Unchanged source immediately before this edit:

```asm
CMP AL,44
JE SCANDONE
CMP AL,58
```

Remove this exact source at old physical positions 231–231:

```asm
JE SCANDONE
```

Replace it with:

```asm
JNE ZSCAN4
JMP SCANDONE
ZSCAN4:
```

The following old source stays in place:

```asm
CMP AL,91
JE SCANDONE
```

### Change 38 near `SCANSPACE:`

Unchanged source immediately before this edit:

```asm
JE SCANEND
STOSB
CMP AL,44
```

Remove this exact source at old physical positions 229–229:

```asm
JE SCANDONE
```

Replace it with:

```asm
JNE ZSCAN3
JMP SCANDONE
ZSCAN3:
```

The following old source stays in place:

```asm
CMP AL,58
JE SCANDONE
```

### Change 39 near `SCANSPACE:`

Unchanged source immediately before this edit:

```asm
CMP AL,0
JE SCANEND
CMP AL,59
```

Remove this exact source at old physical positions 226–226:

```asm
JE SCANEND
```

Replace it with:

```asm
JNE ZSCAN2
JMP SCANEND
ZSCAN2:
```

The following old source stays in place:

```asm
STOSB
CMP AL,44
```

### Change 40 near `SCANSPACE:`

Unchanged source immediately before this edit:

```asm
CMP AL,32
JE SCANSPACE
CMP AL,0
```

Remove this exact source at old physical positions 224–224:

```asm
JE SCANEND
```

Replace it with:

```asm
JNE ZSCAN1
JMP SCANEND
ZSCAN1:
```

The following old source stays in place:

```asm
CMP AL,59
JE SCANEND
```

### Change 41 near `READCHAR:`

Unchanged source immediately before this edit:

```asm
CMP AL,32
JB READBAD
CMP AL,126
```

Remove this exact source at old physical positions 158–158:

```asm
JA READBAD
```

Replace it with:

```asm
JBE ZREADLINE7
JMP READBAD
ZREADLINE7:
```

The following old source stays in place:

```asm
CMP AL,97
JB KEEPCHAR
```

### Change 42 near `READCHAR:`

Unchanged source immediately before this edit:

```asm
CMP AL,9
JE TABCHAR
CMP AL,32
```

Remove this exact source at old physical positions 156–156:

```asm
JB READBAD
```

Replace it with:

```asm
JAE ZREADLINE6
JMP READBAD
ZREADLINE6:
```

The following old source stays in place:

```asm
CMP AL,126
JA READBAD
```

### Change 43 near `READCHAR:`

Unchanged source immediately before this edit:

```asm
CMP AL,26
JE ENDFILE
CMP BP,120
```

Remove this exact source at old physical positions 152–152:

```asm
JAE READFULL
```

Replace it with:

```asm
JB ZREADLINE5
JMP READFULL
ZREADLINE5:
```

The following old source stays in place:

```asm
CMP AL,9
JE TABCHAR
```

### Change 44 near `READCHAR:`

Unchanged source immediately before this edit:

```asm
CMP AL,13
JE CARRIAGE
CMP AL,26
```

Remove this exact source at old physical positions 150–150:

```asm
JE ENDFILE
```

Replace it with:

```asm
JNE ZREADLINE4
JMP ENDFILE
ZREADLINE4:
```

The following old source stays in place:

```asm
CMP BP,120
JAE READFULL
```

### Change 45 near `READCHAR:`

Unchanged source immediately before this edit:

```asm
MOV AH,0
MOV [SKIPLF],AH
CMP AL,13
```

Remove this exact source at old physical positions 148–148:

```asm
JE CARRIAGE
```

Replace it with:

```asm
JNE ZREADLINE3
JMP CARRIAGE
ZREADLINE3:
```

The following old source stays in place:

```asm
CMP AL,26
JE ENDFILE
```

### Change 46 near `READCHAR:`

Unchanged source immediately before this edit:

```asm
JE ENDFILE
MOV AL,[CHAR]
CMP AL,10
```

Remove this exact source at old physical positions 144–144:

```asm
JE LINEFEED
```

Replace it with:

```asm
JNE ZREADLINE2
JMP LINEFEED
ZREADLINE2:
```

The following old source stays in place:

```asm
MOV AH,0
MOV [SKIPLF],AH
```

### Change 47 near `READCHAR:`

Unchanged source immediately before this edit:

```asm
READCHAR:
CALL NEXTBYTE
CMP AX,0
```

Remove this exact source at old physical positions 141–141:

```asm
JE ENDFILE
```

Replace it with:

```asm
JNE ZREADLINE1
JMP ENDFILE
ZREADLINE1:
```

The following old source stays in place:

```asm
MOV AL,[CHAR]
CMP AL,10
```

### Change 48 near `PASSVALID:`

Unchanged source immediately before this edit:

```asm
CALL FLUSH
CALL CLOSEOUT
CALL COMMIT
```

Insert after old physical line 59.

Insert:

```asm
CALL MEMFREE
```

The following old source stays in place:

```asm
MOV DX,OKMSG
CALL TEXT
```

### Change 49 near `ROOM:`

Unchanged source immediately before this edit:

```asm
MOV AX,7
JMP ERROR
ROOM:
```

Insert after old physical line 8.

Insert:

```asm
CALL MEMINIT
CALL EARLYTEST
```

The following old source stays in place:

```asm
CALL PREFLIGHT
MOV AL,1
```

## Build the stopping point

```dos
COPY A13.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 03722 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A13.COM
```

VIEW.BAS must report A13.COM length 3722 bytes. Keep that executable and source together.

## Acceptance check

Create T13.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T13.ASM SOURCE.ASM
```

```dos
CHECK A13
```

Require:

```text
MEMORY READY
OK RESULT.COM 00011 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **11 bytes** and these complete contents:

```text
B2 41 B4 02 CD 21 B8 00 4C CD 21
```

This fixture is a complete program. Save it before another assembly and execute it:

```dos
COPY RESULT.COM TRY.COM
CHECK TRY
```

It displays "A" and the checker reports PASS.

## A rejection check

Create X13.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X13.ASM SOURCE.ASM
CHECK A13
```

Require:

```text
MEMORY READY
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check ES at helper exits, the saved page segment and offset, record padding, and the complete spelling comparison. Check carry after every DOS memory call. A successful allocation does not initialize its contents.
