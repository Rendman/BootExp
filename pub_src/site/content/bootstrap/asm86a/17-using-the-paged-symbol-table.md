+++
title = "17 \u00b7 Using the paged symbol table"
weight = 17
description = "Move definition and value resolution onto the new record helpers."
download = "A17.ASM"
+++

The table is ready to replace the seed's fixed in-segment records.

## The working parts

DEFINE validates a name and register exclusion, refuses duplicates, and creates at most 8192 records. Pass two requires the stored value and kind to agree and marks each definition seen once. DEFSEEN must equal SYMC at the end, in addition to the final PC check.

SYMBOLVALUE finds a record and returns its word value. An unresolved pass-one reference returns a placeholder and sets UNRESOLVED; pass two rejects it. The line/token and I/O addresses still use the seed layout here, so the new table can be checked independently of another buffer move.

## Enter the source

Copy `A16.ASM` to `A17.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `HASHSEG:`

Unchanged source immediately before this edit:

```asm
HASHSEG:
DW 0
```

Remove this exact source at old physical positions 1831–1832:

```asm
TESTNAME:
DB 80,65,71,69,68,0
```

Replace it with:

```asm
UNRESOLVED:
DB 0
```

### Change 2 near `DEFTYPE:`

Unchanged source immediately before this edit:

```asm
DEFTYPE:
DW 0
```

Insert after old physical line 1824.

Insert:

```asm
DEFSEEN:
DW 0
```

The following old source stays in place:

```asm
MEMSEGS:
DW 0,0,0,0,0,0,0,0
```

### Change 3 near `SYMC:`

Unchanged source immediately before this edit:

```asm

SYMC:
DW 0
```

Remove this exact source at old physical positions 1632–1634:

```asm

SYMNEXT:
DW 12288
```

There is no replacement source.

The following old source stays in place:

```asm

TOKLEN:
```

### Change 4 near `EARLYTEST:`

Unchanged source immediately before this edit:

```asm
MOV AX,8192
MOV [SYMID],AX
MOV AX,[SYMID]
```

Remove this exact source at old physical positions 1588–1598:

```asm
CALL RECORDWRITE
CALL SYMLOOK
MOV AX,[SYMID]
CALL SYMPTR
ADD BX,32
MOV AX,ES:[BX]
MOV DX,CS
MOV ES,DX
CALL NUMBER
MOV DX,NEWLINE
CALL TEXT
```

Replace it with:

```asm
MOV ES:[BX],AX
```

The following old source stays in place:

```asm
RET
```

### Change 5 near `EARLYTEST:`

Unchanged source immediately before this edit:

```asm
MOV DI,4080H
CALL COPYZ
POP SI
```

Remove this exact source at old physical positions 1575–1586:

```asm
CALL SYMLOOK
MOV AX,8192
MOV [SYMID],AX
MOV AX,12345
MOV [DEFVALUE],AX
MOV AX,0
MOV [DEFTYPE],AX
MOV [HEADID],AX
MOV [BUCKET],AX
CALL SYMLOOK
MOV AX,8192
MOV [SYMID],AX
```

Replace it with:

```asm
MOV BX,[RECORDPTR]
ADD BX,32
MOV AX,[DEFVALUE]
MOV ES:[BX],AX
ADD BX,2
MOV AX,[HEADID]
MOV ES:[BX],AX
ADD BX,4
MOV AX,[DEFTYPE]
MOV ES:[BX],AX
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,[BUCKET]
```

The following old source stays in place:

```asm
MOV AX,[SYMID]
CALL RECORDWRITE
```

### Change 6 near `EARLYTEST:`

Unchanged source immediately before this edit:

```asm

