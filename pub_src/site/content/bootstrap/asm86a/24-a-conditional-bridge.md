+++
title = "12 \u00b7 A conditional bridge"
weight = 12
description = "Reach a distant target using a fixed five-byte 8086 expansion."
download = "A24.ASM"
cartoon = "asm86a-bridge.png"
+++

A conditional transfer may need to cross more than a signed-byte displacement.

## The working parts

SHORTJUMP recognizes an explicit NEAR qualifier. It emits the opposite short opcode with displacement three, followed by a near JMP whose displacement is calculated from the end of all five bytes. BRDEST retains the target while EMIT changes AX.

The expansion uses no extra symbol record. Ordinary conditionals remain short and range-checked. JZ/JNZ and JC/JNC are documented aliases for the corresponding existing conditions; there is no later-CPU near-conditional instruction.

## Enter the source

Copy `A23.ASM` to `A24.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `NAMELEN:`

Unchanged source immediately before this edit:

```asm
NAMELEN:
DW 0
```

Insert after old physical line 2158.

Insert:

```asm
BRDEST:
DW 0
```

The following old source stays in place:

```asm
LINEHI:
DW 0
```

### Change 2 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 74,71,0,0,0,0,8,127
DB 82,69,83,66,0,0,12,0
DB 82,69,83,87,0,0,12,1
```

Insert after old physical line 2056.

Insert:

```asm
DB 74,90,0,0,0,0,8,116
DB 74,78,90,0,0,0,8,117
DB 74,67,0,0,0,0,8,114
DB 74,78,67,0,0,0,8,115
```

The following old source stays in place:

```asm

SRCNAME:
```

### Change 3 near `SHORTOK:`

Unchanged source immediately before this edit:

```asm
CALL EMIT
POP AX
CALL EMIT
```

Remove this exact source at old physical positions 902–903:

```asm
CALL FINISH
RET
```

Replace it with:

```asm
JMP FINISH
```

The following old source stays in place:

```asm

FINISH:
```

### Change 4 near `SHORTJUMP:`

Unchanged source immediately before this edit:

```asm

SHORTJUMP:
CALL SCAN
```

Insert after old physical line 882.

Insert:

```asm
MOV AX,[0CC00H]
CMP AX,454EH
JE ZSHORTJUM1
JMP SHORTVALUE
ZSHORTJUM1:
MOV AX,[0CC02H]
CMP AX,5241H
JE ZSHORTJUM2
JMP SHORTVALUE
ZSHORTJUM2:
MOV AL,[0CC04H]
CMP AL,0
JE ZSHORTJUM3
JMP SHORTVALUE
ZSHORTJUM3:
CALL SCAN
CALL VALUE
MOV [BRDEST],AX
MOV AL,[OP]
XOR AL,1
CALL EMIT
MOV AL,3
CALL EMIT
MOV AX,[BRDEST]
MOV DX,[PC]
ADD DX,3
SUB AX,DX
PUSH AX
MOV AL,233
CALL EMIT
POP AX
CALL EMITWORD
JMP FINISH
SHORTVALUE:
```

The following old source stays in place:

```asm
CALL VALUE
MOV DX,[PC]
```

### Change 5 near `RESTOREINSTR:`

Unchanged source immediately before this edit:

```asm
POP SI
CALL RESTORENAME
MOV BX,OPTAB
```

Remove this exact source at old physical positions 718–718:

```asm
MOV CX,33
```

Replace it with:

```asm
MOV CX,37
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

```dos
COPY A24.ASM SOURCE.ASM
CHECK ASMA0
```

Require `OK RESULT.COM 04951 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A24.COM
```

VIEW.BAS must report A24.COM length 4951 bytes. Keep that executable and source together.

## Acceptance check

Create T24.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV AX,0
CMP AX,0
JNE NEAR BAD
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
RESB 200
BAD:
MOV AX,4C01H
INT 21H
```

```dos
COPY T24.ASM SOURCE.ASM
```

```dos
CHECK A24
```

Require:

```text
OK RESULT.COM 00228 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **228 bytes** and these first thirty-two bytes:

```text
B8 00 00 81 F8 00 00 74 03 E9 D3 00 B2 41 B4 02 CD 21 B8 00 4C CD 21 00 00 00 00 00 00 00 00 00
```

This fixture is a complete program. Save it before another assembly and execute it:

```dos
COPY RESULT.COM TRY.COM
CHECK TRY
```

It displays "A" and the checker reports PASS.

## A rejection check

Create X24.ASM with this separate source:

```asm
JNE 400H
```

```dos
COPY X24.ASM SOURCE.ASM
CHECK A24
```

Require:

```text
ERROR 0000000001 CODE 4
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check saved expression values across EMIT, the unresolved-reference flag, and fixed statement lengths in both passes. Quoted text bypasses mnemonic folding. A reserve count must be checked before multiplication or output.
