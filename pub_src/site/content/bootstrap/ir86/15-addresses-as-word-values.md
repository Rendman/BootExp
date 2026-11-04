+++
title = "15 \u00b7 Addresses as word values"
weight = 15
description = "Form an address and fetch through the accumulator."
download = "IR15.ASM"
+++

A loop needs to advance a pointer instead of naming every byte separately. ADDR produces an offset as an ordinary word.

## How it works

ADDR name emits MOV AX,U_name. FETCH copies that offset to BX and reads a word through [BX]. FETCHB reads one byte and clears AH. Both replace the address in AX with the fetched value; BX and flags are scratch.

All addresses are offsets in DS, which remains the DOS program segment. No segment value or far pointer is introduced. A pointer can be advanced with the existing word arithmetic. The programmer must keep it within allocated storage and allow two bytes for a word fetch.

The test fetches a declared word and a byte through their addresses, adds the two zero values, and returns zero. The emitted target uses exactly the BX-based memory form already accepted by ASM86.

## Source changes

Copy `IR14.ASM` to `IR15.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_XOR:`

Unchanged code immediately before the edit:

```asm
T_XOR:
DB 80,79,80,32,66,88,13,10,88,79,82,32,65,88,44,66
DB 88,13,10,0
```

Insert after old physical line 956, before the following old line.

Insert this source:

```asm

T_ADDR:
DB 77,79,86,32,65,88,44,85,95,64,13,10,0

T_FETCH:
DB 77,79,86,32,66,88,44,65,88,13,10,77,79,86,32,65
DB 88,44,91,66,88,93,13,10,0

T_FETCHB:
DB 77,79,86,32,66,88,44,65,88,13,10,77,79,86,32,65
DB 76,44,91,66,88,93,13,10,77,79,86,32,65,72,44,48
DB 13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_OR
DB 88,79,82,0,0,0,0,0,0,2,3,0
DW T_XOR
```

Insert after old physical line 798, before the following old line.

Insert this source:

```asm
DB 65,68,68,82,0,0,0,0,2,0,3,0
DW T_ADDR
DB 70,69,84,67,72,0,0,0,0,0,4,0
DW T_FETCH
DB 70,69,84,67,72,66,0,0,0,0,6,0
DW T_FETCHB
```

### Change 3: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 485–485 in `IR14.ASM`):

```asm
MOV CX,18
```

Put this source in their place:

```asm
MOV CX,21
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR15` at ASM86's `Source name:` prompt. Require `OK 02442 bytes` followed by PASS. This builds `IR15.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T15.IR` with `COPY CON T15.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
WORD TOTAL 0
BYTE ITEM 0
LABEL MAIN
ADDR TOTAL
FETCH
PUSH
ADDR ITEM
FETCHB
ADD
EXIT
```

```dos
CHECK IR15
```

Enter `T15` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T15
OK T15.ASM 00255 text bytes
PASS
```

Run `TYPE T15.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_TOTAL:
DW 0
U_ITEM:
DB 0
U_MAIN:
MOV AX,U_TOTAL
MOV BX,AX
MOV AX,[BX]
PUSH AX
MOV AX,U_ITEM
MOV BX,AX
MOV AL,[BX]
MOV AH,0
POP BX
ADD AX,BX
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T15`. Require `OK 00042 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T15.COM`, and require length **42 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 03 00 00
00 00 B8 0F 01 8B D8 8B 07 50 B8 11 01 8B D8 8A
07 B4 00 5B 03 C3 B4 4C CD 21
```

`T15.COM` is a complete program. Run `CHECK T15`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X15.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
ADDR A+B
```

Run `CHECK IR15` and enter `X15`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 3
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.
