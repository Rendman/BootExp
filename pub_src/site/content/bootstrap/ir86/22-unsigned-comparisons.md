+++
title = "22 \u00b7 Unsigned comparisons"
weight = 22
description = "Compare a saved left word with A and branch on the result."
download = "IR22.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

A comparison needs the same two-operand order as subtraction and a clear choice of signedness.

## Operation and backend

EQ and NE compare the saved left word with A for equality or inequality. ULT, ULE, UGT, and UGE compare them as unsigned words. Each consumes the left word, branches on its stated relation, and retains the right operand in A rather than producing a Boolean value.

Effect four consumes one saved word and then requires the expression stack to be empty. Thus both outgoing edges have depth zero, and a comparison cannot discard an unrelated expression temporary. The backend implements the relation with POP BX, CMP BX,AX, and an opposite short condition around a near JMP.

The test compares 65535 with one and takes the unsigned greater-than branch. A signed interpretation of those bits would produce a different result. Missing operands remain translation-time stack errors.

## Source changes

Copy `IR21.ASM` to `IR22.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_JNZ:`

Unchanged code immediately before the edit:

```asm
T_JNZ:
DB 67,77,80,32,65,88,44,48,13,10,74,69,32,73,63,13
DB 10,74,77,80,32,85,95,64,13,10,73,63,58,13,10,0
```

Insert after old physical line 1173, before the following old line.

Insert this source:

```asm

T_EQ:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,78,69,32,73,63,13,10,74,77,80,32,85
DB 95,64,13,10,73,63,58,13,10,0

T_NE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,69,32,73,63,13,10,74,77,80,32,85,95
DB 64,13,10,73,63,58,13,10,0

T_ULT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,65,69,32,73,63,13,10,74,77,80,32,85
DB 95,64,13,10,73,63,58,13,10,0

T_ULE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,65,32,73,63,13,10,74,77,80,32,85,95
DB 64,13,10,73,63,58,13,10,0

T_UGT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,66,69,32,73,63,13,10,74,77,80,32,85
DB 95,64,13,10,73,63,58,13,10,0

T_UGE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,66,32,73,63,13,10,74,77,80,32,85,95
DB 64,13,10,73,63,58,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_JZ
DB 74,78,90,0,0,0,0,0,7,3,9,0
DW T_JNZ
```

Insert after old physical line 955, before the following old line.

Insert this source:

```asm
DB 69,81,0,0,0,0,0,0,7,4,8,0
DW T_EQ
DB 78,69,0,0,0,0,0,0,7,4,8,0
DW T_NE
DB 85,76,84,0,0,0,0,0,7,4,8,0
DW T_ULT
DB 85,76,69,0,0,0,0,0,7,4,8,0
DW T_ULE
DB 85,71,84,0,0,0,0,0,7,4,8,0
DW T_UGT
DB 85,71,69,0,0,0,0,0,7,4,8,0
DW T_UGE
```

### Change 3: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 489–489 in `IR21.ASM`):

```asm
MOV CX,27
```

Put this source in their place:

```asm
MOV CX,33
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR22` at ASM0's `Source name:` prompt. Require `OK 03313 bytes` followed by PASS. This builds `IR22.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T22.IR` with `COPY CON T22.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 65535
PUSH
LIT 1
UGT GOOD
LIT 1
EXIT
LABEL GOOD
LIT 0
EXIT
```

```dos
CHECK IR22
```

Enter `T22` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T22
OK T22.ASM 00240 text bytes
PASS
```

Run `TYPE T22.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_MAIN:
MOV AX,65535
PUSH AX
MOV AX,1
POP BX
CMP BX,AX
JBE I0001
JMP U_GOOD
I0001:
MOV AX,1
MOV AH,4CH
INT 21H
U_GOOD:
MOV AX,0
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T22`. Require `OK 00044 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T22.COM`, and require length **44 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
FF FF 50 B8 01 00 5B 3B D8 76 03 E9 07 00 B8 01
00 B4 4C CD 21 B8 00 00 B4 4C CD 21
```

`T22.COM` is a complete program. Run `CHECK T22`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X22.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
EQ MAIN
```

Run `CHECK IR22` and enter `X22`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.
