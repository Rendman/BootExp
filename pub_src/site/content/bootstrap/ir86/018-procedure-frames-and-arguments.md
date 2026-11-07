+++
title = "18 \u00b7 Procedure frames and arguments"
weight = 18
description = "Name parameter and local slots in IR; leave native frame offsets to the backend."
download = "IR18.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/054-iw-procedure-frames-and-arguments/", "/bootstrap/ir86/18-counting-the-target-image/"]
+++

Name parameter and local slots in IR; leave native frame offsets to the backend.

## Enter the source

Copy IR17.ASM to IR18.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1526

Unchanged source before the edit:

```asm
DW T_WRITE
DB 67,76,79,83,69,0,0,0,0,0,0,0,0,0
DW T_CLOSE
```

Insert in its place:

```asm
DB 80,82,79,67,0,0,0,0,0,0,4,0,0,0
DW T_PROC
DB 82,69,84,85,82,78,0,0,0,0,0,4,0,0
DW T_RETURN
DB 73,78,86,79,75,69,0,0,0,0,5,0,0,0
DW T_INVOKE
DB 76,79,67,65,76,0,0,0,0,0,1,0,0,0
DW T_LOCAL
DB 83,69,84,76,79,67,65,76,0,0,1,0,0,0
DW T_SETLOCAL
DB 76,65,68,68,82,0,0,0,0,0,1,0,0,0
DW T_LADDR
DB 80,65,82,65,77,0,0,0,0,0,1,0,0,0
DW T_PARAM
DB 80,65,68,68,82,0,0,0,0,0,1,0,0,0
DW T_PADDR
DB 77,85,76,0,0,0,0,0,0,0,0,2,0,0
DW T_MUL
DB 67,65,76,76,0,0,0,0,0,0,2,0,0,0
DW T_CALL
```

### Edit at old physical position 1431

Unchanged source before the edit:

```asm

T_JMP:
DB "JMP U_@",13,10
```

Insert in its place:

```asm
DB 0

T_CALL:
DB "CALL U_@",13,10
DB 0

T_PROC:
DB "U_@:",13,10
DB "PUSH BP",13,10
DB "MOV BP,SP",13,10
DB "SUB SP,#",13,10
DB "CMP SP,0F000H",13,10
DB "JB NEAR R_STACKFAIL",13,10
DB 0

T_RETURN:
DB "MOV SP,BP",13,10
DB "POP BP",13,10
DB "RET",13,10
DB 0

T_INVOKE:
DB "CALL U_@",13,10
DB "ADD SP,#",13,10
DB 0

T_LOCAL:
DB "MOV AX,[BP-#]",13,10
DB 0

T_SETLOCAL:
DB "MOV [BP-#],AX",13,10
DB 0

T_LADDR:
DB "LEA AX,[BP-#]",13,10
DB 0

T_PARAM:
DB "MOV AX,[BP+#]",13,10
DB 0

T_PADDR:
DB "LEA AX,[BP+#]",13,10
```

The following old source remains:

```asm
DB 0
```

### Edit at old physical position 1409

Unchanged source before the edit:

```asm
DB "MOV AX,BX",13,10
DB 0
```

Insert in its place:

```asm
T_MUL:
DB "POP BX",13,10
DB "MUL BX",13,10
DB 0
```

The following old source remains:

```asm
T_CEQ:
DB "POP BX",13,10
```

### Edit at old physical position 1099

Unchanged source before the edit:

```asm
DW 0

DEPTH:
```

Insert in its place:

```asm
DW 0

PARAMS:
DW 0

LOCALS:
```

The following old source remains:

```asm
DW 0
```

### Edit at old physical position 908

Unchanged source before the edit:

```asm
JNE NEAR STATLOCAL
CALL BALANCED
STATLOCAL:
```

Insert in its place:

```asm
MOV AX,[TPL]
CMP AX,T_LOCAL
JE NEAR LOCALOFFSET
CMP AX,T_SETLOCAL
JE NEAR LOCALOFFSET
CMP AX,T_LADDR
JE NEAR LOCALOFFSET
CMP AX,T_PARAM
JE NEAR PARAMOFFSET
CMP AX,T_PADDR
JE NEAR PARAMOFFSET
JMP STATFLOW
LOCALOFFSET:
MOV AX,[NUMV]
CMP AX,[LOCALS]
JAE NEAR SYNTAXBAD
INC AX
ADD AX,AX
MOV [NUMV],AX
JMP STATFLOW
PARAMOFFSET:
MOV AX,[PARAMS]
MOV DX,[NUMV]
CMP DX,AX
JAE NEAR SYNTAXBAD
SUB AX,DX
ADD AX,AX
ADD AX,2
MOV [NUMV],AX
```

The following old source remains:

```asm
STATFLOW:
MOV AL,[IRDELTA]
```

### Edit at old physical position 898

Unchanged source before the edit:

```asm
CALL NAMEARG
CALL NUMARG
JMP STATFINISH
```

Insert in its place:

```asm
STATPROC:
CALL BALANCED
CALL NAMEARG
CALL NUMARG
CMP AX,16
JA NEAR SYNTAXBAD
MOV [PARAMS],AX
CALL NUMARG
CMP AX,64
JA NEAR SYNTAXBAD
MOV [LOCALS],AX
ADD AX,AX
MOV [NUMV],AX
JMP STATFINISH
STATINVOKE:
CALL NAMEARG
CALL NUMARG
MOV DX,[DEPTH]
CMP DX,AX
JB NEAR STACKBAD
SUB DX,AX
MOV [DEPTH],DX
ADD AX,AX
MOV [NUMV],AX
JMP STATFINISH
```

The following old source remains:

```asm
STATFINISH:
CALL FINISH
```

### Edit at old physical position 887

Unchanged source before the edit:

```asm
JE NEAR STATNAME
CMP AL,3
JE NEAR STATDATA
```

Insert in its place:

```asm
CMP AL,4
JE NEAR STATPROC
CMP AL,5
JE NEAR STATINVOKE
```

The following old source remains:

```asm
JMP STATFINISH
STATNUMBER:
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
MOV CX,30
```

Insert in its place:

```asm
MOV CX,40
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
COPY IR18.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 06809 bytes`. Save RESULT.COM as IR18.COM. VIEW.BAS must show length 6809.

Create T18.IR:

```ir
PROC MAIN 0 0
LIT 7
PUSH
LIT 9
PUSH
INVOKE TWICE 1
ADD
PUSH
LIT 25
CEQ
PUSH
LIT 1
SUB
RETURN
PROC TWICE 1 1
PARAM 0
PUSH
LIT 2
MUL
SETLOCAL 0
LOCAL 0
RETURN
```

```dos
COPY T18.IR SOURCE.IR
```

```dos
CHECK IR18
```

Require:

```text
OK RESULT.ASM 0000002949 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 587 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 3C 02 E8 04 00 B4 4C CD 21 55 8B EC 81 EC 00 00 81 FC 00 F0 73 03 E9 25
```

Copy it to TRY.COM. CHECK TRY reports PASS.

## Check the new boundary

Use this separate rejected source:

```ir
UNKNOWN
```

Copy it to SOURCE.IR and run CHECK IR18. Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

