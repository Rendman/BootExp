+++
title = "06 \u00b7 Room for names and physical lines"
weight = 6
description = "Move parser and file buffers above a generous resident-image area."
download = "A18.ASM"
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/18-room-for-names-and-physical-lines/"
+++

The names have moved out of the main segment. I spread the memory sketch across another notebook page and give the code, line, token, file blocks and stack their marked ranges. There is room to retain longer spellings and read longer source lines, provided every copy stays within its boundary.

## The working parts

The main segment reserves 0100H through BFFFH for code and static data, C800H through CBFFH for the line, CC00H through CC3FH for a token, and separate 4 KB I/O blocks at D000H and E000H. The stack reservation remains F000H through FFFFH.

Names may contain thirty-one characters; tokens may contain sixty-three; a physical line may contain 1023 characters. The 8192 forty-byte symbol records live outside the main segment. Both the scanner and symbol validator check their own bounds before copying.

## Enter the source

Copy `A17.ASM` to `A18.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `DEFINITIONCLEAR:`

Unchanged source immediately before this edit:

```asm
JNE DEFINITIONCLEAR
MOV DI,[RECORDPTR]
PUSH SI
```

Remove this exact source at old physical positions 1587–1587:

```asm
MOV SI,4080H
```

Replace it with:

```asm
MOV SI,0CC00H
```

The following old source stays in place:

```asm
CALL COPYZ
POP SI
```

### Change 2 near `ZSYMLOOK1:`

Unchanged source immediately before this edit:

```asm
ZSYMLOOK1:
CALL SYMPTR
MOV DI,BX
```

Remove this exact source at old physical positions 1551–1551:

```asm
MOV SI,4080H
```

Replace it with:

```asm
MOV SI,0CC00H
```

The following old source stays in place:

```asm
SYMCHECKCHAR:
LODSB
```

### Change 3 near `SYMLOOK:`

Unchanged source immediately before this edit:

```asm

SYMLOOK:
PUSH SI
```

Remove this exact source at old physical positions 1515–1515:

```asm
MOV SI,4080H
```

Replace it with:

```asm
MOV SI,0CC00H
```

The following old source stays in place:

```asm
MOV AX,0
SYMHASH:
```

### Change 4 near `SEGES:`

Unchanged source immediately before this edit:

```asm
JMP TWOBAD
SEGES:
CALL SCAN
```

Remove this exact source at old physical positions 1330–1330:

```asm
MOV AL,[4080H]
```

Replace it with:

```asm
MOV AL,[0CC00H]
```

The following old source stays in place:

```asm
CMP AL,91
JE SEGMEMORY
```

### Change 5 near `SEGOPERAND:`

Unchanged source immediately before this edit:

```asm
MOV [SEGCODE],AX
PUSH SI
CALL SCAN
```

Remove this exact source at old physical positions 1318–1318:

```asm
MOV AL,[4080H]
```

Replace it with:

```asm
MOV AL,[0CC00H]
```

The following old source stays in place:

```asm
CMP AL,58
JE ZSEGOPERA1
```

### Change 6 near `FLUSH:`

Unchanged source immediately before this edit:

```asm
CMP CX,0
JE FLUSHDONE
MOV BX,[OUTHANDLE]
```

Remove this exact source at old physical positions 1169–1169:

```asm
MOV DX,4600H
```

Replace it with:

```asm
MOV DX,0E000H
```

The following old source stays in place:

```asm
MOV AH,40H
INT 21H
```

### Change 7 near `EMITROOM:`

Unchanged source immediately before this edit:

```asm
MOV BX,[OUTCNT]
INC BX
MOV [OUTCNT],BX
```

Remove this exact source at old physical positions 1052–1052:

```asm
CMP BX,1024
```

Replace it with:

```asm
CMP BX,4096
```

The following old source stays in place:

```asm
JB COUNTBYTE
CALL FLUSH
```

### Change 8 near `EMITROOM:`

Unchanged source immediately before this edit:

```asm
CMP AH,2
JNE COUNTBYTE
MOV BX,[OUTCNT]
```

Remove this exact source at old physical positions 1047–1047:

```asm
ADD BX,4600H
```

Replace it with:

```asm
ADD BX,0E000H
```

The following old source stays in place:

```asm
MOV [BX],AL
MOV BX,[OUTCNT]
```

### Change 9 near `TWOOPERANDS:`

Unchanged source immediately before this edit:

```asm
MOV AX,[VAL]
MOV [V1],AX
CALL SCAN
```

Remove this exact source at old physical positions 850–850:

```asm
MOV AL,[4080H]
```

Replace it with:

```asm
MOV AL,[0CC00H]
```

The following old source stays in place:

```asm
CMP AL,44
JE ZTWOOPERA1
```

### Change 10 near `FINISH:`

Unchanged source immediately before this edit:

```asm

