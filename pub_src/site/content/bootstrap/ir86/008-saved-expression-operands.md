+++
title = "08 \u00b7 Saved expression operands"
weight = 8
description = "Check push/pop depth and apply word arithmetic before a control boundary."
download = "IR08.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/044-iw-saved-expression-operands/", "/bootstrap/ir86/08-loading-an-unsigned-word/"]
+++

Check push/pop depth and apply word arithmetic before a control boundary.

## Enter the source

Copy IR07.ASM to IR08.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1187

Unchanged source before the edit:

```asm
DW T_ADDR
DB 70,69,84,67,72,0,0,0,0,0,0,0,0,0
DW T_FETCH
```

Insert in its place:

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
```

### Edit at old physical position 1168

Unchanged source before the edit:

```asm
DB "MOV AX,[BX]",13,10
DB 0
```

Insert in its place:

```asm
T_PUSH:
DB "PUSH AX",13,10
DB 0

T_POP:
DB "POP AX",13,10
DB 0

T_ADD:
DB "POP BX",13,10
DB "ADD AX,BX",13,10
DB 0

T_AND:
DB "POP BX",13,10
DB "AND AX,BX",13,10
DB 0

T_OR:
DB "POP BX",13,10
DB "OR AX,BX",13,10
DB 0

T_XOR:
DB "POP BX",13,10
DB "XOR AX,BX",13,10
DB 0

T_SUB:
DB "POP BX",13,10
DB "SUB BX,AX",13,10
DB "MOV AX,BX",13,10
DB 0
```

The following old source remains:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
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
MOV CX,9
```

Insert in its place:

```asm
MOV CX,16
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR08.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 03346 bytes`. Save RESULT.COM as IR08.COM. VIEW.BAS must show length 3346.

Create T08.IR:

```ir
LABEL MAIN
LIT 7
PUSH
LIT 7
SUB
EXIT
```

```dos
COPY T08.IR SOURCE.IR
```

```dos
CHECK IR08
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

Require OK and PASS. VIEW.BAS must show RESULT.COM length 38 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 17 00 E8 04 00 B4 4C CD 21 B8 07 00 50 B8 07 00 5B 2B D8 8B C3 B4 4C CD
```

Copy it to TRY.COM. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR08. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

