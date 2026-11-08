+++
title = "03 \u00b7 A clear failure report"
weight = 3
description = "A source line, an error code, and a DOS failure status."
download = "AS03.ASM"
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/03-a-clear-failure-report/"
+++

A tool must make failure visible. We shall add one exit which reports a line number and a reason code, and establish the memory required by this workbench.

## How it works

ERROR takes a small reason code in AX. It saves AL in ERRCODE before displaying any text, then prints ERROR, the five-digit LINENO value, and CODE followed by the reason digit. It finishes with DOS function 4CH and return code one. DOS closes the process's files on termination.

The line number is zero when no source line has been read. Codes 1 through 7 distinguish syntax, values, symbols, range, capacity, file input/output, and memory respectively; the full reference gives their exact use. NUMBER preserves AX and its other saved registers, while TEXT may change AX. Saving the reason first is therefore necessary.

The entry check requires SP=FFFEH, the normal stack pointer for a .COM program given a full 64 KB segment. Our working buffers will use fixed offsets within that segment. Refusing a smaller segment is simpler than relocating all those buffers. Code 7 is a real workbench limit, not a claim that every DOS program needs 64 KB.

To exercise the rejection exit on an otherwise roomy machine, save a separate copy as SMALL.ASM and insert MOV SP,8000H immediately before CMP SP,0FFFEH. This leaves ample stack space for the report but deliberately fails the entry check. Build SMALL with BOOTASM and run CHECK SMALL: it must display ERROR 00000 CODE 7 and FAIL. Keep the normal checkpoint unchanged.

## Source changes

Copy `AS02.ASM` to `AS03.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `DIVEND:`

Unchanged code immediately before this edit:

```asm
DW 10000,1000,100,10,1

DIVEND:
```

Insert after old physical line 63, before the following old line.

Insert this source:

```asm

LINENO:
DW 0

ERRCODE:
DB 0

READYMSG:
DB 82,69,65,68,89,13,10,36
```

### Change 2: following `PRINTDIGIT:`

Unchanged code immediately before this edit:

```asm
POP AX
RET

```

Insert after old physical line 56, before the following old line.

Insert this source:

```asm
ERROR:
MOV [ERRCODE],AL
MOV DX,ERRMSG
CALL TEXT
MOV AX,[LINENO]
CALL NUMBER
MOV DX,CODEMSG
CALL TEXT
MOV AL,[ERRCODE]
ADD AL,48
MOV DL,AL
MOV AH,2
INT 21H
MOV DX,NEWLINE
CALL TEXT
MOV AX,4C01H
INT 21H

ERRMSG:
DB 69,82,82,79,82,32,36

CODEMSG:
DB 32,67,79,68,69,32,36

```

### Change 3: following `START:`

Unchanged code immediately before this edit:

```asm
; ASM86 construction checkpoint. Plain BOOTASM source.
START:
CLD
```

Remove these exact old lines (physical lines 4–14 of `AS02.ASM`):

```asm
MOV AX,0
CALL NUMBER
MOV DX,NEWLINE
CALL TEXT
MOV AX,1000
CALL NUMBER
MOV DX,NEWLINE
CALL TEXT
MOV AX,65535
CALL NUMBER
MOV DX,NEWLINE
```

Put this source in their place:

```asm
CMP SP,0FFFEH
JE ROOM
MOV AX,7
JMP ERROR
ROOM:
MOV DX,READYMSG
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS03.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 164 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS03.COM`. Save this source and executable as a working stopping point.

```dos
CHECK AS03
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
READY
PASS
```

## A rejection check

Use the separate SMALL.ASM experiment described above; build it with BOOTASM, then run `CHECK SMALL`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00000 CODE 7
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the decimal character bytes, the dollar-sign terminators, and the order of saved registers. A RET must match a CALL; the top-level exit uses DOS function 4CH.