EARLYTEST:
PUSH SI
```

Remove this exact source at old physical positions 1571–1572:

```asm
MOV SI,TESTNAME
MOV DI,4080H
```

Replace it with:

```asm
MOV SI,4080H
```

The following old source stays in place:

```asm
CALL COPYZ
POP SI
```

### Change 7 near `SYMFOUND:`

Unchanged source immediately before this edit:

```asm
POP SI
RET
```

Remove this exact source at old physical positions 1569–1569:

```asm
EARLYTEST:
```

Replace it with:

```asm
RECORDWRITE:
CALL SYMPTR
MOV DI,BX
MOV CX,40
MOV AL,0
DEFINITIONCLEAR:
STOSB
DEC CX
JNE DEFINITIONCLEAR
MOV DI,[RECORDPTR]
```

The following old source stays in place:

```asm
PUSH SI
MOV SI,TESTNAME
```

### Change 8 near `SYMOFFSET:`

Unchanged source immediately before this edit:

```asm
MOV [RECORDPTR],BX
RET
```

Remove this exact source at old physical positions 1475–1505:

```asm
RECORDWRITE:
CALL SYMPTR
MOV DI,BX
MOV CX,40
MOV AL,0
DEFINITIONCLEAR:
STOSB
DEC CX
JNE DEFINITIONCLEAR
MOV DI,[RECORDPTR]
PUSH SI
MOV SI,4080H
CALL COPYZ
POP SI
MOV BX,[RECORDPTR]
ADD BX,32
MOV AX,[DEFVALUE]
MOV ES:[BX],AX
ADD BX,2
MOV AX,[HEADID]
MOV ES:[BX],AX
ADD BX,4
MOV AX,[DEFTYPE]
MOV ES:[BX],AX
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,[BUCKET]
MOV AX,[SYMID]
MOV ES:[BX],AX
RET
```

There is no replacement source.

The following old source stays in place:

```asm
SYMLOOK:
PUSH SI
```

### Change 9 near `STNEXT7:`

Unchanged source immediately before this edit:

```asm
JNE STNEXT8
CALL SHORTJUMP
RET
```

Remove this exact source at old physical positions 687–687:

```asm
STNEXT8:
```

Replace it with:

```asm
DISPATCH8:
```

The following old source stays in place:

```asm
CALL TWOOPERANDS
CALL FINISH
```

### Change 10 near `STNEXT7:`

Unchanged source immediately before this edit:

```asm
RET
STNEXT7:
CMP AL,8
```

Remove this exact source at old physical positions 684–684:

```asm
JNE STNEXT8
```

Replace it with:

```asm
JNE DISPATCH8
```

The following old source stays in place:

```asm
CALL SHORTJUMP
RET
```

### Change 11 near `STNEXT6:`

Unchanged source immediately before this edit:

```asm
JNE STNEXT7
CALL NEARJUMP
RET
```

Remove this exact source at old physical positions 682–682:

```asm
STNEXT7:
```

Replace it with:

```asm
DISPATCH7:
```

The following old source stays in place:

```asm
CMP AL,8
JNE STNEXT8
```

### Change 12 near `STNEXT6:`

Unchanged source immediately before this edit:

```asm
RET
STNEXT6:
CMP AL,7
```

Remove this exact source at old physical positions 679–679:

```asm
JNE STNEXT7
```

Replace it with:

```asm
JNE DISPATCH7
```

The following old source stays in place:

```asm
CALL NEARJUMP
RET
```

### Change 13 near `STNEXT5:`

Unchanged source immediately before this edit:

```asm
JNE STNEXT6
CALL INTERRUPT
RET
```

Remove this exact source at old physical positions 677–677:

```asm
STNEXT6:
```

Replace it with:

```asm
DISPATCH6:
```

The following old source stays in place:

```asm
CMP AL,7
JNE STNEXT7
```

### Change 14 near `STNEXT5:`

Unchanged source immediately before this edit:

```asm
RET
STNEXT5:
CMP AL,6
```

Remove this exact source at old physical positions 674–674:

```asm
JNE STNEXT6
```

Replace it with:

```asm
JNE DISPATCH6
```

The following old source stays in place:

```asm
CALL INTERRUPT
RET
```

### Change 15 near `STNEXT2:`

Unchanged source immediately before this edit:

```asm
JNE STNEXT5
CALL SINGLE
RET
```

Remove this exact source at old physical positions 672–672:

```asm
STNEXT5:
```

Replace it with:

```asm
DISPATCH5:
```

The following old source stays in place:

```asm
CMP AL,6
JNE STNEXT6
```

### Change 16 near `STNEXT2:`

Unchanged source immediately before this edit:

```asm
RET
STNEXT2:
CMP AL,5
```

Remove this exact source at old physical positions 669–669:

```asm
JNE STNEXT5
```

Replace it with:

```asm
JNE DISPATCH5
```

The following old source stays in place:

```asm
CALL SINGLE
RET
```

### Change 17 near `STNEXT1:`

Unchanged source immediately before this edit:

```asm
JNE STNEXT2
CALL FIXED
RET
```

Remove this exact source at old physical positions 667–667:

```asm
STNEXT2:
```

Replace it with:

```asm
DISPATCH2:
```

The following old source stays in place:

```asm
CMP AL,5
JNE STNEXT5
```

### Change 18 near `STNEXT1:`

Unchanged source immediately before this edit:

```asm
RET
STNEXT1:
CMP AL,2
```

Remove this exact source at old physical positions 664–664:

```asm
JNE STNEXT2
```

Replace it with:

```asm
JNE DISPATCH2
```

The following old source stays in place:

```asm
CALL FIXED
RET
```

### Change 19 near `STOPFOUND:`

Unchanged source immediately before this edit:

```asm
JNE STNEXT1
CALL DATAITEM
RET
```

Remove this exact source at old physical positions 662–662:

```asm
STNEXT1:
```

Replace it with:

```asm
DISPATCH1:
```

The following old source stays in place:

```asm
CMP AL,2
JNE STNEXT2
```

### Change 20 near `STOPFOUND:`

Unchanged source immediately before this edit:

```asm
MOV [OP],AL
MOV AL,[TYPE]
CMP AL,1
```

Remove this exact source at old physical positions 659–659:

```asm
JNE STNEXT1
```

Replace it with:

```asm
JNE DISPATCH1
```

The following old source stays in place:

```asm
CALL DATAITEM
RET
```

### Change 21 near `INSTRUCTION:`

Unchanged source immediately before this edit:

```asm
MOV AX,8
CALL LOOK
CMP BX,0
```

Remove this exact source at old physical positions 647–650:

```asm
JNE STOPFOUND
MOV AX,1
JMP ERROR
STOPFOUND:
```

Replace it with:

```asm
JNE ZSTATEMEN1
JMP SYNTAXBAD
ZSTATEMEN1:
```

The following old source stays in place:

```asm
ADD BX,6
MOV AL,[BX]
```

### Change 22 near `AFTERWORD:`

Unchanged source immediately before this edit:

```asm
JE AFTERWORD
CMP AL,58
JNE INSTRUCTION
```

Insert after old physical line 636.

Insert:

```asm
MOV AX,[PC]
MOV [DEFVALUE],AX
MOV AX,0
MOV [DEFTYPE],AX
```

The following old source stays in place:

```asm
CALL DEFINE
CALL FINISH
```

### Change 23 near `ZDEFINE4:`

Unchanged source immediately before this edit:

```asm
MOV [SYMNEXT],AX
MOV AX,[SYMC]
INC AX
```

Remove this exact source at old physical positions 539–550:

```asm
MOV [SYMC],AX
RET
CHECKDEFINE:
CMP BX,0
JE DEFINEBAD
ADD BX,18
MOV AX,[BX]
MOV DX,[PC]
CMP AX,DX
JE DEFINEEND
JMP DEFINEBAD
DEFINEEND:
```

Replace it with:

```asm
MOV [DEFSEEN],AX
DEFINITIONEND:
MOV AX,CS
MOV ES,AX
```

The following old source stays in place:

```asm
RET
TABLEFULL:
```

### Change 24 near `ZDEFINE3:`

Unchanged source immediately before this edit:

```asm
JE ZDEFINE3
JMP DEFINEBAD
ZDEFINE3:
```

Remove this exact source at old physical positions 520–537:

```asm
MOV AX,[SYMC]
CMP AX,2048
JB ZDEFINE4
JMP TABLEFULL
ZDEFINE4:
MOV DI,[SYMNEXT]
PUSH SI
MOV SI,4080H
CALL COPYZ
POP SI
MOV BX,[SYMNEXT]
ADD BX,18
MOV AX,[PC]
MOV [BX],AX
MOV AX,[SYMNEXT]
ADD AX,20
MOV [SYMNEXT],AX
MOV AX,[SYMC]
```

Replace it with:

```asm
MOV AX,1
MOV ES:[BX],AX
ADD BX,2
MOV AX,ES:[BX]
MOV DX,[DEFTYPE]
CMP AX,DX
JNE DEFINEBAD
MOV AX,[DEFSEEN]
```

The following old source stays in place:

```asm
INC AX
MOV [SYMC],AX
```

### Change 25 near `ZDEFINE2:`

Unchanged source immediately before this edit:

```asm
JE ZDEFINE2
JMP CHECKDEFINE
ZDEFINE2:
```

Remove this exact source at old physical positions 516–516:

```asm
CMP BX,0
```

Replace it with:

```asm
ADD BX,4
MOV AX,ES:[BX]
CMP AX,0
```

The following old source stays in place:

```asm
JE ZDEFINE3
JMP DEFINEBAD
```

### Change 26 near `ZDEFINE1:`

Unchanged source immediately before this edit:

```asm
MOV AL,[PASS]
CMP AL,1
JE ZDEFINE2
```

Remove this exact source at old physical positions 514–514:

```asm
JMP CHECKDEFINE
```

Replace it with:

```asm
JMP DEFINEBAD
```

The following old source stays in place:

```asm
ZDEFINE2:
CMP BX,0
```

### Change 27 near `ZDEFINE1:`

Unchanged source immediately before this edit:

```asm
JE ZDEFINE1
JMP DEFINEBAD
ZDEFINE1:
```

Remove this exact source at old physical positions 507–512:

```asm
MOV BX,5000H
MOV CX,[SYMC]
MOV AX,20
CALL LOOK
MOV AL,[PASS]
CMP AL,1
```

Replace it with:

```asm
CALL SYMPTR
ADD BX,32
MOV AX,ES:[BX]
MOV DX,[DEFVALUE]
CMP AX,DX
```

The following old source stays in place:

```asm
JE ZDEFINE2
JMP CHECKDEFINE
```

### Change 28 near `DEFINE:`

Unchanged source immediately before this edit:

```asm
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
```

Remove this exact source at old physical positions 504–504:

```asm
JE ZDEFINE1
```

Replace it with:

```asm
JE DEFINITIONNAME
JMP DEFINEBAD
DEFINITIONNAME:
CALL SYMLOOK
MOV AL,[PASS]
CMP AL,1
JNE CHECKDEFINE
MOV AX,[SYMID]
CMP AX,0
JE DEFINITIONNEW
JMP DEFINEBAD
DEFINITIONNEW:
MOV AX,[SYMC]
CMP AX,8192
JB DEFINITIONROOM
JMP TABLEFULL
DEFINITIONROOM:
INC AX
MOV [SYMC],AX
MOV [SYMID],AX
CALL RECORDWRITE
JMP DEFINITIONEND
CHECKDEFINE:
MOV AX,[SYMID]
CMP AX,0
JNE ZDEFINE1
```

The following old source stays in place:

```asm
JMP DEFINEBAD
ZDEFINE1:
```

### Change 29 near `NOTDEFINED:`

Unchanged source immediately before this edit:

```asm
MOV AL,[PASS]
CMP AL,1
JNE VALUEBAD
```

Insert after old physical line 493.

Insert:

```asm
MOV AL,1
MOV [UNRESOLVED],AL
```

The following old source stays in place:

```asm
MOV AX,0
RET
```

### Change 30 near `SYMBOLVALUE:`

Unchanged source immediately before this edit:

```asm
CALL LOOK
CMP BX,0
JE NOTDEFINED
```

Remove this exact source at old physical positions 487–488:

```asm
ADD BX,18
MOV AX,[BX]
```

Replace it with:

```asm
CALL SYMPTR
ADD BX,32
MOV AX,ES:[BX]
MOV DX,CS
MOV ES,DX
```

The following old source stays in place:

```asm
RET
NOTDEFINED:
```

### Change 31 near `SYMBOLVALUE:`

Unchanged source immediately before this edit:

```asm
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
```

Remove this exact source at old physical positions 480–485:

```asm
JNE VALUEBAD
MOV BX,5000H
MOV CX,[SYMC]
MOV AX,20
CALL LOOK
CMP BX,0
```

Replace it with:

```asm
JE ZSYMBOLVA1
JMP VALUEBAD
ZSYMBOLVA1:
CALL SYMLOOK
MOV AX,[SYMID]
CMP AX,0
```

The following old source stays in place:

```asm
JE NOTDEFINED
ADD BX,18
```

### Change 32 near `VALIDNAME:`

Unchanged source immediately before this edit:

```asm
RET

