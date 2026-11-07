+++
title = "23 \u00b7 Checked block access"
weight = 23
description = "Validate an opaque block and byte extent before reading or writing a word."
download = "IR23.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/036-streaming-workbench/", "/bootstrap/ir86/059-iw-checked-block-access/", "/bootstrap/ir86/23-signed-comparisons/", "/bootstrap/ir86/24-calling-a-procedure/", "/bootstrap/ir86/25-preparing-dos-registers/", "/bootstrap/ir86/26-calling-dos-and-testing-carry/", "/bootstrap/ir86/27-reading-a-byte-or-end-of-input/", "/bootstrap/ir86/27-the-complete-pipeline/", "/bootstrap/ir86/28-opening-an-opaque-file-handle/", "/bootstrap/ir86/29-creating-an-output-file/", "/bootstrap/ir86/29-programs/", "/bootstrap/ir86/30-reading-into-a-byte-buffer/", "/bootstrap/ir86/31-writing-bytes-with-an-explicit-count/", "/bootstrap/ir86/32-closing-a-portable-handle/"]
+++

Validate an opaque block and byte extent before reading or writing a word.

## Enter the source

Copy IR22.ASM to IR23.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1981

Unchanged source before the edit:

```asm
DW T_ALLOC
DB 70,82,69,69,66,76,79,67,75,0,0,0,0,0
DW T_FREEBLOCK
```

Insert in its place:

```asm
DB 82,69,78,65,77,69,0,0,0,0,0,2,0,0
DW T_RENAME
DB 71,69,84,56,0,0,0,0,0,0,0,2,0,0
DW T_GET8
DB 71,69,84,49,54,0,0,0,0,0,0,2,0,0
DW T_GET16
DB 83,69,84,56,0,0,0,0,0,0,0,3,0,0
DW T_SET8
DB 83,69,84,49,54,0,0,0,0,0,0,3,0,0
DW T_SET16
```

### Edit at old physical position 1973

Unchanged source before the edit:

```asm
DW T_LITS
DB 69,88,73,83,84,83,0,0,0,0,0,0,0,0
DW T_EXISTS
```

Remove:

```asm
DB 68,69,76,69,84,69,0,0,0,0,0,0,0,0
DW T_DELETE
DB 82,69,78,65,77,69,0,0,0,0,0,2,0,0
DW T_RENAME
```

The following old source remains:

```asm
DB 65,76,76,79,67,0,0,0,0,0,0,0,0,0
DW T_ALLOC
```

### Edit at old physical position 1971

Unchanged source before the edit:

```asm
DW T_CUGE
DB 76,73,84,83,0,0,0,0,0,0,6,0,0,0
DW T_LITS
```

Insert in its place:

```asm
DB 80,85,84,67,0,0,0,0,0,0,0,0,0,0
DW T_PUTC
DB 79,80,69,78,0,0,0,0,0,0,0,0,0,0
DW T_OPEN
DB 67,82,69,65,84,69,0,0,0,0,0,0,0,0
DW T_CREATE
DB 67,76,79,83,69,0,0,0,0,0,0,0,0,0
DW T_CLOSE
DB 83,84,65,84,85,83,0,0,0,0,0,0,0,0
DW T_STATUS
DB 82,69,65,68,0,0,0,0,0,0,0,3,0,0
DW T_READ
DB 87,82,73,84,69,0,0,0,0,0,0,3,0,0
DW T_WRITE
DB 68,69,76,69,84,69,0,0,0,0,0,0,0,0
DW T_DELETE
```

The following old source remains:

```asm
DB 69,88,73,83,84,83,0,0,0,0,0,0,0,0
DW T_EXISTS
```

### Edit at old physical position 1947

Unchanged source before the edit:

```asm
DW T_PARAM
DB 80,65,68,68,82,0,0,0,0,0,1,0,0,0
DW T_PADDR
```

Remove:

