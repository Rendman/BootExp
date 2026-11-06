+++
title = "20 \u00b7 An unconditional transfer"
weight = 20
description = "Transfer to a named code label with an empty expression stack."
download = "IR20.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

JMP lets one basic block transfer to another. The backend must implement the named transfer within its target limits.

## Operation and backend

JMP name emits the near form JMP U_name. Its displacement is resolved by ASM0 from the following instruction to the named label. The target can be forward or backward within the program segment.

The table marks JMP as a terminal control boundary. FLOW requires the expression stack to be empty; LAST suppresses an unnecessary fall-through exit when JMP is the last statement. The translator does not prove that a jump targets code rather than data.

The test jumps over a nonzero EXIT to a zero EXIT. The generated name stays symbolic in the .ASM file, which demonstrates why the translator need not maintain a second address-resolution mechanism.

## Source changes

Copy `IR19.ASM` to `IR20.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_BUFFER:`

Unchanged code immediately before the edit:

```asm

T_BUFFER:
DB 0
```

Insert after old physical line 1104, before the following old line.

Insert this source:

```asm

T_JMP:
DB 74,77,80,32,85,95,64,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_PUTB
DB 66,85,70,70,69,82,0,0,6,0,0,0
DW T_BUFFER
```

Insert after old physical line 905, before the following old line.

Insert this source:

```asm
DB 74,77,80,0,0,0,0,0,2,5,3,0
DW T_JMP
```

### Change 3: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 489–489 in `IR19.ASM`):

```asm
MOV CX,24
```

Put this source in their place:

```asm
MOV CX,25
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR20` at ASM0's `Source name:` prompt. Require `OK 02794 bytes` followed by PASS. This builds `IR20.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T20.IR` with `COPY CON T20.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
JMP GOOD
LIT 1
EXIT
LABEL GOOD
LIT 0
EXIT
```

```dos
CHECK IR20
```

Enter `T20` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T20
OK T20.ASM 00169 text bytes
PASS
```

Run `TYPE T20.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_MAIN:
JMP U_GOOD
MOV AX,1
MOV AH,4CH
INT 21H
U_GOOD:
MOV AX,0
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T20`. Require `OK 00032 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T20.COM`, and require length **32 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 E9
07 00 B8 01 00 B4 4C CD 21 B8 00 00 B4 4C CD 21
```

`T20.COM` is a complete program. Run `CHECK T20`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X20.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
JMP GOOD EXTRA
```

Run `CHECK IR20` and enter `X20`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 1
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.
