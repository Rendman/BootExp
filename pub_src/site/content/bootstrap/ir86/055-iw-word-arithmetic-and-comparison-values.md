+++
title = "IW19 \u00b7 Word arithmetic and comparison values"
weight = 55
description = "Define multiply, unsigned quotient/remainder, masked shifts, and zero-or-one relations."
download = "IW19.ASM"
download_group = "toolchain"
+++

Define multiply, unsigned quotient/remainder, masked shifts, and zero-or-one relations.

## The working parts

Define multiply, unsigned quotient/remainder, masked shifts, and zero-or-one relations. The assembly routines use the inherited bounded reader and owned-file cleanup. The operation table supplies argument class, stack action, and an authored target template. Native encodings belong to this backend; the IR operation retains its abstract meaning.

## Enter the source

Copy IW18.ASM to IW19.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_MUL
DB 67,69,81,0,0,0,0,0,0,0,0,2,0,0
DW T_CEQ
```

Insert after old physical line 1655.

Insert:

```asm
DB 78,69,71,0,0,0,0,0,0,0,0,0,0,0
DW T_NEG
DB 78,79,84,0,0,0,0,0,0,0,0,0,0,0
DW T_NOT
DB 68,73,86,0,0,0,0,0,0,0,0,2,0,0
DW T_DIV
DB 77,79,68,0,0,0,0,0,0,0,0,2,0,0
DW T_MOD
DB 83,72,76,0,0,0,0,0,0,0,0,2,0,0
DW T_SHL
DB 83,72,82,0,0,0,0,0,0,0,0,2,0,0
DW T_SHR
DB 67,78,69,0,0,0,0,0,0,0,0,2,0,0
DW T_CNE
DB 67,85,76,84,0,0,0,0,0,0,0,2,0,0
DW T_CULT
DB 67,85,76,69,0,0,0,0,0,0,0,2,0,0
DW T_CULE
DB 67,85,71,84,0,0,0,0,0,0,0,2,0,0
DW T_CUGT
DB 67,85,71,69,0,0,0,0,0,0,0,2,0,0
DW T_CUGE
DB 67,83,76,84,0,0,0,0,0,0,0,2,0,0
DW T_CSLT
DB 67,83,76,69,0,0,0,0,0,0,0,2,0,0
DW T_CSLE
DB 67,83,71,84,0,0,0,0,0,0,0,2,0,0
DW T_CSGT
DB 67,83,71,69,0,0,0,0,0,0,0,2,0,0
DW T_CSGE
```

### Edit 2

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,76,32,36,43,53,13,10,74,77,80,32,85
DB 95,64,13,10,0
```

Insert after old physical line 1460.

Insert:

```asm

T_CSGE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,48,13,10,74,76,32
DB 36,43,51,13,10,73,78,67,32,65,88,13,10,0
```

The following old source remains in place:

```asm

T_JZ:
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DB 88,13,10,74,76,69,32,36,43,53,13,10,74,77,80,32
DB 85,95,64,13,10,0
```

Insert after old physical line 1456.

Insert:

```asm
T_CSGT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,48,13,10,74,76,69
DB 32,36,43,51,13,10,73,78,67,32,65,88,13,10,0
```

The following old source remains in place:

```asm
T_SGE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
```

### Edit 4

Unchanged source immediately before the edit:

```asm
DB 88,13,10,74,71,32,36,43,53,13,10,74,77,80,32,85
DB 95,64,13,10,0
```

Insert after old physical line 1451.

Insert:

```asm
T_CSLE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,48,13,10,74,71,32
DB 36,43,51,13,10,73,78,67,32,65,88,13,10,0
```

The following old source remains in place:

```asm
T_SGT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
```

### Edit 5

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,71,69,32,36,43,53,13,10,74,77,80,32
DB 85,95,64,13,10,0
```

Insert after old physical line 1445.

Insert:

```asm

T_CSLT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,48,13,10,74,71,69
DB 32,36,43,51,13,10,73,78,67,32,65,88,13,10,0
```

The following old source remains in place:

```asm

T_SLE:
```

### Edit 6

Unchanged source immediately before the edit:

```asm
DB 88,13,10,74,66,32,36,43,53,13,10,74,77,80,32,85
DB 95,64,13,10,0
```

Insert after old physical line 1441.

Insert:

```asm
T_CUGE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,48,13,10,74,66,32
DB 36,43,51,13,10,73,78,67,32,65,88,13,10,0
```

The following old source remains in place:

```asm
T_SLT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
```

### Edit 7

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,66,69,32,36,43,53,13,10,74,77,80,32
DB 85,95,64,13,10,0
```

