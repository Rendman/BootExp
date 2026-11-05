+++
title = "20 \u00b7 Quoted byte data"
weight = 20
description = "Preserve string bytes while folding names outside quotes."
download = "A20.ASM"
+++

Readable messages should not require entering every character as a numeric byte.

## The working parts

READLINE retains the original character case. SCAN folds identifier characters and treats quote as a delimiter. DATAITEM reads quoted DB content directly from the physical line, so it is not limited to the ordinary token length. A doubled quote emits one quote; a semicolon inside a string is data.

Strings can be mixed with numeric DB items. DW rejects quoted strings. A string cannot cross a physical line and must close before its terminator. The test deliberately includes lowercase and a semicolon.

## Enter the source

Copy `A19.ASM` to `A20.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `DATASEP:`

Unchanged source immediately before this edit:

```asm
CMP AL,0
JE ZDATAITEM1
JMP SYNTAXBAD
```

Remove this exact source at old physical positions 739–739:

```asm
ZDATAITEM1:
```

Replace it with:

```asm
ZDATAITEM4:
```

The following old source stays in place:

```asm
RET
```

### Change 2 near `DATASEP:`

Unchanged source immediately before this edit:

```asm
CMP AL,44
JE DATAITEM
CMP AL,0
```

Remove this exact source at old physical positions 737–737:

```asm
JE ZDATAITEM1
```

Replace it with:

```asm
JE ZDATAITEM4
```

The following old source stays in place:

```asm
JMP SYNTAXBAD
ZDATAITEM1:
```

### Change 3 near `DATASEP:`

Unchanged source immediately before this edit:

```asm
CALL SCAN
MOV AL,[0CC00H]
CMP AL,44
```

Remove this exact source at old physical positions 735–735:

```asm
JE DATAITEM
```

Replace it with:

```asm
JNE ZDATAITEM3
JMP DATAITEM
ZDATAITEM3:
```

The following old source stays in place:

```asm
CMP AL,0
JE ZDATAITEM1
```

### Change 4 near `DATABYTE:`

Unchanged source immediately before this edit:

```asm
JMP DATASEP
DATABYTE:
CALL BYTEVALUE
```

Insert after old physical line 730.

Insert:

```asm
JMP DATASEP
DATASTRING:
MOV AL,[OP]
CMP AL,0
JE ZDATAITEM1
JMP SYNTAXBAD
ZDATAITEM1:
STRINGBYTE:
LODSB
CMP AL,0
JNE ZDATAITEM2
JMP SYNTAXBAD
ZDATAITEM2:
CMP AL,34
JNE STRINGEMIT
MOV BX,SI
MOV AL,[BX]
CMP AL,34
JNE DATASEP
INC SI
STRINGEMIT:
CALL EMIT
JMP STRINGBYTE
```

The following old source stays in place:

```asm
DATASEP:
CALL SCAN
```

### Change 5 near `DATAITEM:`

Unchanged source immediately before this edit:

```asm

DATAITEM:
CALL SCAN
```

Insert after old physical line 722.

Insert:

```asm
MOV AL,[0CC00H]
CMP AL,34
JE DATASTRING
```

The following old source stays in place:

```asm
CALL VALUE
MOV DL,[OP]
```

### Change 6 near `TOKENBAD:`

Unchanged source immediately before this edit:

```asm
TOKENBAD:
MOV AX,1
JMP ERROR
```

Insert after old physical line 306.

Insert:

```asm
TOKENCHAR:
CMP AL,97
JB TOKENKEPT
CMP AL,122
JA TOKENKEPT
SUB AL,32
TOKENKEPT:
RET
SEPARATOR:
MOV AH,1
CMP AL,44
JNE ZSCAN4
JMP SEPARATORRET
ZSCAN4:
CMP AL,58
JE SEPARATORRET
CMP AL,91
JE SEPARATORRET
CMP AL,93
JE SEPARATORRET
CMP AL,43
JE SEPARATORRET
CMP AL,45
JE SEPARATORRET
CMP AL,40
JE SEPARATORRET
CMP AL,41
JE SEPARATORRET
CMP AL,34
JE SEPARATORRET
MOV AH,0
SEPARATORRET:
RET
```

The following old source stays in place:

```asm

