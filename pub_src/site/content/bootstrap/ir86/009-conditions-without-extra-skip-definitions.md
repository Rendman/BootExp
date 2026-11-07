+++
title = "09 \u00b7 Conditions without extra skip definitions"
weight = 9
description = "Use fixed native conditional bridges while keeping branch semantics in the virtual machine."
download = "IR09.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/045-iw-conditions-without-extra-skip-definitions/", "/bootstrap/ir86/09-declaring-a-word/"]
+++

Use fixed native conditional bridges while keeping branch semantics in the virtual machine.

## Enter the source

Copy IR08.ASM to IR09.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1235

Unchanged source before the edit:

```asm
DW T_OR
DB 88,79,82,0,0,0,0,0,0,0,0,2,0,0
DW T_XOR
```

Insert in its place:

```asm
DB 74,77,80,0,0,0,0,0,0,0,2,4,0,0
DW T_JMP
DB 74,90,0,0,0,0,0,0,0,0,2,4,0,0
DW T_JZ
DB 74,78,90,0,0,0,0,0,0,0,2,4,0,0
DW T_JNZ
DB 67,69,81,0,0,0,0,0,0,0,0,2,0,0
DW T_CEQ
```

### Edit at old physical position 1202

Unchanged source before the edit:

```asm
DB "MOV AX,BX",13,10
DB 0
```

Insert in its place:

```asm
T_CEQ:
DB "POP BX",13,10
DB "CMP BX,AX",13,10
DB "MOV AX,0",13,10
DB "JNE $+3",13,10
DB "INC AX",13,10
DB 0

T_JZ:
DB "CMP AX,0",13,10
DB "JNE $+5",13,10
DB "JMP U_@",13,10
DB 0

T_JNZ:
DB "CMP AX,0",13,10
DB "JE $+5",13,10
DB "JMP U_@",13,10
DB 0

T_JMP:
DB "JMP U_@",13,10
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
MOV CX,16
```

Insert in its place:

```asm
MOV CX,20
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR09.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 03524 bytes`. Save RESULT.COM as IR09.COM. VIEW.BAS must show length 3524.

Create T09.IR:

```ir
LABEL MAIN
LIT 7
PUSH
LIT 7
CEQ
JNZ GOOD
LIT 1
EXIT
LABEL GOOD
LIT 0
EXIT
```

```dos
COPY T09.IR SOURCE.IR
```

```dos
CHECK IR09
```

Require:

```text
OK RESULT.ASM 0000000314 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 61 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 2E 00 E8 04 00 B4 4C CD 21 B8 07 00 50 B8 07 00 5B 3B D8 B8 00 00 75 01
```

Copy it to TRY.COM. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR09. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

