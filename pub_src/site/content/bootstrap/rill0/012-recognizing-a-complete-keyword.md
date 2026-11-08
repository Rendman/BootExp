+++
title = "12 \u00b7 Recognizing a Complete Keyword"
weight = 12
description = "Build recognizing a complete keyword.."
download = "R12.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/012-compare-the-whole-keyword/", "/bootstrap/rill/12-exact-word-tokens/"]
url = "/bootstrap/rill/012-recognizing-a-complete-keyword/"
+++

Build recognizing a complete keyword..

## Enter the source

Copy R11.IR to R12.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 425

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC ISWORD 0 2
SETLOCAL 0
LD TOK
PUSH
LIT 1
CNE
JNZ WORDNO
LIT 0
SETLOCAL 1
LABEL WORDLOOP
ADDR IDENT
PUSH
LOCAL 1
ADD
FETCHB
PUSH
LOCAL 0
PUSH
LOCAL 1
ADD
FETCHB
CNE
JNZ WORDNO
ADDR IDENT
PUSH
LOCAL 1
ADD
FETCHB
JZ WORDYES
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
JMP WORDLOOP
LABEL WORDYES
LIT 1
RETURN
LABEL WORDNO
LIT 0
RETURN
```

The following old source remains:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit at old physical position 28

Unchanged source before the edit:

```ir
CALL LEX
LIT 43
PUSH
```

Remove:

```ir
INVOKE EXPECT 1
LITS "OK"
CALL PRINT
LIT 0
```

Insert in its place:

```ir
LIT 1
CNE
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 26

Unchanged source before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove:

```ir
LIT 43
```

Insert in its place:

```ir
LITS "FN"
CALL ISWORD
```

The following old source remains:

```ir
PUSH
INVOKE EXPECT 1
```

## Build and check

```dos
COPY R12.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 07986 bytes`. Save RESULT.COM as R12.COM. VIEW.BAS must show length 7986.

Create T12.RIL:

```rill
fn
```

```dos
COPY T12.RIL SOURCE.RIL
```

```dos
CHECK R12
```

Require PASS.

The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

