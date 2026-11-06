+++
title = "11 \u00b7 Decimal word literals"
weight = 11
description = "Reject overflow before a numeric prefix can wrap."
download = "R11.IR"
download_group = "tools/rill0"
reader_names = 1
+++

A checked word literal cannot be formed by allowing arithmetic overflow and inspecting the result afterward.

## The working parts

SCANNUM builds TOKENVAL from decimal digits. Before adding a digit, a prefix above 6553 is rejected; at exactly 6553, the last digit must be at most five. Two times the old prefix is retained in COUNT, then combined with eight times the prefix to form ten times it. WORK holds the current digit.

The token code is 65535. CH retains the first nondigit. Signs and radix prefixes are not part of a numeric token. The diagnostic prints numeric values rather than their common token code. NEXT changes COUNT only after the completed numeric value has been saved.

## Enter the source

Copy `R10.IR` to `R11.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL COMMENTLOOP`

Unchanged source immediately before the edit:

```ir
LIT 13
EQ LEX
JMP COMMENTLOOP
```

Insert after old physical line 313, before the following old line.

Insert this source:

```ir
; SCANNUM
LABEL SCANNUM
LIT 0
ST TOKENVAL
LABEL DIGITLOOP
LD CH
PUSH
LIT 48
ULT NUMBEREND
LD CH
PUSH
LIT 57
UGT NUMBEREND
LD CH
PUSH
LIT 48
SUB
ST WORK
LD TOKENVAL
PUSH
LIT 6553
UGT NUMFAIL
LD TOKENVAL
PUSH
LIT 6553
NE NUMSAFE
LD WORK
PUSH
LIT 5
UGT NUMFAIL
LABEL NUMSAFE
LD TOKENVAL
PUSH
LD TOKENVAL
ADD
ST COUNT
PUSH
LD COUNT
ADD
ST TOKENVAL
LD TOKENVAL
PUSH
LD TOKENVAL
ADD
PUSH
LD COUNT
ADD
PUSH
LD WORK
ADD
ST TOKENVAL
CALL NEXT
JMP DIGITLOOP
LABEL NUMBEREND
LIT 65535
ST TOK
RET
```

### Change 2: following `LABEL LEXSTART`

Unchanged source immediately before the edit:

```ir
PUSH
LIT 47
EQ COMMENT
```

Insert after old physical line 237, before the following old line.

Insert this source:

```ir
LD CH
PUSH
LIT 48
ULT LETTERTEST
LD CH
PUSH
LIT 57
ULE SCANNUM
```

### Change 3: following `LABEL SHOWTOKEN`

Unchanged source immediately before the edit:

```ir
LABEL SHOWTOKEN
LD TOK
JZ TOKENDONE
```

Insert after old physical line 29, before the following old line.

Insert this source:

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

### Change 4: in the declarations

Unchanged source immediately before the edit:

```ir
WORD STEP 0
WORD COUNT 0
WORD INPUT 0
```

Insert after old physical line 10, before the following old line.

Insert this source:

```ir
WORD TOKENVAL 0
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R11` at `IR source name:`. Require `OK R11.ASM 09599 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R11` at `Source name:`, and require `OK 01735 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T11.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```text
0 9 65535
```

Run `COPY T11.RIL SOURCE.RIL`, then `CHECK R11`.

Apart from DOS command echo and the checker's separating blank line, require:

```text
00000 00009 65535 
PASS
```

This is a diagnostic stopping point. It does not create RESULT.IR.

## A rejection check

Create X11.RIL with this separate test:

```text
65536
```

Copy X11.RIL to SOURCE.RIL, then run CHECK R11. Require:

```text
ERROR 00001 CODE 00003
FAIL
```

An unexpected PASS is a failed rejection test.

## If the result differs

Check each service STATUS immediately, the current-byte advance, and any shared work cell needed across a call. Compare token values with the printed result before changing the parser.