FINISH:
CALL SCAN
```

Remove this exact source at old physical positions 829–829:

```asm
MOV AL,[4080H]
```

Replace it with:

```asm
MOV AL,[0CC00H]
```

The following old source stays in place:

```asm
CMP AL,0
JE FINISHED
```

### Change 11 near `DATASEP:`

Unchanged source immediately before this edit:

```asm
CALL BYTEVALUE
DATASEP:
CALL SCAN
```

Remove this exact source at old physical positions 745–745:

```asm
MOV AL,[4080H]
```

Replace it with:

```asm
MOV AL,[0CC00H]
```

The following old source stays in place:

```asm
CMP AL,44
JE DATAITEM
```

### Change 12 near `STATEMENT:`

Unchanged source immediately before this edit:

```asm

STATEMENT:
CALL SCAN
```

Remove this exact source at old physical positions 661–661:

```asm
MOV AL,[4080H]
```

Replace it with:

```asm
MOV AL,[0CC00H]
```

The following old source stays in place:

```asm
CMP AL,0
JNE STWORD
```

### Change 13 near `MEMORYEND:`

Unchanged source immediately before this edit:

```asm
MOV [REG],AL
MEMORYEND:
CALL SCAN
```

Remove this exact source at old physical positions 649–649:

```asm
MOV AL,[4080H]
```

Replace it with:

```asm
MOV AL,[0CC00H]
```

The following old source stays in place:

```asm
CMP AL,93
JE MEMORYOK
```

### Change 14 near `MEMORY:`

Unchanged source immediately before this edit:

```asm
MOV AX,[4080H]
CMP AX,5842H
JNE DIRECTMEM
```

Remove this exact source at old physical positions 636–636:

```asm
MOV AL,[4082H]
```

Replace it with:

```asm
MOV AL,[0CC02H]
```

The following old source stays in place:

```asm
CMP AL,0
JNE DIRECTMEM
```

### Change 15 near `MEMORY:`

Unchanged source immediately before this edit:

```asm

MEMORY:
CALL SCAN
```

Remove this exact source at old physical positions 633–633:

```asm
MOV AX,[4080H]
```

Replace it with:

```asm
MOV AX,[0CC00H]
```

The following old source stays in place:

```asm
CMP AX,5842H
JNE DIRECTMEM
```

### Change 16 near `OPERAND:`

Unchanged source immediately before this edit:

```asm
MOV AL,0
MOV [PREFIX],AL
CALL SCAN
```

Remove this exact source at old physical positions 598–598:

```asm
MOV AL,[4080H]
```

Replace it with:

```asm
MOV AL,[0CC00H]
```

The following old source stays in place:

```asm
CMP AL,91
JNE ZOPERAND1
```

### Change 17 near `LITERAL:`

Unchanged source immediately before this edit:

```asm
PUSH SI
MOV SI,4080H
MOV DI,[TOKLEN]
```

Remove this exact source at old physical positions 423–423:

```asm
ADD DI,4080H
```

Replace it with:

```asm
ADD DI,0CC00H
```

The following old source stays in place:

```asm
MOV BX,DI
DEC BX
```

### Change 18 near `LITERAL:`

Unchanged source immediately before this edit:

```asm
JMP SYMBOLVALUE
LITERAL:
PUSH SI
```

Remove this exact source at old physical positions 421–421:

```asm
MOV SI,4080H
```

Replace it with:

```asm
MOV SI,0CC00H
```

The following old source stays in place:

```asm
MOV DI,[TOKLEN]
ADD DI,4080H
```

### Change 19 near `VALUE:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

