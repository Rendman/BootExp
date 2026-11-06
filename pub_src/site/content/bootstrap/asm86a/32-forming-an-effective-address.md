+++
title = "20 \u00b7 Forming an effective address"
weight = 20
description = "Use LEA when the offset itself is the result."
download = "A32.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

Loading storage and forming a pointer are different operations.

## The working parts

LEA requires an ordinary word destination register and a memory-form effective address. It emits 8DH with that register field and the selected address encoding. It does not read the memory at that address.

The test forms TEXT plus one in DX, copies the offset to BX, then reads and displays that byte. Segment overrides are rejected for LEA because this operation produces an offset rather than performing a segment-selected memory access.

## Enter the source

Copy `A31.ASM` to `A32.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 74,71,0,0,0,0,8,127
DB 82,69,83,66,0,0,12,0
DB 82,69,83,87,0,0,12,1
```

Insert after old physical line 2392.

Insert:

```asm
DB 76,69,65,0,0,0,11,0
```

The following old source stays in place:

```asm
DB 65,68,67,0,0,0,4,2
DB 83,66,66,0,0,0,4,3
```

### Change 2 near `MATHIMMEMIT:`

Unchanged source immediately before this edit:

```asm
CALL ENCODE
JMP EMITIMM
```

Insert after old physical line 2253.

Insert:

```asm
LEAOP:
MOV AL,[K1]
CMP AL,1
JE ZLEAOP1
JMP TWOBAD
ZLEAOP1:
MOV AL,[W1]
CMP AL,1
JE ZLEAOP2
JMP TWOBAD
ZLEAOP2:
MOV AL,[KIND]
CMP AL,2
JE ZLEAOP3
JMP TWOBAD
ZLEAOP3:
CALL RMCURRENT
MOV AL,[RMPREFIX]
CMP AL,0
JE ZLEAOP4
JMP TWOBAD
ZLEAOP4:
MOV AL,[R1]
MOV [REGFIELD],AL
MOV AL,141
MOV [ENCOP],AL
JMP ENCODE
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 3 near `TWOOPERANDS:`

Unchanged source immediately before this edit:

```asm
MOV AL,[TYPE]
CMP AL,3
JE MOVOPERANDS
```

Insert after old physical line 1101.

Insert:

```asm
CMP AL,11
JNE ZTWOOPERA1
JMP LEAOP
ZTWOOPERA1:
```

The following old source stays in place:

```asm
JMP MATHOPERANDS
TWOBAD:
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
MOV CX,40
```

Replace it with:

```asm
MOV CX,41
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

```dos
COPY A32.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 05881 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A32.COM
```

VIEW.BAS must report A32.COM length 5881 bytes. Keep that executable and source together.

## Acceptance check

Create T32.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV BX,TEXT
MOV SI,1
LEA DX,[BX+SI]
MOV BX,DX
MOV DL,[BX]
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
TEXT:
DB "XA"
```

```dos
COPY T32.ASM SOURCE.ASM
```

```dos
CHECK A32
```

Require:

```text
OK RESULT.COM 00023 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **23 bytes** and these complete contents:

```text
BB 15 01 BE 01 00 8D 10 8B DA 8A 17 B4 02 CD 21 B8 00 4C CD 21 58 41
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X32.ASM with this separate source:

```asm
LEA AL,[BX]
```

```dos
COPY X32.ASM SOURCE.ASM
CHECK A32
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
