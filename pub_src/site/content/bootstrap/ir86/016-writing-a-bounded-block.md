+++
title = "16 \u00b7 Writing a bounded block"
weight = 16
description = "Check both service status and actual write progress."
download = "IR16.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/052-iw-writing-a-bounded-block/", "/bootstrap/ir86/16-writing-through-an-address/"]
+++

Check both service status and actual write progress.

## Enter the source

Copy IR15.ASM to IR16.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1468

Unchanged source before the edit:

```asm
DW T_CREATE
DB 82,69,65,68,0,0,0,0,0,0,0,3,0,0
DW T_READ
```

Insert in its place:

```asm
DB 87,82,73,84,69,0,0,0,0,0,0,3,0,0
DW T_WRITE
```

### Edit at old physical position 1411

Unchanged source before the edit:

```asm
DB "CALL R_READ",13,10
DB 0
```

Insert in its place:

```asm
T_WRITE:
DB "POP DX",13,10
DB "POP BX",13,10
DB "CALL R_WRITE",13,10
DB 0
```

The following old source remains:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit at old physical position 1248

Unchanged source before the edit:

```asm
DB "R_READGOOD:",13,10
DB "JMP R_OK",13,10
DB 13,10
```

Insert in its place:

```asm
DB "R_WRITE:",13,10
DB "MOV [R_COUNT],AX",13,10
DB "MOV [R_BUFFER],DX",13,10
DB "CALL R_FIND",13,10
DB "CMP AX,2",13,10
DB "JE NEAR R_WRITEVALID",13,10
DB "JMP R_FAIL",13,10
DB "R_WRITEVALID:",13,10
DB "MOV CX,[R_COUNT]",13,10
DB "CMP CX,0",13,10
DB "JNE NEAR R_WRITEMORE",13,10
DB "MOV AX,0",13,10
DB "JMP R_OK",13,10
DB "R_WRITEMORE:",13,10
DB "MOV DX,[R_BUFFER]",13,10
DB "MOV AH,40H",13,10
DB "INT 21H",13,10
DB "JAE NEAR R_WRITECOUNT",13,10
DB "JMP R_FAIL",13,10
DB "R_WRITECOUNT:",13,10
DB "MOV DX,[R_COUNT]",13,10
DB "CMP AX,DX",13,10
DB "JE NEAR R_WRITEGOOD",13,10
DB "JMP R_ERROR",13,10
DB "R_WRITEGOOD:",13,10
DB "JMP R_OK",13,10
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
COPY IR16.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 05975 bytes`. Save RESULT.COM as IR16.COM. VIEW.BAS must show length 5975.

Create T16.IR:

```ir
WORD NAME 65
WORD H 0
WORD B 65
LABEL MAIN
ADDR NAME
CREATE
ST H
LD H
PUSH
ADDR B
PUSH
LIT 1
WRITE
PUSH
LIT 1
CEQ
JNZ GOOD
LIT 1
EXIT
LABEL GOOD
LIT 0
EXIT
```

```dos
COPY T16.IR SOURCE.IR
```

```dos
CHECK IR16
```

Require:

```text
OK RESULT.ASM 0000002586 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 516 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 F5 01 E8 0A 00 B4 4C CD 21 41 00 00 00 41 00 B8 11 01 E8 7D 00 89 06 13
```

Copy it to TRY.COM. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR16. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

