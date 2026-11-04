+++
title = "13 \u00b7 Adding and subtracting"
weight = 13
description = "Combine a saved left operand with the accumulator right operand."
download = "IR13.ASM"
+++

An arithmetic operation can consume the saved left operand and leave its result in AX.

## How it works

ADD pops the left word into BX and adds it to AX. SUB must retain operand order: it pops BX, subtracts AX from BX, and copies BX to AX. Thus LIT 7, PUSH, LIT 3, SUB computes seven minus three.

Both operations require one saved word and reduce DEPTH by one. Their arithmetic wraps modulo 65536; there is no overflow exception or signed-literal syntax. The same word bits can be interpreted as unsigned or signed when an operation explicitly says which comparison to make.

BX and arithmetic flags are scratch registers for these emitted operations. AX is the result. The test combines subtraction and addition and finally subtracts the known result, so CHECK can report a visible PASS for a computed zero.

## Source changes

Copy `IR12.ASM` to `IR13.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_POP:`

Unchanged code immediately before the edit:

```asm

T_POP:
DB 80,79,80,32,65,88,13,10,0
```

Insert after old physical line 926, before the following old line.

Insert this source:

```asm

T_ADD:
DB 80,79,80,32,66,88,13,10,65,68,68,32,65,88,44,66
DB 88,13,10,0

T_SUB:
DB 80,79,80,32,66,88,13,10,83,85,66,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,66,88,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_PUSH
DB 80,79,80,0,0,0,0,0,0,2,1,0
DW T_POP
```

Insert after old physical line 788, before the following old line.

Insert this source:

```asm
DB 65,68,68,0,0,0,0,0,0,2,3,0
DW T_ADD
DB 83,85,66,0,0,0,0,0,0,2,5,0
DW T_SUB
```

### Change 3: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 485–485 in `IR12.ASM`):

```asm
MOV CX,13
```

Put this source in their place:

```asm
MOV CX,15
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR13` at ASM86's `Source name:` prompt. Require `OK 02226 bytes` followed by PASS. This builds `IR13.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T13.IR` with `COPY CON T13.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 7
PUSH
LIT 3
SUB
PUSH
LIT 2
ADD
PUSH
LIT 6
SUB
EXIT
```

```dos
CHECK IR13
```

Enter `T13` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T13
OK T13.ASM 00253 text bytes
PASS
```

Run `TYPE T13.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_MAIN:
MOV AX,7
PUSH AX
MOV AX,3
POP BX
SUB BX,AX
MOV AX,BX
PUSH AX
MOV AX,2
POP BX
ADD AX,BX
PUSH AX
MOV AX,6
POP BX
SUB BX,AX
MOV AX,BX
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T13`. Require `OK 00047 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T13.COM`, and require length **47 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
07 00 50 B8 03 00 5B 2B D8 8B C3 50 B8 02 00 5B
03 C3 50 B8 06 00 5B 2B D8 8B C3 B4 4C CD 21
```

`T13.COM` is a complete program. Run `CHECK T13`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X13.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
ADD
```

Run `CHECK IR13` and enter `X13`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.
