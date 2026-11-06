+++
title = "26 \u00b7 CL shifts and rotates"
weight = 26
description = "Accept the variable-count forms supported by the 8086."
download = "A38.ASM"
download_group = "tools/asm86"
reader_names = 1
+++

The byte register CL supplies the processor's variable count.

## The working parts

SHIFT recognizes CL and selects D2H or D3H instead of the count-one opcode. ROL/ROR rotate bits within the operand; RCL/RCR rotate through carry. SAL is an alias for SHL. The descriptor and width checks are unchanged.

The source does not acquire arbitrary immediate counts. The test rotates 32 left by the count one in CL, then forms ASCII A. Flag behavior and count preparation remain responsibilities of the emitted program.

## Enter the source

Copy `A37.ASM` to `A38.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 83,72,76,0,0,0,10,4
DB 83,72,82,0,0,0,10,5
DB 83,65,82,0,0,0,10,7
```

Insert after old physical line 2556.

Insert:

```asm
DB 82,79,76,0,0,0,10,0
DB 82,79,82,0,0,0,10,1
DB 82,67,76,0,0,0,10,2
DB 82,67,82,0,0,0,10,3
```

The following old source stays in place:

```asm
DB 74,90,0,0,0,0,8,116
DB 74,78,90,0,0,0,8,117
```

### Change 2 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 68,73,86,0,0,0,9,6
DB 73,68,73,86,0,0,9,7
DB 83,72,76,0,0,0,10,4
```

Insert after old physical line 2554.

Insert:

```asm
DB 83,65,76,0,0,0,10,4
```

The following old source stays in place:

```asm
DB 83,72,82,0,0,0,10,5
DB 83,65,82,0,0,0,10,7
```

### Change 3 near `ZSHIFT2:`

Unchanged source immediately before this edit:

```asm
ZSHIFT2:
CALL SCAN
CALL REGISTER
```

Insert after old physical line 2380.

Insert:

```asm
CMP AX,1
JE SHIFTCL
```

The following old source stays in place:

```asm
CALL VALUE
CMP AX,1
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
MOV CX,50
```

Replace it with:

```asm
MOV CX,55
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

```dos
COPY A38.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 06275 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A38.COM
```

VIEW.BAS must report A38.COM length 6275 bytes. Keep that executable and source together.

## Acceptance check

Create T38.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,32
MOV CL,1
ROL AX,CL
ADD AX,1
MOV DL,AL
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T38.ASM SOURCE.ASM
```

```dos
CHECK A38
```

Require:

```text
OK RESULT.COM 00022 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **22 bytes** and these complete contents:

```text
B8 20 00 B1 01 D3 C0 81 C0 01 00 8A D0 B4 02 CD 21 B8 00 4C CD 21
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X38.ASM with this separate source:

```asm
SHL AX,2
```

```dos
COPY X38.ASM SOURCE.ASM
CHECK A38
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
