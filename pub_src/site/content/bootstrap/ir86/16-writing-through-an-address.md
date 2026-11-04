+++
title = "16 \u00b7 Writing through an address"
weight = 16
description = "Consume a saved pointer and retain the value being stored."
download = "IR16.ASM"
+++

A buffer writer needs a pointer and a value at the same time. The expression stack can retain the pointer while AX receives the value.

## How it works

PUT pops the address into BX and writes AX through [BX]. PUTB writes AL instead. AX retains the stored word in either case, while the expression stack loses the saved pointer. The width of the operation determines how many bytes are written.

The order is address, PUSH, value, PUT. It differs from an arithmetic left operand only in the meaning of the saved word. FLOW applies the same consume-one check, so a missing address cannot accidentally pop a native return address.

These operations perform no runtime bounds check. The test uses declared storage, replaces nonzero initializers with zero through pointers, then reads the named locations and adds their values before EXIT.

## Source changes

Copy `IR15.ASM` to `IR16.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_FETCHB:`

Unchanged code immediately before the edit:

```asm
DB 77,79,86,32,66,88,44,65,88,13,10,77,79,86,32,65
DB 76,44,91,66,88,93,13,10,77,79,86,32,65,72,44,48
DB 13,10,0
```

Insert after old physical line 974, before the following old line.

Insert this source:

```asm

T_PUT:
DB 80,79,80,32,66,88,13,10,77,79,86,32,91,66,88,93
DB 44,65,88,13,10,0

T_PUTB:
DB 80,79,80,32,66,88,13,10,77,79,86,32,91,66,88,93
DB 44,65,76,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_FETCH
DB 70,69,84,67,72,66,0,0,0,0,6,0
DW T_FETCHB
```

Insert after old physical line 804, before the following old line.

Insert this source:

```asm
DB 80,85,84,0,0,0,0,0,0,2,3,0
DW T_PUT
DB 80,85,84,66,0,0,0,0,0,2,3,0
DW T_PUTB
```

### Change 3: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 485–485 in `IR15.ASM`):

```asm
MOV CX,21
```

Put this source in their place:

```asm
MOV CX,23
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR16` at ASM86's `Source name:` prompt. Require `OK 02514 bytes` followed by PASS. This builds `IR16.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T16.IR` with `COPY CON T16.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
WORD TOTAL 7
BYTE ITEM 65
LABEL MAIN
ADDR TOTAL
PUSH
LIT 0
PUT
ADDR ITEM
PUSH
LIT 0
PUTB
LD TOTAL
PUSH
LDB ITEM
ADD
EXIT
```

```dos
CHECK IR16
```

Enter `T16` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T16
OK T16.ASM 00323 text bytes
PASS
```

Run `TYPE T16.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_TOTAL:
DW 7
U_ITEM:
DB 65
U_MAIN:
MOV AX,U_TOTAL
PUSH AX
MOV AX,0
POP BX
MOV [BX],AX
MOV AX,U_ITEM
PUSH AX
MOV AX,0
POP BX
MOV [BX],AL
MOV AX,[U_TOTAL]
PUSH AX
MOV AL,[U_ITEM]
MOV AH,0
POP BX
ADD AX,BX
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T16`. Require `OK 00056 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T16.COM`, and require length **56 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 03 00 07
00 41 B8 0F 01 50 B8 00 00 5B 89 07 B8 11 01 50
B8 00 00 5B 88 07 8B 06 0F 01 50 8A 06 11 01 B4
00 5B 03 C3 B4 4C CD 21
```

`T16.COM` is a complete program. Run `CHECK T16`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X16.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
PUT
```

Run `CHECK IR16` and enter `X16`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the table effect and target-size fields separately. A saved expression word must be consumed before a label or control boundary. Compare the generated source and its byte count before executing the target.
