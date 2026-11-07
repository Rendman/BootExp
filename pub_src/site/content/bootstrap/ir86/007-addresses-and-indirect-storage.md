+++
title = "07 \u00b7 Addresses and indirect storage"
weight = 7
description = "Keep byte addresses and canonical word loads independent of physical registers."
download = "IR07.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/043-iw-addresses-and-indirect-storage/", "/bootstrap/ir86/07-naming-the-entry-point/"]
+++

Keep byte addresses and canonical word loads independent of physical registers.

## Enter the source

Copy IR06.ASM to IR07.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1162

Unchanged source before the edit:

```asm
DW T_WORD
DB 66,85,70,70,69,82,0,0,0,0,3,4,0,0
DW T_BUFFER
```

Insert in its place:

```asm
DB 76,68,0,0,0,0,0,0,0,0,2,0,0,0
DW T_LD
DB 83,84,0,0,0,0,0,0,0,0,2,0,0,0
DW T_ST
DB 65,68,68,82,0,0,0,0,0,0,2,0,0,0
DW T_ADDR
DB 70,69,84,67,72,0,0,0,0,0,0,0,0,0
DW T_FETCH
```

### Edit at old physical position 1149

Unchanged source before the edit:

```asm
T_BUFFER:
DB "U_@:",13,10
DB "RESB #",13,10
```

Insert in its place:

```asm
DB 0

T_LD:
DB "MOV AX,[U_@]",13,10
DB 0

T_ST:
DB "MOV [U_@],AX",13,10
DB 0

T_FETCH:
DB "MOV BX,AX",13,10
DB "MOV AX,[BX]",13,10
```

The following old source remains:

```asm
DB 0
```

### Edit at old physical position 1141

Unchanged source before the edit:

```asm
DB "MOV AX,#",13,10
DB 0
```

Insert in its place:

```asm
T_ADDR:
DB "MOV AX,U_@",13,10
DB 0
```

The following old source remains:

```asm
T_WORD:
DB "U_@:",13,10
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
MOV CX,5
```

Insert in its place:

```asm
MOV CX,9
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR07.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 03105 bytes`. Save RESULT.COM as IR07.COM. VIEW.BAS must show length 3105.

Create T07.IR:

```ir
WORD X 65
LABEL MAIN
ADDR X
FETCH
EXIT
```

```dos
COPY T07.IR SOURCE.IR
```

```dos
CHECK IR07
```

Require:

```text
OK RESULT.ASM 0000000195 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 35 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 14 00 E8 06 00 B4 4C CD 21 41 00 B8 11 01 8B D8 8B 07 B4 4C CD 21 B8 02
```

Copy it to TRY.COM. CHECK TRY reports FAIL because the test returns 65.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR07. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

