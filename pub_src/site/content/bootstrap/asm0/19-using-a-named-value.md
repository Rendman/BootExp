+++
title = "19 \u00b7 Using a named value"
weight = 19
description = "Resolve forward references on the collecting pass."
download = "AS19.ASM"
aliases = ["/bootstrap/asm86/20-using-a-named-value/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/19-using-a-named-value/"
+++

The table can now retain an address. I want to put `TEXT` into an operand and let the value reader find it, including when the definition follows the use. I can keep meaningful names in the source instead of copied addresses.

**Starting source:** `AS18.ASM`. **Save as:** `AS19.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

A token beginning with a decimal digit remains a number. Other tokens enter SYMBOLVALUE, which validates the name, rejects register names, and searches the symbol table. A match returns the word at record offset eighteen in AX.

An unknown name returns zero only during pass one. The width of every statement is fixed, so that placeholder changes no positions. On pass two an unknown name is a symbol error, code 3. The output file has not been opened at that point.

VALUE still preserves SI. The symbol path may change the lookup scratch registers, including BX, CX, DX, DI, and BP. A caller must not keep a live loop count in those registers without saving it.

Our test emits a word before the byte it names. TEXT therefore has loaded offset 0102H. A named address is an ordinary unsigned value: DW can hold it, while DB rejects a value above 255. Expressions such as TEXT+1 remain outside the language.

## Source changes

Copy `AS18.ASM` to `AS19.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `NUMBERBAD:`

Find the unique label `NUMBERBAD:`, then follow this unchanged source through its last displayed instruction:

```asm
NUMBERBAD:
MOV AX,2
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JMP ERROR
```

With:

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
JMP ERROR
```

Keep the following `DEFINE:` label and the source after it in place.

### Change 2 · `WORDVALUE:`

Find the unique label `WORDVALUE:`, then follow this unchanged source through its last displayed instruction:

```asm
WORDVALUE:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
CALL REGISTER
CMP AX,0FFFFH
JNE RESERVEDNUM
JMP NUMBERBAD
RESERVEDNUM:
MOV AX,3
JMP ERROR
```

With:

```asm
JMP SYMBOLVALUE
```

Keep the following `LITERAL:` label and the source after it in place.

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS19.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1530 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS19.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T19.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
DW TEXT
TEXT:
DB 65
```

```dos
COPY T19.ASM SOURCE.ASM
```

```dos
CHECK AS19
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00003 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **3 bytes** with these hexadecimal bytes:

```text
02 01 41
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

The bytes `02 01 41` match the earlier BASIC assembler's result. I can follow how the name went through the table lookup to become `0102H`. There is one less part of this program that I have to take on trust.

## A rejection check

Enter this separate file as `X19.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
DW MISSING
```

```dos
COPY X19.ASM SOURCE.ASM
CHECK AS19
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 3
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Keep both the numeric and symbol error exits. VALUE must restore the source cursor after lookup. A forward reference is provisional only on pass one; pass two must find its definition before output is written.
