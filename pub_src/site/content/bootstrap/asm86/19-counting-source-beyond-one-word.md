+++
title = "07 \u00b7 Counting source beyond one word"
weight = 7
description = "Report source positions with a checked pair of words."
download = "A19.ASM"
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/19-counting-source-beyond-one-word/"
+++

A source file with many comments and definitions can exceed a sixteen-bit line count.

## The working parts

COUNTLINE and COUNTINPUT maintain low/high word pairs and refuse a full-pair wrap. The driver clears the pairs for each pass. NUMBER32 prints ten decimal digits using paired subtraction; ERROR now displays the complete line number.

The byte count records consumed source bytes; a positive short refill is still consumed before reading again. Source counters do not resize an image buffer. A small BASIC text exercise can create a long comment source without requiring a person to type repeated lines.

## Enter the source

Copy `A18.ASM` to `A19.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `UNRESOLVED:`

Unchanged source immediately before this edit:

```asm

UNRESOLVED:
DB 0
```

Insert after old physical line 1827.

Insert:

```asm

LINEHI:
DW 0

INBYTES:
DW 0

INBYTEHI:
DW 0

N32LO:
DW 0

N32HI:
DW 0

D32LO:
DW 0

D32HI:
DW 0

DIV32:
DW 15258,51712,1525,57600,152,38528
DW 15,16960,1,34464,0,10000
DW 0,1000,0,100,0,10
DW 0,1

DIV32END:
```

### Change 2 near `DEFINITIONCLEAR:`

Unchanged source immediately before this edit:

```asm
MOV ES:[BX],AX
RET
```

Insert after old physical line 1600.

Insert:

```asm
COUNTLINE:
MOV AX,[LINENO]
CMP AX,0FFFFH
JNE LINELOW
MOV AX,[LINEHI]
CMP AX,0FFFFH
JE COUNTFULL
INC AX
MOV [LINEHI],AX
MOV AX,0
MOV [LINENO],AX
RET
LINELOW:
INC AX
MOV [LINENO],AX
RET
COUNTFULL:
MOV AX,5
JMP ERROR

COUNTINPUT:
MOV AX,[INBYTES]
CMP AX,0FFFFH
JNE INPUTLOW
MOV AX,[INBYTEHI]
CMP AX,0FFFFH
JE COUNTFULL
INC AX
MOV [INBYTEHI],AX
MOV AX,0
MOV [INBYTES],AX
RET
INPUTLOW:
INC AX
MOV [INBYTES],AX
RET

NUMBER32:
PUSH AX
PUSH BX
PUSH CX
PUSH DX
PUSH SI
MOV [N32LO],AX
MOV [N32HI],DX
MOV SI,DIV32
N32PLACE:
MOV BX,SI
MOV AX,[BX]
MOV [D32HI],AX
ADD BX,2
MOV AX,[BX]
MOV [D32LO],AX
MOV CX,0
N32SUB:
MOV AX,[N32HI]
MOV DX,[D32HI]
CMP AX,DX
JAE ZNUMBER321
JMP N32DIGIT
ZNUMBER321:
JA N32TAKE
MOV AX,[N32LO]
MOV DX,[D32LO]
CMP AX,DX
JAE ZNUMBER322
JMP N32DIGIT
ZNUMBER322:
N32TAKE:
MOV AX,[N32LO]
MOV DX,[D32LO]
SUB AX,DX
MOV [N32LO],AX
JAE N32NOBORROW
MOV AX,[N32HI]
DEC AX
MOV [N32HI],AX
N32NOBORROW:
MOV AX,[N32HI]
MOV DX,[D32HI]
SUB AX,DX
MOV [N32HI],AX
INC CX
JMP N32SUB
N32DIGIT:
MOV DL,CL
ADD DL,48
MOV AH,2
INT 21H
ADD SI,4
CMP SI,DIV32END
JAE ZNUMBER323
JMP N32PLACE
ZNUMBER323:
POP SI
POP DX
POP CX
POP BX
POP AX
RET
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 3 near `ERROR:`

