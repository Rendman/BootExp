+++
title = "02 \u00b7 Tokens without a complete source buffer"
weight = 2
description = "Fold token spellings while preserving the raw line for quoted data."
download = "IR02.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/02-seeing-the-tokens/", "/bootstrap/ir86/038-iw-tokens-without-a-complete-source-buffer/"]
+++

Fold token spellings while preserving the raw line for quoted data.

## Enter the source

Copy IR01.ASM to IR02.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 19

Unchanged source before the edit:

```asm
MOV DL,AL
MOV AH,2
INT 21H
```

Remove:

```asm
JMP SHOWBYTE
SHOWEND:
MOV DX,NEWLINE
CALL TEXT
```

Insert in its place:

```asm
JMP TOKENBYTE
TOKENEND:
MOV DL,93
MOV AH,2
INT 21H
POP SI
JMP SHOWTOKEN
```

The following old source remains:

```asm
JMP READNEXT
READDONE:
```

### Edit at old physical position 15

Unchanged source before the edit:

```asm
SHOWBYTE:
LODSB
CMP AL,0
```

Remove:

```asm
JE NEAR SHOWEND
```

Insert in its place:

```asm
JE NEAR TOKENEND
```

The following old source remains:

```asm
MOV DL,AL
MOV AH,2
```

### Edit at old physical position 12

Unchanged source before the edit:

```asm
CMP AX,0
JE NEAR READDONE
MOV SI,0C800H
```

Remove:

```asm
SHOWBYTE:
```

Insert in its place:

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

The following old source remains:

```asm
LODSB
CMP AL,0
```

## Build and check

```dos
COPY IR02.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 02072 bytes`. Save RESULT.COM as IR02.COM. VIEW.BAS must show length 2072.

Create T02.IR:

```text
lit 7
```

```dos
COPY T02.IR SOURCE.IR
```

```dos
CHECK IR02
```

Require:

```text
[LIT][7]PASS
```

## Check the new boundary

Temporarily rename SOURCE.IR to HOLD.TXT and run CHECK IR02. Restore the source afterward. Require:

```text
IR ERROR 0000000000 CODE 6
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

