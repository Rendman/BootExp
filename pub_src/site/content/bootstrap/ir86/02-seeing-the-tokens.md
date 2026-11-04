+++
title = "02 \u00b7 Seeing the tokens"
weight = 2
description = "Separate words and punctuation without losing the line cursor."
download = "IR02.ASM"
+++

A physical line is not yet an instruction. The scanner can show exactly which tokens a parser receives.

## How it works

SCAN is the published ASM86 scanner. SI is its source cursor; the result is a zero-terminated token at 2300H and a word length in TOKLEN. AX and DI are scratch registers. Spaces are skipped, comma and brackets are individual tokens, and semicolon ends the statement.

The driver saves SI while ZTEXT displays the token, then restores it before calling SCAN again. The bracket characters on the display are diagnostic decoration, not source syntax. An empty token ends the current statement.

The token bound is sixteen characters plus its zero terminator. This bound is independent of the physical-line bound. No quoted-string rule is added. A long unbroken word is rejected even when the entire physical line fits.

## Source changes

Copy `IR01.ASM` to `IR02.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `LINENO:`

Unchanged code immediately before the edit:

```asm
LINENO:
DW 0

```

Insert after old physical line 291, before the following old line.

Insert this source:

```asm
TOKLEN:
DW 0

```

### Change 2: following `READFAIL:`

Unchanged code immediately before the edit:

```asm
MOV [LINENO],DX
JMP ERROR

```

Insert after old physical line 189, before the following old line.

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

Unchanged code immediately before the edit:

```asm
CALL ZTEXT
MOV DX,NEWLINE
CALL TEXT
```

Remove these exact old lines (physical positions 19–19 in `IR01.ASM`):

```asm
JMP DRIVERLINE
```

Put this source in their place:

```asm
JMP TRACETOKEN
```

### Change 4: following `DRIVERLINE:`

Unchanged code immediately before the edit:

```asm
JE DRIVERDONE
MOV SI,2200H
CALL ZTEXT
```

Insert after old physical line 16, before the following old line.

Insert this source:

```asm
POP SI
MOV DL,93
MOV AH,2
INT 21H
```

### Change 5: following `DRIVERLINE:`

Unchanged code immediately before the edit:

```asm
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
```

Insert after old physical line 15, before the following old line.

Insert this source:

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

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR02` at ASM86's `Source name:` prompt. Require `OK 00747 bytes` followed by PASS. This builds `IR02.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T02.IR` with `COPY CON T02.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
lit 1 ; note
```

```dos
CHECK IR02
```

Enter `T02` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T02
[LIT]
[1]
PASS
```

This diagnostic creates no assembly file. Its displayed text is the test result.

## A rejection check

Enter this separate input as `X02.IR` using COPY CON and the same end-of-input keystroke:

```ir
ABCDEFGHIJKLMNOPQ
```

Run `CHECK IR02` and enter `X02`. Require this diagnostic and FAIL:

```text
IR ERROR 00001 CODE 1
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the .IR extension bytes, zero and dollar-sign terminators, and source-cursor saves. A file error is different from end of file; NEXTBYTE returns an explicit count.
