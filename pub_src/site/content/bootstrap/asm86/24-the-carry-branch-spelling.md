+++
title = "12 \u00b7 The carry branch spelling"
weight = 12
description = "Use JC where a runtime service returns carry."
download = "A24.ASM"
cartoon = "asm86a-bridge.png"
aliases = ["/bootstrap/asm86a/24-a-conditional-bridge/"]
download_group = "tools/asm86"
reader_names = 1
url = "/bootstrap/asm86a/24-the-carry-branch-spelling/"
+++

DOS services report carry; JC names that condition directly.

## The working parts

JC has the same condition code as JB. Add one table record using the existing short-branch encoder. No new decoder is required.

## Enter the source

Copy `A23.ASM` to `A24.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `NAMELEN:`

Unchanged source immediately before this edit:

```asm
NAMELEN:
DW 0
```

Insert after old physical line 2153.

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
DB 88,79,82,0,0,0,4,6
DB 82,69,83,66,0,0,12,0
DB 82,69,83,87,0,0,12,1
```

Insert after old physical line 2051.

Insert:

```asm
DB 74,67,0,0,0,0,8,114
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
MOV CX,28
```

Replace it with:

```asm
MOV CX,29
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

## Build the stopping point

```dos
COPY A24.ASM SOURCE.ASM
CHECK ASM1
```

Require `OK RESULT.COM 04887 bytes` and PASS. Preserve this executable before using its fixed output name:

```dos
COPY RESULT.COM A24.COM
```

VIEW.BAS must report A24.COM length 4887 bytes. Keep that executable and source together.

## Acceptance check

Create T24.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
JC X
DB 0
X:
JC X
```

```dos
COPY T24.ASM SOURCE.ASM
```

```dos
CHECK A24
```

Require:

```text
OK RESULT.COM 00005 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **5 bytes** and these complete contents:

```text
72 01 00 72 FE
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X24.ASM with this separate source:

```asm
JNC X
X:
```

```dos
COPY X24.ASM SOURCE.ASM
CHECK A24
```

Require:

```text
ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check saved expression values across EMIT, the unresolved-reference flag, and fixed statement lengths in both passes. Quoted text bypasses mnemonic folding. A reserve count must be checked before multiplication or output.
