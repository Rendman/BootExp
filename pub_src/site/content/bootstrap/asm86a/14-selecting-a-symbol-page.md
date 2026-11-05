+++
title = "14 \u00b7 Selecting a symbol page"
weight = 14
description = "Translate a stable symbol ID into a page and offset."
download = "A14.ASM"
+++

A page selector and offset must travel together inside a table helper.

## The working parts

SYMPTR takes an ID from one through 8192 in AX. Subtracting one yields a page number in groups of 1024 and an index within that page. Forty times the index is the record offset in BX; ES selects its allocated page. RECORDPTR saves that offset.

The entry diagnostic selects ID 8192, writes and reads word 42, restores ES, and displays 00042. It uses the final record slot in the final page. Ordinary assembler processing still uses the retained seed table; the test does not make an arbitrary offset into a main-segment pointer.

## Enter the source

Copy `A13.ASM` to `A14.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `HASHSEG:`

Unchanged source immediately before this edit:

```asm

HASHSEG:
DW 0
```

Remove this exact source at old physical positions 1664–1666:

```asm

READYMSG:
DB 77,69,77,79,82,89,32,82,69,65,68,89,13,10,36
```

There is no replacement source.

### Change 2 near `MEMCOUNT:`

Unchanged source immediately before this edit:

```asm
MEMCOUNT:
DW 0
```

Insert after old physical line 1658.

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

### Change 3 near `EARLYTEST:`

Unchanged source immediately before this edit:

```asm
RET

EARLYTEST:
```

Remove this exact source at old physical positions 1449–1449:

```asm
MOV DX,READYMSG
```

Replace it with:

```asm
MOV AX,8192
CALL SYMPTR
MOV AX,42
MOV ES:[BX],AX
MOV AX,ES:[BX]
MOV DX,CS
MOV ES,DX
CALL NUMBER
MOV DX,NEWLINE
```

The following old source stays in place:

```asm
CALL TEXT
RET
```

### Change 4 near `MEMFREED:`

Unchanged source immediately before this edit:

```asm
MOV ES,AX
RET
```

Insert after old physical line 1447.

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
```

The following old source stays in place:

```asm
EARLYTEST:
MOV DX,READYMSG
```

## Build the stopping point

```dos
COPY A14.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 03784 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A14.COM
```

VIEW.BAS must report A14.COM length 3784 bytes. Keep that executable and source together.

## Acceptance check

Create T14.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T14.ASM SOURCE.ASM
```

```dos
CHECK A14
```

Require:

```text
00042
OK RESULT.COM 00011 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **11 bytes** and these complete contents:

```text
B2 41 B4 02 CD 21 B8 00 4C CD 21
```

This fixture is a complete program. Save it before another assembly and execute it:

```dos
COPY RESULT.COM TRY.COM
CHECK TRY
```

It displays "A" and the checker reports PASS.

## A rejection check

Create X14.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X14.ASM SOURCE.ASM
CHECK A14
```

Require:

```text
00042
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check ES at helper exits, the saved page segment and offset, record padding, and the complete spelling comparison. Check carry after every DOS memory call. A successful allocation does not initialize its contents.