VALIDNAME:
```

Insert after old physical line 353.

Insert:

```asm
MOV AX,[TOKLEN]
CMP AX,31
JBE NAMELIMIT
JMP SYMBOLBAD
NAMELIMIT:
```

The following old source stays in place:

```asm
PUSH SI
MOV SI,4080H
```

### Change 33 near `PASSVALID:`

Unchanged source immediately before this edit:

```asm
CALL CLOSEOUT
CALL COMMIT
CALL MEMFREE
```

Insert after old physical line 62.

Insert:

```asm
MOV AL,[CLEANFAIL]
CMP AL,0
JE FINALCLEAN
MOV AX,7
JMP ERROR
FINALCLEAN:
```

The following old source stays in place:

```asm
MOV DX,OKMSG
CALL TEXT
```

### Change 34 near `PASSVALID:`

Unchanged source immediately before this edit:

```asm
MOV AX,3
JMP ERROR
PASSVALID:
```

Insert after old physical line 58.

Insert:

```asm
MOV AX,[DEFSEEN]
MOV DX,[SYMC]
CMP AX,DX
JE DEFINITIONCOUNT
MOV AX,3
JMP ERROR
DEFINITIONCOUNT:
```

The following old source stays in place:

```asm
CALL FLUSH
CALL CLOSEOUT
```

### Change 35 near `PASSSTART:`

Unchanged source immediately before this edit:

```asm
MOV [RDPOS],AX
MOV [RDLEN],AX
MOV [OUTCNT],AX
```

Insert after old physical line 25.

Insert:

```asm
MOV [DEFSEEN],AX
```

The following old source stays in place:

```asm
MOV [ENDED],AL
MOV [SKIPLF],AL
```

### Change 36 near `ROOM:`

Unchanged source immediately before this edit:

```asm
MOV [PASS],AL
MOV AX,0
MOV [SYMC],AX
```

Remove this exact source at old physical positions 16–17:

```asm
MOV AX,5000H
MOV [SYMNEXT],AX
```

There is no replacement source.

The following old source stays in place:

```asm
PASSSTART:
MOV AX,100H
```

### Change 37 near `ROOM:`

Unchanged source immediately before this edit:

```asm
JMP ERROR
ROOM:
CALL MEMINIT
```

Remove this exact source at old physical positions 10–10:

```asm
CALL EARLYTEST
```

There is no replacement source.

The following old source stays in place:

```asm
CALL PREFLIGHT
MOV AL,1
```

## Build the stopping point

```dos
COPY A17.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 04057 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A17.COM
```

VIEW.BAS must report A17.COM length 4057 bytes. Keep that executable and source together.

## Acceptance check

Create T17.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
HERE:
DW HERE
```

