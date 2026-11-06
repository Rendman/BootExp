+++
title = "19 \u00b7 Arithmetic on a memory operand"
weight = 19
description = "Extend the familiar arithmetic groups without changing operand order."
download = "A31.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

The same effective-address descriptor can serve arithmetic as well as MOV.

## The working parts

MATHOPERANDS selects the direction bit when a register is the destination, or uses a memory/register form when memory is the destination. Immediate arithmetic uses the full byte or word immediate group. There is no value-dependent shortening.

ADC and SBB use their native carry/borrow groups. TEST uses its own register/memory or immediate opcode and does not store a result. Memory-to-memory arithmetic remains invalid. The executed test deliberately produces carry, then uses ADC to obtain ASCII A.

## Enter the source

Copy `A30.ASM` to `A31.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 74,71,0,0,0,0,8,127
DB 82,69,83,66,0,0,12,0
DB 82,69,83,87,0,0,12,1
```

Insert after old physical line 2363.

Insert:

```asm
DB 65,68,67,0,0,0,4,2
DB 83,66,66,0,0,0,4,3
DB 84,69,83,84,0,0,15,0
```

The following old source stays in place:

```asm
DB 74,90,0,0,0,0,8,116
DB 74,78,90,0,0,0,8,117
```

### Change 2 near `MEMORYDONE:`

Unchanged source immediately before this edit:

```asm
MOV [KIND],AL
RET
```

Insert after old physical line 2224.

Insert:

```asm
MATHOPERANDS:
MOV AL,[KIND]
CMP AL,3
JNE ZMATHOPER1
JMP MATHIMMEDIATE
ZMATHOPER1:
MOV AL,[K1]
CMP AL,1
JNE ZMATHOPER2
JMP MATHTOREG
ZMATHOPER2:
CMP AL,2
JE ZMATHOPER3
JMP TWOBAD
ZMATHOPER3:
MOV AL,[KIND]
CMP AL,1
JE ZMATHOPER4
JMP TWOBAD
ZMATHOPER4:
CALL RMFIRST
MOV AL,[WIDTH]
CALL CHECKWIDTH
MOV AL,[REG]
MOV [REGFIELD],AL
MOV AL,[TYPE]
CMP AL,15
JNE ZMATHOPER5
JMP MATHTEST
ZMATHOPER5:
MOV AL,[OP]
CALL TIMES8
MOV DL,[ENCWIDTH]
ADD AL,DL
MOV [ENCOP],AL
JMP ENCODE
MATHTOREG:
MOV AL,[KIND]
CMP AL,2
JBE ZMATHOPER6
JMP TWOBAD
ZMATHOPER6:
CALL RMCURRENT
MOV AL,[W1]
CALL CHECKWIDTH
MOV AL,[R1]
MOV [REGFIELD],AL
MOV AL,[TYPE]
CMP AL,15
JE MATHTEST
MOV AL,[OP]
CALL TIMES8
ADD AL,2
MOV DL,[ENCWIDTH]
ADD AL,DL
MOV [ENCOP],AL
JMP ENCODE
MATHTEST:
MOV AL,[ENCWIDTH]
ADD AL,132
MOV [ENCOP],AL
JMP ENCODE
MATHIMMEDIATE:
MOV AX,[VAL]
MOV [IMMVAL],AX
MOV AL,[K1]
CMP AL,2
JBE ZMATHOPER7
JMP TWOBAD
ZMATHOPER7:
CALL RMFIRST
CALL KNOWNWIDTH
MOV AL,[OP]
MOV [REGFIELD],AL
MOV AL,[TYPE]
CMP AL,15
JE TESTIMMEDIATE
MOV AL,[ENCWIDTH]
ADD AL,128
MOV [ENCOP],AL
JMP MATHIMMEMIT
TESTIMMEDIATE:
MOV AL,0
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
ADD AL,246
MOV [ENCOP],AL
MATHIMMEMIT:
CALL ENCODE
JMP EMITIMM
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 3 near `ZMOVOPERA9:`

Unchanged source immediately before this edit:

```asm
MOV AL,140
MOV [ENCOP],AL
JMP ENCODE
```

Remove this exact source at old physical positions 1251–1278:

```asm

REGMOD:
MOV AL,[R1]
CALL TIMES8
MOV DL,[REG]
ADD AL,DL
ADD AL,192
CALL EMIT
RET

IMMEDVALUE:
MOV AL,[W1]
CMP AL,0
MOV AX,[VAL]
JNE IMMEDWORD
JMP BYTEVALUE
IMMEDWORD:
JMP EMITWORD

SAMEWIDTH:
MOV AL,[W1]
MOV DL,[WIDTH]
CMP AL,DL
JE WIDTHOK
MOV AX,1
JMP ERROR
WIDTHOK:
RET
```

There is no replacement source.

The following old source stays in place:

```asm

TIMES8:
```

### Change 4 near `ZTWOOPERA1:`

Unchanged source immediately before this edit:

```asm
CALL OPERAND
MOV AL,[TYPE]
CMP AL,3
```

Remove this exact source at old physical positions 1103–1136:

```asm
JNE ZTWOOPERA2
JMP MOVOPERANDS
ZTWOOPERA2:
MOV AL,[K1]
CMP AL,1
JE ZTWOOPERA3
JMP TWOBAD
ZTWOOPERA3:
MOV AL,[KIND]
CMP AL,1
JE MATHREG
CMP AL,3
JE ZTWOOPERA4
JMP TWOBAD
ZTWOOPERA4:
MOV AL,[W1]
ADD AL,128
CALL EMIT
MOV AL,[OP]
CALL TIMES8
MOV DL,[R1]
ADD AL,DL
ADD AL,192
CALL EMIT
JMP IMMEDVALUE
MATHREG:
CALL SAMEWIDTH
MOV AL,[OP]
CALL TIMES8
ADD AL,2
MOV DL,[W1]
ADD AL,DL
CALL EMIT
JMP REGMOD
```

Replace it with:

```asm
JE MOVOPERANDS
JMP MATHOPERANDS
```

The following old source stays in place:

```asm
TWOBAD:
MOV AX,1
```

### Change 5 near `TWOOPERANDS:`

Unchanged source immediately before this edit:

```asm
CALL SCAN
MOV AL,[0CC00H]
CMP AL,44
```

Remove this exact source at old physical positions 1097–1099:

```asm
JE ZTWOOPERA1
JMP TWOBAD
ZTWOOPERA1:
```

Replace it with:

```asm
JNE TWOBAD
```

The following old source stays in place:

```asm
CALL OPERAND
MOV AL,[TYPE]
```

### Change 6 near `RESTOREINSTR:`

Unchanged source immediately before this edit:

```asm
POP SI
CALL RESTORENAME
MOV BX,OPTAB
```

Remove this exact source at old physical positions 850–850:

```asm
MOV CX,37
```

Replace it with:

```asm
MOV CX,40
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

```dos
COPY A31.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 05797 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A31.COM
```

VIEW.BAS must report A31.COM length 5797 bytes. Keep that executable and source together.

## Acceptance check

Create T31.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,65535
ADD AX,1
ADC AX,64
MOV DL,AL
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T31.ASM SOURCE.ASM
```

```dos
CHECK A31
```

Require:

```text
OK RESULT.COM 00022 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **22 bytes** and these complete contents:

```text
B8 FF FF 81 C0 01 00 81 D0 40 00 8A D0 B4 02 CD 21 B8 00 4C CD 21
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X31.ASM with this separate source:

```asm
ADD [BX],[SI]
```

```dos
COPY X31.ASM SOURCE.ASM
CHECK A31
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
