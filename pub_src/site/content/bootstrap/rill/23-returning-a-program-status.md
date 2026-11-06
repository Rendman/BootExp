+++
title = "23 \u00b7 Returning a program status"
weight = 23
description = "Compile an explicit termination statement."
download = "R23.IR"
download_group = "tools/rill0"
reader_names = 1
+++

A program needs to report failure and to stop before the normal end of its body.

## The working parts

EXITSTAT validates exit(expression); using the same parentheses and semicolon rules as byte output. Its emitted EXIT terminates with the expression value modulo 256. The driver still appends HALT for a path that reaches the end normally.

Unreachable source is still parsed and checked. exit is a statement, not an expression, and it does not return to a caller. A deliberately nonzero status must be observed immediately by CHECK and reported as FAIL.

## Enter the source

Copy `R22.IR` to `R23.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL PUTSTAT`

Unchanged source immediately before the edit:

```ir
LIT 21840
CALL PAIR
LIT 17236
```

Insert after old physical line 930, before the following old line.

Insert this source:

```ir
CALL PAIR
LIT 2573
CALL PAIR
RET
LABEL EXITSTAT
LIT 20
CALL ENDTOKEN
LIT 40
CALL EXPECT
CALL EXPR
LIT 41
CALL EXPECT
LIT 59
CALL EXPECT
LIT 22597
CALL PAIR
LIT 21577
```

### Change 2: following `LABEL STATEMENT`

Unchanged source immediately before the edit:

```ir
PUSH
LIT 49844
EQ PUTSTAT
```

Insert after old physical line 901, before the following old line.

Insert this source:

```ir
LD TOK
PUSH
LIT 38665
EQ EXITSTAT
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R23` at `IR source name:`. Require `OK R23.ASM 21563 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R23` at `Source name:`, and require `OK 04603 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T23.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){exit(1);}
```

Run `COPY T23.RIL SOURCE.RIL`, then `CHECK R23`.

Require:

```text
OK RESULT.IR 00035
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
LIT 00001
EXIT
HALT
```

Copy RESULT.IR to T23.IR. Translate it with CHECK IRKEEP, entering T23; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00475 bytes` and PASS.

VIEW.BAS must report T23.COM length **475 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T23`. It deliberately returns status 1; the checker must report FAIL. This is the intended executable result.

## A rejection check

Create X23.RIL with this separate test:

```rill
fn main(){exit(0) }
```

Copy X23.RIL to SOURCE.RIL, then run CHECK R23. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.
