+++
title = "08 \u00b7 Opening and closing the source"
weight = 8
description = "Check the file lifetime before interpreting its contents."
download = "R08.IR"
+++

An empty readable file is different from a file that could not be opened.

## The working parts

OPEN receives ADDR NAMEBUF and returns an opaque handle saved in INPUT. STATUS is checked before the handle is used. CLOSE consumes that token and its status is checked independently.

This diagnostic does not read or parse the source. Even an empty SOURCE.RIL is sufficient. A missing source must report category one and FAIL. The input token is never treated as a DOS descriptor or used in arithmetic.

## Enter the source

Copy `R07.IR` to `R08.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
LABEL MAIN
CALL SOURCENAME
ADDR NAMEBUF
```

Remove these exact old lines (physical positions 17–30 in `R07.IR`):

```ir
ST TOKENVAL
LABEL NAMEDISPLAY
LD TOKENVAL
FETCHB
JZ NAMEDONE
CALL CHAR
LD TOKENVAL
PUSH
LIT 1
ADD
ST TOKENVAL
JMP NAMEDISPLAY
LABEL NAMEDONE
CALL NEWLINE
```

Put this source in their place:

```ir
OPEN
ST INPUT
STATUS
JNZ IOFAIL
LD INPUT
CLOSE
STATUS
JNZ IOFAIL
LIT 19279
CALL PAIR
LIT 2573
CALL PAIR
```

### Change 2: in the declarations

Unchanged source immediately before the edit:

```ir
WORD PLACE 0
WORD STEP 0
WORD COUNT 0
```

Remove these exact old lines (physical positions 10–10 in `R07.IR`):

```ir
WORD TOKENVAL 0
```

Put this source in their place:

```ir
WORD INPUT 0
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R08` at `IR source name:`. Require `OK R08.ASM 05104 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R08` at `Source name:`, and require `OK 00954 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create an empty `T08.RIL` using `COPY CON T08.RIL` and Ctrl-Z then Enter. VIEW.BAS must report length zero.

Run `COPY T08.RIL SOURCE.RIL`, then `CHECK R08`.

Apart from DOS command echo and the checker's separating blank line, require:

```text
OK
PASS
```

This is a diagnostic stopping point. It does not create RESULT.IR.

## A rejection check

Rename SOURCE.RIL to HOLD.RIL, run CHECK R08, and require:

```text
ERROR 00001 CODE 00001
FAIL
```

Restore HOLD.RIL to SOURCE.RIL afterward. A missing source is not successful empty input.

An unexpected PASS is a failed rejection test.

## If the result differs

Check each service STATUS immediately, the current-byte advance, and any shared work cell needed across a call. Compare token values with the printed result before changing the parser.