VALUE:
```

Remove this exact source at old physical positions 412–412:

```asm
MOV AL,[4080H]
```

Replace it with:

```asm
MOV AL,[0CC00H]
```

The following old source stays in place:

```asm
CMP AL,48
JB WORDVALUE
```

### Change 20 near `NAMELIMIT:`

Unchanged source immediately before this edit:

```asm
JMP SYMBOLBAD
NAMELIMIT:
PUSH SI
```

Remove this exact source at old physical positions 377–377:

```asm
MOV SI,4080H
```

Replace it with:

```asm
MOV SI,0CC00H
```

The following old source stays in place:

```asm
LODSB
CMP AL,95
```

### Change 21 near `ZLOOK1:`

Unchanged source immediately before this edit:

```asm
JMP LOOKMISS
ZLOOK1:
MOV DI,BP
```

Remove this exact source at old physical positions 330–330:

```asm
MOV SI,4080H
```

Replace it with:

```asm
MOV SI,0CC00H
```

The following old source stays in place:

```asm
LOOKCHAR:
LODSB
```

### Change 22 near `SCANDONE:`

Unchanged source immediately before this edit:

```asm
DEC SI
SCANDONE:
MOV AX,DI
```

Remove this exact source at old physical positions 308–308:

```asm
SUB AX,4080H
```

Replace it with:

```asm
SUB AX,0CC00H
```

The following old source stays in place:

```asm
MOV [TOKLEN],AX
MOV AL,0
```

### Change 23 near `ZSCAN7:`

Unchanged source immediately before this edit:

```asm
JE SCANBACK
CMP AL,93
JE SCANBACK
```

Remove this exact source at old physical positions 300–300:

```asm
CMP DI,4090H
```

Replace it with:

```asm
CMP DI,0CC3FH
```

The following old source stays in place:

```asm
JAE TOKENBAD
STOSB
```

### Change 24 near `SCAN:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

SCAN:
```

Remove this exact source at old physical positions 252–252:

```asm
MOV DI,4080H
```

Replace it with:

```asm
MOV DI,0CC00H
```

The following old source stays in place:

```asm
SCANSPACE:
LODSB
```

### Change 25 near `ZREADLINE4:`

Unchanged source immediately before this edit:

```asm
JNE ZREADLINE4
JMP ENDFILE
ZREADLINE4:
```

Remove this exact source at old physical positions 179–179:

```asm
CMP BP,120
```

Replace it with:

```asm
CMP BP,1023
```

The following old source stays in place:

```asm
JB ZREADLINE5
JMP READFULL
```

### Change 26 near `READLINE:`

Unchanged source immediately before this edit:

```asm
RET

READLINE:
```

Remove this exact source at old physical positions 151–151:

```asm
MOV DI,4000H
```

Replace it with:

```asm
MOV DI,0C800H
```

The following old source stays in place:

```asm
MOV BP,0
MOV AL,[ENDED]
```

### Change 27 near `BUFFERBYTE:`

Unchanged source immediately before this edit:

```asm
JE BUFFEREND
BUFFERBYTE:
MOV BX,[RDPOS]
```

Remove this exact source at old physical positions 138–138:

```asm
ADD BX,4200H
```

Replace it with:

```asm
ADD BX,0D000H
```

The following old source stays in place:

```asm
MOV AL,[BX]
MOV [CHAR],AL
```

### Change 28 near `NEXTBYTE:`

Unchanged source immediately before this edit:

```asm
CMP AX,DX
JB BUFFERBYTE
MOV BX,[HANDLE]
```

Remove this exact source at old physical positions 124–125:

```asm
MOV DX,4200H
MOV CX,1024
```

Replace it with:

```asm
MOV DX,0D000H
MOV CX,4096
```

The following old source stays in place:

```asm
MOV AH,3FH
INT 21H
```

### Change 29 near `NEXTLINE:`

Unchanged source immediately before this edit:

```asm
CALL READLINE
CMP AX,0
JE PASSEND
```

Remove this exact source at old physical positions 37–37:

```asm
MOV SI,4000H
```

Replace it with:

```asm
MOV SI,0C800H
```

The following old source stays in place:

```asm
CALL STATEMENT
JMP NEXTLINE
```

## Build the stopping point

```dos
CHECK ASM1 A18.ASM RESULT.COM
```

Require `OK RESULT.COM 04455 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A18.COM
```

VIEW.BAS must report A18.COM length 4455 bytes. Keep that executable and source together.

## Acceptance check

Create T18.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
ABCDEFGHIJKLMNOPQRSTUVWXYZABCDE:
DW ABCDEFGHIJKLMNOPQRSTUVWXYZABCDE
```

```dos
CHECK A18 T18.ASM RESULT.COM
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

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X18.ASM with this separate source:

```asm
ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEF:
```

```dos
CHECK A18 X18.ASM RESULT.COM
```

Require:

```text
ERROR 00001 CODE 3
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with C:\DOS\FC.EXE /B if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check ES at helper exits, the saved page segment and offset, record padding, and the complete spelling comparison. Check carry after every DOS memory call. A successful allocation does not initialize its contents.