Insert after old physical line 1435.

Insert:

```asm

T_CUGT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,48,13,10,74,66,69
DB 32,36,43,51,13,10,73,78,67,32,65,88,13,10,0
```

The following old source remains in place:

```asm

T_UGE:
```

### Edit 8

Unchanged source immediately before the edit:

```asm
DB 88,13,10,74,65,32,36,43,53,13,10,74,77,80,32,85
DB 95,64,13,10,0
```

Insert after old physical line 1431.

Insert:

```asm
T_CULE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,48,13,10,74,65,32
DB 36,43,51,13,10,73,78,67,32,65,88,13,10,0
```

The following old source remains in place:

```asm
T_UGT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
```

### Edit 9

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,65,69,32,36,43,53,13,10,74,77,80,32
DB 85,95,64,13,10,0
```

Insert after old physical line 1425.

Insert:

```asm

T_CULT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,48,13,10,74,65,69
DB 32,36,43,51,13,10,73,78,67,32,65,88,13,10,0
```

The following old source remains in place:

```asm

T_ULE:
```

### Edit 10

Unchanged source immediately before the edit:

```asm
DB 88,13,10,74,69,32,36,43,53,13,10,74,77,80,32,85
DB 95,64,13,10,0
```

Insert after old physical line 1421.

Insert:

```asm
T_CNE:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,48,13,10,74,69,32
DB 36,43,51,13,10,73,78,67,32,65,88,13,10,0
```

The following old source remains in place:

```asm
T_ULT:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
```

### Edit 11

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,66,88,13,10,77,85,76,32,66,88,13,10
DB 0
```

Insert after old physical line 1406.

Insert:

```asm
T_DIV:
DB 77,79,86,32,66,88,44,65,88,13,10,80,79,80,32,65
DB 88,13,10,67,77,80,32,66,88,44,48,13,10,74,69,32
DB 78,69,65,82,32,82,95,83,84,65,67,75,70,65,73,76
DB 13,10,88,79,82,32,68,88,44,68,88,13,10,68,73,86
DB 32,66,88,13,10,0

T_MOD:
DB 77,79,86,32,66,88,44,65,88,13,10,80,79,80,32,65
DB 88,13,10,67,77,80,32,66,88,44,48,13,10,74,69,32
DB 78,69,65,82,32,82,95,83,84,65,67,75,70,65,73,76
DB 13,10,88,79,82,32,68,88,44,68,88,13,10,68,73,86
DB 32,66,88,13,10,77,79,86,32,65,88,44,68,88,13,10
DB 0

T_SHL:
DB 77,79,86,32,67,88,44,65,88,13,10,65,78,68,32,67
DB 88,44,49,53,13,10,80,79,80,32,65,88,13,10,83,72
DB 76,32,65,88,44,67,76,13,10,0

T_SHR:
DB 77,79,86,32,67,88,44,65,88,13,10,65,78,68,32,67
DB 88,44,49,53,13,10,80,79,80,32,65,88,13,10,83,72
DB 82,32,65,88,44,67,76,13,10,0
```

The following old source remains in place:

```asm
T_EQ:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
```

### Edit 12

Unchanged source immediately before the edit:

```asm
DB 76,44,91,66,88,93,13,10,77,79,86,32,65,72,44,48
DB 13,10,0
```

Insert after old physical line 1368.

Insert:

```asm
T_NEG:
DB 78,69,71,32,65,88,13,10,0

T_NOT:
DB 78,79,84,32,65,88,13,10,0
```

The following old source remains in place:

```asm
T_PUSH:
DB 80,85,83,72,32,65,88,13,10,0
```

### Edit 13

Unchanged source immediately before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove this source at old physical positions 834–834 in IW18.ASM:

```asm
MOV CX,58
```

Replace it with:

```asm
MOV CX,73
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW19.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 08686 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW19.COM
```

VIEW.BAS must report IW19.COM length 8686 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW19.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
PROC MAIN 0 0
LIT 65535
PUSH
LIT 255
DIV
PUSH
LIT 257
CNE
RETURN
```

```dos
COPY TIW19.IR SOURCE.IR
```

```dos
CHECK IW19
```

Require, apart from command echo and the checker's separator:

```text
OK RESULT.ASM 0000002939 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00592 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 592 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 41 02 E8 04 00 B4 4C CD 21 55 8B EC 81 EC 00 00 81 FC 00 F0 73 03 E9 2A
```

Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW19.IR:

```ir
UNKNOWN
```

```dos
COPY XIW19.IR SOURCE.IR
CHECK IW19
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
