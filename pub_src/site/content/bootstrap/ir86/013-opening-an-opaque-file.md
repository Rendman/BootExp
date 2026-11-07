+++
title = "13 \u00b7 Opening an opaque file"
weight = 13
description = "Give OPEN an ordinary terminated filename and return a checked handle."
download = "IR13.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/049-iw-opening-an-opaque-file/", "/bootstrap/ir86/13-adding-and-subtracting/"]
+++

Give OPEN an ordinary terminated filename and return a checked handle.

## Enter the source

Copy IR12.ASM to IR13.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1335

Unchanged source before the edit:

```asm
DW T_STATUS
DB 70,69,84,67,72,66,0,0,0,0,0,0,0,0
DW T_FETCHB
```

Insert in its place:

```asm
DB 79,80,69,78,0,0,0,0,0,0,0,0,0,0
DW T_OPEN
```

### Edit at old physical position 1280

Unchanged source before the edit:

```asm
DB "CALL R_PUTC",13,10
DB 0
```

Insert in its place:

```asm
T_OPEN:
DB "CALL R_OPEN",13,10
DB 0
```

The following old source remains:

```asm
T_STATUS:
DB "MOV AX,[R_STATUS]",13,10
```

### Edit at old physical position 1156

Unchanged source before the edit:

```asm
DB 13,10
DB "R_BYTE:",13,10
DB "DB 0",13,10
```

Insert in its place:

```asm
DB 13,10
DB "R_MODE:",13,10
DB "DW 0",13,10
DB "R_NAME:",13,10
DB "DW 0",13,10
DB "R_SLOT:",13,10
DB "DW 0",13,10
DB "R_NUMBER:",13,10
DB "DW 0",13,10
DB "R_HANDLES:",13,10
DB "DW 0,0,0,0,0,0,0,0",13,10
```

The following old source remains:

```asm
DB 13,10
DB "R_STACKFAIL:",13,10
```

### Edit at old physical position 1151

Unchanged source before the edit:

```asm
DB "R_PUTGOOD:",13,10
DB "JMP R_OK",13,10
DB 13,10
```

Insert in its place:

```asm
DB "R_OPEN:",13,10
DB "MOV DX,3D00H",13,10
DB "JMP R_FILE",13,10
DB 13,10
DB "R_FILE:",13,10
DB "MOV [R_MODE],DX",13,10
DB "MOV [R_NAME],AX",13,10
DB "CALL R_FREE",13,10
DB "CMP BX,0",13,10
DB "JNE NEAR R_HAVESLOT",13,10
DB "JMP R_FAIL",13,10
DB "R_HAVESLOT:",13,10
DB "MOV DX,[R_NAME]",13,10
DB "MOV CX,0",13,10
DB "MOV AX,[R_MODE]",13,10
DB "INT 21H",13,10
DB "JAE NEAR R_FILEGOOD",13,10
DB "JMP R_FAIL",13,10
DB "R_FILEGOOD:",13,10
DB "INC AX",13,10
DB "MOV DX,[R_MODE]",13,10
DB "CMP DX,3C00H",13,10
DB "JNE NEAR R_READSLOT",13,10
DB "ADD AX,8000H",13,10
DB "R_READSLOT:",13,10
DB "MOV BX,[R_SLOT]",13,10
DB "MOV [BX],AX",13,10
DB "MOV AX,[R_NUMBER]",13,10
DB "JMP R_OK",13,10
DB "R_FREE:",13,10
DB "MOV BX,R_HANDLES",13,10
DB "MOV CX,1",13,10
DB "R_NEXTSLOT:",13,10
DB "MOV AX,[BX]",13,10
DB "CMP AX,0",13,10
DB "JE NEAR R_SLOTFOUND",13,10
DB "ADD BX,2",13,10
DB "INC CX",13,10
DB "CMP CX,9",13,10
DB "JB NEAR R_NEXTSLOT",13,10
DB "MOV BX,0",13,10
DB "RET",13,10
DB "R_SLOTFOUND:",13,10
DB "MOV [R_SLOT],BX",13,10
DB "MOV [R_NUMBER],CX",13,10
DB "RET",13,10
DB 13,10
```

The following old source remains:

```asm
DB "R_STATUS:",13,10
DB "DW 0",13,10
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
MOV CX,25
```

Insert in its place:

```asm
MOV CX,26
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR13.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 04800 bytes`. Save RESULT.COM as IR13.COM. VIEW.BAS must show length 4800.

Create T13.IR:

```ir
WORD NAME 65
LABEL MAIN
ADDR NAME
OPEN
STATUS
JZ GOOD
LIT 1
EXIT
LABEL GOOD
LIT 0
EXIT
```

```dos
COPY T13.IR SOURCE.IR
```

```dos
CHECK IR13
```

Require:

```text
OK RESULT.ASM 0000001351 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 271 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 00 01 E8 06 00 B4 4C CD 21 41 00 B8 11 01 E8 59 00 8B 06 EF 01 81 F8 00
```

Copy it to TRY.COM. First create A with `ECHO A>A`. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR13. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

