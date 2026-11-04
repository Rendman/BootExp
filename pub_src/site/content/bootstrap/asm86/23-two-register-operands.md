+++
title = "23 \u00b7 Two register operands"
weight = 23
description = "Put destination and source numbers into ModR/M."
download = "AS23.ASM"
+++

We shall let MOV copy between registers of equal width, using the saved first operand and the newly read second operand.

## How it works

KIND=1 for the second operand selects MOVREG. SAMEWIDTH compares W1 with WIDTH and selects syntax code 1 if a byte and a word register were mixed. No extension or truncation rule is implied.

The opcode is 8AH for byte registers and 8BH for word registers. REGMOD constructs the second byte: 192 for mode 11, eight times the destination number R1 for bits 5-3, and the source number REG for bits 2-0. Thus MOV AX,BX is 8B C3.

TIMES8 changes only AL and flags. SAMEWIDTH changes AL, DL, and flags; the caller reloads the value needed for encoding afterward. EMIT preserves AX and BX, so emitting the opcode does not destroy the saved operand fields. As before, MOV itself does not change arithmetic flags when the assembled program runs.

## Source changes

Copy `AS22.ASM` to `AS23.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `IMMEDVALUE:`

Unchanged code immediately before this edit:

```asm
MOV AX,[VAL]
JE BYTEVALUE
JMP EMITWORD
```

Insert after old physical line 673, before the following old line.

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

Insert after old physical line 667, before the following old line.

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

Insert after old physical line 657, before the following old line.

Insert this source:

```asm
CMP AL,1
JE MOVREG
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BOOTASM.BAS
```

Enter `AS23` at its source prompt. Require `OK AS23.COM 1982 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T23.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
MOV AX,BX
MOV DL,AL
MOV CH,BH
```

```dos
CHECK AS23
```

Enter `T23` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T23
OK 00006 bytes
PASS
```

Inspect `T23.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `T23.COM`, and require a length of **6 bytes** with these hexadecimal bytes:

```text
8B C3 8A D0 8A EF
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X23.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
MOV AX,AL
```

Run `CHECK AS23` and enter `X23`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 1
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
