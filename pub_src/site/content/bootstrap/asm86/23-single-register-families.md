+++
title = "23 \u00b7 Single-register families"
weight = 23
description = "Increment, decrement, save, and restore a word register."
download = "AS23.ASM"
aliases = ["/bootstrap/asm86/24-single-register-families/"]
download_group = "tools/asm0"
reader_names = 1
+++

Four instruction families use the same register-number calculation and one-byte output.

## How it works

The class-five records carry bases 40H, 48H, 50H, and 58H for INC, DEC, PUSH, and POP. SINGLE reads a register and accepts only codes eight through fifteen, the word-register half of REGTAB. Subtracting eight recovers the processor's register number.

INC and DEC change a word by one with wraparound and preserve carry. PUSH subtracts two from SP and stores a word at SS:SP. POP reads a word and advances SP; neither instruction changes arithmetic flags. Every ordinary saved word must be balanced before a return.

SINGLE changes the scanner and lookup scratch registers, AL, output state, and flags used by the assembler. FINISH refuses a second operand. Byte INC/DEC, memory forms, and immediate PUSH are excluded. PUSH SP has the original 8086/8088 behavior of storing the decremented SP; avoid it in ordinary saved-register code. POP SP also changes the stack pointer itself.

## Source changes

Copy `AS22.ASM` to `AS23.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `OPTAB:`

Unchanged code immediately before this edit:

```asm
DB 76,79,68,83,66,0,2,172
DB 83,84,79,83,66,0,2,170
DB 77,79,86,0,0,0,3,0
```

Insert after old physical line 872, before the following old line.

Insert this source:

```asm
DB 73,78,67,0,0,0,5,64
DB 68,69,67,0,0,0,5,72
DB 80,85,83,72,0,0,5,80
DB 80,79,80,0,0,0,5,88
```

### Change 2: following `FIXED:`

Unchanged code immediately before this edit:

```asm

FIXED:
MOV AL,[OP]
```

Insert after old physical line 565, before the following old line.

Insert this source:

```asm
CALL EMIT
CALL FINISH
RET

SINGLE:
CALL SCAN
CALL REGISTER
CMP AX,8
JB SYNTAXBAD
CMP AX,15
JA SYNTAXBAD
SUB AL,8
MOV DL,[OP]
ADD AL,DL
```

### Change 3: following `STNEXT2:`

Unchanged code immediately before this edit:

```asm
CALL FIXED
RET
STNEXT2:
```

Insert after old physical line 537, before the following old line.

Insert this source:

```asm
CMP AL,5
JNE STNEXT5
CALL SINGLE
RET
STNEXT5:
```

### Change 4: following `INSTRUCTION:`

Unchanged code immediately before this edit:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

Remove these exact old lines (physical lines 513–513 of `AS22.ASM`):

```asm
MOV CX,7
```

Put this source in their place:

```asm
MOV CX,11
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS23.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1906 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS23.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T23.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
INC BX
DEC CX
PUSH AX
POP DX
```

```dos
COPY T23.ASM SOURCE.ASM
```

```dos
CHECK AS23
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00004 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **4 bytes** with these hexadecimal bytes:

```text
43 49 50 5A
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X23.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
INC AL
```

```dos
COPY X23.ASM SOURCE.ASM
CHECK AS23
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 1
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
