+++
title = "21 \u00b7 File publication services"
weight = 21
description = "Normalize existence, deletion, and rename without exposing DOS error values."
download = "IR21.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/057-iw-file-publication-services/", "/bootstrap/ir86/21-testing-the-accumulator/"]
+++

Normalize existence, deletion, and rename without exposing DOS error values.

## Enter the source

Copy IR20.ASM to IR21.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1834

Unchanged source before the edit:

```asm
DW T_CUGE
DB 76,73,84,83,0,0,0,0,0,0,6,0,0,0
DW T_LITS
```

Insert in its place:

```asm
DB 69,88,73,83,84,83,0,0,0,0,0,0,0,0
DW T_EXISTS
DB 68,69,76,69,84,69,0,0,0,0,0,0,0,0
DW T_DELETE
DB 82,69,78,65,77,69,0,0,0,0,0,2,0,0
DW T_RENAME
```

### Edit at old physical position 1733

Unchanged source before the edit:

```asm
DB "CALL R_WRITE",13,10
DB 0
```

Insert in its place:

```asm
T_DELETE:
DB "CALL R_DELETE",13,10
DB 0

T_EXISTS:
DB "CALL R_EXISTS",13,10
DB 0

T_RENAME:
DB "POP DX",13,10
DB "CALL R_RENAME",13,10
DB 0
```

The following old source remains:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit at old physical position 1448

Unchanged source before the edit:

```asm
DB "R_BUFFER:",13,10
DB "DW 0",13,10
DB 13,10
```

Insert in its place:

```asm
DB "; Authored portable-services binding. No physical values escape this layer.",13,10
DB "R_DELETE:",13,10
DB "MOV DX,AX",13,10
DB "MOV AH,41H",13,10
DB "INT 21H",13,10
DB "JC NEAR R_DFAIL",13,10
DB "MOV AX,0",13,10
DB "JMP R_OK",13,10
DB "R_DFAIL:",13,10
DB "JMP R_FAIL",13,10
DB "R_RENAME:",13,10
DB "MOV DI,AX",13,10
DB "MOV AX,DS",13,10
DB "MOV ES,AX",13,10
DB "MOV AH,56H",13,10
DB "INT 21H",13,10
DB "JC NEAR R_DFAIL",13,10
DB "MOV AX,0",13,10
DB "JMP R_OK",13,10
DB "R_EXISTS:",13,10
DB "MOV DX,AX",13,10
DB "MOV AX,3D00H",13,10
DB "INT 21H",13,10
DB "JC NEAR R_NOFILE",13,10
DB "MOV BX,AX",13,10
DB "MOV AH,3EH",13,10
DB "INT 21H",13,10
DB "JC NEAR R_DFAIL",13,10
DB "MOV AX,1",13,10
DB "JMP R_OK",13,10
DB "R_NOFILE:",13,10
DB "CMP AX,2",13,10
DB "JNE NEAR R_EFAIL",13,10
DB "MOV AX,0",13,10
DB "JMP R_OK",13,10
DB "R_EFAIL:",13,10
DB "MOV AX,65535",13,10
DB "JMP R_ERROR",13,10
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
MOV CX,50
```

Insert in its place:

```asm
MOV CX,53
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR21.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 08281 bytes`. Save RESULT.COM as IR21.COM. VIEW.BAS must show length 8281.

Create T21.IR:

```ir
PROC MAIN 0 0
LITS "A"
EXISTS
PUSH
LIT 1
CNE
RETURN
```

```dos
COPY T21.IR SOURCE.IR
```

```dos
CHECK IR21
```

Require:

```text
OK RESULT.ASM 0000003193 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 623 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 60 02 E8 04 00 B4 4C CD 21 55 8B EC 81 EC 00 00 81 FC 00 F0 73 03 E9 49
```

Copy it to TRY.COM. First create A with `ECHO A>A`. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR21. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

