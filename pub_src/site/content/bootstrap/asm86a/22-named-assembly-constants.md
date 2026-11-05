+++
title = "22 \u00b7 Named assembly constants"
weight = 22
description = "Give a known value a name without allocating bytes."
download = "A22.ASM"
+++

An explicit constant can replace repeated counts while leaving the location counter unchanged.

## The working parts

STATEMENT saves the first spelling before looking for EQU. Its expression must be resolved on pass one, then RESTORENAME restores the definition token for DEFINE. DEFTYPE distinguishes this absolute constant from a loaded label.

Forward or cyclic EQU definitions are rejected. Earlier labels and constants may participate in an expression, including a difference from $. Pass two must reproduce the same constant and kind. Defining a constant emits no bytes.

## Enter the source

Copy `A21.ASM` to `A22.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `EXPRDEPTH:`

Unchanged source immediately before this edit:

```asm
EXPRDEPTH:
DW 0
```

Insert after old physical line 2064.

Insert:

```asm
NAMELEN:
DW 0
```

The following old source stays in place:

```asm
LINEHI:
DW 0
```

### Change 2 near `SYNTAXBAD:`

Unchanged source immediately before this edit:

```asm
SYNTAXBAD:
MOV AX,1
JMP ERROR
```

Insert after old physical line 729.

Insert:

```asm
RESTORENAME:
PUSH SI
MOV SI,0CC40H
MOV DI,0CC00H
CALL COPYZ
POP SI
MOV AX,[NAMELEN]
MOV [TOKLEN],AX
RET
```

The following old source stays in place:

```asm

DATAITEM:
```

### Change 3 near `INSTRUCTION:`

Unchanged source immediately before this edit:

```asm
CMP BX,0
JNE ZSTATEMEN1
JMP SYNTAXBAD
```

Remove this exact source at old physical positions 686–686:

```asm
ZSTATEMEN1:
```

Replace it with:

```asm
ZSTATEMEN3:
```

The following old source stays in place:

```asm
ADD BX,6
MOV AL,[BX]
```

### Change 4 near `INSTRUCTION:`

Unchanged source immediately before this edit:

```asm
MOV AX,8
CALL LOOK
CMP BX,0
```

Remove this exact source at old physical positions 684–684:

```asm
JNE ZSTATEMEN1
```

Replace it with:

```asm
JNE ZSTATEMEN3
```

The following old source stays in place:

```asm
JMP SYNTAXBAD
ZSTATEMEN1:
```

### Change 5 near `INSTRUCTION:`

Unchanged source immediately before this edit:

```asm
RET
INSTRUCTION:
DEC SI
```

Insert after old physical line 678.

Insert:

```asm
PUSH SI
MOV AX,[TOKLEN]
MOV [NAMELEN],AX
MOV DI,0CC40H
MOV SI,0CC00H
CALL COPYZ
POP SI
PUSH SI
CALL SCAN
MOV AX,[0CC00H]
CMP AX,5145H
JE ZSTATEMEN1
JMP RESTOREINSTR
ZSTATEMEN1:
MOV AX,[0CC02H]
CMP AX,85
JNE RESTOREINSTR
POP AX
CALL SCAN
CALL VALUE
MOV [DEFVALUE],AX
MOV AL,[UNRESOLVED]
CMP AL,0
JE ZSTATEMEN2
JMP DEFINEBAD
ZSTATEMEN2:
MOV AX,1
MOV [DEFTYPE],AX
CALL FINISH
CALL RESTORENAME
CALL DEFINE
RET
RESTOREINSTR:
POP SI
CALL RESTORENAME
```

The following old source stays in place:

```asm
MOV BX,OPTAB
MOV CX,31
```

### Change 6 near `AFTERWORD:`

Unchanged source immediately before this edit:

```asm
CALL DEFINE
CALL FINISH
RET
```

Remove this exact source at old physical positions 677–677:

```asm
INSTRUCTION:
```

Replace it with:

```asm
EQUORINSTR:
```

The following old source stays in place:

```asm
DEC SI
MOV BX,OPTAB
```

### Change 7 near `AFTERWORD:`

Unchanged source immediately before this edit:

```asm
CMP AL,32
JE AFTERWORD
CMP AL,58
```

Remove this exact source at old physical positions 669–669:

```asm
JNE INSTRUCTION
```

Replace it with:

```asm
JNE EQUORINSTR
```

The following old source stays in place:

```asm
MOV AX,[PC]
MOV [DEFVALUE],AX
```

### Change 8 near `AFTERWORD:`

Unchanged source immediately before this edit:

```asm
LODSB
CMP AL,32
JE AFTERWORD
```

Insert after old physical line 667.

Insert:

```asm
CMP AL,9
JE AFTERWORD
```

The following old source stays in place:

```asm
CMP AL,58
JNE INSTRUCTION
```

### Change 9 near `STATEMENT:`

Unchanged source immediately before this edit:

```asm
CMP AL,0
JNE STWORD
RET
```

Remove this exact source at old physical positions 663–663:

```asm
STWORD:
```

There is no replacement source.

The following old source stays in place:

```asm
AFTERWORD:
LODSB
```

### Change 10 near `STATEMENT:`

Unchanged source immediately before this edit:

```asm
CALL SCAN
MOV AL,[0CC00H]
CMP AL,0
```

Remove this exact source at old physical positions 661–661:

```asm
JNE STWORD
```

Replace it with:

```asm
JNE AFTERWORD
```

The following old source stays in place:

```asm
RET
STWORD:
```

### Change 11 near `STATEMENT:`

Unchanged source immediately before this edit:

```asm
RET

STATEMENT:
```

Insert after old physical line 657.

Insert:

```asm
MOV AL,0
MOV [UNRESOLVED],AL
```

The following old source stays in place:

```asm
CALL SCAN
MOV AL,[0CC00H]
```

## Build the stopping point

```dos
COPY A22.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 04728 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A22.COM
```

VIEW.BAS must report A22.COM length 4728 bytes. Keep that executable and source together.

## Acceptance check

Create T22.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
N EQU 3
DW N
```

```dos
COPY T22.ASM SOURCE.ASM
```

```dos
CHECK A22
```

Require:

```text
OK RESULT.COM 00002 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **2 bytes** and these complete contents:

```text
03 00
```

This result is an encoding or data exercise. Inspect its bytes; do not execute it.

## A rejection check

Create X22.ASM with this separate source:

```asm
N EQU LATER
LATER:
```

```dos
COPY X22.ASM SOURCE.ASM
CHECK A22
```

Require:

```text
ERROR 0000000001 CODE 3
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check saved expression values across EMIT, the unresolved-reference flag, and fixed statement lengths in both passes. Quoted text bypasses mnemonic folding. A reserve count must be checked before multiplication or output.
