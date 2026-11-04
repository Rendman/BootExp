+++
title = "01 \u00b7 Reading an IR source"
weight = 1
description = "Carry the published file reader into a new language workshop."
download = "IR01.ASM"
+++

A translator begins by reading its source reliably. We shall use the file reader already constructed in ASM86, with an IR filename and a diagnostic display.

## Operation and backend

Begin with the saved AS07.ASM program from the ASM86 collection. Its GETNAME, OPENFILE, NEXTBYTE, READLINE, and CLOSEFILE routines provide the complete input path. The source extension is .IR; the DOS output strings still end in a dollar sign, and file extensions end in a zero byte.

READLINE returns AX=1 with uppercase text at 2200H, or AX=0 at end of file. ZTEXT walks a zero-terminated line from SI and changes AX, DX, and SI. The driver resets SI for each line and displays a separate CR/LF. LINENO counts physical lines, including comments and blank lines.

This is a text diagnostic. It performs no language translation and creates no assembly output. The inherited reader admits 120 physical characters per line and rejects an overrun before writing outside its buffer. It retains the full-segment stack check and the DOS failure status.

## Source changes

Copy `AS07.ASM` to `IR01.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `ERRCODE:`

Unchanged code immediately before the edit:

```asm

ERRCODE:
DB 0
```

Insert after old physical line 307, before the following old line.

Insert this source:

```asm

IREXT:
DB 46,73,82,0
```

### Change 2: following `DIVISORS:`

Unchanged code immediately before the edit:

```asm

DIVISORS:
DW 10000,1000,100,10,1
```

Remove these exact old lines (physical positions 282–282 in `AS07.ASM`):

```asm

```

No replacement source is needed.

### Change 3: following `NEWLINE:`

Unchanged code immediately before the edit:

```asm
NEWLINE:
DB 13,10,36

```

Remove these exact old lines (physical positions 277–279 in `AS07.ASM`):

```asm
ASMEXT:
DB 46,65,83,77,0

```

No replacement source is needed.

### Change 4: following `ERRMSG:`

Unchanged code immediately before the edit:

```asm
DB 83,111,117,114,99,101,32,110,97,109,101,58,32,36

ERRMSG:
```

Remove these exact old lines (physical positions 269–269 in `AS07.ASM`):

```asm
DB 69,82,82,79,82,32,36
```

Put this source in their place:

```asm
DB 73,82,32,69,82,82,79,82,32,36
```

### Change 5: following `PROMPT:`

Unchanged code immediately before the edit:

```asm
RET

PROMPT:
```

Remove these exact old lines (physical positions 266–266 in `AS07.ASM`):

```asm
DB 83,111,117,114,99,101,32,110,97,109,101,58,32,36
```

Put this source in their place:

```asm
DB 73,82,32,115,111,117,114,99,101,32,110,97,109,101,58,32
DB 36
```

### Change 6: following `NAMECHAR:`

Unchanged code immediately before the edit:

```asm
DEC CX
JNE NAMELOOP
MOV [EXTP],DI
```

Remove these exact old lines (physical positions 92–92 in `AS07.ASM`):

```asm
MOV SI,ASMEXT
```

Put this source in their place:

```asm
MOV SI,IREXT
```

### Change 7: following `DRIVERDONE:`

Unchanged code immediately before the edit:

```asm
JMP DRIVERLINE
DRIVERDONE:
CALL CLOSEFILE
```

Remove these exact old lines (physical positions 23–23 in `AS07.ASM`):

```asm
GOOD:
```

No replacement source is needed.

### Change 8: following `DRIVERLINE:`

Unchanged code immediately before the edit:

```asm
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
```

Remove these exact old lines (physical positions 16–16 in `AS07.ASM`):

```asm
MOV SI,2200H
```

No replacement source is needed.

### Change 9: at the beginning

Remove these exact old lines (physical positions 1–1 in `AS07.ASM`):

```asm
; ASM86 construction checkpoint. Plain BOOTASM source.
```

Put this source in their place:

```asm
; IR86 construction source. Assemble with ASM86.
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR01` at ASM86's `Source name:` prompt. Require `OK 00605 bytes` followed by PASS. This builds `IR01.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T01.IR` with `COPY CON T01.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
word total 0
label main
halt
```

```dos
CHECK IR01
```

Enter `T01` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T01
WORD TOTAL 0
LABEL MAIN
HALT
PASS
```

This diagnostic creates no assembly file. Its displayed text is the test result.

## A rejection check

Enter this separate input as `X01.IR` using COPY CON and the same end-of-input keystroke:

```ir
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

The unbroken X line has 121 characters, exceeding the 120-character physical input bound.

Run `CHECK IR01` and enter `X01`. Require this diagnostic and FAIL:

```text
IR ERROR 00001 CODE 5
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the .IR extension bytes, zero and dollar-sign terminators, and source-cursor saves. A file error is different from end of file; NEXTBYTE returns an explicit count.
