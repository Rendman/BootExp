+++
title = "06 \u00b7 Physical source lines"
weight = 6
description = "Bound each line and handle CR, LF, and the last line at EOF."
download = "AS06.ASM"
aliases = ["/bootstrap/asm86/07-physical-source-lines/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/06-physical-source-lines/"
+++

A parser needs complete source lines. We shall collect a line in a fixed buffer and return an explicit end-of-file indication.

## How it works

READLINE stores text at 2200H, followed by a zero byte. DI is the next free destination; BP counts physical characters. AX=1 means a line is ready and AX=0 means there is no more source. The routine changes the ordinary working registers and the ENDED, SKIPLF, and LINENO fields.

A carriage return finishes a line and sets SKIPLF. A following line feed is consumed without creating a second empty line. A bare line feed also finishes a line. Control-Z and a zero-byte read set ENDED. If characters preceded that ending, they form one last line; otherwise the routine returns zero immediately.

Tabs become spaces and lowercase ASCII letters become uppercase. Other control bytes and bytes above 126 are rejected as file/text errors. Comments still occupy physical buffer space; their semicolon is interpreted by the token reader, not discarded here.

The limit is 120 physical characters per line and 4,000 physical lines per input. The extra zero byte fits in the reserved buffer. READFAIL advances the report to the line which could not be completed. Once a complete line has been accepted, LINENO is its one-based physical line number.

The diagnostic driver prints each completed line with ZTEXT. It is a text reader, not an assembler. Blank lines are visible as blank display lines, and a final line without CR/LF is still displayed once.

## Source changes

Copy `AS05.ASM` to `AS06.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `LINENO:`

Unchanged code immediately before this edit:

```asm
LINENO:
DW 0

```

Insert after old physical line 134, before the following old line.

Insert this source:

```asm
ENDED:
DB 0

SKIPLF:
DB 0

```

### Change 2: following `ERROR:`

Unchanged code immediately before this edit:

```asm
MOV AX,4C01H
INT 21H

```

Insert after old physical line 111, before the following old line.

Insert this source:

```asm
ZTEXT:
LODSB
CMP AL,0
JE ZDONE
MOV DL,AL
MOV AH,2
INT 21H
JMP ZTEXT
ZDONE:
RET

```

### Change 3: following `BYTEOK:`

Unchanged code immediately before this edit:

```asm
JMP ERROR
BYTEOK:
RET
```

Insert after old physical line 55, before the following old line.

Insert this source:

```asm

READLINE:
MOV DI,2200H
MOV BP,0
MOV AL,[ENDED]
CMP AL,0
JE READCHAR
MOV AX,0
RET
READCHAR:
CALL NEXTBYTE
CMP AX,0
JE ENDFILE
MOV AL,[CHAR]
CMP AL,10
JE LINEFEED
MOV AH,0
MOV [SKIPLF],AH
CMP AL,13
JE CARRIAGE
CMP AL,26
JE ENDFILE
CMP BP,120
JAE READFULL
CMP AL,9
JE TABCHAR
CMP AL,32
JB READBAD
CMP AL,126
JA READBAD
CMP AL,97
JB KEEPCHAR
CMP AL,122
JA KEEPCHAR
SUB AL,32
JMP KEEPCHAR
TABCHAR:
MOV AL,32
KEEPCHAR:
STOSB
INC BP
JMP READCHAR
LINEFEED:
MOV AL,[SKIPLF]
CMP AL,0
JE LINEEND
MOV AL,0
MOV [SKIPLF],AL
JMP READCHAR
CARRIAGE:
MOV AL,1
MOV [SKIPLF],AL
JMP LINEEND
ENDFILE:
MOV AL,1
MOV [ENDED],AL
CMP BP,0
JE EMPTYEND
LINEEND:
MOV AL,0
STOSB
MOV AX,[LINENO]
INC AX
CMP AX,4000
JA READFULL
MOV [LINENO],AX
MOV AX,1
RET
EMPTYEND:
MOV AX,0
RET
READFULL:
MOV AX,5
JMP READFAIL
READBAD:
MOV AX,6
READFAIL:
MOV DX,[LINENO]
INC DX
MOV [LINENO],DX
JMP ERROR
```

### Change 4: following `DUMPBYTE:`

Unchanged code immediately before this edit:

```asm
DUMPBYTE:
CALL NEXTBYTE
CMP AX,0
```

Remove these exact old lines (physical lines 13–18 of `AS05.ASM`):

```asm
JE DUMPEND
MOV DL,[CHAR]
MOV AH,2
INT 21H
JMP DUMPBYTE
DUMPEND:
```

Put this source in their place:

```asm
JE DRIVERDONE
MOV SI,2200H
MOV SI,2200H
CALL ZTEXT
MOV DX,NEWLINE
CALL TEXT
JMP DRIVERLINE
DRIVERDONE:
```

### Change 5: following `ROOM:`

Unchanged code immediately before this edit:

```asm
JMP ERROR
ROOM:
CALL OPENFILE
```

Remove these exact old lines (physical lines 10–11 of `AS05.ASM`):

```asm
DUMPBYTE:
CALL NEXTBYTE
```

Put this source in their place:

```asm
DRIVERLINE:
CALL READLINE
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS06.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 456 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS06.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T06.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
one
two
```

```dos
COPY T06.ASM SOURCE.ASM
```

```dos
CHECK AS06
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
ONE
TWO
PASS
```

## A rejection check

Enter this separate file as `X06.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

The test line contains exactly 121 X characters. Count carefully: 120 is allowed.

```dos
COPY X06.ASM SOURCE.ASM
CHECK AS06
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 5
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
