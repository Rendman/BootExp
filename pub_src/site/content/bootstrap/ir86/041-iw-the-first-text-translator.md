+++
title = "IW05 \u00b7 The first text translator"
weight = 41
description = "Expand names and literal operands into a complete native assembly file."
download = "IW05.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Expand names and literal operands into a complete native assembly file.

## Enter the source

Copy IW04.ASM to IW05.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_LIT
DB 72,65,76,84,0,0,0,0,0,0,0,4,0,0
DW T_HALT
```

Insert after old physical line 586.

Insert:

```asm
DB 76,65,66,69,76,0,0,0,0,0,2,0,0,0
DW T_LABEL
DB 78,79,80,0,0,0,0,0,0,0,0,0,0,0
DW T_NOP
DB 69,88,73,84,0,0,0,0,0,0,0,4,0,0
DW T_EXIT
```

### Edit 2

Unchanged source immediately before the edit:

```asm
T_HALT:
DB 77,79,86,32,65,88,44,52,67,48,48,72,13,10,73,78
DB 84,32,50,49,72,13,10,0
```

Insert after old physical line 577.

Insert:

```asm

T_EXIT:
DB 77,79,86,32,65,72,44,52,67,72,13,10,73,78,84,32
DB 50,49,72,13,10,0

T_LABEL:
DB 85,95,64,58,13,10,0
```

The following old source remains in place:

```asm

T_LIT:
```

### Edit 3

Unchanged source immediately before the edit:

```asm

DEPTH:
DW 0
```

Insert after old physical line 573.

Insert:

```asm

STRID:
DW 0

IRCLASS:
DB 0

IRDELTA:
DB 0

IRNAME:
RESB 32

T_HEADER:
DB 67,76,68,13,10,67,77,80,32,83,80,44,48,70,70,70
DB 69,72,13,10,74,78,69,32,78,69,65,82,32,82,95,83
DB 84,65,67,75,70,65,73,76,13,10,67,65,76,76,32,85
DB 95,77,65,73,78,13,10,77,79,86,32,65,72,44,52,67
DB 72,13,10,73,78,84,32,50,49,72,13,10,0

T_RUNTIME:
DB 82,95,83,84,65,67,75,70,65,73,76,58,13,10,77,79
DB 86,32,65,88,44,52,67,48,50,72,13,10,73,78,84,32
DB 50,49,72,13,10,0

T_NOP:
DB 78,79,80,13,10,0
```

The following old source remains in place:

```asm

T_HALT:
```

### Edit 4

Unchanged source immediately before the edit:

```asm
DW 0,1
DIV32END:
```

Insert after old physical line 571.

Insert:

```asm
TOTALLO:
DW 0

TOTALHI:
DW 0

NUMV:
DW 0

TPL:
DW 0
```

The following old source remains in place:

```asm
DEPTH:
DW 0
```

### Edit 5

Unchanged source immediately before the edit:

```asm
DW 0

RDLEN:
```

Insert after old physical line 520.

Insert:

```asm
DW 0

OUTCNT:
```

The following old source remains in place:

```asm
DW 0
```

### Edit 6

Unchanged source immediately before the edit:

```asm
TMPNAME:
DB 73,82,84,88,46,84,77,80,0
```

Insert after old physical line 511.

Insert:

```asm
RESNAME:
DB 82,69,83,85,76,84,46,65,83,77,0

BAKNAME:
DB 73,82,82,69,83,46,66,65,75,0
```

The following old source remains in place:

```asm
RECOVERMSG:
DB 82,101,99,111,118,101,114,121,58,32,105,110,115,112,101,99
```

### Edit 7

Unchanged source immediately before the edit:

```asm

NEWLINE:
DB 13,10,36
```

Insert after old physical line 480.

Insert:

```asm

DIVISORS:
DW 10000,1000,100,10,1
DIVEND:
```

The following old source remains in place:

```asm

HANDLE:
```

### Edit 8

Unchanged source immediately before the edit:

```asm
MOV AX,5
JMP ERROR
```

Insert after old physical line 472.

Insert:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,65,83,77,32,36

BYTEMSG:
DB 32,116,101,120,116,32,98,121,116,101,115,13,10,36
```

The following old source remains in place:

```asm
ERRMSG:
DB 73,82,32,69,82,82,79,82,32,36
```

### Edit 9

Unchanged source immediately before the edit:

```asm
POP AX
RET
```

