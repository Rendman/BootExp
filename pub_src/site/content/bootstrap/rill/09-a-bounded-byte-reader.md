+++
title = "09 \u00b7 A bounded byte reader"
weight = 9
description = "Distinguish source bytes, text termination, and input errors."
download = "R09.IR"
+++

A scanner needs one current byte and a reliable end marker.

## The working parts

NEXT consumes the previous CH and reads at most one byte into INBYTE. It increments LINE when the consumed byte is LF, so CR/LF and LF text have the same line count. READ uses the saved handle, saved buffer pointer, and count one. COUNT holds its actual result while STATUS is checked.

Zero bytes read means end of file. Control-Z also ends source text. The internal end marker is CH zero; a zero byte in the file itself is rejected. Printable ASCII, tab, CR, and LF are admitted. READTOTAL bounds the actual source at 4096 bytes. Invalid source bytes are syntax errors. This driver displays accepted text rather than compiling it.

## Enter the source

Copy `R08.IR` to `R09.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL ERROR`

Unchanged source immediately before the edit:

```ir
CALL NEWLINE
LIT 1
EXIT
```

Insert after old physical line 147, before the following old line.

Insert this source:

```ir
; NEXT
LABEL NEXT
LD CH
PUSH
LIT 10
NE NEXTREAD
LD LINE
PUSH
LIT 1
ADD
ST LINE
LABEL NEXTREAD
LD INPUT
PUSH
ADDR INBYTE
PUSH
LIT 1
READ
ST COUNT
STATUS
JNZ IOFAIL
LD COUNT
JZ ATEND
LD READTOTAL
PUSH
LIT 1
ADD
ST READTOTAL
PUSH
LIT 4096
UGT CAPFAIL
LDB INBYTE
ST CH
PUSH
LIT 26
EQ ATEND
LD CH
PUSH
LIT 127
UGE SYNTAX
LD CH
PUSH
LIT 32
UGE NEXTDONE
LD CH
PUSH
LIT 9
EQ NEXTDONE
LD CH
PUSH
LIT 10
EQ NEXTDONE
LD CH
PUSH
LIT 13
EQ NEXTDONE
JMP SYNTAX
LABEL ATEND
LIT 0
ST CH
LABEL NEXTDONE
RET
```

### Change 2: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
CLOSE
STATUS
JNZ IOFAIL
```

Remove these exact old lines (physical positions 25–28 in `R08.IR`):

```ir
LIT 19279
CALL PAIR
LIT 2573
CALL PAIR
```

No replacement source is needed.

### Change 3: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
ST INPUT
STATUS
JNZ IOFAIL
```

Insert after old physical line 20, before the following old line.

Insert this source:

```ir
CALL NEXT
LABEL DISPLAY
LD CH
JZ DISPLAYDONE
CALL CHAR
CALL NEXT
JMP DISPLAY
LABEL DISPLAYDONE
```

### Change 4: in the declarations

Unchanged source immediately before the edit:

```ir
WORD STEP 0
WORD COUNT 0
WORD INPUT 0
```

Insert after old physical line 10, before the following old line.

Insert this source:

```ir
WORD CH 0
BUFFER INBYTE 1
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R09` at `IR source name:`. Require `OK R09.ASM 06419 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R09` at `Source name:`, and require `OK 01188 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T09.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```text
One
Two
```

Run `COPY T09.RIL SOURCE.RIL`, then `CHECK R09`.

Apart from DOS command echo and the checker's separating blank line, require:

```text
One
Two
PASS
```

This is a diagnostic stopping point. It does not create RESULT.IR.

## A rejection check

Create X09.RIL with COPY CON: press Ctrl-A once, then Ctrl-Z and Enter. VIEW.BAS must show leading byte 01. This deliberately invalid source byte is not a printed RILL token.

Copy X09.RIL to SOURCE.RIL, then run CHECK R09. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

An unexpected PASS is a failed rejection test.

## If the result differs

Check each service STATUS immediately, the current-byte advance, and any shared work cell needed across a call. Compare token values with the printed result before changing the parser.
