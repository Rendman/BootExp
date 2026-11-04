+++
title = "27 \u00b7 Reading a byte or end of input"
weight = 27
description = "Keep all byte values distinct from the end-of-input sentinel."
download = "IR27.ASM"
+++

GETC reports a byte or a distinct end-of-input word, with errors reported through STATUS.

## Operation and backend

GETC returns zero through 255 for a byte, or 65535 at end of input. EOF is successful and leaves STATUS zero; an input error returns 65535 with STATUS one. A byte value 255 is therefore distinct from EOF. The expression stack is empty at the service boundary.

The DOS binding translates a one-byte handle read into this contract. Its register choices and carry result stay inside the runtime. Terminal buffering and echo are environment details; use redirected byte input for a reproducible check.

The test saves its input before observing STATUS. Equality branches retain the right operand, so LETTER is reloaded before PUTC. Input Q produces Q; empty input takes the EOF path without output.

## Source changes

Copy `IR26.ASM` to `IR27.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_PUTC:`

Unchanged code immediately before the edit:

```asm

T_PUTC:
DB 67,65,76,76,32,82,95,80,85,84,67,13,10,0
```

Insert after old physical line 1303, before the following old line.

Insert this source:

```asm

T_GETC:
DB 67,65,76,76,32,82,95,71,69,84,67,13,10,0
```

### Change 2: following `T_RTPUTC:`

Unchanged code immediately before the edit:

```asm
DB 68,13,10,74,77,80,32,82,95,69,82,82,79,82,13,10
DB 82,95,80,85,84,71,79,79,68,58,13,10,74,77,80,32
DB 82,95,79,75,13,10,13,10,0
```

Insert after old physical line 1133, before the following old line.

Insert this source:

```asm

T_RTGETC:
DB 82,95,71,69,84,67,58,13,10,77,79,86,32,66,88,44
DB 48,13,10,77,79,86,32,67,88,44,49,13,10,77,79,86
DB 32,68,88,44,82,95,66,89,84,69,13,10,77,79,86,32
DB 65,72,44,51,70,72,13,10,73,78,84,32,50,49,72,13
DB 10,74,65,69,32,82,95,71,69,84,67,79,85,78,84,13
DB 10,77,79,86,32,65,88,44,54,53,53,51,53,13,10,74
DB 77,80,32,82,95,69,82,82,79,82,13,10,82,95,71,69
DB 84,67,79,85,78,84,58,13,10,67,77,80,32,65,88,44
DB 48,13,10,74,78,69,32,82,95,71,69,84,66,89,84,69
DB 13,10,77,79,86,32,65,88,44,54,53,53,51,53,13,10
DB 74,77,80,32,82,95,79,75,13,10,82,95,71,69,84,66
DB 89,84,69,58,13,10,77,79,86,32,65,76,44,91,82,95
DB 66,89,84,69,93,13,10,77,79,86,32,65,72,44,48,13
DB 10,74,77,80,32,82,95,79,75,13,10,13,10,0
```

### Change 3: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_STATUS
DB 80,85,84,67,0,0,0,0,0,3,3,0
DW T_PUTC
```

Insert after old physical line 991, before the following old line.

Insert this source:

```asm
DB 71,69,84,67,0,0,0,0,0,3,3,0
DW T_GETC
```

### Change 4: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 497–497 in `IR26.ASM`):

```asm
MOV CX,41
```

Put this source in their place:

```asm
MOV CX,42
```

### Change 5: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
MOV SI,T_RTRESULT
CALL OUTTEXT
MOV SI,T_RTPUTC
```

Insert after old physical line 38, before the following old line.

Insert this source:

```asm
CALL OUTTEXT
MOV SI,T_RTGETC
```

### Change 6: following `ROOM:`

Unchanged code immediately before the edit:

```asm
MOV [OUTPTR],AX
MOV AX,74
MOV [TARGETSIZE],AX
```

Remove these exact old lines (physical positions 14–14 in `IR26.ASM`):

```asm
MOV AX,9
```

Put this source in their place:

```asm
MOV AX,12
```

### Change 7: following `ROOM:`

Unchanged code immediately before the edit:

```asm
CALL GETNAME
MOV AX,6000H
MOV [OUTPTR],AX
```

Remove these exact old lines (physical positions 12–12 in `IR26.ASM`):

```asm
MOV AX,74
```

Put this source in their place:

```asm
MOV AX,116
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR27` at ASM86's `Source name:` prompt. Require `OK 04263 bytes` followed by PASS. This builds `IR27.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T27.IR` with `COPY CON T27.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
WORD LETTER 0
LABEL MAIN
GETC
ST LETTER
STATUS
JNZ FAILURE
LD LETTER
PUSH
LIT 65535
EQ DONE
LD LETTER
PUTC
STATUS
EXIT
LABEL DONE
HALT
LABEL FAILURE
LIT 1
EXIT
```

```dos
CHECK IR27
```

Enter `T27` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T27
OK T27.ASM 00994 text bytes
PASS
```

Run `TYPE T27.ASM`. The program prefix must be as follows; the backend runtime follows it.

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_LETTER:
DW 0
U_MAIN:
CALL R_GETC
MOV [U_LETTER],AX
MOV AX,[R_STATUS]
CMP AX,0
JE I0001
JMP U_FAILURE
I0001:
MOV AX,[U_LETTER]
PUSH AX
MOV AX,65535
POP BX
CMP BX,AX
JNE I0002
JMP U_DONE
I0002:
MOV AX,[U_LETTER]
CALL R_PUTC
MOV AX,[R_STATUS]
MOV AH,4CH
INT 21H
U_DONE:
MOV AX,4C00H
INT 21H
U_FAILURE:
MOV AX,1
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T27`. Require `OK 00181 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T27.COM`, and require length **181 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

This checkpoint includes the runtime fragments introduced so far. The reference lists the complete final binding. Compare the leading bytes below; the viewer must still report the full file length.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 02 00 00
00 E8 74 00 89 06 0F 01 8B 06 B2 01 81 F8 00 00
74 03 E9 24 00 8B 06 0F 01 50 B8 FF FF 5B 3B D8
75 03 E9 0F 00 8B 06 0F 01 E8 2A 00 8B 06 B2 01
```

`T27.COM` is a complete program. Create KEY.TXT with `ECHO Q>KEY.TXT`. Run `CHECK T27 <KEY.TXT`. It displays `Q` and then the checker reports PASS.

## A rejection check

Enter this separate input as `X27.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
GETC EXTRA
```

Run `CHECK IR27` and enter `X27`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 1
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.
