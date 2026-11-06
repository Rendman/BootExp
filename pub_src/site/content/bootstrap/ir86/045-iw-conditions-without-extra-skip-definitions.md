+++
title = "IW09 \u00b7 Conditions without extra skip definitions"
weight = 45
description = "Use fixed native conditional bridges while keeping branch semantics in the virtual machine."
download = "IW09.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Use fixed native conditional bridges while keeping branch semantics in the virtual machine.

## Enter the source

Copy IW08.ASM to IW09.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_PUT
DB 80,85,84,66,0,0,0,0,0,0,0,2,0,0
DW T_PUTB
```

Insert after old physical line 1226.

Insert:

```asm
DB 74,77,80,0,0,0,0,0,0,0,2,4,0,0
DW T_JMP
DB 74,90,0,0,0,0,0,0,0,0,2,4,0,0
DW T_JZ
DB 74,78,90,0,0,0,0,0,0,0,2,4,0,0
DW T_JNZ
DB 69,81,0,0,0,0,0,0,0,0,2,2,0,0
DW T_EQ
DB 78,69,0,0,0,0,0,0,0,0,2,2,0,0
DW T_NE
DB 85,76,84,0,0,0,0,0,0,0,2,2,0,0
DW T_ULT
DB 85,76,69,0,0,0,0,0,0,0,2,2,0,0
DW T_ULE
DB 85,71,84,0,0,0,0,0,0,0,2,2,0,0
DW T_UGT
DB 85,71,69,0,0,0,0,0,0,0,2,2,0,0
DW T_UGE
DB 83,76,84,0,0,0,0,0,0,0,2,2,0,0
DW T_SLT
DB 83,76,69,0,0,0,0,0,0,0,2,2,0,0
DW T_SLE
DB 83,71,84,0,0,0,0,0,0,0,2,2,0,0
DW T_SGT
DB 83,71,69,0,0,0,0,0,0,0,2,2,0,0
DW T_SGE
```

### Edit 2

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,66,88,13,10,83,85,66,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,66,88,13,10,0
```

Insert after old physical line 1177.

Insert:

```asm
T_EQ:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,78,69,32,36,43,53,13,10,74,77,80,32
DB 85,95,64,13,10,0

T_NE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,69,32,36,43,53,13,10,74,77,80,32,85
DB 95,64,13,10,0

T_ULT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,65,69,32,36,43,53,13,10,74,77,80,32
DB 85,95,64,13,10,0

T_ULE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,65,32,36,43,53,13,10,74,77,80,32,85
DB 95,64,13,10,0

T_UGT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,66,69,32,36,43,53,13,10,74,77,80,32
DB 85,95,64,13,10,0

T_UGE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,66,32,36,43,53,13,10,74,77,80,32,85
DB 95,64,13,10,0

T_SLT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,71,69,32,36,43,53,13,10,74,77,80,32
DB 85,95,64,13,10,0

T_SLE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,71,32,36,43,53,13,10,74,77,80,32,85
DB 95,64,13,10,0

T_SGT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,76,69,32,36,43,53,13,10,74,77,80,32
DB 85,95,64,13,10,0

T_SGE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,76,32,36,43,53,13,10,74,77,80,32,85
DB 95,64,13,10,0

T_JZ:
DB 67,77,80,32,65,88,44,48,13,10,74,78,69,32,36,43
DB 53,13,10,74,77,80,32,85,95,64,13,10,0

T_JNZ:
DB 67,77,80,32,65,88,44,48,13,10,74,69,32,36,43,53
DB 13,10,74,77,80,32,85,95,64,13,10,0

T_JMP:
DB 74,77,80,32,85,95,64,13,10,0
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

Remove this source at old physical positions 834–834 in IW08.ASM:

```asm
MOV CX,24
```

Replace it with:

```asm
MOV CX,37
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW09.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 04230 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW09.COM
```

VIEW.BAS must report IW09.COM length 4230 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW09.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
LABEL MAIN
LIT 7
PUSH
LIT 7
EQ GOOD
LIT 1
EXIT
LABEL GOOD
HALT
```

```dos
COPY TIW09.IR SOURCE.IR
```

```dos
CHECK IW09
```

Require:

```text
OK RESULT.ASM 0000000266 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00049 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 49 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 22 00 E8 04 00 B4 4C CD 21 B8 07 00 50 B8 07 00 5B 3B D8 75 03 E9 07 00
```

Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW09.IR:

```ir
UNKNOWN
```

```dos
COPY XIW09.IR SOURCE.IR
CHECK IW09
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
