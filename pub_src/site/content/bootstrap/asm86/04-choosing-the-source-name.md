+++
title = "04 \u00b7 Choosing the source name"
weight = 4
description = "Read, check, and uppercase a short DOS base name."
download = "AS04.ASM"
+++

We shall ask for a source name once and construct its .ASM filename in a bounded buffer.

## How it works

GETNAME takes no arguments. It displays PROMPT, reads a console line, validates the base name, copies it to FNAME, and appends .ASM plus a zero byte. It changes AX, BX, CX, DX, SI, DI, and the flags. EXTP retains the position at which the extension begins.

DOS function 0AH expects a buffer whose first byte is its maximum size. We place that buffer at 2400H. DOS stores the actual character count at 2401H and the text at 2402H. A maximum of ten allows nine typed characters plus a carriage return; we reject counts above eight instead of quietly accepting a truncated eight-character name.

DOS echoes the entered carriage return without a line feed, so the explicit TEXT call displays NEWLINE before any report. The copy loop permits letters, digits, and underscores. ASCII lowercase letters are converted by subtracting 32. LODSB reads DS:SI and advances SI; STOSB writes ES:DI and advances DI. CLD at entry makes both advance. The DOS .COM entry convention gives DS and ES the same segment, which the program retains.

COPYZ copies a zero-terminated string from SI to DI, including its final zero. The extension strings use zero terminators because DOS file services require them. TEXT's display strings still use dollar signs; they are different interfaces.

The small diagnostic printer ZTEXT displays a zero-terminated string from SI with function 02H. It advances SI and changes AX and DX. The visible filename proves that the copy and extension are in the right places. Use ordinary disk filenames, never DOS device names such as CON or NUL.

## Source changes

Copy `AS03.ASM` to `AS04.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `ERRCODE:`

Unchanged code immediately before this edit:

```asm

ERRCODE:
DB 0
```

Remove these exact old lines (physical lines 89–91 of `AS03.ASM`):

```asm

READYMSG:
DB 82,69,65,68,89,13,10,36
```

No replacement lines are needed.

### Change 2: following `DIVEND:`

Unchanged code immediately before this edit:

```asm
DW 10000,1000,100,10,1

DIVEND:
```

Insert after old physical line 82, before the following old line.

Insert this source:

```asm

FNAME:
DB 0,0,0,0,0,0,0,0,0,0,0,0,0

EXTP:
DW 0
```

### Change 3: following `NEWLINE:`

Unchanged code immediately before this edit:

```asm
NEWLINE:
DB 13,10,36

```

Insert after old physical line 78, before the following old line.

Insert this source:

```asm
ASMEXT:
DB 46,65,83,77,0

```

### Change 4: following `ERROR:`

Unchanged code immediately before this edit:

```asm
MOV AX,4C01H
INT 21H

```

Insert after old physical line 69, before the following old line.

Insert this source:

```asm
ZTEXT:
LODSB
CMP AL,0
JE ZDONE
MOV DL,AL
MOV AH,2
INT 21H
JMP ZTEXT
ZDONE:
RET

PROMPT:
DB 83,111,117,114,99,101,32,110,97,109,101,58,32,36

```

### Change 5: following `GOOD:`

Unchanged code immediately before this edit:

```asm
GOOD:
MOV AX,4C00H
INT 21H
```

Insert after old physical line 13, before the following old line.

Insert this source:

```asm

GETNAME:
MOV DX,PROMPT
CALL TEXT
MOV BX,2400H
MOV AL,10
MOV [BX],AL
MOV DX,2400H
MOV AH,10
INT 21H
MOV DX,NEWLINE
CALL TEXT
MOV BX,2401H
MOV AL,[BX]
MOV AH,0
CMP AX,1
JB BADNAME
CMP AX,8
JA BADNAME
MOV CX,AX
MOV SI,2402H
MOV DI,FNAME
NAMELOOP:
LODSB
CMP AL,97
JB NAMEUP
CMP AL,122
JA NAMEUP
SUB AL,32
NAMEUP:
CMP AL,95
JE NAMECHAR
CMP AL,48
JB BADNAME
CMP AL,57
JBE NAMECHAR
CMP AL,65
JB BADNAME
CMP AL,90
JA BADNAME
NAMECHAR:
STOSB
DEC CX
JNE NAMELOOP
MOV [EXTP],DI
MOV SI,ASMEXT
CALL COPYZ
RET
BADNAME:
MOV AX,1
JMP ERROR

COPYZ:
LODSB
STOSB
CMP AL,0
JNE COPYZ
RET
```

### Change 6: following `ROOM:`

Unchanged code immediately before this edit:

```asm
MOV AX,7
JMP ERROR
ROOM:
```

Remove these exact old lines (physical lines 9–9 of `AS03.ASM`):

```asm
MOV DX,READYMSG
```

Put this source in their place:

```asm
CALL GETNAME
MOV SI,FNAME
CALL ZTEXT
MOV DX,NEWLINE
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BOOTASM.BAS
```

Enter `AS04` at its source prompt. Require `OK AS04.COM 336 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T04.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
; A filename test.
```

```dos
CHECK AS04
```

Enter `T04` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T04
T04.ASM
PASS
```

## A rejection check

Run `CHECK AS04` and enter `BAD.NAME` as the base name. The dot is forbidden.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00000 CODE 1
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
