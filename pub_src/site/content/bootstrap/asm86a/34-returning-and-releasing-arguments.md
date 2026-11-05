+++
title = "34 \u00b7 Returning and releasing arguments"
weight = 34
description = "Encode the optional near-return adjustment explicitly."
download = "A34.ASM"
+++

A callee can return while discarding a stated amount of argument storage.

## The working parts

A bare RET remains C3H. RET followed by a word expression emits C2H and that word. The return address is removed first, then the stack adjustment is applied by the processor.

The test passes a word, establishes BP, reads the argument, restores BP, and uses RET 2. The assembler accepts the encoding; agreeing on argument ownership remains a program calling-convention responsibility.

## Enter the source

Copy `A33.ASM` to `A34.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 68,66,0,0,0,0,1,0
DB 68,87,0,0,0,0,1,1
DB 78,79,80,0,0,0,2,144
```

Remove this exact source at old physical positions 2421–2421:

```asm
DB 82,69,84,0,0,0,2,195
```

Replace it with:

```asm
DB 82,69,84,0,0,0,14,195
```

The following old source stays in place:

```asm
DB 67,76,68,0,0,0,2,252
DB 76,79,68,83,66,0,2,172
```

### Change 2 near `ZLEAOP4:`

Unchanged source immediately before this edit:

```asm
MOV [ENCOP],AL
JMP ENCODE
```

Insert after old physical line 2311.

Insert:

```asm
RETURNOP:
PUSH SI
CALL SCAN
MOV AL,[0CC00H]
CMP AL,0
JNE RETURNVALUE
POP SI
MOV AL,195
CALL EMIT
JMP FINISH
RETURNVALUE:
POP AX
CALL VALUE
PUSH AX
MOV AL,194
CALL EMIT
POP AX
CALL EMITWORD
JMP FINISH
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 3 near `DISPATCH12:`

Unchanged source immediately before this edit:

```asm
CALL RESERVE
RET
DISPATCH12:
```

Insert after old physical line 898.

Insert:

```asm
CMP AL,14
JNE DISPATCH14
CALL RETURNOP
RET
DISPATCH14:
```

The following old source stays in place:

```asm
CALL TWOOPERANDS
CALL FINISH
```

## Build the stopping point

```dos
COPY A34.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 05993 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A34.COM
```

VIEW.BAS must report A34.COM length 5993 bytes. Keep that executable and source together.

## Acceptance check

Create T34.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,65
PUSH AX
CALL F
MOV DL,AL
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
F:
PUSH BP
MOV BP,SP
MOV AX,[BP+4]
POP BP
RET 2
```

```dos
COPY T34.ASM SOURCE.ASM
```

```dos
CHECK A34
```

Require:

```text
OK RESULT.COM 00029 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **29 bytes** and these complete contents:

```text
B8 41 00 50 E8 0B 00 8A D0 B4 02 CD 21 B8 00 4C CD 21 55 8B EC 8B 86 04 00 5D C2 02 00
```

This fixture is a complete program. Save it before another assembly and execute it:

```dos
COPY RESULT.COM TRY.COM
CHECK TRY
```

It displays "A" and the checker reports PASS.

## A rejection check

Create X34.ASM with this separate source:

```asm
RET LOST
```

```dos
COPY X34.ASM SOURCE.ASM
CHECK A34
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
