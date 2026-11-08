+++
title = "04 \u00b7 Looking up the complete spelling"
weight = 4
description = "Use buckets to find candidates and compare every character."
download = "A16.ASM"
cartoon = "asm86a-cloakroom.png"
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/16-looking-up-the-complete-spelling/"
+++

A hash narrows a search but cannot decide whether two names are equal.

## The working parts

SYMLOOK folds the name into a sixteen-bit rotating hash, selects one of 4096 word buckets, then follows record IDs. Every candidate is compared with the complete spelling through its zero terminator. HEADID retains the original bucket head while SYMID follows the chain.

The entry test looks up PAGED before insertion, writes its record into the selected bucket, then looks it up again and compares the saved value with 12345 and rejects a mismatch. It restores the line cursor and ES. Colliding names remain distinct; no name is accepted merely because its hash matches.

## Enter the source

Copy `A15.ASM` to `A16.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `EARLYTEST:`

Unchanged source immediately before this edit:

```asm
MOV [BUCKET],AX
MOV AX,[SYMID]
CALL RECORDWRITE
```

Remove this exact source at old physical positions 1522–1522:

```asm
MOV AX,8192
```

Replace it with:

```asm
CALL SYMLOOK
MOV AX,[SYMID]
```

The following old source stays in place:

```asm
CALL SYMPTR
ADD BX,32
```

### Change 2 near `EARLYTEST:`

Unchanged source immediately before this edit:

```asm
MOV [DEFTYPE],AX
MOV [HEADID],AX
MOV [BUCKET],AX
```

Insert after old physical line 1519.

Insert:

```asm
CALL SYMLOOK
MOV AX,8192
MOV [SYMID],AX
```

The following old source stays in place:

```asm
MOV AX,[SYMID]
CALL RECORDWRITE
```

### Change 3 near `EARLYTEST:`

Unchanged source immediately before this edit:

```asm
MOV DI,4080H
CALL COPYZ
POP SI
```

Insert after old physical line 1511.

Insert:

```asm
CALL SYMLOOK
```

The following old source stays in place:

```asm
MOV AX,8192
MOV [SYMID],AX
```

### Change 4 near `DEFINITIONCLEAR:`

Unchanged source immediately before this edit:

```asm
MOV ES:[BX],AX
RET
```

Insert after old physical line 1505.

Insert:

```asm
SYMLOOK:
PUSH SI
MOV SI,4080H
MOV AX,0
SYMHASH:
MOV BX,SI
MOV DL,[BX]
MOV DH,0
CMP DX,0
JE SYMHASHED
MOV CX,5
HASHROTATE:
ADD AX,AX
JAE HASHNOCARRY
INC AX
HASHNOCARRY:
DEC CX
JNE HASHROTATE
XOR AX,DX
INC SI
JMP SYMHASH
SYMHASHED:
AND AX,4095
ADD AX,AX
MOV [BUCKET],AX
MOV BX,AX
MOV AX,[HASHSEG]
MOV ES,AX
MOV AX,ES:[BX]
MOV [HEADID],AX
SYMFIND:
MOV [SYMID],AX
CMP AX,0
JNE ZSYMLOOK1
JMP SYMMISS
ZSYMLOOK1:
CALL SYMPTR
MOV DI,BX
MOV SI,4080H
SYMCHECKCHAR:
LODSB
MOV BX,DI
MOV DL,ES:[BX]
CMP AL,DL
JNE SYMNEXTID
CMP AL,0
JE SYMFOUND
INC DI
JMP SYMCHECKCHAR
SYMNEXTID:
MOV BX,[RECORDPTR]
ADD BX,34
MOV AX,ES:[BX]
JMP SYMFIND
SYMMISS:
MOV AX,0
MOV [SYMID],AX
SYMFOUND:
MOV AX,CS
MOV ES,AX
POP SI
RET
```

The following old source stays in place:

```asm
EARLYTEST:
PUSH SI
```

## Build the stopping point

```dos
COPY A16.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 04034 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A16.COM
```

VIEW.BAS must report A16.COM length 4034 bytes. Keep that executable and source together.

## Acceptance check

Create T16.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T16.ASM SOURCE.ASM
```

```dos
CHECK A16
```

Require:

```text
OK RESULT.COM 00011 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **11 bytes** and these complete contents:

```text
B2 41 B4 02 CD 21 B8 00 4C CD 21
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X16.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X16.ASM SOURCE.ASM
CHECK A16
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check ES at helper exits, the saved page segment and offset, record padding, and the complete spelling comparison. Check carry after every DOS memory call. A successful allocation does not initialize its contents.
