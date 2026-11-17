+++
title = "08 \u00b7 Reading a File in Blocks"
weight = 8
description = "Refill a small block instead of making a DOS call for every byte."
download = "A02.ASM"
cartoon = "asm86a-press.png"
aliases = ["/bootstrap/asm86a/02-reading-an-input-block/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/02-reading-an-input-block/"
+++

I follow the source reader in my notebook: it asks DOS for one byte, then asks again for the next. I want to collect a small block at once and let the reader hand those bytes to the parser one at a time. The parser should still receive the same characters in the same order.

## The working parts

NEXTBYTE retains its interface: AX is one with CHAR set, or zero at EOF. RDPOS and RDLEN describe bytes already returned by DOS. A refill requests 1024 bytes at 5000H. Any positive returned count is consumed completely before another refill; a short positive read is not EOF.

The driver clears both fields at the start of each pass. NEXTBYTE changes AX, BX, CX, DX, flags, CHAR, and the two cursors, while preserving SI, DI, and BP. The line and token readers therefore need no new calling convention.

## Enter the source

Copy `A01.ASM` to `A02.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `INOPEN:`

Find the unique label `INOPEN:`. Insert the new source immediately before this existing label:

```asm
INOPEN:
```

Insert:

```asm
RDPOS:
DW 0
RDLEN:
DW 0
```

### Change 2 · `NEXTBYTE:`

Find the unique label `NEXTBYTE:`, then follow this unchanged source through its last displayed instruction:

```asm
NEXTBYTE:
MOV BX,[HANDLE]
MOV CX,1
MOV DX,CHAR
MOV AH,3FH
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE BYTEOK
MOV AX,6
JMP ERROR
BYTEOK:
```

With:

```asm
JAE REFILLED
JMP FILEBAD
REFILLED:
MOV [RDLEN],AX
MOV DX,0
MOV [RDPOS],DX
CMP AX,0
JE BUFFEREND
BUFFERBYTE:
MOV BX,[RDPOS]
ADD BX,5000H
MOV AL,[BX]
MOV [CHAR],AL
MOV AX,[RDPOS]
INC AX
MOV [RDPOS],AX
MOV AX,1
RET
BUFFEREND:
MOV AX,0
```

### Change 3 · `NEXTBYTE:`

Find the unique label `NEXTBYTE:`, then follow this unchanged source through its last displayed instruction:

```asm
NEXTBYTE:
MOV BX,[HANDLE]
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV CX,1
MOV DX,CHAR
```

With:

```asm
MOV DX,5000H
MOV CX,1024
```

### Change 4 · `NEXTBYTE:`

Find the unique label `NEXTBYTE:`, then follow this unchanged source through its last displayed instruction:

```asm
NEXTBYTE:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AX,[RDPOS]
MOV DX,[RDLEN]
CMP AX,DX
JB BUFFERBYTE
```

### Change 5 · `PASSSTART:`

Find the unique label `PASSSTART:`, then follow this unchanged source through its last displayed instruction:

```asm
PASSSTART:
MOV AX,100H
MOV [PC],AX
MOV AX,6000H
MOV [OUTPTR],AX
MOV AX,0
MOV [LINENO],AX
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV [RDPOS],AX
MOV [RDLEN],AX
```

## Build the stopping point

Copy `A02.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03007 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A02.COM`.

VIEW.BAS must report A02.COM length 3007 bytes. Keep that executable and source together.

## Acceptance check

Create T02.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
CHECK A02 T02.ASM RESULT.COM
```

Require:

```text
OK RESULT.COM 00011 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **11 bytes** and these complete contents:

```text
B2 41 B4 02 CD 21 B8 00 4C CD 21
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X02.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
CHECK A02 X02.ASM RESULT.COM
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with C:\DOS\FC.EXE /B if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check the saved argument names and terminators, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
