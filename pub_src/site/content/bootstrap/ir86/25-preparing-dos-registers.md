+++
title = "25 \u00b7 Preparing DOS registers"
weight = 25
description = "Move words between AX and the three DOS argument registers."
download = "IR25.ASM"
+++

DOS handle services take arguments in BX, CX, and DX. Small register-transfer operations connect the accumulator model to that interface.

## How it works

TOBX, TOCX, and TODX copy AX into the named register. FROMBX, FROMCX, and FROMDX copy it back into AX. Each lowers to one ordinary word MOV, changes no expression-stack depth, and leaves arithmetic flags unchanged.

These registers are not independent IR variables. Binary operators and pointer operations use BX as scratch. Prepare DOS argument registers after any computation which might disturb them, then load AX with the service number and call DOS. Values which must survive arbitrary procedures belong in named storage.

No segment register or SP transfer is provided. DS remains the program segment, pointers are offsets within it, and the expression/call-stack convention remains intact. The test saves zero in DX, disturbs AX, then retrieves the saved value for EXIT.

## Source changes

Copy `IR24.ASM` to `IR25.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_RET:`

Unchanged code immediately before the edit:

```asm

T_RET:
DB 82,69,84,13,10,0
```

Insert after old physical line 1253, before the following old line.

Insert this source:

```asm

T_TOBX:
DB 77,79,86,32,66,88,44,65,88,13,10,0

T_TOCX:
DB 77,79,86,32,67,88,44,65,88,13,10,0

T_TODX:
DB 77,79,86,32,68,88,44,65,88,13,10,0

T_FROMBX:
DB 77,79,86,32,65,88,44,66,88,13,10,0

T_FROMCX:
DB 77,79,86,32,65,88,44,67,88,13,10,0

T_FROMDX:
DB 77,79,86,32,65,88,44,68,88,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_CALL
DB 82,69,84,0,0,0,0,0,0,5,1,0
DW T_RET
```

Insert after old physical line 979, before the following old line.

Insert this source:

```asm
DB 84,79,66,88,0,0,0,0,0,0,2,0
DW T_TOBX
DB 84,79,67,88,0,0,0,0,0,0,2,0
DW T_TOCX
DB 84,79,68,88,0,0,0,0,0,0,2,0
DW T_TODX
DB 70,82,79,77,66,88,0,0,0,0,2,0
DW T_FROMBX
DB 70,82,79,77,67,88,0,0,0,0,2,0
DW T_FROMCX
DB 70,82,79,77,68,88,0,0,0,0,2,0
DW T_FROMDX
```

### Change 3: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 489–489 in `IR24.ASM`):

```asm
MOV CX,39
```

Put this source in their place:

```asm
MOV CX,45
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR25` at ASM86's `Source name:` prompt. Require `OK 03736 bytes` followed by PASS. This builds `IR25.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T25.IR` with `COPY CON T25.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 0
TODX
LIT 99
FROMDX
EXIT
```

```dos
CHECK IR25
```

Enter `T25` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T25
OK T25.ASM 00150 text bytes
PASS
```

Run `TYPE T25.ASM`. Its complete text must be:

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
MOV DX,AX
MOV AX,99
MOV AX,DX
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T25`. Require `OK 00029 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T25.COM`, and require length **29 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
00 00 8B D0 B8 63 00 8B C2 B4 4C CD 21
```

`T25.COM` is a complete program. Run `CHECK T25`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X25.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
TOCX EXTRA
```

Run `CHECK IR25` and enter `X25`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 1
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. A DOS carry branch must immediately follow DOS apart from empty or comment lines.
