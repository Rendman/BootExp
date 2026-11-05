+++
title = "23 \u00b7 Zero-filled storage directives"
weight = 23
description = "Reserve bytes or words with checked output arithmetic."
download = "A23.ASM"
+++

A fixed working area should have one clear declaration instead of a long repeated data list.

## The working parts

RESERVE evaluates a resolved count and rejects an unresolved layout value. RESW checks before doubling the count; both forms check against the remaining image space before emitting any zeroes. EMIT then streams the zero-filled region through the same output block.

The reserved bytes exist in the flat COM file. They are not a request for extra DOS memory. An image may fill offsets 0100H through EFFFH, with F000H as its end label, while the assembler's own workspace remains separate.

## Enter the source

Copy `A22.ASM` to `A23.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 74,71,69,0,0,0,8,125
DB 74,76,69,0,0,0,8,126
DB 74,71,0,0,0,0,8,127
```

Insert after old physical line 2012.

Insert:

```asm
DB 82,69,83,66,0,0,12,0
DB 82,69,83,87,0,0,12,1
```

The following old source stays in place:

```asm

SRCNAME:
```

### Change 2 near `NUMBERBAD:`

Unchanged source immediately before this edit:

```asm
MOV AX,2
JMP ERROR
```

Insert after old physical line 1875.

Insert:

```asm
RESERVE:
CALL SCAN
CALL VALUE
MOV DL,[UNRESOLVED]
CMP DL,0
JE ZRESERVE1
JMP DEFINEBAD
ZRESERVE1:
PUSH AX
CALL FINISH
POP CX
MOV AL,[OP]
CMP AL,0
JE RESERVEBYTES
CMP CX,32767
JBE ZRESERVE2
JMP TABLEFULL
ZRESERVE2:
ADD CX,CX
RESERVEBYTES:
MOV AX,[PC]
MOV DX,0F000H
SUB DX,AX
CMP CX,DX
JBE ZRESERVE3
JMP TABLEFULL
ZRESERVE3:
RESERVELOOP:
CMP CX,0
JE RESERVEND
MOV AL,0
CALL EMIT
DEC CX
JMP RESERVELOOP
RESERVEND:
RET
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

Insert after old physical line 761.

Insert:

```asm
CMP AL,12
JNE DISPATCH12
CALL RESERVE
RET
DISPATCH12:
```

The following old source stays in place:

```asm
CALL TWOOPERANDS
CALL FINISH
```

### Change 4 near `RESTOREINSTR:`

Unchanged source immediately before this edit:

```asm
POP SI
CALL RESTORENAME
MOV BX,OPTAB
```

Remove this exact source at old physical positions 718–718:

```asm
MOV CX,31
```

Replace it with:

```asm
MOV CX,33
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

```dos
COPY A23.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 04828 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A23.COM
```

VIEW.BAS must report A23.COM length 4828 bytes. Keep that executable and source together.

## Acceptance check

Create T23.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
RESB 17
RESW 3
```

```dos
COPY T23.ASM SOURCE.ASM
```

```dos
CHECK A23
```

Require:

```text
OK RESULT.COM 00023 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **23 bytes** and these complete contents:

```text
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

This result is an encoding or data exercise. Inspect its bytes; do not execute it.

## A rejection check

Create X23.ASM with this separate source:

```asm
RESW 32768
```

```dos
COPY X23.ASM SOURCE.ASM
CHECK A23
```

Require:

```text
ERROR 0000000001 CODE 5
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

## Reach the image boundary

Make LIMIT.ASM containing `RESB 61184`. Copy it to SOURCE.ASM and run CHECK A23. Require `OK RESULT.COM 61184 bytes` and PASS. VIEW.BAS must show length 61184 and zero bytes. This is storage data, never a runnable program. Preserve it; change the count to 61185 and repeat. Require `ERROR 0000000001 CODE 5` and FAIL, with the previous result unchanged. The target limit is independent of the assembler's output-block size.

An unexpected PASS fails this rejection test.

## If the result differs

Check saved expression values across EMIT, the unresolved-reference flag, and fixed statement lengths in both passes. Quoted text bypasses mnemonic folding. A reserve count must be checked before multiplication or output.
