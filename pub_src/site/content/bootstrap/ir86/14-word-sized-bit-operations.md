+++
title = "14 \u00b7 Word-sized bit operations"
weight = 14
description = "AND, OR, and XOR use the same operand discipline."
download = "IR14.ASM"
+++

Bit masks and packed fields need logical operations on the complete word.

## Operation and backend

AND retains bits set in both the saved left word and A. OR retains bits set in either, and XOR retains bits which differ. Each consumes one saved expression word and leaves the sixteen-bit result in A.

The backend pops the saved word into BX and combines it with AX. The instruction table supplies the same consume-one effect as ADD, so no separate parser is needed for each mnemonic. A missing left operand is a stack error, not a zero silently supplied by the translator.

The test forms (15 AND 10) XOR 3 OR 1, which is nine, then subtracts nine. Unsigned decimal spelling is used for the masks; equivalent hexadecimal spelling is accepted by the existing numeric reader.

## Source changes

Copy `IR13.ASM` to `IR14.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_SUB:`

Unchanged code immediately before the edit:

```asm
T_SUB:
DB 80,79,80,32,66,88,13,10,83,85,66,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,66,88,13,10,0
```

Insert after old physical line 938, before the following old line.

Insert this source:

```asm

T_AND:
DB 80,79,80,32,66,88,13,10,65,78,68,32,65,88,44,66
DB 88,13,10,0

T_OR:
DB 80,79,80,32,66,88,13,10,79,82,32,65,88,44,66,88
DB 13,10,0

T_XOR:
DB 80,79,80,32,66,88,13,10,88,79,82,32,65,88,44,66
DB 88,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_ADD
DB 83,85,66,0,0,0,0,0,0,2,5,0
DW T_SUB
```

Insert after old physical line 792, before the following old line.

Insert this source:

```asm
DB 65,78,68,0,0,0,0,0,0,2,3,0
DW T_AND
DB 79,82,0,0,0,0,0,0,0,2,3,0
DW T_OR
DB 88,79,82,0,0,0,0,0,0,2,3,0
DW T_XOR
```

### Change 3: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 485–485 in `IR13.ASM`):

```asm
MOV CX,15
```

Put this source in their place:

```asm
MOV CX,18
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR14` at ASM86's `Source name:` prompt. Require `OK 02327 bytes` followed by PASS. This builds `IR14.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T14.IR` with `COPY CON T14.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 15
PUSH
LIT 10
AND
PUSH
LIT 3
XOR
PUSH
LIT 1
OR
PUSH
LIT 9
SUB
EXIT
```

```dos
CHECK IR14
```

Enter `T14` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T14
OK T14.ASM 00281 text bytes
PASS
```

Run `TYPE T14.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_MAIN:
MOV AX,15
PUSH AX
MOV AX,10
POP BX
AND AX,BX
PUSH AX
MOV AX,3
POP BX
XOR AX,BX
PUSH AX
MOV AX,1
POP BX
OR AX,BX
PUSH AX
MOV AX,9
POP BX
SUB BX,AX
MOV AX,BX
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T14`. Require `OK 00052 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T14.COM`, and require length **52 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
0F 00 50 B8 0A 00 5B 23 C3 50 B8 03 00 5B 33 C3
50 B8 01 00 5B 0B C3 50 B8 09 00 5B 2B D8 8B C3
B4 4C CD 21
```

`T14.COM` is a complete program. Run `CHECK T14`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X14.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
XOR
```

Run `CHECK IR14` and enter `X14`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.
