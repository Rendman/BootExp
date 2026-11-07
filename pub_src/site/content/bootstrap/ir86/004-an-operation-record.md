+++
title = "04 \u00b7 An operation record"
weight = 4
description = "Look up the complete mnemonic and inspect its argument-class field."
download = "IR04.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/04-inspecting-an-instruction-record/", "/bootstrap/ir86/040-iw-an-operation-record/"]
+++

Look up the complete mnemonic and inspect its argument-class field.

## Enter the source

Copy IR03.ASM to IR04.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 918

Unchanged source before the edit:

```asm

DEPTH:
DW 0
```

Insert in its place:

```asm

STRID:
DW 0

IRNAME:
RESB 32

T_EXIT:
DB "MOV AH,4CH",13,10
DB "INT 21H",13,10
DB 0

T_LIT:
DB "MOV AX,#",13,10
DB 0

IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
DW T_LIT
DB 69,88,73,84,0,0,0,0,0,0,0,4,0,0
DW T_EXIT
```

### Edit at old physical position 916

Unchanged source before the edit:

```asm
TOTALHI:
DW 0
```

Insert in its place:

```asm
NUMV:
DW 0
```

The following old source remains:

```asm
DEPTH:
DW 0
```

### Edit at old physical position 791

Unchanged source before the edit:

```asm
TABLEFULL:
MOV AX,5
JMP ERROR
```

Remove:

```asm

OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,65,83,77,32,36

BYTEMSG:
DB 32,116,101,120,116,32,98,121,116,101,115,13,10,36
```

The following old source remains:

```asm

ERRMSG:
```

### Edit at old physical position 777

Unchanged source before the edit:

```asm
OUTDONE:
RET
```

Insert in its place:

```asm
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
```

The following old source remains:

```asm
BALANCED:
MOV AX,[DEPTH]
```

### Edit at old physical position 18

Unchanged source before the edit:

```asm
JMP COPYBYTE
COPYDONE:
CALL CLOSEFILE
```

Remove:

```asm
CALL FLUSH
CALL CLOSEOUT
CALL COMMIT
MOV DX,OKMSG
CALL TEXT
MOV AX,[TOTALLO]
MOV DX,[TOTALHI]
CALL NUMBER32
MOV DX,BYTEMSG
CALL TEXT
```

The following old source remains:

```asm
MOV AX,4C00H
INT 21H
```

### Edit at old physical position 12

Unchanged source before the edit:

```asm
COPYBYTE:
CALL NEXTBYTE
CMP AX,0
```

Remove:

```asm
JE NEAR COPYDONE
MOV AL,[CHAR]
CALL EMITCHAR
JMP COPYBYTE
COPYDONE:
```

Insert in its place:

```asm
JE NEAR READDONE
MOV SI,0C800H
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
CALL NUMBER32
MOV DX,NEWLINE
CALL TEXT
JMP READNEXT
READDONE:
```

The following old source remains:

```asm
CALL CLOSEFILE
CALL FLUSH
```

### Edit at old physical position 8

Unchanged source before the edit:

```asm
JNE NEAR MEMORYBAD
CALL PREFLIGHT
CALL OPENFILE
```

Remove:

```asm
CALL CREATEOUT
COPYBYTE:
CALL NEXTBYTE
```

Insert in its place:

```asm
READNEXT:
CALL READLINE
```

The following old source remains:

```asm
CMP AX,0
JE NEAR COPYDONE
```

### Edit at old physical position 6

Unchanged source before the edit:

```asm
CLD
CMP SP,0FFFEH
JNE NEAR MEMORYBAD
```

Remove:

```asm
CALL PREFLIGHT
```

The following old source remains:

```asm
CALL OPENFILE
CALL CREATEOUT
```

## Build and check

```dos
COPY IR04.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 02458 bytes`. Save RESULT.COM as IR04.COM. VIEW.BAS must show length 2458.

Create T04.IR:

```text
LIT
```

```dos
COPY T04.IR SOURCE.IR
```

```dos
CHECK IR04
```

Require:

```text
0000000001
PASS
```

## Check the new boundary

Temporarily rename SOURCE.IR to HOLD.TXT and run CHECK IR04. Restore the source afterward. Require:

```text
IR ERROR 0000000000 CODE 6
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

