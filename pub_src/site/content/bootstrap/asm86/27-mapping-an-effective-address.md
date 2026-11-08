+++
title = "15 \u00b7 Mapping an effective address"
weight = 15
description = "Choose the legal 8086 memory code before emitting it."
download = "A27.ASM"
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/27-mapping-an-effective-address/"
+++

A parser should separate an address's meaning from its ModR/M representation.

## The working parts

MEMFINISH maps a BX/BP/SI/DI mask to one of the eight memory codes. It rejects illegal register combinations. MEMHAD says whether a displacement was written; that selects a fixed word displacement. Bare BP uses its required zero-byte displacement.

The small parser at this stopping point still supplies only BX or a direct value. It feeds the shared mapping and emitter, so their existing cases are exercised before the richer address parser is connected. No pass-dependent displacement shortening is introduced.

## Enter the source

Copy `A26.ASM` to `A27.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `MOD:`

Unchanged source immediately before this edit:

```asm
DB 0

MOD:
```

Insert after old physical line 2277.

Insert:

```asm
DB 0

ADDRMASK:
DB 0

MEMHAD:
```

The following old source stays in place:

```asm
DB 0
```

### Change 2 near `NAMELEN:`

Unchanged source immediately before this edit:

```asm
NAMELEN:
DW 0
```

Insert after old physical line 2267.

Insert:

```asm
MEMDISP:
DW 0
```

The following old source stays in place:

```asm
RMDISP:
DW 0
```

### Change 3 near `ZWIDTHHEL2:`

Unchanged source immediately before this edit:

```asm
MOV [ENCWIDTH],AL
RET
```

Insert after old physical line 2030.

Insert:

```asm
MEMFINISH:
MOV AL,[ADDRMASK]
CMP AL,0
JNE ZMEMMAP1
JMP MEMDIRECT
ZMEMMAP1:
CMP AL,1
JE MEMRM7
CMP AL,2
JNE ZMEMMAP2
JMP MEMRM6
ZMEMMAP2:
CMP AL,4
JNE ZMEMMAP3
JMP MEMRM4
ZMEMMAP3:
CMP AL,8
JNE ZMEMMAP4
JMP MEMRM5
ZMEMMAP4:
CMP AL,5
JNE ZMEMMAP5
JMP MEMRM0
ZMEMMAP5:
CMP AL,9
JNE ZMEMMAP6
JMP MEMRM1
ZMEMMAP6:
CMP AL,6
JNE ZMEMMAP7
JMP MEMRM2
ZMEMMAP7:
CMP AL,10
JNE ZMEMMAP8
JMP MEMRM3
ZMEMMAP8:
JMP TWOBAD
MEMRM7:
MOV AL,7
JMP MEMREGSET
MEMRM6:
MOV AL,6
JMP MEMREGSET
MEMRM4:
MOV AL,4
JMP MEMREGSET
MEMRM5:
MOV AL,5
JMP MEMREGSET
MEMRM0:
MOV AL,0
JMP MEMREGSET
MEMRM1:
MOV AL,1
JMP MEMREGSET
MEMRM2:
MOV AL,2
JMP MEMREGSET
MEMRM3:
MOV AL,3
MEMREGSET:
MOV [REG],AL
MOV AL,[MEMHAD]
CMP AL,0
JNE MEMDISPLACED
MOV AL,0
MOV [MOD],AL
MOV AL,[REG]
CMP AL,6
JNE MEMORYDONE
MOV AL,1
MOV [MOD],AL
JMP MEMORYDONE
MEMDISPLACED:
MOV AL,2
MOV [MOD],AL
JMP MEMORYDONE
MEMDIRECT:
MOV AL,[MEMHAD]
CMP AL,0
JNE ZMEMMAP9
JMP TWOBAD
ZMEMMAP9:
MOV AL,0
MOV [MOD],AL
MOV AL,6
MOV [REG],AL
MEMORYDONE:
MOV AX,[MEMDISP]
MOV [VAL],AX
MOV AL,[EXWIDTH]
MOV [WIDTH],AL
MOV AL,2
MOV [KIND],AL
RET
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 4 near `MEMORYEND:`

