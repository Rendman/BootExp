+++
title = "39 \u00b7 Repeated byte and word movement"
weight = 39
description = "Restrict REP to the explicitly supported string instructions."
download = "A39.ASM"
+++

A block move should name its count and source/destination convention clearly.

## The working parts

REPEAT looks up MOVSB, MOVSW, STOSB, STOSW, LODSB, or LODSW in STRINGTAB, emits F3H and the fixed operation, then requires end of statement. Other REP combinations are rejected. CLD establishes forward movement; the program supplies the relevant segment registers, pointers, and CX.

The complete test copies Hi into declared storage with REP MOVSB, then displays the copy. These are genuine 8086 forms. The assembler does not initialize a program's copy count or direction flag for it.

## Enter the source

Copy `A38.ASM` to `A39.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `REGFIELD:`

Unchanged source immediately before this edit:

```asm
REGFIELD:
DB 0
```

Insert after old physical line 2723.

Insert:

```asm
STRINGOP:
DB 0
```

The following old source stays in place:

```asm
LINEHI:
DW 0
```

### Change 2 near `UNRESOLVED:`

Unchanged source immediately before this edit:

```asm
UNRESOLVED:
DB 0
```

Insert after old physical line 2663.

Insert:

```asm
STRINGTAB:
DB 77,79,86,83,66,0,2,164
DB 77,79,86,83,87,0,2,165
DB 83,84,79,83,66,0,2,170
DB 83,84,79,83,87,0,2,171
DB 76,79,68,83,66,0,2,172
DB 76,79,68,83,87,0,2,173
```

The following old source stays in place:

```asm
EXPRDEPTH:
DW 0
```

### Change 3 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 82,79,82,0,0,0,10,1
DB 82,67,76,0,0,0,10,2
DB 82,67,82,0,0,0,10,3
```

Insert after old physical line 2563.

Insert:

```asm
DB 76,79,68,83,87,0,2,173
DB 83,84,79,83,87,0,2,171
DB 77,79,86,83,66,0,2,164
DB 77,79,86,83,87,0,2,165
DB 82,69,80,0,0,0,13,243
```

The following old source stays in place:

```asm
DB 74,90,0,0,0,0,8,116
DB 74,78,90,0,0,0,8,117
```

### Change 4 near `SHIFTRANGE:`

Unchanged source immediately before this edit:

```asm
MOV AX,4
JMP ERROR
```

Insert after old physical line 2406.

Insert:

```asm
REPEAT:
CALL SCAN
MOV BX,STRINGTAB
MOV CX,6
MOV AX,8
CALL LOOK
CMP BX,0
JNE ZREPEAT1
JMP TWOBAD
ZREPEAT1:
ADD BX,7
MOV AL,[BX]
MOV [STRINGOP],AL
MOV AL,243
CALL EMIT
MOV AL,[STRINGOP]
CALL EMIT
JMP FINISH
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 5 near `DISPATCH12:`

Unchanged source immediately before this edit:

```asm
CALL RESERVE
RET
DISPATCH12:
```

Insert after old physical line 908.

Insert:

```asm
CMP AL,13
JNE DISPATCH13
CALL REPEAT
RET
DISPATCH13:
```

The following old source stays in place:

```asm
CMP AL,14
JNE DISPATCH14
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
MOV CX,55
```

Replace it with:

```asm
MOV CX,60
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

```dos
COPY A39.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 06422 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A39.COM
```

VIEW.BAS must report A39.COM length 6422 bytes. Keep that executable and source together.

## Acceptance check

Create T39.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
CLD
MOV SI,TEXT
MOV DI,DEST
MOV CX,2
REP MOVSB
MOV SI,DEST
MOV CX,2
SHOW:
MOV DL,[SI]
MOV AH,2
INT 21H
INC SI
DEC CX
JNE SHOW
MOV AX,4C00H
INT 21H
TEXT:
DB "Hi"
DEST:
RESB 2
```

```dos
COPY T39.ASM SOURCE.ASM
```

```dos
CHECK A39
```

Require:

```text
OK RESULT.COM 00037 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **37 bytes** and these first thirty-two bytes:

```text
FC BE 21 01 BF 23 01 B9 02 00 F3 A4 BE 23 01 B9 02 00 8A 14 B4 02 CD 21 46 49 75 F6 B8 00 4C CD
```

This fixture is a complete program. Save it before another assembly and execute it:

```dos
COPY RESULT.COM TRY.COM
CHECK TRY
```

It displays "Hi" and the checker reports PASS.

## A rejection check

Create X39.ASM with this separate source:

```asm
REP RET
```

```dos
COPY X39.ASM SOURCE.ASM
CHECK A39
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
