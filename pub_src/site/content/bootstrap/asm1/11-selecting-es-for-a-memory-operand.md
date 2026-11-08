+++
title = "11 \u00b7 Selecting ES for a memory operand"
weight = 11
description = "Emit a segment prefix on the existing memory forms."
download = "A11.ASM"
aliases = ["/bootstrap/asm86a/11-selecting-es-for-a-memory-operand/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/11-selecting-es-for-a-memory-operand/"
+++

A word in another allocated segment needs both an offset and a segment selection.

## The working parts

SEGOPERAND distinguishes a standalone segment register from ES: followed by a memory operand. It saves and restores the source cursor when a colon is absent. PREFIX belongs to the current operand; P1 saves it for the first operand.

LOADMEM and STOREMEM emit prefix 26H before the ordinary MOV encoding. An ES override changes the selected memory segment, not the offset or operand width. At this seed stopping point only ES is accepted as a memory override.

## Enter the source

Copy `A10.ASM` to `A11.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `SEGOPERAND:`

Unchanged source immediately before this edit:

```asm
JNE SEGREGISTER
POP AX
JMP TWOBAD
```

Insert after old physical line 1200.

Insert:

```asm
SEGES:
CALL SCAN
MOV AL,[4080H]
CMP AL,91
JE SEGMEMORY
JMP TWOBAD
SEGMEMORY:
CALL MEMORY
MOV AL,38
MOV [PREFIX],AL
RET
```

The following old source stays in place:

```asm
SEGREGISTER:
POP SI
```

### Change 2 near `SEGOPERAND:`

Unchanged source immediately before this edit:

```asm
CMP AL,58
JNE SEGREGISTER
POP AX
```

Insert after old physical line 1199.

Insert:

```asm
MOV AX,[SEGCODE]
CMP AX,16
JE SEGES
```

The following old source stays in place:

```asm
JMP TWOBAD
SEGREGISTER:
```

## Build the stopping point

Copy `A11.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03302 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A11.COM`.

VIEW.BAS must report A11.COM length 3302 bytes. Keep that executable and source together.

## Acceptance check

Create T11.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T11.ASM SOURCE.ASM
```

```dos
CHECK A11
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

Create X11.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X11.ASM SOURCE.ASM
CHECK A11
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
