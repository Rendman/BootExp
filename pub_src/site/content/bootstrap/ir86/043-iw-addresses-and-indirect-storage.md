+++
title = "IW07 \u00b7 Addresses and indirect storage"
weight = 43
description = "Keep byte addresses and canonical word loads independent of physical registers."
download = "IW07.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Keep byte addresses and canonical word loads independent of physical registers.

## Enter the source

Copy IW06.ASM to IW07.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_BYTE
DB 66,85,70,70,69,82,0,0,0,0,3,4,0,0
DW T_BUFFER
```

Insert after old physical line 1135.

Insert:

```asm
DB 76,68,0,0,0,0,0,0,0,0,2,0,0,0
DW T_LD
DB 83,84,0,0,0,0,0,0,0,0,2,0,0,0
DW T_ST
DB 76,68,66,0,0,0,0,0,0,0,2,0,0,0
DW T_LDB
DB 83,84,66,0,0,0,0,0,0,0,2,0,0,0
DW T_STB
DB 65,68,68,82,0,0,0,0,0,0,2,0,0,0
DW T_ADDR
DB 70,69,84,67,72,0,0,0,0,0,0,0,0,0
DW T_FETCH
DB 70,69,84,67,72,66,0,0,0,0,0,0,0,0
DW T_FETCHB
```

### Edit 2

Unchanged source immediately before the edit:

```asm

T_BUFFER:
DB 85,95,64,58,13,10,82,69,83,66,32,35,13,10,0
```

Insert after old physical line 1117.

Insert:

```asm

T_LD:
DB 77,79,86,32,65,88,44,91,85,95,64,93,13,10,0

T_ST:
DB 77,79,86,32,91,85,95,64,93,44,65,88,13,10,0

T_LDB:
DB 77,79,86,32,65,76,44,91,85,95,64,93,13,10,77,79
DB 86,32,65,72,44,48,13,10,0

T_STB:
DB 77,79,86,32,91,85,95,64,93,44,65,76,13,10,0

T_FETCH:
DB 77,79,86,32,66,88,44,65,88,13,10,77,79,86,32,65
DB 88,44,91,66,88,93,13,10,0

T_FETCHB:
DB 77,79,86,32,66,88,44,65,88,13,10,77,79,86,32,65
DB 76,44,91,66,88,93,13,10,77,79,86,32,65,72,44,48
DB 13,10,0
```

The following old source remains in place:

```asm

IRTAB:
```

### Edit 3

Unchanged source immediately before the edit:

```asm
T_LIT:
DB 77,79,86,32,65,88,44,35,13,10,0
```

Insert after old physical line 1109.

Insert:

```asm
T_ADDR:
DB 77,79,86,32,65,88,44,85,95,64,13,10,0
```

The following old source remains in place:

```asm
T_WORD:
DB 85,95,64,58,13,10,68,87,32,35,13,10,0
```

### Edit 4

Unchanged source immediately before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove this source at old physical positions 834–834 in IW06.ASM:

```asm
MOV CX,8
```

Replace it with:

```asm
MOV CX,15
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW07.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 03263 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW07.COM
```

VIEW.BAS must report IW07.COM length 3263 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW07.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
WORD X 65
LABEL MAIN
ADDR X
FETCHB
EXIT
```

```dos
COPY TIW07.IR SOURCE.IR
```

```dos
CHECK IW07
```

Require:

```text
OK RESULT.ASM 0000000205 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00037 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 37 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 16 00 E8 06 00 B4 4C CD 21 41 00 B8 11 01 8B D8 8A 07 B4 00 B4 4C CD 21
```

Run CHECK TRY. It deliberately returns 65; the checker reports FAIL. This verifies the program's explicit exit value.

## A rejection or boundary check

Create XIW07.IR:

```ir
UNKNOWN
```

```dos
COPY XIW07.IR SOURCE.IR
CHECK IW07
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
