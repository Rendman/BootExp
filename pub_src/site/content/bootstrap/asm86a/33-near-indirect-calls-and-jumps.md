+++
title = "21 \u00b7 Near indirect calls and jumps"
weight = 21
description = "Transfer through an ordinary word register or word memory location."
download = "A33.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

A near destination can be a runtime word rather than a fixed source label.

## The working parts

NEARJUMP retains the existing E8H/E9H direct relative forms for values. For register or memory operands it emits FFH with group two for CALL or four for JMP. The operand must have word width; an unannotated memory form can infer that width from the instruction.

These are near transfers within the current code segment. There is no far pointer or second code segment. The test obtains SAY's offset in BX, calls through BX, and returns normally.

## Enter the source

Copy `A32.ASM` to `A33.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `NEARJUMP:`

Unchanged source immediately before this edit:

```asm
CALL EMIT
POP AX
CALL EMITWORD
```

Remove this exact source at old physical positions 1010–1011:

```asm
CALL FINISH
RET
```

Replace it with:

```asm
JMP FINISH
```

The following old source stays in place:

```asm

SHORTJUMP:
```

### Change 2 near `NEARJUMP:`

Unchanged source immediately before this edit:

```asm
RET

NEARJUMP:
```

Remove this exact source at old physical positions 1000–1001:

```asm
CALL SCAN
CALL VALUE
```

Replace it with:

```asm
CALL OPERAND
MOV AL,[KIND]
CMP AL,3
JNE ZNEARJUMP1
JMP NEARDIRECT
ZNEARJUMP1:
CALL RMCURRENT
MOV AL,[RMKIND]
CMP AL,2
JBE ZNEARJUMP2
JMP TWOBAD
ZNEARJUMP2:
MOV AL,1
CALL CHECKWIDTH
MOV AL,[OP]
CMP AL,232
JE INDIRECTCALL
MOV AL,4
JMP INDIRECTGROUP
INDIRECTCALL:
MOV AL,2
INDIRECTGROUP:
MOV [REGFIELD],AL
MOV AL,255
MOV [ENCOP],AL
CALL ENCODE
JMP FINISH
NEARDIRECT:
MOV AX,[VAL]
```

The following old source stays in place:

```asm
MOV DX,[PC]
ADD DX,3
```

## Build the stopping point

```dos
COPY A33.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 05945 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A33.COM
```

VIEW.BAS must report A33.COM length 5945 bytes. Keep that executable and source together.

## Acceptance check

Create T33.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV BX,SAY
CALL BX
MOV AX,4C00H
INT 21H
SAY:
MOV DL,65
MOV AH,2
INT 21H
RET
```

```dos
COPY T33.ASM SOURCE.ASM
```

```dos
CHECK A33
```

Require:

```text
OK RESULT.COM 00017 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **17 bytes** and these complete contents:

```text
BB 0A 01 FF D3 B8 00 4C CD 21 B2 41 B4 02 CD 21 C3
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X33.ASM with this separate source:

```asm
CALL AL
```

```dos
COPY X33.ASM SOURCE.ASM
CHECK A33
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
