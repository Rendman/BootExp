+++
title = "IW18 \u00b7 Procedure frames and arguments"
weight = 54
description = "Name parameter and local slots in IR; leave native frame offsets to the backend."
download = "IW18.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Name parameter and local slots in IR; leave native frame offsets to the backend.

## Enter the source

Copy IW17.ASM to IW18.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_WRITE
DB 67,76,79,83,69,0,0,0,0,0,0,0,0,0
DW T_CLOSE
```

Insert after old physical line 1525.

Insert:

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
DB 83,69,84,80,65,82,65,77,0,0,1,0,0,0
DW T_SETPARAM
DB 80,65,68,68,82,0,0,0,0,0,1,0,0,0
DW T_PADDR
DB 77,85,76,0,0,0,0,0,0,0,0,2,0,0
DW T_MUL
DB 67,69,81,0,0,0,0,0,0,0,0,2,0,0
DW T_CEQ
```

### Edit 2

Unchanged source immediately before the edit:

```asm

T_RET:
DB 82,69,84,13,10,0
```

Insert after old physical line 1402.

Insert:

```asm

T_PROC:
DB 85,95,64,58,13,10,80,85,83,72,32,66,80,13,10,77
DB 79,86,32,66,80,44,83,80,13,10,83,85,66,32,83,80
DB 44,35,13,10,67,77,80,32,83,80,44,48,70,48,48,48
DB 72,13,10,74,66,32,78,69,65,82,32,82,95,83,84,65
DB 67,75,70,65,73,76,13,10,0

T_RETURN:
DB 77,79,86,32,83,80,44,66,80,13,10,80,79,80,32,66
DB 80,13,10,82,69,84,13,10,0

T_INVOKE:
DB 67,65,76,76,32,85,95,64,13,10,65,68,68,32,83,80
DB 44,35,13,10,0

T_LOCAL:
DB 77,79,86,32,65,88,44,91,66,80,45,35,93,13,10,0

T_SETLOCAL:
DB 77,79,86,32,91,66,80,45,35,93,44,65,88,13,10,0

T_LADDR:
DB 76,69,65,32,65,88,44,91,66,80,45,35,93,13,10,0

T_PARAM:
DB 77,79,86,32,65,88,44,91,66,80,43,35,93,13,10,0

T_SETPARAM:
DB 77,79,86,32,91,66,80,43,35,93,44,65,88,13,10,0

T_PADDR:
DB 76,69,65,32,65,88,44,91,66,80,43,35,93,13,10,0
```

The following old source remains in place:

```asm

T_PUTC:
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,74,78,69,32,36,43,53,13,10,74,77,80,32
DB 85,95,64,13,10,0
```

Insert after old physical line 1340.

Insert:

```asm

T_CEQ:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,48,13,10,74,78,69
DB 32,36,43,51,13,10,73,78,67,32,65,88,13,10,0
```

The following old source remains in place:

```asm

T_NE:
```

### Edit 4

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,66,88,13,10,83,85,66,32,66,88,44,65
DB 88,13,10,77,79,86,32,65,88,44,66,88,13,10,0
```

Insert after old physical line 1336.

Insert:

```asm
T_MUL:
DB 80,79,80,32,66,88,13,10,77,85,76,32,66,88,13,10
DB 0
```

The following old source remains in place:

```asm
T_EQ:
DB 80,79,80,32,66,88,13,10,67,77,80,32,66,88,44,65
```

### Edit 5

Unchanged source immediately before the edit:

```asm
DW 0

DEPTH:
```

Insert after old physical line 1066.

Insert:

```asm
DW 0

PARAMS:
DW 0

LOCALS:
```

The following old source remains in place:

```asm
DW 0
```

### Edit 6

Unchanged source immediately before the edit:

```asm
JNE NEAR STATLOCAL
CALL BALANCED
STATLOCAL:
```

Insert after old physical line 875.

Insert:

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
CMP AX,T_SETPARAM
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

The following old source remains in place:

```asm
STATFLOW:
MOV AL,[IRDELTA]
```

### Edit 7

Unchanged source immediately before the edit:

```asm
CALL NAMEARG
CALL NUMARG
JMP STATFINISH
```

Insert after old physical line 865.

Insert:

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

The following old source remains in place:

```asm
STATFINISH:
CALL FINISH
```

### Edit 8

Unchanged source immediately before the edit:

```asm
JE NEAR STATNAME
CMP AL,3
JE NEAR STATDATA
```

Insert after old physical line 854.

Insert:

```asm
CMP AL,4
JE NEAR STATPROC
CMP AL,5
JE NEAR STATINVOKE
```

The following old source remains in place:

```asm
JMP STATFINISH
STATNUMBER:
```

### Edit 9

Unchanged source immediately before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove this source at old physical positions 834–834 in IW17.ASM:

```asm
MOV CX,47
```

Replace it with:

```asm
MOV CX,58
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

## Build this stopping point

```dos
COPY IW18.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 07775 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW18.COM
```

VIEW.BAS must report IW18.COM length 7775 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW18.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

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
COPY TIW18.IR SOURCE.IR
```

```dos
CHECK IW18
```

Require:

```text
OK RESULT.ASM 0000003180 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00635 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 635 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 6C 02 E8 04 00 B4 4C CD 21 55 8B EC 81 EC 00 00 81 FC 00 F0 73 03 E9 55
```

Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW18.IR:

```ir
UNKNOWN
```

```dos
COPY XIW18.IR SOURCE.IR
CHECK IW18
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
