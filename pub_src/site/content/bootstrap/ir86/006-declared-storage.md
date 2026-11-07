+++
title = "06 \u00b7 Declared storage"
weight = 6
description = "Declare initialized words with WORD and byte extents with BUFFER; emit larger storage with RESB."
download = "IR06.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/042-iw-declared-storage/", "/bootstrap/ir86/06-substituting-a-name/"]
+++

Declare initialized words with WORD and byte extents with BUFFER; emit larger storage with RESB.

## Enter the source

Copy IR05.ASM to IR06.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1148

Unchanged source before the edit:

```asm
DW T_EXIT
DB 76,65,66,69,76,0,0,0,0,0,2,0,0,0
DW T_LABEL
```

Insert in its place:

```asm
DB 87,79,82,68,0,0,0,0,0,0,3,4,0,0
DW T_WORD
DB 66,85,70,70,69,82,0,0,0,0,3,4,0,0
DW T_BUFFER
```

### Edit at old physical position 1141

Unchanged source before the edit:

```asm
DB "MOV AX,#",13,10
DB 0
```

Insert in its place:

```asm
T_WORD:
DB "U_@:",13,10
DB "DW #",13,10
DB 0

T_BUFFER:
DB "U_@:",13,10
DB "RESB #",13,10
DB 0
```

The following old source remains:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
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
MOV CX,3
```

Insert in its place:

```asm
MOV CX,5
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR06.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 02973 bytes`. Save RESULT.COM as IR06.COM. VIEW.BAS must show length 2973.

Create T06.IR:

```ir
WORD X 0
WORD Y 65
BUFFER B 300
LABEL MAIN
LIT 0
EXIT
```

```dos
COPY T06.IR SOURCE.IR
```

```dos
CHECK IR06
```

Require:

```text
OK RESULT.ASM 0000000207 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 333 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 3E 01 E8 34 01 B4 4C CD 21 00 00 41 00 00 00 00 00 00 00 00 00 00 00 00
```

Copy it to TRY.COM. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR06. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