Insert after old physical line 457.

Insert:

```asm
EMITCHAR:
PUSH BX
MOV BX,[OUTCNT]
ADD BX,0E000H
MOV [BX],AL
MOV BX,[TOTALLO]
INC BX
MOV [TOTALLO],BX
CMP BX,0
JNE NEAR COUNTGOOD
MOV BX,[TOTALHI]
INC BX
MOV [TOTALHI],BX
CMP BX,0
JE NEAR TABLEFULL
COUNTGOOD:
MOV BX,[OUTCNT]
INC BX
MOV [OUTCNT],BX
CMP BX,4096
JNE NEAR CHARDONE
CALL FLUSH
CHARDONE:
POP BX
RET

OUTTEXT:
LODSB
CMP AL,0
JE NEAR OUTDONE
CALL EMITCHAR
JMP OUTTEXT
OUTDONE:
RET

OUTNUM:
PUSH AX
PUSH BX
PUSH CX
PUSH DX
PUSH SI
MOV CX,AX
MOV SI,DIVISORS
OUTPLACE:
MOV BX,SI
MOV DX,[BX]
MOV AL,48
OUTSUB:
CMP CX,DX
JB NEAR OUTDIGIT
SUB CX,DX
ADD AL,1
JMP OUTSUB
OUTDIGIT:
CALL EMITCHAR
ADD SI,2
CMP SI,DIVEND
JB NEAR OUTPLACE
POP SI
POP DX
POP CX
POP BX
POP AX
RET

EXPAND:
LODSB
CMP AL,0
JE NEAR EXPANDDONE
CMP AL,64
JE NEAR EXPANDNAME
CMP AL,35
JE NEAR EXPANDNUM
CMP AL,63
JE NEAR EXPANDID
CALL EMITCHAR
JMP EXPAND
EXPANDNAME:
PUSH SI
MOV SI,IRNAME
CALL OUTTEXT
POP SI
JMP EXPAND
EXPANDNUM:
MOV AX,[NUMV]
CALL OUTNUM
JMP EXPAND
EXPANDID:
MOV AX,[STRID]
CALL OUTNUM
JMP EXPAND
EXPANDDONE:
RET

NUMARG:
CALL SCAN
CALL ATOM
MOV [NUMV],AX
RET

NAMEARG:
CALL SCAN
MOV AX,[TOKLEN]
CMP AX,29
JA NEAR SYMBOLBAD
CALL VALIDNAME
PUSH SI
MOV SI,0CC00H
MOV DI,IRNAME
CALL COPYZ
POP SI
RET

STATEMENT:
CALL SCAN
MOV AL,[0CC00H]
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
MOV CX,5
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

The following old source remains in place:

```asm
BALANCED:
MOV AX,[DEPTH]
```

### Edit 10

Unchanged source immediately before the edit:

```asm
ERROREXIT:
MOV AX,4C01H
INT 21H
```

Insert after old physical line 325.

Insert:

```asm

EXISTS:
MOV AX,3D00H
INT 21H
JAE NEAR FILEEXISTS
CMP AX,2
JE NEAR FILENONE
JMP FILEBAD
FILEEXISTS:
MOV BX,AX
MOV AH,3EH
INT 21H
JAE NEAR EXISTSCLOSED
JMP FILEBAD
EXISTSCLOSED:
MOV AX,1
RET
FILENONE:
MOV AX,0
RET
PREFLIGHT:
MOV DX,TMPNAME
CALL EXISTS
CMP AX,0
JNE NEAR NAMEBUSY
MOV DX,BAKNAME
CALL EXISTS
CMP AX,0
JE NEAR PREFLIGHTOK
NAMEBUSY:
MOV AX,8
JMP ERROR
PREFLIGHTOK:
RET

