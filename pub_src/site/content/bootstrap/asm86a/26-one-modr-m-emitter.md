+++
title = "14 \u00b7 One ModR/M emitter"
weight = 14
description = "Encode register or memory fields through one checked path."
download = "A26.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

Address-byte construction should be shared by the instructions that use it.

## The working parts

ENCODE emits an optional segment prefix, the chosen opcode, and the ModR/M byte. RMMOD selects no displacement, a byte displacement, or a word displacement; direct mode zero with code six also emits a word address. Register mode adds 192.

CHECKWIDTH infers an unspecified memory width from a register and rejects an explicit disagreement. The MOV bridges provide their opcode and register field, then use the common emitter. Known-width and immediate helpers are separate entry points for instructions needing those rules.

## Enter the source

Copy `A25.ASM` to `A26.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `RMPREFIX:`

Unchanged source immediately before this edit:

```asm
DB 0

RMPREFIX:
```

Insert after old physical line 2247.

Insert:

```asm
DB 0

ENCWIDTH:
DB 0

ENCOP:
DB 0

REGFIELD:
```

The following old source stays in place:

```asm
DB 0
```

### Change 2 near `BRDEST:`

Unchanged source immediately before this edit:

```asm
BRDEST:
DW 0
```

Insert after old physical line 2228.

Insert:

```asm
EXWIDTH:
DB 0
```

The following old source stays in place:

```asm
MOD:
DB 0
```

### Change 3 near `RMFIRST:`

Unchanged source immediately before this edit:

```asm
MOV [RMDISP],AX
RET
```

Insert after old physical line 1985.

Insert:

```asm
ENCODE:
MOV AL,[RMPREFIX]
CMP AL,0
JE ENCODEPREFIX
CALL EMIT
ENCODEPREFIX:
MOV AL,[ENCOP]
CALL EMIT
MOV AL,[REGFIELD]
CALL TIMES8
MOV DL,[RMREG]
ADD AL,DL
MOV DL,[RMKIND]
CMP DL,1
JNE ZENCODE1
JMP ENCODEREG
ZENCODE1:
MOV DL,AL
MOV AL,[RMMOD]
ADD AL,AL
ADD AL,AL
ADD AL,AL
ADD AL,AL
ADD AL,AL
ADD AL,AL
ADD AL,DL
CALL EMIT
MOV AL,[RMMOD]
CMP AL,2
JE ENCODEWORD
CMP AL,1
JE ENCODEBYTE
MOV AL,[RMREG]
CMP AL,6
JE ENCODEWORD
RET
ENCODEREG:
ADD AL,192
JMP EMIT
ENCODEWORD:
MOV AX,[RMDISP]
JMP EMITWORD
ENCODEBYTE:
MOV AL,[RMDISP]
JMP EMIT

CHECKWIDTH:
MOV DL,[RMWIDTH]
CMP DL,255
JE WIDTHCHOSEN
CMP AL,DL
JE ZWIDTHHEL1
JMP TWOBAD
ZWIDTHHEL1:
WIDTHCHOSEN:
MOV [ENCWIDTH],AL
RET
KNOWNWIDTH:
MOV AL,[RMWIDTH]
CMP AL,1
JBE ZWIDTHHEL2
JMP TWOBAD
ZWIDTHHEL2:
MOV [ENCWIDTH],AL
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
STOREPREFIX:
MOV AL,[WIDTH]
ADD AL,136
```

Remove this exact source at old physical positions 1108–1119:

```asm
CALL EMIT
MOV AL,[REG]
CALL TIMES8
MOV DL,[RMREG]
ADD AL,DL
CALL EMIT
CMP DL,6
JNE STOREEND
MOV AX,[RMDISP]
CALL EMITWORD
STOREEND:
RET
```

Replace it with:

```asm
MOV [ENCOP],AL
JMP ENCODE
```

The following old source stays in place:

```asm

SAMEWIDTH:
```

### Change 5 near `STOREPREFIX:`

Unchanged source immediately before this edit:

```asm
CALL EMIT
STOREPREFIX:
MOV AL,[WIDTH]
```

Insert after old physical line 1106.

Insert:

```asm
CALL CHECKWIDTH
MOV AL,[REG]
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
```

The following old source stays in place:

```asm
ADD AL,136
CALL EMIT
```

### Change 6 near `STOREOK:`

Unchanged source immediately before this edit:

```asm
JMP ERROR
STOREOK:
CALL RMFIRST
```

Remove this exact source at old physical positions 1101–1105:

```asm
MOV AL,[P1]
CMP AL,0
JE STOREPREFIX
CALL EMIT
STOREPREFIX:
```

There is no replacement source.

The following old source stays in place:

```asm
MOV AL,[WIDTH]
ADD AL,136
```

### Change 7 near `STOREMEM:`

Unchanged source immediately before this edit:

```asm
STOREMEM:
MOV AL,[KIND]
CMP AL,1
```

Remove this exact source at old physical positions 1096–1099:

```asm
JE STOREOK
MOV AX,1
JMP ERROR
STOREOK:
```

Replace it with:

```asm
JE ZSTOREMEM1
JMP TWOBAD
ZSTOREMEM1:
```

The following old source stays in place:

```asm
CALL RMFIRST
MOV AL,[P1]
```

### Change 8 near `LOADPREFIX:`

Unchanged source immediately before this edit:

```asm
LOADPREFIX:
MOV AL,[W1]
ADD AL,138
```

Remove this exact source at old physical positions 1080–1091:

```asm
CALL EMIT
MOV AL,[R1]
CALL TIMES8
MOV DL,[RMREG]
ADD AL,DL
CALL EMIT
CMP DL,6
JNE LOADEND
MOV AX,[RMDISP]
CALL EMITWORD
LOADEND:
RET
```

Replace it with:

```asm
MOV [ENCOP],AL
JMP ENCODE
```

The following old source stays in place:

```asm

STOREMEM:
```

### Change 9 near `LOADPREFIX:`

Unchanged source immediately before this edit:

```asm
CALL EMIT
LOADPREFIX:
MOV AL,[W1]
```

Insert after old physical line 1078.

Insert:

```asm
CALL CHECKWIDTH
MOV AL,[R1]
MOV [REGFIELD],AL
MOV AL,[ENCWIDTH]
```

The following old source stays in place:

```asm
ADD AL,138
CALL EMIT
```

### Change 10 near `LOADMEM:`

Unchanged source immediately before this edit:

```asm

LOADMEM:
CALL RMCURRENT
```

Remove this exact source at old physical positions 1073–1077:

```asm
MOV AL,[PREFIX]
CMP AL,0
JE LOADPREFIX
CALL EMIT
LOADPREFIX:
```

There is no replacement source.

The following old source stays in place:

```asm
MOV AL,[W1]
ADD AL,138
```

### Change 11 near `OPERAND:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

OPERAND:
```

Insert after old physical line 592.

Insert:

```asm
MOV AL,255
MOV [EXWIDTH],AL
```

The following old source stays in place:

```asm
MOV AL,0
MOV [PREFIX],AL
```

## Build the stopping point

```dos
COPY A26.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 05126 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A26.COM
```

VIEW.BAS must report A26.COM length 5126 bytes. Keep that executable and source together.

## Acceptance check

Create T26.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,[1234H]
MOV [BX],AX
```

```dos
COPY T26.ASM SOURCE.ASM
```

```dos
CHECK A26
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

Create X26.ASM with this separate source:

```asm
MOV AX,[BP]
```

```dos
COPY X26.ASM SOURCE.ASM
CHECK A26
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