```asm
DB 77,85,76,0,0,0,0,0,0,0,0,2,0,0
DW T_MUL
DB 67,65,76,76,0,0,0,0,0,0,2,0,0,0
DW T_CALL
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
DB 76,73,84,83,0,0,0,0,0,0,6,0,0,0
DW T_LITS
```

### Edit at old physical position 1909

Unchanged source before the edit:

```asm
DW T_JZ
DB 74,78,90,0,0,0,0,0,0,0,2,4,0,0
DW T_JNZ
```

Remove:

```asm
DB 67,69,81,0,0,0,0,0,0,0,0,2,0,0
DW T_CEQ
DB 80,85,84,0,0,0,0,0,0,0,0,2,0,0
DW T_PUT
DB 80,85,84,66,0,0,0,0,0,0,0,2,0,0
DW T_PUTB
DB 80,85,84,67,0,0,0,0,0,0,0,0,0,0
DW T_PUTC
DB 83,84,65,84,85,83,0,0,0,0,0,0,0,0
DW T_STATUS
DB 70,69,84,67,72,66,0,0,0,0,0,0,0,0
DW T_FETCHB
DB 79,80,69,78,0,0,0,0,0,0,0,0,0,0
DW T_OPEN
DB 67,82,69,65,84,69,0,0,0,0,0,0,0,0
DW T_CREATE
DB 82,69,65,68,0,0,0,0,0,0,0,3,0,0
DW T_READ
DB 87,82,73,84,69,0,0,0,0,0,0,3,0,0
DW T_WRITE
DB 67,76,79,83,69,0,0,0,0,0,0,0,0,0
DW T_CLOSE
```

Insert in its place:

```asm
DB 74,77,80,0,0,0,0,0,0,0,2,4,0,0
DW T_JMP
DB 67,65,76,76,0,0,0,0,0,0,2,0,0,0
DW T_CALL
```

The following old source remains:

```asm
DB 80,82,79,67,0,0,0,0,0,0,4,0,0,0
DW T_PROC
```

### Edit at old physical position 1903

Unchanged source before the edit:

```asm
DW T_OR
DB 88,79,82,0,0,0,0,0,0,0,0,2,0,0
DW T_XOR
```

Remove:

```asm
DB 74,77,80,0,0,0,0,0,0,0,2,4,0,0
DW T_JMP
```

Insert in its place:

```asm
DB 83,85,66,0,0,0,0,0,0,0,0,2,0,0
DW T_SUB
DB 77,85,76,0,0,0,0,0,0,0,0,2,0,0
DW T_MUL
DB 68,73,86,0,0,0,0,0,0,0,0,2,0,0
DW T_DIV
DB 77,79,68,0,0,0,0,0,0,0,0,2,0,0
DW T_MOD
DB 83,72,76,0,0,0,0,0,0,0,0,2,0,0
DW T_SHL
DB 83,72,82,0,0,0,0,0,0,0,0,2,0,0
DW T_SHR
DB 67,69,81,0,0,0,0,0,0,0,0,2,0,0
DW T_CEQ
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
DB 74,90,0,0,0,0,0,0,0,0,2,4,0,0
DW T_JZ
```

### Edit at old physical position 1895

Unchanged source before the edit:

```asm
DW T_POP
DB 65,68,68,0,0,0,0,0,0,0,0,2,0,0
DW T_ADD
```

Remove:

```asm
DB 83,85,66,0,0,0,0,0,0,0,0,2,0,0
DW T_SUB
```

The following old source remains:

```asm
DB 65,78,68,0,0,0,0,0,0,0,0,2,0,0
DW T_AND
```

### Edit at old physical position 1893

Unchanged source before the edit:

```asm
DW T_PUSH
DB 80,79,80,0,0,0,0,0,0,0,0,2,0,0
DW T_POP
```

Insert in its place:

```asm
DB 80,85,84,0,0,0,0,0,0,0,0,2,0,0
DW T_PUT
DB 80,85,84,66,0,0,0,0,0,0,0,2,0,0
DW T_PUTB
```

