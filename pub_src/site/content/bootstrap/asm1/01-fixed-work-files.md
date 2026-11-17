+++
title = "07 \u00b7 Adding XOR to the Arithmetic Table"
weight = 7
description = "Extend the shared arithmetic encoder with one explicitly documented table record."
download = "A01.ASM"
aliases = ["/bootstrap/asm86a/01-fixed-work-files/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/01-fixed-work-files/"
+++

I have followed the names from the PSP to the file services and into the success report. Now I turn to the arithmetic table. The next assembler will hash names, and I need to account for the XOR instruction it will use.

## The working parts

The preceding A01F source already selects PSP filenames, reports the selected result and records input-handle state. This step adds only XOR recognition. The instruction-table count changes from twenty-five to twenty-six, and one eight-byte record is appended before SRCNAME.

The first six bytes, 88,79,82,0,0,0, spell XOR with zero padding. The next byte, 4, selects the existing two-operand arithmetic path. The final byte, 6, is the operation selector, not an opcode byte to copy into the result. The register encoder computes selector times eight plus two plus the width bit, producing 32H for byte registers and 33H for word registers. The immediate encoder uses the same selector in the ModR/M operation field with 80H or 81H.

Accepted forms are XOR between same-width registers, or a register and an immediate value, for bytes and words. Memory arithmetic is not added. A mismatched register width remains an error. No new emitter or filename routine is needed. The DB records after SRCNAME are filename and state data; the counted table lookup stops before them.

The required successor, ASM86, uses XOR while hashing symbol names. Teaching it as a separate operation here makes that dependency explicit. Keep ASMKEEP as the ASM0 builder: the new source uses only instructions it already accepts, and the new mnemonic is represented by ordinary DB data.

## Enter the source

Copy `A01F.ASM` to `A01.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 74,78,69,0,0,0,8,117
DB 74,66,69,0,0,0,8,118
DB 74,65,0,0,0,0,8,119
```

Insert after old physical line 1276.

Insert:

```asm
DB 88,79,82,0,0,0,4,6
```

The following old source stays in place:

```asm

SRCNAME:
```

### Change 2 near `INSTRUCTION:`

Unchanged source immediately before this edit:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

Remove this exact source at old physical positions 564–564:

```asm
MOV CX,25
```

Replace it with:

```asm
MOV CX,26
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

Copy `A01.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 02939 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A01.COM`.

VIEW.BAS must report A01.COM length 2939 bytes. Keep that executable and source together.

## Acceptance check

Create T01.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
XOR AL,AL
XOR AX,BX
XOR AL,80H
XOR AX,1234H
```

```dos
CHECK A01 T01.ASM RESULT.COM
```

Require:

```text
OK RESULT.COM 00011 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **11 bytes** and these complete contents:

```text
32 C0 33 C3 80 F0 80 81 F0 34 12
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X01.ASM with this separate source:

```asm
XOR AX,BL
```

```dos
CHECK A01 X01.ASM RESULT.COM
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with C:\DOS\FC.EXE /B if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check the six spelling bytes, the table count of twenty-six, class four and selector six. Register widths must agree. The existing arithmetic encoder supplies the instruction bytes.
