+++
title = "15 \u00b7 Reading the source twice"
weight = 15
description = "Reopen the source and reproduce the same instruction positions."
download = "AS15.ASM"
aliases = ["/bootstrap/asm86/16-reading-the-source-twice/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/15-reading-the-source-twice/"
+++

We shall count the source on pass one and collect its bytes on pass two, while all values are still numeric.

## How it works

PASS begins at one. PASSSTART resets PC, OUTPTR, LINENO, ENDED, and SKIPLF before reopening the source. A closed input handle is not reused as though its file position had reset; OPENFILE obtains a fresh handle.

EMIT already knows the pass convention. It performs range and capacity checks in either pass, but only pass two writes the output buffer. Every accepted form has a fixed length, so both passes must advance PC in the same way.

After a successful close, PASS is increased. A value below three repeats the source; otherwise the completed buffer is written. Only one output file and one OK report are produced. Do not edit a source while the assembler is processing it.

The visible byte check is deliberately unchanged. Reading twice must not duplicate the data or append an old file tail.

## Source changes

Copy `AS14.ASM` to `AS15.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `PASSEND:`

Unchanged code immediately before this edit:

```asm
JMP NEXTLINE
PASSEND:
CALL CLOSEFILE
```

Insert after old physical line 29, before the following old line.

Insert this source:

```asm
MOV AL,[PASS]
ADD AL,1
MOV [PASS],AL
CMP AL,3
JB PASSSTART
```

### Change 2: following `ROOM:`

Unchanged code immediately before this edit:

```asm
MOV AX,7
JMP ERROR
ROOM:
```

Remove these exact old lines (physical lines 9–9 of `AS14.ASM`):

```asm
MOV AL,2
```

Put this source in their place:

```asm
MOV AL,1
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS15.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1118 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS15.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T15.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
DW 1234H
DB 65
```

```dos
COPY T15.ASM SOURCE.ASM
```

```dos
CHECK AS15
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00003 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **3 bytes** with these hexadecimal bytes:

```text
34 12 41
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X15.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
DW 65536
```

```dos
COPY X15.ASM SOURCE.ASM
CHECK AS15
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 2
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
