+++
title = "16 \u00b7 Operand widths and segment selection"
weight = 16
description = "Check BYTE/WORD annotations and explicit segment overrides."
download = "A28.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

A memory operand sometimes needs information which no ordinary register supplies.

## The working parts

OPERAND recognizes optional BYTE or WORD, then a register, value, or bracketed address. Segment-register tokens are either standalone operands or prefixes followed by a colon and brackets. The prefix byte selects ES, CS, SS, or DS.

Annotations apply only to memory. A known byte width cannot be paired with a word register, and vice versa. The saved source cursor distinguishes a segment operand from an override without losing the following comma. Memory-to-segment transfers are not yet accepted by the MOV handler here.

## Enter the source

Copy `A27.ASM` to `A28.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `CLEANEND:`

Unchanged source immediately before this edit:

```asm
MOV [CLEANFAIL],AL
CLEANEND:
CALL MEMFREE
```

Remove this exact source at old physical positions 1415–1450:

```asm
RET

SEGOPERAND:
MOV [SEGCODE],AX
PUSH SI
CALL SCAN
MOV AL,[0CC00H]
CMP AL,58
JE ZSEGOPERA1
JMP SEGREGISTER
ZSEGOPERA1:
POP AX
MOV AX,[SEGCODE]
CMP AX,16
JE SEGES
JMP TWOBAD
SEGES:
CALL SCAN
MOV AL,[0CC00H]
CMP AL,91
JE SEGMEMORY
JMP TWOBAD
SEGMEMORY:
CALL MEMORY
MOV AL,38
MOV [PREFIX],AL
RET
SEGREGISTER:
POP SI
MOV AX,[SEGCODE]
SUB AX,16
MOV [REG],AL
MOV AL,1
MOV [WIDTH],AL
MOV AL,4
MOV [KIND],AL
```

There is no replacement source.

The following old source stays in place:

```asm
RET
```

### Change 2 near `IMMEDIATE:`

Unchanged source immediately before this edit:

```asm
MOV [KIND],AL
RET
IMMEDIATE:
```

Insert after old physical line 624.

Insert:

```asm
MOV AL,[EXWIDTH]
CMP AL,255
JE ZOPERAND7
JMP TWOBAD
ZOPERAND7:
```

The following old source stays in place:

```asm
CALL VALUE
MOV [VAL],AX
```

### Change 3 near `NORMALREGISTER:`

Unchanged source immediately before this edit:

```asm
JMP SEGOPERAND
NORMALREGISTER:
MOV DL,AL
```

Insert after old physical line 612.

Insert:

```asm
MOV AL,[EXWIDTH]
CMP AL,255
JE ZOPERAND6
JMP TWOBAD
ZOPERAND6:
MOV AL,DL
```

The following old source stays in place:

```asm
AND AL,7
MOV [REG],AL
```

### Change 4 near `ZOPERAND2:`

Unchanged source immediately before this edit:

```asm
JMP IMMEDIATE
ZOPERAND2:
CMP AX,16
```

Remove this exact source at old physical positions 609–610:

```asm
JB NORMALREGISTER
JMP SEGOPERAND
```

Replace it with:

```asm
JAE ZOPERAND3
JMP NORMALREGISTER
ZOPERAND3:
SUB AX,16
MOV [SEGCODE],AX
PUSH SI
CALL SCAN
MOV AL,[0CC00H]
CMP AL,58
JNE SEGISTER
POP AX
MOV AX,[SEGCODE]
CALL TIMES8
ADD AL,38
MOV [PREFIX],AL
CALL SCAN
MOV AL,[0CC00H]
CMP AL,91
JE ZOPERAND4
JMP TWOBAD
ZOPERAND4:
JMP MEMORY
SEGISTER:
POP SI
MOV AL,[EXWIDTH]
CMP AL,255
JE ZOPERAND5
JMP TWOBAD
ZOPERAND5:
MOV AX,[SEGCODE]
MOV [REG],AL
MOV AL,1
MOV [WIDTH],AL
MOV AL,4
MOV [KIND],AL
RET
```

The following old source stays in place:

```asm
NORMALREGISTER:
MOV DL,AL
```

### Change 5 near `OPERAND:`

Unchanged source immediately before this edit:

```asm
MOV AL,0
MOV [PREFIX],AL
CALL SCAN
```

Insert after old physical line 597.

Insert:

```asm
JMP OPERANDCORE
TRYWORDSIZE:
MOV AX,[0CC00H]
CMP AX,4F57H
JNE OPERANDCORE
MOV AX,[0CC02H]
CMP AX,4452H
JNE OPERANDCORE
MOV AL,[0CC04H]
CMP AL,0
JNE OPERANDCORE
MOV AL,1
MOV [EXWIDTH],AL
CALL SCAN
OPERANDCORE:
```

The following old source stays in place:

```asm
MOV AL,[0CC00H]
CMP AL,91
```

### Change 6 near `OPERAND:`

Unchanged source immediately before this edit:

```asm
MOV AL,255
MOV [EXWIDTH],AL
MOV AL,0
```

Remove this exact source at old physical positions 596–596:

```asm
MOV [PREFIX],AL
```

Replace it with:

```asm
MOV [EXWIDTH],AL
```

The following old source stays in place:

```asm
CALL SCAN
MOV AL,[0CC00H]
```

### Change 7 near `OPERAND:`

Unchanged source immediately before this edit:

```asm
OPERAND:
MOV AL,255
MOV [EXWIDTH],AL
```

Insert after old physical line 594.

Insert:

```asm
CALL SCAN
MOV AX,[0CC00H]
CMP AX,5942H
JNE TRYWORDSIZE
MOV AX,[0CC02H]
CMP AX,4554H
JNE TRYWORDSIZE
MOV AL,[0CC04H]
CMP AL,0
JNE TRYWORDSIZE
```

The following old source stays in place:

```asm
MOV AL,0
MOV [PREFIX],AL
```

### Change 8 near `OPERAND:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

OPERAND:
```

Insert after old physical line 592.

Insert:

```asm
MOV AL,0
MOV [PREFIX],AL
```

The following old source stays in place:

```asm
MOV AL,255
MOV [EXWIDTH],AL
```

## Build the stopping point

```dos
COPY A28.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 05510 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A28.COM
```

VIEW.BAS must report A28.COM length 5510 bytes. Keep that executable and source together.

## Acceptance check

Create T28.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,WORD [1234H]
MOV ES:[BX],AL
```

```dos
COPY T28.ASM SOURCE.ASM
```

```dos
CHECK A28
```

Require:

```text
OK RESULT.COM 00007 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **7 bytes** and these complete contents:

```text
8B 06 34 12 26 88 07
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X28.ASM with this separate source:

```asm
MOV AX,BYTE [BX]
```

```dos
COPY X28.ASM SOURCE.ASM
CHECK A28
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