The following old source remains:

```asm
DB 65,68,68,0,0,0,0,0,0,0,0,2,0,0
DW T_ADD
```

### Edit at old physical position 1889

Unchanged source before the edit:

```asm
DW T_ADDR
DB 70,69,84,67,72,0,0,0,0,0,0,0,0,0
DW T_FETCH
```

Insert in its place:

```asm
DB 70,69,84,67,72,66,0,0,0,0,0,0,0,0
DW T_FETCHB
```

The following old source remains:

```asm
DB 80,85,83,72,0,0,0,0,0,0,0,1,0,0
DW T_PUSH
```

### Edit at old physical position 1885

Unchanged source before the edit:

```asm
DW T_LD
DB 83,84,0,0,0,0,0,0,0,0,2,0,0,0
DW T_ST
```

Remove:

```asm
DB 65,68,68,82,0,0,0,0,0,0,2,0,0,0
DW T_ADDR
```

The following old source remains:

```asm
DB 70,69,84,67,72,0,0,0,0,0,0,0,0,0
DW T_FETCH
```

### Edit at old physical position 1877

Unchanged source before the edit:

```asm
DW T_EXIT
DB 76,65,66,69,76,0,0,0,0,0,2,0,0,0
DW T_LABEL
```

Insert in its place:

```asm
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
DW T_LIT
DB 65,68,68,82,0,0,0,0,0,0,2,0,0,0
DW T_ADDR
```

The following old source remains:

```asm
DB 87,79,82,68,0,0,0,0,0,0,3,4,0,0
DW T_WORD
```

### Edit at old physical position 1871

Unchanged source before the edit:

```asm
DB 0

IRTAB:
```

Remove:

```asm
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
DW T_LIT
```

The following old source remains:

```asm
DB 69,88,73,84,0,0,0,0,0,0,0,4,0,0
DW T_EXIT
```

### Edit at old physical position 1870

Unchanged source before the edit:

```asm
DB "CALL R_RENAME",13,10
DB 0
```

Insert in its place:

```asm
T_GET8:
DB "POP BX",13,10
DB "MOV CX,1",13,10
DB "CALL R_GETMEM",13,10
DB 0

T_GET16:
DB "POP BX",13,10
DB "MOV CX,2",13,10
DB "CALL R_GETMEM",13,10
DB 0

T_SET8:
DB "POP DX",13,10
DB "POP BX",13,10
DB "MOV CX,1",13,10
DB "CALL R_SETMEM",13,10
DB 0

T_SET16:
DB "POP DX",13,10
DB "POP BX",13,10
DB "MOV CX,2",13,10
DB "CALL R_SETMEM",13,10
DB 0
```

The following old source remains:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit at old physical position 1560

Unchanged source before the edit:

```asm
DB "R_STACKFAIL:",13,10
DB "MOV AX,4C02H",13,10
DB "INT 21H",13,10
```

Remove:

```asm
DB 13,10
```

The following old source remains:

```asm
DB "R_WANT:",13,10
DB "DW 0",13,10
```

### Edit at old physical position 1556

Unchanged source before the edit:

```asm
DB "MOV AX,CS",13,10
DB "MOV ES,AX",13,10
DB "JMP R_FAIL",13,10
```

Remove:

```asm
DB 13,10
```

The following old source remains:

```asm
DB "R_STACKFAIL:",13,10
DB "MOV AX,4C02H",13,10
```

### Edit at old physical position 1529

Unchanged source before the edit:

```asm
DB "MOV AX,CS",13,10
DB "MOV ES,AX",13,10
DB "JMP R_FAIL",13,10
```

Insert in its place:

