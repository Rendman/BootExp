+++
title = "02 \u00b7 Numbers in the report"
weight = 2
description = "Display an unsigned word without a divide instruction."
download = "AS02.ASM"
download_group = "tools/asm0"
reader_names = 1
+++

An assembly-language tool needs to report counts. We shall print an unsigned word as five decimal digits using repeated subtraction.

## How it works

NUMBER takes its value in AX and preserves every word register. The five PUSH instructions save AX, BX, CX, DX, and SI; the POP instructions restore them in reverse order. DI and BP are not touched. The routine uses ten stack bytes for its saved registers, in addition to its return address.

CX holds the amount still to be displayed. SI points at a table of word divisors: 10000, 1000, 100, 10, and 1. BX copies that pointer because our assembler accepts a word load through BX. For each divisor, AL begins with the code for 0. Repeated subtraction advances the digit until CX is smaller than the divisor.

Function 02H displays the character in DL. The arithmetic remainder stays in CX, because DOS may change AL. All five places are printed, including leading zeroes; this makes the routine small and keeps zero unambiguous. The tests show the low bound, a middle value, and the largest unsigned word. DIVEND names the byte just after the divisor table and emits no data.

## Source changes

Copy `AS01.ASM` to `AS02.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `TEXT:`

Unchanged code immediately before this edit:

```asm
INT 21H
RET

```

Remove these exact old lines (physical lines 15–16 of `AS01.ASM`):

```asm
HELLOMSG:
DB 65,83,77,48,13,10,36
```

Put this source in their place:

```asm
NUMBER:
PUSH AX
PUSH BX
PUSH CX
PUSH DX
PUSH SI
MOV CX,AX
MOV SI,DIVISORS
NEXTPLACE:
MOV BX,SI
MOV DX,[BX]
MOV AL,48
SUBTRACT:
CMP CX,DX
JB PRINTDIGIT
SUB CX,DX
ADD AL,1
JMP SUBTRACT
PRINTDIGIT:
MOV DL,AL
MOV AH,2
INT 21H
ADD SI,2
CMP SI,DIVEND
JB NEXTPLACE
POP SI
POP DX
POP CX
POP BX
POP AX
RET

NEWLINE:
DB 13,10,36

DIVISORS:
DW 10000,1000,100,10,1

DIVEND:
```

### Change 2: following `START:`

Unchanged code immediately before this edit:

```asm
; ASM86 construction checkpoint. Plain BOOTASM source.
START:
CLD
```

Remove these exact old lines (physical lines 4–4 of `AS01.ASM`):

```asm
MOV DX,HELLOMSG
```

Put this source in their place:

```asm
MOV AX,0
CALL NUMBER
MOV DX,NEWLINE
CALL TEXT
MOV AX,1000
CALL NUMBER
MOV DX,NEWLINE
CALL TEXT
MOV AX,65535
CALL NUMBER
MOV DX,NEWLINE
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS02.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 110 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS02.COM`. Save this source and executable as a working stopping point.

```dos
CHECK AS02
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
00000
01000
65535
PASS
```

## If the result differs

Check the decimal character bytes, the dollar-sign terminators, and the order of saved registers. A RET must match a CALL; the top-level exit uses DOS function 4CH.
