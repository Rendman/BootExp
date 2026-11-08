+++
title = "24 \u00b7 Assembling a DOS request"
weight = 24
description = "Emit CDH and a checked interrupt number."
download = "AS24.ASM"
aliases = ["/bootstrap/asm86/25-assembling-a-dos-request/"]
download_group = "tools/asm0"
reader_names = 1
+++

A source program can now prepare registers. We shall add INT so a complete assembled program can display a character and terminate through DOS.

## How it works

INTERRUPT reads one value, saves AX while it emits CDH, then passes the restored value through BYTEVALUE. That bound check is essential: the interrupt number occupies one byte. FINISH rejects another token.

In the test, DL holds Z and AH holds function 02H. INT 21H displays the character. Loading AX with 4C00H then requests function 4CH with a zero return code in AL. The source is a complete executable, unlike the earlier encoding fixtures.

INTERRUPT changes VALUE's scratch registers, AX, PC, OUTPTR, and flags. Its temporary saved AX costs two stack bytes. The interrupt instruction itself causes the processor to save flags, CS, and IP while the service runs; the caller must use the documented DOS register interface, not treat a software interrupt as an ordinary subroutine.

## Source changes

Copy `AS23.ASM` to `AS24.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `OPTAB:`

Unchanged code immediately before this edit:

```asm
DB 68,69,67,0,0,0,5,72
DB 80,85,83,72,0,0,5,80
DB 80,79,80,0,0,0,5,88
```

Insert after old physical line 895, before the following old line.

Insert this source:

```asm
DB 73,78,84,0,0,0,6,205
```

### Change 2: following `SINGLE:`

Unchanged code immediately before this edit:

```asm
MOV DL,[OP]
ADD AL,DL
CALL EMIT
```

Insert after old physical line 585, before the following old line.

Insert this source:

```asm
CALL FINISH
RET

INTERRUPT:
CALL SCAN
CALL VALUE
PUSH AX
MOV AL,205
CALL EMIT
POP AX
CALL BYTEVALUE
```

### Change 3: following `STNEXT5:`

Unchanged code immediately before this edit:

```asm
CALL SINGLE
RET
STNEXT5:
```

Insert after old physical line 542, before the following old line.

Insert this source:

```asm
CMP AL,6
JNE STNEXT6
CALL INTERRUPT
RET
STNEXT6:
```

### Change 4: following `INSTRUCTION:`

Unchanged code immediately before this edit:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

Remove these exact old lines (physical lines 513–513 of `AS23.ASM`):

```asm
MOV CX,11
```

Put this source in their place:

```asm
MOV CX,12
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS24.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1943 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS24.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T24.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
MOV DL,5AH
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T24.ASM SOURCE.ASM
```

```dos
CHECK AS24
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00011 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **11 bytes** with these hexadecimal bytes:

```text
B2 5A B4 02 CD 21 B8 00 4C CD 21
```

Use `SYSTEM` to return to DOS.

`RESULT.COM` is also a complete executable. Preserve it with `COPY RESULT.COM T24.COM`, then run `CHECK T24`. It displays `Z` followed by the checker's blank line and `PASS`.

## A rejection check

Enter this separate file as `X24.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
INT 256
```

```dos
COPY X24.ASM SOURCE.ASM
CHECK AS24
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
