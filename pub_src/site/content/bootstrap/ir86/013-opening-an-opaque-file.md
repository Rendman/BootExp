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

ARGC returns the number of command arguments. ARG takes a one-based argument index in A and returns a stable, zero-terminated byte-addressed string, with STATUS indicating success or failure. An invalid index returns zero and failed status. The entry binding copies and validates the PSP tail before MAIN; up to three unquoted 8.3 filename arguments fit the owned slots. The IR program sees strings and counts, not PSP offsets or processor registers. Follow CMDINIT in the emitted runtime and the small R_ARGC/R_ARG entries.

## Enter the source

Copy IR12.ASM to IR13.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1498

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
DB 65,82,71,67,0,0,0,0,0,0,0,0,0,0
DW T_ARGC
DB 65,82,71,0,0,0,0,0,0,0,0,0,0,0
DW T_ARG
```

The following old source remains:

```asm

CMDCOUNT:
```

### Edit at old physical position 1443

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

T_ARGC:
DB "CALL R_ARGC",13,10
DB 0

T_ARG:
DB "CALL R_ARG",13,10
DB 0
```

The following old source remains:

```asm
T_STATUS:
DB "MOV AX,[R_STATUS]",13,10
```

### Edit at old physical position 1323

Unchanged source before the edit:

```asm
DB "R_STACKFAIL:",13,10
DB "MOV AX,4C02H",13,10
DB "INT 21H",13,10
```

Insert in its place:

```asm
DB 13,10
DB "CMDINIT:",13,10
DB "MOV SI,81H",13,10
DB "MOV DI,CMDBUF",13,10
DB "MOV [CMDPTR],DI",13,10
DB "MOV AL,[80H]",13,10
DB "MOV AH,0",13,10
DB "MOV CX,AX",13,10
DB "CMP CX,127",13,10
DB "JAE NEAR CMDBAD",13,10
DB "CMDSKIP:",13,10
DB "CMP CX,0",13,10
DB "JE NEAR CMDDONE",13,10
DB "LODSB",13,10
DB "DEC CX",13,10
DB "CMP AL,32",13,10
DB "JE NEAR CMDSKIP",13,10
DB "CMP AL,9",13,10
DB "JE NEAR CMDSKIP",13,10
DB "MOV BX,[CMDCOUNT]",13,10
DB "CMP BX,3",13,10
DB "JAE NEAR CMDBAD",13,10
DB "INC BX",13,10
DB "MOV [CMDCOUNT],BX",13,10
DB "MOV BX,0",13,10
DB "MOV DX,8",13,10
DB "CMDCHAR:",13,10
DB "CMP AL,46",13,10
DB "JE NEAR CMDDOT",13,10
DB "CMP AL,97",13,10
DB "JB NEAR CMDUP",13,10
DB "CMP AL,122",13,10
DB "JA NEAR CMDUP",13,10
DB "SUB AL,32",13,10
DB "CMDUP:",13,10
DB "CMP AL,65",13,10
DB "JB NEAR CMDNUM",13,10
DB "CMP AL,90",13,10
DB "JBE NEAR CMDPUT",13,10
DB "CMDNUM:",13,10
DB "CMP AL,48",13,10
DB "JB NEAR CMDEXTRA",13,10
DB "CMP AL,57",13,10
DB "JBE NEAR CMDPUT",13,10
DB "CMDEXTRA:",13,10
DB "CMP AL,95",13,10
DB "JE NEAR CMDPUT",13,10
DB "CMP AL,45",13,10
DB "JNE NEAR CMDBAD",13,10
DB "CMDPUT:",13,10
DB "INC BX",13,10
DB "CMP BX,DX",13,10
DB "JA NEAR CMDBAD",13,10
DB "STOSB",13,10
DB "JMP CMDNEXT",13,10
DB "CMDDOT:",13,10
DB "CMP DX,8",13,10
DB "JNE NEAR CMDBAD",13,10
DB "CMP BX,0",13,10
DB "JE NEAR CMDBAD",13,10
DB "MOV DX,3",13,10
DB "MOV BX,0",13,10
DB "STOSB",13,10
DB "CMDNEXT:",13,10
DB "CMP CX,0",13,10
DB "JE NEAR CMDEND",13,10
DB "LODSB",13,10
DB "DEC CX",13,10
DB "CMP AL,32",13,10
DB "JE NEAR CMDEND",13,10
DB "CMP AL,9",13,10
DB "JNE NEAR CMDCHAR",13,10
DB "CMDEND:",13,10
DB "CMP BX,0",13,10
DB "JE NEAR CMDBAD",13,10
DB "MOV AL,0",13,10
DB "STOSB",13,10
DB "MOV DI,[CMDPTR]",13,10
DB "ADD DI,13",13,10
DB "MOV [CMDPTR],DI",13,10
DB "JMP CMDSKIP",13,10
DB "CMDDONE:",13,10
DB "MOV AX,[CMDCOUNT]",13,10
DB "RET",13,10
DB "CMDBAD:",13,10
DB "MOV AX,65535",13,10
DB "RET",13,10
DB "R_ARGC:",13,10
DB "MOV AX,[CMDCOUNT]",13,10
DB "JMP R_OK",13,10
DB "R_ARG:",13,10
DB "CMP AX,1",13,10
DB "JB NEAR R_ARGBAD",13,10
DB "MOV BX,[CMDCOUNT]",13,10
DB "CMP AX,BX",13,10
DB "JA NEAR R_ARGBAD",13,10
DB "MOV BX,CMDBUF",13,10
DB "R_ARGNEXT:",13,10
DB "DEC AX",13,10
DB "JE NEAR R_ARGDONE",13,10
DB "ADD BX,13",13,10
DB "JMP R_ARGNEXT",13,10
DB "R_ARGDONE:",13,10
DB "MOV AX,BX",13,10
DB "JMP R_OK",13,10
DB "R_ARGBAD:",13,10
DB "MOV AX,0",13,10
DB "JMP R_ERROR",13,10
DB "CMDCOUNT:",13,10
DB "DW 0",13,10
DB "CMDPTR:",13,10
DB "DW 0",13,10
DB "CMDBUF:",13,10
DB "DB 0,0,0,0,0,0,0,0,0,0,0,0,0",13,10
DB "DB 0,0,0,0,0,0,0,0,0,0,0,0,0",13,10
DB "DB 0,0,0,0,0,0,0,0,0,0,0,0,0",13,10
```

