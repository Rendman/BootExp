+++
title = "31 \u00b7 Writing bytes with an explicit count"
weight = 31
description = "Report partial progress separately from success or failure."
download = "IR31.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

WRITE sends bytes to a writable file using the same virtual argument order as READ.

## Operation and backend

Save the writable handle, then the buffer pointer, and supply the count in A. WRITE consumes both saved words and requires an otherwise empty expression stack. It returns the actual byte count. STATUS is zero for a complete write and one for an error or short write; partial progress is retained.

The DOS binding requires a CREATE handle and normalizes both a carry error and a smaller returned count. A zero-length request performs no write and leaves the file unchanged. R_ERROR changes the status while retaining a partial result.

The test writes Q to OUT.TXT. It compares the returned count before reading STATUS, demonstrating that arithmetic and comparison flags cannot destroy the service status.

## Source changes

Copy `IR30.ASM` to `IR31.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_READ:`

Unchanged code immediately before the edit:

```asm
T_READ:
DB 80,79,80,32,68,88,13,10,80,79,80,32,66,88,13,10
DB 67,65,76,76,32,82,95,82,69,65,68,13,10,0
```

Insert after old physical line 1467, before the following old line.

Insert this source:

```asm

T_WRITE:
DB 80,79,80,32,68,88,13,10,80,79,80,32,66,88,13,10
DB 67,65,76,76,32,82,95,87,82,73,84,69,13,10,0
```

### Change 2: following `T_RTREAD:`

Unchanged code immediately before the edit:

```asm
DB 82,95,82,69,65,68,71,79,79,68,58,13,10,74,77,80
DB 32,82,95,79,75,13,10,13,10,0

```

Insert after old physical line 1270, before the following old line.

Insert this source:

```asm
T_RTWRITE:
DB 82,95,87,82,73,84,69,58,13,10,77,79,86,32,91,82
DB 95,67,79,85,78,84,93,44,65,88,13,10,77,79,86,32
DB 91,82,95,66,85,70,70,69,82,93,44,68,88,13,10,67
DB 65,76,76,32,82,95,70,73,78,68,13,10,67,77,80,32
DB 65,88,44,50,13,10,74,69,32,82,95,87,82,73,84,69
DB 86,65,76,73,68,13,10,74,77,80,32,82,95,70,65,73
DB 76,13,10,82,95,87,82,73,84,69,86,65,76,73,68,58
DB 13,10,77,79,86,32,67,88,44,91,82,95,67,79,85,78
DB 84,93,13,10,67,77,80,32,67,88,44,48,13,10,74,78
DB 69,32,82,95,87,82,73,84,69,77,79,82,69,13,10,77
DB 79,86,32,65,88,44,48,13,10,74,77,80,32,82,95,79
DB 75,13,10,82,95,87,82,73,84,69,77,79,82,69,58,13
DB 10,77,79,86,32,68,88,44,91,82,95,66,85,70,70,69
DB 82,93,13,10,77,79,86,32,65,72,44,52,48,72,13,10
DB 73,78,84,32,50,49,72,13,10,74,65,69,32,82,95,87
DB 82,73,84,69,67,79,85,78,84,13,10,74,77,80,32,82
DB 95,70,65,73,76,13,10,82,95,87,82,73,84,69,67,79
DB 85,78,84,58,13,10,77,79,86,32,68,88,44,91,82,95
DB 67,79,85,78,84,93,13,10,67,77,80,32,65,88,44,68
DB 88,13,10,74,69,32,82,95,87,82,73,84,69,71,79,79
DB 68,13,10,74,77,80,32,82,95,69,82,82,79,82,13,10
DB 82,95,87,82,73,84,69,71,79,79,68,58,13,10,74,77
DB 80,32,82,95,79,75,13,10,13,10,0

```

