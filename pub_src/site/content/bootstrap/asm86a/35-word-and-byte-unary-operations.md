+++
title = "23 \u00b7 Word and byte unary operations"
weight = 23
description = "Select NEG and NOT through the shared r/m group."
download = "A35.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

Negation and bit inversion have fixed operand widths and a common encoding structure.

## The working parts

GROUP parses a register or explicitly sized memory operand, selects its known width, and emits F6H or F7H with the table's extension field. NEG uses field three and NOT field two.

A memory operand needs a size because there is no second register to supply one. The test turns one into FFFFH with NEG, then into zero with NOT, and adds 65 for a visible A.

## Enter the source

Copy `A34.ASM` to `A35.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 65,68,67,0,0,0,4,2
DB 83,66,66,0,0,0,4,3
DB 84,69,83,84,0,0,15,0
```

Insert after old physical line 2479.

Insert:

```asm
DB 78,69,71,0,0,0,9,3
DB 78,79,84,0,0,0,9,2
```

The following old source stays in place:

```asm
DB 74,90,0,0,0,0,8,116
DB 74,78,90,0,0,0,8,117
```

### Change 2 near `RETURNVALUE:`

Unchanged source immediately before this edit:

```asm
CALL EMITWORD
JMP FINISH
```

Insert after old physical line 2336.

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
MOV CX,41
```

Replace it with:

```asm
MOV CX,43
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

```dos
COPY A35.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 06064 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A35.COM
```

VIEW.BAS must report A35.COM length 6064 bytes. Keep that executable and source together.

## Acceptance check

Create T35.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,1
NEG AX
NOT AX
ADD AX,65
MOV DL,AL
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T35.ASM SOURCE.ASM
```

```dos
CHECK A35
```

Require:

```text
OK RESULT.COM 00022 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **22 bytes** and these complete contents:

```text
B8 01 00 F7 D8 F7 D0 81 C0 41 00 8A D0 B4 02 CD 21 B8 00 4C CD 21
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X35.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X35.ASM SOURCE.ASM
CHECK A35
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