```asm
DB "R_BLOCKPTR:",13,10
DB "CMP BX,1",13,10
DB "JB NEAR R_BLOCKBAD",13,10
DB "CMP BX,16",13,10
DB "JA NEAR R_BLOCKBAD",13,10
DB "DEC BX",13,10
DB "SHL BX,1",13,10
DB "SHL BX,1",13,10
DB "ADD BX,R_BLOCKS",13,10
DB "MOV SI,BX",13,10
DB "MOV BX,[SI]",13,10
DB "CMP BX,0",13,10
DB "JE NEAR R_BLOCKBAD",13,10
DB "MOV ES,BX",13,10
DB "MOV BX,[SI+2]",13,10
DB "CMP AX,BX",13,10
DB "JAE NEAR R_BLOCKBAD",13,10
DB "SUB BX,AX",13,10
DB "CMP BX,CX",13,10
DB "JB NEAR R_BLOCKBAD",13,10
DB "MOV BX,AX",13,10
DB "MOV AX,1",13,10
DB "RET",13,10
DB "R_BLOCKBAD:",13,10
DB "MOV AX,CS",13,10
DB "MOV ES,AX",13,10
DB "MOV AX,0",13,10
DB "RET",13,10
DB "R_GETMEM:",13,10
DB "PUSH CX",13,10
DB "CALL R_BLOCKPTR",13,10
DB "POP CX",13,10
DB "CMP AX,0",13,10
DB "JE NEAR R_DFAIL",13,10
DB "MOV AL,ES:[BX]",13,10
DB "MOV AH,0",13,10
DB "CMP CX,1",13,10
DB "JE NEAR R_MEMDONE",13,10
DB "MOV AX,ES:[BX]",13,10
DB "R_MEMDONE:",13,10
DB "MOV DX,CS",13,10
DB "MOV ES,DX",13,10
DB "JMP R_OK",13,10
DB "R_SETMEM:",13,10
DB "MOV [R_MEMVALUE],AX",13,10
DB "MOV AX,DX",13,10
DB "CALL R_BLOCKPTR",13,10
DB "CMP AX,0",13,10
DB "JE NEAR R_DFAIL",13,10
DB "MOV AX,[R_MEMVALUE]",13,10
DB "CMP CX,1",13,10
DB "JNE NEAR R_SETWORD",13,10
DB "MOV ES:[BX],AL",13,10
DB "JMP R_MEMDONE",13,10
DB "R_SETWORD:",13,10
DB "MOV ES:[BX],AX",13,10
DB "JMP R_MEMDONE",13,10
```

The following old source remains:

```asm
DB "R_FREEBLOCK:",13,10
DB "MOV BX,AX",13,10
```

### Edit at old physical position 1486

Unchanged source before the edit:

```asm
DB "R_EFAIL:",13,10
DB "MOV AX,65535",13,10
DB "JMP R_ERROR",13,10
```

Remove:

```asm
DB 13,10
```

The following old source remains:

```asm
DB "R_ALLOC:",13,10
DB "CMP AX,0",13,10
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
MOV CX,55
```

Insert in its place:

```asm
MOV CX,59
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR23.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 10255 bytes`. Save RESULT.COM as IR23.COM. VIEW.BAS must show length 10255.

Create T23.IR:

```ir
WORD H 0
PROC MAIN 0 1
LIT 40960
ALLOC
ST H
LD H
PUSH
LIT 40958
PUSH
LIT 4660
SET16
LD H
PUSH
LIT 40958
GET16
PUSH
LIT 4660
CNE
SETLOCAL 0
LD H
FREEBLOCK
LOCAL 0
RETURN
```

```dos
COPY T23.IR SOURCE.IR
```

```dos
CHECK IR23
```

Require:

```text
OK RESULT.ASM 0000005104 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 1091 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 F0 03 E8 06 00 B4 4C CD 21 00 00 55 8B EC 81 EC 02 00 81 FC 00 F0 73 03
```

Copy it to TRY.COM. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR23. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

```dos
COPY IR23.COM IRKEEP.COM
COPY IRKEEP.COM IWKEEP.COM
```

IR86.ASM and this final source are identical. Continue with [RILL0](../../rill/index.html).
