+++
title = "21 \u00b7 Unary negation"
weight = 21
description = "Express a negative word using defined wrapping arithmetic."
download = "R21.IR"
download_group = "tools/rill0"
reader_names = 1
+++

Negation needs no signed literal token or processor-specific instruction.

## The working parts

FACTORMINUS consumes -, emits LIT 0 and PUSH, compiles another FACTOR, and emits SUB. The result is zero minus the operand modulo 65536. Unary minus therefore binds more tightly than the binary + and - operators.

The recursive FACTOR uses the same depth check as parentheses. A chain of unary operators is bounded rather than consuming an unchecked native call stack. The source spelling -1 denotes the word 65535; it does not change the language to signed arithmetic.

## Enter the source

Copy `R20.IR` to `R21.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL FACTORPAREN`

Unchanged source immediately before the edit:

```ir
CALL EXPR
LIT 41
CALL EXPECT
```

Insert after old physical line 787, before the following old line.

Insert this source:

```ir
JMP FACTORDONE
LABEL FACTORMINUS
CALL LEX
LIT 18764
CALL PAIR
LIT 8276
CALL PAIR
LIT 3376
CALL PAIR
LIT 20490
CALL PAIR
LIT 21333
CALL PAIR
LIT 3400
CALL PAIR
LIT 10
CALL CHAR
CALL FACTOR
LIT 21843
CALL PAIR
LIT 3394
CALL PAIR
LIT 10
CALL CHAR
```

### Change 2: following `LABEL FACTOR`

Unchanged source immediately before the edit:

```ir
PUSH
LIT 40
EQ FACTORPAREN
```

Insert after old physical line 761, before the following old line.

Insert this source:

```ir
LD TOK
PUSH
LIT 45
EQ FACTORMINUS
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R21` at `IR source name:`. Require `OK R21.ASM 20473 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R21` at `Source name:`, and require `OK 04406 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T21.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){putc(66+-1);}
```

Run `COPY T21.RIL SOURCE.RIL`, then `CHECK R21`.

Require:

```text
OK RESULT.IR 00075
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
LIT 00066
PUSH
LIT 0
PUSH
LIT 00001
SUB
ADD
PUTC
HALT
```

Copy RESULT.IR to T21.IR. Translate it with CHECK IRKEEP, entering T21; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00490 bytes` and PASS.

VIEW.BAS must report T21.COM length **490 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T21`. It displays `A` and the checker reports PASS.

## A rejection check

Create X21.RIL with this separate test:

```rill
fn main(){putc(--------1);}
```

Copy X21.RIL to SOURCE.RIL, then run CHECK R21. Require:

```text
ERROR 00001 CODE 00005
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.
