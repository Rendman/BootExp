+++
title = "17 \u00b7 Indexed and frame-relative memory"
weight = 17
description = "Parse valid base/index combinations and explicit displacements."
download = "A29.ASM"
+++

A word within a record, array, or procedure frame needs more than one fixed address form.

## The working parts

MEMORY accumulates a register mask and a word displacement, preserving the sign of each constant term. Only BX, BP, SI, and DI may participate. A repeated register, two bases, two indexes, or subtraction of a register is rejected. MEMFINISH selects the encoding after the closing bracket.

A written displacement always uses its word form, even when zero or temporarily unresolved. The complete test establishes a BP frame, reads its argument at BP+4, stores a local at BP-2, and releases that local before returning.

## Enter the source

Copy `A28.ASM` to `A29.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `MEMHAD:`

Unchanged source immediately before this edit:

```asm
MEMHAD:
DB 0
```

Insert after old physical line 2427.

Insert:

```asm
MEMSIGN:
DB 0
```

The following old source stays in place:

```asm
M1:
DB 0
```

### Change 2 near `SIMPLEMEMEND:`

Unchanged source immediately before this edit:

```asm
CMP AL,93
JE ZMEMORY1
JMP TWOBAD
```

Remove this exact source at old physical positions 729–730:

```asm
ZMEMORY1:
JMP MEMFINISH
```

Replace it with:

```asm
ZMEMORY5:
MOV AL,1
MOV [MEMSIGN],AL
JMP MEMTERM
MEMPOSITIVE:
MOV AL,0
MOV [MEMSIGN],AL
JMP MEMTERM
```

The following old source stays in place:

```asm

STATEMENT:
```

### Change 3 near `SIMPLEMEMEND:`

Unchanged source immediately before this edit:

```asm
CALL SCAN
MOV AL,[0CC00H]
CMP AL,93
```

Remove this exact source at old physical positions 727–727:

```asm
JE ZMEMORY1
```

Replace it with:

```asm
JNE ZMEMORY4
JMP MEMFINISH
ZMEMORY4:
CMP AL,43
JE MEMPOSITIVE
CMP AL,45
JE ZMEMORY5
```

The following old source stays in place:

```asm
JMP TWOBAD
ZMEMORY1:
```

### Change 4 near `SIMPLEMEMVAL:`

Unchanged source immediately before this edit:

```asm
MOV [MEMDISP],AX
MOV AL,1
MOV [MEMHAD],AL
```

Remove this exact source at old physical positions 723–723:

```asm
SIMPLEMEMEND:
```

Replace it with:

```asm
MEMAFTER:
```

The following old source stays in place:

```asm
CALL SCAN
MOV AL,[0CC00H]
```

### Change 5 near `MEMORY:`

Unchanged source immediately before this edit:

```asm
MOV AX,0
MOV [MEMDISP],AX
MOV [ADDRMASK],AL
```

Remove this exact source at old physical positions 707–720:

```asm
MOV [MEMHAD],AL
CALL SCAN
MOV AX,[0CC00H]
CMP AX,5842H
JNE SIMPLEMEMVAL
MOV AL,[0CC02H]
CMP AL,0
JNE SIMPLEMEMVAL
MOV AL,1
MOV [ADDRMASK],AL
JMP SIMPLEMEMEND
SIMPLEMEMVAL:
CALL VALUE
MOV [MEMDISP],AX
```

Replace it with:

```asm
JMP MEMAFTER
MEMCONSTANT:
CALL FACTOR
MOV DL,[MEMSIGN]
CMP DL,0
JE MEMADD
MOV DX,[MEMDISP]
SUB DX,AX
JMP MEMSAVED
MEMADD:
MOV DX,[MEMDISP]
ADD DX,AX
MEMSAVED:
MOV [MEMDISP],DX
```

The following old source stays in place:

```asm
MOV AL,1
MOV [MEMHAD],AL
```

### Change 6 near `MEMORY:`

Unchanged source immediately before this edit:

```asm
MEMORY:
MOV AX,0
MOV [MEMDISP],AX
```

Insert after old physical line 705.

Insert:

```asm
MEMTERM:
CALL SCAN
CALL REGISTER
CMP AX,0FFFFH
JNE ZMEMORY1
JMP MEMCONSTANT
ZMEMORY1:
MOV DL,[MEMSIGN]
CMP DL,0
JE ZMEMORY2
JMP TWOBAD
ZMEMORY2:
CMP AX,11
JE MEMBX
CMP AX,13
JE MEMBP
CMP AX,14
JE MEMSI
CMP AX,15
JE MEMDI
JMP TWOBAD
MEMBX:
MOV AL,1
JMP MEMREGBIT
MEMBP:
MOV AL,2
JMP MEMREGBIT
MEMSI:
MOV AL,4
JMP MEMREGBIT
MEMDI:
MOV AL,8
MEMREGBIT:
MOV DL,[ADDRMASK]
MOV AH,AL
AND AH,DL
CMP AH,0
JE ZMEMORY3
JMP TWOBAD
ZMEMORY3:
OR AL,DL
```

The following old source stays in place:

```asm
MOV [ADDRMASK],AL
MOV [MEMHAD],AL
```

### Change 7 near `MEMORY:`

Unchanged source immediately before this edit:

```asm
RET

MEMORY:
```

Insert after old physical line 703.

Insert:

```asm
MOV AL,0
MOV [ADDRMASK],AL
MOV [MEMHAD],AL
MOV [MEMSIGN],AL
```

The following old source stays in place:

```asm
MOV AX,0
MOV [MEMDISP],AX
```

## Build the stopping point

```dos
COPY A29.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 05634 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A29.COM
```

VIEW.BAS must report A29.COM length 5634 bytes. Keep that executable and source together.

## Acceptance check

Create T29.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,7
PUSH AX
CALL F
ADD SP,2
MOV DX,AX
ADD DL,48
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
F:
PUSH BP
MOV BP,SP
SUB SP,2
MOV AX,[BP+4]
MOV [BP-2],AX
MOV AX,[BP-2]
MOV SP,BP
POP BP
RET
```

```dos
COPY T29.ASM SOURCE.ASM
```

```dos
CHECK A29
```

Require:

```text
OK RESULT.COM 00048 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **48 bytes** and these first thirty-two bytes:

```text
B8 07 00 50 E8 12 00 81 C4 02 00 8B D0 80 C2 30 B4 02 CD 21 B8 00 4C CD 21 55 8B EC 81 EC 02 00
```

This fixture is a complete program. Save it before another assembly and execute it:

```dos
COPY RESULT.COM TRY.COM
CHECK TRY
```

It displays "7" and the checker reports PASS.

## A rejection check

Create X29.ASM with this separate source:

```asm
MOV AX,[BX+BP]
```

```dos
COPY X29.ASM SOURCE.ASM
CHECK A29
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
