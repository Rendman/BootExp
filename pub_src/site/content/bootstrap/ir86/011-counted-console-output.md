+++
title = "11 \u00b7 Counted console output"
weight = 11
description = "Bind PUTC and persistent STATUS to checked byte output."
download = "IR11.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/047-iw-counted-console-output/", "/bootstrap/ir86/11-byte-storage/"]
+++

Bind PUTC and persistent STATUS to checked byte output.

## Enter the source

Copy IR10.ASM to IR11.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1281

Unchanged source before the edit:

```asm
DW T_PUT
DB 80,85,84,66,0,0,0,0,0,0,0,2,0,0
DW T_PUTB
```

Insert in its place:

```asm
DB 80,85,84,67,0,0,0,0,0,0,0,0,0,0
DW T_PUTC
DB 83,84,65,84,85,83,0,0,0,0,0,0,0,0
DW T_STATUS
```

### Edit at old physical position 1236

Unchanged source before the edit:

```asm
DB "JMP U_@",13,10
DB 0
```

Insert in its place:

```asm
T_PUTC:
DB "CALL R_PUTC",13,10
DB 0

T_STATUS:
DB "MOV AX,[R_STATUS]",13,10
DB 0
```

The following old source remains:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit at old physical position 1123

Unchanged source before the edit:

```asm
DB 0

T_RUNTIME:
```

Insert in its place:

```asm
DB "R_OK:",13,10
DB "MOV DX,0",13,10
DB "MOV [R_STATUS],DX",13,10
DB "RET",13,10
DB "R_ERROR:",13,10
DB "MOV DX,1",13,10
DB "MOV [R_STATUS],DX",13,10
DB "RET",13,10
DB "R_FAIL:",13,10
DB "MOV AX,0",13,10
DB "JMP R_ERROR",13,10
DB 13,10
DB "R_PUTC:",13,10
DB "MOV [R_BYTE],AL",13,10
DB "MOV BX,1",13,10
DB "MOV CX,1",13,10
DB "MOV DX,R_BYTE",13,10
DB "MOV AH,40H",13,10
DB "INT 21H",13,10
DB "JAE NEAR R_PUTCOUNT",13,10
DB "JMP R_FAIL",13,10
DB "R_PUTCOUNT:",13,10
DB "CMP AX,1",13,10
DB "JE NEAR R_PUTGOOD",13,10
DB "JMP R_ERROR",13,10
DB "R_PUTGOOD:",13,10
DB "JMP R_OK",13,10
DB 13,10
DB "R_STATUS:",13,10
DB "DW 0",13,10
DB 13,10
DB "R_BYTE:",13,10
DB "DB 0",13,10
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
MOV CX,22
```

Insert in its place:

```asm
MOV CX,24
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR11.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 04015 bytes`. Save RESULT.COM as IR11.COM. VIEW.BAS must show length 4015.

Create T11.IR:

```ir
LABEL MAIN
LIT 65
PUTC
LIT 0
EXIT
```

```dos
COPY T11.IR SOURCE.IR
```

```dos
CHECK IR11
```

Require:

```text
OK RESULT.ASM 0000000533 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 100 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 55 00 E8 04 00 B4 4C CD 21 B8 41 00 E8 1D 00 B8 00 00 B4 4C CD 21 BA 00
```

Copy it to TRY.COM. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR11. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

