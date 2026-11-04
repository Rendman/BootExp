+++
title = "12 \u00b7 A bounded expression stack"
weight = 12
description = "Save A and retrieve it with an explicit stack effect."
download = "IR12.ASM"
cartoon = "ir86-plates.png"
+++

One accumulator cannot retain both sides of an expression. PUSH saves its word; POP restores the latest saved word.

## Operation and backend

The expression stack is an abstract stack of IR words. This backend implements it with native PUSH AX and POP AX. DEPTH is a translation-time count, initially zero. FLOW checks each table effect before emitting it: PUSH adds one, POP requires a saved word and removes one, and a control boundary requires an empty expression stack. BALANCED performs that common boundary check.

The bound is thirty-two saved words. It limits expression bookkeeping and temporary stack demand without pretending to limit the CPU's stack. The IR verification rule requires an empty expression stack at a label, branch, procedure call, return, or termination. It applies independently of the target calling convention. Each basic block starts and ends with an empty expression stack.

This simple rule avoids a control-flow analysis of different stack depths arriving at one label. It permits straight expressions within a block and makes an unmatched POP a translation error. AX and arithmetic flags are scratch state in FLOW; its counters belong to the translator, not the emitted program.

## Source changes

Copy `IR11.ASM` to `IR12.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_STB:`

Unchanged code immediately before the edit:

```asm

T_STB:
DB 77,79,86,32,91,85,95,64,93,44,65,76,13,10,0
```

Insert after old physical line 868, before the following old line.

Insert this source:

```asm

T_PUSH:
DB 80,85,83,72,32,65,88,13,10,0

T_POP:
DB 80,79,80,32,65,88,13,10,0
```

### Change 2: following `TPL:`

Unchanged code immediately before the edit:

```asm
TPL:
DW 0

```

Insert after old physical line 811, before the following old line.

Insert this source:

```asm
DEPTH:
DW 0

```

### Change 3: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_LDB
DB 83,84,66,0,0,0,0,0,2,0,4,0
DW T_STB
```

Insert after old physical line 739, before the following old line.

Insert this source:

```asm
DB 80,85,83,72,0,0,0,0,0,1,1,0
DW T_PUSH
DB 80,79,80,0,0,0,0,0,0,2,1,0
DW T_POP
```

### Change 4: following `MAINBAD:`

Unchanged code immediately before the edit:

```asm
MOV AX,3
JMP ERROR

```

Insert after old physical line 707, before the following old line.

Insert this source:

```asm
FLOW:
MOV AL,[EFFECT]
FLOWORDINARY:
CMP AL,0
JE FLOWDONE
CMP AL,1
JE STACKPUSH
CMP AL,2
JE STACKPOP
CMP AL,4
JE STACKPOP
JMP BALANCED
STACKPUSH:
MOV AX,[DEPTH]
CMP AX,32
JAE STACKFULL
INC AX
MOV [DEPTH],AX
RET
STACKPOP:
MOV AX,[DEPTH]
CMP AX,0
JE STACKBAD
DEC AX
MOV [DEPTH],AX
MOV AL,[EFFECT]
CMP AL,4
JE BALANCED
FLOWDONE:
RET
STACKFULL:
MOV AX,5
JMP ERROR

BALANCED:
MOV AX,[DEPTH]
CMP AX,0
JNE STACKBAD
RET
STACKBAD:
MOV AX,4
JMP ERROR

```

### Change 5: following `STATLAST:`

Unchanged code immediately before the edit:

```asm
CALL ARGUMENTS
CALL FINISH
CALL CONTEXT
```

Insert after old physical line 513, before the following old line.

Insert this source:

```asm
CALL FLOW
```

### Change 6: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 484–484 in `IR11.ASM`):

```asm
MOV CX,11
```

Put this source in their place:

```asm
MOV CX,13
```

### Change 7: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
MOV AX,3
JMP ERROR
MAINPRESENT:
```

Insert after old physical line 29, before the following old line.

Insert this source:

```asm
CALL BALANCED
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR12` at ASM86's `Source name:` prompt. Require `OK 02147 bytes` followed by PASS. This builds `IR12.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T12.IR` with `COPY CON T12.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 0
PUSH
LIT 99
POP
EXIT
```

```dos
CHECK IR12
```

Enter `T12` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T12
OK T12.ASM 00145 text bytes
PASS
```

Run `TYPE T12.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_MAIN:
MOV AX,0
PUSH AX
MOV AX,99
POP AX
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T12`. Require `OK 00027 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T12.COM`, and require length **27 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
00 00 50 B8 63 00 58 B4 4C CD 21
```

`T12.COM` is a complete program. Run `CHECK T12`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X12.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
POP
```

Run `CHECK IR12` and enter `X12`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.
