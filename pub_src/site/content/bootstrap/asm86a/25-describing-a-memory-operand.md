+++
title = "13 \u00b7 Describing a memory operand"
weight = 13
description = "Save a reusable record before choosing its encoding."
download = "A25.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

Several instruction families need the same memory-address information.

## The working parts

RMCURRENT and RMFIRST copy kind, register/memory code, width, mode, prefix, and displacement into a common descriptor. The load/store paths use that descriptor for their already supported direct and BX-based forms.

The first operand's MOD is saved in M1 before the second operand is parsed. A memory operand without an explicit width uses 255 as an unknown marker. It is not silently assumed to be a byte. The generated test bytes remain identical.

## Enter the source

Copy `A24.ASM` to `A25.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `BRDEST:`

Unchanged source immediately before this edit:

```asm

BRDEST:
DW 0
```

Insert after old physical line 2197.

Insert:

```asm

MOD:
DB 0

M1:
DB 0

RMKIND:
DB 0

RMREG:
DB 0

RMWIDTH:
DB 0

RMMOD:
DB 0

RMPREFIX:
DB 0
```

The following old source stays in place:

```asm

LINEHI:
```

### Change 2 near `NAMELEN:`

Unchanged source immediately before this edit:

```asm
NAMELEN:
DW 0
```

Insert after old physical line 2195.

Insert:

```asm
RMDISP:
DW 0
```

The following old source stays in place:

```asm
BRDEST:
DW 0
```

### Change 3 near `RESERVEND:`

Unchanged source immediately before this edit:

```asm
RESERVEND:
RET
```

Insert after old physical line 1950.

Insert:

```asm
RMCURRENT:
MOV AL,[KIND]
MOV [RMKIND],AL
MOV AL,[REG]
MOV [RMREG],AL
MOV AL,[WIDTH]
MOV [RMWIDTH],AL
MOV AL,[MOD]
MOV [RMMOD],AL
MOV AL,[PREFIX]
MOV [RMPREFIX],AL
MOV AX,[VAL]
MOV [RMDISP],AX
RET
RMFIRST:
MOV AL,[K1]
MOV [RMKIND],AL
MOV AL,[R1]
MOV [RMREG],AL
MOV AL,[W1]
MOV [RMWIDTH],AL
MOV AL,[M1]
MOV [RMMOD],AL
MOV AL,[P1]
MOV [RMPREFIX],AL
MOV AX,[V1]
MOV [RMDISP],AX
RET
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 4 near `STOREPREFIX:`

Unchanged source immediately before this edit:

```asm
CALL EMIT
CMP DL,6
JNE STOREEND
```

Remove this exact source at old physical positions 1110–1110:

```asm
MOV AX,[V1]
```

Replace it with:

```asm
MOV AX,[RMDISP]
```

The following old source stays in place:

```asm
CALL EMITWORD
STOREEND:
```

### Change 5 near `STOREPREFIX:`

Unchanged source immediately before this edit:

```asm
CALL EMIT
MOV AL,[REG]
CALL TIMES8
```

Remove this exact source at old physical positions 1105–1105:

```asm
MOV DL,[R1]
```

Replace it with:

```asm
MOV DL,[RMREG]
```

The following old source stays in place:

```asm
ADD AL,DL
CALL EMIT
```

### Change 6 near `STOREOK:`

Unchanged source immediately before this edit:

```asm
MOV AX,1
JMP ERROR
STOREOK:
```

Insert after old physical line 1094.

Insert:

```asm
CALL RMFIRST
```

The following old source stays in place:

```asm
MOV AL,[P1]
CMP AL,0
```

### Change 7 near `LOADPREFIX:`

Unchanged source immediately before this edit:

```asm
CALL EMIT
CMP DL,6
JNE LOADEND
```

Remove this exact source at old physical positions 1083–1083:

```asm
MOV AX,[VAL]
```

Replace it with:

```asm
MOV AX,[RMDISP]
```

The following old source stays in place:

```asm
CALL EMITWORD
LOADEND:
```

### Change 8 near `LOADPREFIX:`

Unchanged source immediately before this edit:

```asm
CALL EMIT
MOV AL,[R1]
CALL TIMES8
```

Remove this exact source at old physical positions 1078–1078:

```asm
MOV DL,[REG]
```

Replace it with:

```asm
MOV DL,[RMREG]
```

The following old source stays in place:

```asm
ADD AL,DL
CALL EMIT
```

### Change 9 near `LOADMEM:`

Unchanged source immediately before this edit:

```asm
JMP EMITWORD

LOADMEM:
```

Insert after old physical line 1067.

Insert:

```asm
CALL RMCURRENT
```

The following old source stays in place:

```asm
MOV AL,[PREFIX]
CMP AL,0
```

### Change 10 near `TWOOPERANDS:`

Unchanged source immediately before this edit:

```asm
MOV [W1],AL
MOV AL,[REG]
MOV [R1],AL
```

Insert after old physical line 955.

Insert:

```asm
MOV AL,[MOD]
MOV [M1],AL
```

The following old source stays in place:

```asm
MOV AL,[PREFIX]
MOV [P1],AL
```

### Change 11 near `MEMORY:`

Unchanged source immediately before this edit:

```asm
RET

MEMORY:
```

Insert after old physical line 629.

Insert:

```asm
MOV AL,0
MOV [MOD],AL
```

The following old source stays in place:

```asm
CALL SCAN
MOV AX,[0CC00H]
```

## Build the stopping point

```dos
COPY A25.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 05078 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A25.COM
```

VIEW.BAS must report A25.COM length 5078 bytes. Keep that executable and source together.

## Acceptance check

Create T25.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,[1234H]
MOV [BX],AX
```

```dos
COPY T25.ASM SOURCE.ASM
```

```dos
CHECK A25
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

Create X25.ASM with this separate source:

```asm
MOV AX,[BP]
```

```dos
COPY X25.ASM SOURCE.ASM
CHECK A25
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
