+++
title = "03 \u00b7 Publishing streamed assembly text"
weight = 3
description = "Copy a byte stream through a checked output block and recoverable publication."
download = "IR03.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/03-buffering-assembly-text/", "/bootstrap/ir86/039-iw-publishing-streamed-assembly-text/"]
+++

Copy a byte stream through a checked output block and recoverable publication.

## Enter the source

Copy IR02.ASM to IR03.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 864

Unchanged source before the edit:

```asm
DW 0,1000,0,100,0,10
DW 0,1
DIV32END:
```

Insert in its place:

```asm

TOTALLO:
DW 0

TOTALHI:
DW 0

DEPTH:
DW 0
```

### Edit at old physical position 753

Unchanged source before the edit:

```asm
POP AX
RET
```

Insert in its place:

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

BALANCED:
MOV AX,[DEPTH]
CMP AX,0
JNE NEAR STACKBAD
RET
STACKBAD:
MOV AX,4
JMP ERROR
SYNTAXBAD:
MOV AX,1
JMP ERROR
TABLEFULL:
MOV AX,5
JMP ERROR

OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,65,83,77,32,36

BYTEMSG:
DB 32,116,101,120,116,32,98,121,116,101,115,13,10,36
```

The following old source remains:

```asm
ERRMSG:
DB 73,82,32,69,82,82,79,82,32,36
```

### Edit at old physical position 39

Unchanged source before the edit:

```asm
JMP READNEXT
READDONE:
CALL CLOSEFILE
```

Insert in its place:

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

### Edit at old physical position 10

Unchanged source before the edit:

```asm
READNEXT:
CALL READLINE
CMP AX,0
```

Remove:

```asm
JE NEAR READDONE
MOV SI,0C800H
SHOWTOKEN:
CALL SCAN
MOV AX,[TOKLEN]
CMP AX,0
JE NEAR READNEXT
PUSH SI
MOV SI,0CC00H
MOV DL,91
MOV AH,2
INT 21H
TOKENBYTE:
LODSB
CMP AL,0
JE NEAR TOKENEND
MOV DL,AL
MOV AH,2
INT 21H
JMP TOKENBYTE
TOKENEND:
MOV DL,93
MOV AH,2
INT 21H
POP SI
JMP SHOWTOKEN
JMP READNEXT
READDONE:
```

Insert in its place:

```asm
JE NEAR COPYDONE
MOV AL,[CHAR]
CALL EMITCHAR
JMP COPYBYTE
COPYDONE:
```

The following old source remains:

```asm
CALL CLOSEFILE
MOV AX,4C00H
```

### Edit at old physical position 7

Unchanged source before the edit:

```asm
CMP SP,0FFFEH
JNE NEAR MEMORYBAD
CALL OPENFILE
```

Remove:

```asm
READNEXT:
CALL READLINE
```

Insert in its place:

```asm
CALL CREATEOUT
COPYBYTE:
CALL NEXTBYTE
```

The following old source remains:

```asm
CMP AX,0
JE NEAR READDONE
```

### Edit at old physical position 6

Unchanged source before the edit:

```asm
CLD
CMP SP,0FFFEH
JNE NEAR MEMORYBAD
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
COPY IR03.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 02213 bytes`. Save RESULT.COM as IR03.COM. VIEW.BAS must show length 2213.

Create T03.IR:

```text
ABC
```

```dos
COPY T03.IR SOURCE.IR
```

```dos
CHECK IR03
```

Require:

```text
OK RESULT.ASM 0000000005 text bytes
PASS
```

Inspect RESULT.ASM with VIEW.BAS: length 5, bytes `41 42 43 0D 0A`. This copied data is not a program.

## Check the new boundary

Temporarily rename SOURCE.IR to HOLD.TXT and run CHECK IR03. Restore the source afterward. Require:

```text
IR ERROR 0000000000 CODE 6
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

