+++
title = "18 \u00b7 Checking a label line"
weight = 18
description = "Accept a standalone name and reject malformed or reserved spellings."
download = "AS18.ASM"
+++

A label has a syntax of its own. We shall recognize that syntax before giving definitions storage in a symbol table.

## How it works

After the first token, STATEMENT looks past spaces for a colon. A colon selects DEFINE; otherwise the cursor is put back at the first operand character and mnemonic lookup proceeds normally. FINISH requires the label to occupy the statement by itself. A comment may follow it.

VALIDNAME accepts one through sixteen characters: letters, digits, and underscores, with a letter or underscore first. SCAN already enforces the length. The routine preserves SI and changes AL, flags, and the lookup scratch state used by REGISTER. Register names are reserved.

At this stopping point DEFINE checks spelling and returns without storing an address. Label lines emit no bytes, but labels are not yet accepted as values and duplicate definitions are not detected. Keeping that distinction explicit makes the spelling and statement-boundary checks observable on their own.

## Source changes

Copy `AS17.ASM` to `AS18.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `DATASEP:`

Unchanged code immediately before this edit:

```asm
JE DATAITEM
CMP AL,0
JNE SYNTAXBAD
```

Insert after old physical line 469, before the following old line.

Insert this source:

```asm
RET

FINISH:
CALL SCAN
MOV AL,[2300H]
CMP AL,0
JE FINISHED
MOV AX,1
JMP ERROR
FINISHED:
```

### Change 2: following `STWORD:`

Unchanged code immediately before this edit:

```asm
JNE STWORD
RET
STWORD:
```

Insert after old physical line 426, before the following old line.

Insert this source:

```asm
AFTERWORD:
LODSB
CMP AL,32
JE AFTERWORD
CMP AL,58
JNE INSTRUCTION
CALL DEFINE
CALL FINISH
RET
INSTRUCTION:
DEC SI
```

### Change 3: following `NUMBERBAD:`

Unchanged code immediately before this edit:

```asm
MOV AX,2
JMP ERROR

```

Insert after old physical line 419, before the following old line.

Insert this source:

```asm
DEFINE:
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
JE SPELLGOOD
MOV AX,3
JMP ERROR
SPELLGOOD:
RET

```

### Change 4: following `NOREGISTER:`

Unchanged code immediately before this edit:

```asm
MOV AX,0FFFFH
RET

```

Insert after old physical line 340, before the following old line.

Insert this source:

```asm
VALIDNAME:
PUSH SI
MOV SI,2300H
LODSB
CMP AL,95
JE NAMEVALID
CMP AL,65
JB SYMBOLBAD
CMP AL,90
JA SYMBOLBAD
NAMEVALID:
LODSB
CMP AL,0
JE NAMEVALIDEND
CMP AL,95
JE NAMEVALID
CMP AL,48
JB SYMBOLBAD
CMP AL,57
JBE NAMEVALID
CMP AL,65
JB SYMBOLBAD
CMP AL,90
JBE NAMEVALID
JMP SYMBOLBAD
NAMEVALIDEND:
POP SI
RET
SYMBOLBAD:
MOV AX,3
JMP ERROR

```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BAWIDE.BAS
```

Enter `AS18` at its source prompt. Require `OK AS18.COM 1498 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T18.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
START:
DB 65
```

```dos
CHECK AS18
```

Enter `T18` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T18
OK 00001 bytes
PASS
```

Inspect `T18.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `T18.COM`, and require a length of **1 bytes** with these hexadecimal bytes:

```text
41
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X18.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
1BAD:
DB 0
```

Run `CHECK AS18` and enter `X18`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 3
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
