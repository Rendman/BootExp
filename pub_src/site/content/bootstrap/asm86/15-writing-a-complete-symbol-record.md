+++
title = "03 \u00b7 Writing a complete symbol record"
weight = 3
description = "Initialize spelling, value, link, flags, and kind together."
download = "A15.ASM"
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/15-writing-a-complete-symbol-record/"
+++

Allocated RAM is not guaranteed to contain zeroes.

## The working parts

RECORDWRITE clears a forty-byte record, copies the current zero-terminated name, writes DEFVALUE, the prior bucket HEADID, and DEFTYPE, then installs SYMID as the bucket head. Name padding and pass flags therefore have known values.

The diagnostic creates a PAGED record with value 12345 and reads it through SYMPTR. It restores ES before comparing the result with 12345. The record writer changes the working registers and record/bucket cursors; the input name and explicit fields are its interface.

## Enter the source

Copy `A14.ASM` to `A15.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `HASHSEG:`

Unchanged source immediately before this edit:

```asm

HASHSEG:
DW 0
```

Insert after old physical line 1698.

Insert:

```asm

TESTNAME:
DB 80,65,71,69,68,0
```

### Change 2 near `RECORDPTR:`

Unchanged source immediately before this edit:

```asm
RECORDPTR:
DW 0
```

Insert after old physical line 1693.

Insert:

```asm
BUCKET:
DW 0

HEADID:
DW 0

SYMID:
DW 0

DEFVALUE:
DW 0

DEFTYPE:
DW 0
```

The following old source stays in place:

```asm
MEMSEGS:
DW 0,0,0,0,0,0,0,0
```

### Change 3 near `EARLYTEST:`

Unchanged source immediately before this edit:

```asm
MOV AX,ES:[BX]
MOV DX,CS
MOV ES,DX
```

Remove this exact source at old physical positions 1483–1483:

```asm
CMP AX,42
```

Replace it with:

```asm
CMP AX,12345
```

The following old source stays in place:

```asm
JE EARLYPASS
MOV AX,7
```

### Change 4 near `EARLYTEST:`

Unchanged source immediately before this edit:

```asm
EARLYTEST:
MOV AX,8192
CALL SYMPTR
```

Remove this exact source at old physical positions 1478–1479:

```asm
MOV AX,42
MOV ES:[BX],AX
```

Replace it with:

```asm
ADD BX,32
```

The following old source stays in place:

```asm
MOV AX,ES:[BX]
MOV DX,CS
```

### Change 5 near `EARLYTEST:`

Unchanged source immediately before this edit:

```asm
RET

EARLYTEST:
```

Insert after old physical line 1475.

Insert:

```asm
PUSH SI
MOV SI,TESTNAME
MOV DI,4080H
CALL COPYZ
POP SI
MOV AX,8192
MOV [SYMID],AX
MOV AX,12345
MOV [DEFVALUE],AX
MOV AX,0
MOV [DEFTYPE],AX
MOV [HEADID],AX
MOV [BUCKET],AX
MOV AX,[SYMID]
CALL RECORDWRITE
```

The following old source stays in place:

```asm
MOV AX,8192
CALL SYMPTR
```

### Change 6 near `SYMOFFSET:`

Unchanged source immediately before this edit:

```asm
MOV [RECORDPTR],BX
RET
```

Insert after old physical line 1474.

Insert:

```asm
RECORDWRITE:
CALL SYMPTR
MOV DI,BX
MOV CX,40
MOV AL,0
DEFINITIONCLEAR:
STOSB
DEC CX
JNE DEFINITIONCLEAR
MOV DI,[RECORDPTR]
PUSH SI
MOV SI,4080H
CALL COPYZ
POP SI
MOV BX,[RECORDPTR]
ADD BX,32
MOV AX,[DEFVALUE]
MOV ES:[BX],AX
ADD BX,2
MOV AX,[HEADID]
MOV ES:[BX],AX
ADD BX,4
MOV AX,[DEFTYPE]
MOV ES:[BX],AX
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,[BUCKET]
MOV AX,[SYMID]
MOV ES:[BX],AX
RET
```

The following old source stays in place:

```asm
EARLYTEST:
MOV AX,8192
```

## Build the stopping point

```dos
COPY A15.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 03889 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A15.COM
```

VIEW.BAS must report A15.COM length 3889 bytes. Keep that executable and source together.

## Acceptance check

Create T15.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T15.ASM SOURCE.ASM
```

```dos
CHECK A15
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

Create X15.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X15.ASM SOURCE.ASM
CHECK A15
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
