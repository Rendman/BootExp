+++
title = "05 \u00b7 The first text translator"
weight = 5
description = "Expand names and literal operands into a complete native assembly file."
download = "IR05.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/041-iw-the-first-text-translator/", "/bootstrap/ir86/05-selecting-a-translation-pattern/"]
+++

Expand names and literal operands into a complete native assembly file.

## Enter the source

Copy IR04.ASM to IR05.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1176

Unchanged source before the edit:

```asm
DW T_LIT
DB 69,88,73,84,0,0,0,0,0,0,0,4,0,0
DW T_EXIT
```

Insert in its place:

```asm
DB 76,65,66,69,76,0,0,0,0,0,2,0,0,0
DW T_LABEL
```

The following old source remains:

```asm

CMDCOUNT:
```

### Edit at old physical position 1165

Unchanged source before the edit:

```asm
T_EXIT:
DB "MOV AH,4CH",13,10
DB "INT 21H",13,10
```

Insert in its place:

```asm
DB 0

T_LABEL:
DB "U_@:",13,10
```

The following old source remains:

```asm
DB 0
```

### Edit at old physical position 1161

Unchanged source before the edit:

```asm

IRNAME:
RESB 32
```

Insert in its place:

```asm

T_HEADER:
DB "CLD",13,10
DB "CMP SP,0FFFEH",13,10
DB "JNE NEAR R_STACKFAIL",13,10
DB "CALL U_MAIN",13,10
DB "MOV AH,4CH",13,10
DB "INT 21H",13,10
DB 0

T_RUNTIME:
DB "R_STACKFAIL:",13,10
DB "MOV AX,4C02H",13,10
DB "INT 21H",13,10
DB 0
```

The following old source remains:

```asm

T_EXIT:
```

### Edit at old physical position 1159

Unchanged source before the edit:

```asm
STRID:
DW 0
```

Insert in its place:

```asm
IRCLASS:
DB 0

IRDELTA:
DB 0
```

The following old source remains:

```asm
IRNAME:
RESB 32
```

### Edit at old physical position 1153

Unchanged source before the edit:

```asm
NUMV:
DW 0
```

Insert in its place:

```asm
TPL:
DW 0
```

The following old source remains:

```asm
DEPTH:
DW 0
```

### Edit at old physical position 1032

Unchanged source before the edit:

```asm
CMDTEXTEND:
RET
```

Insert in its place:

```asm
OKMSG:
DB 79,75,32,36

BYTEMSG:
DB 32,116,101,120,116,32,98,121,116,101,115,13,10,36
```

The following old source remains:

```asm
ERRMSG:
DB 73,82,32,69,82,82,79,82,32,36
```

### Edit at old physical position 860

Unchanged source before the edit:

```asm
POP SI
RET
```

Insert in its place:

```asm
STATEMENT:
CALL SCAN
MOV AL,[0CC00H]
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
MOV CX,3
MOV AX,16
CALL LOOK
CMP BX,0
JE NEAR SYNTAXBAD
ADD BX,10
MOV AL,[BX]
MOV [IRCLASS],AL
INC BX
MOV AL,[BX]
MOV [IRDELTA],AL
ADD BX,3
MOV AX,[BX]
MOV [TPL],AX
MOV AL,[IRCLASS]
CMP AL,1
JE NEAR STATNUMBER
CMP AL,2
JE NEAR STATNAME
CMP AL,3
JE NEAR STATDATA
JMP STATFINISH
STATNUMBER:
CALL NUMARG
JMP STATFINISH
STATNAME:
CALL NAMEARG
JMP STATFINISH
STATDATA:
CALL NAMEARG
CALL NUMARG
JMP STATFINISH
STATFINISH:
CALL FINISH
MOV AL,[IRCLASS]
CMP AL,2
JNE NEAR STATLOCAL
MOV AX,[TPL]
CMP AX,T_LABEL
JNE NEAR STATLOCAL
CALL BALANCED
STATLOCAL:
STATFLOW:
MOV AL,[IRDELTA]
CMP AL,1
JE NEAR FLOWPUSH
CMP AL,2
JE NEAR FLOWPOP
CMP AL,3
JE NEAR FLOWTWO
CMP AL,4
JE NEAR FLOWBOUND
JMP STATEXPAND
FLOWPUSH:
MOV AX,[DEPTH]
CMP AX,256
JAE NEAR TABLEFULL
INC AX
MOV [DEPTH],AX
JMP STATEXPAND
FLOWTWO:
MOV AX,[DEPTH]
CMP AX,2
JB NEAR STACKBAD
SUB AX,2
MOV [DEPTH],AX
JMP STATEXPAND
FLOWPOP:
MOV AX,[DEPTH]
CMP AX,0
JE NEAR STACKBAD
DEC AX
MOV [DEPTH],AX
MOV AL,[IRCLASS]
CMP AL,2
JNE NEAR FLOWPOPDONE
CALL BALANCED
FLOWPOPDONE:
JMP STATEXPAND
FLOWBOUND:
CALL BALANCED
STATEXPAND:
MOV SI,[TPL]
CALL EXPAND
STATDONE:
RET
```

