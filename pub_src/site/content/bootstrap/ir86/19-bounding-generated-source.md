+++
title = "19 \u00b7 Bounding generated source"
weight = 19
description = "Account for target definitions and completed assembly lines."
download = "IR19.ASM"
+++

A translator should respect the assembler's source and name limits as well as its byte-image limit.

## How it works

DEFS begins at one for I_ENTRY. NEWDEF counts each emitted user definition and refuses a count above 256. EMITCHAR now counts line feeds in OUTLINES and refuses more than 4000 assembly lines. The check happens before a successful output file is reported.

These are separate resources: a label emits no machine bytes, while a short DB row may emit many bytes on one line. Counting only output bytes would not protect the other limits. The generated template lines fit within ASM86's physical line width.

The name test uses the longest permitted IR spelling. U_ plus that name exactly fits the assembler's name bound. A longer name is rejected by NAMEARG before it can create invalid assembly. Duplicate and undefined user names are still diagnosed by ASM86, which owns address resolution.

## Source changes

Copy `IR18.ASM` to `IR19.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `TARGETSIZE:`

Unchanged code immediately before the edit:

```asm
TARGETSIZE:
DW 0

```

Insert after old physical line 957, before the following old line.

Insert this source:

```asm
DEFS:
DW 0

OUTLINES:
DW 0

```

### Change 2: following `SIZEGOOD:`

Unchanged code immediately before the edit:

```asm
MOV [TARGETSIZE],AX
RET

```

Insert after old physical line 787, before the following old line.

Insert this source:

```asm
NEWDEF:
MOV AX,[DEFS]
CMP AX,256
JB DEFROOM
MOV AX,5
JMP ERROR
DEFROOM:
INC AX
MOV [DEFS],AX
RET

```

### Change 3: following `CHARROOM:`

Unchanged code immediately before the edit:

```asm
MOV [BX],AL
INC BX
MOV [OUTPTR],BX
```

Insert after old physical line 577, before the following old line.

Insert this source:

```asm
CMP AL,10
JNE CHARDONE
MOV BX,[OUTLINES]
INC BX
CMP BX,4000
JBE LINEROOM
JMP TEXTFULL
LINEROOM:
MOV [OUTLINES],BX
```

### Change 4: following `STATLAST:`

Unchanged code immediately before the edit:

```asm
CALL FLOW
CALL SIZEADD
MOV AL,[CLASS]
```

Insert after old physical line 519, before the following old line.

Insert this source:

```asm
CMP AL,3
JB STATNODEF
CMP AL,6
JA STATNODEF
CALL NEWDEF
STATNODEF:
MOV AL,[CLASS]
```

### Change 5: following `ROOM:`

Unchanged code immediately before the edit:

```asm
MOV [OUTPTR],AX
MOV AX,15
MOV [TARGETSIZE],AX
```

Insert after old physical line 13, before the following old line.

Insert this source:

```asm
MOV AX,1
MOV [DEFS],AX
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR19` at ASM86's `Source name:` prompt. Require `OK 02770 bytes` followed by PASS. This builds `IR19.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T19.IR` with `COPY CON T19.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
WORD ABCDEFGHIJKLMN 0
LABEL MAIN
LD ABCDEFGHIJKLMN
EXIT
```

```dos
CHECK IR19
```

Enter `T19` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T19
OK T19.ASM 00159 text bytes
PASS
```

Run `TYPE T19.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_ABCDEFGHIJKLMN:
DW 0
U_MAIN:
MOV AX,[U_ABCDEFGHIJKLMN]
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T19`. Require `OK 00025 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T19.COM`, and require length **25 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 02 00 00
00 8B 06 0F 01 B4 4C CD 21
```

`T19.COM` is a complete program. Run `CHECK T19`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X19.IR` using COPY CON and the same end-of-input keystroke:

```ir
WORD ABCDEFGHIJKLMNO 0
LABEL MAIN
HALT
```

Run `CHECK IR19` and enter `X19`. Require this diagnostic and FAIL:

```text
IR ERROR 00001 CODE 3
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.
