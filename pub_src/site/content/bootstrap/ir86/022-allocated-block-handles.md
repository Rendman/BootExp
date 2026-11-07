+++
title = "22 \u00b7 Allocated block handles"
weight = 22
description = "Allocate byte extents beyond the main image and release owned blocks."
download = "IR22.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/058-iw-allocated-block-handles/", "/bootstrap/ir86/22-unsigned-comparisons/"]
+++

Allocate byte extents beyond the main image and release owned blocks.

## Enter the source

Copy IR21.ASM to IR22.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1892

Unchanged source before the edit:

```asm
DW T_DELETE
DB 82,69,78,65,77,69,0,0,0,0,0,2,0,0
DW T_RENAME
```

Insert in its place:

```asm
DB 65,76,76,79,67,0,0,0,0,0,0,0,0,0
DW T_ALLOC
DB 70,82,69,69,66,76,79,67,75,0,0,0,0,0
DW T_FREEBLOCK
```

### Edit at old physical position 1780

Unchanged source before the edit:

```asm
DB "CALL R_EXISTS",13,10
DB 0
```

Insert in its place:

```asm
T_ALLOC:
DB "CALL R_ALLOC",13,10
DB 0

T_FREEBLOCK:
DB "CALL R_FREEBLOCK",13,10
DB 0
```

The following old source remains:

```asm
T_RENAME:
DB "POP DX",13,10
```

### Edit at old physical position 1490

Unchanged source before the edit:

```asm
DB "R_STACKFAIL:",13,10
DB "MOV AX,4C02H",13,10
DB "INT 21H",13,10
```

Insert in its place:

```asm
DB 13,10
DB "R_WANT:",13,10
DB "DW 0",13,10
DB "R_MEMVALUE:",13,10
DB "DW 0",13,10
DB "R_BLOCKS:",13,10
DB "RESW 32",13,10
```

The following old source remains:

```asm
DB 0
```

### Edit at old physical position 1487

Unchanged source before the edit:

```asm
DB "MOV AX,65535",13,10
DB "JMP R_ERROR",13,10
DB 13,10
```

Insert in its place:

```asm
DB "R_ALLOC:",13,10
DB "CMP AX,0",13,10
DB "JE NEAR R_DFAIL",13,10
DB "MOV [R_WANT],AX",13,10
DB "MOV AX,CS",13,10
DB "MOV ES,AX",13,10
DB "MOV BX,1000H",13,10
DB "MOV AH,4AH",13,10
DB "INT 21H",13,10
DB "JC NEAR R_DFAIL",13,10
DB "MOV SI,R_BLOCKS",13,10
DB "MOV DI,1",13,10
DB "R_ALLOCSLOT:",13,10
DB "CMP WORD [SI],0",13,10
DB "JE NEAR R_ALLOCFOUND",13,10
DB "ADD SI,4",13,10
DB "INC DI",13,10
DB "CMP DI,17",13,10
DB "JB NEAR R_ALLOCSLOT",13,10
DB "JMP R_FAIL",13,10
DB "R_ALLOCFOUND:",13,10
DB "MOV BX,[R_WANT]",13,10
DB "MOV CL,4",13,10
DB "SHR BX,CL",13,10
DB "MOV AX,[R_WANT]",13,10
DB "AND AX,15",13,10
DB "CMP AX,0",13,10
DB "JE NEAR R_ALLOCROUND",13,10
DB "INC BX",13,10
DB "R_ALLOCROUND:",13,10
DB "MOV AH,48H",13,10
DB "INT 21H",13,10
DB "JC NEAR R_ALLOCBAD",13,10
DB "MOV [SI],AX",13,10
DB "MOV AX,[R_WANT]",13,10
DB "MOV [SI+2],AX",13,10
DB "MOV AX,DI",13,10
DB "JMP R_OK",13,10
DB "R_ALLOCBAD:",13,10
DB "MOV AX,CS",13,10
DB "MOV ES,AX",13,10
DB "JMP R_FAIL",13,10
DB "R_FREEBLOCK:",13,10
DB "MOV BX,AX",13,10
DB "CMP BX,1",13,10
DB "JB NEAR R_DFAIL",13,10
DB "CMP BX,16",13,10
DB "JA NEAR R_DFAIL",13,10
DB "DEC BX",13,10
DB "SHL BX,1",13,10
DB "SHL BX,1",13,10
DB "ADD BX,R_BLOCKS",13,10
DB "MOV SI,BX",13,10
DB "MOV AX,[SI]",13,10
DB "CMP AX,0",13,10
DB "JE NEAR R_DFAIL",13,10
DB "MOV ES,AX",13,10
DB "MOV AH,49H",13,10
DB "INT 21H",13,10
DB "JC NEAR R_FREEBAD",13,10
DB "MOV WORD [SI],0",13,10
DB "MOV AX,CS",13,10
DB "MOV ES,AX",13,10
DB "MOV AX,0",13,10
DB "JMP R_OK",13,10
DB "R_FREEBAD:",13,10
DB "MOV AX,CS",13,10
DB "MOV ES,AX",13,10
DB "JMP R_FAIL",13,10
DB 13,10
```

The following old source remains:

```asm
DB "R_STACKFAIL:",13,10
DB "MOV AX,4C02H",13,10
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
MOV CX,53
```

Insert in its place:

```asm
MOV CX,55
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR22.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 09297 bytes`. Save RESULT.COM as IR22.COM. VIEW.BAS must show length 9297.

Create T22.IR:

```ir
WORD H 0
PROC MAIN 0 0
LIT 40960
ALLOC
ST H
STATUS
JNZ BAD
LD H
FREEBLOCK
STATUS
RETURN
LABEL BAD
LIT 1
RETURN
```

```dos
COPY T22.IR SOURCE.IR
```

```dos
CHECK IR22
```

Require:

```text
OK RESULT.ASM 0000004198 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 902 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 33 03 E8 06 00 B4 4C CD 21 00 00 55 8B EC 81 EC 00 00 81 FC 00 F0 73 03
```

Copy it to TRY.COM. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR22. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

