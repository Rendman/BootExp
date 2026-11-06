+++
title = "IW12 \u00b7 Input bytes and EOF"
weight = 48
description = "Distinguish every byte from EOF without exposing a native status flag."
download = "IW12.ASM"
download_group = "toolchain"
+++

Distinguish every byte from EOF without exposing a native status flag.

## The working parts

Distinguish every byte from EOF without exposing a native status flag. The assembly routines use the inherited bounded reader and owned-file cleanup. The operation table supplies argument class, stack action, and an authored target template. Native encodings belong to this backend; the IR operation retains its abstract meaning.

## Enter the source

Copy IW11.ASM to IW12.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_PUTC
DB 83,84,65,84,85,83,0,0,0,0,0,0,0,0
DW T_STATUS
```

Insert after old physical line 1356.

Insert:

```asm
DB 71,69,84,67,0,0,0,0,0,0,0,0,0,0
DW T_GETC
```

### Edit 2

Unchanged source immediately before the edit:

```asm
T_PUTC:
DB 67,65,76,76,32,82,95,80,85,84,67,13,10,0
```

Insert after old physical line 1269.

Insert:

```asm
T_GETC:
DB 67,65,76,76,32,82,95,71,69,84,67,13,10,0
```

The following old source remains in place:

```asm
T_STATUS:
DB 77,79,86,32,65,88,44,91,82,95,83,84,65,84,85,83
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DB 10,74,69,32,78,69,65,82,32,82,95,80,85,84,71,79
DB 79,68,13,10,74,77,80,32,82,95,69,82,82,79,82,13
DB 10,82,95,80,85,84,71,79,79,68,58,13,10,74,77,80
```

Remove this source at old physical positions 1108–1113 in IW11.ASM:

```asm
DB 32,82,95,79,75,13,10,13,10,82,95,83,84,65,84,85
DB 83,58,13,10,68,87,32,48,13,10,13,10,82,95,66,89
DB 84,69,58,13,10,68,66,32,48,13,10,13,10,82,95,83
DB 84,65,67,75,70,65,73,76,58,13,10,77,79,86,32,65
DB 88,44,52,67,48,50,72,13,10,73,78,84,32,50,49,72
DB 13,10,0
```

Replace it with:

```asm
DB 32,82,95,79,75,13,10,13,10,82,95,71,69,84,67,58
DB 13,10,77,79,86,32,66,88,44,48,13,10,77,79,86,32
DB 67,88,44,49,13,10,77,79,86,32,68,88,44,82,95,66
DB 89,84,69,13,10,77,79,86,32,65,72,44,51,70,72,13
DB 10,73,78,84,32,50,49,72,13,10,74,65,69,32,78,69
DB 65,82,32,82,95,71,69,84,67,79,85,78,84,13,10,77
DB 79,86,32,65,88,44,54,53,53,51,53,13,10,74,77,80
DB 32,82,95,69,82,82,79,82,13,10,82,95,71,69,84,67
DB 79,85,78,84,58,13,10,67,77,80,32,65,88,44,48,13
DB 10,74,78,69,32,78,69,65,82,32,82,95,71,69,84,66
DB 89,84,69,13,10,77,79,86,32,65,88,44,54,53,53,51
DB 53,13,10,74,77,80,32,82,95,79,75,13,10,82,95,71
DB 69,84,66,89,84,69,58,13,10,77,79,86,32,65,76,44
DB 91,82,95,66,89,84,69,93,13,10,77,79,86,32,65,72
DB 44,48,13,10,74,77,80,32,82,95,79,75,13,10,13,10
DB 82,95,83,84,65,84,85,83,58,13,10,68,87,32,48,13
DB 10,13,10,82,95,66,89,84,69,58,13,10,68,66,32,48
DB 13,10,13,10,82,95,83,84,65,67,75,70,65,73,76,58
DB 13,10,77,79,86,32,65,88,44,52,67,48,50,72,13,10
DB 73,78,84,32,50,49,72,13,10,0
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

Remove this source at old physical positions 834–834 in IW11.ASM:

```asm
MOV CX,41
```

Replace it with:

```asm
MOV CX,42
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW12.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 04955 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW12.COM
```

VIEW.BAS must report IW12.COM length 4955 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW12.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
LABEL MAIN
GETC
PUTC
HALT
```

```dos
COPY TIW12.IR SOURCE.IR
```

```dos
CHECK IW12
```

Require, apart from command echo and the checker's separator:

```text
OK RESULT.ASM 0000000751 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00146 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 146 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 83 00 E8 04 00 B4 4C CD 21 E8 46 00 E8 1B 00 B8 00 4C CD 21 BA 00 00 89
```

Create KEY.TXT with `ECHO A>KEY.TXT` and run CHECK TRY <KEY.TXT. It displays `A` and reports PASS.

## A rejection or boundary check

Create XIW12.IR:

```ir
UNKNOWN
```

```dos
COPY XIW12.IR SOURCE.IR
CHECK IW12
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
