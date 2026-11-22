+++
title = "21 \u00b7 A register and an immediate"
weight = 21
description = "Determine MOV size from its destination register."
download = "AS21.ASM"
aliases = ["/bootstrap/asm86/22-a-register-and-an-immediate/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/21-a-register-and-an-immediate/"
+++

We shall add MOV with a register destination and a numeric or named immediate value.

**Starting source:** `AS20.ASM`. **Save as:** `AS21.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

OPERAND scans one operand and tries REGISTER first. A register code supplies its number, REG, and width, WIDTH: zero for byte or one for word. KIND=1 identifies a register. A token which is not a register is read through VALUE and stored in VAL with KIND=3. The source cursor SI remains just after the operand.

TWOOPERANDS saves the first kind, width, and register in K1, W1, and R1. It then requires a comma and reads the second operand into the ordinary result fields. Those saved fields prevent the second lookup from destroying the destination description.

For this form, MOVOPERANDS requires a register first and an immediate second. The opcode is B0H plus the byte register number, or B8H plus the word register number. TIMES8 supplies the width contribution with three doublings. IMMEDVALUE reads VAL and chooses BYTEVALUE or EMITWORD from W1.

The routine changes the operand fields, parser scratch registers, and output state. A byte destination rejects values above 255. Register-to-register MOV is not accepted at this checkpoint. The source uses the same small instruction vocabulary as the routines it constructs; no extra assembler is involved.

## Source changes

Copy `AS20.ASM` to `AS21.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

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
```

The edit begins immediately after that unchanged block.

Insert:

```asm
DB 77,79,86,0,0,0,3,0
```

### Change 2 · `OP:`

Find the unique label `OP:`, then follow this unchanged source through its last displayed instruction:

```asm
OP:
```

The edit begins immediately after that unchanged block.

Insert:

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

### Change 3 · `PASS:`

Find the unique label `PASS:`. Insert the new source immediately before this existing label:

```asm
PASS:
```

Insert:

```asm
VAL:
DW 0
```

### Change 4 · `FINISHED:`

Find the unique label `FINISHED:`, then follow this unchanged source through its last displayed instruction:

```asm
FINISHED:
```

The edit begins immediately after that unchanged block.

Insert:

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

### Change 5 · `STNEXT2:`

Find the unique label `STNEXT2:`, then follow this unchanged source through its last displayed instruction:

```asm
STNEXT2:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JMP SYNTAXBAD
```

With:

```asm
CALL TWOOPERANDS
CALL FINISH
RET
```

Keep the following `SYNTAXBAD:` label and the source after it in place.

### Change 6 · `INSTRUCTION:`

Find the unique label `INSTRUCTION:`, then follow this unchanged source through its last displayed instruction:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV CX,6
```

With:

```asm
MOV CX,7
```

### Change 7 · `STATEMENT:`

Find the unique label `STATEMENT:`. Insert the new source immediately before this existing label:

```asm
STATEMENT:
```

Insert:

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
COPY AS21.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1771 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS21.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T21.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
MOV AL,41H
MOV AX,1234H
```

```dos
COPY T21.ASM SOURCE.ASM
```

```dos
CHECK AS21
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00005 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **5 bytes** with these hexadecimal bytes:

```text
B0 41 B8 34 12
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X21.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
MOV AL,256
```

```dos
COPY X21.ASM SOURCE.ASM
CHECK AS21
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check K1, W1 and R1 after reading the second operand. The destination width selects B0H or B8H and the immediate width; a byte value must pass BYTEVALUE without truncation.
