+++
title = "11 \u00b7 Hexadecimal values"
weight = 11
description = "A final H selects base sixteen; a leading digit keeps names distinct."
download = "AS11.ASM"
+++

We shall extend VALUE to recognize hexadecimal while retaining the same unsigned-word result and overflow checks.

## How it works

The final character is examined before the digit loop. H selects base sixteen and is excluded from the digits to be read. Otherwise BP remains ten. A value must still begin with a decimal digit: write 0FFH, not FFH.

Characters A through F become values ten through fifteen. The digit must be smaller than the selected base, so a letter in a decimal token is rejected. Before a hexadecimal step, CX must be no greater than 4095. Four doublings then multiply it by sixteen, and the checked digit is added.

VALUE's input, result, preserved SI, and scratch registers are unchanged. No BASIC-style prefixes, signed literals, character constants, or expression arithmetic are added. A hexadecimal word is simply another way to write a number from zero through 65535.

## Source changes

Copy `AS10.ASM` to `AS11.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `DECDIGIT:`

Unchanged code immediately before this edit:

```asm
ADD AX,AX
ADD AX,AX
ADD CX,AX
```

Insert after old physical line 290, before the following old line.

Insert this source:

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

### Change 2: following `DIGITOK:`

Unchanged code immediately before this edit:

```asm
MOV DX,AX
CMP DX,BP
JAE NUMBERBAD
```

Insert after old physical line 278, before the following old line.

Insert this source:

```asm
CMP BP,16
JE HEXDIGIT
```

### Change 3: following `DIGIT:`

Unchanged code immediately before this edit:

```asm
LODSB
SUB AL,48
CMP AL,9
```

Insert after old physical line 272, before the following old line.

Insert this source:

```asm
JBE DIGITOK
SUB AL,7
CMP AL,10
JB NUMBERBAD
CMP AL,15
```

### Change 4: following `LITERAL:`

Unchanged code immediately before this edit:

```asm
MOV DI,[TOKLEN]
ADD DI,2300H
MOV BP,10
```

Insert after old physical line 264, before the following old line.

Insert this source:

```asm
CMP AL,72
JNE NUMBERSTART
MOV BP,16
DEC DI
```

### Change 5: following `LITERAL:`

Unchanged code immediately before this edit:

```asm
MOV SI,2300H
MOV DI,[TOKLEN]
ADD DI,2300H
```

Insert after old physical line 263, before the following old line.

Insert this source:

```asm
MOV BX,DI
DEC BX
MOV AL,[BX]
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BOOTASM.BAS
```

Enter `AS11` at its source prompt. Require `OK AS11.COM 875 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T11.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
0FFH
1234H
```

```dos
CHECK AS11
```

Enter `T11` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T11
00255
04660
PASS
```

## A rejection check

Enter this separate file as `X11.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
0GH
```

Run `CHECK AS11` and enter `X11`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 2
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
