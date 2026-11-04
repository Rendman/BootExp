+++
title = "26 \u00b7 Calling DOS and testing carry"
weight = 26
description = "Use INT 21H with a checked, immediate carry branch."
download = "IR26.ASM"
+++

A useful translation target must perform console and file I/O without an outside runtime library.

## How it works

DOS emits INT 21H. AX supplies the service and, where required, an AL argument; BX, CX, and DX supply its other documented arguments. AX and other documented DOS results remain available afterward. DOS is an empty-expression-stack boundary.

JC and JNC use an opposite short carry condition around a near JMP. They must be the next nonempty statement after DOS. HASCARRY enforces that rule during translation: effect six establishes a pending carry result and effect seven consumes it; another instruction or label clears it. Comments and blank lines emit nothing and do not consume it.

The test deliberately tries to close the invalid handle FFFFH. DOS must set carry; JC selects the success path of this test. That path displays I with function 02H and returns zero through EXIT. A carry branch without a preceding DOS operation is a translation error. Check the DOS manual for each service's result registers and carry convention; the translator does not infer them.

## Source changes

Copy `IR25.ASM` to `IR26.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_FROMDX:`

Unchanged code immediately before the edit:

```asm

T_FROMDX:
DB 77,79,86,32,65,88,44,68,88,13,10,0
```

Insert after old physical line 1283, before the following old line.

Insert this source:

```asm

T_DOS:
DB 73,78,84,32,50,49,72,13,10,0

T_JC:
DB 74,65,69,32,73,63,13,10,74,77,80,32,85,95,64,13
DB 10,73,63,58,13,10,0

T_JNC:
DB 74,66,32,73,63,13,10,74,77,80,32,85,95,64,13,10
DB 73,63,58,13,10,0
```

### Change 2: following `LAST:`

Unchanged code immediately before the edit:

```asm
DB 0

LAST:
```

Insert after old physical line 1098, before the following old line.

Insert this source:

```asm
DB 0

HASCARRY:
```

### Change 3: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_FROMCX
DB 70,82,79,77,68,88,0,0,0,0,2,0
DW T_FROMDX
```

Insert after old physical line 991, before the following old line.

Insert this source:

```asm
DB 68,79,83,0,0,0,0,0,0,6,2,0
DW T_DOS
DB 74,67,0,0,0,0,0,0,7,7,5,0
DW T_JC
DB 74,78,67,0,0,0,0,0,7,7,5,0
DW T_JNC
```

### Change 4: following `FLOW:`

Unchanged code immediately before the edit:

```asm

FLOW:
MOV AL,[EFFECT]
```

Insert after old physical line 790, before the following old line.

Insert this source:

```asm
MOV DL,[HASCARRY]
MOV AH,0
MOV [HASCARRY],AH
CMP AL,6
JNE FLOWCARRY
MOV AH,1
MOV [HASCARRY],AH
JMP BALANCED
FLOWCARRY:
CMP AL,7
JNE FLOWORDINARY
CMP DL,1
JNE STACKBAD
JMP BALANCED
```

### Change 5: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 489–489 in `IR25.ASM`):

```asm
MOV CX,45
```

Put this source in their place:

```asm
MOV CX,48
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR26` at ASM86's `Source name:` prompt. Require `OK 03871 bytes` followed by PASS. This builds `IR26.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T26.IR` with `COPY CON T26.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 65535
TOBX
LIT 3E00H
DOS
JC GOOD
LIT 1
EXIT
LABEL GOOD
LIT 73
TODX
LIT 200H
DOS
LIT 0
EXIT
```

```dos
CHECK IR26
```

Enter `T26` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T26
OK T26.ASM 00280 text bytes
PASS
```

Run `TYPE T26.ASM`. Its complete text must be:

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
MOV BX,AX
MOV AX,3E00H
INT 21H
JAE I0001
JMP U_GOOD
I0001:
MOV AX,1
MOV AH,4CH
INT 21H
U_GOOD:
MOV AX,73
MOV DX,AX
MOV AX,200H
INT 21H
MOV AX,0
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T26`. Require `OK 00054 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T26.COM`, and require length **54 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
FF FF 8B D8 B8 00 3E CD 21 73 03 E9 07 00 B8 01
00 B4 4C CD 21 B8 49 00 8B D0 B8 00 02 CD 21 B8
00 00 B4 4C CD 21
```

`T26.COM` is a complete program. Run `CHECK T26`. It displays `I` and then the checker reports PASS.

## A rejection check

Enter this separate input as `X26.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
JC MAIN
```

Run `CHECK IR26` and enter `X26`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. A DOS carry branch must immediately follow DOS apart from empty or comment lines.
