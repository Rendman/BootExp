+++
title = "28 \u00b7 Near calls and jumps"
weight = 28
description = "Subtract the address after the three-byte instruction."
download = "AS28.ASM"
download_group = "tools/asm0"
reader_names = 1
+++

We shall assemble control transfers which remain in the current code segment, including a forward call to a named routine.

## How it works

Class seven carries E8H for CALL or E9H for JMP. NEARJUMP reads the destination, subtracts PC plus three, and emits the opcode and a word displacement. The 8086/8088 subtraction already wraps into the unsigned sixteen-bit pattern needed for a backward transfer.

CALL pushes the offset of the following instruction. RET takes that offset back from the stack; a routine must restore its own saved words first. JMP pushes nothing. Neither transfer changes arithmetic flags by itself, although a called routine may do so.

NEARJUMP preserves the computed displacement on the stack while emitting the opcode. It changes VALUE's scratch state, AX, DX, PC, OUTPTR, and flags. Every accepted near transfer is three bytes. Far calls, indirect transfers, and automatic short-JMP selection are omitted because this workbench uses one .COM segment and fixed instruction sizes.

The complete test calls SAY, which displays C, then returns to the termination code. SAY begins five bytes beyond the return address, so the CALL displacement is 0005H.

## Source changes

Copy `AS27.ASM` to `AS28.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `OPTAB:`

Unchanged code immediately before this edit:

```asm
DB 80,85,83,72,0,0,5,80
DB 80,79,80,0,0,0,5,88
DB 73,78,84,0,0,0,6,205
```

Insert after old physical line 1090, before the following old line.

Insert this source:

```asm
DB 67,65,76,76,0,0,7,232
DB 74,77,80,0,0,0,7,233
```

### Change 2: following `INTERRUPT:`

Unchanged code immediately before this edit:

```asm
CALL EMIT
POP AX
CALL BYTEVALUE
```

Insert after old physical line 687, before the following old line.

Insert this source:

```asm
CALL FINISH
RET

NEARJUMP:
CALL SCAN
CALL VALUE
MOV DX,[PC]
ADD DX,3
SUB AX,DX
PUSH AX
MOV AL,[OP]
CALL EMIT
POP AX
CALL EMITWORD
```

### Change 3: following `STNEXT6:`

Unchanged code immediately before this edit:

```asm
CALL INTERRUPT
RET
STNEXT6:
```

Insert after old physical line 633, before the following old line.

Insert this source:

```asm
CMP AL,7
JNE STNEXT7
CALL NEARJUMP
RET
STNEXT7:
```

### Change 4: following `INSTRUCTION:`

Unchanged code immediately before this edit:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

Remove these exact old lines (physical lines 599–599 of `AS27.ASM`):

```asm
MOV CX,19
```

Put this source in their place:

```asm
MOV CX,21
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BOOTASM.BAS
```

Enter `AS28` at its source prompt. Require `OK AS28.COM 2474 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T28.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
CALL SAY
MOV AX,4C00H
INT 21H
SAY:
MOV DL,43H
MOV AH,2
INT 21H
RET
```

```dos
CHECK AS28
```

Enter `T28` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T28
OK 00015 bytes
PASS
```

Inspect `T28.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `T28.COM`, and require a length of **15 bytes** with these hexadecimal bytes:

```text
E8 05 00 B8 00 4C CD 21 B2 43 B4 02 CD 21 C3
```

Use `SYSTEM` to return to DOS.

`T28.COM` is also a complete executable. Run `CHECK T28`. It displays `C` followed by the checker's blank line and `PASS`.

## A rejection check

Enter this separate file as `X28.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
CALL LOST
```

Run `CHECK AS28` and enter `X28`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 3
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
