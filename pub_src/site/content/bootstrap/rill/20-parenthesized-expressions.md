+++
title = "20 \u00b7 Parenthesized expressions"
weight = 20
description = "Use recursive parsing with an explicit depth bound."
download = "R20.IR"
+++

Parentheses let the programmer choose a grouping different from left-to-right evaluation.

## The working parts

A parenthesized FACTOR consumes (, calls EXPR, and requires ). FACTOR returns only after its DEPTH contribution is removed. BODY and FACTOR share the same depth count, so the eight active levels include the main body and current primary expression.

The caller has already saved any pending operator or assignment name in FRAMES. Recursive EXPR calls can change token and formatting work cells without losing that saved state. The test distinguishes 1+(2+3) from a missing or misplaced closing delimiter.

## Enter the source

Copy `R19.IR` to `R20.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL FACTORNUM`

Unchanged source immediately before the edit:

```ir
CALL NUMBER
CALL NEWLINE
CALL LEX
```

Insert after old physical line 777, before the following old line.

Insert this source:

```ir
JMP FACTORDONE
LABEL FACTORPAREN
CALL LEX
CALL EXPR
LIT 41
CALL EXPECT
```

### Change 2: following `LABEL FACTOR`

Unchanged source immediately before the edit:

```ir
PUSH
LIT 65535
EQ FACTORNUM
```

Insert after old physical line 757, before the following old line.

Insert this source:

```ir
LD TOK
PUSH
LIT 40
EQ FACTORPAREN
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R20` at `IR source name:`. Require `OK R20.ASM 20059 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R20` at `Source name:`, and require `OK 04321 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T20.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){putc(60+(2+3));}
```

Run `COPY T20.RIL SOURCE.RIL`, then `CHECK R20`.

Require:

```text
OK RESULT.IR 00079
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
LIT 00060
PUSH
LIT 00002
PUSH
LIT 00003
ADD
ADD
PUTC
HALT
```

Copy RESULT.IR to T20.IR. Translate it with CHECK IRKEEP, entering T20; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00488 bytes` and PASS.

VIEW.BAS must report T20.COM length **488 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T20`. It displays `A` and the checker reports PASS.

## A rejection check

Create X20.RIL with this separate test:

```rill
fn main(){putc((65);}
```

Copy X20.RIL to SOURCE.RIL, then run CHECK R20. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.
