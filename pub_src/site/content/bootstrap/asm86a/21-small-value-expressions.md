+++
title = "09 \u00b7 Small value expressions"
weight = 9
description = "Evaluate unary signs, grouping, addition, subtraction, and the current address."
download = "A21.ASM"
+++

Addresses and counts often differ from a named value by a small offset.

## The working parts

VALUE combines FACTOR results left to right. FACTOR recognizes a number or symbol through ATOM, unary plus/minus, parentheses, and $. Native stack saves keep intermediate values distinct during recursive parsing. EXPRDEPTH bounds active factors at sixteen.

Values wrap as words, but byte and size contexts still check their own ranges. UNRESOLVED propagates through a first-pass expression so a provisional value cannot silently decide a layout count. The test uses only arithmetic whose byte results are known.

## Enter the source

Copy `A20.ASM` to `A21.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `UNRESOLVED:`

Unchanged source immediately before this edit:

```asm
UNRESOLVED:
DB 0
```

Insert after old physical line 1970.

Insert:

```asm
EXPRDEPTH:
DW 0
```

The following old source stays in place:

```asm
LINEHI:
DW 0
```

### Change 2 near `ZNUMBER323:`

Unchanged source immediately before this edit:

```asm
POP AX
RET
```

Insert after old physical line 1737.

Insert:

```asm
ATOM:
MOV AL,[0CC00H]
CMP AL,48
JB WORDVALUE
CMP AL,57
JBE LITERAL
WORDVALUE:
JMP SYMBOLVALUE
LITERAL:
PUSH SI
MOV SI,0CC00H
MOV DI,[TOKLEN]
ADD DI,0CC00H
MOV BX,DI
DEC BX
MOV AL,[BX]
MOV BP,10
CMP AL,72
JNE NUMBERSTART
MOV BP,16
DEC DI
NUMBERSTART:
CMP SI,DI
JNE ZATOM1
JMP NUMBERBAD
ZATOM1:
MOV CX,0
DIGIT:
LODSB
SUB AL,48
CMP AL,9
JBE DIGITOK
SUB AL,7
CMP AL,10
JAE ZATOM2
JMP NUMBERBAD
ZATOM2:
CMP AL,15
JBE ZATOM3
JMP NUMBERBAD
ZATOM3:
DIGITOK:
MOV AH,0
MOV DX,AX
CMP DX,BP
JB ZATOM4
JMP NUMBERBAD
ZATOM4:
CMP BP,16
JE HEXDIGIT
CMP CX,6553
JBE ZATOM5
JMP NUMBERBAD
ZATOM5:
JB DECDIGIT
CMP DX,5
JBE ZATOM6
JMP NUMBERBAD
ZATOM6:
DECDIGIT:
MOV AX,CX
ADD CX,CX
ADD AX,AX
ADD AX,AX
ADD AX,AX
ADD CX,AX
JMP ADDDIGIT
HEXDIGIT:
CMP CX,4095
JA NUMBERBAD
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADDDIGIT:
ADD CX,DX
CMP SI,DI
JAE ZATOM7
JMP DIGIT
ZATOM7:
MOV AX,CX
POP SI
RET
NUMBERBAD:
MOV AX,2
JMP ERROR
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 3 near `BYTEVALUE:`

Unchanged source immediately before this edit:

```asm
RET

BYTEVALUE:
```

Insert after old physical line 1049.

Insert:

```asm
MOV DL,[PASS]
CMP DL,1
JNE BYTECHECK
MOV DL,[UNRESOLVED]
CMP DL,0
JNE EMIT
BYTECHECK:
```

The following old source stays in place:

```asm
CMP AX,255
JBE EMIT
```

### Change 4 near `ZVALUE7:`

Unchanged source immediately before this edit:

```asm
MOV AX,CX
POP SI
RET
```

Remove this exact source at old physical positions 495–497:

```asm
NUMBERBAD:
MOV AX,2
JMP ERROR
```

There is no replacement source.

The following old source stays in place:

```asm

SYMBOLVALUE:
```

### Change 5 near `ZVALUE3:`

Unchanged source immediately before this edit:

```asm
JBE ZVALUE3
JMP NUMBERBAD
ZVALUE3:
```

Remove this exact source at old physical positions 453–493:

```asm
DIGITOK:
MOV AH,0
MOV DX,AX
CMP DX,BP
JB ZVALUE4
JMP NUMBERBAD
ZVALUE4:
CMP BP,16
JE HEXDIGIT
CMP CX,6553
JBE ZVALUE5
JMP NUMBERBAD
ZVALUE5:
JB DECDIGIT
CMP DX,5
JBE ZVALUE6
JMP NUMBERBAD
ZVALUE6:
DECDIGIT:
MOV AX,CX
ADD CX,CX
ADD AX,AX
ADD AX,AX
ADD AX,AX
ADD CX,AX
JMP ADDDIGIT
HEXDIGIT:
CMP CX,4095
JA NUMBERBAD
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADDDIGIT:
ADD CX,DX
CMP SI,DI
JAE ZVALUE7
JMP DIGIT
ZVALUE7:
MOV AX,CX
POP SI
```

