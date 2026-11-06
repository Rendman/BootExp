+++
title = "IW11 \u00b7 Counted console output"
weight = 47
description = "Bind PUTC and persistent STATUS to checked byte output."
download = "IW11.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Bind PUTC and persistent STATUS to checked byte output.

## Enter the source

Copy IW10.ASM to IW11.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_CALL
DB 82,69,84,0,0,0,0,0,0,0,0,4,0,0
DW T_RET
```

Insert after old physical line 1323.

Insert:

```asm
DB 80,85,84,67,0,0,0,0,0,0,0,0,0,0
DW T_PUTC
DB 83,84,65,84,85,83,0,0,0,0,0,0,0,0
DW T_STATUS
```

### Edit 2

Unchanged source immediately before the edit:

```asm
T_RET:
DB 82,69,84,13,10,0
```

Insert after old physical line 1244.

Insert:

```asm
T_PUTC:
DB 67,65,76,76,32,82,95,80,85,84,67,13,10,0

T_STATUS:
DB 77,79,86,32,65,88,44,91,82,95,83,84,65,84,85,83
DB 93,13,10,0
```

The following old source remains in place:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DB 72,13,10,73,78,84,32,50,49,72,13,10,0

T_RUNTIME:
```

Remove this source at old physical positions 1089–1091 in IW10.ASM:

```asm
DB 82,95,83,84,65,67,75,70,65,73,76,58,13,10,77,79
DB 86,32,65,88,44,52,67,48,50,72,13,10,73,78,84,32
DB 50,49,72,13,10,0
```

Replace it with:

```asm
DB 82,95,79,75,58,13,10,77,79,86,32,68,88,44,48,13
DB 10,77,79,86,32,91,82,95,83,84,65,84,85,83,93,44
DB 68,88,13,10,82,69,84,13,10,82,95,69,82,82,79,82
DB 58,13,10,77,79,86,32,68,88,44,49,13,10,77,79,86
DB 32,91,82,95,83,84,65,84,85,83,93,44,68,88,13,10
DB 82,69,84,13,10,82,95,70,65,73,76,58,13,10,77,79
DB 86,32,65,88,44,48,13,10,74,77,80,32,82,95,69,82
DB 82,79,82,13,10,13,10,82,95,80,85,84,67,58,13,10
DB 77,79,86,32,91,82,95,66,89,84,69,93,44,65,76,13
DB 10,77,79,86,32,66,88,44,49,13,10,77,79,86,32,67
DB 88,44,49,13,10,77,79,86,32,68,88,44,82,95,66,89
DB 84,69,13,10,77,79,86,32,65,72,44,52,48,72,13,10
DB 73,78,84,32,50,49,72,13,10,74,65,69,32,78,69,65
DB 82,32,82,95,80,85,84,67,79,85,78,84,13,10,74,77
DB 80,32,82,95,70,65,73,76,13,10,82,95,80,85,84,67
DB 79,85,78,84,58,13,10,67,77,80,32,65,88,44,49,13
DB 10,74,69,32,78,69,65,82,32,82,95,80,85,84,71,79
DB 79,68,13,10,74,77,80,32,82,95,69,82,82,79,82,13
DB 10,82,95,80,85,84,71,79,79,68,58,13,10,74,77,80
DB 32,82,95,79,75,13,10,13,10,82,95,83,84,65,84,85
DB 83,58,13,10,68,87,32,48,13,10,13,10,82,95,66,89
DB 84,69,58,13,10,68,66,32,48,13,10,13,10,82,95,83
DB 84,65,67,75,70,65,73,76,58,13,10,77,79,86,32,65
DB 88,44,52,67,48,50,72,13,10,73,78,84,32,50,49,72
DB 13,10,0
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

Remove this source at old physical positions 834–834 in IW10.ASM:

```asm
MOV CX,39
```

Replace it with:

```asm
MOV CX,41
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW11.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 04694 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW11.COM
```

VIEW.BAS must report IW11.COM length 4694 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW11.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
LABEL MAIN
LIT 65
PUTC
HALT
```

```dos
COPY TIW11.IR SOURCE.IR
```

```dos
CHECK IW11
```

Require:

```text
OK RESULT.ASM 0000000521 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00098 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 98 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 53 00 E8 04 00 B4 4C CD 21 B8 41 00 E8 1B 00 B8 00 4C CD 21 BA 00 00 89
```

Run CHECK TRY. It displays `A` and reports PASS.

## A rejection or boundary check

Create XIW11.IR:

```ir
UNKNOWN
```

```dos
COPY XIW11.IR SOURCE.IR
CHECK IW11
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
