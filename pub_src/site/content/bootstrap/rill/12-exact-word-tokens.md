+++
title = "12 \u00b7 Exact word tokens"
weight = 12
description = "Retain every letter of a short word without a dictionary file."
download = "R12.IR"
cartoon = "rill-tails.png"
+++

Recognizing the beginning of a keyword is insufficient: putc and putcat must remain different.

## The working parts

SCANWORD admits at most six lowercase letters. Each letter becomes a value from one through twenty-six. Doubling TOKENVAL five times multiplies it by 32 before the letter is added. The first group of at most three letters goes in TOK; the remaining group goes in SUFFIX. Adding 32768 distinguishes a word from punctuation. A single letter instead keeps its ASCII code for a variable.

Base 32 fits three letters in a word without discarding bits. Nonzero letter digits make both groups exact, including their lengths. WORK counts letters and STEP holds the current letter while COUNT controls doubling. The diagnostic displays both fields; the parser must check both before accepting a keyword.

## Enter the source

Copy `R11.IR` to `R12.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL NUMBEREND`

Unchanged source immediately before the edit:

```ir
LIT 65535
ST TOK
RET
```

Insert after old physical line 387, before the following old line.

Insert this source:

```ir
; SCANWORD
LABEL SCANWORD
LIT 0
ST WORK
ST TOKENVAL
LABEL WORDLOOP
LD WORK
PUSH
LIT 6
UGE NAMEFAIL
LD CH
PUSH
LIT 96
SUB
ST STEP
LIT 5
ST COUNT
LABEL WORDSHIFT
LD TOKENVAL
PUSH
LD TOKENVAL
ADD
ST TOKENVAL
LD COUNT
PUSH
LIT 1
SUB
ST COUNT
JNZ WORDSHIFT
LD TOKENVAL
PUSH
LD STEP
ADD
ST TOKENVAL
LD WORK
PUSH
LIT 1
ADD
ST WORK
PUSH
LIT 3
NE WORDNEXT
LD TOKENVAL
ST TOK
LIT 0
ST TOKENVAL
LABEL WORDNEXT
CALL NEXT
LD CH
PUSH
LIT 97
ULT WORDEND
LD CH
PUSH
LIT 122
ULE WORDLOOP
LABEL WORDEND
LD WORK
PUSH
LIT 1
NE WORDLONG
LD TOKENVAL
PUSH
LIT 96
ADD
ST TOK
RET
LABEL WORDLONG
LD WORK
PUSH
LIT 3
UGE WORDTAIL
LD TOKENVAL
ST TOK
LIT 0
ST TOKENVAL
LABEL WORDTAIL
LD TOKENVAL
ST SUFFIX
LD TOK
PUSH
LIT 32768
ADD
ST TOK
RET
```

### Change 2: following `LABEL LETTERTEST`

Unchanged source immediately before the edit:

```ir
LIT 57
ULE SCANNUM
LABEL LETTERTEST
```

Insert after old physical line 255, before the following old line.

Insert this source:

```ir
LD CH
PUSH
LIT 97
ULT PUNCT
LD CH
PUSH
LIT 122
ULE SCANWORD
```

### Change 3: following `LABEL SHOWTOKEN`

Unchanged source immediately before the edit:

```ir
LABEL SHOWTOKEN
LD TOK
JZ TOKENDONE
```

Remove these exact old lines (physical positions 31–38 in `R11.IR`):

```ir
PUSH
LIT 65535
NE SHOWVALUE
LD TOKENVAL
JMP TOKENPRINT
LABEL SHOWVALUE
LD TOK
LABEL TOKENPRINT
```

Put this source in their place:

```ir
CALL NUMBER
LIT 58
CALL CHAR
LD SUFFIX
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R12` at `IR source name:`. Require `OK R12.ASM 11165 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R12` at `Source name:`, and require `OK 02030 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T12.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```text
fn main let mut putc getc status if else while exit x
```

Run `COPY T12.RIL SOURCE.RIL`, then `CHECK R12`.

Apart from DOS command echo and the checker's separating blank line, require:

```text
32974:00000 46121:00014 45236:00000 46772:00000 49844:00003 40116:00003 52865:21171 33062:00000 38291:00005 56585:00389 38665:00020 00120:00000 
PASS
```

This is a diagnostic stopping point. It does not create RESULT.IR.

## A rejection check

Create X12.RIL with this separate test:

```text
abcdefg
```

Copy X12.RIL to SOURCE.RIL, then run CHECK R12. Require:

```text
ERROR 00001 CODE 00004
FAIL
```

An unexpected PASS is a failed rejection test.

## If the result differs

Check each service STATUS immediately, the current-byte advance, and any shared work cell needed across a call. Compare token values with the printed result before changing the parser.
