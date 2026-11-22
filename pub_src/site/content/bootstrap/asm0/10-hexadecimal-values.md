+++
title = "10 \u00b7 Hexadecimal values"
weight = 10
description = "A final H selects base sixteen; a leading digit keeps names distinct."
download = "AS10.ASM"
aliases = ["/bootstrap/asm86/11-hexadecimal-values/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/10-hexadecimal-values/"
+++

We shall extend VALUE to recognize hexadecimal while retaining the same unsigned-word result and overflow checks.

**Starting source:** `AS09.ASM`. **Save as:** `AS10.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

The final character is examined before the digit loop. H selects base sixteen and is excluded from the digits to be read. Otherwise BP remains ten. A value must still begin with a decimal digit: write 0FFH, not FFH.

Characters A through F become values ten through fifteen. The digit must be smaller than the selected base, so a letter in a decimal token is rejected. Before a hexadecimal step, CX must be no greater than 4095. Four doublings then multiply it by sixteen, and the checked digit is added.

VALUE's input, result, preserved SI, and scratch registers are unchanged. No BASIC-style prefixes, signed literals, character constants, or expression arithmetic are added. A hexadecimal word is simply another way to write a number from zero through 65535.

## Source changes

Copy `AS09.ASM` to `AS10.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `ADDDIGIT:`

Find the unique label `ADDDIGIT:`. Insert the new source immediately before this existing label:

```asm
ADDDIGIT:
```

Insert:

```asm
JMP ADDDIGIT
HEXDIGIT:
CMP CX,4095
JA NUMBERBAD
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADD CX,CX
```

### Change 2 · `DIGITOK:`

Find the unique label `DIGITOK:`, then follow this unchanged source through its last displayed instruction:

```asm
DIGITOK:
MOV AH,0
MOV DX,AX
CMP DX,BP
JAE NUMBERBAD
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CMP BP,16
JE HEXDIGIT
```

### Change 3 · `NUMBERSTART:`

Find the unique label `NUMBERSTART:`, then follow this unchanged source through its last displayed instruction:

```asm
NUMBERSTART:
CMP SI,DI
JE NUMBERBAD
MOV CX,0
DIGIT:
LODSB
SUB AL,48
CMP AL,9
```

The edit begins immediately after that unchanged block.

Insert:

```asm
JBE DIGITOK
SUB AL,7
CMP AL,10
JB NUMBERBAD
CMP AL,15
```

### Change 4 · `NUMBERSTART:`

Find the unique label `NUMBERSTART:`. Insert the new source immediately before this existing label:

```asm
NUMBERSTART:
```

Insert:

```asm
CMP AL,72
JNE NUMBERSTART
MOV BP,16
DEC DI
```

### Change 5 · `LITERAL:`

Find the unique label `LITERAL:`, then follow this unchanged source through its last displayed instruction:

```asm
LITERAL:
PUSH SI
MOV SI,2300H
MOV DI,[TOKLEN]
ADD DI,2300H
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV BX,DI
DEC BX
MOV AL,[BX]
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS10.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 728 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS10.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T10.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
0FFH
1234H
```

```dos
COPY T10.ASM SOURCE.ASM
```

```dos
CHECK AS10
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
00255
04660
PASS
```

## A rejection check

Enter this separate file as `X10.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
0GH
```

```dos
COPY X10.ASM SOURCE.ASM
CHECK AS10
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 2
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check that the trailing H is excluded from the digit loop and that a hexadecimal token begins with a decimal digit. Decimal and hexadecimal overflow use different pre-multiplication bounds.
