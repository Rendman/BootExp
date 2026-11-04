+++
title = "24 \u00b7 Calling a procedure"
weight = 24
description = "Balance expression temporaries before native calls and returns."
download = "IR24.ASM"
+++

A repeated computation can be placed under a label and called by name.

## How it works

CALL emits a near CALL U_name and RET emits the matching near return. AX carries an input and a returned result by convention. Other ordinary registers and flags are scratch unless the procedure explicitly preserves them through its own program logic.

Both operations require expression depth zero. Native CALL puts a return offset on SS:SP; the called block may use balanced expression temporaries above that offset. The static empty-boundary rule prevents POP from treating the return address as an expression operand. There is no parameter list or automatic local-variable frame.

Place procedure bodies after a terminating main path or jump around them. A label alone does not prevent fall-through. Native call depth and recursion are not bounded by DEPTH; keep the reserved high stack area clear and call nesting modest. The test returns a zero result from ANSWER to the main EXIT.

## Source changes

Copy `IR23.ASM` to `IR24.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_SGE:`

Unchanged code immediately before the edit:

```asm
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,76,32,73,63,13,10,74,77,80,32,85,95
DB 64,13,10,73,63,58,13,10,0
```

Insert after old physical line 1243, before the following old line.

Insert this source:

```asm

T_CALL:
DB 67,65,76,76,32,85,95,64,13,10,0

T_RET:
DB 82,69,84,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_SGT
DB 83,71,69,0,0,0,0,0,7,4,8,0
DW T_SGE
```

Insert after old physical line 975, before the following old line.

Insert this source:

```asm
DB 67,65,76,76,0,0,0,0,2,3,3,0
DW T_CALL
DB 82,69,84,0,0,0,0,0,0,5,1,0
DW T_RET
```

### Change 3: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 489–489 in `IR23.ASM`):

```asm
MOV CX,37
```

Put this source in their place:

```asm
MOV CX,39
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR24` at ASM86's `Source name:` prompt. Require `OK 03580 bytes` followed by PASS. This builds `IR24.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T24.IR` with `COPY CON T24.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
CALL ANSWER
EXIT
LABEL ANSWER
LIT 0
RET
```

```dos
CHECK IR24
```

Enter `T24` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T24
OK T24.ASM 00148 text bytes
PASS
```

Run `TYPE T24.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_MAIN:
CALL U_ANSWER
MOV AH,4CH
INT 21H
U_ANSWER:
MOV AX,0
RET
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T24`. Require `OK 00026 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T24.COM`, and require length **26 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 E8
04 00 B4 4C CD 21 B8 00 00 C3
```

`T24.COM` is a complete program. Run `CHECK T24`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X24.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
LIT 1
PUSH
CALL ANSWER
```

Run `CHECK IR24` and enter `X24`. Require this diagnostic and FAIL:

```text
IR ERROR 00004 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. A DOS carry branch must immediately follow DOS apart from empty or comment lines.