Unchanged source immediately before this edit:

```asm
CALL SCAN
MOV AL,[0CC00H]
CMP AL,93
```

Remove this exact source at old physical positions 653–659:

```asm
JE MEMORYOK
MOV AX,1
JMP ERROR
MEMORYOK:
MOV AL,2
MOV [KIND],AL
RET
```

Replace it with:

```asm
JE ZMEMORY1
JMP TWOBAD
ZMEMORY1:
JMP MEMFINISH
```

The following old source stays in place:

```asm

STATEMENT:
```

### Change 5 near `DIRECTMEM:`

Unchanged source immediately before this edit:

```asm
JMP MEMORYEND
DIRECTMEM:
CALL VALUE
```

Remove this exact source at old physical positions 646–649:

```asm
MOV [VAL],AX
MOV AL,6
MOV [REG],AL
MEMORYEND:
```

Replace it with:

```asm
MOV [MEMDISP],AX
MOV AL,1
MOV [MEMHAD],AL
SIMPLEMEMEND:
```

The following old source stays in place:

```asm
CALL SCAN
MOV AL,[0CC00H]
```

### Change 6 near `MEMORY:`

Unchanged source immediately before this edit:

```asm
JNE DIRECTMEM
MOV AL,[0CC02H]
CMP AL,0
```

Remove this exact source at old physical positions 640–644:

```asm
JNE DIRECTMEM
MOV AL,7
MOV [REG],AL
JMP MEMORYEND
DIRECTMEM:
```

Replace it with:

```asm
JNE SIMPLEMEMVAL
MOV AL,1
MOV [ADDRMASK],AL
JMP SIMPLEMEMEND
SIMPLEMEMVAL:
```

The following old source stays in place:

```asm
CALL VALUE
MOV [VAL],AX
```

### Change 7 near `MEMORY:`

Unchanged source immediately before this edit:

```asm
CALL SCAN
MOV AX,[0CC00H]
CMP AX,5842H
```

Remove this exact source at old physical positions 637–637:

```asm
JNE DIRECTMEM
```

Replace it with:

```asm
JNE SIMPLEMEMVAL
```

The following old source stays in place:

```asm
MOV AL,[0CC02H]
CMP AL,0
```

### Change 8 near `MEMORY:`

Unchanged source immediately before this edit:

```asm
RET

MEMORY:
```

Remove this exact source at old physical positions 632–633:

```asm
MOV AL,0
MOV [MOD],AL
```

Replace it with:

```asm
MOV AX,0
MOV [MEMDISP],AX
MOV [ADDRMASK],AL
MOV [MEMHAD],AL
```

The following old source stays in place:

```asm
CALL SCAN
MOV AX,[0CC00H]
```

## Build the stopping point

```dos
COPY A27.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 05338 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A27.COM
```

VIEW.BAS must report A27.COM length 5338 bytes. Keep that executable and source together.

## Acceptance check

Create T27.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,[1234H]
MOV [BX],AX
```

```dos
COPY T27.ASM SOURCE.ASM
```

```dos
CHECK A27
```

Require:

```text
OK RESULT.COM 00006 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **6 bytes** and these complete contents:

```text
8B 06 34 12 89 07
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X27.ASM with this separate source:

```asm
MOV AX,[BP]
```

```dos
COPY X27.ASM SOURCE.ASM
CHECK A27
```

Require:

```text
ERROR 0000000001 CODE 3
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check descriptor width, segment selection, ModR/M bits, displacement order, and registers changed by EMIT. Use the printed bytes to distinguish a parser mistake from an encoding mistake. Keep the branch size the same in both passes.
