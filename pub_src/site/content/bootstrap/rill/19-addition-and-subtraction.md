+++
title = "19 \u00b7 Addition and subtraction"
weight = 19
description = "Compile left-to-right word expressions with explicit operands."
download = "R19.IR"
download_group = "tools/rill0"
reader_names = 1
+++

An expression can combine several primary values without changing the assignment interface.

## The working parts

EXPR compiles one FACTOR, then accepts repeated + or - followed by another FACTOR. It emits PUSH for the source left value, saves the operator in FRAMES, and compiles the right value. Restoring the operator selects ADD or SUB. Both operators have the same precedence and associate left to right.

The saved compiler operator and emitted program expression word belong to different stacks. The compiler never leaves an IR expression temporary across its own CALL. Runtime addition and subtraction wrap modulo 65536. The test makes the result visible as an ASCII byte.

## Enter the source

Copy `R18.IR` to `R19.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL EXPR`

Unchanged source immediately before the edit:

```ir
; EXPRESSION
LABEL EXPR
CALL FACTOR
```

Insert after old physical line 702, before the following old line.

Insert this source:

```ir
LABEL EXPRLOOP
LD TOK
PUSH
LIT 43
EQ EXPROPERATOR
LD TOK
PUSH
LIT 45
NE EXPRDONE
LABEL EXPROPERATOR
LIT 21840
CALL PAIR
LIT 18515
CALL PAIR
LIT 2573
CALL PAIR
LD TOK
CALL SAVE
CALL LEX
CALL FACTOR
CALL RESTORE
PUSH
LIT 43
EQ EXPRADD
LIT 21843
CALL PAIR
LIT 3394
CALL PAIR
LIT 10
CALL CHAR
JMP EXPRLOOP
LABEL EXPRADD
LIT 17473
CALL PAIR
LIT 3396
CALL PAIR
LIT 10
CALL CHAR
JMP EXPRLOOP
LABEL EXPRDONE
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R19` at `IR source name:`. Require `OK R19.ASM 19881 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R19` at `Source name:`, and require `OK 04290 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T19.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){putc(70-6+1);}
```

Run `COPY T19.RIL SOURCE.RIL`, then `CHECK R19`.

Require:

```text
OK RESULT.IR 00079
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
LIT 00070
PUSH
LIT 00006
SUB
PUSH
LIT 00001
ADD
PUTC
HALT
```

Copy RESULT.IR to T19.IR. Translate it with CHECK IRKEEP, entering T19; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00490 bytes` and PASS.

VIEW.BAS must report T19.COM length **490 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T19`. It displays `A` and the checker reports PASS.

## A rejection check

Create X19.RIL with this separate test:

```rill
fn main(){putc(1*2);}
```

Copy X19.RIL to SOURCE.RIL, then run CHECK R19. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.
