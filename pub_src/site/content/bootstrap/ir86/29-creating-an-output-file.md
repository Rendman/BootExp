+++
title = "29 \u00b7 Creating an output file"
weight = 29
description = "Request writable storage and keep its descriptor private."
download = "IR29.ASM"
+++

CREATE prepares a writable output file through the same opaque handle interface.

## Operation and backend

CREATE takes a zero-terminated file name and returns a handle or zero, with STATUS distinguishing success and failure. Successful creation replaces the contents with an empty byte sequence. A zero result is not a valid handle.

The DOS binding shares R_FILE with OPEN and selects its create service internally. Its slot records write permission as well as an encoded descriptor. The IR program sees only the token. Finding a slot first prevents an exhausted table from needlessly truncating a file.

The test creates OUT.TXT and checks its status. Its empty output is a visible result: inspect the file length. No data is written by this program.

## Source changes

Copy `IR28.ASM` to `IR29.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_OPEN:`

Unchanged code immediately before the edit:

```asm

T_OPEN:
DB 67,65,76,76,32,82,95,79,80,69,78,13,10,0
```

Insert after old physical line 1388, before the following old line.

Insert this source:

```asm

T_CREATE:
DB 67,65,76,76,32,82,95,67,82,69,65,84,69,13,10,0
```

### Change 2: following `T_RTOPEN:`

Unchanged code immediately before the edit:

```asm
DB 82,95,79,80,69,78,58,13,10,77,79,86,32,68,88,44
DB 51,68,48,48,72,13,10,74,77,80,32,82,95,70,73,76
DB 69,13,10,13,10,0
```

Insert after old physical line 1166, before the following old line.

Insert this source:

```asm

T_RTCREATE:
DB 82,95,67,82,69,65,84,69,58,13,10,77,79,86,32,68
DB 88,44,51,67,48,48,72,13,10,74,77,80,32,82,95,70
DB 73,76,69,13,10,13,10,0
```

### Change 3: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_GETC
DB 79,80,69,78,0,0,0,0,0,3,3,0
DW T_OPEN
```

Insert after old physical line 1003, before the following old line.

Insert this source:

```asm
DB 67,82,69,65,84,69,0,0,0,3,3,0
DW T_CREATE
```

### Change 4: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 505–505 in `IR28.ASM`):

```asm
MOV CX,43
```

Put this source in their place:

```asm
MOV CX,44
```

### Change 5: following `MAINPRESENT:`

Unchanged code immediately before the edit:

```asm
MOV SI,T_RTGETC
CALL OUTTEXT
MOV SI,T_RTOPEN
```

Insert after old physical line 42, before the following old line.

Insert this source:

```asm
CALL OUTTEXT
MOV SI,T_RTCREATE
```

### Change 6: following `ROOM:`

Unchanged code immediately before the edit:

```asm
MOV [OUTPTR],AX
MOV AX,250
MOV [TARGETSIZE],AX
```

Remove these exact old lines (physical positions 14–14 in `IR28.ASM`):

```asm
MOV AX,25
```

Put this source in their place:

```asm
MOV AX,26
```

### Change 7: following `ROOM:`

Unchanged code immediately before the edit:

```asm
CALL GETNAME
MOV AX,6000H
MOV [OUTPTR],AX
```

Remove these exact old lines (physical positions 12–12 in `IR28.ASM`):

```asm
MOV AX,250
```

Put this source in their place:

```asm
MOV AX,256
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR29` at ASM86's `Source name:` prompt. Require `OK 05067 bytes` followed by PASS. This builds `IR29.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T29.IR` with `COPY CON T29.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
BYTE F0 79
BYTE F1 85
BYTE F2 84
BYTE F3 46
BYTE F4 84
BYTE F5 88
BYTE F6 84
BYTE F7 0
LABEL MAIN
ADDR F0
CREATE
STATUS
EXIT
```

```dos
CHECK IR29
```

Enter `T29` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T29
OK T29.ASM 01541 text bytes
PASS
```

Run `TYPE T29.ASM`. The program prefix must be as follows; the backend runtime follows it.

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
U_MAIN:
MOV AX,U_F0
CALL R_CREATE
MOV AX,[R_STATUS]
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T29`. Require `OK 00278 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T29.COM`, and require length **278 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

This checkpoint includes the runtime fragments introduced so far. The reference lists the complete final binding. Compare the leading bytes below; the viewer must still report the full file length.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 08 00 4F
55 54 2E 54 58 54 00 B8 0F 01 E8 70 00 8B 06 FB
01 B4 4C CD 21 BA 00 00 89 16 FB 01 C3 BA 01 00
89 16 FB 01 C3 B8 00 00 E9 F2 FF 88 06 FD 01 BB
```

`T29.COM` is a complete program. Prepare `OUT.TXT` with `ECHO old contents>OUT.TXT`. Run `CHECK T29`. It returns zero and the checker reports PASS.

Inspect `OUT.TXT` with VIEW.BAS. Require length 0.

## A rejection check

Enter this separate input as `X29.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
CREATE EXTRA
```

Run `CHECK IR29` and enter `X29`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 1
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. Read runtime STATUS as an ordinary word; comparisons and arithmetic must not change it.
