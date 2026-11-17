+++
title = "14 \u00b7 A longer source count"
weight = 14
description = "Keep source extent separate from the emitted image limit."
download = "A08.ASM"
aliases = ["/bootstrap/asm86a/08-a-longer-source-count/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/08-a-longer-source-count/"
+++

I look at the comments and labels in my source: much of what I type never becomes an instruction byte. The block reader can keep going through a long file, but its line counter still stops at 4000. I'll extend that counter's permitted range while keeping a check against wraparound.

## The working parts

READLINE permits up to 65535 physical lines per pass instead of the earlier 4000. It checks before a count can wrap; at this limit the diagnostic remains saturated at the last representable line. Width remains 120 characters.

READLINE still treats CR/LF as one ending, accepts bare CR or LF and a final unterminated line, and recognizes source Control-Z. A block refill may split any of these sequences. This is a bounded counter change, not a source-file buffer.

## Enter the source

Copy `A07.ASM` to `A08.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `READFAIL:`

Find the unique label `READFAIL:`, then follow this unchanged source through its last displayed instruction:

```asm
READFAIL:
MOV DX,[LINENO]
INC DX
```

The edit begins immediately after that unchanged block.

Insert:

```asm
READLIMIT:
```

### Change 2 · `READFAIL:`

Find the unique label `READFAIL:`, then follow this unchanged source through its last displayed instruction:

```asm
READFAIL:
MOV DX,[LINENO]
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CMP DX,0FFFFH
JE READLIMIT
```

### Change 3 · `LINEEND:`

Find the unique label `LINEEND:`, then follow this unchanged source through its last displayed instruction:

```asm
LINEEND:
MOV AL,0
STOSB
MOV AX,[LINENO]
INC AX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
CMP AX,4000
JA READFULL
```

With:

```asm
CMP AX,0
JNE LINECOUNTSAFE
MOV AX,5
JMP ERROR
LINECOUNTSAFE:
```

## Build the stopping point

Copy `A08.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03466 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A08.COM`.

VIEW.BAS must report A08.COM length 3466 bytes. Keep that executable and source together.

## Acceptance check

Create T08.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
CHECK A08 T08.ASM RESULT.COM
```

Require:

```text
OK RESULT.COM 00011 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **11 bytes** and these complete contents:

```text
B2 41 B4 02 CD 21 B8 00 4C CD 21
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X08.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
CHECK A08 X08.ASM RESULT.COM
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with C:\DOS\FC.EXE /B if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check the saved argument names and terminators, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
