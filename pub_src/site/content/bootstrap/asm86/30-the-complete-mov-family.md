+++
title = "18 \u00b7 The complete MOV family"
weight = 18
description = "Use the common descriptor for values, memory, and segment transfers."
download = "A30.ASM"
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/30-the-complete-mov-family/"
+++

A fixed-width memory store and a segment transfer can now share the checked address machinery.

## The working parts

MOVOPERANDS selects register/immediate, register/memory, memory/register, memory/immediate, or segment-transfer forms. An immediate-to-memory destination requires BYTE or WORD. A segment transfer requires word width, and CS remains forbidden as a destination.

EMITIMM narrows according to the chosen width. Prefixes precede the opcode and every address is emitted through ENCODE. The test writes a declared byte by immediate value, reloads it, and displays A.

## Enter the source

Copy `A29.ASM` to `A30.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `RMDISP:`

Unchanged source immediately before this edit:

```asm
RMDISP:
DW 0
```

Insert after old physical line 2461.

Insert:

```asm
IMMVAL:
DW 0
```

The following old source stays in place:

```asm
BRDEST:
DW 0
```

### Change 2 near `ZWIDTHHEL2:`

Unchanged source immediately before this edit:

```asm
MOV [ENCWIDTH],AL
RET
```

Insert after old physical line 2122.

Insert:

```asm
EMITIMM:
MOV AL,[ENCWIDTH]
CMP AL,0
MOV AX,[IMMVAL]
JNE ZEMITIMM1
JMP BYTEVALUE
ZEMITIMM1:
JMP EMITWORD
```

The following old source stays in place:

```asm
MEMFINISH:
MOV AL,[ADDRMASK]
```

### Change 3 near `CLEANEND:`

Unchanged source immediately before this edit:

```asm
CLEANEND:
CALL MEMFREE
RET
```

Remove this exact source at old physical positions 1545–1589:

```asm

SEGMOV:
MOV AL,[K1]
CMP AL,4
JNE SEGLOAD
MOV AL,[R1]
CMP AL,1
JNE ZSEGMOV1
JMP SEGBAD
ZSEGMOV1:
MOV AL,[KIND]
CMP AL,1
JE ZSEGMOV2
JMP SEGBAD
ZSEGMOV2:
MOV AL,[WIDTH]
CMP AL,1
JE ZSEGMOV3
JMP SEGBAD
ZSEGMOV3:
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

There is no replacement source.

The following old source stays in place:

```asm

MEMINIT:
```

### Change 4 near `IMMEDWORD:`

Unchanged source immediately before this edit:

```asm
JMP BYTEVALUE
IMMEDWORD:
JMP EMITWORD
```

Remove this exact source at old physical positions 1200–1226:

```asm

LOADMEM:
CALL RMCURRENT
MOV AL,[W1]
CALL CHECKWIDTH
MOV AL,[R1]
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
ADD AL,138
MOV [ENCOP],AL
JMP ENCODE

STOREMEM:
MOV AL,[KIND]
CMP AL,1
JE ZSTOREMEM1
JMP TWOBAD
ZSTOREMEM1:
CALL RMFIRST
MOV AL,[WIDTH]
CALL CHECKWIDTH
MOV AL,[REG]
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
ADD AL,136
MOV [ENCOP],AL
JMP ENCODE
```

There is no replacement source.

The following old source stays in place:

```asm

SAMEWIDTH:
```

### Change 5 near `ZMOVOPERA2:`

Unchanged source immediately before this edit:

```asm
MOV DL,[R1]
ADD AL,DL
CALL EMIT
```

Remove this exact source at old physical positions 1174–1181:

```asm
JMP IMMEDVALUE

MOVREG:
CALL SAMEWIDTH
MOV AL,[W1]
ADD AL,138
CALL EMIT
JMP REGMOD
```

Replace it with:

```asm
JMP EMITIMM
MOVTOSEG:
MOV AL,[R1]
CMP AL,1
JNE ZMOVOPERA7
JMP TWOBAD
ZMOVOPERA7:
MOV AL,[KIND]
CMP AL,2
JBE ZMOVOPERA8
JMP TWOBAD
ZMOVOPERA8:
CALL RMCURRENT
MOV AL,1
CALL CHECKWIDTH
MOV AL,[R1]
MOV [REGFIELD],AL
MOV AL,142
MOV [ENCOP],AL
JMP ENCODE
MOVFROMSEG:
MOV AL,[K1]
CMP AL,2
JBE ZMOVOPERA9
JMP TWOBAD
ZMOVOPERA9:
CALL RMFIRST
MOV AL,1
CALL CHECKWIDTH
MOV AL,[REG]
MOV [REGFIELD],AL
MOV AL,140
MOV [ENCOP],AL
JMP ENCODE
```

The following old source stays in place:

```asm

REGMOD:
```

### Change 6 near `ZMOVOPERA2:`

Unchanged source immediately before this edit:

```asm
JMP LOADMEM
ZMOVOPERA2:
MOV AL,[W1]
```

Insert after old physical line 1168.

Insert:

```asm
CALL CHECKWIDTH
MOV AL,[R1]
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
ADD AL,138
MOV [ENCOP],AL
JMP ENCODE
MOVIMMEDIATE:
MOV AX,[VAL]
MOV [IMMVAL],AX
MOV AL,[K1]
CMP AL,1
JE MOVREGIMM
CMP AL,2
JE ZMOVOPERA6
JMP TWOBAD
ZMOVOPERA6:
CALL RMFIRST
CALL KNOWNWIDTH
MOV AL,0
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
ADD AL,198
MOV [ENCOP],AL
CALL ENCODE
JMP EMITIMM
MOVREGIMM:
MOV AL,[W1]
MOV [ENCWIDTH],AL
```

The following old source stays in place:

```asm
CALL TIMES8
ADD AL,176
```

### Change 7 near `ZMOVOPERA1:`

Unchanged source immediately before this edit:

```asm
CMP AL,1
JE MOVREG
CMP AL,2
```

Remove this exact source at old physical positions 1165–1167:

```asm
JNE ZMOVOPERA2
JMP LOADMEM
ZMOVOPERA2:
```

Replace it with:

```asm
JBE ZMOVOPERA5
JMP TWOBAD
ZMOVOPERA5:
CALL RMCURRENT
```

The following old source stays in place:

```asm
MOV AL,[W1]
CALL TIMES8
```

### Change 8 near `ZMOVOPERA1:`

Unchanged source immediately before this edit:

```asm
ZMOVOPERA1:
MOV AL,[KIND]
CMP AL,1
```

Remove this exact source at old physical positions 1163–1163:

```asm
JE MOVREG
```

Replace it with:

```asm
JE ZMOVOPERA4
JMP TWOBAD
ZMOVOPERA4:
CALL RMFIRST
MOV AL,[WIDTH]
CALL CHECKWIDTH
MOV AL,[REG]
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
ADD AL,136
MOV [ENCOP],AL
JMP ENCODE
MOVTOREG:
MOV AL,[KIND]
```

The following old source stays in place:

```asm
CMP AL,2
JNE ZMOVOPERA2
```

### Change 9 near `MOVNOTSRC:`

Unchanged source immediately before this edit:

```asm
MOVNOTSRC:
MOV AL,[K1]
CMP AL,2
```

Remove this exact source at old physical positions 1154–1160:

```asm
JNE MOVDESTREG
JMP STOREMEM
MOVDESTREG:
CMP AL,1
JE ZMOVOPERA1
JMP TWOBAD
ZMOVOPERA1:
```

Replace it with:

```asm
JNE TWOBAD
```

The following old source stays in place:

```asm
MOV AL,[KIND]
CMP AL,1
```

### Change 10 near `MOVNOTSRC:`

Unchanged source immediately before this edit:

```asm
JMP SEGMOV
MOVNOTSRC:
MOV AL,[K1]
```

Insert after old physical line 1152.

Insert:

```asm
CMP AL,1
JE MOVTOREG
```

The following old source stays in place:

```asm
CMP AL,2
JNE MOVDESTREG
```

### Change 11 near `MOVNOTSEG:`

Unchanged source immediately before this edit:

```asm
MOVNOTSEG:
MOV AL,[KIND]
CMP AL,4
```

Remove this exact source at old physical positions 1149–1151:

```asm
JNE MOVNOTSRC
JMP SEGMOV
MOVNOTSRC:
```

Replace it with:

```asm
JNE ZMOVOPERA2
JMP MOVFROMSEG
ZMOVOPERA2:
CMP AL,3
JNE ZMOVOPERA3
JMP MOVIMMEDIATE
ZMOVOPERA3:
```

The following old source stays in place:

```asm
MOV AL,[K1]
CMP AL,2
```

### Change 12 near `MOVOPERANDS:`

Unchanged source immediately before this edit:

```asm
MOVOPERANDS:
MOV AL,[K1]
CMP AL,4
```

Remove this exact source at old physical positions 1144–1146:

```asm
JNE MOVNOTSEG
JMP SEGMOV
MOVNOTSEG:
```

Replace it with:

```asm
JNE ZMOVOPERA1
JMP MOVTOSEG
ZMOVOPERA1:
```

The following old source stays in place:

```asm
MOV AL,[KIND]
CMP AL,4
```

## Build the stopping point

```dos
COPY A30.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 05606 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A30.COM
```

VIEW.BAS must report A30.COM length 5606 bytes. Keep that executable and source together.

## Acceptance check

Create T30.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV BYTE [LETTER],65
MOV DL,[LETTER]
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
LETTER:
DB 0
```

```dos
COPY T30.ASM SOURCE.ASM
```

```dos
CHECK A30
```

Require:

```text
OK RESULT.COM 00019 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **19 bytes** and these complete contents:

```text
C6 06 12 01 41 8A 16 12 01 B4 02 CD 21 B8 00 4C CD 21 00
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X30.ASM with this separate source:

```asm
MOV CS,AX
```

```dos
COPY X30.ASM SOURCE.ASM
CHECK A30
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
