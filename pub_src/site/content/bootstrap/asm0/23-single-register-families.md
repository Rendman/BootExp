+++
title = "23 \u00b7 Single-register families"
weight = 23
description = "Increment, decrement, save, and restore a word register."
download = "AS23.ASM"
aliases = ["/bootstrap/asm86/24-single-register-families/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/23-single-register-families/"
+++

Four instruction families use the same register-number calculation and one-byte output.

**Starting source:** `AS22.ASM`. **Save as:** `AS23.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

The class-five records carry bases 40H, 48H, 50H, and 58H for INC, DEC, PUSH, and POP. SINGLE reads a register and accepts only codes eight through fifteen, the word-register half of REGTAB. Subtracting eight recovers the processor's register number.

INC and DEC change a word by one with wraparound and preserve carry. PUSH subtracts two from SP and stores a word at SS:SP. POP reads a word and advances SP; neither instruction changes arithmetic flags. Every ordinary saved word must be balanced before a return.

SINGLE changes the scanner and lookup scratch registers, AL, output state, and flags used by the assembler. FINISH refuses a second operand. Byte INC/DEC, memory forms, and immediate PUSH are excluded. PUSH SP has the original 8086/8088 behavior of storing the decremented SP; avoid it in ordinary saved-register code. POP SP also changes the stack pointer itself.

## Source changes

Copy `AS22.ASM` to `AS23.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

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
DB 73,78,67,0,0,0,5,64
DB 68,69,67,0,0,0,5,72
DB 80,85,83,72,0,0,5,80
DB 80,79,80,0,0,0,5,88
```

### Change 2 · `FIXED:`

Find the unique label `FIXED:`, then follow this unchanged source through its last displayed instruction:

```asm
FIXED:
MOV AL,[OP]
```

The edit begins immediately after that unchanged block.

Insert:

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

### Change 3 · `STNEXT2:`

Find the unique label `STNEXT2:`, then follow this unchanged source through its last displayed instruction:

```asm
STNEXT2:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CMP AL,5
JNE STNEXT5
CALL SINGLE
RET
STNEXT5:
```

### Change 4 · `INSTRUCTION:`

Find the unique label `INSTRUCTION:`, then follow this unchanged source through its last displayed instruction:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV CX,7
```

With:

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

Check that SINGLE accepts only the word-register half of REGTAB and subtracts eight before adding the opcode base. Balance the generated PUSH and POP operations before a return.
