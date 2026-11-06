+++
title = "IW02 \u00b7 Tokens without a complete source buffer"
weight = 38
description = "Fold token spellings while preserving the raw line for quoted data."
download = "IW02.ASM"
download_group = "tools/toolchain"
reader_names = 1
+++

## The working parts

Fold token spellings while preserving the raw line for quoted data.

## Enter the source

Copy IW01.ASM to IW02.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
LINENO:
DW 0
```

Insert after old physical line 341.

Insert:

```asm
TOKLEN:
DW 0
```

The following old source remains in place:

```asm
ENDED:
DB 0
```

### Edit 2

Unchanged source immediately before the edit:

```asm
CALL COUNTLINE
POP AX
JMP ERROR
```

Insert after old physical line 159.

Insert:

```asm

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
```

The following old source remains in place:

```asm

TEXT:
```

### Edit 3

Unchanged source immediately before the edit:

```asm
MOV DL,AL
MOV AH,2
INT 21H
```

Remove this source at old physical positions 19–22 in IW01.ASM:

```asm
JMP SHOWBYTE
SHOWEND:
MOV DX,NEWLINE
CALL TEXT
```

Replace it with:

```asm
JMP TOKENBYTE
TOKENEND:
MOV DL,93
MOV AH,2
INT 21H
POP SI
JMP SHOWTOKEN
```

The following old source remains in place:

```asm
JMP READNEXT
READDONE:
```

### Edit 4

Unchanged source immediately before the edit:

```asm
SHOWBYTE:
LODSB
CMP AL,0
```

Remove this source at old physical positions 15–15 in IW01.ASM:

```asm
JE NEAR SHOWEND
```

Replace it with:

```asm
JE NEAR TOKENEND
```

The following old source remains in place:

```asm
MOV DL,AL
MOV AH,2
```

### Edit 5

Unchanged source immediately before the edit:

```asm
CMP AX,0
JE NEAR READDONE
MOV SI,0C800H
```

Remove this source at old physical positions 12–12 in IW01.ASM:

```asm
SHOWBYTE:
```

Replace it with:

```asm
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
```

The following old source remains in place:

```asm
LODSB
CMP AL,0
```

## Build this stopping point

```dos
COPY IW02.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 01255 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW02.COM
```

VIEW.BAS must report IW02.COM length 1255 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW02.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```text
lit 7
```

```dos
COPY TIW02.IR SOURCE.IR
```

```dos
CHECK IW02
```

Require:

```text
[LIT][7]
PASS
```

## A rejection or boundary check

Rename SOURCE.IR to an unused HOLD.IR, then run CHECK IW02. Restore the source after the test.

Require:

```text
IR ERROR 0000000000 CODE 6
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Compare the new routine with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
