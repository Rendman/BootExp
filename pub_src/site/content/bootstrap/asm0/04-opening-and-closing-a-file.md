+++
title = "04 \u00b7 Opening and closing a file"
weight = 4
description = "Let DOS return a handle, and check carry immediately."
download = "AS04.ASM"
aliases = ["/bootstrap/asm86/04-choosing-the-source-name/", "/bootstrap/asm86/05-opening-and-closing-a-file/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/04-opening-and-closing-a-file/"
+++

A filename is useful only if DOS can open it. We shall open an existing source file for input and close its handle before returning.

## How it works

FNAME contains the zero-terminated name SOURCE.ASM. Use COPY to select a source before running the assembler; no console input is read. OPENFILE passes FNAME in DS:DX to DOS function 3DH with AL=0 for read-only access. On success AX is the handle, a small number which DOS uses to identify the open file. HANDLE retains it. The carry flag reports an error; JAE takes the carry-clear success path, while the near jump reaches FILEBAD on failure.

CLOSEFILE loads the saved handle into BX and uses function 3EH. Its carry result is checked before another operation can replace it. FILEBAD selects code 6 and reaches the common report. Neither routine returns after an error.

OPENFILE changes AX, DX, the flags, and HANDLE. CLOSEFILE uses BX and AH and changes the flags DOS returns. They do not read or interpret file contents. This checkpoint reports Opened only after both calls succeed. The missing-file test is useful: the existence of a filename in memory is not evidence that a disk file was opened.

## Source changes

Copy `AS03.ASM` to `AS04.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `ERRCODE:`

Unchanged code immediately before this edit:

```asm
ERRCODE:
DB 0

```

Remove these exact old lines (physical lines 90–91 of `AS03.ASM`):

```asm
READYMSG:
DB 82,69,65,68,89,13,10,36
```

Put this source in their place:

```asm
OPENMSG:
DB 79,112,101,110,101,100,13,10,36
```

### Change 2: following `DIVEND:`

Unchanged code immediately before this edit:

```asm

DIVEND:

```

Insert after old physical line 83, before the following old line.

Insert this source:

```asm
FNAME:
DB 83,79,85,82,67,69,46,65,83,77,0

HANDLE:
DW 0

```

### Change 3: following `GOOD:`

Unchanged code immediately before this edit:

```asm
GOOD:
MOV AX,4C00H
INT 21H
```

Insert after old physical line 13, before the following old line.

Insert this source:

```asm

FILEBAD:
MOV AX,6
JMP ERROR

OPENFILE:
MOV DX,FNAME
MOV AX,3D00H
INT 21H
JAE INPUTOPEN
JMP FILEBAD
INPUTOPEN:
MOV [HANDLE],AX
RET

CLOSEFILE:
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
JB FILEBAD
RET
```

### Change 4: following `ROOM:`

Unchanged code immediately before this edit:

```asm
MOV AX,7
JMP ERROR
ROOM:
```

Remove these exact old lines (physical lines 9–9 of `AS03.ASM`):

```asm
MOV DX,READYMSG
```

Put this source in their place:

```asm
CALL OPENFILE
CALL CLOSEFILE
MOV DX,OPENMSG
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS04.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 219 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS04.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T04.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
DB 65
```

```dos
COPY T04.ASM SOURCE.ASM
```

```dos
CHECK AS04
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Opened
PASS
```

## A rejection check

```dos
REN SOURCE.ASM HOLD.ASM
CHECK AS04
```

Use an unused HOLD.ASM name and restore it to SOURCE.ASM after the test.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00000 CODE 6
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
