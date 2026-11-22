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

**Starting source:** `A01.ASM`. **Save as:** `A02.ASM`. **Build with:** `ASMKEEP.COM`.

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

Keep that executable and source together.

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

The byte inspection checks the accepted result. Keep it as data.

## Cross the input-block boundaries

Enter STREAM.BAS. It writes assembly source text; the assembler still makes every executable byte.

```basic
10 N=1024
20 OPEN "LONG.ASM" FOR OUTPUT AS #1
30 FOR I=1 TO N
40 PRINT #1,"DB 65"
50 NEXT I
60 PRINT #1,"DB 66"
70 CLOSE #1
80 PRINT "LONG.ASM READY"
```

```dos
GWBASIC STREAM.BAS
```

Require LONG.ASM READY, then use SYSTEM to return to DOS. The source contains repeated DB statements and a final different value. Its text occupies 7,176 bytes, including BASIC's closing Control-Z. Tokens and CR/LF pairs cross the 1,024-byte input boundaries. Each pass must read through them without losing or repeating a character.

```dos
CHECK A02 LONG.ASM RESULT.COM
```

Require `OK RESULT.COM 01025 bytes` and PASS. VIEW.BAS must show length 1025: the first 1024 bytes are `41` and the final byte is `42`. The final display row contains that one `42`. Inspect this result as data.

Keep the accepted result before trying an error near the end of the same long input:

```dos
COPY RESULT.COM HOLD.COM
GWBASIC STREAM.BAS
```

At the BASIC prompt replace line 60 with the following line, then RUN and SYSTEM:

```basic
60 PRINT #1,"DB 256"
```

```dos
CHECK A02 LONG.ASM RESULT.COM
C:\DOS\FC.EXE /B HOLD.COM RESULT.COM
```

Require `ERROR 01025 CODE 4` and FAIL, followed by FC reporting no differences. The reader must reach the final statement before its byte-range check rejects the value.

Run GWBASIC STREAM.BAS again and return with SYSTEM. The saved helper still contains DB 66: the trial change was only in BASIC's memory. This leaves LONG.ASM valid for the copy exercise. Keep STREAM.BAS with the workbench sources.

An unexpected PASS fails this rejection test.

## If the result differs

Check RDPOS against RDLEN before refilling. Consume every byte of a short positive read; only a zero read is file EOF. Reset both cursors before each input pass.
