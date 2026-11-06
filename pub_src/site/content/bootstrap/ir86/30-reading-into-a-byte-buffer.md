+++
title = "30 \u00b7 Reading into a byte buffer"
weight = 30
description = "Pass a handle, a destination, and a requested count as IR values."
download = "IR30.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

The expression stack supplies a portable argument order for a block read.

## Operation and backend

Save the handle with PUSH, then the buffer pointer with PUSH, and put the requested count in A. READ consumes both saved words and requires the remaining stack to be empty. It returns a byte count. Zero with STATUS zero means EOF; zero with STATUS one means failure. A short read is successful.

The 8086 pattern removes the two virtual arguments before calling R_READ. R_FIND validates the token and its access kind, then obtains the private descriptor. Reads require an OPEN handle; CREATE handles are write-only. The runtime saves the count and buffer while checking the token. A zero-length request succeeds without touching the buffer.

The test saves the returned count before observing STATUS, checks that one byte arrived, and writes that byte to the output stream. Its source mentions no target registers or flags.

## Source changes

Copy `IR29.ASM` to `IR30.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_CREATE:`

Unchanged code immediately before the edit:

```asm

T_CREATE:
DB 67,65,76,76,32,82,95,67,82,69,65,84,69,13,10,0
```

Insert after old physical line 1400, before the following old line.

Insert this source:

```asm

T_READ:
DB 80,79,80,32,68,88,13,10,80,79,80,32,66,88,13,10
DB 67,65,76,76,32,82,95,82,69,65,68,13,10,0
```

### Change 2: following `T_RTFILEDATA:`

Unchanged code immediately before the edit:

```asm
DB 83,76,79,84,58,13,10,68,87,32,48,13,10,82,95,78
DB 85,77,66,69,82,58,13,10,68,87,32,48,13,10,82,95
DB 72,65,78,68,76,69,83,58,13,10,68,87,32,48,44,48
```

Remove these exact old lines (physical positions 1224–1224 in `IR29.ASM`):

```asm
DB 44,48,44,48,44,48,44,48,44,48,44,48,13,10,0
```

Put this source in their place:

```asm
DB 44,48,44,48,44,48,44,48,44,48,44,48,13,10,13,10
DB 0

T_RTTRANSFERDATA:
DB 82,95,67,79,85,78,84,58,13,10,68,87,32,48,13,10
DB 82,95,66,85,70,70,69,82,58,13,10,68,87,32,48,13
DB 10,0
```

### Change 3: following `T_RTFILE:`

Unchanged code immediately before the edit:

```asm
DB 85,77,66,69,82,93,44,67,88,13,10,82,69,84,13,10
DB 13,10,0

```

Insert after old physical line 1213, before the following old line.

Insert this source:

```asm
T_RTFIND:
DB 82,95,70,73,78,68,58,13,10,67,77,80,32,66,88,44
DB 49,13,10,74,66,32,82,95,66,65,68,72,65,78,68,76
DB 69,13,10,67,77,80,32,66,88,44,56,13,10,74,65,32
DB 82,95,66,65,68,72,65,78,68,76,69,13,10,68,69,67
DB 32,66,88,13,10,65,68,68,32,66,88,44,66,88,13,10
DB 65,68,68,32,66,88,44,82,95,72,65,78,68,76,69,83
DB 13,10,77,79,86,32,91,82,95,83,76,79,84,93,44,66
DB 88,13,10,77,79,86,32,66,88,44,91,66,88,93,13,10
DB 67,77,80,32,66,88,44,48,13,10,74,69,32,82,95,66
DB 65,68,72,65,78,68,76,69,13,10,77,79,86,32,65,88
DB 44,49,13,10,67,77,80,32,66,88,44,56,48,48,48,72
DB 13,10,74,66,32,82,95,72,65,78,68,76,69,75,73,78
DB 68,13,10,65,78,68,32,66,88,44,55,70,70,70,72,13
DB 10,77,79,86,32,65,88,44,50,13,10,82,95,72,65,78
DB 68,76,69,75,73,78,68,58,13,10,68,69,67,32,66,88
DB 13,10,82,69,84,13,10,82,95,66,65,68,72,65,78,68
DB 76,69,58,13,10,77,79,86,32,65,88,44,48,13,10,82
DB 69,84,13,10,13,10,0

T_RTREAD:
DB 82,95,82,69,65,68,58,13,10,77,79,86,32,91,82,95
DB 67,79,85,78,84,93,44,65,88,13,10,77,79,86,32,91
DB 82,95,66,85,70,70,69,82,93,44,68,88,13,10,67,65
DB 76,76,32,82,95,70,73,78,68,13,10,67,77,80,32,65
DB 88,44,49,13,10,74,69,32,82,95,82,69,65,68,86,65
DB 76,73,68,13,10,74,77,80,32,82,95,70,65,73,76,13
DB 10,82,95,82,69,65,68,86,65,76,73,68,58,13,10,77
DB 79,86,32,67,88,44,91,82,95,67,79,85,78,84,93,13
DB 10,67,77,80,32,67,88,44,48,13,10,74,78,69,32,82
DB 95,82,69,65,68,77,79,82,69,13,10,77,79,86,32,65
DB 88,44,48,13,10,74,77,80,32,82,95,79,75,13,10,82
DB 95,82,69,65,68,77,79,82,69,58,13,10,77,79,86,32
DB 68,88,44,91,82,95,66,85,70,70,69,82,93,13,10,77
DB 79,86,32,65,72,44,51,70,72,13,10,73,78,84,32,50
DB 49,72,13,10,74,65,69,32,82,95,82,69,65,68,71,79
DB 79,68,13,10,74,77,80,32,82,95,70,65,73,76,13,10
DB 82,95,82,69,65,68,71,79,79,68,58,13,10,74,77,80
DB 32,82,95,79,75,13,10,13,10,0

```

