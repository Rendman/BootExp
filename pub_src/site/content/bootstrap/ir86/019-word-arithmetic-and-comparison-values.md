+++
title = "19 \u00b7 Word arithmetic and comparison values"
weight = 19
description = "Define multiply, unsigned quotient/remainder, masked shifts, and zero-or-one relations."
download = "IR19.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/055-iw-word-arithmetic-and-comparison-values/", "/bootstrap/ir86/19-bounding-generated-source/"]
+++

The procedure machinery can carry values between calls. I want the word operations those routines will need for counts, masks, and character tests to have precise results too. This checkpoint completes the arithmetic and comparison set, including unsigned division and relations that produce exactly zero or one.

**Starting source:** `IR18.ASM`. **Save as:** `IR19.ASM`. **Build with:** `ASMAKEEP.COM`.

## How it works

Define multiply, unsigned quotient/remainder, masked shifts, and zero-or-one relations.

## Enter the source

Copy IR18.ASM to IR19.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1953

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

The following old source remains:

```asm

CMDCOUNT:
```

### Edit at old physical position 1765

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

### Edit at old physical position 1760

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

### Edit at old physical position 872

Unchanged source before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove:

```asm
MOV CX,42
```

Insert in its place:

```asm
MOV CX,51
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
CHECK ASMAKEEP IR19.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 09468 bytes`. Save RESULT.COM as IR19.COM. VIEW.BAS must show length 9468.

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
CHECK IR19 T19.IR RESULT.ASM
```

Require:

```text
OK RESULT.ASM 0000004204 text bytes
PASS
```

```dos
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 906 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 1D 02 E8 1F 02 81 F8 FF FF 75 03 E9 11 02 E8 04 00 B4 4C CD 21 55 8B EC
```

Copy it to TRY.COM. CHECK TRY reports PASS.

The fixture divides 65535 by 255 and checks for 257. It returns zero when the comparison agrees. The compiler's calculations can now rely on the language's unsigned word rules while the backend handles their native implementation.

## Check the new boundary

Save this separate rejected source as X19.IR:

```ir
UNKNOWN
```

```dos
CHECK IR19 X19.IR RESULT.ASM
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

