+++
title = "25 \u00b7 Arithmetic and comparisons"
weight = 25
description = "Select a group number, register form, or full-width immediate."
download = "AS25.ASM"
aliases = ["/bootstrap/asm86/26-arithmetic-and-comparisons/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/25-arithmetic-and-comparisons/"
+++

Five related instruction families can share the operand reader and much of their encoding work.

## How it works

The class-four parameters are the processor's group numbers: ADD=0, OR=1, AND=4, SUB=5, and CMP=7. They are not a consecutive numbering invented by this assembler.

TWOOPERANDS requires a register destination. For a register source, SAMEWIDTH checks the widths and the opcode is eight times OP plus two plus W1. REGMOD supplies the ordinary two-register ModR/M byte.

For an immediate source, the opcode is 80H for a byte or 81H for a word. ModR/M is 192 plus eight times OP plus the destination register. IMMEDVALUE emits the full selected width. The shorter sign-extended 83H form is deliberately omitted, keeping instruction sizes independent of a value's eventual address.

ADD and SUB store their arithmetic result; CMP sets subtraction flags without storing it. AND and OR operate on corresponding bits. The assembled operations affect flags; the parser and encoding helpers also use flags internally, so the assembler saves state in fields rather than depending on a comparison across a helper call. Memory arithmetic and signed literal syntax remain excluded.

## Source changes

Copy `AS24.ASM` to `AS25.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `OPTAB:`

Unchanged code immediately before this edit:

```asm
DB 76,79,68,83,66,0,2,172
DB 83,84,79,83,66,0,2,170
DB 77,79,86,0,0,0,3,0
```

Insert after old physical line 907, before the following old line.

Insert this source:

```asm
DB 65,68,68,0,0,0,4,0
DB 79,82,0,0,0,0,4,1
DB 65,78,68,0,0,0,4,4
DB 83,85,66,0,0,0,4,5
DB 67,77,80,0,0,0,4,7
```

### Change 2: following `TWOOPERANDS:`

Unchanged code immediately before this edit:

```asm
CMP AL,44
JNE TWOBAD
CALL OPERAND
```

Remove these exact old lines (physical lines 628–628 of `AS24.ASM`):

```asm
JMP MOVOPERANDS
```

Put this source in their place:

```asm
MOV AL,[TYPE]
CMP AL,3
JE MOVOPERANDS
MOV AL,[K1]
CMP AL,1
JNE TWOBAD
MOV AL,[KIND]
CMP AL,1
JE MATHREG
CMP AL,3
JNE TWOBAD
MOV AL,[W1]
ADD AL,128
CALL EMIT
MOV AL,[OP]
CALL TIMES8
MOV DL,[R1]
ADD AL,DL
ADD AL,192
CALL EMIT
JMP IMMEDVALUE
MATHREG:
CALL SAMEWIDTH
MOV AL,[OP]
CALL TIMES8
ADD AL,2
MOV DL,[W1]
ADD AL,DL
CALL EMIT
JMP REGMOD
```

### Change 3: following `INSTRUCTION:`

Unchanged code immediately before this edit:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

Remove these exact old lines (physical lines 513–513 of `AS24.ASM`):

```asm
MOV CX,12
```

Put this source in their place:

```asm
MOV CX,17
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS25.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 2069 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS25.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T25.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
ADD AX,BX
SUB CX,1
CMP AL,41H
AND AL,0DFH
OR BL,20H
```

```dos
COPY T25.ASM SOURCE.ASM
```

```dos
CHECK AS25
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00015 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **15 bytes** with these hexadecimal bytes:

```text
03 C3 81 E9 01 00 80 F8 41 80 E0 DF 80 CB 20
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X25.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
ADD AX,AL
```

```dos
COPY X25.ASM SOURCE.ASM
CHECK AS25
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 1
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
