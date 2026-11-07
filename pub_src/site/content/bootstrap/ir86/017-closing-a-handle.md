+++
title = "17 \u00b7 Closing a handle"
weight = 17
description = "Retire an owned handle only after a successful close."
download = "IR17.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/053-iw-closing-a-handle/", "/bootstrap/ir86/17-reserving-a-byte-buffer/"]
+++

Retire an owned handle only after a successful close.

## Enter the source

Copy IR16.ASM to IR17.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1503

Unchanged source before the edit:

```asm
DW T_READ
DB 87,82,73,84,69,0,0,0,0,0,0,3,0,0
DW T_WRITE
```

Insert in its place:

```asm
DB 67,76,79,83,69,0,0,0,0,0,0,0,0,0
DW T_CLOSE
```

### Edit at old physical position 1428

Unchanged source before the edit:

```asm
DB "CALL R_CREATE",13,10
DB 0
```

Insert in its place:

```asm
T_CLOSE:
DB "CALL R_CLOSE",13,10
DB 0
```

The following old source remains:

```asm
T_STATUS:
DB "MOV AX,[R_STATUS]",13,10
```

### Edit at old physical position 1275

Unchanged source before the edit:

```asm
DB "R_WRITEGOOD:",13,10
DB "JMP R_OK",13,10
DB 13,10
```

Insert in its place:

```asm
DB "R_CLOSE:",13,10
DB "MOV BX,AX",13,10
DB "CALL R_FIND",13,10
DB "CMP AX,0",13,10
DB "JNE NEAR R_CLOSEVALID",13,10
DB "JMP R_FAIL",13,10
DB "R_CLOSEVALID:",13,10
DB "MOV AH,3EH",13,10
DB "INT 21H",13,10
DB "JAE NEAR R_CLOSEGOOD",13,10
DB "JMP R_FAIL",13,10
DB "R_CLOSEGOOD:",13,10
DB "MOV BX,[R_SLOT]",13,10
DB "MOV AX,0",13,10
DB "MOV [BX],AX",13,10
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
MOV CX,29
```

Insert in its place:

```asm
MOV CX,30
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR17.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 06221 bytes`. Save RESULT.COM as IR17.COM. VIEW.BAS must show length 6221.

Create T17.IR:

```ir
WORD NAME 65
LABEL MAIN
ADDR NAME
OPEN
CLOSE
STATUS
EXIT
```

```dos
COPY T17.IR SOURCE.IR
```

```dos
CHECK IR17
```

Require:

```text
OK RESULT.ASM 0000002541 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 507 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 EC 01 E8 06 00 B4 4C CD 21 41 00 B8 11 01 E8 49 00 E8 92 01 8B 06 D7 02
```

Copy it to TRY.COM. First create A with `ECHO A>A`. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR17. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

