+++
title = "10 \u00b7 Encoding segment-register moves"
weight = 10
description = "Teach an instruction form before using it in a successor."
download = "A10.ASM"
aliases = ["/bootstrap/asm86a/10-encoding-segment-register-moves/"]
download_group = "tools/asm1"
reader_names = 1
+++

Allocated workspace needs a way to select a segment, but the seed itself can remain in one segment.

## The working parts

REGISTER adds ES, CS, SS, and DS after the sixteen ordinary registers. OPERAND marks them as a distinct kind. SEGMOV emits 8CH for a segment source or 8EH for a segment destination, with the segment field and ordinary word-register field in ModR/M. CS is never accepted as a destination.

The seed implementation still uses only instructions accepted by ASM0. It encodes these forms as output for another program; it does not yet execute them. Register widths and mixed segment/ordinary forms are checked explicitly.

## Enter the source

Copy `A09.ASM` to `A10.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `CLEANFAIL:`

Unchanged source immediately before this edit:

```asm

CLEANFAIL:
DB 0
```

Insert after old physical line 1344.

Insert:

```asm

PREFIX:
DB 0

P1:
DB 0
```

### Change 2 near `ENDPC:`

Unchanged source immediately before this edit:

```asm
ENDPC:
DW 0
```

Insert after old physical line 1327.

Insert:

```asm
SEGCODE:
DW 0
```

The following old source stays in place:

```asm
INOPEN:
DB 0
```

### Change 3 near `REGTAB:`

Unchanged source immediately before this edit:

```asm
DB 66,80,0,13
DB 83,73,0,14
DB 68,73,0,15
```

Insert after old physical line 1266.

Insert:

```asm
DB 69,83,0,16
DB 67,83,0,17
DB 83,83,0,18
DB 68,83,0,19
```

The following old source stays in place:

```asm

OPTAB:
```

### Change 4 near `CLEANEND:`

Unchanged source immediately before this edit:

```asm
CLEANEND:
RET
```

Insert after old physical line 1163.

Insert:

```asm
SEGOPERAND:
MOV [SEGCODE],AX
PUSH SI
CALL SCAN
MOV AL,[4080H]
CMP AL,58
JNE SEGREGISTER
POP AX
JMP TWOBAD
SEGREGISTER:
POP SI
MOV AX,[SEGCODE]
SUB AX,16
MOV [REG],AL
MOV AL,1
MOV [WIDTH],AL
MOV AL,4
MOV [KIND],AL
RET

SEGMOV:
MOV AL,[K1]
CMP AL,4
JNE SEGLOAD
MOV AL,[R1]
CMP AL,1
JE SEGBAD
MOV AL,[KIND]
CMP AL,1
JNE SEGBAD
MOV AL,[WIDTH]
CMP AL,1
JNE SEGBAD
MOV AL,142
CALL EMIT
MOV AL,[R1]
CALL TIMES8
MOV DL,[REG]
JMP SEGMOD
SEGLOAD:
MOV AL,[K1]
CMP AL,1
JNE SEGBAD
MOV AL,[W1]
CMP AL,1
JNE SEGBAD
MOV AL,140
CALL EMIT
MOV AL,[REG]
CALL TIMES8
MOV DL,[R1]
SEGMOD:
ADD AL,DL
ADD AL,192
CALL EMIT
RET
SEGBAD:
JMP TWOBAD
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 5 near `STOREOK:`

Unchanged source immediately before this edit:

```asm
MOV AX,1
JMP ERROR
STOREOK:
```

Insert after old physical line 841.

Insert:

```asm
MOV AL,[P1]
CMP AL,0
JE STOREPREFIX
CALL EMIT
STOREPREFIX:
```

The following old source stays in place:

```asm
MOV AL,[WIDTH]
ADD AL,136
```

### Change 6 near `LOADMEM:`

Unchanged source immediately before this edit:

```asm
JMP EMITWORD

LOADMEM:
```

Insert after old physical line 819.

Insert:

```asm
MOV AL,[PREFIX]
CMP AL,0
JE LOADPREFIX
CALL EMIT
LOADPREFIX:
```

The following old source stays in place:

```asm
MOV AL,[W1]
ADD AL,138
```

### Change 7 near `MOVOPERANDS:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

MOVOPERANDS:
```

Insert after old physical line 773.

Insert:

```asm
MOV AL,[K1]
CMP AL,4
JNE MOVNOTSEG
JMP SEGMOV
MOVNOTSEG:
MOV AL,[KIND]
CMP AL,4
JNE MOVNOTSRC
JMP SEGMOV
MOVNOTSRC:
```

The following old source stays in place:

```asm
MOV AL,[K1]
CMP AL,2
```

### Change 8 near `TWOOPERANDS:`

Unchanged source immediately before this edit:

```asm
MOV [W1],AL
MOV AL,[REG]
MOV [R1],AL
```

Insert after old physical line 731.

Insert:

```asm
MOV AL,[PREFIX]
MOV [P1],AL
```

The following old source stays in place:

```asm
MOV AX,[VAL]
MOV [V1],AX
```

### Change 9 near `OPERAND:`

Unchanged source immediately before this edit:

```asm
CALL REGISTER
CMP AX,0FFFFH
JE IMMEDIATE
```

Insert after old physical line 507.

Insert:

```asm
CMP AX,16
JB NORMALREGISTER
JMP SEGOPERAND
NORMALREGISTER:
```

The following old source stays in place:

```asm
MOV DL,AL
AND AL,7
```

### Change 10 near `OPERAND:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

OPERAND:
```

Insert after old physical line 500.

Insert:

```asm
MOV AL,0
MOV [PREFIX],AL
```

The following old source stays in place:

```asm
CALL SCAN
MOV AL,[4080H]
```

### Change 11 near `REGISTER:`

Unchanged source immediately before this edit:

```asm

REGISTER:
MOV BX,REGTAB
```

Remove this exact source at old physical positions 307–307:

```asm
MOV CX,16
```

Replace it with:

```asm
MOV CX,20
```

The following old source stays in place:

```asm
MOV AX,4
CALL LOOK
```

## Build the stopping point

Run `CHECK ASMKEEP`, enter `A10` at `Source name:`, and require `OK 03267 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. It creates A10.COM.

VIEW.BAS must report A10.COM length 3267 bytes. Keep that executable and source together.

## Acceptance check

Create T10.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T10.ASM SOURCE.ASM
```

```dos
CHECK A10
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

Create X10.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X10.ASM SOURCE.ASM
CHECK A10
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
