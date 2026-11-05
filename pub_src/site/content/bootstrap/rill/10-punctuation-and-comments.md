+++
title = "10 \u00b7 Punctuation and comments"
weight = 10
description = "Turn character pairs into unambiguous tokens."
download = "R10.IR"
+++

The parser should see one token for == or <=, rather than two unrelated characters.

## The working parts

LEX skips spaces and line endings, sets SUFFIX zero, and puts a punctuation code in TOK. The codes for ==, !=, <=, and >= are 200 through 203; other punctuation keeps its ASCII value. It retains the first byte after a token in CH.

COMMENT requires a second slash and consumes through CR, LF, or end of source. A lone slash is an error because division is not in this subset. The diagnostic displays each token code as a word. It does not validate a RILL program.

## Enter the source

Copy `R09.IR` to `R10.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL NEXTDONE`

Unchanged source immediately before the edit:

```ir
ST CH
LABEL NEXTDONE
RET
```

Insert after old physical line 215, before the following old line.

Insert this source:

```ir
; LEX
LABEL LEX
LIT 0
ST SUFFIX
LD CH
JZ LEXEND
PUSH
LIT 32
UGT LEXSTART
CALL NEXT
JMP LEX
LABEL LEXSTART
LD CH
PUSH
LIT 47
EQ COMMENT
LABEL LETTERTEST
LABEL PUNCT
LD CH
ST TOK
CALL NEXT
LD TOK
PUSH
LIT 61
EQ CHECKPAIR
LD TOK
PUSH
LIT 33
EQ CHECKPAIR
LD TOK
PUSH
LIT 60
EQ CHECKPAIR
LD TOK
PUSH
LIT 62
NE LEXDONE
LABEL CHECKPAIR
LD CH
PUSH
LIT 61
NE LEXDONE
LD TOK
PUSH
LIT 61
EQ EQUALPAIR
LD TOK
PUSH
LIT 33
EQ UNEQUALPAIR
LD TOK
PUSH
LIT 60
EQ LESSPAIR
LIT 203
JMP PAIRTOKEN
LABEL EQUALPAIR
LIT 200
JMP PAIRTOKEN
LABEL UNEQUALPAIR
LIT 201
JMP PAIRTOKEN
LABEL LESSPAIR
LIT 202
LABEL PAIRTOKEN
ST TOK
CALL NEXT
LABEL LEXDONE
RET
LABEL LEXEND
LIT 0
ST TOK
RET
; COMMENT
LABEL COMMENT
CALL NEXT
LD CH
PUSH
LIT 47
NE SYNTAX
LABEL COMMENTLOOP
CALL NEXT
LD CH
JZ LEX
PUSH
LIT 10
EQ LEX
LD CH
PUSH
LIT 13
EQ LEX
JMP COMMENTLOOP
```

### Change 2: following `LABEL DISPLAY`

Unchanged source immediately before the edit:

```ir
LD CH
JZ DISPLAYDONE
CALL CHAR
```

Remove these exact old lines (physical positions 28–30 in `R09.IR`):

```ir
CALL NEXT
JMP DISPLAY
LABEL DISPLAYDONE
```

Put this source in their place:

```ir
CALL LEX
JMP SHOWTOKEN
LABEL TOKENDONE
CALL NEWLINE
```

### Change 3: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
STATUS
JNZ IOFAIL
CALL NEXT
```

Remove these exact old lines (physical positions 24–26 in `R09.IR`):

```ir
LABEL DISPLAY
LD CH
JZ DISPLAYDONE
```

Put this source in their place:

```ir
CALL LEX
LABEL SHOWTOKEN
LD TOK
JZ TOKENDONE
CALL NUMBER
LIT 32
```

### Change 4: in the declarations

Unchanged source immediately before the edit:

```ir
WORD INPUT 0
WORD CH 0
BUFFER INBYTE 1
```

Insert after old physical line 12, before the following old line.

Insert this source:

```ir
WORD SUFFIX 0
WORD TOK 0
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R10` at `IR source name:`. Require `OK R10.ASM 08214 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R10` at `Source name:`, and require `OK 01500 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T10.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```text
()+-{}; == != <= >= // comment
```

Run `COPY T10.RIL SOURCE.RIL`, then `CHECK R10`.

Apart from DOS command echo and the checker's separating blank line, require:

```text
00040 00041 00043 00045 00123 00125 00059 00200 00201 00202 00203 
PASS
```

This is a diagnostic stopping point. It does not create RESULT.IR.

## A rejection check

Create X10.RIL with this separate test:

```text
/
```

Copy X10.RIL to SOURCE.RIL, then run CHECK R10. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

An unexpected PASS is a failed rejection test.

## If the result differs

Check each service STATUS immediately, the current-byte advance, and any shared work cell needed across a call. Compare token values with the printed result before changing the parser.
