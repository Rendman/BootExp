+++
title = "12 \u00b7 Reading a declared byte"
weight = 12
description = "Zero-extend one byte from declared storage without a processor register in the source."
download = "IR12.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/048-iw-input-bytes-and-eof/", "/bootstrap/ir86/12-a-bounded-expression-stack/"]
+++

Zero-extend one byte from declared storage without a processor register in the source.

## Enter the source

Copy IR11.ASM to IR12.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1327

Unchanged source before the edit:

```asm
DW T_PUTC
DB 83,84,65,84,85,83,0,0,0,0,0,0,0,0
DW T_STATUS
```

Insert in its place:

```asm
DB 70,69,84,67,72,66,0,0,0,0,0,0,0,0
DW T_FETCHB
```

### Edit at old physical position 1202

Unchanged source before the edit:

```asm
DB "MOV AX,[BX]",13,10
DB 0
```

Insert in its place:

```asm
T_FETCHB:
DB "MOV BX,AX",13,10
DB "MOV AL,[BX]",13,10
DB "MOV AH,0",13,10
DB 0
```

The following old source remains:

```asm
T_PUSH:
DB "PUSH AX",13,10
```

### Edit at old physical position 866

Unchanged source before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove:

```asm
MOV CX,24
```

Insert in its place:

```asm
MOV CX,25
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR12.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 04066 bytes`. Save RESULT.COM as IR12.COM. VIEW.BAS must show length 4066.

Create T12.IR:

```ir
WORD X 65
LABEL MAIN
ADDR X
FETCHB
PUTC
LIT 0
EXIT
```

```dos
COPY T12.IR SOURCE.IR
```

```dos
CHECK IR12
```

Require:

```text
OK RESULT.ASM 0000000581 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 108 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 5D 00 E8 06 00 B4 4C CD 21 41 00 B8 11 01 8B D8 8A 07 B4 00 E8 1D 00 B8
```

Copy it to TRY.COM. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR12. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

