+++
title = "24 \u00b7 Multiply and divide groups"
weight = 24
description = "Expose the original 8086 single-operand arithmetic forms."
download = "A36.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

The group encoder can supply multiplication and division without new operand syntax.

## The working parts

MUL, IMUL, DIV, and IDIV add extension fields four through seven to GROUP. The source has one explicit byte or word operand; the processor supplies its defined accumulator/result registers. The test uses word MUL and DIV with divisor one.

These are the original single-operand forms. Two- or three-operand IMUL is rejected. Programs must prepare the implicit dividend and avoid zero divisors or quotient overflow; the assembler cannot prove runtime arithmetic safety.

## Enter the source

Copy `A35.ASM` to `A36.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 84,69,83,84,0,0,15,0
DB 78,69,71,0,0,0,9,3
DB 78,79,84,0,0,0,9,2
```

Insert after old physical line 2503.

Insert:

```asm
DB 77,85,76,0,0,0,9,4
DB 73,77,85,76,0,0,9,5
DB 68,73,86,0,0,0,9,6
DB 73,68,73,86,0,0,9,7
```

The following old source stays in place:

```asm
DB 74,90,0,0,0,0,8,116
DB 74,78,90,0,0,0,8,117
```

### Change 2 near `RESTOREINSTR:`

Unchanged source immediately before this edit:

```asm
POP SI
CALL RESTORENAME
MOV BX,OPTAB
```

Remove this exact source at old physical positions 850–850:

```asm
MOV CX,43
```

Replace it with:

```asm
MOV CX,47
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

```dos
COPY A36.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 06096 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A36.COM
```

VIEW.BAS must report A36.COM length 6096 bytes. Keep that executable and source together.

## Acceptance check

Create T36.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,65
MOV BX,1
MUL BX
DIV BX
MOV DL,AL
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T36.ASM SOURCE.ASM
```

```dos
CHECK A36
```

Require:

```text
OK RESULT.COM 00021 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **21 bytes** and these complete contents:

```text
B8 41 00 BB 01 00 F7 E3 F7 F3 8A D0 B4 02 CD 21 B8 00 4C CD 21
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X36.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X36.ASM SOURCE.ASM
CHECK A36
```

Require:

```text
ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check descriptor width, segment selection, ModR/M bits, displacement order, and registers changed by EMIT. Use the printed bytes to distinguish a parser mistake from an encoding mistake. Keep the branch size the same in both passes.
