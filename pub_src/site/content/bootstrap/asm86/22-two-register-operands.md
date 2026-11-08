+++
title = "22 \u00b7 Two register operands"
weight = 22
description = "Put destination and source numbers into ModR/M."
download = "AS22.ASM"
aliases = ["/bootstrap/asm86/23-two-register-operands/"]
download_group = "tools/asm0"
reader_names = 1
+++

We shall let MOV copy between registers of equal width, using the saved first operand and the newly read second operand.

## How it works

KIND=1 for the second operand selects MOVREG. SAMEWIDTH compares W1 with WIDTH and selects syntax code 1 if a byte and a word register were mixed. No extension or truncation rule is implied.

The opcode is 8AH for byte registers and 8BH for word registers. REGMOD constructs the second byte: 192 for mode 11, eight times the destination number R1 for bits 5-3, and the source number REG for bits 2-0. Thus MOV AX,BX is 8B C3.

TIMES8 changes only AL and flags. SAMEWIDTH changes AL, DL, and flags; the caller reloads the value needed for encoding afterward. EMIT preserves AX and BX, so emitting the opcode does not destroy the saved operand fields. As before, MOV itself does not change arithmetic flags when the assembled program runs.

## Source changes

Copy `AS21.ASM` to `AS22.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `IMMEDVALUE:`

Unchanged code immediately before this edit:

```asm
MOV AX,[VAL]
JE BYTEVALUE
JMP EMITWORD
```

Insert after old physical line 618, before the following old line.

Insert this source:

```asm

SAMEWIDTH:
MOV AL,[W1]
MOV DL,[WIDTH]
CMP AL,DL
JE WIDTHOK
MOV AX,1
JMP ERROR
WIDTHOK:
RET
```

### Change 2: following `MOVOPERANDS:`

Unchanged code immediately before this edit:

```asm
CALL EMIT
JMP IMMEDVALUE

```

Insert after old physical line 612, before the following old line.

Insert this source:

```asm
MOVREG:
CALL SAMEWIDTH
MOV AL,[W1]
ADD AL,138
CALL EMIT
JMP REGMOD

REGMOD:
MOV AL,[R1]
CALL TIMES8
MOV DL,[REG]
ADD AL,DL
ADD AL,192
CALL EMIT
RET

```

### Change 3: following `MOVOPERANDS:`

Unchanged code immediately before this edit:

```asm
CMP AL,1
JNE TWOBAD
MOV AL,[KIND]
```

Insert after old physical line 602, before the following old line.

Insert this source:

```asm
CMP AL,1
JE MOVREG
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS22.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1831 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS22.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T22.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
MOV AX,BX
MOV DL,AL
MOV CH,BH
```

```dos
COPY T22.ASM SOURCE.ASM
```

```dos
CHECK AS22
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00006 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **6 bytes** with these hexadecimal bytes:

```text
8B C3 8A D0 8A EF
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X22.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
MOV AX,AL
```

```dos
COPY X22.ASM SOURCE.ASM
CHECK AS22
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 1
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
