+++
title = "03 \u00b7 Writing a complete symbol record"
weight = 3
description = "Initialize spelling, value, link, flags, and kind together."
download = "A15.ASM"
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/15-writing-a-complete-symbol-record/"
+++

DOS has given me storage, but it has not promised what bytes are already there. I sketch one complete symbol record in the notebook and mark what every field should contain. The writer must establish all of it, including the unused name bytes.

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

Insert after old physical line 1887.

Insert:

```asm

TESTNAME:
DB 80,65,71,69,68,0
```

The following old source stays in place:

```asm

CMDCOUNT:
```

### Change 2 near `RECORDPTR:`

Unchanged source immediately before this edit:

```asm
RECORDPTR:
DW 0
```

Insert after old physical line 1882.

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

Remove this exact source at old physical positions 1489–1489:

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

Remove this exact source at old physical positions 1484–1485:

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

Insert after old physical line 1481.

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

Insert after old physical line 1480.

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
CHECK ASM1 A15.ASM RESULT.COM
```

Require `OK RESULT.COM 04327 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A15.COM
```

VIEW.BAS must report A15.COM length 4327 bytes. Keep that executable and source together.

## Check the new memory routines

The small T input below checks that ordinary assembly still works. For a direct check of the added routines, make a separate diagnostic copy. Keep the accepted construction source and executable for the next article.

Copy `A15.ASM` to `M15.ASM`. The [complete diagnostic source](../../../downloads/tools/asm86/M15.ASM) is also available. Apply the edits to your own typed source to check your routines; the download is a reference copy. These edits use labels and existing source as locators; no physical line numbers are needed.

The test fills record 1026 with A5H and places guard bytes before and after it. It writes a 31-character spelling, value 1234H, link 8192 and kind 1 into bucket offset 8190. It independently selects page 1, offset 40 and compares all forty bytes against a literal expected record. It then overwrites the spelling with Q, changes the fields and dirties the pass flags; every name-padding and flag byte must become zero. Both runs verify the guards, the bucket head, its neighbor and bucket zero. The long spelling exercises the record writer directly; it does not extend the seed parser's accepted identifier length.

Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Diagnostic edit 1 · `CMDINIT:`

Find the unique label `CMDINIT:`. Insert the new source immediately before this existing label:

```asm
CMDINIT:
```

Insert:

```asm
PROBELONG:
DB 65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80
DB 81,82,83,84,85,86,87,88,89,90,65,66,67,68,69,0
PROBESHORT:
DB 81,0
PROBEEXPECT1:
DB 65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80
DB 81,82,83,84,85,86,87,88,89,90,65,66,67,68,69,0
DW 1234H,8192,0,1
PROBEEXPECT2:
DB 81,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
DB 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
DW 0BEEFH,1025,0,0
PROBERECOK:
DB 82,69,67,79,82,68,32,70,73,69,76,68,83,32,65,78,68,32,71,85,65,82,68,83,32,80,65,83,83,13,10,36
PROBEEQUAL:
CMP AX,DX
JE PROBEEQUALOK
JMP PROBEFAIL
PROBEEQUALOK:
RET
PROBEFAIL:
MOV AX,CS
MOV ES,AX
CALL MEMFREE
MOV DX,PROBEFAILMSG
CALL TEXT
MOV AX,4C01H
INT 21H
PROBEFAILMSG:
DB 77,69,77,79,82,89,32,84,69,83,84,32,70,65,73,76,69,68,13,10,36
```

### Diagnostic edit 2 · `EARLYTEST:`

Find the unique label `EARLYTEST:`, then follow this unchanged source through its last displayed instruction:

```asm
EARLYTEST:
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
MOV AX,8192
CALL SYMPTR
ADD BX,32
MOV AX,ES:[BX]
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV DX,CS
MOV ES,DX
CMP AX,12345
JE EARLYPASS
MOV AX,7
JMP ERROR
EARLYPASS:
```

With:

```asm
MOV DX,1026
CALL PROBEEQUAL
MOV BX,8188
MOV AX,ES:[BX]
MOV DX,55AAH
CALL PROBEEQUAL
MOV BX,0
MOV AX,ES:[BX]
MOV DX,0
CALL PROBEEQUAL
```

### Diagnostic edit 3 · `EARLYTEST:`

Find the unique label `EARLYTEST:`, then follow this unchanged source through its last displayed instruction:

```asm
EARLYTEST:
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

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AX,8192
CALL SYMPTR
ADD BX,32
```

With:

```asm
MOV SI,PROBEEXPECT1
CALL PROBERECORD
CALL PROBERECPAGE
MOV BX,76
MOV AX,0FFFFH
MOV ES:[BX],AX
MOV AX,CS
MOV ES,AX
MOV SI,PROBESHORT
MOV DI,4080H
CALL COPYZ
MOV AX,0BEEFH
MOV [DEFVALUE],AX
MOV AX,1025
MOV [HEADID],AX
MOV AX,0
MOV [DEFTYPE],AX
MOV AX,[SYMID]
CALL RECORDWRITE
MOV SI,PROBEEXPECT2
CALL PROBERECORD
MOV AX,CS
MOV ES,AX
MOV DX,PROBERECOK
CALL TEXT
RET
PROBERECPAGE:
MOV BX,MEMSEGS
ADD BX,2
MOV AX,[BX]
MOV ES,AX
RET
PROBERECORD:
CALL PROBERECPAGE
MOV BX,40
MOV CX,40
PROBERECBYTE:
LODSB
MOV AH,0
MOV DL,ES:[BX]
MOV DH,0
CALL PROBEEQUAL
INC BX
DEC CX
JNE PROBERECBYTE
MOV BX,39
MOV AL,ES:[BX]
MOV AH,0
MOV DX,5AH
CALL PROBEEQUAL
MOV BX,80
MOV AL,ES:[BX]
MOV AH,0
MOV DX,6BH
CALL PROBEEQUAL
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,8190
```

### Diagnostic edit 4 · `EARLYTEST:`

Find the unique label `EARLYTEST:`, then follow this unchanged source through its last displayed instruction:

```asm
EARLYTEST:
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
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV [HEADID],AX
```

With:

```asm
MOV AX,8190
```

### Diagnostic edit 5 · `EARLYTEST:`

Find the unique label `EARLYTEST:`, then follow this unchanged source through its last displayed instruction:

```asm
EARLYTEST:
PUSH SI
MOV SI,TESTNAME
MOV DI,4080H
CALL COPYZ
POP SI
MOV AX,8192
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV [SYMID],AX
MOV AX,12345
MOV [DEFVALUE],AX
MOV AX,0
```

With:

```asm
MOV [HEADID],AX
MOV AX,1
```

### Diagnostic edit 6 · `EARLYTEST:`

Find the unique label `EARLYTEST:`, then follow this unchanged source through its last displayed instruction:

```asm
EARLYTEST:
PUSH SI
MOV SI,TESTNAME
MOV DI,4080H
CALL COPYZ
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
POP SI
```

With:

```asm
MOV AX,1026
MOV [SYMID],AX
MOV AX,1234H
MOV [DEFVALUE],AX
```

### Diagnostic edit 7 · `EARLYTEST:`

Find the unique label `EARLYTEST:`, then follow this unchanged source through its last displayed instruction:

```asm
EARLYTEST:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
PUSH SI
MOV SI,TESTNAME
```

With:

```asm
CALL PROBERECPAGE
MOV BX,39
MOV AL,5AH
MOV ES:[BX],AL
MOV BX,80
MOV AL,6BH
MOV ES:[BX],AL
MOV BX,40
MOV CX,40
MOV AL,0A5H
PROBERECDIRTY:
MOV ES:[BX],AL
INC BX
DEC CX
JNE PROBERECDIRTY
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,8188
MOV AX,55AAH
MOV ES:[BX],AX
MOV BX,8190
MOV AX,8192
MOV ES:[BX],AX
MOV AX,CS
MOV ES,AX
MOV SI,PROBELONG
```

### Build and run M15

```dos
CHECK ASM1 M15.ASM M15.COM
CHECK M15 T15.ASM RESULT.COM
```

Require `OK M15.COM 04739 bytes` and PASS from the build. The diagnostic run must show:

```text
RECORD FIELDS AND GUARDS PASS
OK RESULT.COM 00011 bytes
PASS
```

MEMORY TEST FAILED, an unexpected error, or a missing diagnostic message fails this check.

Continue the construction from your accepted A15.ASM, not M15.ASM.

## Ordinary assembly regression check

Create T15.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
CHECK A15 T15.ASM RESULT.COM
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
CHECK A15 X15.ASM RESULT.COM
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with C:\DOS\FC.EXE /B if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check ES at helper exits, the saved page segment and offset, record padding, and the complete spelling comparison. Check carry after every DOS memory call. A successful allocation does not initialize its contents.