```dos
COPY T17.ASM SOURCE.ASM
```

```dos
CHECK A17
```

Require:

```text
OK RESULT.COM 00002 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **2 bytes** and these complete contents:

```text
00 01
```

This result is an encoding or data exercise. Inspect its bytes; do not execute it.

## A rejection check

Create X17.ASM with this separate source:

```asm
SAME:
SAME:
```

```dos
COPY X17.ASM SOURCE.ASM
CHECK A17
```

Require:

```text
ERROR 00002 CODE 3
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

## Fill the symbol table

Enter SYMS.BAS as a source-text exercise:

```basic
10 N=8192
20 OPEN "SOURCE.ASM" FOR OUTPUT AS #1
30 FOR I=0 TO N-1
40 PRINT #1,"S"+MID$(STR$(I),2)+":"
50 NEXT I
60 PRINT #1,"DW S0,S"+MID$(STR$(N-1),2)
70 CLOSE #1
80 PRINT "SOURCE.ASM READY"
```

Run GWBASIC SYMS.BAS, require SOURCE.ASM READY, and use SYSTEM to return to DOS. BASIC closes the text file with its normal source Control-Z marker. Run CHECK A17. Require `OK RESULT.COM 00004 bytes` and PASS. VIEW.BAS must show `00 01 00 01`: all definitions have value 0100H because none emits bytes. This file is data, not an executable.

Keep a copy of that result. Change BASIC line 10 to `10 N=8193` and RUN again. CHECK A17 must report `ERROR 08193 CODE 5` and FAIL, preserving the four-byte result. Restore the stated accepted N before another run. The BASIC program creates assembly source, never executable bytes.

An unexpected PASS fails this rejection test.

## If the result differs

Check ES at helper exits, the saved page segment and offset, record padding, and the complete spelling comparison. Check carry after every DOS memory call. A successful allocation does not initialize its contents.
