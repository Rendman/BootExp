+++
title = "22 \u00b7 Two register operands"
weight = 22
description = "Put destination and source numbers into ModR/M."
download = "AS22.ASM"
aliases = ["/bootstrap/asm86/23-two-register-operands/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/22-two-register-operands/"
+++

We shall let MOV copy between registers of equal width, using the saved first operand and the newly read second operand.

**Starting source:** `AS21.ASM`. **Save as:** `AS22.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

KIND=1 for the second operand selects MOVREG. SAMEWIDTH compares W1 with WIDTH and selects syntax code 1 if a byte and a word register were mixed. No extension or truncation rule is implied.

The opcode is 8AH for byte registers and 8BH for word registers. REGMOD constructs the second byte: 192 for mode 11, eight times the destination number R1 for bits 5-3, and the source number REG for bits 2-0. Thus MOV AX,BX is 8B C3.

TIMES8 changes only AL and flags. SAMEWIDTH changes AL, DL, and flags; the caller reloads the value needed for encoding afterward. EMIT preserves AX and BX, so emitting the opcode does not destroy the saved operand fields. As before, MOV itself does not change arithmetic flags when the assembled program runs.

## Source changes

Copy `AS21.ASM` to `AS22.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `TIMES8:`

Find the unique label `TIMES8:`. Insert the new source immediately before this existing label:

```asm
TIMES8:
```

Insert:

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

### Change 2 · `IMMEDVALUE:`

Find the unique label `IMMEDVALUE:`. Insert the new source immediately before this existing label:

```asm
IMMEDVALUE:
```

Insert:

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

### Change 3 · `MOVOPERANDS:`

Find the unique label `MOVOPERANDS:`, then follow this unchanged source through its last displayed instruction:

```asm
MOVOPERANDS:
MOV AL,[K1]
CMP AL,1
JNE TWOBAD
MOV AL,[KIND]
```

The edit begins immediately after that unchanged block.

Insert:

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

Check SAMEWIDTH before constructing ModR/M. The destination belongs in bits 5–3 and the source in bits 2–0; reload any encoding value changed by the width check.
