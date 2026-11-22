+++
title = "02 \u00b7 Tokens without a complete source buffer"
weight = 2
description = "Fold token spellings while preserving the raw line for quoted data."
download = "IR02.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/02-seeing-the-tokens/", "/bootstrap/ir86/038-iw-tokens-without-a-complete-source-buffer/"]
+++

I can read the input. Now I need to separate an operation name from its operand without losing my place. I shall try a lowercase `lit 7` and have the scanner show the two tokens it found. Later, quoted text will need its original spelling, so folding a token must leave the raw line available.

**Starting source:** `IR01.ASM`. **Save as:** `IR02.ASM`. **Build with:** `ASMAKEEP.COM`.

## How it works

Fold token spellings while preserving the raw line for quoted data.

## Enter the source

Copy IR01.ASM to IR02.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 20

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

### Edit at old physical position 16

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

### Edit at old physical position 13

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
CHECK ASMAKEEP IR02.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 02564 bytes`. Save RESULT.COM as IR02.COM. VIEW.BAS must show length 2564.

Create T02.IR:

```text
lit 7
```

```dos
CHECK IR02 T02.IR RESULT.ASM
```

Require:

```text
[LIT][7]PASS
```

`[LIT][7]` shows that the scanner found a complete operation spelling and a separate operand. I can now build the output side while keeping this small scanner test as an accepted stopping point.

## Check the new boundary

Choose an absent disk filename, ABSENT.IR, and run:

```dos
CHECK IR02 ABSENT.IR RESULT.ASM
```

Require:

```text
IR ERROR 0000000000 CODE 6
FAIL
```

An unexpected PASS fails this check. This checkpoint creates no result file; an existing selected result must remain untouched.

