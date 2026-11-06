+++
title = "IW16 \u00b7 Writing a bounded block"
weight = 52
description = "Check both service status and actual write progress."
download = "IW16.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Check both service status and actual write progress.

## Enter the source

Copy IW15.ASM to IW16.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_CREATE
DB 82,69,65,68,0,0,0,0,0,0,0,3,0,0
DW T_READ
```

Insert after old physical line 1477.

Insert:

```asm
DB 87,82,73,84,69,0,0,0,0,0,0,3,0,0
DW T_WRITE
```

### Edit 2

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,68,88,13,10,80,79,80,32,66,88,13,10
DB 67,65,76,76,32,82,95,82,69,65,68,13,10,0
```

Insert after old physical line 1386.

Insert:

```asm
T_WRITE:
DB 80,79,80,32,68,88,13,10,80,79,80,32,66,88,13,10
DB 67,65,76,76,32,82,95,87,82,73,84,69,13,10,0
```

The following old source remains in place:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DB 65,69,32,78,69,65,82,32,82,95,82,69,65,68,71,79
DB 79,68,13,10,74,77,80,32,82,95,70,65,73,76,13,10
DB 82,95,82,69,65,68,71,79,79,68,58,13,10,74,77,80
```

Remove this source at old physical positions 1200–1213 in IW15.ASM:

```asm
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

Replace it with:

```asm
DB 32,82,95,79,75,13,10,13,10,82,95,87,82,73,84,69
DB 58,13,10,77,79,86,32,91,82,95,67,79,85,78,84,93
DB 44,65,88,13,10,77,79,86,32,91,82,95,66,85,70,70
DB 69,82,93,44,68,88,13,10,67,65,76,76,32,82,95,70
DB 73,78,68,13,10,67,77,80,32,65,88,44,50,13,10,74
DB 69,32,78,69,65,82,32,82,95,87,82,73,84,69,86,65
DB 76,73,68,13,10,74,77,80,32,82,95,70,65,73,76,13
DB 10,82,95,87,82,73,84,69,86,65,76,73,68,58,13,10
DB 77,79,86,32,67,88,44,91,82,95,67,79,85,78,84,93
DB 13,10,67,77,80,32,67,88,44,48,13,10,74,78,69,32
DB 78,69,65,82,32,82,95,87,82,73,84,69,77,79,82,69
DB 13,10,77,79,86,32,65,88,44,48,13,10,74,77,80,32
DB 82,95,79,75,13,10,82,95,87,82,73,84,69,77,79,82
DB 69,58,13,10,77,79,86,32,68,88,44,91,82,95,66,85
DB 70,70,69,82,93,13,10,77,79,86,32,65,72,44,52,48
DB 72,13,10,73,78,84,32,50,49,72,13,10,74,65,69,32
DB 78,69,65,82,32,82,95,87,82,73,84,69,67,79,85,78
DB 84,13,10,74,77,80,32,82,95,70,65,73,76,13,10,82
DB 95,87,82,73,84,69,67,79,85,78,84,58,13,10,77,79
DB 86,32,68,88,44,91,82,95,67,79,85,78,84,93,13,10
DB 67,77,80,32,65,88,44,68,88,13,10,74,69,32,78,69
DB 65,82,32,82,95,87,82,73,84,69,71,79,79,68,13,10
DB 74,77,80,32,82,95,69,82,82,79,82,13,10,82,95,87
DB 82,73,84,69,71,79,79,68,58,13,10,74,77,80,32,82
DB 95,79,75,13,10,13,10,82,95,83,84,65,84,85,83,58
DB 13,10,68,87,32,48,13,10,13,10,82,95,66,89,84,69
DB 58,13,10,68,66,32,48,13,10,13,10,82,95,77,79,68
DB 69,58,13,10,68,87,32,48,13,10,82,95,78,65,77,69
DB 58,13,10,68,87,32,48,13,10,82,95,83,76,79,84,58
DB 13,10,68,87,32,48,13,10,82,95,78,85,77,66,69,82
DB 58,13,10,68,87,32,48,13,10,82,95,72,65,78,68,76
DB 69,83,58,13,10,68,87,32,48,44,48,44,48,44,48,44
DB 48,44,48,44,48,44,48,13,10,13,10,82,95,67,79,85
DB 78,84,58,13,10,68,87,32,48,13,10,82,95,66,85,70
DB 70,69,82,58,13,10,68,87,32,48,13,10,13,10,82,95
DB 83,84,65,67,75,70,65,73,76,58,13,10,77,79,86,32
DB 65,88,44,52,67,48,50,72,13,10,73,78,84,32,50,49
DB 72,13,10,0
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

Remove this source at old physical positions 834–834 in IW15.ASM:

```asm
MOV CX,45
```

Replace it with:

```asm
MOV CX,46
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW16.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 06864 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW16.COM
```

VIEW.BAS must report IW16.COM length 6864 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW16.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
WORD NAME 65
WORD H 0
BYTE B 65
LABEL MAIN
ADDR NAME
CREATE
ST H
LD H
PUSH
ADDR B
PUSH
LIT 1
WRITE
PUSH
LIT 1
EQ GOOD
LIT 1
EXIT
LABEL GOOD
HALT
```

```dos
COPY TIW16.IR SOURCE.IR
```

```dos
CHECK IW16
```

Require:

```text
OK RESULT.ASM 0000002769 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00551 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 551 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 18 02 E8 09 00 B4 4C CD 21 41 00 00 00 41 B8 11 01 E8 A1 00 89 06 13 01
```

Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW16.IR:

```ir
UNKNOWN
```

```dos
COPY XIW16.IR SOURCE.IR
CHECK IW16
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
