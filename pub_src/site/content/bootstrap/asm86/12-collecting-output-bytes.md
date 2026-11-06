+++
title = "12 \u00b7 Collecting output bytes"
weight = 12
description = "Count loaded offsets while retaining bytes in a separate buffer."
download = "AS12.ASM"
download_group = "tools/asm0"
reader_names = 1
+++

We shall collect byte values in memory before opening any output file. An invalid source must not be mistaken for a new program.

## How it works

PC begins at 0100H, the loaded address of the first .COM byte. OUTPTR begins at 6000H, the location of the output buffer in the assembler's own segment. These are different addresses with different purposes. Every emitted byte advances both by one.

EMIT takes the byte in AL and preserves AX and BX. On pass two it stores the byte at OUTPTR; on pass one it only counts. The current driver sets PASS to two. The 2100H limit on PC allows 8192 output bytes and refuses the next byte before storing beyond the buffer.

BYTEVALUE takes a full value in AX. Values above 255 select code 4; otherwise it enters EMIT. The caller therefore cannot accidentally truncate a word into a byte. EMIT selects code 5 if the image is full. Its nested PUSH instructions use four stack bytes in addition to the call's return address.

This checkpoint accepts one numeric byte value per line, checks the end of each statement, and reports the count collected. It writes no .COM file yet. The distinction lets us test conversion and capacity without disk-output behavior.

## Source changes

Copy `AS11.ASM` to `AS12.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `ERRCODE:`

Unchanged code immediately before this edit:

```asm

ERRCODE:
DB 0
```

Insert after old physical line 441, before the following old line.

Insert this source:

```asm

BUFFERMSG:
DB 66,117,102,102,101,114,101,100,32,36
```

### Change 2: following `TOKLEN:`

Unchanged code immediately before this edit:

```asm

TOKLEN:
DW 0
```

Insert after old physical line 429, before the following old line.

Insert this source:

```asm

PASS:
DB 1
```

### Change 3: following `LINENO:`

Unchanged code immediately before this edit:

```asm
LINENO:
DW 0

```

Insert after old physical line 427, before the following old line.

Insert this source:

```asm
PC:
DW 256

OUTPTR:
DW 24576

```

### Change 4: following `PROMPT:`

Unchanged code immediately before this edit:

```asm
PROMPT:
DB 83,111,117,114,99,101,32,110,97,109,101,58,32,36

```

Insert after old physical line 398, before the following old line.

Insert this source:

```asm
BYTEMSG:
DB 32,98,121,116,101,115,13,10,36

```

### Change 5: following `FINISHED:`

Unchanged code immediately before this edit:

```asm
FINISHED:
RET

```

Insert after old physical line 333, before the following old line.

Insert this source:

```asm
BYTEVALUE:
CMP AX,255
JBE EMIT
MOV AX,4
JMP ERROR

EMIT:
PUSH AX
PUSH BX
MOV BX,[PC]
CMP BX,2100H
JAE IMAGEFULL
MOV AH,[PASS]
CMP AH,2
JNE COUNTBYTE
MOV BX,[OUTPTR]
MOV [BX],AL
COUNTBYTE:
MOV BX,[PC]
INC BX
MOV [PC],BX
MOV BX,[OUTPTR]
INC BX
MOV [OUTPTR],BX
POP BX
POP AX
RET
IMAGEFULL:
MOV AX,5
JMP ERROR

```

### Change 6: following `DRIVERDONE:`

Unchanged code immediately before this edit:

```asm
JMP DRIVERLINE
DRIVERDONE:
CALL CLOSEFILE
```

Insert after old physical line 26, before the following old line.

Insert this source:

```asm
MOV DX,BUFFERMSG
CALL TEXT
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

### Change 7: following `DRIVERLINE:`

Unchanged code immediately before this edit:

```asm
CALL VALUE
PUSH AX
CALL FINISH
```

Remove these exact old lines (physical lines 20–23 of `AS11.ASM`):

```asm
POP AX
CALL NUMBER
MOV DX,NEWLINE
CALL TEXT
```

No replacement lines are needed.

### Change 8: following `DRIVERLINE:`

Unchanged code immediately before this edit:

```asm
MOV SI,2200H
CALL SCAN
CALL VALUE
```

Remove these exact old lines (physical lines 18–18 of `AS11.ASM`):

```asm
PUSH AX
```

Put this source in their place:

```asm
CALL BYTEVALUE
```

### Change 9: following `ROOM:`

Unchanged code immediately before this edit:

```asm
JMP ERROR
ROOM:
CALL GETNAME
```

Insert after old physical line 9, before the following old line.

Insert this source:

```asm
MOV AL,2
MOV [PASS],AL
MOV AX,100H
MOV [PC],AX
MOV AX,6000H
MOV [OUTPTR],AX
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BOOTASM.BAS
```

Enter `AS12` at its source prompt. Require `OK AS12.COM 1000 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T12.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
65
66
```

```dos
CHECK AS12
```

Enter `T12` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T12
Buffered 00002 bytes
PASS
```

## A rejection check

Enter this separate file as `X12.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
256
```

Run `CHECK AS12` and enter `X12`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