### Change 3: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_CREATE
DB 82,69,65,68,0,0,0,0,0,6,5,0
DW T_READ
```

Insert after old physical line 1024, before the following old line.

Insert this source:

```asm
DB 87,82,73,84,69,0,0,0,0,6,5,0
DW T_WRITE
```

### Change 4: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 513–513 in `IR30.ASM`):

```asm
MOV CX,45
```

Put this source in their place:

```asm
MOV CX,46
```

### Change 5: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
MOV SI,T_RTFIND
CALL OUTTEXT
MOV SI,T_RTREAD
```

Insert after old physical line 50, before the following old line.

Insert this source:

```asm
CALL OUTTEXT
MOV SI,T_RTWRITE
```

### Change 6: following `ROOM:`

Unchanged code immediately before the edit:

```asm
MOV [OUTPTR],AX
MOV AX,365
MOV [TARGETSIZE],AX
```

Remove these exact old lines (physical positions 14–14 in `IR30.ASM`):

```asm
MOV AX,35
```

Put this source in their place:

```asm
MOV AX,40
```

### Change 7: following `ROOM:`

Unchanged code immediately before the edit:

```asm
CALL GETNAME
MOV AX,6000H
MOV [OUTPTR],AX
```

Remove these exact old lines (physical positions 12–12 in `IR30.ASM`):

```asm
MOV AX,365
```

Put this source in their place:

```asm
MOV AX,428
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR31` at ASM0's `Source name:` prompt. Require `OK 06166 bytes` followed by PASS. This builds `IR31.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T31.IR` with `COPY CON T31.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
BYTE F0 79
BYTE F1 85
BYTE F2 84
BYTE F3 46
BYTE F4 84
BYTE F5 88
BYTE F6 84
BYTE F7 0
BYTE DATA 81
WORD HANDLE 0
LABEL MAIN
ADDR F0
CREATE
ST HANDLE
STATUS
JNZ FAILURE
LD HANDLE
PUSH
ADDR DATA
PUSH
LIT 1
WRITE
PUSH
LIT 1
NE FAILURE
STATUS
EXIT
LABEL FAILURE
LIT 1
EXIT
```

```dos
CHECK IR31
```

Enter `T31` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T31
OK T31.ASM 02817 text bytes
PASS
```

Run `TYPE T31.ASM`. The program prefix must be as follows; the backend runtime follows it.

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_F0:
DB 79
U_F1:
DB 85
U_F2:
DB 84
U_F3:
DB 46
U_F4:
DB 84
U_F5:
DB 88
U_F6:
DB 84
U_F7:
DB 0
U_DATA:
DB 81
U_HANDLE:
DW 0
U_MAIN:
MOV AX,U_F0
CALL R_CREATE
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
CALL R_WRITE
PUSH AX
MOV AX,1
POP BX
CMP BX,AX
JE I0002
JMP U_FAILURE
I0002:
MOV AX,[R_STATUS]
MOV AH,4CH
INT 21H
U_FAILURE:
MOV AX,1
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T31`. Require `OK 00506 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T31.COM`, and require length **506 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

This checkpoint includes the runtime fragments introduced so far. The reference lists the complete final binding. Compare the leading bytes below; the viewer must still report the full file length.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 0B 00 4F
55 54 2E 54 58 54 00 51 00 00 B8 0F 01 E8 A5 00
89 06 18 01 8B 06 DB 02 81 F8 00 00 74 03 E9 25
00 8B 06 18 01 50 B8 17 01 50 B8 01 00 5A 5B E8
```

`T31.COM` is a complete program. Prepare `OUT.TXT` with `ECHO old contents>OUT.TXT`. Run `CHECK T31`. It returns zero and the checker reports PASS.

Inspect `OUT.TXT` with VIEW.BAS. Require length 1 and byte 51.

## A rejection check

Enter this separate input as `X31.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
LIT 1
PUSH
WRITE
```

Run `CHECK IR31` and enter `X31`. Require this diagnostic and FAIL:

```text
IR ERROR 00004 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.
