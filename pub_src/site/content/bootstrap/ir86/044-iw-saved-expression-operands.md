+++
title = "IW08 \u00b7 Saved expression operands"
weight = 44
description = "Check push/pop depth and apply word arithmetic before a control boundary."
download = "IW08.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Check push/pop depth and apply word arithmetic before a control boundary.

## Enter the source

Copy IW07.ASM to IW08.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_FETCH
DB 70,69,84,67,72,66,0,0,0,0,0,0,0,0
DW T_FETCHB
```

Insert after old physical line 1174.

Insert:

```asm
DB 80,85,83,72,0,0,0,0,0,0,0,1,0,0
DW T_PUSH
DB 80,79,80,0,0,0,0,0,0,0,0,2,0,0
DW T_POP
DB 65,68,68,0,0,0,0,0,0,0,0,2,0,0
DW T_ADD
DB 83,85,66,0,0,0,0,0,0,0,0,2,0,0
DW T_SUB
DB 65,78,68,0,0,0,0,0,0,0,0,2,0,0
DW T_AND
DB 79,82,0,0,0,0,0,0,0,0,0,2,0,0
DW T_OR
DB 88,79,82,0,0,0,0,0,0,0,0,2,0,0
DW T_XOR
DB 80,85,84,0,0,0,0,0,0,0,0,2,0,0
DW T_PUT
DB 80,85,84,66,0,0,0,0,0,0,0,2,0,0
DW T_PUTB
```

### Edit 2

Unchanged source immediately before the edit:

```asm
DB 76,44,91,66,88,93,13,10,77,79,86,32,65,72,44,48
DB 13,10,0
```

Insert after old physical line 1143.

Insert:

```asm
T_PUSH:
DB 80,85,83,72,32,65,88,13,10,0

T_POP:
DB 80,79,80,32,65,88,13,10,0

T_PUT:
DB 80,79,80,32,66,88,13,10,77,79,86,32,91,66,88,93
DB 44,65,88,13,10,0

T_PUTB:
DB 80,79,80,32,66,88,13,10,77,79,86,32,91,66,88,93
DB 44,65,76,13,10,0

T_ADD:
DB 80,79,80,32,66,88,13,10,65,68,68,32,65,88,44,66
DB 88,13,10,0

T_AND:
DB 80,79,80,32,66,88,13,10,65,78,68,32,65,88,44,66
DB 88,13,10,0

T_OR:
DB 80,79,80,32,66,88,13,10,79,82,32,65,88,44,66,88
DB 13,10,0

T_XOR:
DB 80,79,80,32,66,88,13,10,88,79,82,32,65,88,44,66
DB 88,13,10,0

T_SUB:
DB 80,79,80,32,66,88,13,10,83,85,66,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,66,88,13,10,0
```

The following old source remains in place:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit 3

Unchanged source immediately before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove this source at old physical positions 834–834 in IW07.ASM:

```asm
MOV CX,15
```

Replace it with:

```asm
MOV CX,24
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW08.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 03580 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW08.COM
```

VIEW.BAS must report IW08.COM length 3580 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW08.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
LABEL MAIN
LIT 7
PUSH
LIT 7
SUB
EXIT
```

```dos
COPY TIW08.IR SOURCE.IR
```

```dos
CHECK IW08
```

Require:

```text
OK RESULT.ASM 0000000210 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00038 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 38 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 17 00 E8 04 00 B4 4C CD 21 B8 07 00 50 B8 07 00 5B 2B D8 8B C3 B4 4C CD
```

Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW08.IR:

```ir
UNKNOWN
```

```dos
COPY XIW08.IR SOURCE.IR
CHECK IW08
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
