+++
title = "13 \u00b7 The DB directive"
weight = 13
description = "Look up a mnemonic, then read its comma-separated byte values."
download = "AS13.ASM"
aliases = ["/bootstrap/asm86/14-the-db-directive/"]
download_group = "tools/asm0"
reader_names = 1
+++

We shall replace the one-number-per-line input with an assembly statement: DB followed by one or more byte values.

## How it works

STATEMENT takes SI at the beginning of a cleaned line. An empty token is an empty statement. Otherwise LOOK searches OPTAB, now containing the DB record. The record supplies TYPE, which selects the handler, and OP, its small parameter. The record count is an explicit part of the search.

A conditional branch reaches a nearby test label; CALL reaches the handler without the short branch's distance limit. The handler returns through STATEMENT to the source loop. This dispatcher changes the parser's working registers and TYPE and OP.

DATAITEM scans a value, converts it, and sends it through BYTEVALUE. It then scans either a comma, which requests another value, or the empty token at the end of the statement. A trailing comma requests a missing value and is rejected. Comments and spaces are handled by the existing reader and scanner.

The first complete byte statement can now hold a row of data. Unknown mnemonics and unexpected separators select syntax code 1. The output remains buffered until the source succeeds.

## Source changes

Copy `AS12.ASM` to `AS13.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `ERRCODE:`

Unchanged code immediately before this edit:

```asm

ERRCODE:
DB 0
```

Insert after old physical line 454, before the following old line.

Insert this source:

```asm

OPTAB:
DB 68,66,0,0,0,0,1,0
```

### Change 2: following `CHAR:`

Unchanged code immediately before this edit:

```asm
CHAR:
DB 0

```

Insert after old physical line 452, before the following old line.

Insert this source:

```asm
TYPE:
DB 0

OP:
DB 0

```

### Change 3: following `TOKLEN:`

Unchanged code immediately before this edit:

```asm
TOKLEN:
DW 0

```

Insert after old physical line 440, before the following old line.

Insert this source:

```asm
STRIDE:
DW 0

```

### Change 4: following `FINISH:`

Unchanged code immediately before this edit:

```asm
JE FINISHED
MOV AX,1
JMP ERROR
```

Remove these exact old lines (physical lines 311–311 of `AS12.ASM`):

```asm
FINISHED:
```

Put this source in their place:

```asm
STOPFOUND:
ADD BX,6
MOV AL,[BX]
MOV [TYPE],AL
INC BX
MOV AL,[BX]
MOV [OP],AL
MOV AL,[TYPE]
CMP AL,1
JNE STNEXT1
CALL DATAITEM
RET
STNEXT1:
JMP SYNTAXBAD
SYNTAXBAD:
MOV AX,1
JMP ERROR

DATAITEM:
CALL SCAN
CALL VALUE
CALL BYTEVALUE
DATASEP:
CALL SCAN
MOV AL,[2300H]
CMP AL,44
JE DATAITEM
CMP AL,0
JNE SYNTAXBAD
```

### Change 5: following `FINISH:`

Unchanged code immediately before this edit:

```asm
CALL SCAN
MOV AL,[2300H]
CMP AL,0
```

Remove these exact old lines (physical lines 308–308 of `AS12.ASM`):

```asm
JE FINISHED
```

Put this source in their place:

```asm
JNE STWORD
RET
STWORD:
MOV BX,OPTAB
MOV CX,1
MOV AX,8
CALL LOOK
CMP BX,0
JNE STOPFOUND
```

### Change 6: following `NUMBERBAD:`

Unchanged code immediately before this edit:

```asm
MOV AX,2
JMP ERROR

```

Remove these exact old lines (physical lines 304–304 of `AS12.ASM`):

```asm
FINISH:
```

Put this source in their place:

```asm
STATEMENT:
```

### Change 7: following `TOKENBAD:`

Unchanged code immediately before this edit:

```asm
MOV AX,1
JMP ERROR

```

Insert after old physical line 230, before the following old line.

Insert this source:

```asm
LOOK:
MOV [STRIDE],AX
PUSH SI
MOV BP,BX
LOOKNEXT:
CMP CX,0
JE LOOKMISS
MOV DI,BP
MOV SI,2300H
LOOKCHAR:
LODSB
MOV BX,DI
MOV DL,[BX]
CMP AL,DL
JNE LOOKSTEP
CMP AL,0
JE LOOKFOUND
INC DI
JMP LOOKCHAR
LOOKSTEP:
MOV AX,[STRIDE]
ADD BP,AX
DEC CX
JMP LOOKNEXT
LOOKFOUND:
MOV BX,BP
POP SI
RET
LOOKMISS:
MOV BX,0
POP SI
RET

```

### Change 8: following `DRIVERLINE:`

Unchanged code immediately before this edit:

```asm
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
```

Remove these exact old lines (physical lines 21–26 of `AS12.ASM`):

```asm
CALL SCAN
CALL VALUE
CALL BYTEVALUE
CALL FINISH
JMP DRIVERLINE
DRIVERDONE:
```

Put this source in their place:

```asm
CALL STATEMENT
JMP NEXTLINE
PASSEND:
```

### Change 9: following `DRIVERLINE:`

Unchanged code immediately before this edit:

```asm
DRIVERLINE:
CALL READLINE
CMP AX,0
```

Remove these exact old lines (physical lines 19–19 of `AS12.ASM`):

```asm
JE DRIVERDONE
```

Put this source in their place:

```asm
JE PASSEND
```

### Change 10: following `ROOM:`

Unchanged code immediately before this edit:

```asm
MOV AX,6000H
MOV [OUTPTR],AX
CALL OPENFILE
```

Remove these exact old lines (physical lines 16–16 of `AS12.ASM`):

```asm
DRIVERLINE:
```

Put this source in their place:

```asm
NEXTLINE:
```

### Change 11: following `ROOM:`

Unchanged code immediately before this edit:

```asm
MOV [PC],AX
MOV AX,6000H
MOV [OUTPTR],AX
```

Insert after old physical line 14, before the following old line.

Insert this source:

```asm
MOV AX,0
MOV [LINENO],AX
MOV [ENDED],AL
MOV [SKIPLF],AL
```

### Change 12: following `ROOM:`

Unchanged code immediately before this edit:

```asm
ROOM:
MOV AL,2
MOV [PASS],AL
```

Insert after old physical line 10, before the following old line.

Insert this source:

```asm
PASSSTART:
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS13.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1068 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS13.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T13.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
DB 41H,42H,43H
```

```dos
COPY T13.ASM SOURCE.ASM
```

```dos
CHECK AS13
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00003 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **3 bytes** with these hexadecimal bytes:

```text
41 42 43
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X13.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
NOPE 1
```

```dos
COPY X13.ASM SOURCE.ASM
CHECK AS13
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 1
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
