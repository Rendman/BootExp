+++
title = "28 \u00b7 Opening an opaque file handle"
weight = 28
description = "A file result is independent of an operating-system descriptor."
download = "IR28.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

OPEN gives a program a readable file without exposing the representation used by its environment.

## Operation and backend

OPEN takes a pointer to a zero-terminated ASCII file name. It returns an opaque nonzero handle on success, or zero on failure, and sets STATUS. Save the handle in word storage and pass it to file services; do not derive an operating-system descriptor or perform arithmetic on it.

The DOS binding keeps eight slots. R_FREE finds an unused slot before requesting an open. R_FILE stores the private descriptor and returns a token for the slot. The stored descriptor is encoded one above its real value, leaving zero as the free marker even when a real descriptor happens to be zero.

Supported file-name forms and open-file capacity belong to the environment binding. The test uses IN.TXT, observes STATUS, and checks for a nonzero token. Remaining handles are released when the program terminates.

## Source changes

Copy `IR27.ASM` to `IR28.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_GETC:`

Unchanged code immediately before the edit:

```asm

T_GETC:
DB 67,65,76,76,32,82,95,71,69,84,67,13,10,0
```

Insert after old physical line 1326, before the following old line.

Insert this source:

```asm

T_OPEN:
DB 67,65,76,76,32,82,95,79,80,69,78,13,10,0
```

### Change 2: following `T_RTBYTE:`

Unchanged code immediately before the edit:

```asm
DB 10,74,77,80,32,82,95,79,75,13,10,13,10,0

T_RTBYTE:
```

Remove these exact old lines (physical positions 1156–1156 in `IR27.ASM`):

```asm
DB 82,95,66,89,84,69,58,13,10,68,66,32,48,13,10,0
```

Put this source in their place:

```asm
DB 82,95,66,89,84,69,58,13,10,68,66,32,48,13,10,13
DB 10,0

T_RTFILEDATA:
DB 82,95,77,79,68,69,58,13,10,68,87,32,48,13,10,82
DB 95,78,65,77,69,58,13,10,68,87,32,48,13,10,82,95
DB 83,76,79,84,58,13,10,68,87,32,48,13,10,82,95,78
DB 85,77,66,69,82,58,13,10,68,87,32,48,13,10,82,95
DB 72,65,78,68,76,69,83,58,13,10,68,87,32,48,44,48
DB 44,48,44,48,44,48,44,48,44,48,44,48,13,10,0
```

### Change 3: following `T_RTGETC:`

Unchanged code immediately before the edit:

```asm
DB 66,89,84,69,93,13,10,77,79,86,32,65,72,44,48,13
DB 10,74,77,80,32,82,95,79,75,13,10,13,10,0

```

Insert after old physical line 1154, before the following old line.

Insert this source:

```asm
T_RTOPEN:
DB 82,95,79,80,69,78,58,13,10,77,79,86,32,68,88,44
DB 51,68,48,48,72,13,10,74,77,80,32,82,95,70,73,76
DB 69,13,10,13,10,0

T_RTFILE:
DB 82,95,70,73,76,69,58,13,10,77,79,86,32,91,82,95
DB 77,79,68,69,93,44,68,88,13,10,77,79,86,32,91,82
DB 95,78,65,77,69,93,44,65,88,13,10,67,65,76,76,32
DB 82,95,70,82,69,69,13,10,67,77,80,32,66,88,44,48
DB 13,10,74,78,69,32,82,95,72,65,86,69,83,76,79,84
DB 13,10,74,77,80,32,82,95,70,65,73,76,13,10,82,95
DB 72,65,86,69,83,76,79,84,58,13,10,77,79,86,32,68
DB 88,44,91,82,95,78,65,77,69,93,13,10,77,79,86,32
DB 67,88,44,48,13,10,77,79,86,32,65,88,44,91,82,95
DB 77,79,68,69,93,13,10,73,78,84,32,50,49,72,13,10
DB 74,65,69,32,82,95,70,73,76,69,71,79,79,68,13,10
DB 74,77,80,32,82,95,70,65,73,76,13,10,82,95,70,73
DB 76,69,71,79,79,68,58,13,10,73,78,67,32,65,88,13
DB 10,77,79,86,32,68,88,44,91,82,95,77,79,68,69,93
DB 13,10,67,77,80,32,68,88,44,51,67,48,48,72,13,10
DB 74,78,69,32,82,95,82,69,65,68,83,76,79,84,13,10
DB 65,68,68,32,65,88,44,56,48,48,48,72,13,10,82,95
DB 82,69,65,68,83,76,79,84,58,13,10,77,79,86,32,66
DB 88,44,91,82,95,83,76,79,84,93,13,10,77,79,86,32
DB 91,66,88,93,44,65,88,13,10,77,79,86,32,65,88,44
DB 91,82,95,78,85,77,66,69,82,93,13,10,74,77,80,32
DB 82,95,79,75,13,10,82,95,70,82,69,69,58,13,10,77
DB 79,86,32,66,88,44,82,95,72,65,78,68,76,69,83,13
DB 10,77,79,86,32,67,88,44,49,13,10,82,95,78,69,88
DB 84,83,76,79,84,58,13,10,77,79,86,32,65,88,44,91
DB 66,88,93,13,10,67,77,80,32,65,88,44,48,13,10,74
DB 69,32,82,95,83,76,79,84,70,79,85,78,68,13,10,65
DB 68,68,32,66,88,44,50,13,10,73,78,67,32,67,88,13
DB 10,67,77,80,32,67,88,44,57,13,10,74,66,32,82,95
DB 78,69,88,84,83,76,79,84,13,10,77,79,86,32,66,88
DB 44,48,13,10,82,69,84,13,10,82,95,83,76,79,84,70
DB 79,85,78,68,58,13,10,77,79,86,32,91,82,95,83,76
DB 79,84,93,44,66,88,13,10,77,79,86,32,91,82,95,78
DB 85,77,66,69,82,93,44,67,88,13,10,82,69,84,13,10
DB 13,10,0

```

