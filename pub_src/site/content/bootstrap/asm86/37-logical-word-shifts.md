+++
title = "23 \u00b7 Logical word shifts"
weight = 23
description = "Shift by one or a saved count in CL."
download = "A37.ASM"
aliases = ["/bootstrap/asm86a/37-a-single-bit-shift/", "/bootstrap/asm86a/38-cl-shifts-and-rotates/", "/bootstrap/asm86a/39-repeated-byte-and-word-movement/"]
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/37-logical-word-shifts/"
+++

The tool implementations need bit masks and word shifts.

## The working parts

SHL and SHR accept count one or CL. The virtual machine masks the source count to fifteen before selecting the native CL form. Rotate, arithmetic-shift, and alternate spellings are omitted.

## Enter the source

Copy `A36.ASM` to `A37.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 76,69,65,0,0,0,11,0
DB 77,85,76,0,0,0,9,4
DB 68,73,86,0,0,0,9,6
```

Insert after old physical line 2447.

Insert:

```asm
DB 83,72,76,0,0,0,10,4
DB 83,72,82,0,0,0,10,5
```

The following old source stays in place:

```asm
DB 74,67,0,0,0,0,8,114
```

### Change 2 near `ZGROUP1:`

Unchanged source immediately before this edit:

```asm
CALL ENCODE
JMP FINISH
```

Insert after old physical line 2310.

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
CMP AX,1
JE SHIFTCL
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
MOV CX,32
```

Replace it with:

```asm
MOV CX,34
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

Require `OK RESULT.COM 05995 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A37.COM
```

VIEW.BAS must report A37.COM length 5995 bytes. Keep that executable and source together.

## Acceptance check

Create T37.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
SHL AX,1
SHR AX,CL
```

```dos
COPY T37.ASM SOURCE.ASM
```

```dos
CHECK A37
```

Require:

```text
OK RESULT.COM 00004 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **4 bytes** and these complete contents:

```text
D1 E0 D3 E8
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
