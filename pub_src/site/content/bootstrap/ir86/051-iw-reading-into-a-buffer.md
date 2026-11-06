+++
title = "IW15 \u00b7 Reading into a buffer"
weight = 51
description = "Consume a saved handle and pointer, return actual progress, and refill after short reads."
download = "IW15.ASM"
download_group = "toolchain"
+++

Consume a saved handle and pointer, return actual progress, and refill after short reads.

## The working parts

Consume a saved handle and pointer, return actual progress, and refill after short reads. The assembly routines use the inherited bounded reader and owned-file cleanup. The operation table supplies argument class, stack action, and an authored target template. Native encodings belong to this backend; the IR operation retains its abstract meaning.

## Enter the source

Copy IW14.ASM to IW15.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_OPEN
DB 67,82,69,65,84,69,0,0,0,0,0,0,0,0
DW T_CREATE
```

Insert after old physical line 1432.

Insert:

```asm
DB 82,69,65,68,0,0,0,0,0,0,0,3,0,0
DW T_READ
```

### Edit 2

Unchanged source immediately before the edit:

```asm
DB 77,79,86,32,65,88,44,91,82,95,83,84,65,84,85,83
DB 93,13,10,0
```

Insert after old physical line 1343.

Insert:

```asm
T_READ:
DB 80,79,80,32,68,88,13,10,80,79,80,32,66,88,13,10
DB 67,65,76,76,32,82,95,82,69,65,68,13,10,0
```

The following old source remains in place:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DB 83,76,79,84,70,79,85,78,68,58,13,10,77,79,86,32
DB 91,82,95,83,76,79,84,93,44,66,88,13,10,77,79,86
DB 32,91,82,95,78,85,77,66,69,82,93,44,67,88,13,10
```

Remove this source at old physical positions 1163–1174 in IW14.ASM:

```asm
DB 82,69,84,13,10,13,10,82,95,83,84,65,84,85,83,58
DB 13,10,68,87,32,48,13,10,13,10,82,95,66,89,84,69
DB 58,13,10,68,66,32,48,13,10,13,10,82,95,77,79,68
DB 69,58,13,10,68,87,32,48,13,10,82,95,78,65,77,69
DB 58,13,10,68,87,32,48,13,10,82,95,83,76,79,84,58
DB 13,10,68,87,32,48,13,10,82,95,78,85,77,66,69,82
DB 58,13,10,68,87,32,48,13,10,82,95,72,65,78,68,76
DB 69,83,58,13,10,68,87,32,48,44,48,44,48,44,48,44
DB 48,44,48,44,48,44,48,13,10,13,10,82,95,83,84,65
DB 67,75,70,65,73,76,58,13,10,77,79,86,32,65,88,44
DB 52,67,48,50,72,13,10,73,78,84,32,50,49,72,13,10
DB 0
```

Replace it with:

