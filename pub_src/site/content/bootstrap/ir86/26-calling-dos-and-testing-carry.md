+++
title = "26 \u00b7 Writing one byte"
weight = 26
description = "A stream service has a value result and a separate status."
download = "IR26.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

PUTC writes a byte to the output stream without making a program arrange target registers.

## Operation and backend

PUTC takes the low eight bits of A as a byte. It returns one after writing that byte, or zero on failure, and updates STATUS. It requires an empty expression stack and performs no newline conversion. The status can be read after intervening ordinary operations because it is a stored language value.

The DOS binding stores the byte in R_BYTE and writes it to its output handle. R_OK sets the status to zero while retaining the result; R_ERROR sets it to one; R_FAIL supplies a zero result on failure. Register choices and the operating-system call belong to these backend routines.

The compiler emits CALL R_PUTC for this binding. Runtime text is appended in separate fragments so tested parts remain in place. The test writes I, disturbs A, then returns the observed success status.

## Source changes

Copy `IR25.ASM` to `IR26.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_STATUS:`

Unchanged code immediately before the edit:

```asm
T_STATUS:
DB 77,79,86,32,65,88,44,91,82,95,83,84,65,84,85,83
DB 93,13,10,0
```

Insert after old physical line 1265, before the following old line.

Insert this source:

```asm

T_PUTC:
DB 67,65,76,76,32,82,95,80,85,84,67,13,10,0
```

### Change 2: following `T_RTSTATUS:`

Unchanged code immediately before the edit:

```asm

T_RTSTATUS:
DB 82,95,83,84,65,84,85,83,58,13,10,68,87,32,48,13
```

Remove these exact old lines (physical positions 1101–1101 in `IR25.ASM`):

```asm
DB 10,0
```

Put this source in their place:

```asm
DB 10,13,10,0

T_RTRESULT:
DB 82,95,79,75,58,13,10,77,79,86,32,68,88,44,48,13
DB 10,77,79,86,32,91,82,95,83,84,65,84,85,83,93,44
DB 68,88,13,10,82,69,84,13,10,82,95,69,82,82,79,82
DB 58,13,10,77,79,86,32,68,88,44,49,13,10,77,79,86
DB 32,91,82,95,83,84,65,84,85,83,93,44,68,88,13,10
DB 82,69,84,13,10,82,95,70,65,73,76,58,13,10,77,79
DB 86,32,65,88,44,48,13,10,74,77,80,32,82,95,69,82
DB 82,79,82,13,10,13,10,0

T_RTPUTC:
DB 82,95,80,85,84,67,58,13,10,77,79,86,32,91,82,95
DB 66,89,84,69,93,44,65,76,13,10,77,79,86,32,66,88
DB 44,49,13,10,77,79,86,32,67,88,44,49,13,10,77,79
DB 86,32,68,88,44,82,95,66,89,84,69,13,10,77,79,86
DB 32,65,72,44,52,48,72,13,10,73,78,84,32,50,49,72
DB 13,10,74,65,69,32,82,95,80,85,84,67,79,85,78,84
DB 13,10,74,77,80,32,82,95,70,65,73,76,13,10,82,95
DB 80,85,84,67,79,85,78,84,58,13,10,67,77,80,32,65
DB 88,44,49,13,10,74,69,32,82,95,80,85,84,71,79,79
DB 68,13,10,74,77,80,32,82,95,69,82,82,79,82,13,10
DB 82,95,80,85,84,71,79,79,68,58,13,10,74,77,80,32
DB 82,95,79,75,13,10,13,10,0

T_RTBYTE:
DB 82,95,66,89,84,69,58,13,10,68,66,32,48,13,10,0
```

### Change 3: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_RET
DB 83,84,65,84,85,83,0,0,0,0,4,0
DW T_STATUS
```

Insert after old physical line 983, before the following old line.

Insert this source:

```asm
DB 80,85,84,67,0,0,0,0,0,3,3,0
DW T_PUTC
```

### Change 4: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 491–491 in `IR25.ASM`):

```asm
MOV CX,40
```

Put this source in their place:

```asm
MOV CX,41
```

### Change 5: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
CALL BALANCED
CALL FINISHOUTPUT
MOV SI,T_RTSTATUS
```

Insert after old physical line 36, before the following old line.

Insert this source:

```asm
CALL OUTTEXT
MOV SI,T_RTBYTE
```

### Change 6: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
MAINPRESENT:
CALL BALANCED
CALL FINISHOUTPUT
```

Insert after old physical line 35, before the following old line.

Insert this source:

```asm
MOV SI,T_RTRESULT
CALL OUTTEXT
MOV SI,T_RTPUTC
CALL OUTTEXT
```

### Change 7: following `ROOM:`

Unchanged code immediately before the edit:

```asm
MOV [OUTPTR],AX
MOV AX,17
MOV [TARGETSIZE],AX
```

Remove these exact old lines (physical positions 14–14 in `IR25.ASM`):

```asm
MOV AX,2
```

Put this source in their place:

```asm
MOV AX,9
```

### Change 8: following `ROOM:`

Unchanged code immediately before the edit:

```asm
CALL GETNAME
MOV AX,6000H
MOV [OUTPTR],AX
```

Remove these exact old lines (physical positions 12–12 in `IR25.ASM`):

```asm
MOV AX,17
```

Put this source in their place:

```asm
MOV AX,74
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR26` at ASM0's `Source name:` prompt. Require `OK 04007 bytes` followed by PASS. This builds `IR26.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T26.IR` with `COPY CON T26.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 73
PUTC
LIT 99
STATUS
EXIT
```

```dos
CHECK IR26
```

Enter `T26` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T26
OK T26.ASM 00498 text bytes
PASS
```

Run `TYPE T26.ASM`. The program prefix must be as follows; the backend runtime follows it.

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_MAIN:
MOV AX,73
CALL R_PUTC
MOV AX,99
MOV AX,[R_STATUS]
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T26`. Require `OK 00091 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T26.COM`, and require length **91 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

This checkpoint includes the runtime fragments introduced so far. The reference lists the complete final binding. Compare the leading bytes below; the viewer must still report the full file length.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
49 00 E8 21 00 B8 63 00 8B 06 58 01 B4 4C CD 21
BA 00 00 89 16 58 01 C3 BA 01 00 89 16 58 01 C3
B8 00 00 E9 F2 FF 88 06 5A 01 BB 01 00 B9 01 00
```

`T26.COM` is a complete program. Run `CHECK T26`. It displays `I` and then the checker reports PASS.

## A rejection check

Enter this separate input as `X26.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
LIT 1
PUSH
PUTC
```

Run `CHECK IR26` and enter `X26`. Require this diagnostic and FAIL:

```text
IR ERROR 00004 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.
