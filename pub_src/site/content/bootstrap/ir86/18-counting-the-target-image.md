+++
title = "18 \u00b7 Counting the target image"
weight = 18
description = "Check machine-byte demand separately from assembly-text length."
download = "IR18.ASM"
+++

The assembly text and the program it describes have different sizes. Both need their own bounds.

## How it works

Each instruction record carries its emitted machine-byte count. SIZEADD adds that count to TARGETSIZE; BUFFER contributes NUMV instead. The fixed header begins the count at fifteen bytes. An appended HALT contributes five, just as an explicit HALT does.

The count may not exceed ASM86's 8192-byte image limit. Every selected instruction form has a fixed encoding length; there is no immediate shortening or branch relaxation. The count therefore remains independent of forward-reference values.

The rejection source fits the text buffer but its buffer declarations exceed the machine-image bound. This distinguishes the image check from the existing text-byte check. A failure still occurs before output creation, so an older .ASM is not replaced.

## Source changes

Copy `IR17.ASM` to `IR18.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `DEPTH:`

Unchanged code immediately before the edit:

```asm
DEPTH:
DW 0

```

Insert after old physical line 928, before the following old line.

Insert this source:

```asm
TARGETSIZE:
DW 0

```

### Change 2: following `FINISHOUTPUT:`

Unchanged code immediately before the edit:

```asm
MOV AL,[LAST]
CMP AL,1
JE OUTPUTDONE
```

Insert after old physical line 796, before the following old line.

Insert this source:

```asm
MOV AL,0
MOV [CLASS],AL
MOV AL,5
MOV [INSIZE],AL
CALL SIZEADD
```

### Change 3: following `STACKBAD:`

Unchanged code immediately before the edit:

```asm
MOV AX,4
JMP ERROR

```

Insert after old physical line 766, before the following old line.

Insert this source:

```asm
SIZEADD:
MOV AL,[INSIZE]
MOV AH,0
MOV DL,[CLASS]
CMP DL,6
JNE ADDSIZE
MOV AX,[NUMV]
ADDSIZE:
MOV DX,[TARGETSIZE]
ADD AX,DX
CMP AX,8192
JBE SIZEGOOD
MOV AX,5
JMP ERROR
SIZEGOOD:
MOV [TARGETSIZE],AX
RET

```

### Change 4: following `STATLAST:`

Unchanged code immediately before the edit:

```asm
CALL FINISH
CALL CONTEXT
CALL FLOW
```

Insert after old physical line 515, before the following old line.

Insert this source:

```asm
CALL SIZEADD
```

### Change 5: following `ROOM:`

Unchanged code immediately before the edit:

```asm
CALL GETNAME
MOV AX,6000H
MOV [OUTPTR],AX
```

Insert after old physical line 11, before the following old line.

Insert this source:

```asm
MOV AX,15
MOV [TARGETSIZE],AX
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR18` at ASM86's `Source name:` prompt. Require `OK 02697 bytes` followed by PASS. This builds `IR18.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T18.IR` with `COPY CON T18.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
BUFFER DATA 17
LABEL MAIN
HALT
```

```dos
CHECK IR18
```

Enter `T18` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T18
OK T18.ASM 00160 text bytes
PASS
```

Run `TYPE T18.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_DATA:
DB 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
DB 0
U_MAIN:
MOV AX,4C00H
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T18`. Require `OK 00037 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T18.COM`, and require length **37 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 11 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
B8 00 4C CD 21
```

`T18.COM` is a complete program. Run `CHECK T18`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X18.IR` using COPY CON and the same end-of-input keystroke:

```ir
BUFFER B0 256
BUFFER B1 256
BUFFER B2 256
BUFFER B3 256
BUFFER B4 256
BUFFER B5 256
BUFFER B6 256
BUFFER B7 256
BUFFER B8 256
BUFFER B9 256
BUFFER B10 256
BUFFER B11 256
BUFFER B12 256
BUFFER B13 256
BUFFER B14 256
BUFFER B15 256
BUFFER B16 256
BUFFER B17 256
BUFFER B18 256
BUFFER B19 256
BUFFER B20 256
BUFFER B21 256
BUFFER B22 256
BUFFER B23 256
BUFFER B24 256
BUFFER B25 256
BUFFER B26 256
BUFFER B27 256
BUFFER B28 256
BUFFER B29 256
BUFFER B30 256
BUFFER B31 256
LABEL MAIN
HALT
```

Run `CHECK IR18` and enter `X18`. Require this diagnostic and FAIL:

```text
IR ERROR 00032 CODE 5
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.
