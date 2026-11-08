+++
title = "18 \u00b7 Recording an address"
weight = 18
description = "Store up to 256 names in fixed twenty-byte records."
download = "AS18.ASM"
aliases = ["/bootstrap/asm86/19-recording-an-address/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/18-recording-an-address/"
+++

The parser can recognize a label line. I want ASM0 to remember what that label means after it has read past it. I'll store the spelling and the current address together, then check that address when the second pass reaches the same name.

## How it works

SYMC counts the records in use and SYMNEXT points at the next free slot, initially 3000H. A symbol record occupies twenty bytes: seventeen bytes for a name and zero terminator, one padding byte, and a word value at offset eighteen. The table's 256 records occupy 3000H through 43FFH.

DEFINE validates the token, refuses a register name, and searches the existing records. On pass one a match is a duplicate error. Otherwise COPYZ writes the name, PC supplies the word value, SYMNEXT advances by twenty, and SYMC advances by one. A full table selects capacity code 5 before another record is written.

Pass two does not enter definitions again. It requires each name to exist and its retained value to equal the current PC. This detects an inconsistent definition rather than silently changing the table. SYMC and SYMNEXT are initialized once, outside PASSSTART, so the first-pass table survives reopening the source.

Only names and their addresses are being recorded here; data operands remain numeric. The byte result demonstrates that definitions themselves occupy no space. A repeated definition must now be rejected.

## Source changes

Copy `AS17.ASM` to `AS18.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `OUTPTR:`

Unchanged code immediately before this edit:

```asm
OUTPTR:
DW 24576

```

Insert after old physical line 611, before the following old line.

Insert this source:

```asm
SYMC:
DW 0

SYMNEXT:
DW 12288

```

### Change 2: following `IMAGEFULL:`

Unchanged code immediately before this edit:

```asm
MOV AX,5
JMP ERROR

```

Insert after old physical line 518, before the following old line.

Insert this source:

```asm
COPYZ:
LODSB
STOSB
CMP AL,0
JNE COPYZ
RET

```

### Change 3: following `DEFINE:`

Unchanged code immediately before this edit:

```asm
JE SPELLGOOD
MOV AX,3
JMP ERROR
```

Remove these exact old lines (physical lines 404–405 of `AS17.ASM`):

```asm
SPELLGOOD:
RET
```

No replacement lines are needed.

### Change 4: following `DEFINE:`

Unchanged code immediately before this edit:

```asm
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
```

Remove these exact old lines (physical lines 401–401 of `AS17.ASM`):

```asm
JE SPELLGOOD
```

Put this source in their place:

```asm
JNE DEFINEBAD
MOV BX,3000H
MOV CX,[SYMC]
MOV AX,20
CALL LOOK
MOV AL,[PASS]
CMP AL,1
JNE CHECKDEFINE
CMP BX,0
JNE DEFINEBAD
MOV AX,[SYMC]
CMP AX,256
JAE TABLEFULL
MOV DI,[SYMNEXT]
PUSH SI
MOV SI,2300H
CALL COPYZ
POP SI
MOV BX,[SYMNEXT]
ADD BX,18
MOV AX,[PC]
MOV [BX],AX
MOV AX,[SYMNEXT]
ADD AX,20
MOV [SYMNEXT],AX
MOV AX,[SYMC]
INC AX
MOV [SYMC],AX
RET
CHECKDEFINE:
CMP BX,0
JE DEFINEBAD
ADD BX,18
MOV AX,[BX]
MOV DX,[PC]
CMP AX,DX
JE DEFINEEND
JMP DEFINEBAD
DEFINEEND:
RET
TABLEFULL:
MOV AX,5
JMP ERROR
DEFINEBAD:
```

### Change 5: following `ROOM:`

Unchanged code immediately before this edit:

```asm
ROOM:
MOV AL,1
MOV [PASS],AL
```

Insert after old physical line 10, before the following old line.

Insert this source:

```asm
MOV AX,0
MOV [SYMC],AX
MOV AX,3000H
MOV [SYMNEXT],AX
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS18.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1488 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS18.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T18.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
START:
DB 65
END:
```

```dos
COPY T18.ASM SOURCE.ASM
```

```dos
CHECK AS18
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00001 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **1 bytes** with these hexadecimal bytes:

```text
41
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X18.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
AGAIN:
DB 1
AGAIN:
```

```dos
COPY X18.ASM SOURCE.ASM
CHECK AS18
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00003 CODE 3
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
