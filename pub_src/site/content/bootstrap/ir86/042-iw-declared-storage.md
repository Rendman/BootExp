+++
title = "IW06 \u00b7 Declared storage"
weight = 42
description = "Give named byte and word storage fixed sizes and materialize larger buffers with RESB."
download = "IW06.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Give named byte and word storage fixed sizes and materialize larger buffers with RESB.

## Enter the source

Copy IW05.ASM to IW06.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_NOP
DB 69,88,73,84,0,0,0,0,0,0,0,4,0,0
DW T_EXIT
```

Insert after old physical line 1120.

Insert:

```asm
DB 87,79,82,68,0,0,0,0,0,0,3,4,0,0
DW T_WORD
DB 66,89,84,69,0,0,0,0,0,0,3,4,0,0
DW T_BYTE
DB 66,85,70,70,69,82,0,0,0,0,3,4,0,0
DW T_BUFFER
```

### Edit 2

Unchanged source immediately before the edit:

```asm
T_LIT:
DB 77,79,86,32,65,88,44,35,13,10,0
```

Insert after old physical line 1109.

Insert:

```asm
T_WORD:
DB 85,95,64,58,13,10,68,87,32,35,13,10,0

T_BYTE:
DB 85,95,64,58,13,10,68,66,32,35,13,10,0

T_BUFFER:
DB 85,95,64,58,13,10,82,69,83,66,32,35,13,10,0
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

Remove this source at old physical positions 834–834 in IW05.ASM:

```asm
MOV CX,5
```

Replace it with:

```asm
MOV CX,8
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW06.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 03008 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW06.COM
```

VIEW.BAS must report IW06.COM length 3008 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW06.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
WORD X 0
BYTE Y 65
BUFFER B 300
LABEL MAIN
HALT
```

```dos
COPY TIW06.IR SOURCE.IR
```

```dos
CHECK IW06
```

Require:

```text
OK RESULT.ASM 0000000195 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00330 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 330 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 3B 01 E8 33 01 B4 4C CD 21 00 00 41 00 00 00 00 00 00 00 00 00 00 00 00
```

Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW06.IR:

```ir
UNKNOWN
```

```dos
COPY XIW06.IR SOURCE.IR
CHECK IW06
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
