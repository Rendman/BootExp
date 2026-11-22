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

**Starting source:** `AS24.ASM`. **Save as:** `AS25.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

The class-four parameters are the processor's group numbers: ADD=0, OR=1, AND=4, SUB=5, and CMP=7. They are not a consecutive numbering invented by this assembler.

TWOOPERANDS requires a register destination. For a register source, SAMEWIDTH checks the widths and the opcode is eight times OP plus two plus W1. REGMOD supplies the ordinary two-register ModR/M byte.

For an immediate source, the opcode is 80H for a byte or 81H for a word. ModR/M is 192 plus eight times OP plus the destination register. IMMEDVALUE emits the full selected width. The shorter sign-extended 83H form is deliberately omitted, keeping instruction sizes independent of a value's eventual address.

ADD and SUB store their arithmetic result; CMP sets subtraction flags without storing it. AND and OR operate on corresponding bits. The assembled operations affect flags; the parser and encoding helpers also use flags internally, so the assembler saves state in fields rather than depending on a comparison across a helper call. Memory arithmetic and signed literal syntax remain excluded.

## Source changes

Copy `AS24.ASM` to `AS25.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OPTAB:`

Find the unique label `OPTAB:`, then follow this unchanged source through its last displayed instruction:

```asm
OPTAB:
DB 68,66,0,0,0,0,1,0
DB 68,87,0,0,0,0,1,1
DB 82,69,84,0,0,0,2,195
DB 67,76,68,0,0,0,2,252
DB 76,79,68,83,66,0,2,172
DB 83,84,79,83,66,0,2,170
DB 77,79,86,0,0,0,3,0
```

The edit begins immediately after that unchanged block.

Insert:

```asm
DB 65,68,68,0,0,0,4,0
DB 79,82,0,0,0,0,4,1
DB 65,78,68,0,0,0,4,4
DB 83,85,66,0,0,0,4,5
DB 67,77,80,0,0,0,4,7
```

### Change 2 · `TWOOPERANDS:`

Find the unique label `TWOOPERANDS:`, then follow this unchanged source through its last displayed instruction:

```asm
TWOOPERANDS:
CALL OPERAND
MOV AL,[KIND]
MOV [K1],AL
MOV AL,[WIDTH]
MOV [W1],AL
MOV AL,[REG]
MOV [R1],AL
CALL SCAN
MOV AL,[2300H]
CMP AL,44
JNE TWOBAD
CALL OPERAND
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JMP MOVOPERANDS
```

With:

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

Keep the following `TWOBAD:` label and the source after it in place.

### Change 3 · `INSTRUCTION:`

Find the unique label `INSTRUCTION:`, then follow this unchanged source through its last displayed instruction:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV CX,12
```

With:

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

Check the arithmetic group numbers rather than assigning consecutive table selectors. Register forms and full-width immediate forms use different opcode calculations; CMP emits an operation that changes flags without storing a result.
