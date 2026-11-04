+++
title = "20 \u00b7 Using a named value"
weight = 20
description = "Resolve forward references on the collecting pass."
download = "AS20.ASM"
+++

A saved address can replace a hand-counted number. We shall let VALUE use a label, including one defined farther down the source.

## How it works

A token beginning with a decimal digit remains a number. Other tokens enter SYMBOLVALUE, which validates the name, rejects register names, and searches the symbol table. A match returns the word at record offset eighteen in AX.

An unknown name returns zero only during pass one. The width of every statement is fixed, so that placeholder changes no positions. On pass two an unknown name is a symbol error, code 3. The output file has not been opened at that point.

VALUE still preserves SI. The symbol path may change the lookup scratch registers, including BX, CX, DX, DI, and BP. A caller must not keep a live loop count in those registers without saving it.

Our test emits a word before the byte it names. TEXT therefore has loaded offset 0102H. A named address is an ordinary unsigned value: DW can hold it, while DB rejects a value above 255. Expressions such as TEXT+1 remain outside the language.

## Source changes

Copy `AS19.ASM` to `AS20.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `NUMBERBAD:`

Unchanged code immediately before this edit:

```asm
RET
NUMBERBAD:
MOV AX,2
```

Insert after old physical line 453, before the following old line.

Insert this source:

```asm
JMP ERROR

SYMBOLVALUE:
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
JNE VALUEBAD
MOV BX,3000H
MOV CX,[SYMC]
MOV AX,20
CALL LOOK
CMP BX,0
JE NOTDEFINED
ADD BX,18
MOV AX,[BX]
RET
NOTDEFINED:
MOV AL,[PASS]
CMP AL,1
JNE VALUEBAD
MOV AX,0
RET
VALUEBAD:
MOV AX,3
```

### Change 2: following `WORDVALUE:`

Unchanged code immediately before this edit:

```asm
CMP AL,57
JBE LITERAL
WORDVALUE:
```

Remove these exact old lines (physical lines 384–390 of `AS19.ASM`):

```asm
CALL REGISTER
CMP AX,0FFFFH
JNE RESERVEDNUM
JMP NUMBERBAD
RESERVEDNUM:
MOV AX,3
JMP ERROR
```

Put this source in their place:

```asm
JMP SYMBOLVALUE
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BAWIDE.BAS
```

Enter `AS20` at its source prompt. Require `OK AS20.COM 1673 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T20.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
DW TEXT
TEXT:
DB 65
```

```dos
CHECK AS20
```

Enter `T20` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T20
OK 00003 bytes
PASS
```

Inspect `T20.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `T20.COM`, and require a length of **3 bytes** with these hexadecimal bytes:

```text
02 01 41
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X20.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
DW MISSING
```

Run `CHECK AS20` and enter `X20`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 3
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
