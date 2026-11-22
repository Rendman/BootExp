+++
title = "13 \u00b7 The DB directive"
weight = 13
description = "Look up a mnemonic, then read its comma-separated byte values."
download = "AS13.ASM"
aliases = ["/bootstrap/asm86/14-the-db-directive/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/13-the-db-directive/"
+++

The trial inputs have been rows of numbers. I want to put a familiar line such as `DB 41H,42H,43H` in `SOURCE.ASM` and have ASM0 read it. The scanner, table search, value reader and output buffer can now do that job together.

**Starting source:** `AS12.ASM`. **Save as:** `AS13.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

STATEMENT takes SI at the beginning of a cleaned line. An empty token is an empty statement. Otherwise LOOK searches OPTAB, now containing the DB record. The record supplies TYPE, which selects the handler, and OP, its small parameter. The record count is an explicit part of the search.

A conditional branch reaches a nearby test label; CALL reaches the handler without the short branch's distance limit. The handler returns through STATEMENT to the source loop. This dispatcher changes the parser's working registers and TYPE and OP.

DATAITEM scans a value, converts it, and sends it through BYTEVALUE. It then scans either a comma, which requests another value, or the empty token at the end of the statement. A trailing comma requests a missing value and is rejected. Comments and spaces are handled by the existing reader and scanner.

The first complete byte statement can now hold a row of data. Unknown mnemonics and unexpected separators select syntax code 1. The output remains buffered until the source succeeds.

## Source changes

Copy `AS12.ASM` to `AS13.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `ERRCODE:`

Find the unique label `ERRCODE:`, then follow this unchanged source through its last displayed instruction:

```asm
ERRCODE:
DB 0
```

The edit begins immediately after that unchanged block.

Insert:

```asm
OPTAB:
DB 68,66,0,0,0,0,1,0
```

### Change 2 · `ERRCODE:`

Find the unique label `ERRCODE:`. Insert the new source immediately before this existing label:

```asm
ERRCODE:
```

Insert:

```asm
TYPE:
DB 0
OP:
DB 0
```

### Change 3 · `PASS:`

Find the unique label `PASS:`. Insert the new source immediately before this existing label:

```asm
PASS:
```

Insert:

```asm
STRIDE:
DW 0
```

### Change 4 · `FINISHED:`

Find the unique label `FINISHED:`. The old block below starts at that label.

Replace this existing source:

```asm
FINISHED:
```

With:

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

### Change 5 · `FINISH:`

Find the unique label `FINISH:`, then follow this unchanged source through its last displayed instruction:

```asm
FINISH:
CALL SCAN
MOV AL,[2300H]
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE FINISHED
```

With:

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

### Change 6 · `FINISH:`

Find the unique label `FINISH:`. The old block below starts at that label.

Replace this existing source:

```asm
FINISH:
```

With:

```asm
STATEMENT:
```

### Change 7 · `TOKENBAD:`

Find the unique label `TOKENBAD:`, then follow this unchanged source through its last displayed instruction:

```asm
TOKENBAD:
MOV AX,1
JMP ERROR
```

The edit begins immediately after that unchanged block.

Insert:

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

### Change 8 · `DRIVERLINE:`

Find the unique label `DRIVERLINE:`, then follow this unchanged source through its last displayed instruction:

```asm
DRIVERLINE:
CALL READLINE
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
CALL SCAN
CALL VALUE
CALL BYTEVALUE
CALL FINISH
JMP DRIVERLINE
DRIVERDONE:
```

With:

```asm
CALL STATEMENT
JMP NEXTLINE
PASSEND:
```

### Change 9 · `DRIVERLINE:`

Find the unique label `DRIVERLINE:`, then follow this unchanged source through its last displayed instruction:

```asm
DRIVERLINE:
CALL READLINE
CMP AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE DRIVERDONE
```

With:

```asm
JE PASSEND
```

### Change 10 · `DRIVERLINE:`

Find the unique label `DRIVERLINE:`. The old block below starts at that label.

Replace this existing source:

```asm
DRIVERLINE:
```

With:

```asm
NEXTLINE:
```

### Change 11 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
MOV AL,2
MOV [PASS],AL
MOV AX,100H
MOV [PC],AX
MOV AX,6000H
MOV [OUTPTR],AX
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AX,0
MOV [LINENO],AX
MOV [ENDED],AL
MOV [SKIPLF],AL
```

### Change 12 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
MOV AL,2
MOV [PASS],AL
```

The edit begins immediately after that unchanged block.

Insert:

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

Check the counted DB table record and the dispatch class. DATAITEM must require a new value after every comma, including a comma at the end of the line.
