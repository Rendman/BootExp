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

In BASIC, opening the source was one statement. Now I have to ask DOS for it and keep the handle DOS returns. I'll start by opening `SOURCE.ASM` for reading and closing it again, with the file itself left alone.

**Starting source:** `AS03.ASM`. **Save as:** `AS04.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

FNAME contains the zero-terminated name SOURCE.ASM. Use COPY to select a source before running the assembler; no console input is read. OPENFILE passes FNAME in DS:DX to DOS function 3DH with AL=0 for read-only access. On success AX is the handle, a small number which DOS uses to identify the open file. HANDLE retains it. The carry flag reports an error; JAE takes the carry-clear success path, while the near jump reaches FILEBAD on failure.

CLOSEFILE loads the saved handle into BX and uses function 3EH. Its carry result is checked before another operation can replace it. FILEBAD selects code 6 and reaches the common report. Neither routine returns after an error.

OPENFILE changes AX, DX, the flags, and HANDLE. CLOSEFILE uses BX and AH and changes the flags DOS returns. They do not read or interpret file contents. This checkpoint reports Opened only after both calls succeed. The missing-file test is useful: the existence of a filename in memory is not evidence that a disk file was opened.

## Source changes

Copy `AS03.ASM` to `AS04.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `READYMSG:`

Find the unique label `READYMSG:`. The old block below starts at that label.

Replace this existing source:

```asm
READYMSG:
DB 82,69,65,68,89,13,10,36
```

With:

```asm
OPENMSG:
DB 79,112,101,110,101,100,13,10,36
```

### Change 2 · `LINENO:`

Find the unique label `LINENO:`. Insert the new source immediately before this existing label:

```asm
LINENO:
```

Insert:

```asm
FNAME:
DB 83,79,85,82,67,69,46,65,83,77,0
HANDLE:
DW 0
```

### Change 3 · `TEXT:`

Find the unique label `TEXT:`. Insert the new source immediately before this existing label:

```asm
TEXT:
```

Insert:

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

### Change 4 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV DX,READYMSG
```

With:

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

Check the zero after SOURCE.ASM and save the handle returned in AX only after a successful open. Both open and close must test carry before another instruction changes the flags.
