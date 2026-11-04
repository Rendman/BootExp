+++
title = "29 \u00b7 Short conditional branches"
weight = 29
description = "A signed byte selects a nearby path from the flags."
download = "AS29.ASM"
cartoon = "asm86-signals.png"
+++

A comparison needs a way to select a path. We shall add the ten short conditions and reject a destination outside their signed-byte reach.

## How it works

Class eight carries the condition opcode: 72H through 77H for unsigned comparisons, and 7CH through 7FH for signed comparisons. JE and JNE test equality for either interpretation. The reference gives the flag expressions for every accepted spelling.

SHORTJUMP subtracts PC plus two from the target. Pass one accepts a placeholder for an unknown name. Pass two accepts unsigned word results 0000H through 007FH or FF80H through FFFFH, the bit patterns for displacements zero through 127 or minus 128 through minus one. Any other result selects range code 4.

Only AL is emitted as the displacement byte. AX is saved while the opcode is emitted, then restored. VALUE's scratch registers, AX, DX, PC, OUTPTR, and flags may change. There is no silent widening or processor upgrade.

A distant conditional transfer must be written as the opposite nearby condition around a three-byte near JMP. That pattern is also visible in the assembler's own source wherever a shared error exit is farther away than a short branch can reach. A CALL can reach a handler without asking a conditional branch to span the whole handler.

The complete test displays 0, 1, and 2. CMP DL,33H sets the flags for JB; no flag-changing instruction lies between that comparison and its branch.

## Source changes

Copy `AS28.ASM` to `AS29.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `OPTAB:`

Unchanged code immediately before this edit:

```asm
DB 73,78,84,0,0,0,6,205
DB 67,65,76,76,0,0,7,232
DB 74,77,80,0,0,0,7,233
```

Insert after old physical line 1111, before the following old line.

Insert this source:

```asm
DB 74,66,0,0,0,0,8,114
DB 74,65,69,0,0,0,8,115
DB 74,69,0,0,0,0,8,116
DB 74,78,69,0,0,0,8,117
DB 74,66,69,0,0,0,8,118
DB 74,65,0,0,0,0,8,119
DB 74,76,0,0,0,0,8,124
DB 74,71,69,0,0,0,8,125
DB 74,76,69,0,0,0,8,126
DB 74,71,0,0,0,0,8,127
```

### Change 2: following `NEARJUMP:`

Unchanged code immediately before this edit:

```asm
CALL EMIT
POP AX
CALL EMITWORD
```

Insert after old physical line 706, before the following old line.

Insert this source:

```asm
CALL FINISH
RET

SHORTJUMP:
CALL SCAN
CALL VALUE
MOV DX,[PC]
ADD DX,2
SUB AX,DX
MOV DL,[PASS]
CMP DL,1
JE SHORTOK
CMP AX,127
JBE SHORTOK
CMP AX,0FF80H
JAE SHORTOK
MOV AX,4
JMP ERROR
SHORTOK:
PUSH AX
MOV AL,[OP]
CALL EMIT
POP AX
CALL EMIT
```

### Change 3: following `STNEXT7:`

Unchanged code immediately before this edit:

```asm
CALL NEARJUMP
RET
STNEXT7:
```

Insert after old physical line 638, before the following old line.

Insert this source:

```asm
CMP AL,8
JNE STNEXT8
CALL SHORTJUMP
RET
STNEXT8:
```

### Change 4: following `INSTRUCTION:`

Unchanged code immediately before this edit:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

Remove these exact old lines (physical lines 599–599 of `AS28.ASM`):

```asm
MOV CX,21
```

Put this source in their place:

```asm
MOV CX,31
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BAWIDE.BAS
```

Enter `AS29` at its source prompt. Require `OK AS29.COM 2622 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T29.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
MOV DL,30H
AGAIN:
MOV AH,2
INT 21H
INC DX
CMP DL,33H
JB AGAIN
MOV AX,4C00H
INT 21H
```

```dos
CHECK AS29
```

Enter `T29` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T29
OK 00017 bytes
PASS
```

Inspect `T29.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `T29.COM`, and require a length of **17 bytes** with these hexadecimal bytes:

```text
B2 30 B4 02 CD 21 42 80 FA 33 72 F6 B8 00 4C CD 21
```

Use `SYSTEM` to return to DOS.

`T29.COM` is also a complete executable. Run `CHECK T29`. It displays `012` followed by the checker's blank line and `PASS`.

## A rejection check

Enter this separate file as `X29.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
JE 400H
```

Run `CHECK AS29` and enter `X29`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
