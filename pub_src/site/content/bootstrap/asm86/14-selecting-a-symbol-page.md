+++
title = "02 \u00b7 Selecting a symbol page"
weight = 2
description = "Translate a stable symbol ID into a page and offset."
download = "A14.ASM"
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/14-selecting-a-symbol-page/"
+++

My memory sketch now has boxes outside the main segment. A record number must lead me to both the right box and the right place inside it. I'll check the last record slot in the last page before trusting that calculation with any source names.

## The working parts

SYMPTR takes an ID from one through 8192 in AX. Subtracting one yields a page number in groups of 1024 and an index within that page. Forty times the index is the record offset in BX; ES selects its allocated page. RECORDPTR saves that offset.

The entry diagnostic selects ID 8192, writes and reads word 42, restores ES, and compares the loaded word with 42 and rejects a mismatch. It uses the final record slot in the final page. Ordinary assembler processing still uses the retained seed table; the test does not make an arbitrary offset into a main-segment pointer.

## Enter the source

Copy `A13.ASM` to `A14.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `MEMCOUNT:`

Unchanged source immediately before this edit:

```asm
MEMCOUNT:
DW 0
```

Insert after old physical line 1836.

Insert:

```asm
RECORDPTR:
DW 0
```

The following old source stays in place:

```asm
MEMSEGS:
DW 0,0,0,0,0,0,0,0
```

### Change 2 near `MEMFREED:`

Unchanged source immediately before this edit:

```asm
MOV ES,AX
RET
```

Insert after old physical line 1452.

Insert:

```asm
SYMPTR:
DEC AX
MOV DX,0
SYMPAGE:
CMP AX,1024
JB SYMOFFSET
SUB AX,1024
ADD DX,2
JMP SYMPAGE
SYMOFFSET:
PUSH AX
MOV BX,MEMSEGS
ADD BX,DX
MOV AX,[BX]
MOV ES,AX
POP AX
ADD AX,AX
ADD AX,AX
ADD AX,AX
MOV CX,AX
ADD AX,AX
ADD AX,AX
ADD AX,CX
MOV BX,AX
MOV [RECORDPTR],BX
RET

EARLYTEST:
MOV AX,8192
CALL SYMPTR
MOV AX,42
MOV ES:[BX],AX
MOV AX,ES:[BX]
MOV DX,CS
MOV ES,DX
CMP AX,42
JE EARLYPASS
MOV AX,7
JMP ERROR
EARLYPASS:
RET
```

The following old source stays in place:

```asm
CMDINIT:
MOV SI,81H
```

### Change 3 near `ROOM:`

Unchanged source immediately before this edit:

```asm
ROOM:
CALL CMDFILES
CALL MEMINIT
```

Insert after old physical line 10.

Insert:

```asm
CALL EARLYTEST
```

The following old source stays in place:

```asm
CALL PREFLIGHT
MOV AL,1
```

## Build the stopping point

```dos
CHECK ASM1 A14.ASM RESULT.COM
```

Require `OK RESULT.COM 04185 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A14.COM
```

VIEW.BAS must report A14.COM length 4185 bytes. Keep that executable and source together.

## Check the new memory routines

The small T input below checks that ordinary assembly still works. For a direct check of the added routines, make a separate diagnostic copy. Keep the accepted construction source and executable for the next article.

Copy `A14.ASM` to `M14.ASM`. The [complete diagnostic source](../../../downloads/tools/asm86/M14.ASM) is also available. Apply the edits to your own typed source to check your routines; the download is a reference copy. These edits use labels and existing source as locators; no physical line numbers are needed.

The case table gives each ID an independently expected page-word offset and record offset. It checks ES, BX and RECORDPTR directly; it never uses SYMPTR to calculate its expected answer or to read back a write.

| ID | Symbol page | Record offset |
|---|---|---|
| 1 | 0 | 0 |
| 2 | 0 | 40 |
| 1023 | 0 | 40880 |
| 1024 | 0 | 40920 |
| 1025 | 1 | 0 |
| 1026 | 1 | 40 |
| 8191 | 7 | 40880 |
| 8192 | 7 | 40920 |

Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Diagnostic edit 1 · `CMDINIT:`

Find the unique label `CMDINIT:`. Insert the new source immediately before this existing label:

```asm
CMDINIT:
```

Insert:

```asm
PROBECASES:
DW 1,0,0
DW 2,0,40
DW 1023,0,40880
DW 1024,0,40920
DW 1025,2,0
DW 1026,2,40
DW 8191,14,40880
DW 8192,14,40920
PROBEOFF:
DW 0
PROBESEG:
DW 0
PROBEPAGEOK:
DB 80,65,71,69,32,66,79,85,78,68,65,82,73,69,83,32,80,65,83,83,13,10,36
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
MOV AX,8192
CALL SYMPTR
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AX,42
MOV ES:[BX],AX
MOV AX,ES:[BX]
MOV DX,CS
MOV ES,DX
CMP AX,42
JE EARLYPASS
MOV AX,7
JMP ERROR
EARLYPASS:
```

With:

```asm
MOV AX,BX
MOV DX,[PROBEOFF]
CALL PROBEEQUAL
MOV AX,ES
MOV DX,[PROBESEG]
CALL PROBEEQUAL
MOV AX,[RECORDPTR]
MOV DX,[PROBEOFF]
CALL PROBEEQUAL
ADD DI,6
DEC BP
JNE PROBECASE
MOV AX,CS
MOV ES,AX
MOV DX,PROBEPAGEOK
CALL TEXT
```

### Diagnostic edit 3 · `EARLYTEST:`

Find the unique label `EARLYTEST:`, then follow this unchanged source through its last displayed instruction:

```asm
EARLYTEST:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AX,8192
```

With:

```asm
MOV DI,PROBECASES
MOV BP,8
PROBECASE:
MOV BX,DI
MOV AX,[BX]
PUSH AX
ADD BX,2
MOV DX,[BX]
ADD BX,2
MOV AX,[BX]
MOV [PROBEOFF],AX
MOV BX,MEMSEGS
ADD BX,DX
MOV AX,[BX]
MOV [PROBESEG],AX
POP AX
```

### Build and run M14

```dos
CHECK ASM1 M14.ASM M14.COM
CHECK M14 T14.ASM RESULT.COM
```

Require `OK M14.COM 04364 bytes` and PASS from the build. The diagnostic run must show:

```text
PAGE BOUNDARIES PASS
OK RESULT.COM 00011 bytes
PASS
```

MEMORY TEST FAILED, an unexpected error, or a missing diagnostic message fails this check.

Continue the construction from your accepted A14.ASM, not M14.ASM.

## Ordinary assembly regression check

Create T14.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
CHECK A14 T14.ASM RESULT.COM
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

Create X14.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
CHECK A14 X14.ASM RESULT.COM
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
