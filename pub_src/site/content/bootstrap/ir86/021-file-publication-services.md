+++
title = "21 \u00b7 File publication services"
weight = 21
description = "Normalize existence, deletion, and rename without exposing DOS error values."
download = "IR21.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/057-iw-file-publication-services/", "/bootstrap/ir86/21-testing-the-accumulator/"]
+++

Writing an output file is only part of finishing a compiler run. I want the compiler to be able to check a name, remove an obsolete file, and rename a completed temporary file into place. These services will give the later compiler the same tools for protecting accepted output that our native workbench already uses.

## How it works

Normalize existence, deletion, and rename without exposing DOS error values.

## Enter the source

Copy IR20.ASM to IR21.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 2128

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

The following old source remains:

```asm

CMDCOUNT:
```

### Edit at old physical position 2023

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

### Edit at old physical position 1614

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

### Edit at old physical position 872

Unchanged source before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove:

```asm
MOV CX,52
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
CHECK ASMAKEEP IR21.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 10329 bytes`. Save RESULT.COM as IR21.COM. VIEW.BAS must show length 10329.

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
CHECK IR21 T21.IR RESULT.ASM
```

Require:

```text
OK RESULT.ASM 0000004689 text bytes
PASS
```

```dos
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 985 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 6C 02 E8 6E 02 81 F8 FF FF 75 03 E9 60 02 E8 04 00 B4 4C CD 21 55 8B EC
```

Copy it to TRY.COM. First create A with `ECHO A>A`. CHECK TRY reports PASS.

The fixture confirms that EXISTS recognizes the file A. Together with DELETE and RENAME, the completed service set lets the compiler describe its own temporary-file and backup sequence and check each result before moving on.

## Check the new boundary

Save this separate rejected source as X21.IR:

```ir
UNKNOWN
```

```dos
CHECK IR21 X21.IR RESULT.ASM
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

