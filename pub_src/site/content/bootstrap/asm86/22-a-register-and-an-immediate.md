+++
title = "22 \u00b7 A register and an immediate"
weight = 22
description = "Determine MOV size from its destination register."
download = "AS22.ASM"
+++

We shall add MOV with a register destination and a numeric or named immediate value.

## How it works

OPERAND scans one operand and tries REGISTER first. A register code supplies its number, REG, and width, WIDTH: zero for byte or one for word. KIND=1 identifies a register. A token which is not a register is read through VALUE and stored in VAL with KIND=3. The source cursor SI remains just after the operand.

TWOOPERANDS saves the first kind, width, and register in K1, W1, and R1. It then requires a comma and reads the second operand into the ordinary result fields. Those saved fields prevent the second lookup from destroying the destination description.

For this form, MOVOPERANDS requires a register first and an immediate second. The opcode is B0H plus the byte register number, or B8H plus the word register number. TIMES8 supplies the width contribution with three doublings. IMMEDVALUE reads VAL and chooses BYTEVALUE or EMITWORD from W1.

The routine changes the operand fields, parser scratch registers, and output state. A byte destination rejects values above 255. Register-to-register MOV is not accepted at this checkpoint. The source uses the same small instruction vocabulary as the routines it constructs; no extra assembler is involved.

## Source changes

Copy `AS21.ASM` to `AS22.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `OPTAB:`

Unchanged code immediately before this edit:

```asm
DB 67,76,68,0,0,0,2,252
DB 76,79,68,83,66,0,2,172
DB 83,84,79,83,66,0,2,170
```

Insert after old physical line 815, before the following old line.

Insert this source:

```asm
DB 77,79,86,0,0,0,3,0
```

### Change 2: following `OP:`

Unchanged code immediately before this edit:

```asm
DB 0

OP:
```

Insert after old physical line 784, before the following old line.

Insert this source:

```asm
DB 0

KIND:
DB 0

WIDTH:
DB 0

REG:
DB 0

K1:
DB 0

W1:
DB 0

R1:
```

### Change 3: following `STRIDE:`

Unchanged code immediately before this edit:

```asm
STRIDE:
DW 0

```

Insert after old physical line 768, before the following old line.

Insert this source:

```asm
VAL:
DW 0

```

### Change 4: following `FINISHED:`

Unchanged code immediately before this edit:

```asm
MOV AX,1
JMP ERROR
FINISHED:
```

Insert after old physical line 606, before the following old line.

Insert this source:

```asm
RET

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
JMP MOVOPERANDS
TWOBAD:
MOV AX,1
JMP ERROR

MOVOPERANDS:
MOV AL,[K1]
CMP AL,1
JNE TWOBAD
MOV AL,[KIND]
CMP AL,3
JNE TWOBAD
MOV AL,[W1]
CALL TIMES8
ADD AL,176
MOV DL,[R1]
ADD AL,DL
CALL EMIT
JMP IMMEDVALUE

IMMEDVALUE:
MOV AL,[W1]
CMP AL,0
MOV AX,[VAL]
JE BYTEVALUE
JMP EMITWORD

TIMES8:
ADD AL,AL
ADD AL,AL
ADD AL,AL
```

### Change 5: following `STNEXT2:`

Unchanged code immediately before this edit:

```asm
CALL FIXED
RET
STNEXT2:
```

Remove these exact old lines (physical lines 569–569 of `AS21.ASM`):

```asm
JMP SYNTAXBAD
```

Put this source in their place:

```asm
CALL TWOOPERANDS
CALL FINISH
RET
```

### Change 6: following `INSTRUCTION:`

Unchanged code immediately before this edit:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

Remove these exact old lines (physical lines 544–544 of `AS21.ASM`):

```asm
MOV CX,7
```

Put this source in their place:

```asm
MOV CX,8
```

### Change 7: following `DEFINEBAD:`

Unchanged code immediately before this edit:

```asm
MOV AX,3
JMP ERROR

```

Insert after old physical line 524, before the following old line.

Insert this source:

```asm
OPERAND:
CALL SCAN
CALL REGISTER
CMP AX,0FFFFH
JE IMMEDIATE
MOV DL,AL
AND AL,7
MOV [REG],AL
MOV AL,0
CMP DL,8
JB REGWIDTH
MOV AL,1
REGWIDTH:
MOV [WIDTH],AL
MOV AL,1
MOV [KIND],AL
RET
IMMEDIATE:
CALL VALUE
MOV [VAL],AX
MOV AL,3
MOV [KIND],AL
RET

```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BOOTASM.BAS
```

Enter `AS22` at its source prompt. Require `OK AS22.COM 1922 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T22.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
MOV AL,41H
MOV AX,1234H
```

```dos
CHECK AS22
```

Enter `T22` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T22
OK 00005 bytes
PASS
```

Inspect `T22.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `T22.COM`, and require a length of **5 bytes** with these hexadecimal bytes:

```text
B0 41 B8 34 12
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X22.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
MOV AL,256
```

Run `CHECK AS22` and enter `X22`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
