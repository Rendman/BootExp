+++
title = "10 \u00b7 Loading and storing a word"
weight = 10
description = "Move between AX and a named word without changing its address."
download = "IR10.ASM"
+++

A declaration becomes useful when the program can read it and replace its value.

## How it works

LD name emits MOV AX,[U_name]. ST name emits MOV [U_name],AX and retains the accumulator. Both transfer a word at DS:offset; a word occupies two consecutive bytes. The name operand is checked by NAMEARG and resolved by ASM86.

These templates use direct memory operands, so BX is not required to hold the address. They do not imply that the translator tracks a declaration's type. The programmer must pair a word access with storage large enough for a word.

The test stores zero into a word initialized to seven, then loads it after replacing AX with 99. EXIT must receive zero. This distinguishes a working load from an unchanged accumulator and a working store from the original initializer.

## Source changes

Copy `IR09.ASM` to `IR10.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_WORD:`

Unchanged code immediately before the edit:

```asm

T_WORD:
DB 85,95,64,58,13,10,68,87,32,35,13,10,0
```

Insert after old physical line 835, before the following old line.

Insert this source:

```asm

T_LD:
DB 77,79,86,32,65,88,44,91,85,95,64,93,13,10,0

T_ST:
DB 77,79,86,32,91,85,95,64,93,44,65,88,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_EXIT
DB 87,79,82,68,0,0,0,0,5,0,2,0
DW T_WORD
```

Insert after old physical line 722, before the following old line.

Insert this source:

```asm
DB 76,68,0,0,0,0,0,0,2,0,4,0
DW T_LD
DB 83,84,0,0,0,0,0,0,2,0,4,0
DW T_ST
```

### Change 3: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 484–484 in `IR09.ASM`):

```asm
MOV CX,6
```

Put this source in their place:

```asm
MOV CX,8
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR10` at ASM86's `Source name:` prompt. Require `OK 01884 bytes` followed by PASS. This builds `IR10.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T10.IR` with `COPY CON T10.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
WORD TOTAL 7
LABEL MAIN
LIT 0
ST TOTAL
LIT 99
LD TOTAL
EXIT
```

```dos
CHECK IR10
```

Enter `T10` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T10
OK T10.ASM 00180 text bytes
PASS
```

Run `TYPE T10.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_TOTAL:
DW 7
U_MAIN:
MOV AX,0
MOV [U_TOTAL],AX
MOV AX,99
MOV AX,[U_TOTAL]
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T10`. Require `OK 00035 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T10.COM`, and require length **35 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 02 00 07
00 B8 00 00 89 06 0F 01 B8 63 00 8B 06 0F 01 B4
4C CD 21
```

`T10.COM` is a complete program. Run `CHECK T10`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X10.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
LD 12
```

Run `CHECK IR10` and enter `X10`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 3
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the record stride and count, the saved template pointer, and each substitution buffer. The name and numeric token must survive FINISH. Compare the generated assembly before asking ASM86 to assemble it.
