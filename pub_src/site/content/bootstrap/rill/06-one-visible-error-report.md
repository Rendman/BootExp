+++
title = "06 \u00b7 One visible error report"
weight = 6
description = "Give failures a location, a category, and a nonzero status."
download = "R06.IR"
+++

A checker can report FAIL, but the compiler should also say where it stopped.

## The working parts

ERROR takes an error category in A, stores it in READTOTAL, selects console output with DEST zero, and prints LINE and the category. It terminates with status one. The entry labels IOFAIL, SYNTAX, NUMFAIL, NAMEFAIL, and CAPFAIL supply categories one through five.

READTOTAL can hold the category because an error never resumes input. The line begins at one. This diagnostic uses redirected input containing A for success and B for the deliberate syntax failure. These are test bytes, not RILL programs. A failure of CHAR itself still exits immediately with status four.

## Enter the source

Copy `R05.IR` to `R06.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL NUMDONE`

Unchanged source immediately before the edit:

```ir
JMP NUMPRINT
LABEL NUMDONE
RET
```

Insert after old physical line 91, before the following old line.

Insert this source:

```ir
; ERROR
LABEL IOFAIL
LIT 1
JMP ERROR
LABEL SYNTAX
LIT 2
JMP ERROR
LABEL NUMFAIL
LIT 3
JMP ERROR
LABEL NAMEFAIL
LIT 4
JMP ERROR
LABEL CAPFAIL
LIT 5
JMP ERROR
LABEL ERROR
ST READTOTAL
LIT 0
ST DEST
LIT 21061
CALL PAIR
LIT 20306
CALL PAIR
LIT 8274
CALL PAIR
LD LINE
CALL NUMBER
LIT 17184
CALL PAIR
LIT 17487
CALL PAIR
LIT 8261
CALL PAIR
LD READTOTAL
CALL NUMBER
CALL NEWLINE
LIT 1
EXIT
```

### Change 2: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
WORD COUNT 0
; Driver
LABEL MAIN
```

Remove these exact old lines (physical positions 9–11 in `R05.IR`):

```ir
LIT 65535
CALL NUMBER
CALL NEWLINE
```

Put this source in their place:

```ir
GETC
PUSH
LIT 65
NE SYNTAX
LIT 19279
CALL PAIR
LIT 2573
CALL PAIR
```

### Change 3: in the declarations

Unchanged source immediately before the edit:

```ir
; DATA
```

Insert after old physical line 1, before the following old line.

Insert this source:

```ir
WORD LINE 1
WORD READTOTAL 0
WORD DEST 0
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R06` at `IR source name:`. Require `OK R06.ASM 04496 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R06` at `Source name:`, and require `OK 00833 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T06.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```text
A
```

Run `CHECK R06 <T06.RIL`. This is diagnostic byte input, not a RILL program.

Apart from DOS command echo and the checker's separating blank line, require:

```text
OK
PASS
```

This is a diagnostic stopping point. It does not create RESULT.IR.

## A rejection check

Create X06.RIL with this separate test:

```text
B
```

Run `CHECK R06 <X06.RIL`. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

An unexpected PASS is a failed rejection test.

## If the result differs

Check each service STATUS immediately, the current-byte advance, and any shared work cell needed across a call. Compare token values with the printed result before changing the parser.
