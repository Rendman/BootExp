+++
title = "22 \u00b7 Byte input and persistent status"
weight = 22
description = "Compile portable runtime calls as primary expressions."
download = "R22.IR"
+++

An input byte and its success indication are separate values and must both be available to a source program.

## The working parts

FACTORSERVICE saves the selected keyword, validates the remaining c or tus letters, and requires an empty parenthesis pair. It emits GETC or STATUS. GETC returns a byte or 65535 for EOF/error. STATUS returns zero for success, including EOF, or one for failure.

An assignment preserves the byte before a following status() call replaces A. Arithmetic and comparisons do not change the runtime status. All ordinary byte values, including 255, remain distinct from EOF. Terminal policy belongs to the binding; redirected input makes these tests reproducible.

## Enter the source

Copy `R21.IR` to `R22.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL FACTORMINUS`

Unchanged source immediately before the edit:

```ir
LIT 10
CALL CHAR
JMP FACTORDONE
```

Insert after old physical line 816, before the following old line.

Insert this source:

```ir
LABEL FACTORSERVICE
LD TOK
CALL SAVE
PUSH
LIT 40116
EQ CHECKGETC
LIT 21171
JMP CHECKSERVICE
LABEL CHECKGETC
LIT 3
LABEL CHECKSERVICE
CALL ENDTOKEN
LIT 40
CALL EXPECT
LIT 41
CALL EXPECT
CALL RESTORE
PUSH
LIT 40116
EQ FACTORGETC
LIT 21587
CALL PAIR
LIT 21569
CALL PAIR
LIT 21333
CALL PAIR
LIT 2573
CALL PAIR
JMP FACTORDONE
LABEL FACTORGETC
LIT 17735
CALL PAIR
LIT 17236
CALL PAIR
LIT 2573
CALL PAIR
```

### Change 2: following `LABEL FACTOR`

Unchanged source immediately before the edit:

```ir
PUSH
LIT 45
EQ FACTORMINUS
```

Insert after old physical line 765, before the following old line.

Insert this source:

```ir
LD TOK
PUSH
LIT 40116
EQ FACTORSERVICE
LD TOK
PUSH
LIT 52865
EQ FACTORSERVICE
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R22` at `IR source name:`. Require `OK R22.ASM 21253 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R22` at `Source name:`, and require `OK 04541 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T22.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){let mut c=0;let mut s=0;c=getc();s=status();putc(c);putc(s+48);}
```

Run `COPY T22.RIL SOURCE.RIL`, then `CHECK R22`.

Require:

```text
OK RESULT.IR 00118
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
WORD c 00000
WORD s 00000
LABEL MAIN
GETC
ST c
STATUS
ST s
LD c
PUTC
LD s
PUSH
LIT 00048
ADD
PUTC
HALT
```

Copy RESULT.IR to T22.IR. Translate it with CHECK IRKEEP, entering T22; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00508 bytes` and PASS.

VIEW.BAS must report T22.COM length **508 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 04 00 00
```

Create KEY.TXT with `ECHO Q>KEY.TXT`. Run `CHECK T22 <KEY.TXT`. It displays `Q0` and the checker reports PASS.

## A rejection check

Create X22.RIL with this separate test:

```rill
fn main(){putc(getcat());}
```

Copy X22.RIL to SOURCE.RIL, then run CHECK R22. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.