### Change 4: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_OPEN
DB 67,82,69,65,84,69,0,0,0,3,3,0
DW T_CREATE
```

Insert after old physical line 1007, before the following old line.

Insert this source:

```asm
DB 82,69,65,68,0,0,0,0,0,6,5,0
DW T_READ
```

### Change 5: following `FLOWDONE:`

Unchanged code immediately before the edit:

```asm
JE BALANCED
FLOWDONE:
RET
```

Insert after old physical line 836, before the following old line.

Insert this source:

```asm
STACKTWO:
MOV AX,[DEPTH]
CMP AX,2
JB STACKBAD
SUB AX,2
MOV [DEPTH],AX
JMP BALANCED
```

### Change 6: following `FLOW:`

Unchanged code immediately before the edit:

```asm

FLOW:
MOV AL,[EFFECT]
```

Insert after old physical line 808, before the following old line.

Insert this source:

```asm
CMP AL,6
JE STACKTWO
```

### Change 7: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 507–507 in `IR29.ASM`):

```asm
MOV CX,44
```

Put this source in their place:

```asm
MOV CX,45
```

### Change 8: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
MOV SI,T_RTBYTE
CALL OUTTEXT
MOV SI,T_RTFILEDATA
```

Insert after old physical line 52, before the following old line.

Insert this source:

```asm
CALL OUTTEXT
MOV SI,T_RTTRANSFERDATA
```

### Change 9: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
CALL OUTTEXT
MOV SI,T_RTFILE
CALL OUTTEXT
```

Insert after old physical line 47, before the following old line.

Insert this source:

```asm
MOV SI,T_RTFIND
CALL OUTTEXT
MOV SI,T_RTREAD
CALL OUTTEXT
```

### Change 10: following `ROOM:`

Unchanged code immediately before the edit:

```asm
MOV [OUTPTR],AX
MOV AX,256
MOV [TARGETSIZE],AX
```

Remove these exact old lines (physical positions 14–14 in `IR29.ASM`):

```asm
MOV AX,26
```

Put this source in their place:

```asm
MOV AX,35
```

### Change 11: following `ROOM:`

Unchanged code immediately before the edit:

```asm
CALL GETNAME
MOV AX,6000H
MOV [OUTPTR],AX
```

Remove these exact old lines (physical positions 12–12 in `IR29.ASM`):

```asm
MOV AX,256
```

Put this source in their place:

```asm
MOV AX,365
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR30` at ASM0's `Source name:` prompt. Require `OK 05752 bytes` followed by PASS. This builds `IR30.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T30.IR` with `COPY CON T30.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
BYTE F0 73
BYTE F1 78
BYTE F2 46
BYTE F3 84
BYTE F4 88
BYTE F5 84
BYTE F6 0
WORD HANDLE 0
WORD COUNT 0
BUFFER DATA 1
LABEL MAIN
ADDR F0
OPEN
ST HANDLE
STATUS
JNZ FAILURE
LD HANDLE
PUSH
ADDR DATA
PUSH
LIT 1
READ
ST COUNT
STATUS
JNZ FAILURE
LD COUNT
PUSH
LIT 1
NE FAILURE
ADDR DATA
FETCHB
PUTC
STATUS
EXIT
LABEL FAILURE
LIT 1
EXIT
```

```dos
CHECK IR30
```

Enter `T30` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T30
OK T30.ASM 02613 text bytes
PASS
```

Run `TYPE T30.ASM`. The program prefix must be as follows; the backend runtime follows it.

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_F0:
DB 73
U_F1:
DB 78
U_F2:
DB 46
U_F3:
DB 84
U_F4:
DB 88
U_F5:
DB 84
U_F6:
DB 0
U_HANDLE:
DW 0
U_COUNT:
DW 0
U_DATA:
DB 0
U_MAIN:
MOV AX,U_F0
CALL R_OPEN
MOV [U_HANDLE],AX
MOV AX,[R_STATUS]
CMP AX,0
JE I0001
JMP U_FAILURE
I0001:
MOV AX,[U_HANDLE]
PUSH AX
MOV AX,U_DATA
PUSH AX
MOV AX,1
POP DX
POP BX
CALL R_READ
MOV [U_COUNT],AX
MOV AX,[R_STATUS]
CMP AX,0
JE I0002
JMP U_FAILURE
I0002:
MOV AX,[U_COUNT]
PUSH AX
MOV AX,1
POP BX
CMP BX,AX
JE I0003
JMP U_FAILURE
I0003:
MOV AX,U_DATA
MOV BX,AX
MOV AL,[BX]
MOV AH,0
CALL R_PUTC
MOV AX,[R_STATUS]
MOV AH,4CH
INT 21H
U_FAILURE:
MOV AX,1
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T30`. Require `OK 00477 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T30.COM`, and require length **477 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

This checkpoint includes the runtime fragments introduced so far. The reference lists the complete final binding. Compare the leading bytes below; the viewer must still report the full file length.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 0C 00 49
4E 2E 54 58 54 00 00 00 00 00 00 B8 0F 01 E8 C0
00 89 06 16 01 8B 06 BE 02 81 F8 00 00 74 03 E9
46 00 8B 06 16 01 50 B8 1A 01 50 B8 01 00 5A 5B
```

`T30.COM` is a complete program. Prepare `IN.TXT` with `ECHO Q>IN.TXT`. Run `CHECK T30`. It displays `Q` and then the checker reports PASS.

## A rejection check

Enter this separate input as `X30.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
LIT 1
READ
```

Run `CHECK IR30` and enter `X30`. Require this diagnostic and FAIL:

```text
IR ERROR 00003 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.
