+++
title = "22 \u00b7 Unsigned multiply and divide"
weight = 22
description = "Provide the word arithmetic needed by the compiler."
download = "A36.ASM"
aliases = ["/bootstrap/asm86a/34-returning-and-releasing-arguments/", "/bootstrap/asm86a/35-word-and-byte-unary-operations/", "/bootstrap/asm86a/36-multiply-and-divide-groups/"]
download_group = "tools/asm86"
reader_names = 1
+++

Word expressions and decimal formatting need unsigned multiplication and division.

## The working parts

MUL and DIV use the 8086 group encodings for one register or memory operand. The runtime checks a zero divisor before DIV; signed variants are outside the bootstrap assembler.

## Enter the source

Copy `A33.ASM` to `A36.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 82,69,83,66,0,0,12,0
DB 82,69,83,87,0,0,12,1
DB 76,69,65,0,0,0,11,0
```

Insert after old physical line 2423.

Insert:

```asm
DB 77,85,76,0,0,0,9,4
DB 68,73,86,0,0,0,9,6
```

The following old source stays in place:

```asm
DB 74,67,0,0,0,0,8,114
```

### Change 2 near `ZLEAOP4:`

Unchanged source immediately before this edit:

```asm
MOV [ENCOP],AL
JMP ENCODE
```

Insert after old physical line 2288.

Insert:

```asm
GROUP:
CALL OPERAND
CALL RMCURRENT
MOV AL,[RMKIND]
CMP AL,2
JBE ZGROUP1
JMP TWOBAD
ZGROUP1:
CALL KNOWNWIDTH
MOV AL,[OP]
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
ADD AL,246
MOV [ENCOP],AL
CALL ENCODE
JMP FINISH
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 3 near `DISPATCH8:`

Unchanged source immediately before this edit:

```asm
CALL SHORTJUMP
RET
DISPATCH8:
```

Insert after old physical line 893.

Insert:

```asm
CMP AL,9
JNE DISPATCH9
CALL GROUP
RET
DISPATCH9:
```

The following old source stays in place:

```asm
CMP AL,12
JNE DISPATCH12
```

### Change 4 near `RESTOREINSTR:`

Unchanged source immediately before this edit:

```asm
POP SI
CALL RESTORENAME
MOV BX,OPTAB
```

Remove this exact source at old physical positions 850–850:

```asm
MOV CX,30
```

Replace it with:

```asm
MOV CX,32
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

Require `OK RESULT.COM 05864 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A36.COM
```

VIEW.BAS must report A36.COM length 5864 bytes. Keep that executable and source together.

## Acceptance check

Create T36.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MUL BX
DIV BL
```

```dos
COPY T36.ASM SOURCE.ASM
```

```dos
CHECK A36
```

Require:

```text
OK RESULT.COM 00004 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **4 bytes** and these complete contents:

```text
F7 E3 F6 F3
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X36.ASM with this separate source:

```asm
MUL AX,BX
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
