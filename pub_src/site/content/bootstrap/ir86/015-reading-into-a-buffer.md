+++
title = "15 \u00b7 Reading into a buffer"
weight = 15
description = "Consume a saved handle and pointer, return actual progress, and refill after short reads."
download = "IR15.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/051-iw-reading-into-a-buffer/", "/bootstrap/ir86/15-addresses-as-word-values/"]
+++

Consume a saved handle and pointer, return actual progress, and refill after short reads.

## Enter the source

Copy IR14.ASM to IR15.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1409

Unchanged source before the edit:

```asm
DW T_OPEN
DB 67,82,69,65,84,69,0,0,0,0,0,0,0,0
DW T_CREATE
```

Insert in its place:

```asm
DB 82,69,65,68,0,0,0,0,0,0,0,3,0,0
DW T_READ
```

### Edit at old physical position 1354

Unchanged source before the edit:

```asm
DB "MOV AX,[R_STATUS]",13,10
DB 0
```

Insert in its place:

```asm
T_READ:
DB "POP DX",13,10
DB "POP BX",13,10
DB "CALL R_READ",13,10
DB 0
```

The following old source remains:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit at old physical position 1218

Unchanged source before the edit:

```asm
DB "DW 0",13,10
DB "R_HANDLES:",13,10
DB "DW 0,0,0,0,0,0,0,0",13,10
```

Insert in its place:

```asm
DB 13,10
DB "R_COUNT:",13,10
DB "DW 0",13,10
DB "R_BUFFER:",13,10
DB "DW 0",13,10
```

The following old source remains:

```asm
DB 13,10
DB "R_STACKFAIL:",13,10
```

### Edit at old physical position 1202

Unchanged source before the edit:

```asm
DB "MOV [R_NUMBER],CX",13,10
DB "RET",13,10
DB 13,10
```

Insert in its place:

```asm
DB "R_FIND:",13,10
DB "CMP BX,1",13,10
DB "JB NEAR R_BADHANDLE",13,10
DB "CMP BX,8",13,10
DB "JA NEAR R_BADHANDLE",13,10
DB "DEC BX",13,10
DB "ADD BX,BX",13,10
DB "ADD BX,R_HANDLES",13,10
DB "MOV [R_SLOT],BX",13,10
DB "MOV BX,[BX]",13,10
DB "CMP BX,0",13,10
DB "JE NEAR R_BADHANDLE",13,10
DB "MOV AX,1",13,10
DB "CMP BX,8000H",13,10
DB "JB NEAR R_HANDLEKIND",13,10
DB "AND BX,7FFFH",13,10
DB "MOV AX,2",13,10
DB "R_HANDLEKIND:",13,10
DB "DEC BX",13,10
DB "RET",13,10
DB "R_BADHANDLE:",13,10
DB "MOV AX,0",13,10
DB "RET",13,10
DB 13,10
DB "R_READ:",13,10
DB "MOV [R_COUNT],AX",13,10
DB "MOV [R_BUFFER],DX",13,10
DB "CALL R_FIND",13,10
DB "CMP AX,1",13,10
DB "JE NEAR R_READVALID",13,10
DB "JMP R_FAIL",13,10
DB "R_READVALID:",13,10
DB "MOV CX,[R_COUNT]",13,10
DB "CMP CX,0",13,10
DB "JNE NEAR R_READMORE",13,10
DB "MOV AX,0",13,10
DB "JMP R_OK",13,10
DB "R_READMORE:",13,10
DB "MOV DX,[R_BUFFER]",13,10
DB "MOV AH,3FH",13,10
DB "INT 21H",13,10
DB "JAE NEAR R_READGOOD",13,10
DB "JMP R_FAIL",13,10
DB "R_READGOOD:",13,10
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
MOV CX,27
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
COPY IR15.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 05546 bytes`. Save RESULT.COM as IR15.COM. VIEW.BAS must show length 5546.

Create T15.IR:

```ir
WORD NAME 65
WORD H 0
BUFFER B 1
LABEL MAIN
ADDR NAME
OPEN
ST H
LD H
PUSH
ADDR B
PUSH
LIT 1
READ
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
COPY T15.IR SOURCE.IR
```

```dos
CHECK IR15
```

Require:

```text
OK RESULT.ASM 0000002203 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 440 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 A9 01 E8 09 00 B4 4C CD 21 41 00 00 00 00 B8 11 01 E8 77 00 89 06 13 01
```

Copy it to TRY.COM. First create A with `ECHO A>A`. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR15. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

