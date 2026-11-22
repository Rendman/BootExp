+++
title = "05 \u00b7 Reading one byte"
weight = 5
description = "A handle-based read distinguishes data from end of file."
download = "AS05.ASM"
aliases = ["/bootstrap/asm86/06-reading-one-byte/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/05-reading-one-byte/"
+++

We shall read the source a byte at a time and display exactly the bytes read. This isolates file input from parsing.

**Starting source:** `AS04.ASM`. **Save as:** `AS05.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

NEXTBYTE requests one byte with DOS function 3FH: BX is HANDLE, CX is one, and DS:DX points at CHAR. Carry indicates a file error. With carry clear, AX is the number of bytes read: one for a character, zero for end of file. CHAR is meaningful only when AX is one.

The routine changes AX, BX, CX, DX, and flags. It preserves the index registers, which lets a line-building loop keep its destination pointer while requesting another byte. A failed read selects code 6.

The driver checks AX before copying CHAR to DL for display. Function 02H may change AL, but the next read returns a new count. CLOSEFILE runs after the zero count. Reading one byte per DOS call is deliberately simple and can be slow on a long source file; it avoids a second buffered-input mechanism while the parser is being constructed.

At this checkpoint no case conversion or comment handling is performed. The source is displayed as text, not executed. A zero-byte input produces no copied characters and still returns successfully.

## Source changes

Copy `AS04.ASM` to `AS05.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OPENMSG:`

Find the unique label `OPENMSG:`. The old block below starts at that label.

Remove this existing source:

```asm
OPENMSG:
DB 79,112,101,110,101,100,13,10,36
```

### Change 2 · `ERRCODE:`

Find the unique label `ERRCODE:`. Insert the new source immediately before this existing label:

```asm
ERRCODE:
```

Insert:

```asm
CHAR:
DB 0
```

### Change 3 · `CLOSEFILE:`

Find the unique label `CLOSEFILE:`, then follow this unchanged source through its last displayed instruction:

```asm
CLOSEFILE:
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
JB FILEBAD
```

The edit begins immediately after that unchanged block.

Insert:

```asm
RET
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
```

### Change 4 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
CALL OPENFILE
CALL CLOSEFILE
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
MOV DX,OPENMSG
CALL TEXT
```

Keep the following `GOOD:` label and the source after it in place.

### Change 5 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
CALL OPENFILE
```

The edit begins immediately after that unchanged block.

Insert:

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
COPY AS05.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 248 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS05.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T05.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
Abc
```

```dos
COPY T05.ASM SOURCE.ASM
```

```dos
CHECK AS05
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Abc
PASS
```

## A rejection check

```dos
REN SOURCE.ASM HOLD.ASM
CHECK AS05
```

Use an unused HOLD.ASM name and restore it to SOURCE.ASM after the test.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00000 CODE 6
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Test the returned AX count before using CHAR: a zero count means EOF and leaves no new character to print. Check that the driver closes the source after its reading loop.
