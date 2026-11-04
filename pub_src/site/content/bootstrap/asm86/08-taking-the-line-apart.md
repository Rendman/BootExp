+++
title = "08 \u00b7 Taking the line apart"
weight = 8
description = "Words and punctuation become bounded tokens."
download = "AS08.ASM"
+++

We shall give the parser one word or punctuation mark at a time, while retaining a cursor into the current line.

## How it works

SCAN takes SI as the current position in the zero-terminated line. It skips spaces and returns one token at 2300H, a zero byte after it, and its length in TOKLEN. SI remains at the next separator or at the end marker. A zero token length means end of statement. The routine changes AX and DI as well as SI and TOKLEN.

Comma, colon, and square brackets are single-character tokens. A punctuation mark encountered after a word is put back by decrementing SI so the next call can return it separately. A semicolon means the rest of the line is a comment. Neither a zero byte nor a semicolon is consumed past the statement's end, so another call still sees an empty token.

A token may contain at most sixteen characters. The bound is checked before storing another character; its terminating zero occupies the seventeenth byte. This limit is independent of the 120-character physical-line limit. Quoted strings are not recognized.

The driver displays each token between brackets. It saves SI while ZTEXT walks the token buffer, then restores the line cursor. Without that saved cursor, the next SCAN would continue inside the token instead of the source line. This test separates token boundaries from their eventual meaning.

## Source changes

Copy `AS07.ASM` to `AS08.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `LINENO:`

Unchanged code immediately before this edit:

```asm
LINENO:
DW 0

```

Insert after old physical line 296, before the following old line.

Insert this source:

```asm
TOKLEN:
DW 0

```

### Change 2: following `READFAIL:`

Unchanged code immediately before this edit:

```asm
MOV [LINENO],DX
JMP ERROR

```

Insert after old physical line 191, before the following old line.

Insert this source:

```asm
SCAN:
MOV DI,2300H
SCANSPACE:
LODSB
CMP AL,32
JE SCANSPACE
CMP AL,0
JE SCANEND
CMP AL,59
JE SCANEND
STOSB
CMP AL,44
JE SCANDONE
CMP AL,58
JE SCANDONE
CMP AL,91
JE SCANDONE
CMP AL,93
JE SCANDONE
SCANMORE:
LODSB
CMP AL,0
JE SCANBACK
CMP AL,32
JE SCANBACK
CMP AL,59
JE SCANBACK
CMP AL,44
JE SCANBACK
CMP AL,58
JE SCANBACK
CMP AL,91
JE SCANBACK
CMP AL,93
JE SCANBACK
CMP DI,2310H
JAE TOKENBAD
STOSB
JMP SCANMORE
SCANBACK:
DEC SI
SCANDONE:
MOV AX,DI
SUB AX,2300H
MOV [TOKLEN],AX
MOV AL,0
STOSB
RET
SCANEND:
DEC SI
JMP SCANDONE
TOKENBAD:
MOV AX,1
JMP ERROR

```

### Change 3: following `DRIVERLINE:`

Unchanged code immediately before this edit:

```asm
CALL ZTEXT
MOV DX,NEWLINE
CALL TEXT
```

Remove these exact old lines (physical lines 20–20 of `AS07.ASM`):

```asm
JMP DRIVERLINE
```

Put this source in their place:

```asm
JMP TRACETOKEN
```

### Change 4: following `DRIVERLINE:`

Unchanged code immediately before this edit:

```asm
MOV SI,2200H
MOV SI,2200H
CALL ZTEXT
```

Insert after old physical line 17, before the following old line.

Insert this source:

```asm
POP SI
MOV DL,93
MOV AH,2
INT 21H
```

### Change 5: following `DRIVERLINE:`

Unchanged code immediately before this edit:

```asm
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
```

Remove these exact old lines (physical lines 16–16 of `AS07.ASM`):

```asm
MOV SI,2200H
```

Put this source in their place:

```asm
TRACETOKEN:
CALL SCAN
MOV AL,[2300H]
CMP AL,0
JE DRIVERLINE
MOV DL,91
MOV AH,2
INT 21H
PUSH SI
MOV SI,2300H
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BAWIDE.BAS
```

Enter `AS08` at its source prompt. Require `OK AS08.COM 742 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T08.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
db 1,2 ; a note
```

```dos
CHECK AS08
```

Enter `T08` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T08
[DB]
[1]
[,]
[2]
PASS
```

## A rejection check

Enter this separate file as `X08.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
ABCDEFGHIJKLMNOPQ
```

Run `CHECK AS08` and enter `X08`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 1
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
