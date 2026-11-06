+++
title = "IW22 \u00b7 Allocated block handles"
weight = 58
description = "Allocate byte extents beyond the main image and release owned blocks."
download = "IW22.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Allocate byte extents beyond the main image and release owned blocks.

## Enter the source

Copy IW21.ASM to IW22.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_DELETE
DB 82,69,78,65,77,69,0,0,0,0,0,2,0,0
DW T_RENAME
```

Insert after old physical line 1891.

Insert:

```asm
DB 65,76,76,79,67,0,0,0,0,0,0,0,0,0
DW T_ALLOC
DB 70,82,69,69,66,76,79,67,75,0,0,0,0,0
DW T_FREEBLOCK
```

### Edit 2

Unchanged source immediately before the edit:

```asm
T_EXISTS:
DB 67,65,76,76,32,82,95,69,88,73,83,84,83,13,10,0
```

Insert after old physical line 1732.

Insert:

```asm
T_ALLOC:
DB 67,65,76,76,32,82,95,65,76,76,79,67,13,10,0

T_FREEBLOCK:
DB 67,65,76,76,32,82,95,70,82,69,69,66,76,79,67,75
DB 13,10,0
```

The following old source remains in place:

```asm
T_RENAME:
DB 80,79,80,32,68,88,13,10,67,65,76,76,32,82,95,82
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DB 48,13,10,74,77,80,32,82,95,79,75,13,10,82,95,69
DB 70,65,73,76,58,13,10,77,79,86,32,65,88,44,54,53
DB 53,51,53,13,10,74,77,80,32,82,95,69,82,82,79,82
```

Remove this source at old physical positions 1416–1418 in IW21.ASM:

```asm
DB 13,10,13,10,82,95,83,84,65,67,75,70,65,73,76,58
DB 13,10,77,79,86,32,65,88,44,52,67,48,50,72,13,10
DB 73,78,84,32,50,49,72,13,10,0
```

Replace it with:

```asm
DB 13,10,13,10,82,95,65,76,76,79,67,58,13,10,67,77
DB 80,32,65,88,44,48,13,10,74,69,32,78,69,65,82,32
DB 82,95,68,70,65,73,76,13,10,77,79,86,32,91,82,95
DB 87,65,78,84,93,44,65,88,13,10,77,79,86,32,65,88
DB 44,67,83,13,10,77,79,86,32,69,83,44,65,88,13,10
DB 77,79,86,32,66,88,44,49,48,48,48,72,13,10,77,79
DB 86,32,65,72,44,52,65,72,13,10,73,78,84,32,50,49
DB 72,13,10,74,67,32,78,69,65,82,32,82,95,68,70,65
DB 73,76,13,10,77,79,86,32,83,73,44,82,95,66,76,79
DB 67,75,83,13,10,77,79,86,32,68,73,44,49,13,10,82
DB 95,65,76,76,79,67,83,76,79,84,58,13,10,67,77,80
DB 32,87,79,82,68,32,91,83,73,93,44,48,13,10,74,69
DB 32,78,69,65,82,32,82,95,65,76,76,79,67,70,79,85
DB 78,68,13,10,65,68,68,32,83,73,44,52,13,10,73,78
DB 67,32,68,73,13,10,67,77,80,32,68,73,44,49,55,13
DB 10,74,66,32,78,69,65,82,32,82,95,65,76,76,79,67
DB 83,76,79,84,13,10,74,77,80,32,82,95,70,65,73,76
DB 13,10,82,95,65,76,76,79,67,70,79,85,78,68,58,13
DB 10,77,79,86,32,66,88,44,91,82,95,87,65,78,84,93
DB 13,10,77,79,86,32,67,76,44,52,13,10,83,72,82,32
DB 66,88,44,67,76,13,10,77,79,86,32,65,88,44,91,82
DB 95,87,65,78,84,93,13,10,65,78,68,32,65,88,44,49
DB 53,13,10,67,77,80,32,65,88,44,48,13,10,74,69,32
DB 78,69,65,82,32,82,95,65,76,76,79,67,82,79,85,78
DB 68,13,10,73,78,67,32,66,88,13,10,82,95,65,76,76
DB 79,67,82,79,85,78,68,58,13,10,77,79,86,32,65,72
DB 44,52,56,72,13,10,73,78,84,32,50,49,72,13,10,74
DB 67,32,78,69,65,82,32,82,95,65,76,76,79,67,66,65
DB 68,13,10,77,79,86,32,91,83,73,93,44,65,88,13,10
DB 77,79,86,32,65,88,44,91,82,95,87,65,78,84,93,13
DB 10,77,79,86,32,91,83,73,43,50,93,44,65,88,13,10
DB 77,79,86,32,65,88,44,68,73,13,10,74,77,80,32,82
DB 95,79,75,13,10,82,95,65,76,76,79,67,66,65,68,58
DB 13,10,77,79,86,32,65,88,44,67,83,13,10,77,79,86
DB 32,69,83,44,65,88,13,10,74,77,80,32,82,95,70,65
DB 73,76,13,10,82,95,70,82,69,69,66,76,79,67,75,58
DB 13,10,77,79,86,32,66,88,44,65,88,13,10,67,77,80
DB 32,66,88,44,49,13,10,74,66,32,78,69,65,82,32,82
DB 95,68,70,65,73,76,13,10,67,77,80,32,66,88,44,49
DB 54,13,10,74,65,32,78,69,65,82,32,82,95,68,70,65
DB 73,76,13,10,68,69,67,32,66,88,13,10,83,72,76,32
DB 66,88,44,49,13,10,83,72,76,32,66,88,44,49,13,10
DB 65,68,68,32,66,88,44,82,95,66,76,79,67,75,83,13
DB 10,77,79,86,32,83,73,44,66,88,13,10,77,79,86,32
DB 65,88,44,91,83,73,93,13,10,67,77,80,32,65,88,44
DB 48,13,10,74,69,32,78,69,65,82,32,82,95,68,70,65
DB 73,76,13,10,77,79,86,32,69,83,44,65,88,13,10,77
DB 79,86,32,65,72,44,52,57,72,13,10,73,78,84,32,50
DB 49,72,13,10,74,67,32,78,69,65,82,32,82,95,70,82
DB 69,69,66,65,68,13,10,77,79,86,32,87,79,82,68,32
DB 91,83,73,93,44,48,13,10,77,79,86,32,65,88,44,67
DB 83,13,10,77,79,86,32,69,83,44,65,88,13,10,77,79
DB 86,32,65,88,44,48,13,10,74,77,80,32,82,95,79,75
DB 13,10,82,95,70,82,69,69,66,65,68,58,13,10,77,79
DB 86,32,65,88,44,67,83,13,10,77,79,86,32,69,83,44
DB 65,88,13,10,74,77,80,32,82,95,70,65,73,76,13,10
DB 13,10,82,95,83,84,65,67,75,70,65,73,76,58,13,10
DB 77,79,86,32,65,88,44,52,67,48,50,72,13,10,73,78
DB 84,32,50,49,72,13,10,13,10,82,95,87,65,78,84,58
DB 13,10,68,87,32,48,13,10,82,95,77,69,77,86,65,76
DB 85,69,58,13,10,68,87,32,48,13,10,82,95,66,76,79
DB 67,75,83,58,13,10,82,69,83,87,32,51,50,13,10,0
```

The following old source remains in place:

```asm

T_LITS:
```

### Edit 4

Unchanged source immediately before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove this source at old physical positions 834–834 in IW21.ASM:

```asm
MOV CX,77
```

Replace it with:

```asm
MOV CX,79
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW22.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 10563 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW22.COM
```

VIEW.BAS must report IW22.COM length 10563 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW22.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
WORD H 0
PROC MAIN 0 0
LIT 40960
ALLOC
ST H
STATUS
JNZ BAD
LD H
FREEBLOCK
STATUS
RETURN
LABEL BAD
LIT 1
RETURN
```

```dos
COPY TIW22.IR SOURCE.IR
```

```dos
CHECK IW22
```

Require:

```text
OK RESULT.ASM 0000004429 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00950 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 950 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 63 03 E8 06 00 B4 4C CD 21 00 00 55 8B EC 81 EC 00 00 81 FC 00 F0 73 03
```

Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW22.IR:

```ir
UNKNOWN
```

```dos
COPY XIW22.IR SOURCE.IR
CHECK IW22
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
