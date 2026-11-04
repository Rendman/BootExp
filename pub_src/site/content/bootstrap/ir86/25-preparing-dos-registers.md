+++
title = "25 \u00b7 A portable runtime status"
weight = 25
description = "Observe an ordinary word result without exposing processor flags."
download = "IR25.ASM"
+++

Input and output need a defined failure result which remains meaningful on different processors and operating systems.

## Operation and backend

STATUS replaces virtual accumulator A with the result of the most recent runtime service: zero means success and one means failure. At program entry that value is zero. Ordinary arithmetic, storage, and comparisons do not change it. A procedure can change it by performing a service.

The 8086 binding stores this word in R_STATUS. Its STATUS pattern is a word load; the compiler appends runtime data after the program exit. Target-byte and definition accounting reserve that data before user operations. R_ names belong to the binding, separate from U_ program names.

The language exposes neither a CPU flag nor an operating-system error number. Another backend can represent the status differently while preserving the returned word. The test disturbs A and then observes the initial zero.

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

T_STATUS:
DB 77,79,86,32,65,88,44,91,82,95,83,84,65,84,85,83
DB 93,13,10,0
```

### Change 2: following `ZERONEXT:`

Unchanged code immediately before the edit:

```asm

ZERONEXT:
DB 44,48,0
```

Insert after old physical line 1093, before the following old line.

Insert this source:

```asm

T_RTSTATUS:
DB 82,95,83,84,65,84,85,83,58,13,10,68,87,32,48,13
DB 10,0
```

### Change 3: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_CALL
DB 82,69,84,0,0,0,0,0,0,5,1,0
DW T_RET
```

Insert after old physical line 979, before the following old line.

Insert this source:

```asm
DB 83,84,65,84,85,83,0,0,0,0,4,0
DW T_STATUS
```

### Change 4: following `STATWORD:`

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
MOV CX,40
```

### Change 5: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
MAINPRESENT:
CALL BALANCED
CALL FINISHOUTPUT
```

Insert after old physical line 35, before the following old line.

Insert this source:

```asm
MOV SI,T_RTSTATUS
CALL OUTTEXT
```

### Change 6: following `ROOM:`

Unchanged code immediately before the edit:

```asm
MOV [OUTPTR],AX
MOV AX,15
MOV [TARGETSIZE],AX
```

Remove these exact old lines (physical positions 14–14 in `IR24.ASM`):

```asm
MOV AX,1
```

Put this source in their place:

```asm
MOV AX,2
```

### Change 7: following `ROOM:`

Unchanged code immediately before the edit:

```asm
CALL GETNAME
MOV AX,6000H
MOV [OUTPTR],AX
```

Remove these exact old lines (physical positions 12–12 in `IR24.ASM`):

```asm
MOV AX,15
```

Put this source in their place:

```asm
MOV AX,17
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR25` at ASM86's `Source name:` prompt. Require `OK 03638 bytes` followed by PASS. This builds `IR25.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T25.IR` with `COPY CON T25.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 99
STATUS
EXIT
```

```dos
CHECK IR25
```

Enter `T25` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T25
OK T25.ASM 00154 text bytes
PASS
```

Run `TYPE T25.ASM`. The program prefix must be as follows; the backend runtime follows it.

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_MAIN:
MOV AX,99
MOV AX,[R_STATUS]
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T25`. Require `OK 00028 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T25.COM`, and require length **28 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

This checkpoint includes the runtime fragments introduced so far. The reference lists the complete final binding. Compare the leading bytes below; the viewer must still report the full file length.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
63 00 8B 06 1A 01 B4 4C CD 21 00 00
```

`T25.COM` is a complete program. Run `CHECK T25`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X25.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
STATUS EXTRA
```

Run `CHECK IR25` and enter `X25`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 1
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.
