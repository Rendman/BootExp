+++
title = "IW17 \u00b7 Closing a handle"
weight = 53
description = "Retire an owned handle only after a successful close."
download = "IW17.ASM"
download_group = "toolchain"
+++

Retire an owned handle only after a successful close.

## The working parts

Retire an owned handle only after a successful close. The assembly routines use the inherited bounded reader and owned-file cleanup. The operation table supplies argument class, stack action, and an authored target template. Native encodings belong to this backend; the IR operation retains its abstract meaning.

## Enter the source

Copy IW16.ASM to IW17.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_READ
DB 87,82,73,84,69,0,0,0,0,0,0,3,0,0
DW T_WRITE
```

Insert after old physical line 1507.

Insert:

```asm
DB 67,76,79,83,69,0,0,0,0,0,0,0,0,0
DW T_CLOSE
```

### Edit 2

Unchanged source immediately before the edit:

```asm
T_CREATE:
DB 67,65,76,76,32,82,95,67,82,69,65,84,69,13,10,0
```

Insert after old physical line 1402.

Insert:

```asm
T_CLOSE:
DB 67,65,76,76,32,82,95,67,76,79,83,69,13,10,0
```

The following old source remains in place:

```asm
T_STATUS:
DB 77,79,86,32,65,88,44,91,82,95,83,84,65,84,85,83
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DB 65,82,32,82,95,87,82,73,84,69,71,79,79,68,13,10
DB 74,77,80,32,82,95,69,82,82,79,82,13,10,82,95,87
DB 82,73,84,69,71,79,79,68,58,13,10,74,77,80,32,82
```

Remove this source at old physical positions 1224–1237 in IW16.ASM:

```asm
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

Replace it with:

```asm
DB 95,79,75,13,10,13,10,82,95,67,76,79,83,69,58,13
DB 10,77,79,86,32,66,88,44,65,88,13,10,67,65,76,76
DB 32,82,95,70,73,78,68,13,10,67,77,80,32,65,88,44
DB 48,13,10,74,78,69,32,78,69,65,82,32,82,95,67,76
DB 79,83,69,86,65,76,73,68,13,10,74,77,80,32,82,95
DB 70,65,73,76,13,10,82,95,67,76,79,83,69,86,65,76
DB 73,68,58,13,10,77,79,86,32,65,72,44,51,69,72,13
DB 10,73,78,84,32,50,49,72,13,10,74,65,69,32,78,69
DB 65,82,32,82,95,67,76,79,83,69,71,79,79,68,13,10
DB 74,77,80,32,82,95,70,65,73,76,13,10,82,95,67,76
DB 79,83,69,71,79,79,68,58,13,10,77,79,86,32,66,88
DB 44,91,82,95,83,76,79,84,93,13,10,77,79,86,32,65
DB 88,44,48,13,10,77,79,86,32,91,66,88,93,44,65,88
DB 13,10,74,77,80,32,82,95,79,75,13,10,13,10,82,95
DB 83,84,65,84,85,83,58,13,10,68,87,32,48,13,10,13
DB 10,82,95,66,89,84,69,58,13,10,68,66,32,48,13,10
DB 13,10,82,95,77,79,68,69,58,13,10,68,87,32,48,13
DB 10,82,95,78,65,77,69,58,13,10,68,87,32,48,13,10
DB 82,95,83,76,79,84,58,13,10,68,87,32,48,13,10,82
DB 95,78,85,77,66,69,82,58,13,10,68,87,32,48,13,10
DB 82,95,72,65,78,68,76,69,83,58,13,10,68,87,32,48
DB 44,48,44,48,44,48,44,48,44,48,44,48,44,48,13,10
DB 13,10,82,95,67,79,85,78,84,58,13,10,68,87,32,48
DB 13,10,82,95,66,85,70,70,69,82,58,13,10,68,87,32
DB 48,13,10,13,10,82,95,83,84,65,67,75,70,65,73,76
DB 58,13,10,77,79,86,32,65,88,44,52,67,48,50,72,13
DB 10,73,78,84,32,50,49,72,13,10,0
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

Remove this source at old physical positions 834–834 in IW16.ASM:

```asm
MOV CX,46
```

Replace it with:

```asm
MOV CX,47
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW17.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 07110 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW17.COM
```

VIEW.BAS must report IW17.COM length 7110 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW17.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
WORD NAME 65
LABEL MAIN
ADDR NAME
OPEN
CLOSE
STATUS
EXIT
```

```dos
COPY TIW17.IR SOURCE.IR
```

```dos
CHECK IW17
```

Require, apart from command echo and the checker's separator:

```text
OK RESULT.ASM 0000002772 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00555 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 555 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 1C 02 E8 06 00 B4 4C CD 21 41 00 B8 11 01 E8 79 00 E8 C2 01 8B 06 07 03
```

First create the ordinary input file A with `ECHO A>A`. Its declared filename is the word 65 followed by its zero high byte. Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW17.IR:

```ir
UNKNOWN
```

```dos
COPY XIW17.IR SOURCE.IR
CHECK IW17
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
