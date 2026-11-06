+++
title = "32 \u00b7 Closing a portable handle"
weight = 32
description = "Release a resource and observe its normalized result."
download = "IR32.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

CLOSE releases a file explicitly so a program can check completion and reuse its bounded handle capacity.

## Operation and backend

CLOSE takes an opaque handle and returns zero. STATUS distinguishes success and failure. After successful close the token is invalid; a binding may reuse its value for a newly opened file, so a saved closed token must not be reused.

The DOS binding locates the slot, closes its private descriptor, and clears the slot only after success. An invalid or closed token produces STATUS one, without exposing a DOS error number. The same source operation closes a readable or writable file.

The test opens IN.TXT, checks the status, closes its saved token, and returns the close status. This completes the portable service interface independently of the calls chosen by this backend.

## Source changes

Copy `IR31.ASM` to `IR32.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_WRITE:`

Unchanged code immediately before the edit:

```asm
T_WRITE:
DB 80,79,80,32,68,88,13,10,80,79,80,32,66,88,13,10
DB 67,65,76,76,32,82,95,87,82,73,84,69,13,10,0
```

Insert after old physical line 1500, before the following old line.

Insert this source:

```asm

T_CLOSE:
DB 67,65,76,76,32,82,95,67,76,79,83,69,13,10,0
```

### Change 2: following `T_RTWRITE:`

Unchanged code immediately before the edit:

```asm
DB 82,95,87,82,73,84,69,71,79,79,68,58,13,10,74,77
DB 80,32,82,95,79,75,13,10,13,10,0

```

Insert after old physical line 1299, before the following old line.

Insert this source:

```asm
T_RTCLOSE:
DB 82,95,67,76,79,83,69,58,13,10,77,79,86,32,66,88
DB 44,65,88,13,10,67,65,76,76,32,82,95,70,73,78,68
DB 13,10,67,77,80,32,65,88,44,48,13,10,74,78,69,32
DB 82,95,67,76,79,83,69,86,65,76,73,68,13,10,74,77
DB 80,32,82,95,70,65,73,76,13,10,82,95,67,76,79,83
DB 69,86,65,76,73,68,58,13,10,77,79,86,32,65,72,44
DB 51,69,72,13,10,73,78,84,32,50,49,72,13,10,74,65
DB 69,32,82,95,67,76,79,83,69,71,79,79,68,13,10,74
DB 77,80,32,82,95,70,65,73,76,13,10,82,95,67,76,79
DB 83,69,71,79,79,68,58,13,10,77,79,86,32,66,88,44
DB 91,82,95,83,76,79,84,93,13,10,77,79,86,32,65,88
DB 44,48,13,10,77,79,86,32,91,66,88,93,44,65,88,13
DB 10,74,77,80,32,82,95,79,75,13,10,13,10,0

```

### Change 3: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_READ
DB 87,82,73,84,69,0,0,0,0,6,5,0
DW T_WRITE
```

Insert after old physical line 1028, before the following old line.

Insert this source:

```asm
DB 67,76,79,83,69,0,0,0,0,3,3,0
DW T_CLOSE
```

### Change 4: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 515–515 in `IR31.ASM`):

```asm
MOV CX,46
```

Put this source in their place:

```asm
MOV CX,47
```

### Change 5: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
MOV SI,T_RTREAD
CALL OUTTEXT
MOV SI,T_RTWRITE
```

Insert after old physical line 52, before the following old line.

Insert this source:

```asm
CALL OUTTEXT
MOV SI,T_RTCLOSE
```

### Change 6: following `ROOM:`

Unchanged code immediately before the edit:

```asm
MOV [OUTPTR],AX
MOV AX,428
MOV [TARGETSIZE],AX
```

Remove these exact old lines (physical positions 14–14 in `IR31.ASM`):

```asm
MOV AX,40
```

Put this source in their place:

```asm
MOV AX,43
```

### Change 7: following `ROOM:`

Unchanged code immediately before the edit:

```asm
CALL GETNAME
MOV AX,6000H
MOV [OUTPTR],AX
```

Remove these exact old lines (physical positions 12–12 in `IR31.ASM`):

```asm
MOV AX,428
```

Put this source in their place:

```asm
MOV AX,463
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR32` at ASM0's `Source name:` prompt. Require `OK 06407 bytes` followed by PASS. This builds `IR32.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T32.IR` with `COPY CON T32.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
BYTE F0 73
BYTE F1 78
BYTE F2 46
BYTE F3 84
BYTE F4 88
BYTE F5 84
BYTE F6 0
WORD HANDLE 0
LABEL MAIN
ADDR F0
OPEN
ST HANDLE
STATUS
JNZ FAILURE
LD HANDLE
CLOSE
STATUS
EXIT
LABEL FAILURE
LIT 1
EXIT
```

```dos
CHECK IR32
```

Enter `T32` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T32
OK T32.ASM 02860 text bytes
PASS
```

Run `TYPE T32.ASM`. The program prefix must be as follows; the backend runtime follows it.

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
CALL R_CLOSE
MOV AX,[R_STATUS]
MOV AH,4CH
INT 21H
U_FAILURE:
MOV AX,1
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T32`. Require `OK 00517 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T32.COM`, and require length **517 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

This checkpoint includes the runtime fragments introduced so far. The reference lists the complete final binding. Compare the leading bytes below; the viewer must still report the full file length.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 09 00 49
4E 2E 54 58 54 00 00 00 B8 0F 01 E8 89 00 89 06
16 01 8B 06 E6 02 81 F8 00 00 74 03 E9 0F 00 8B
06 16 01 E8 8D 01 8B 06 E6 02 B4 4C CD 21 B8 01
```

`T32.COM` is a complete program. Prepare `IN.TXT` with `ECHO Q>IN.TXT`. Run `CHECK T32`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X32.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
CLOSE EXTRA
```

Run `CHECK IR32` and enter `X32`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 1
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.
