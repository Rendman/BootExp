+++
title = "23 \u00b7 Signed comparisons"
weight = 23
description = "Interpret the same word bits as two's-complement values."
download = "IR23.ASM"
+++

Signed ordering differs from unsigned ordering when the high bit is set. It must be requested explicitly.

## Operation and backend

SLT, SLE, SGT, and SGE compare the saved left word with A as signed values. Words with bit fifteen set represent -32768 through -1; the others represent zero through 32767. LIT still uses unsigned spelling, so 65535 supplies the bit pattern for -1.

Operand order, the consumed expression word, and the retained right operand in A match the unsigned comparisons. Equality needs no signed variant because equal bit patterns compare equal either way. The backend implements the relations with 8086 signed conditions after CMP BX,AX.

The test takes -1 less than one. It contrasts with the unsigned test while using the same numeric literal spellings. No signed arithmetic overflow exception is added: ADD and SUB still wrap as words.

## Source changes

Copy `IR22.ASM` to `IR23.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_UGE:`

Unchanged code immediately before the edit:

```asm
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,66,32,73,63,13,10,74,77,80,32,85,95
DB 64,13,10,73,63,58,13,10,0
```

Insert after old physical line 1215, before the following old line.

Insert this source:

```asm

T_SLT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,71,69,32,73,63,13,10,74,77,80,32,85
DB 95,64,13,10,73,63,58,13,10,0

T_SLE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,71,32,73,63,13,10,74,77,80,32,85,95
DB 64,13,10,73,63,58,13,10,0

T_SGT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,76,69,32,73,63,13,10,74,77,80,32,85
DB 95,64,13,10,73,63,58,13,10,0

T_SGE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,76,32,73,63,13,10,74,77,80,32,85,95
DB 64,13,10,73,63,58,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_UGT
DB 85,71,69,0,0,0,0,0,7,4,8,0
DW T_UGE
```

Insert after old physical line 967, before the following old line.

Insert this source:

```asm
DB 83,76,84,0,0,0,0,0,7,4,8,0
DW T_SLT
DB 83,76,69,0,0,0,0,0,7,4,8,0
DW T_SLE
DB 83,71,84,0,0,0,0,0,7,4,8,0
DW T_SGT
DB 83,71,69,0,0,0,0,0,7,4,8,0
DW T_SGE
```

### Change 3: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 489–489 in `IR22.ASM`):

```asm
MOV CX,33
```

Put this source in their place:

```asm
MOV CX,37
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR23` at ASM86's `Source name:` prompt. Require `OK 03535 bytes` followed by PASS. This builds `IR23.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T23.IR` with `COPY CON T23.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 65535
PUSH
LIT 1
SLT GOOD
LIT 1
EXIT
LABEL GOOD
LIT 0
EXIT
```

```dos
CHECK IR23
```

Enter `T23` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T23
OK T23.ASM 00240 text bytes
PASS
```

Run `TYPE T23.ASM`. Its complete text must be:

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
JGE I0001
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

Assemble that generated source with `CHECK ASMKEEP`, entering `T23`. Require `OK 00044 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T23.COM`, and require length **44 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
FF FF 50 B8 01 00 5B 3B D8 7D 03 E9 07 00 B8 01
00 B4 4C CD 21 B8 00 00 B4 4C CD 21
```

`T23.COM` is a complete program. Run `CHECK T23`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X23.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
SLT MAIN
```

Run `CHECK IR23` and enter `X23`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.
