+++
title = "06 \u00b7 Reading one byte"
weight = 6
description = "A handle-based read distinguishes data from end of file."
download = "AS06.ASM"
+++

We shall read the source a byte at a time and display exactly the bytes read. This isolates file input from parsing.

## How it works

NEXTBYTE requests one byte with DOS function 3FH: BX is HANDLE, CX is one, and DS:DX points at CHAR. Carry indicates a file error. With carry clear, AX is the number of bytes read: one for a character, zero for end of file. CHAR is meaningful only when AX is one.

The routine changes AX, BX, CX, DX, and flags. It preserves the index registers, which lets a line-building loop keep its destination pointer while requesting another byte. A failed read selects code 6.

The driver checks AX before copying CHAR to DL for display. Function 02H may change AL, but the next read returns a new count. CLOSEFILE runs after the zero count. Reading one byte per DOS call is deliberately simple and can be slow on a long source file; it avoids a second buffered-input mechanism while the parser is being constructed.

At this checkpoint no case conversion or comment handling is performed. The source is displayed as text, not executed. A zero-byte input produces no copied characters and still returns successfully.

## Source changes

Copy `AS05.ASM` to `AS06.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `ERRCODE:`

Unchanged code immediately before this edit:

```asm

ERRCODE:
DB 0
```

Remove these exact old lines (physical lines 186–188 of `AS05.ASM`):

```asm

OPENMSG:
DB 79,112,101,110,101,100,13,10,36
```

No replacement lines are needed.

### Change 2: following `LINENO:`

Unchanged code immediately before this edit:

```asm
LINENO:
DW 0

```

Insert after old physical line 183, before the following old line.

Insert this source:

```asm
CHAR:
DB 0

```

### Change 3: following `BADNAME:`

Unchanged code immediately before this edit:

```asm
BADNAME:
MOV AX,1
JMP ERROR
```

Insert after old physical line 88, before the following old line.

Insert this source:

```asm

NEXTBYTE:
MOV BX,[HANDLE]
MOV CX,1
MOV DX,CHAR
MOV AH,3FH
INT 21H
JAE BYTEOK
MOV AX,6
JMP ERROR
BYTEOK:
RET
```

### Change 4: following `ROOM:`

Unchanged code immediately before this edit:

```asm
CALL GETNAME
CALL OPENFILE
CALL CLOSEFILE
```

Remove these exact old lines (physical lines 12–13 of `AS05.ASM`):

```asm
MOV DX,OPENMSG
CALL TEXT
```

No replacement lines are needed.

### Change 5: following `ROOM:`

Unchanged code immediately before this edit:

```asm
ROOM:
CALL GETNAME
CALL OPENFILE
```

Insert after old physical line 10, before the following old line.

Insert this source:

```asm
DUMPBYTE:
CALL NEXTBYTE
CMP AX,0
JE DUMPEND
MOV DL,[CHAR]
MOV AH,2
INT 21H
JMP DUMPBYTE
DUMPEND:
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BOOTASM.BAS
```

Enter `AS06` at its source prompt. Require `OK AS06.COM 395 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T06.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
Abc
```

```dos
CHECK AS06
```

Enter `T06` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T06
Abc
PASS
```

## A rejection check

Choose `X06` as a fresh name with **no** `X06.ASM` on disk. Run `CHECK AS06` and enter `X06`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00000 CODE 6
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
