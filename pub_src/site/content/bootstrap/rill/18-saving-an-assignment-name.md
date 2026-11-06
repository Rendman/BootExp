+++
title = "18 \u00b7 Saving an assignment name"
weight = 18
description = "Preserve parser state across nested routine calls."
download = "R18.IR"
cartoon = "rill-drawers.png"
download_group = "tools/rill0"
reader_names = 1
+++

The name on the left of an assignment must survive scanning and compiling its right side.

## The working parts

SAVE receives a word in A and places it in FRAMES at twice SAVECNT. It checks the thirty-two-word bound first and returns the saved value. RESTORE refuses an empty stack, decrements the count, and returns the latest word. VALUE is scratch for the store. This is compiler data, separate from the IR expression stack.

STATEMENT saves the checked destination letter, parses = and its expression, and restores the letter for ST. FACTOR similarly emits LD for a declared variable. Pending names live in FRAMES rather than in VARNAME, which another variable reference may change. All helper calls keep the IR expression stack balanced.

## Enter the source

Copy `R17.IR` to `R18.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL STATEMENT`

Unchanged source immediately before the edit:

```ir
PUSH
LIT 49844
EQ PUTSTAT
```

Remove these exact old lines (physical positions 728–728 in `R17.IR`):

```ir
JMP SYNTAX
```

Put this source in their place:

```ir
CALL USEVAR
CALL SAVE
CALL LEX
LIT 61
CALL EXPECT
CALL EXPR
LIT 59
CALL EXPECT
LIT 21587
CALL PAIR
LIT 32
CALL CHAR
CALL RESTORE
CALL CHAR
CALL NEWLINE
RET
```

### Change 2: following `LABEL FACTOR`

Unchanged source immediately before the edit:

```ir
LD TOK
PUSH
LIT 65535
```

Remove these exact old lines (physical positions 676–676 in `R17.IR`):

```ir
NE SYNTAX
```

Put this source in their place:

```ir
EQ FACTORNUM
CALL USEVAR
CALL SAVE
CALL LEX
LIT 17484
CALL PAIR
LIT 32
CALL CHAR
CALL RESTORE
CALL CHAR
CALL NEWLINE
JMP FACTORDONE
```

### Change 3: following `LABEL DECLARE`

Unchanged source immediately before the edit:

```ir
LIT 59
CALL EXPECT
RET
```

Insert after old physical line 658, before the following old line.

Insert this source:

```ir
; SAVE
LABEL SAVE
ST VALUE
LD SAVECNT
PUSH
LIT 32
UGE CAPFAIL
LD SAVECNT
PUSH
LD SAVECNT
ADD
PUSH
ADDR FRAMES
ADD
PUSH
LD VALUE
PUT
LD SAVECNT
PUSH
LIT 1
ADD
ST SAVECNT
LD VALUE
RET
LABEL RESTORE
LD SAVECNT
JZ CAPFAIL
PUSH
LIT 1
SUB
ST SAVECNT
PUSH
LD SAVECNT
ADD
PUSH
ADDR FRAMES
ADD
FETCH
RET
```

### Change 4: in the declarations

Unchanged source immediately before the edit:

```ir
WORD TOK 0
WORD VARNAME 0
BUFFER VARS 26
```

Insert after old physical line 19, before the following old line.

Insert this source:

```ir
WORD SAVECNT 0
BUFFER FRAMES 64
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R18` at `IR source name:`. Require `OK R18.ASM 19232 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R18` at `Source name:`, and require `OK 04170 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T18.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){let mut x=65;let mut y=0;y=x;putc(y);}
```

Run `COPY T18.RIL SOURCE.RIL`, then `CHECK R18`.

Require:

```text
OK RESULT.IR 00070
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
WORD x 00065
WORD y 00000
LABEL MAIN
LD x
ST y
LD y
PUTC
HALT
```

Copy RESULT.IR to T18.IR. Translate it with CHECK IRKEEP, entering T18; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00487 bytes` and PASS.

VIEW.BAS must report T18.COM length **487 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 04 00 41
```

Run `CHECK T18`. It displays `A` and the checker reports PASS.

## A rejection check

Create X18.RIL with this separate test:

```rill
fn main(){putc(x);}
```

Copy X18.RIL to SOURCE.RIL, then run CHECK R18. Require:

```text
ERROR 00001 CODE 00004
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.
