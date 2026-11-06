+++
title = "IW04 \u00b7 An operation record"
weight = 40
description = "Look up the complete mnemonic and inspect its argument-class field."
download = "IW04.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Look up the complete mnemonic and inspect its argument-class field.

## Enter the source

Copy IW03.ASM to IW04.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
TOTALHI:
DW 0
```

Remove this source at old physical positions 548–549 in IW03.ASM:

```asm
DEPTH:
DW 0
```

Replace it with:

```asm
T_LIT:
DB 77,79,86,32,65,88,44,35,13,10,0

IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
DW T_LIT
DB 72,65,76,84,0,0,0,0,0,0,0,4,0,0
DW T_HALT
```

### Edit 2

Unchanged source immediately before the edit:

```asm
TOTALLO:
DW 0
```

Remove this source at old physical positions 545–546 in IW03.ASM:

```asm
TOTALHI:
DW 0
```

Replace it with:

```asm
T_HALT:
DB 77,79,86,32,65,88,44,52,67,48,48,72,13,10,73,78
DB 84,32,50,49,72,13,10,0
```

The following old source remains in place:

```asm

DEPTH:
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DW 0,1
DIV32END:
```

Remove this source at old physical positions 542–542 in IW03.ASM:

```asm
TOTALLO:
```

Replace it with:

```asm
DEPTH:
```

The following old source remains in place:

```asm
DW 0
```

### Edit 4

Unchanged source immediately before the edit:

```asm
DW 0

RDLEN:
```

Remove this source at old physical positions 488–490 in IW03.ASM:

```asm
DW 0

OUTCNT:
```

There is no replacement source.

The following old source remains in place:

```asm
DW 0
```

### Edit 5

Unchanged source immediately before the edit:

```asm
TMPNAME:
DB 73,82,84,88,46,84,77,80,0
```

Remove this source at old physical positions 473–478 in IW03.ASM:

```asm
RESNAME:
DB 82,69,83,85,76,84,46,65,83,77,0

BAKNAME:
DB 73,82,82,69,83,46,66,65,75,0
```

There is no replacement source.

The following old source remains in place:

```asm
RECOVERMSG:
DB 82,101,99,111,118,101,114,121,58,32,105,110,115,112,101,99
```

### Edit 6

Unchanged source immediately before the edit:

```asm
LINENO:
DW 0
```

Insert after old physical line 460.

Insert:

```asm
TOKLEN:
DW 0

STRIDE:
DW 0

ENDED:
DB 0

SKIPLF:
DB 0
```

The following old source remains in place:

```asm
CHAR:
DB 0
```

### Edit 7

Unchanged source immediately before the edit:

```asm
TABLEFULL:
MOV AX,5
JMP ERROR
```

Remove this source at old physical positions 439–444 in IW03.ASM:

```asm

OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,65,83,77,32,36

BYTEMSG:
DB 32,116,101,120,116,32,98,121,116,101,115,13,10,36
```

There is no replacement source.

The following old source remains in place:

```asm

ERRMSG:
```

### Edit 8

Unchanged source immediately before the edit:

```asm
POP AX
RET
```

Remove this source at old physical positions 399–424 in IW03.ASM:

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
```

There is no replacement source.

The following old source remains in place:

```asm
BALANCED:
MOV AX,[DEPTH]
```

### Edit 9

Unchanged source immediately before the edit:

```asm
ERROREXIT:
MOV AX,4C01H
INT 21H
```

Remove this source at old physical positions 180–266 in IW03.ASM:

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

There is no replacement source.

The following old source remains in place:

```asm

CLEANUP:
```

### Edit 10

Unchanged source immediately before the edit:

```asm
RET
BUFFEREND:
MOV AX,0
```

Insert after old physical line 143.

Insert:

