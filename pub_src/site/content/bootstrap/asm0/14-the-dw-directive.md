+++
title = "14 \u00b7 The DW directive"
weight = 14
description = "A word is two bytes, low byte first."
download = "AS14.ASM"
aliases = ["/bootstrap/asm86/15-the-dw-directive/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/14-the-dw-directive/"
+++

DW adds a word-sized data item without changing the meaning of DB or the value reader.

**Starting source:** `AS13.ASM`. **Save as:** `AS14.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

OPTAB gains the DW record, with class one and parameter one. DATAITEM uses that parameter to choose BYTEVALUE or EMITWORD. The dispatcher still calls the same data handler.

EMITWORD takes AX, saves it, emits AL, copies AH into AL, emits the high byte, and restores AX. EMIT itself preserves AX, so the high byte survives the first call. The routine changes PC and OUTPTR, and uses two additional stack bytes for its saved word.

The order is little-endian: 1234H becomes 34 12. No alignment byte is inserted between adjacent directives. DW permits 65535; DB still rejects a value above 255. The native assembler's buffer can hold 8192 bytes, but each item must fit its selected width.

## Source changes

Copy `AS13.ASM` to `AS14.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OPTAB:`

Find the unique label `OPTAB:`, then follow this unchanged source through its last displayed instruction:

```asm
OPTAB:
DB 68,66,0,0,0,0,1,0
```

The edit begins immediately after that unchanged block.

Insert:

```asm
DB 68,87,0,0,0,0,1,1
```

### Change 2 · `EMIT:`

Find the unique label `EMIT:`. Insert the new source immediately before this existing label:

```asm
EMIT:
```

Insert:

```asm
EMITWORD:
PUSH AX
CALL EMIT
MOV AL,AH
CALL EMIT
POP AX
RET
```

### Change 3 · `DATAITEM:`

Find the unique label `DATAITEM:`, then follow this unchanged source through its last displayed instruction:

```asm
DATAITEM:
CALL SCAN
CALL VALUE
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV DL,[OP]
CMP DL,0
JE DATABYTE
CALL EMITWORD
JMP DATASEP
DATABYTE:
```

### Change 4 · `STWORD:`

Find the unique label `STWORD:`, then follow this unchanged source through its last displayed instruction:

```asm
STWORD:
MOV BX,OPTAB
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV CX,1
```

With:

```asm
MOV CX,2
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS14.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1102 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS14.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T14.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
DW 1234H,65535
DB 0
```

```dos
COPY T14.ASM SOURCE.ASM
```

```dos
CHECK AS14
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00005 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **5 bytes** with these hexadecimal bytes:

```text
34 12 FF FF 00
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X14.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
DB 256
```

```dos
COPY X14.ASM SOURCE.ASM
CHECK AS14
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the DW parameter and the two calls to EMIT. The low byte is written first; saving AX across the operation keeps the original high byte available.