The following old source remains:

```asm
DB 0
```

### Edit at old physical position 1320

Unchanged source before the edit:

```asm
DB "R_BYTE:",13,10
DB "DB 0",13,10
DB 13,10
```

Insert in its place:

```asm
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
DB 13,10
```

The following old source remains:

```asm
DB "R_STACKFAIL:",13,10
DB "MOV AX,4C02H",13,10
```

### Edit at old physical position 1314

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

### Edit at old physical position 1280

Unchanged source before the edit:

```asm
DB "CLD",13,10
DB "CMP SP,0FFFEH",13,10
DB "JNE NEAR R_STACKFAIL",13,10
```

Insert in its place:

```asm
DB "CALL CMDINIT",13,10
DB "CMP AX,65535",13,10
DB "JE NEAR R_STACKFAIL",13,10
```

The following old source remains:

```asm
DB "CALL U_MAIN",13,10
DB "MOV AH,4CH",13,10
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
MOV CX,25
```

Insert in its place:

```asm
MOV CX,28
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
CHECK ASMAKEEP IR13.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 06848 bytes`. Save RESULT.COM as IR13.COM. VIEW.BAS must show length 6848.

Create T13.IR:

```ir
LABEL MAIN
ARGC
PUSH
LIT 1
CEQ
JNZ NAMED
LIT 1
EXIT
LABEL NAMED
LIT 1
ARG
OPEN
STATUS
EXIT
```

```dos
CHECK IR13 T13.IR RESULT.ASM
```

Require:

```text
OK RESULT.ASM 0000002908 text bytes
PASS
```

```dos
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 647 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 1A 01 E8 1C 01 81 F8 FF FF 75 03 E9 0E 01 E8 04 00 B4 4C CD 21 E8 06 02
```

Copy it to TRY.COM. First create A with `ECHO A>A`. `CHECK TRY A` reports PASS.

## Check the new boundary

Save this separate rejected source as X13.IR:

```ir
UNKNOWN
```

```dos
CHECK IR13 X13.IR RESULT.ASM
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