COMMIT:
MOV DX,RESNAME
CALL EXISTS
CMP AX,0
JE NEAR PUBLISH
MOV DX,RESNAME
MOV DI,BAKNAME
MOV AH,56H
INT 21H
JAE NEAR BACKEDUP
JMP FILEBAD
BACKEDUP:
MOV AL,1
MOV [HAVEBAK],AL
PUBLISH:
MOV DX,TMPNAME
MOV DI,RESNAME
MOV AH,56H
INT 21H
JAE NEAR PUBLISHED
MOV AL,[HAVEBAK]
CMP AL,0
JE NEAR PUBLISHFAIL
MOV DX,BAKNAME
MOV DI,RESNAME
MOV AH,56H
INT 21H
JAE NEAR RESTORED
MOV AL,1
MOV [KEEPFILES],AL
JMP PUBLISHFAIL
RESTORED:
MOV AL,0
MOV [HAVEBAK],AL
PUBLISHFAIL:
JMP FILEBAD
PUBLISHED:
MOV AL,0
MOV [OWNTMP],AL
MOV AL,[HAVEBAK]
CMP AL,0
JE NEAR COMMITDONE
MOV DX,BAKNAME
MOV AH,41H
INT 21H
JAE NEAR BACKREMOVED
JMP FILEBAD
BACKREMOVED:
MOV AL,0
MOV [HAVEBAK],AL
COMMITDONE:
RET
```

The following old source remains in place:

```asm

CLEANUP:
```

### Edit 11

Unchanged source immediately before the edit:

```asm
MOV AX,1
JMP ERROR
FINISHED:
```

Insert after old physical line 289.

Insert:

```asm
RET

COPYZ:
LODSB
STOSB
CMP AL,0
JNE NEAR COPYZ
```

The following old source remains in place:

```asm
RET
```

### Edit 12

Unchanged source immediately before the edit:

```asm
POP SI
RET
```

Insert after old physical line 281.

Insert:

```asm
VALIDNAME:
MOV AX,[TOKLEN]
CMP AX,31
JBE NEAR NAMELIMIT
JMP SYMBOLBAD
NAMELIMIT:
PUSH SI
MOV SI,0CC00H
LODSB
CMP AL,95
JE NEAR NAMEVALID
CMP AL,65
JB NEAR SYMBOLBAD
CMP AL,90
JA NEAR SYMBOLBAD
NAMEVALID:
LODSB
CMP AL,0
JE NEAR NAMEVALIDEND
CMP AL,95
JE NEAR NAMEVALID
CMP AL,48
JB NEAR SYMBOLBAD
CMP AL,57
JBE NEAR NAMEVALID
CMP AL,65
JB NEAR SYMBOLBAD
CMP AL,90
JBE NEAR NAMEVALID
JMP SYMBOLBAD
NAMEVALIDEND:
POP SI
RET
SYMBOLBAD:
MOV AX,3
JMP ERROR

ATOM:
MOV AL,[0CC00H]
CMP AL,48
JB NEAR WORDVALUE
CMP AL,57
JBE NEAR LITERAL
WORDVALUE:
JMP NUMBERBAD
LITERAL:
PUSH SI
MOV SI,0CC00H
MOV DI,[TOKLEN]
ADD DI,0CC00H
MOV BX,DI
DEC BX
MOV AL,[BX]
MOV BP,10
CMP AL,72
JNE NEAR NUMBERSTART
MOV BP,16
DEC DI
NUMBERSTART:
CMP SI,DI
JE NEAR NUMBERBAD
MOV CX,0
DIGIT:
LODSB
SUB AL,48
CMP AL,9
JBE NEAR DIGITOK
SUB AL,7
CMP AL,10
JB NEAR NUMBERBAD
CMP AL,15
JA NEAR NUMBERBAD
DIGITOK:
MOV AH,0
MOV DX,AX
CMP DX,BP
JAE NEAR NUMBERBAD
CMP BP,16
JE NEAR HEXDIGIT
CMP CX,6553
JA NEAR NUMBERBAD
JB NEAR DECDIGIT
CMP DX,5
JA NEAR NUMBERBAD
DECDIGIT:
MOV AX,CX
ADD CX,CX
ADD AX,AX
ADD AX,AX
ADD AX,AX
ADD CX,AX
JMP ADDDIGIT
HEXDIGIT:
CMP CX,4095
JA NEAR NUMBERBAD
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADDDIGIT:
ADD CX,DX
CMP SI,DI
JB NEAR DIGIT
MOV AX,CX
POP SI
RET
NUMBERBAD:
MOV AX,2
JMP ERROR
```

The following old source remains in place:

```asm
FINISH:
CALL SCAN
```

### Edit 13

Unchanged source immediately before the edit:

```asm
INPUTCLOSED:
MOV AL,0
MOV [INOPEN],AL
```

Insert after old physical line 62.

Insert:

```asm
RET