Replace it with:

```asm
POP AX
JMP FACTORRETURN
FACTORPC:
MOV AX,[PC]
FACTORRETURN:
PUSH AX
MOV AX,[EXPRDEPTH]
DEC AX
MOV [EXPRDEPTH],AX
POP AX
```

The following old source stays in place:

```asm
RET
NUMBERBAD:
```

### Change 6 near `ZVALUE2:`

Unchanged source immediately before this edit:

```asm
JAE ZVALUE2
JMP NUMBERBAD
ZVALUE2:
```

Remove this exact source at old physical positions 449–451:

```asm
CMP AL,15
JBE ZVALUE3
JMP NUMBERBAD
```

Replace it with:

```asm
CALL ATOM
JMP FACTORRETURN
FACTORPLUS:
CALL SCAN
CALL FACTOR
JMP FACTORRETURN
FACTORNEG:
CALL SCAN
CALL FACTOR
MOV DX,0
SUB DX,AX
MOV AX,DX
JMP FACTORRETURN
FACTORPAREN:
CALL SCAN
CALL VALUE
PUSH AX
CALL SCAN
MOV AL,[0CC00H]
CMP AL,41
JE ZVALUE3
JMP SYNTAXBAD
```

The following old source stays in place:

```asm
ZVALUE3:
DIGITOK:
```

### Change 7 near `ZVALUE1:`

Unchanged source immediately before this edit:

```asm
JNE ZVALUE1
JMP NUMBERBAD
ZVALUE1:
```

Remove this exact source at old physical positions 438–447:

```asm
MOV CX,0
DIGIT:
LODSB
SUB AL,48
CMP AL,9
JBE DIGITOK
SUB AL,7
CMP AL,10
JAE ZVALUE2
JMP NUMBERBAD
```

Replace it with:

```asm
MOV AL,[0CC00H]
CMP AL,43
JE FACTORPLUS
CMP AL,45
JE FACTORNEG
CMP AL,40
JE FACTORPAREN
CMP AL,36
JNE ZVALUE2
JMP FACTORPC
```

The following old source stays in place:

```asm
ZVALUE2:
CMP AL,15
```

### Change 8 near `VALUE:`

Unchanged source immediately before this edit:

```asm

VALUE:
MOV AL,[0CC00H]
```

Remove this exact source at old physical positions 414–436:

```asm
CMP AL,48
JB WORDVALUE
CMP AL,57
JBE LITERAL
WORDVALUE:
JMP SYMBOLVALUE
LITERAL:
PUSH SI
MOV SI,0CC00H
MOV DI,[TOKLEN]
ADD DI,0CC00H
MOV BX,DI
DEC BX
MOV AL,[BX]
MOV BP,10
CMP AL,72
JNE NUMBERSTART
MOV BP,16
DEC DI
NUMBERSTART:
CMP SI,DI
JNE ZVALUE1
JMP NUMBERBAD
```

Replace it with:

```asm
CMP AL,43
JE EXPRESSIONADD
CMP AL,45
JE EXPRESSIONSUB
POP SI
POP AX
RET
EXPRESSIONADD:
POP AX
CALL SCAN
CALL FACTOR
MOV DX,AX
POP AX
ADD AX,DX
JMP EXPRESSIONLOOP
EXPRESSIONSUB:
POP AX
CALL SCAN
CALL FACTOR
MOV DX,AX
POP AX
SUB AX,DX
JMP EXPRESSIONLOOP
FACTOR:
MOV AX,[EXPRDEPTH]
INC AX
MOV [EXPRDEPTH],AX
CMP AX,16
JBE ZVALUE1
JMP TABLEFULL
```

The following old source stays in place:

```asm
ZVALUE1:
MOV CX,0
```

### Change 9 near `VALUE:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

VALUE:
```

Insert after old physical line 412.

Insert:

```asm
CALL FACTOR
EXPRESSIONLOOP:
PUSH AX
PUSH SI
CALL SCAN
```

The following old source stays in place:

```asm
MOV AL,[0CC00H]
CMP AL,48
```

## Build the stopping point

```dos
COPY A21.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 04605 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A21.COM
```

VIEW.BAS must report A21.COM length 4605 bytes. Keep that executable and source together.

## Acceptance check

Create T21.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
DB 1+2,4-1,(5-2),-(-3)
```

```dos
COPY T21.ASM SOURCE.ASM
```

```dos
CHECK A21
```

Require:

```text
OK RESULT.COM 00004 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **4 bytes** and these complete contents:

```text
03 03 03 03
```

This result is an encoding or data exercise. Inspect its bytes; do not execute it.

## A rejection check

Create X21.ASM with this separate source:

```asm
DW 65536
```

```dos
COPY X21.ASM SOURCE.ASM
CHECK A21
```

Require:

```text
ERROR 0000000001 CODE 2
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check saved expression values across EMIT, the unresolved-reference flag, and fixed statement lengths in both passes. Quoted text bypasses mnemonic folding. A reserve count must be checked before multiplication or output.