LOOK:
```

### Change 7 near `ZSCAN7:`

Unchanged source immediately before this edit:

```asm
JE SCANBACK
CMP DI,0CC3FH
JAE TOKENBAD
```

Insert after old physical line 289.

Insert:

```asm
CALL TOKENCHAR
```

The following old source stays in place:

```asm
STOSB
JMP SCANMORE
```

### Change 8 near `ZSCAN7:`

Unchanged source immediately before this edit:

```asm
JE SCANBACK
CMP AL,59
JE SCANBACK
```

Remove this exact source at old physical positions 280–286:

```asm
CMP AL,44
JE SCANBACK
CMP AL,58
JE SCANBACK
CMP AL,91
JE SCANBACK
CMP AL,93
```

Replace it with:

```asm
CALL SEPARATOR
CMP AH,1
```

The following old source stays in place:

```asm
JE SCANBACK
CMP DI,0CC3FH
```

### Change 9 near `ZSCAN7:`

Unchanged source immediately before this edit:

```asm
JMP SCANBACK
ZSCAN7:
CMP AL,32
```

Insert after old physical line 276.

Insert:

```asm
JE SCANBACK
CMP AL,9
```

The following old source stays in place:

```asm
JE SCANBACK
CMP AL,59
```

### Change 10 near `SCANMORE:`

Unchanged source immediately before this edit:

```asm
SCANMORE:
LODSB
CMP AL,0
```

Remove this exact source at old physical positions 273–275:

```asm
JNE ZSCAN7
JMP SCANBACK
ZSCAN7:
```

Replace it with:

```asm
JE SCANBACK
```

The following old source stays in place:

```asm
CMP AL,32
JE SCANBACK
```

### Change 11 near `ZSCAN3:`

Unchanged source immediately before this edit:

```asm
JNE ZSCAN3
JMP SCANDONE
ZSCAN3:
```

Remove this exact source at old physical positions 258–269:

```asm
CMP AL,58
JNE ZSCAN4
JMP SCANDONE
ZSCAN4:
CMP AL,91
JNE ZSCAN5
JMP SCANDONE
ZSCAN5:
CMP AL,93
JNE ZSCAN6
JMP SCANDONE
ZSCAN6:
```

There is no replacement source.

The following old source stays in place:

```asm
SCANMORE:
LODSB
```

### Change 12 near `ZSCAN2:`

Unchanged source immediately before this edit:

```asm
JMP SCANEND
ZSCAN2:
STOSB
```

Remove this exact source at old physical positions 254–254:

```asm
CMP AL,44
```

Replace it with:

```asm
CALL SEPARATOR
CMP AH,1
```

The following old source stays in place:

```asm
JNE ZSCAN3
JMP SCANDONE
```

### Change 13 near `ZSCAN2:`

Unchanged source immediately before this edit:

```asm
JNE ZSCAN2
JMP SCANEND
ZSCAN2:
```

Insert after old physical line 252.

Insert:

```asm
CALL TOKENCHAR
```

The following old source stays in place:

```asm
STOSB
CMP AL,44
```

### Change 14 near `SCANSPACE:`

Unchanged source immediately before this edit:

```asm
LODSB
CMP AL,32
JE SCANSPACE
```

Insert after old physical line 244.

Insert:

```asm
CMP AL,9
JE SCANSPACE
```

The following old source stays in place:

```asm
CMP AL,0
JNE ZSCAN1
```

### Change 15 near `ZREADLINE7:`

Unchanged source immediately before this edit:

```asm
JBE ZREADLINE7
JMP READBAD
ZREADLINE7:
```

Remove this exact source at old physical positions 191–198:

```asm
CMP AL,97
JB KEEPCHAR
CMP AL,122
JA KEEPCHAR
SUB AL,32
JMP KEEPCHAR
TABCHAR:
MOV AL,32
```

There is no replacement source.

The following old source stays in place:

```asm
KEEPCHAR:
STOSB
```

### Change 16 near `ZREADLINE5:`

Unchanged source immediately before this edit:

```asm
JMP READFULL
ZREADLINE5:
CMP AL,9
```

Remove this exact source at old physical positions 182–182:

```asm
JE TABCHAR
```

Replace it with:

```asm
JE KEEPCHAR
```

The following old source stays in place:

```asm
CMP AL,32
JAE ZREADLINE6
```

## Build the stopping point

```dos
COPY A20.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 04412 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A20.COM
```

VIEW.BAS must report A20.COM length 4412 bytes. Keep that executable and source together.

## Acceptance check

Create T20.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
DB "Hello; x",13,10,0
```

```dos
COPY T20.ASM SOURCE.ASM
```

```dos
CHECK A20
```

Require:

```text
OK RESULT.COM 00011 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **11 bytes** and these complete contents:

```text
48 65 6C 6C 6F 3B 20 78 0D 0A 00
```

This result is an encoding or data exercise. Inspect its bytes; do not execute it.

## A rejection check

Create X20.ASM with this separate source:

```asm
DB "open
```

```dos
COPY X20.ASM SOURCE.ASM
CHECK A20
```

Require:

```text
ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check saved expression values across EMIT, the unresolved-reference flag, and fixed statement lengths in both passes. Quoted text bypasses mnemonic folding. A reserve count must be checked before multiplication or output.
