+++
title = "IW21 \u00b7 File publication services"
weight = 57
description = "Normalize existence, deletion, and rename without exposing DOS error values."
download = "IW21.ASM"
download_group = "toolchain"
+++

Normalize existence, deletion, and rename without exposing DOS error values.

## The working parts

Normalize existence, deletion, and rename without exposing DOS error values. The assembly routines use the inherited bounded reader and owned-file cleanup. The operation table supplies argument class, stack action, and an authored target template. Native encodings belong to this backend; the IR operation retains its abstract meaning.

## Enter the source

Copy IW20.ASM to IW21.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_CSGE
DB 76,73,84,83,0,0,0,0,0,0,6,0,0,0
DW T_LITS
```

Insert after old physical line 1843.

Insert:

```asm
DB 69,88,73,83,84,83,0,0,0,0,0,0,0,0
DW T_EXISTS
DB 68,69,76,69,84,69,0,0,0,0,0,0,0,0
DW T_DELETE
DB 82,69,78,65,77,69,0,0,0,0,0,2,0,0
DW T_RENAME
```

### Edit 2

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,68,88,13,10,80,79,80,32,66,88,13,10
DB 67,65,76,76,32,82,95,87,82,73,84,69,13,10,0
```

Insert after old physical line 1694.

Insert:

```asm
T_DELETE:
DB 67,65,76,76,32,82,95,68,69,76,69,84,69,13,10,0

T_EXISTS:
DB 67,65,76,76,32,82,95,69,88,73,83,84,83,13,10,0

T_RENAME:
DB 80,79,80,32,68,88,13,10,67,65,76,76,32,82,95,82
DB 69,78,65,77,69,13,10,0
```

The following old source remains in place:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DB 44,48,44,48,44,48,44,48,44,48,44,48,44,48,13,10
DB 13,10,82,95,67,79,85,78,84,58,13,10,68,87,32,48
DB 13,10,82,95,66,85,70,70,69,82,58,13,10,68,87,32
```

Remove this source at old physical positions 1384–1386 in IW20.ASM:

```asm
DB 48,13,10,13,10,82,95,83,84,65,67,75,70,65,73,76
DB 58,13,10,77,79,86,32,65,88,44,52,67,48,50,72,13
DB 10,73,78,84,32,50,49,72,13,10,0
```

Replace it with:

```asm
DB 48,13,10,13,10,59,32,65,117,116,104,111,114,101,100,32
DB 112,111,114,116,97,98,108,101,45,115,101,114,118,105,99,101
DB 115,32,98,105,110,100,105,110,103,46,32,78,111,32,112,104
DB 121,115,105,99,97,108,32,118,97,108,117,101,115,32,101,115
DB 99,97,112,101,32,116,104,105,115,32,108,97,121,101,114,46
DB 13,10,82,95,68,69,76,69,84,69,58,13,10,77,79,86
DB 32,68,88,44,65,88,13,10,77,79,86,32,65,72,44,52
DB 49,72,13,10,73,78,84,32,50,49,72,13,10,74,67,32
DB 78,69,65,82,32,82,95,68,70,65,73,76,13,10,77,79
DB 86,32,65,88,44,48,13,10,74,77,80,32,82,95,79,75
DB 13,10,82,95,68,70,65,73,76,58,13,10,74,77,80,32
DB 82,95,70,65,73,76,13,10,82,95,82,69,78,65,77,69
DB 58,13,10,77,79,86,32,68,73,44,65,88,13,10,77,79
DB 86,32,65,88,44,68,83,13,10,77,79,86,32,69,83,44
DB 65,88,13,10,77,79,86,32,65,72,44,53,54,72,13,10
DB 73,78,84,32,50,49,72,13,10,74,67,32,78,69,65,82
DB 32,82,95,68,70,65,73,76,13,10,77,79,86,32,65,88
DB 44,48,13,10,74,77,80,32,82,95,79,75,13,10,82,95
DB 69,88,73,83,84,83,58,13,10,77,79,86,32,68,88,44
DB 65,88,13,10,77,79,86,32,65,88,44,51,68,48,48,72
DB 13,10,73,78,84,32,50,49,72,13,10,74,67,32,78,69
DB 65,82,32,82,95,78,79,70,73,76,69,13,10,77,79,86
DB 32,66,88,44,65,88,13,10,77,79,86,32,65,72,44,51
DB 69,72,13,10,73,78,84,32,50,49,72,13,10,74,67,32
DB 78,69,65,82,32,82,95,68,70,65,73,76,13,10,77,79
DB 86,32,65,88,44,49,13,10,74,77,80,32,82,95,79,75
DB 13,10,82,95,78,79,70,73,76,69,58,13,10,67,77,80
DB 32,65,88,44,50,13,10,74,78,69,32,78,69,65,82,32
DB 82,95,69,70,65,73,76,13,10,77,79,86,32,65,88,44
DB 48,13,10,74,77,80,32,82,95,79,75,13,10,82,95,69
DB 70,65,73,76,58,13,10,77,79,86,32,65,88,44,54,53
DB 53,51,53,13,10,74,77,80,32,82,95,69,82,82,79,82
DB 13,10,13,10,82,95,83,84,65,67,75,70,65,73,76,58
DB 13,10,77,79,86,32,65,88,44,52,67,48,50,72,13,10
DB 73,78,84,32,50,49,72,13,10,0
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

Remove this source at old physical positions 834–834 in IW20.ASM:

```asm
MOV CX,74
```

Replace it with:

```asm
MOV CX,77
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW21.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 09547 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW21.COM
```

VIEW.BAS must report IW21.COM length 9547 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW21.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
PROC MAIN 0 0
LITS "A"
EXISTS
PUSH
LIT 1
CNE
RETURN
```

```dos
COPY TIW21.IR SOURCE.IR
```

```dos
CHECK IW21
```

Require, apart from command echo and the checker's separator:

```text
OK RESULT.ASM 0000003424 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00671 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 671 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 90 02 E8 04 00 B4 4C CD 21 55 8B EC 81 EC 00 00 81 FC 00 F0 73 03 E9 79
```

First create the ordinary input file A with `ECHO A>A`. Its declared filename is the word 65 followed by its zero high byte. Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW21.IR:

```ir
UNKNOWN
```

```dos
COPY XIW21.IR SOURCE.IR
CHECK IW21
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
