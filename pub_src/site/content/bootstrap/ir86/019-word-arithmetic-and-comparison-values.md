+++
title = "19 \u00b7 Word arithmetic and comparison values"
weight = 19
description = "Define multiply, unsigned quotient/remainder, masked shifts, and zero-or-one relations."
download = "IR19.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/055-iw-word-arithmetic-and-comparison-values/", "/bootstrap/ir86/19-bounding-generated-source/"]
+++

Define multiply, unsigned quotient/remainder, masked shifts, and zero-or-one relations.

## Enter the source

Copy IR18.ASM to IR19.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1659

Unchanged source before the edit:

```asm
DW T_MUL
DB 67,65,76,76,0,0,0,0,0,0,2,0,0,0
DW T_CALL
```

Insert in its place:

```asm
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
```

### Edit at old physical position 1483

Unchanged source before the edit:

```asm
DB "CMP BX,AX",13,10
DB "MOV AX,0",13,10
DB "JNE $+3",13,10
```

Insert in its place:

```asm
DB "INC AX",13,10
DB 0

T_CNE:
DB "POP BX",13,10
DB "CMP BX,AX",13,10
DB "MOV AX,0",13,10
DB "JE $+3",13,10
DB "INC AX",13,10
DB 0

T_CULT:
DB "POP BX",13,10
DB "CMP BX,AX",13,10
DB "MOV AX,0",13,10
DB "JAE $+3",13,10
DB "INC AX",13,10
DB 0

T_CULE:
DB "POP BX",13,10
DB "CMP BX,AX",13,10
DB "MOV AX,0",13,10
DB "JA $+3",13,10
DB "INC AX",13,10
DB 0

T_CUGT:
DB "POP BX",13,10
DB "CMP BX,AX",13,10
DB "MOV AX,0",13,10
DB "JBE $+3",13,10
DB "INC AX",13,10
DB 0

T_CUGE:
DB "POP BX",13,10
DB "CMP BX,AX",13,10
DB "MOV AX,0",13,10
DB "JB $+3",13,10
```

The following old source remains:

```asm
DB "INC AX",13,10
DB 0
```

### Edit at old physical position 1478

Unchanged source before the edit:

```asm
DB "MUL BX",13,10
DB 0
```

Insert in its place:

```asm
T_DIV:
DB "MOV BX,AX",13,10
DB "POP AX",13,10
DB "CMP BX,0",13,10
DB "JE NEAR R_STACKFAIL",13,10
DB "XOR DX,DX",13,10
DB "DIV BX",13,10
DB 0

T_MOD:
DB "MOV BX,AX",13,10
DB "POP AX",13,10
DB "CMP BX,0",13,10
DB "JE NEAR R_STACKFAIL",13,10
DB "XOR DX,DX",13,10
DB "DIV BX",13,10
DB "MOV AX,DX",13,10
DB 0

T_SHL:
DB "MOV CX,AX",13,10
DB "AND CX,15",13,10
DB "POP AX",13,10
DB "SHL AX,CL",13,10
DB 0

T_SHR:
DB "MOV CX,AX",13,10
DB "AND CX,15",13,10
DB "POP AX",13,10
DB "SHR AX,CL",13,10
DB 0
```

The following old source remains:

```asm
T_CEQ:
DB "POP BX",13,10
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
MOV CX,40
```

Insert in its place:

```asm
MOV CX,49
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR19.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 07420 bytes`. Save RESULT.COM as IR19.COM. VIEW.BAS must show length 7420.

Create T19.IR:

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
COPY T19.IR SOURCE.IR
```

```dos
CHECK IR19
```

Require:

```text
OK RESULT.ASM 0000002708 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 544 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 11 02 E8 04 00 B4 4C CD 21 55 8B EC 81 EC 00 00 81 FC 00 F0 73 03 E9 FA
```

Copy it to TRY.COM. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR19. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

