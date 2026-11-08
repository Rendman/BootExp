+++
title = "10 \u00b7 Checked decimal words"
weight = 10
description = "Keep the token kind, numeric value, and complete spelling separate."
download = "R10.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/10-punctuation-and-comments/"]
url = "/bootstrap/rill/010-checked-decimal-words/"
+++

Accumulate decimal VALUE only after checking that the next digit fits a word. TOK identifies a number; CH retains the first following character. Names and punctuation keep their earlier behavior; strings are still rejected.

## Enter the source

Copy R09.IR to R10.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 366

Unchanged source before the edit:

```ir
ST TOK
RETURN
LABEL LEXNUMBER
```

Remove:

```ir
JMP SYNTAX
```

Insert in its place:

```ir
LIT 0
ST VALUE
LABEL NUMBERLOOP
LD VALUE
PUSH
LIT 6553
CUGT
JNZ NUMBERFAIL
LD VALUE
PUSH
LIT 6553
CNE
JNZ NUMBERCALC
LD CH
PUSH
LIT 53
CUGT
JNZ NUMBERFAIL
LABEL NUMBERCALC
LD VALUE
PUSH
LIT 10
MUL
PUSH
LD CH
ADD
PUSH
LIT 48
SUB
ST VALUE
CALL NEXT
LD CH
PUSH
INVOKE DIGIT 1
JNZ NUMBERLOOP
LIT 2
ST TOK
RETURN
```

The following old source remains:

```ir
LABEL LEXSTRING
JMP SYNTAX
```

### Edit at old physical position 25

Unchanged source before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove:

```ir
ADDR IDENT
CALL PRINT
LIT 0
```

Insert in its place:

```ir
LD VALUE
PUSH
LIT 65535
CNE
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 4

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
WORD TABLE 0
WORD TOK 0
```

Insert in its place:

```ir
WORD VALUE 0
```

The following old source remains:

```ir
WORD CH 0
WORD LINE 1
```

## Build and check

```dos
COPY R10.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 07760 bytes`. Save RESULT.COM as R10.COM. VIEW.BAS must show length 7760.

Create T10.RIL:

```rill
65535
```

```dos
COPY T10.RIL SOURCE.RIL
```

```dos
CHECK R10
```

Require PASS.

The driver compares the result with 65535 and returns nonzero on a mismatch; it adds no display routine.

## Check the new boundary

Use this separate rejected source:

```rill
65536
```

Copy it to SOURCE.RIL and run CHECK R10. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

