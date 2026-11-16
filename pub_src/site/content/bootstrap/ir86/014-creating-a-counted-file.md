+++
title = "14 \u00b7 Creating a counted file"
weight = 14
description = "Create writable handles through the same opaque slot table."
download = "IR14.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/050-iw-creating-a-counted-file/", "/bootstrap/ir86/14-word-sized-bit-operations/"]
+++

Create writable handles through the same opaque slot table.

## Enter the source

Copy IR13.ASM to IR14.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1693

Unchanged source before the edit:

```asm
DW T_ARGC
DB 65,82,71,0,0,0,0,0,0,0,0,0,0,0
DW T_ARG
```

Insert in its place:

```asm
DB 67,82,69,65,84,69,0,0,0,0,0,0,0,0
DW T_CREATE
```

The following old source remains:

```asm

CMDCOUNT:
```

### Edit at old physical position 1624

Unchanged source before the edit:

```asm
DB "CALL R_OPEN",13,10
DB 0
```

Insert in its place:

```asm
T_CREATE:
DB "CALL R_CREATE",13,10
DB 0
```

The following old source remains:

```asm
T_ARGC:
DB "CALL R_ARGC",13,10
```

### Edit at old physical position 1321

Unchanged source before the edit:

```asm
DB "MOV DX,3D00H",13,10
DB "JMP R_FILE",13,10
DB 13,10
```

Insert in its place:

```asm
DB "R_CREATE:",13,10
DB "MOV DX,3C00H",13,10
DB "JMP R_FILE",13,10
DB 13,10
```

The following old source remains:

```asm
DB "R_FILE:",13,10
DB "MOV [R_MODE],DX",13,10
```

### Edit at old physical position 872

Unchanged source before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove:

```asm
MOV CX,28
```

Insert in its place:

```asm
MOV CX,29
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
CHECK ASMAKEEP IR14.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 06919 bytes`. Save RESULT.COM as IR14.COM. VIEW.BAS must show length 6919.

Create T14.IR:

```ir
WORD NAME 65
LABEL MAIN
ADDR NAME
CREATE
STATUS
JZ GOOD
LIT 1
EXIT
LABEL GOOD
LIT 0
EXIT
```

```dos
CHECK IR14 T14.IR RESULT.ASM
```

Require:

```text
OK RESULT.ASM 0000002888 text bytes
PASS
```

```dos
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 639 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 12 01 E8 14 01 81 F8 FF FF 75 03 E9 06 01 E8 06 00 B4 4C CD 21 41 00 B8
```

Copy it to TRY.COM. CHECK TRY reports PASS.

## Check the new boundary

Save this separate rejected source as X14.IR:

```ir
UNKNOWN
```

```dos
CHECK IR14 X14.IR RESULT.ASM
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

