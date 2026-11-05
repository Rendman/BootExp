+++
title = "13 \u00b7 Recognizing the program frame"
weight = 13
description = "Require the complete spelling and punctuation of fn main()."
download = "R13.IR"
+++

A parser can begin with a complete empty program before it accepts statements.

## The working parts

EXPECT receives the required token code in A. It compares TOK and the expected suffix WANTTAIL, clears WANTTAIL, and calls LEX. The main keyword has a remaining n, represented by suffix fourteen; the shorter fn token has an empty suffix. Punctuation also has an empty suffix.

ENDTOKEN checks a suffix for a keyword whose first group was already selected by a dispatcher. Both routines consume exactly one token on success. The driver requires fn main() followed by an empty brace pair and end of source. This is a recognizer: it reports OK but creates no IR file.

## Enter the source

Copy `R12.IR` to `R13.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL WORDTAIL`

Unchanged source immediately before the edit:

```ir
ADD
ST TOK
RET
```

Insert after old physical line 476, before the following old line.

Insert this source:

```ir
; EXPECT
LABEL EXPECT
PUSH
LD TOK
NE SYNTAX
LD WANTTAIL
PUSH
LD SUFFIX
NE SYNTAX
LIT 0
ST WANTTAIL
CALL LEX
RET
LABEL ENDTOKEN
PUSH
LD SUFFIX
NE SYNTAX
CALL LEX
RET
```

### Change 2: following `LABEL TOKENDONE`

Unchanged source immediately before the edit:

```ir
CLOSE
STATUS
JNZ IOFAIL
```

Insert after old physical line 45, before the following old line.

Insert this source:

```ir
LIT 19279
CALL PAIR
LIT 2573
CALL PAIR
```

### Change 3: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove these exact old lines (physical positions 28–41 in `R12.IR`):

```ir
LABEL SHOWTOKEN
LD TOK
JZ TOKENDONE
CALL NUMBER
LIT 58
CALL CHAR
LD SUFFIX
CALL NUMBER
LIT 32
CALL CHAR
CALL LEX
JMP SHOWTOKEN
LABEL TOKENDONE
CALL NEWLINE
```

Put this source in their place:

```ir
LIT 32974
CALL EXPECT
LIT 14
ST WANTTAIL
LIT 46121
CALL EXPECT
LIT 40
CALL EXPECT
LIT 41
CALL EXPECT
LIT 123
CALL EXPECT
LIT 125
CALL EXPECT
LIT 0
CALL EXPECT
```

### Change 4: in the declarations

Unchanged source immediately before the edit:

```ir
WORD CH 0
BUFFER INBYTE 1
WORD SUFFIX 0
```

Insert after old physical line 14, before the following old line.

Insert this source:

```ir
WORD WANTTAIL 0
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R13` at `IR source name:`. Require `OK R13.ASM 11570 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R13` at `Source name:`, and require `OK 02107 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T13.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main() {}
```

Run `COPY T13.RIL SOURCE.RIL`, then `CHECK R13`.

Apart from DOS command echo and the checker's separating blank line, require:

```text
OK
PASS
```

This is a diagnostic stopping point. It does not create RESULT.IR.

## A rejection check

Create X13.RIL with this separate test:

```rill
fn mainz() {}
```

Copy X13.RIL to SOURCE.RIL, then run CHECK R13. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

An unexpected PASS is a failed rejection test.

## If the result differs

Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.