Unchanged source immediately before this edit:

```asm
MOV DX,ERRMSG
CALL TEXT
MOV AX,[LINENO]
```

Remove this exact source at old physical positions 1107–1107:

```asm
CALL NUMBER
```

Replace it with:

```asm
MOV DX,[LINEHI]
CALL NUMBER32
```

The following old source stays in place:

```asm
MOV DX,CODEMSG
CALL TEXT
```

### Change 4 near `READFAIL:`

Unchanged source immediately before this edit:

```asm
READBAD:
MOV AX,6
READFAIL:
```

Remove this exact source at old physical positions 237–242:

```asm
MOV DX,[LINENO]
CMP DX,0FFFFH
JE READLIMIT
INC DX
READLIMIT:
MOV [LINENO],DX
```

Replace it with:

```asm
PUSH AX
CALL COUNTLINE
POP AX
```

The following old source stays in place:

```asm
JMP ERROR
```

### Change 5 near `LINEEND:`

Unchanged source immediately before this edit:

```asm
LINEEND:
MOV AL,0
STOSB
```

Remove this exact source at old physical positions 218–225:

```asm
MOV AX,[LINENO]
INC AX
CMP AX,0
JNE LINECOUNTSAFE
MOV AX,5
JMP ERROR
LINECOUNTSAFE:
MOV [LINENO],AX
```

Replace it with:

```asm
CALL COUNTLINE
```

The following old source stays in place:

```asm
MOV AX,1
RET
```

### Change 6 near `BUFFERBYTE:`

Unchanged source immediately before this edit:

```asm
MOV AX,[RDPOS]
INC AX
MOV [RDPOS],AX
```

Insert after old physical line 137.

Insert:

```asm
CALL COUNTINPUT
```

The following old source stays in place:

```asm
MOV AX,1
RET
```

### Change 7 near `PASSSTART:`

Unchanged source immediately before this edit:

```asm
MOV [PC],AX
MOV AX,0
MOV [LINENO],AX
```

Insert after old physical line 19.

Insert:

```asm
MOV [LINEHI],AX
MOV [INBYTES],AX
MOV [INBYTEHI],AX
```

The following old source stays in place:

```asm
MOV [RDPOS],AX
MOV [RDLEN],AX
```

## Build the stopping point

```dos
COPY A19.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 04286 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A19.COM
```

VIEW.BAS must report A19.COM length 4286 bytes. Keep that executable and source together.

## Acceptance check

Create T19.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
DB 1
```

```dos
COPY T19.ASM SOURCE.ASM
```

```dos
CHECK A19
```

Require:

```text
OK RESULT.COM 00001 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **1 bytes** and these complete contents:

```text
01
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X19.ASM with this separate source:

```asm
UNKNOWN
```

```dos
COPY X19.ASM SOURCE.ASM
CHECK A19
```

Require:

```text
ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

## A long source, a small result

Enter LONGSRC.BAS:

```basic
10 OPEN "SOURCE.ASM" FOR OUTPUT AS #1
20 FOR I=1 TO 65536
30 PRINT #1,";"
40 NEXT I
50 PRINT #1,"DB 1"
60 CLOSE #1
70 PRINT "SOURCE.ASM READY"
```

Run it in BASIC, require SOURCE.ASM READY, and return to DOS with SYSTEM. Its closed text file includes BASIC's ordinary source Control-Z. CHECK A19 must report `OK RESULT.COM 00001 bytes` and PASS. VIEW.BAS must show exactly `01`. The comments exceed a word-sized physical-line count while the output stays small; do not execute this data.

Change BASIC line 50 to `50 PRINT #1,"UNKNOWN"`, RUN again, and return to DOS. CHECK A19 must report `ERROR 0000065537 CODE 1` and FAIL. The one-byte accepted RESULT.COM must remain unchanged. Restore the original line 50 before another run.

An unexpected PASS fails this rejection test.

## If the result differs

Check ES at helper exits, the saved page segment and offset, record padding, and the complete spelling comparison. Check carry after every DOS memory call. A successful allocation does not initialize its contents.
