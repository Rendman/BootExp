+++
title = "08 \u00b7 A longer source count"
weight = 8
description = "Keep source extent separate from the emitted image limit."
download = "A08.ASM"
aliases = ["/bootstrap/asm86a/08-a-longer-source-count/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/08-a-longer-source-count/"
+++

A source file can contain much more text than its executable contains bytes.

## The working parts

READLINE permits up to 65535 physical lines per pass instead of the earlier 4000. It checks before a count can wrap; at this limit the diagnostic remains saturated at the last representable line. Width remains 120 characters.

READLINE still treats CR/LF as one ending, accepts bare CR or LF and a final unterminated line, and recognizes source Control-Z. A block refill may split any of these sequences. This is a bounded counter change, not a source-file buffer.

## Enter the source

Copy `A07.ASM` to `A08.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `READFAIL:`

Unchanged source immediately before this edit:

```asm
READFAIL:
MOV DX,[LINENO]
INC DX
```

Insert after old physical line 207.

Insert:

```asm
READLIMIT:
```

The following old source stays in place:

```asm
MOV [LINENO],DX
JMP ERROR
```

### Change 2 near `READFAIL:`

Unchanged source immediately before this edit:

```asm
MOV AX,6
READFAIL:
MOV DX,[LINENO]
```

Insert after old physical line 206.

Insert:

```asm
CMP DX,0FFFFH
JE READLIMIT
```

The following old source stays in place:

```asm
INC DX
MOV [LINENO],DX
```

### Change 3 near `LINEEND:`

Unchanged source immediately before this edit:

```asm
STOSB
MOV AX,[LINENO]
INC AX
```

Remove this exact source at old physical positions 192–193:

```asm
CMP AX,4000
JA READFULL
```

Replace it with:

```asm
CMP AX,0
JNE LINECOUNTSAFE
MOV AX,5
JMP ERROR
LINECOUNTSAFE:
```

The following old source stays in place:

```asm
MOV [LINENO],AX
MOV AX,1
```

## Build the stopping point

Copy `A08.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03028 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A08.COM`.

VIEW.BAS must report A08.COM length 3028 bytes. Keep that executable and source together.

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
COPY T08.ASM SOURCE.ASM
```

```dos
CHECK A08
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
COPY X08.ASM SOURCE.ASM
CHECK A08
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check the fixed name bytes, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
