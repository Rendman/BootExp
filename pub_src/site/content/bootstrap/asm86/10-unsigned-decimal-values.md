+++
title = "10 \u00b7 Unsigned decimal values"
weight = 10
description = "Check every digit before multiplying the accumulated value."
download = "AS10.ASM"
download_group = "tools/asm0"
reader_names = 1
+++

A token of decimal digits must become a word without accepting a sign, an expression, or an overflow.

## How it works

VALUE takes the token at 2300H and returns its unsigned value in AX. It preserves the source cursor SI by saving it on the stack. The numeric work uses CX as the accumulated value, DX as the next digit, and DI as the end of the token. AX, BX, CX, DX, DI, BP, and flags are scratch state.

Each character must lie between the codes for 0 and 9. Before multiplying, the accumulated value must be below 6553, or exactly 6553 with a final digit no greater than five. That check admits 65535 and rejects the next value before arithmetic can wrap.

Multiplication by ten is eight times the old value plus twice the old value. ADD performs those doublings with instructions BOOTASM already accepts. This keeps the routine's implementation vocabulary small; it does not imply the CPU lacks a multiply instruction.

The diagnostic driver reads one number per line. It saves AX while FINISH checks that no extra token follows, then prints the result. Empty values, malformed digits, and overflow select code 2. Only decimal numbers are accepted by this checkpoint.

## Source changes

Copy `AS09.ASM` to `AS10.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `ERRCODE:`

Unchanged code immediately before this edit:

```asm

ERRCODE:
DB 0
```

Remove these exact old lines (physical lines 416–419 of `AS09.ASM`):

```asm

OPTAB:
DB 68,66,0,0,0,0,1,0
DB 68,87,0,0,0,0,1,1
```

No replacement lines are needed.

### Change 2: following `TOKLEN:`

Unchanged code immediately before this edit:

```asm
TOKLEN:
DW 0

```

Remove these exact old lines (physical lines 402–404 of `AS09.ASM`):

```asm
STRIDE:
DW 0

```

No replacement lines are needed.

### Change 3: following `LOOKFOUND:`

Unchanged code immediately before this edit:

```asm
MOV BX,BP
POP SI
RET
```

Remove these exact old lines (physical lines 290–293 of `AS09.ASM`):

```asm
LOOKMISS:
MOV BX,0
POP SI
RET
```

Put this source in their place:

```asm
NUMBERBAD:
MOV AX,2
JMP ERROR
```

### Change 4: following `LOOKCHAR:`

Unchanged code immediately before this edit:

```asm
MOV SI,2300H
LOOKCHAR:
LODSB
```

Remove these exact old lines (physical lines 273–287 of `AS09.ASM`):

```asm
MOV BX,DI
MOV DL,[BX]
CMP AL,DL
JNE LOOKSTEP
CMP AL,0
JE LOOKFOUND
INC DI
JMP LOOKCHAR
LOOKSTEP:
MOV AX,[STRIDE]
ADD BP,AX
DEC CX
JMP LOOKNEXT
LOOKFOUND:
MOV BX,BP
```

Put this source in their place:

```asm
SUB AL,48
CMP AL,9
JA NUMBERBAD
DIGITOK:
MOV AH,0
MOV DX,AX
CMP DX,BP
JAE NUMBERBAD
CMP CX,6553
JA NUMBERBAD
JB DECDIGIT
CMP DX,5
JA NUMBERBAD
DECDIGIT:
MOV AX,CX
ADD CX,CX
ADD AX,AX
ADD AX,AX
ADD AX,AX
ADD CX,AX
ADDDIGIT:
ADD CX,DX
CMP SI,DI
JB DIGIT
MOV AX,CX
```

### Change 5: following `LOOKNEXT:`

Unchanged code immediately before this edit:

```asm
JE LOOKMISS
MOV DI,BP
MOV SI,2300H
```

Remove these exact old lines (physical lines 271–271 of `AS09.ASM`):

```asm
LOOKCHAR:
```

Put this source in their place:

```asm
MOV DI,[TOKLEN]
ADD DI,2300H
MOV BP,10
NUMBERSTART:
CMP SI,DI
JE NUMBERBAD
MOV CX,0
DIGIT:
```

### Change 6: following `LOOK:`

Unchanged code immediately before this edit:

```asm
LOOK:
MOV [STRIDE],AX
PUSH SI
```

Remove these exact old lines (physical lines 265–269 of `AS09.ASM`):

```asm
MOV BP,BX
LOOKNEXT:
CMP CX,0
JE LOOKMISS
MOV DI,BP
```

No replacement lines are needed.

### Change 7: following `TOKENBAD:`

Unchanged code immediately before this edit:

```asm
MOV AX,1
JMP ERROR

```

Remove these exact old lines (physical lines 262–263 of `AS09.ASM`):

```asm
LOOK:
MOV [STRIDE],AX
```

Put this source in their place:

```asm
VALUE:
MOV AL,[2300H]
CMP AL,48
JB WORDVALUE
CMP AL,57
JBE LITERAL
WORDVALUE:
JMP NUMBERBAD
LITERAL:
```

### Change 8: following `DRIVERLINE:`

Unchanged code immediately before this edit:

```asm
JE DRIVERDONE
MOV SI,2200H
CALL SCAN
```

Remove these exact old lines (physical lines 17–28 of `AS09.ASM`):

```asm
MOV BX,OPTAB
MOV CX,2
MOV AX,8
CALL LOOK
CMP BX,0
JNE TRACEFOUND
MOV AX,1
JMP ERROR
TRACEFOUND:
ADD BX,7
MOV AL,[BX]
MOV AH,0
```

Put this source in their place:

```asm
CALL VALUE
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BOOTASM.BAS
```

Enter `AS10` at its source prompt. Require `OK AS10.COM 825 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T10.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
42
65535
```

```dos
CHECK AS10
```

Enter `T10` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T10
00042
65535
PASS
```

## A rejection check

Enter this separate file as `X10.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
65536
```

Run `CHECK AS10` and enter `X10`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 2
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
