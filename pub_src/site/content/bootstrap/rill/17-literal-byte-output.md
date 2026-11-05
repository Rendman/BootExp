+++
title = "17 \u00b7 Literal byte output"
weight = 17
description = "Compile a useful statement through a small expression interface."
download = "R17.IR"
+++

putc(65); gives the parser a complete statement with a visible runtime effect.

## The working parts

BODY repeatedly calls STATEMENT until a closing brace. It consumes that brace and returns. BLOCK first requires an opening brace and then uses BODY. DEPTH counts active body and primary-expression calls; exceeding eight is a capacity error.

EXPR calls FACTOR. FACTOR checks the numeric token and emits LIT with its value; PUTSTAT checks the parentheses and semicolon and emits PUTC. These routines compile operations rather than performing the source program output. At this stopping point only numeric primary expressions and putc statements are accepted.

## Enter the source

Copy `R16.IR` to `R17.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL DECLARE`

Unchanged source immediately before the edit:

```ir
LIT 59
CALL EXPECT
RET
```

Insert after old physical line 658, before the following old line.

Insert this source:

```ir
; EXPRESSION
LABEL EXPR
CALL FACTOR
RET
; FACTOR
LABEL FACTOR
LD DEPTH
PUSH
LIT 1
ADD
ST DEPTH
PUSH
LIT 8
UGT CAPFAIL
LD TOK
PUSH
LIT 65535
NE SYNTAX
LABEL FACTORNUM
LIT 18764
CALL PAIR
LIT 8276
CALL PAIR
LD TOKENVAL
CALL NUMBER
CALL NEWLINE
CALL LEX
JMP FACTORDONE
LABEL FACTORDONE
LD DEPTH
PUSH
LIT 1
SUB
ST DEPTH
RET
; BODY
LABEL BLOCK
LIT 123
CALL EXPECT
LABEL BODY
LD DEPTH
PUSH
LIT 1
ADD
ST DEPTH
PUSH
LIT 8
UGT CAPFAIL
LABEL BODYLOOP
LD TOK
PUSH
LIT 125
EQ BODYDONE
CALL STATEMENT
JMP BODYLOOP
LABEL BODYDONE
CALL LEX
LD DEPTH
PUSH
LIT 1
SUB
ST DEPTH
RET
; STATEMENT
LABEL STATEMENT
LD TOK
PUSH
LIT 49844
EQ PUTSTAT
JMP SYNTAX
LABEL PUTSTAT
LIT 3
CALL ENDTOKEN
LIT 40
CALL EXPECT
CALL EXPR
LIT 41
CALL EXPECT
LIT 59
CALL EXPECT
LIT 21840
CALL PAIR
LIT 17236
CALL PAIR
LIT 2573
CALL PAIR
RET
```

### Change 2: following `LABEL DECLDONE`

Unchanged source immediately before the edit:

```ir
CALL PAIR
LIT 2573
CALL PAIR
```

Remove these exact old lines (physical positions 70–71 in `R16.IR`):

```ir
LIT 125
CALL EXPECT
```

Put this source in their place:

```ir
CALL BODY
```

### Change 3: in the declarations

Unchanged source immediately before the edit:

```ir
WORD TOK 0
WORD VARNAME 0
BUFFER VARS 26
```

Insert after old physical line 19, before the following old line.

Insert this source:

```ir
WORD DEPTH 0
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R17` at `IR source name:`. Require `OK R17.ASM 18061 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R17` at `Source name:`, and require `OK 03915 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T17.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){putc(72);putc(73);}
```

Run `COPY T17.RIL SOURCE.RIL`, then `CHECK R17`.

Require:

```text
OK RESULT.IR 00052
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
LIT 00072
PUTC
LIT 00073
PUTC
HALT
```

Copy RESULT.IR to T17.IR. Translate it with CHECK IRKEEP, entering T17; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00480 bytes` and PASS.

VIEW.BAS must report T17.COM length **480 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T17`. It displays `HI` and the checker reports PASS.

## A rejection check

Create X17.RIL with this separate test:

```rill
fn main(){putc(65536);}
```

Copy X17.RIL to SOURCE.RIL, then run CHECK R17. Require:

```text
ERROR 00001 CODE 00003
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.
