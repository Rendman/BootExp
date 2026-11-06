+++
title = "IW14 \u00b7 Creating a counted file"
weight = 50
description = "Create writable handles through the same opaque slot table."
download = "IW14.ASM"
download_group = "toolchain"
+++

Create writable handles through the same opaque slot table.

## The working parts

Create writable handles through the same opaque slot table. The assembly routines use the inherited bounded reader and owned-file cleanup. The operation table supplies argument class, stack action, and an authored target template. Native encodings belong to this backend; the IR operation retains its abstract meaning.

## Enter the source

Copy IW13.ASM to IW14.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_GETC
DB 79,80,69,78,0,0,0,0,0,0,0,0,0,0
DW T_OPEN
```

Insert after old physical line 1424.

Insert:

```asm
DB 67,82,69,65,84,69,0,0,0,0,0,0,0,0
DW T_CREATE
```

### Edit 2

Unchanged source immediately before the edit:

```asm
T_OPEN:
DB 67,65,76,76,32,82,95,79,80,69,78,13,10,0
```

Insert after old physical line 1333.

Insert:

```asm
T_CREATE:
DB 67,65,76,76,32,82,95,67,82,69,65,84,69,13,10,0
```

The following old source remains in place:

```asm
T_STATUS:
DB 77,79,86,32,65,88,44,91,82,95,83,84,65,84,85,83
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DB 44,48,13,10,74,77,80,32,82,95,79,75,13,10,13,10
DB 82,95,79,80,69,78,58,13,10,77,79,86,32,68,88,44
DB 51,68,48,48,72,13,10,74,77,80,32,82,95,70,73,76
```

Remove this source at old physical positions 1125–1171 in IW13.ASM:

```asm
DB 69,13,10,13,10,82,95,70,73,76,69,58,13,10,77,79
DB 86,32,91,82,95,77,79,68,69,93,44,68,88,13,10,77
DB 79,86,32,91,82,95,78,65,77,69,93,44,65,88,13,10
DB 67,65,76,76,32,82,95,70,82,69,69,13,10,67,77,80
DB 32,66,88,44,48,13,10,74,78,69,32,78,69,65,82,32
DB 82,95,72,65,86,69,83,76,79,84,13,10,74,77,80,32
DB 82,95,70,65,73,76,13,10,82,95,72,65,86,69,83,76
DB 79,84,58,13,10,77,79,86,32,68,88,44,91,82,95,78
DB 65,77,69,93,13,10,77,79,86,32,67,88,44,48,13,10
DB 77,79,86,32,65,88,44,91,82,95,77,79,68,69,93,13
DB 10,73,78,84,32,50,49,72,13,10,74,65,69,32,78,69
DB 65,82,32,82,95,70,73,76,69,71,79,79,68,13,10,74
DB 77,80,32,82,95,70,65,73,76,13,10,82,95,70,73,76
DB 69,71,79,79,68,58,13,10,73,78,67,32,65,88,13,10
DB 77,79,86,32,68,88,44,91,82,95,77,79,68,69,93,13
DB 10,67,77,80,32,68,88,44,51,67,48,48,72,13,10,74
DB 78,69,32,78,69,65,82,32,82,95,82,69,65,68,83,76
DB 79,84,13,10,65,68,68,32,65,88,44,56,48,48,48,72
DB 13,10,82,95,82,69,65,68,83,76,79,84,58,13,10,77
DB 79,86,32,66,88,44,91,82,95,83,76,79,84,93,13,10
DB 77,79,86,32,91,66,88,93,44,65,88,13,10,77,79,86
DB 32,65,88,44,91,82,95,78,85,77,66,69,82,93,13,10
DB 74,77,80,32,82,95,79,75,13,10,82,95,70,82,69,69
DB 58,13,10,77,79,86,32,66,88,44,82,95,72,65,78,68
DB 76,69,83,13,10,77,79,86,32,67,88,44,49,13,10,82
DB 95,78,69,88,84,83,76,79,84,58,13,10,77,79,86,32
DB 65,88,44,91,66,88,93,13,10,67,77,80,32,65,88,44
DB 48,13,10,74,69,32,78,69,65,82,32,82,95,83,76,79
DB 84,70,79,85,78,68,13,10,65,68,68,32,66,88,44,50
DB 13,10,73,78,67,32,67,88,13,10,67,77,80,32,67,88
DB 44,57,13,10,74,66,32,78,69,65,82,32,82,95,78,69
DB 88,84,83,76,79,84,13,10,77,79,86,32,66,88,44,48
DB 13,10,82,69,84,13,10,82,95,83,76,79,84,70,79,85
DB 78,68,58,13,10,77,79,86,32,91,82,95,83,76,79,84
DB 93,44,66,88,13,10,77,79,86,32,91,82,95,78,85,77
DB 66,69,82,93,44,67,88,13,10,82,69,84,13,10,13,10
DB 82,95,83,84,65,84,85,83,58,13,10,68,87,32,48,13
DB 10,13,10,82,95,66,89,84,69,58,13,10,68,66,32,48
DB 13,10,13,10,82,95,77,79,68,69,58,13,10,68,87,32
DB 48,13,10,82,95,78,65,77,69,58,13,10,68,87,32,48
DB 13,10,82,95,83,76,79,84,58,13,10,68,87,32,48,13
DB 10,82,95,78,85,77,66,69,82,58,13,10,68,87,32,48
DB 13,10,82,95,72,65,78,68,76,69,83,58,13,10,68,87
DB 32,48,44,48,44,48,44,48,44,48,44,48,44,48,44,48
DB 13,10,13,10,82,95,83,84,65,67,75,70,65,73,76,58
DB 13,10,77,79,86,32,65,88,44,52,67,48,50,72,13,10
DB 73,78,84,32,50,49,72,13,10,0
```

Replace it with:

```asm
DB 69,13,10,13,10,82,95,67,82,69,65,84,69,58,13,10
DB 77,79,86,32,68,88,44,51,67,48,48,72,13,10,74,77
DB 80,32,82,95,70,73,76,69,13,10,13,10,82,95,70,73
DB 76,69,58,13,10,77,79,86,32,91,82,95,77,79,68,69
DB 93,44,68,88,13,10,77,79,86,32,91,82,95,78,65,77
DB 69,93,44,65,88,13,10,67,65,76,76,32,82,95,70,82
DB 69,69,13,10,67,77,80,32,66,88,44,48,13,10,74,78
DB 69,32,78,69,65,82,32,82,95,72,65,86,69,83,76,79
DB 84,13,10,74,77,80,32,82,95,70,65,73,76,13,10,82
DB 95,72,65,86,69,83,76,79,84,58,13,10,77,79,86,32
DB 68,88,44,91,82,95,78,65,77,69,93,13,10,77,79,86
DB 32,67,88,44,48,13,10,77,79,86,32,65,88,44,91,82
DB 95,77,79,68,69,93,13,10,73,78,84,32,50,49,72,13
DB 10,74,65,69,32,78,69,65,82,32,82,95,70,73,76,69
DB 71,79,79,68,13,10,74,77,80,32,82,95,70,65,73,76
DB 13,10,82,95,70,73,76,69,71,79,79,68,58,13,10,73
DB 78,67,32,65,88,13,10,77,79,86,32,68,88,44,91,82
DB 95,77,79,68,69,93,13,10,67,77,80,32,68,88,44,51
DB 67,48,48,72,13,10,74,78,69,32,78,69,65,82,32,82
DB 95,82,69,65,68,83,76,79,84,13,10,65,68,68,32,65
DB 88,44,56,48,48,48,72,13,10,82,95,82,69,65,68,83
DB 76,79,84,58,13,10,77,79,86,32,66,88,44,91,82,95
DB 83,76,79,84,93,13,10,77,79,86,32,91,66,88,93,44
DB 65,88,13,10,77,79,86,32,65,88,44,91,82,95,78,85
DB 77,66,69,82,93,13,10,74,77,80,32,82,95,79,75,13
DB 10,82,95,70,82,69,69,58,13,10,77,79,86,32,66,88
DB 44,82,95,72,65,78,68,76,69,83,13,10,77,79,86,32
DB 67,88,44,49,13,10,82,95,78,69,88,84,83,76,79,84
DB 58,13,10,77,79,86,32,65,88,44,91,66,88,93,13,10
DB 67,77,80,32,65,88,44,48,13,10,74,69,32,78,69,65
DB 82,32,82,95,83,76,79,84,70,79,85,78,68,13,10,65
DB 68,68,32,66,88,44,50,13,10,73,78,67,32,67,88,13
DB 10,67,77,80,32,67,88,44,57,13,10,74,66,32,78,69
DB 65,82,32,82,95,78,69,88,84,83,76,79,84,13,10,77
DB 79,86,32,66,88,44,48,13,10,82,69,84,13,10,82,95
DB 83,76,79,84,70,79,85,78,68,58,13,10,77,79,86,32
DB 91,82,95,83,76,79,84,93,44,66,88,13,10,77,79,86
DB 32,91,82,95,78,85,77,66,69,82,93,44,67,88,13,10
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

Remove this source at old physical positions 834–834 in IW13.ASM:

```asm
MOV CX,43
```

Replace it with:

```asm
MOV CX,44
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW14.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 05760 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW14.COM
```

VIEW.BAS must report IW14.COM length 5760 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW14.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
WORD NAME 65
LABEL MAIN
ADDR NAME
CREATE
STATUS
JZ GOOD
LIT 1
EXIT
LABEL GOOD
HALT
```

```dos
COPY TIW14.IR SOURCE.IR
```

```dos
CHECK IW14
```

Require, apart from command echo and the checker's separator:

```text
OK RESULT.ASM 0000001611 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00323 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 323 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 34 01 E8 06 00 B4 4C CD 21 41 00 B8 11 01 E8 8D 00 8B 06 23 02 81 F8 00
```

Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW14.IR:

```ir
UNKNOWN
```

```dos
COPY XIW14.IR SOURCE.IR
CHECK IW14
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