```asm
DB 82,69,84,13,10,13,10,82,95,70,73,78,68,58,13,10
DB 67,77,80,32,66,88,44,49,13,10,74,66,32,78,69,65
DB 82,32,82,95,66,65,68,72,65,78,68,76,69,13,10,67
DB 77,80,32,66,88,44,56,13,10,74,65,32,78,69,65,82
DB 32,82,95,66,65,68,72,65,78,68,76,69,13,10,68,69
DB 67,32,66,88,13,10,65,68,68,32,66,88,44,66,88,13
DB 10,65,68,68,32,66,88,44,82,95,72,65,78,68,76,69
DB 83,13,10,77,79,86,32,91,82,95,83,76,79,84,93,44
DB 66,88,13,10,77,79,86,32,66,88,44,91,66,88,93,13
DB 10,67,77,80,32,66,88,44,48,13,10,74,69,32,78,69
DB 65,82,32,82,95,66,65,68,72,65,78,68,76,69,13,10
DB 77,79,86,32,65,88,44,49,13,10,67,77,80,32,66,88
DB 44,56,48,48,48,72,13,10,74,66,32,78,69,65,82,32
DB 82,95,72,65,78,68,76,69,75,73,78,68,13,10,65,78
DB 68,32,66,88,44,55,70,70,70,72,13,10,77,79,86,32
DB 65,88,44,50,13,10,82,95,72,65,78,68,76,69,75,73
DB 78,68,58,13,10,68,69,67,32,66,88,13,10,82,69,84
DB 13,10,82,95,66,65,68,72,65,78,68,76,69,58,13,10
DB 77,79,86,32,65,88,44,48,13,10,82,69,84,13,10,13
DB 10,82,95,82,69,65,68,58,13,10,77,79,86,32,91,82
DB 95,67,79,85,78,84,93,44,65,88,13,10,77,79,86,32
DB 91,82,95,66,85,70,70,69,82,93,44,68,88,13,10,67
DB 65,76,76,32,82,95,70,73,78,68,13,10,67,77,80,32
DB 65,88,44,49,13,10,74,69,32,78,69,65,82,32,82,95
DB 82,69,65,68,86,65,76,73,68,13,10,74,77,80,32,82
DB 95,70,65,73,76,13,10,82,95,82,69,65,68,86,65,76
DB 73,68,58,13,10,77,79,86,32,67,88,44,91,82,95,67
DB 79,85,78,84,93,13,10,67,77,80,32,67,88,44,48,13
DB 10,74,78,69,32,78,69,65,82,32,82,95,82,69,65,68
DB 77,79,82,69,13,10,77,79,86,32,65,88,44,48,13,10
DB 74,77,80,32,82,95,79,75,13,10,82,95,82,69,65,68
DB 77,79,82,69,58,13,10,77,79,86,32,68,88,44,91,82
DB 95,66,85,70,70,69,82,93,13,10,77,79,86,32,65,72
DB 44,51,70,72,13,10,73,78,84,32,50,49,72,13,10,74
DB 65,69,32,78,69,65,82,32,82,95,82,69,65,68,71,79
DB 79,68,13,10,74,77,80,32,82,95,70,65,73,76,13,10
DB 82,95,82,69,65,68,71,79,79,68,58,13,10,74,77,80
DB 32,82,95,79,75,13,10,13,10,82,95,83,84,65,84,85
DB 83,58,13,10,68,87,32,48,13,10,13,10,82,95,66,89
DB 84,69,58,13,10,68,66,32,48,13,10,13,10,82,95,77
DB 79,68,69,58,13,10,68,87,32,48,13,10,82,95,78,65
DB 77,69,58,13,10,68,87,32,48,13,10,82,95,83,76,79
DB 84,58,13,10,68,87,32,48,13,10,82,95,78,85,77,66
DB 69,82,58,13,10,68,87,32,48,13,10,82,95,72,65,78
DB 68,76,69,83,58,13,10,68,87,32,48,44,48,44,48,44
DB 48,44,48,44,48,44,48,44,48,13,10,13,10,82,95,67
DB 79,85,78,84,58,13,10,68,87,32,48,13,10,82,95,66
DB 85,70,70,69,82,58,13,10,68,87,32,48,13,10,13,10
DB 82,95,83,84,65,67,75,70,65,73,76,58,13,10,77,79
DB 86,32,65,88,44,52,67,48,50,72,13,10,73,78,84,32
DB 50,49,72,13,10,0
```

The following old source remains in place:

```asm

T_NOP:
```

### Edit 4

Unchanged source immediately before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove this source at old physical positions 834–834 in IW14.ASM:

```asm
MOV CX,44
```

Replace it with:

```asm
MOV CX,45
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW15.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 06435 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW15.COM
```

VIEW.BAS must report IW15.COM length 6435 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW15.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
WORD NAME 65
WORD H 0
BUFFER B 1
LABEL MAIN
ADDR NAME
OPEN
ST H
LD H
PUSH
ADDR B
PUSH
LIT 1
READ
PUSH
LIT 1
EQ GOOD
LIT 1
EXIT
LABEL GOOD
HALT
```

```dos
COPY TIW15.IR SOURCE.IR
```

```dos
CHECK IW15
```

Require, apart from command echo and the checker's separator:

```text
OK RESULT.ASM 0000002386 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00476 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 476 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 CD 01 E8 09 00 B4 4C CD 21 41 00 00 00 00 B8 11 01 E8 9B 00 89 06 13 01
```

First create the ordinary input file A with `ECHO A>A`. Its declared filename is the word 65 followed by its zero high byte. Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW15.IR:

```ir
UNKNOWN
```

```dos
COPY XIW15.IR SOURCE.IR
CHECK IW15
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
