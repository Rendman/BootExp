+++
title = "28 \u00b7 Short conditional branches"
weight = 28
description = "A signed byte selects a nearby path from the flags."
download = "AS28.ASM"
cartoon = "asm86-signals.png"
aliases = ["/bootstrap/asm86/29-short-conditional-branches/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/28-short-conditional-branches/"
+++

Conditional jumps are still missing from the language ASM0 accepts, although I have used them throughout its source. I'll add the short conditions and their distance checks. Then I can look at the whole assembler listing and ask whether every line is within its vocabulary.

## How it works

Class eight carries the condition opcode: 72H through 77H for unsigned comparisons. JE and JNE test equality for either interpretation. The reference gives the flag expressions for every accepted spelling.

SHORTJUMP subtracts PC plus two from the target. Pass one accepts a placeholder for an unknown name. Pass two accepts unsigned word results 0000H through 007FH or FF80H through FFFFH, the bit patterns for displacements zero through 127 or minus 128 through minus one. Any other result selects range code 4.

Only AL is emitted as the displacement byte. AX is saved while the opcode is emitted, then restored. VALUE's scratch registers, AX, DX, PC, OUTPTR, and flags may change. There is no silent widening or processor upgrade.

A distant conditional transfer must be written as the opposite nearby condition around a three-byte near JMP. That pattern is also visible in the assembler's own source wherever a shared error exit is farther away than a short branch can reach. A CALL can reach a handler without asking a conditional branch to span the whole handler.

The complete test displays 0, 1, and 2. CMP DL,33H sets the flags for JB; no flag-changing instruction lies between that comparison and its branch.

## Source changes

Copy `AS27.ASM` to `AS28.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `OPTAB:`

Unchanged code immediately before this edit:

```asm
DB 73,78,84,0,0,0,6,205
DB 67,65,76,76,0,0,7,232
DB 74,77,80,0,0,0,7,233
```

Insert after old physical line 1045, before the following old line.

Insert this source:

```asm
DB 74,66,0,0,0,0,8,114
DB 74,65,69,0,0,0,8,115
DB 74,69,0,0,0,0,8,116
DB 74,78,69,0,0,0,8,117
DB 74,66,69,0,0,0,8,118
DB 74,65,0,0,0,0,8,119
```

### Change 2: following `NEARJUMP:`

Unchanged code immediately before this edit:

```asm
CALL EMIT
POP AX
CALL EMITWORD
```

Insert after old physical line 651, before the following old line.

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

Insert after old physical line 583, before the following old line.

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

Remove these exact old lines (physical lines 544–544 of `AS27.ASM`):

```asm
MOV CX,19
```

Put this source in their place:

```asm
MOV CX,25
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS28.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 2431 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS28.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T28.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

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
COPY T28.ASM SOURCE.ASM
```

```dos
CHECK AS28
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00017 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **17 bytes** with these hexadecimal bytes:

```text
B2 30 B4 02 CD 21 42 80 FA 33 72 F6 B8 00 4C CD 21
```

Use `SYSTEM` to return to DOS.

`RESULT.COM` is also a complete executable. Preserve it with `COPY RESULT.COM T28.COM`, then run `CHECK T28`. It displays `012` followed by the checker's blank line and `PASS`.

## A rejection check

Enter this separate file as `X28.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
JE 400H
```

```dos
COPY X28.ASM SOURCE.ASM
CHECK AS28
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