```asm
RET

READLINE:
MOV DI,0C800H
MOV BP,0
MOV AL,[ENDED]
CMP AL,0
JE NEAR READCHAR
MOV AX,0
RET
READCHAR:
CALL NEXTBYTE
CMP AX,0
JE NEAR ENDFILE
MOV AL,[CHAR]
CMP AL,10
JE NEAR LINEFEED
MOV AH,0
MOV [SKIPLF],AH
CMP AL,13
JE NEAR CARRIAGE
CMP AL,26
JE NEAR ENDFILE
CMP BP,1023
JAE NEAR READFULL
CMP AL,9
JE NEAR KEEPCHAR
CMP AL,32
JB NEAR READBAD
CMP AL,126
JA NEAR READBAD
KEEPCHAR:
STOSB
INC BP
JMP READCHAR
LINEFEED:
MOV AL,[SKIPLF]
CMP AL,0
JE NEAR LINEEND
MOV AL,0
MOV [SKIPLF],AL
JMP READCHAR
CARRIAGE:
MOV AL,1
MOV [SKIPLF],AL
JMP LINEEND
ENDFILE:
MOV AL,1
MOV [ENDED],AL
CMP BP,0
JE NEAR EMPTYEND
LINEEND:
MOV AL,0
STOSB
CALL COUNTLINE
MOV AX,1
RET
EMPTYEND:
MOV AX,0
RET
READFULL:
MOV AX,5
JMP READFAIL
READBAD:
MOV AX,6
READFAIL:
PUSH AX
CALL COUNTLINE
POP AX
JMP ERROR

SCAN:
MOV DI,0CC00H
SCANSPACE:
LODSB
CMP AL,32
JE NEAR SCANSPACE
CMP AL,9
JE NEAR SCANSPACE
CMP AL,0
JE NEAR SCANEND
CMP AL,59
JE NEAR SCANEND
CALL TOKENCHAR
STOSB
CALL SEPARATOR
CMP AH,1
JE NEAR SCANDONE
SCANMORE:
LODSB
CMP AL,0
JE NEAR SCANBACK
CMP AL,32
JE NEAR SCANBACK
CMP AL,9
JE NEAR SCANBACK
CMP AL,59
JE NEAR SCANBACK
CALL SEPARATOR
CMP AH,1
JE NEAR SCANBACK
CMP DI,0CC3FH
JAE NEAR TOKENBAD
CALL TOKENCHAR
STOSB
JMP SCANMORE
SCANBACK:
DEC SI
SCANDONE:
MOV AX,DI
SUB AX,0CC00H
MOV [TOKLEN],AX
MOV AL,0
STOSB
RET
SCANEND:
DEC SI
JMP SCANDONE
TOKENBAD:
MOV AX,1
JMP ERROR
TOKENCHAR:
CMP AL,97
JB NEAR TOKENKEPT
CMP AL,122
JA NEAR TOKENKEPT
SUB AL,32
TOKENKEPT:
RET
SEPARATOR:
MOV AH,1
CMP AL,44
JE NEAR SEPARATORRET
CMP AL,58
JE NEAR SEPARATORRET
CMP AL,91
JE NEAR SEPARATORRET
CMP AL,93
JE NEAR SEPARATORRET
CMP AL,43
JE NEAR SEPARATORRET
CMP AL,45
JE NEAR SEPARATORRET
CMP AL,40
JE NEAR SEPARATORRET
CMP AL,41
JE NEAR SEPARATORRET
CMP AL,34
JE NEAR SEPARATORRET
MOV AH,0
SEPARATORRET:
RET

LOOK:
MOV [STRIDE],AX
PUSH SI
MOV BP,BX
LOOKNEXT:
CMP CX,0
JE NEAR LOOKMISS
MOV DI,BP
MOV SI,0CC00H
LOOKCHAR:
LODSB
MOV BX,DI
MOV DL,[BX]
CMP AL,DL
JNE NEAR LOOKSTEP
CMP AL,0
JE NEAR LOOKFOUND
INC DI
JMP LOOKCHAR
LOOKSTEP:
MOV AX,[STRIDE]
ADD BP,AX
DEC CX
JMP LOOKNEXT
LOOKFOUND:
MOV BX,BP
POP SI
RET
LOOKMISS:
MOV BX,0
POP SI
RET

FINISH:
CALL SCAN
MOV AL,[0CC00H]
CMP AL,0
JE NEAR FINISHED
MOV AX,1
JMP ERROR
FINISHED:
```

The following old source remains in place:

```asm
RET
```

### Edit 11

Unchanged source immediately before the edit:

```asm
MOV [INOPEN],AL
RET
```

Remove this source at old physical positions 61–112 in IW03.ASM:

```asm
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
RET
```

There is no replacement source.

The following old source remains in place:

```asm
NEXTBYTE:
MOV AX,[RDPOS]
```

### Edit 12

Unchanged source immediately before the edit:

```asm
JMP COPYBYTE
COPYDONE:
CALL CLOSEFILE
```

Remove this source at old physical positions 18–27 in IW03.ASM:

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

There is no replacement source.

The following old source remains in place:

```asm
MOV AX,4C00H
INT 21H
```

### Edit 13

Unchanged source immediately before the edit:

```asm
COPYBYTE:
CALL NEXTBYTE
CMP AX,0
```

Remove this source at old physical positions 12–16 in IW03.ASM:

```asm
JE NEAR COPYDONE
MOV AL,[CHAR]
CALL EMITCHAR
JMP COPYBYTE
COPYDONE:
```

Replace it with:

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

The following old source remains in place:

```asm
CALL CLOSEFILE
CALL FLUSH
```

### Edit 14

Unchanged source immediately before the edit:

```asm
JNE NEAR MEMORYBAD
CALL PREFLIGHT
CALL OPENFILE
```

Remove this source at old physical positions 8–10 in IW03.ASM:

```asm
CALL CREATEOUT
COPYBYTE:
CALL NEXTBYTE
```

Replace it with:

```asm
READNEXT:
CALL READLINE
```

The following old source remains in place:

```asm
CMP AX,0
JE NEAR COPYDONE
```

### Edit 15

Unchanged source immediately before the edit:

```asm
CLD
CMP SP,0FFFEH
JNE NEAR MEMORYBAD
```

Remove this source at old physical positions 6–6 in IW03.ASM:

```asm
CALL PREFLIGHT
```

There is no replacement source.

The following old source remains in place:

```asm
CALL OPENFILE
CALL CREATEOUT
```

## Build this stopping point

```dos
COPY IW04.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 01439 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW04.COM
```

VIEW.BAS must report IW04.COM length 1439 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW04.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```text
LIT
```

```dos
COPY TIW04.IR SOURCE.IR
```

```dos
CHECK IW04
```

Require:

```text
0000000001
PASS
```

## A rejection or boundary check

Rename SOURCE.IR to an unused HOLD.IR, then run CHECK IW04. Restore the source after the test.

Require:

```text
IR ERROR 0000000000 CODE 6
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
