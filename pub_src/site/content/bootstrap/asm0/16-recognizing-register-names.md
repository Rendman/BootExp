+++
title = "16 \u00b7 Recognizing register names"
weight = 16
description = "A four-byte dictionary distinguishes registers from values."
download = "AS16.ASM"
aliases = ["/bootstrap/asm86/17-recognizing-register-names/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/16-recognizing-register-names/"
+++

Register names must be recognizable before they can be used as operands or rejected as labels. We shall add their small dictionary to the token lookup.

**Starting source:** `AS15.ASM`. **Save as:** `AS16.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

REGTAB contains sixteen four-byte records: two name characters, a zero, and an encoding number. Codes zero through seven denote byte registers AL, CL, DL, BL, AH, CH, DH, and BH. Codes eight through fifteen denote word registers AX, CX, DX, BX, SP, BP, SI, and DI.

REGISTER calls LOOK with that table and stride four. On a match it returns the code in AX; on a miss it returns FFFFH. It preserves SI through LOOK and changes the lookup scratch registers. Zero is a real code for AL, so FFFFH is the unambiguous miss result.

For this checkpoint, a recognized register in a data value is rejected with symbol code 3; another nonnumeric token remains a value error. Registers are not data constants. This exercises the dictionary without yet claiming support for MOV or other register instructions.

## Source changes

Copy `AS15.ASM` to `AS16.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OPTAB:`

Find the unique label `OPTAB:`. Insert the new source immediately before this existing label:

```asm
OPTAB:
```

Insert:

```asm
REGTAB:
DB 65,76,0,0
DB 67,76,0,1
DB 68,76,0,2
DB 66,76,0,3
DB 65,72,0,4
DB 67,72,0,5
DB 68,72,0,6
DB 66,72,0,7
DB 65,88,0,8
DB 67,88,0,9
DB 68,88,0,10
DB 66,88,0,11
DB 83,80,0,12
DB 66,80,0,13
DB 83,73,0,14
DB 68,73,0,15
```

### Change 2 · `LITERAL:`

Find the unique label `LITERAL:`. Insert the new source immediately before this existing label:

```asm
LITERAL:
```

Insert:

```asm
RESERVEDNUM:
MOV AX,3
JMP ERROR
```

### Change 3 · `WORDVALUE:`

Find the unique label `WORDVALUE:`, then follow this unchanged source through its last displayed instruction:

```asm
WORDVALUE:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CALL REGISTER
CMP AX,0FFFFH
JNE RESERVEDNUM
```

### Change 4 · `LOOKMISS:`

Find the unique label `LOOKMISS:`, then follow this unchanged source through its last displayed instruction:

```asm
LOOKMISS:
MOV BX,0
POP SI
RET
```

The edit begins immediately after that unchanged block.

Insert:

```asm
REGISTER:
MOV BX,REGTAB
MOV CX,16
MOV AX,4
CALL LOOK
CMP BX,0
JE NOREGISTER
ADD BX,3
MOV AL,[BX]
MOV AH,0
RET
NOREGISTER:
MOV AX,0FFFFH
RET
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS16.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1228 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS16.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T16.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
DB 65
```

```dos
COPY T16.ASM SOURCE.ASM
```

```dos
CHECK AS16
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00001 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **1 byte** with these hexadecimal bytes:

```text
41
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X16.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
DW AX
```

```dos
COPY X16.ASM SOURCE.ASM
CHECK AS16
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 3
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the four-byte register records and the distinction between AL's valid code zero and the miss result FFFFH. A recognized register in a data value must take the symbol-error path.
