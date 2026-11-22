+++
title = "03 \u00b7 Publishing streamed assembly text"
weight = 3
description = "Copy a byte stream through a checked output block and recoverable publication."
download = "IR03.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/03-buffering-assembly-text/", "/bootstrap/ir86/039-iw-publishing-streamed-assembly-text/"]
+++

The scanner can tell me what it read, but the finished translator must leave an assembly file on disk. I shall exercise the output path with a simple copy before asking it to generate instructions. The temporary-file and recovery rules inherited from the assembler will protect the last accepted result here too.

**Starting source:** `IR02.ASM`. **Save as:** `IR03.ASM`. **Build with:** `ASMAKEEP.COM`.

## How it works

Copy a byte stream through a checked output block and recoverable publication.

## Enter the source

Copy IR02.ASM to IR03.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1023

Unchanged source before the edit:

```asm
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

The following old source remains:

```asm
CMDCOUNT:
DW 0
```

### Edit at old physical position 911

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

### Edit at old physical position 754

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
```

The following old source remains:

```asm
CMDINIT:
MOV SI,81H
```

### Edit at old physical position 23

Unchanged source before the edit:

```asm
MOV DL,91
MOV AH,2
INT 21H
```

Remove:

```asm
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
CALL CLOSEFILE
```

Insert in its place:

```asm
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
MOV SI,0C800H
SHOWTOKEN:
CALL SCAN
MOV AX,[TOKLEN]
CMP AX,0
JE NEAR READNEXT
PUSH SI
MOV SI,0CC00H
MOV DL,91
```

Insert in its place:

```asm
JE NEAR COPYDONE
MOV AL,[CHAR]
CALL EMITCHAR
JMP COPYBYTE
COPYDONE:
CALL CLOSEFILE
CALL FLUSH
CALL CLOSEOUT
CALL COMMIT
MOV DX,OKMSG
CALL TEXT
MOV SI,RESNAME
CALL CMDTEXT
MOV DL,32
```

The following old source remains:

```asm
MOV AH,2
INT 21H
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
CHECK ASMAKEEP IR03.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 02706 bytes`. Save RESULT.COM as IR03.COM. VIEW.BAS must show length 2706.

Create T03.IR:

```text
ABC
```

```dos
CHECK IR03 T03.IR RESULT.ASM
```

Require:

```text
OK RESULT.ASM 0000000005 text bytes
PASS
```

Inspect RESULT.ASM with VIEW.BAS: length 5, bytes `41 42 43 0D 0A`. This copied data is not a program.

The five bytes in RESULT.ASM prove that a stream can pass through the writer and become a published file. It is still copied data. The next two steps will give that writer generated assembly to carry.

## Check the new boundary

Choose an absent disk filename, ABSENT.IR, and run:

```dos
CHECK IR03 ABSENT.IR RESULT.ASM
```

Require:

```text
IR ERROR 0000000000 CODE 6
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

