+++
title = "02 \u00b7 Reading a File in Blocks"
weight = 2
description = "Refill a small block instead of making a DOS call for every byte."
download = "A02.ASM"
cartoon = "asm86a-press.png"
aliases = ["/bootstrap/asm86a/02-reading-an-input-block/"]
download_group = "tools/asm1"
reader_names = 1
+++

A sequential reader can handle a long file with bounded working storage.

## The working parts

NEXTBYTE retains its interface: AX is one with CHAR set, or zero at EOF. RDPOS and RDLEN describe bytes already returned by DOS. A refill requests 1024 bytes at 5000H. Any positive returned count is consumed completely before another refill; a short positive read is not EOF.

The driver clears both fields at the start of each pass. NEXTBYTE changes AX, BX, CX, DX, flags, CHAR, and the two cursors, while preserving SI, DI, and BP. The line and token readers therefore need no new calling convention.

## Enter the source

Copy `A01.ASM` to `A02.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `RESNAME:`

Unchanged source immediately before this edit:

```asm
RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0
```

Insert after old physical line 1100.

Insert:

```asm
RDPOS:
DW 0

RDLEN:
DW 0
```

The following old source stays in place:

```asm
INOPEN:
DB 0
```

### Change 2 near `NEXTBYTE:`

Unchanged source immediately before this edit:

```asm
MOV DX,CHAR
MOV AH,3FH
INT 21H
```

Remove this exact source at old physical positions 114–117:

```asm
JAE BYTEOK
MOV AX,6
JMP ERROR
BYTEOK:
```

Replace it with:

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

The following old source stays in place:

```asm
RET
```

### Change 3 near `NEXTBYTE:`

Unchanged source immediately before this edit:

```asm

NEXTBYTE:
MOV BX,[HANDLE]
```

Remove this exact source at old physical positions 110–111:

```asm
MOV CX,1
MOV DX,CHAR
```

Replace it with:

```asm
MOV DX,5000H
MOV CX,1024
```

The following old source stays in place:

```asm
MOV AH,3FH
INT 21H
```

### Change 4 near `NEXTBYTE:`

Unchanged source immediately before this edit:

```asm
RET

NEXTBYTE:
```

Insert after old physical line 108.

Insert:

```asm
MOV AX,[RDPOS]
MOV DX,[RDLEN]
CMP AX,DX
JB BUFFERBYTE
```

The following old source stays in place:

```asm
MOV BX,[HANDLE]
MOV CX,1
```

### Change 5 near `PASSSTART:`

Unchanged source immediately before this edit:

```asm
MOV [OUTPTR],AX
MOV AX,0
MOV [LINENO],AX
```

Insert after old physical line 21.

Insert:

```asm
MOV [RDPOS],AX
MOV [RDLEN],AX
```

The following old source stays in place:

```asm
MOV [ENDED],AL
MOV [SKIPLF],AL
```

## Build the stopping point

Run `CHECK ASMKEEP`, enter `A02` at `Source name:`, and require `OK 02589 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. It creates A02.COM.

VIEW.BAS must report A02.COM length 2589 bytes. Keep that executable and source together.

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
COPY T02.ASM SOURCE.ASM
```

```dos
CHECK A02
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
COPY X02.ASM SOURCE.ASM
CHECK A02
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check the fixed name bytes, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
