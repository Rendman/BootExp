+++
title = "26 \u00b7 Moving through memory"
weight = 26
description = "Use BX or one direct offset; let the register determine width."
download = "AS26.ASM"
aliases = ["/bootstrap/asm86/27-moving-through-memory/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/26-moving-through-memory/"
+++

We shall add bracketed MOV operands without adding an expression parser or the processor's entire addressing vocabulary.

## How it works

An opening bracket selects MEMORY. The inner token BX selects r/m=7; every other inner token is a value or label and selects r/m=6 with a direct word offset. A closing bracket is required. KIND=2 identifies memory, REG holds that r/m number, and VAL holds the direct offset when needed.

The first operand's value is now saved in V1 as well. For a load into a register, LOADMEM uses opcode 8AH or 8BH and ModR/M equal to eight times R1 plus the memory r/m number. A direct offset follows only for r/m=6.

For a store, STOREMEM requires a register source, uses 88H or 89H, and puts that register number in the middle field. V1 supplies a direct destination offset. The memory operand has no width of its own; the register on the other side supplies it.

These routines change the operand fields, VALUE and lookup scratch state, AL and DL, and output state. EMIT preserves DX, so the r/m number in DL survives while the instruction bytes are emitted. Memory-to-memory and immediate-to-memory MOV are rejected. Segment overrides, [SI], [BP], and indexed combinations are omitted to keep the grammar and record of instruction lengths small. The processor supports more than this source language accepts.

## Source changes

Copy `AS25.ASM` to `AS26.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `VAL:`

Unchanged code immediately before this edit:

```asm
VAL:
DW 0

```

Insert after old physical line 871, before the following old line.

Insert this source:

```asm
V1:
DW 0

```

### Change 2: following `IMMEDVALUE:`

Unchanged code immediately before this edit:

```asm
MOV AX,[VAL]
JE BYTEVALUE
JMP EMITWORD
```

Insert after old physical line 700, before the following old line.

Insert this source:

```asm

LOADMEM:
MOV AL,[W1]
ADD AL,138
CALL EMIT
MOV AL,[R1]
CALL TIMES8
MOV DL,[REG]
ADD AL,DL
CALL EMIT
CMP DL,6
JNE LOADEND
MOV AX,[VAL]
CALL EMITWORD
LOADEND:
RET

STOREMEM:
MOV AL,[KIND]
CMP AL,1
JE STOREOK
MOV AX,1
JMP ERROR
STOREOK:
MOV AL,[WIDTH]
ADD AL,136
CALL EMIT
MOV AL,[REG]
CALL TIMES8
MOV DL,[R1]
ADD AL,DL
CALL EMIT
CMP DL,6
JNE STOREEND
MOV AX,[V1]
CALL EMITWORD
STOREEND:
RET
```

### Change 3: following `MOVOPERANDS:`

Unchanged code immediately before this edit:

```asm
MOV AL,[KIND]
CMP AL,1
JE MOVREG
```

Remove these exact old lines (physical lines 669–670 of `AS25.ASM`):

```asm
CMP AL,3
JNE TWOBAD
```

Put this source in their place:

```asm
CMP AL,2
JE LOADMEM
```

### Change 4: following `MOVOPERANDS:`

Unchanged code immediately before this edit:

```asm

MOVOPERANDS:
MOV AL,[K1]
```

Insert after old physical line 663, before the following old line.

Insert this source:

```asm
CMP AL,2
JNE MOVDESTREG
JMP STOREMEM
MOVDESTREG:
```

### Change 5: following `TWOOPERANDS:`

Unchanged code immediately before this edit:

```asm
MOV [W1],AL
MOV AL,[REG]
MOV [R1],AL
```

Insert after old physical line 622, before the following old line.

Insert this source:

```asm
MOV AX,[VAL]
MOV [V1],AX
```

### Change 6: following `IMMEDIATE:`

Unchanged code immediately before this edit:

```asm
CALL VALUE
MOV [VAL],AX
MOV AL,3
```

Insert after old physical line 490, before the following old line.

Insert this source:

```asm
MOV [KIND],AL
RET

MEMORY:
CALL SCAN
MOV AX,[2300H]
CMP AX,5842H
JNE DIRECTMEM
MOV AL,[2302H]
CMP AL,0
JNE DIRECTMEM
MOV AL,7
MOV [REG],AL
JMP MEMORYEND
DIRECTMEM:
CALL VALUE
MOV [VAL],AX
MOV AL,6
MOV [REG],AL
MEMORYEND:
CALL SCAN
MOV AL,[2300H]
CMP AL,93
JE MEMORYOK
MOV AX,1
JMP ERROR
MEMORYOK:
MOV AL,2
```

### Change 7: following `OPERAND:`

Unchanged code immediately before this edit:

```asm

OPERAND:
CALL SCAN
```

Insert after old physical line 471, before the following old line.

Insert this source:

```asm
MOV AL,[2300H]
CMP AL,91
JE MEMORY
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS26.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 2258 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS26.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T26.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
MOV AL,[BX]
MOV [BX],AL
MOV AX,[200H]
MOV [200H],AX
```

```dos
COPY T26.ASM SOURCE.ASM
```

```dos
CHECK AS26
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00012 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **12 bytes** with these hexadecimal bytes:

```text
8A 07 88 07 8B 06 00 02 89 06 00 02
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X26.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
MOV [BX],1
```

```dos
COPY X26.ASM SOURCE.ASM
CHECK AS26
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 1
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