CREATEOUT:
MOV DX,TMPNAME
MOV CX,0
MOV AH,3CH
INT 21H
JAE NEAR OUTPUTOPEN
JMP FILEBAD
OUTPUTOPEN:
MOV [OUTHANDLE],AX
MOV AL,1
MOV [OUTOPEN],AL
MOV [OWNTMP],AL
RET
CLOSEOUT:
MOV BX,[OUTHANDLE]
MOV AH,3EH
INT 21H
JAE NEAR OUTPUTCLOSED
JMP FILEBAD
OUTPUTCLOSED:
MOV AL,0
MOV [OUTOPEN],AL
RET

FLUSH:
PUSH AX
PUSH BX
PUSH CX
PUSH DX
MOV CX,[OUTCNT]
CMP CX,0
JE NEAR FLUSHDONE
MOV BX,[OUTHANDLE]
MOV DX,0E000H
MOV AH,40H
INT 21H
JAE NEAR FLUSHCOUNT
JMP FILEBAD
FLUSHCOUNT:
CMP AX,CX
JE NEAR FLUSHGOOD
JMP FILEBAD
FLUSHGOOD:
MOV AX,0
MOV [OUTCNT],AX
FLUSHDONE:
POP DX
POP CX
POP BX
POP AX
```

The following old source remains in place:

```asm
RET
```

### Edit 14

Unchanged source immediately before the edit:

```asm
CALL NUMBER32
MOV DX,NEWLINE
CALL TEXT
```

Remove this source at old physical positions 29–31 in IW04.ASM:

```asm
JMP READNEXT
READDONE:
CALL CLOSEFILE
```

There is no replacement source.

The following old source remains in place:

```asm
MOV AX,4C00H
INT 21H
```

### Edit 15

Unchanged source immediately before the edit:

```asm
POP AX
MOV DX,0
CALL NUMBER32
```

Remove this source at old physical positions 27–27 in IW04.ASM:

```asm
MOV DX,NEWLINE
```

Replace it with:

```asm
MOV DX,BYTEMSG
```

The following old source remains in place:

```asm
CALL TEXT
JMP READNEXT
```

### Edit 16

Unchanged source immediately before the edit:

```asm
CMP AX,0
JE NEAR READDONE
MOV SI,0C800H
```

Remove this source at old physical positions 12–25 in IW04.ASM:

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

Replace it with:

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
MOV AX,[TOTALLO]
MOV DX,[TOTALHI]
```

The following old source remains in place:

```asm
CALL NUMBER32
MOV DX,NEWLINE
```

### Edit 17

Unchanged source immediately before the edit:

```asm
READNEXT:
CALL READLINE
CMP AX,0
```

Remove this source at old physical positions 10–10 in IW04.ASM:

```asm
JE NEAR READDONE
```

Replace it with:

```asm
JE NEAR IRDONE
```

The following old source remains in place:

```asm
MOV SI,0C800H
CALL SCAN
```

### Edit 18

Unchanged source immediately before the edit:

```asm
CMP SP,0FFFEH
JNE NEAR MEMORYBAD
CALL OPENFILE
```

Remove this source at old physical positions 7–7 in IW04.ASM:

```asm
READNEXT:
```

Replace it with:

```asm
CALL CREATEOUT
MOV SI,T_HEADER
CALL OUTTEXT
IRLINE:
```

The following old source remains in place:

```asm
CALL READLINE
CMP AX,0
```

### Edit 19

Unchanged source immediately before the edit:

```asm
CLD
CMP SP,0FFFEH
JNE NEAR MEMORYBAD
```

Insert after old physical line 5.

Insert:

```asm
CALL PREFLIGHT
```

The following old source remains in place:

```asm
CALL OPENFILE
READNEXT:
```

## Build this stopping point

```dos
COPY IW05.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 02919 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW05.COM
```

VIEW.BAS must report IW05.COM length 2919 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW05.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
LABEL MAIN
LIT 0
HALT
```

```dos
COPY TIW05.IR SOURCE.IR
```

```dos
CHECK IW05
```

Require:

```text
OK RESULT.ASM 0000000159 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 00030 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 30 and these complete bytes:

```text
FC 81 FC FE FF 74 03 E9 0F 00 E8 04 00 B4 4C CD 21 B8 00 00 B8 00 4C CD 21 B8 02 4C CD 21
```

Run CHECK TRY. It returns zero and the checker reports PASS.

## A rejection or boundary check

Create XIW05.IR:

```ir
UNKNOWN
```

```dos
COPY XIW05.IR SOURCE.IR
CHECK IW05
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
