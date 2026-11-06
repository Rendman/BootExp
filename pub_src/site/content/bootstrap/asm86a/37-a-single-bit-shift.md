+++
title = "25 \u00b7 A single-bit shift"
weight = 25
description = "Use the original fixed-count shift encoding."
download = "A37.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

The 8086 has a dedicated form for shifting once.

## The working parts

SHIFT saves the r/m descriptor, requires a comma and a resolved count of one, then emits D0H or D1H with the operation's field. SHL, SHR, and SAR choose logical-left, logical-right, and arithmetic-right behavior.

No immediate-count byte is emitted. Counts zero or two are rejected rather than encoded with a later-CPU instruction. The test doubles 32 with SHL by one, then adds one and displays A.

## Enter the source

Copy `A36.ASM` to `A37.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 73,77,85,76,0,0,9,5
DB 68,73,86,0,0,0,9,6
DB 73,68,73,86,0,0,9,7
```

Insert after old physical line 2507.

Insert:

```asm
DB 83,72,76,0,0,0,10,4
DB 83,72,82,0,0,0,10,5
DB 83,65,82,0,0,0,10,7
```

The following old source stays in place:

```asm
DB 74,90,0,0,0,0,8,116
DB 74,78,90,0,0,0,8,117
```

### Change 2 near `ZGROUP1:`

Unchanged source immediately before this edit:

```asm
CALL ENCODE
JMP FINISH
```

Insert after old physical line 2358.

Insert:

```asm
SHIFT:
CALL OPERAND
CALL RMCURRENT
MOV AL,[RMKIND]
CMP AL,2
JBE ZSHIFT1
JMP TWOBAD
ZSHIFT1:
CALL KNOWNWIDTH
CALL SCAN
MOV AL,[0CC00H]
CMP AL,44
JE ZSHIFT2
JMP TWOBAD
ZSHIFT2:
CALL SCAN
CALL REGISTER
CALL VALUE
CMP AX,1
JNE SHIFTRANGE
MOV AL,[UNRESOLVED]
CMP AL,0
JE ZSHIFT3
JMP DEFINEBAD
ZSHIFT3:
MOV AL,208
JMP SHIFTOPCODE
SHIFTCL:
MOV AL,210
SHIFTOPCODE:
MOV DL,[ENCWIDTH]
ADD AL,DL
MOV [ENCOP],AL
MOV AL,[OP]
MOV [REGFIELD],AL
CALL ENCODE
JMP FINISH
SHIFTRANGE:
MOV AX,4
JMP ERROR
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 3 near `DISPATCH9:`

Unchanged source immediately before this edit:

```asm
CALL GROUP
RET
DISPATCH9:
```

Insert after old physical line 898.

Insert:

```asm
CMP AL,10
JNE DISPATCH10
CALL SHIFT
RET
DISPATCH10:
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
MOV CX,47
```

Replace it with:

```asm
MOV CX,50
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

```dos
COPY A37.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 06229 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A37.COM
```

VIEW.BAS must report A37.COM length 6229 bytes. Keep that executable and source together.

## Acceptance check

Create T37.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,32
SHL AX,1
ADD AX,1
MOV DL,AL
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T37.ASM SOURCE.ASM
```

```dos
CHECK A37
```

Require:

```text
OK RESULT.COM 00020 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **20 bytes** and these complete contents:

```text
B8 20 00 D1 E0 81 C0 01 00 8A D0 B4 02 CD 21 B8 00 4C CD 21
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X37.ASM with this separate source:

```asm
SHL AX,2
```

```dos
COPY X37.ASM SOURCE.ASM
CHECK A37
```

Require:

```text
ERROR 0000000001 CODE 4
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check descriptor width, segment selection, ModR/M bits, displacement order, and registers changed by EMIT. Use the printed bytes to distinguish a parser mistake from an encoding mistake. Keep the branch size the same in both passes.