The following old source remains:

```asm
BALANCED:
MOV AX,[DEPTH]
```

### Edit at old physical position 30

Unchanged source before the edit:

```asm
CALL NUMBER32
MOV DX,NEWLINE
CALL TEXT
```

Remove:

```asm
JMP READNEXT
READDONE:
CALL CLOSEFILE
```

The following old source remains:

```asm
MOV AX,4C00H
INT 21H
```

### Edit at old physical position 28

Unchanged source before the edit:

```asm
POP AX
MOV DX,0
CALL NUMBER32
```

Remove:

```asm
MOV DX,NEWLINE
```

Insert in its place:

```asm
MOV DX,BYTEMSG
```

The following old source remains:

```asm
CALL TEXT
JMP READNEXT
```

### Edit at old physical position 13

Unchanged source before the edit:

```asm
CMP AX,0
JE NEAR READDONE
MOV SI,0C800H
```

Remove:

```asm
CALL SCAN
MOV BX,IRTAB
MOV CX,2
MOV AX,16
CALL LOOK
CMP BX,0
JE NEAR SYNTAXBAD
ADD BX,10
MOV AL,[BX]
MOV AH,0
PUSH AX
CALL FINISH
POP AX
MOV DX,0
```

Insert in its place:

```asm
CALL STATEMENT
JMP IRLINE
IRDONE:
CALL BALANCED
CALL CLOSEFILE
MOV SI,T_RUNTIME
CALL OUTTEXT
CALL FLUSH
CALL CLOSEOUT
CALL COMMIT
MOV DX,OKMSG
CALL TEXT
MOV SI,RESNAME
CALL CMDTEXT
MOV DL,32
MOV AH,2
INT 21H
MOV AX,[TOTALLO]
MOV DX,[TOTALHI]
```

The following old source remains:

```asm
CALL NUMBER32
MOV DX,NEWLINE
```

### Edit at old physical position 11

Unchanged source before the edit:

```asm
READNEXT:
CALL READLINE
CMP AX,0
```

Remove:

```asm
JE NEAR READDONE
```

Insert in its place:

```asm
JE NEAR IRDONE
```

The following old source remains:

```asm
MOV SI,0C800H
CALL SCAN
```

### Edit at old physical position 8

Unchanged source before the edit:

```asm
JNE NEAR MEMORYBAD
CALL CMDFILES
CALL OPENFILE
```

Remove:

```asm
READNEXT:
```

Insert in its place:

```asm
CALL CREATEOUT
MOV SI,T_HEADER
CALL OUTTEXT
IRLINE:
```

The following old source remains:

```asm
CALL READLINE
CMP AX,0
```

### Edit at old physical position 7

Unchanged source before the edit:

```asm
CMP SP,0FFFEH
JNE NEAR MEMORYBAD
CALL CMDFILES
```

Insert in its place:

```asm
CALL PREFLIGHT
```

The following old source remains:

```asm
CALL OPENFILE
READNEXT:
```

## Build and check

```dos
CHECK ASMAKEEP IR05.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 03406 bytes`. Save RESULT.COM as IR05.COM. VIEW.BAS must show length 3406.

Create T05.IR:

```ir
LABEL MAIN
LIT 0
LIT 0
EXIT
```

```dos
CHECK IR05 T05.IR RESULT.ASM
```

Require:

```text
OK RESULT.ASM 0000000171 text bytes
PASS
```

```dos
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 32 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 11 00 E8 04 00 B4 4C CD 21 B8 00 00 B8 00 00 B4 4C CD 21 B8 02 4C CD 21
```

Copy it to TRY.COM. CHECK TRY reports PASS.

## Check the new boundary

Save this separate rejected source as X05.IR:

```ir
UNKNOWN
```

```dos
CHECK IR05 X05.IR RESULT.ASM
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