### Change 4: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_PUTC
DB 71,69,84,67,0,0,0,0,0,3,3,0
DW T_GETC
```

Insert after old physical line 995, before the following old line.

Insert this source:

```asm
DB 79,80,69,78,0,0,0,0,0,3,3,0
DW T_OPEN
```

### Change 5: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 499–499 in `IR27.ASM`):

```asm
MOV CX,42
```

Put this source in their place:

```asm
MOV CX,43
```

### Change 6: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
MOV SI,T_RTSTATUS
CALL OUTTEXT
MOV SI,T_RTBYTE
```

Insert after old physical line 44, before the following old line.

Insert this source:

```asm
CALL OUTTEXT
MOV SI,T_RTFILEDATA
```

### Change 7: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
CALL OUTTEXT
MOV SI,T_RTGETC
CALL OUTTEXT
```

Insert after old physical line 41, before the following old line.

Insert this source:

```asm
MOV SI,T_RTOPEN
CALL OUTTEXT
MOV SI,T_RTFILE
CALL OUTTEXT
```

### Change 8: following `ROOM:`

Unchanged code immediately before the edit:

```asm
MOV [OUTPTR],AX
MOV AX,116
MOV [TARGETSIZE],AX
```

Remove these exact old lines (physical positions 14–14 in `IR27.ASM`):

```asm
MOV AX,12
```

Put this source in their place:

```asm
MOV AX,25
```

### Change 9: following `ROOM:`

Unchanged code immediately before the edit:

```asm
CALL GETNAME
MOV AX,6000H
MOV [OUTPTR],AX
```

Remove these exact old lines (physical positions 12–12 in `IR27.ASM`):

```asm
MOV AX,116
```

Put this source in their place:

```asm
MOV AX,250
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR28` at ASM0's `Source name:` prompt. Require `OK 04991 bytes` followed by PASS. This builds `IR28.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T28.IR` with `COPY CON T28.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

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
JZ FAILURE
HALT
LABEL FAILURE
LIT 1
EXIT
```

```dos
CHECK IR28
```

Enter `T28` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T28
OK T28.ASM 01673 text bytes
PASS
```

Run `TYPE T28.ASM`. The program prefix must be as follows; the backend runtime follows it.

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
CMP AX,0
JNE I0002
JMP U_FAILURE
I0002:
MOV AX,4C00H
INT 21H
U_FAILURE:
MOV AX,1
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T28`. Require `OK 00307 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T28.COM`, and require length **307 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

This checkpoint includes the runtime fragments introduced so far. The reference lists the complete final binding. Compare the leading bytes below; the viewer must still report the full file length.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 09 00 49
4E 2E 54 58 54 00 00 00 B8 0F 01 E8 8C 00 89 06
16 01 8B 06 18 02 81 F8 00 00 74 03 E9 12 00 8B
06 16 01 81 F8 00 00 75 03 E9 05 00 B8 00 4C CD
```

`T28.COM` is a complete program. Prepare `IN.TXT` with `ECHO Q>IN.TXT`. Run `CHECK T28`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X28.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
LIT 1
PUSH
OPEN
```

Run `CHECK IR28` and enter `X28`. Require this diagnostic and FAIL:

```text
IR ERROR 00004 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.
