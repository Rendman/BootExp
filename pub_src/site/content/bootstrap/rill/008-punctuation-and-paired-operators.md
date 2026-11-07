+++
title = "08 \u00b7 Punctuation and paired operators"
weight = 8
description = "Keep the token kind, numeric value, and complete spelling separate."
download = "R08.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/08-opening-and-closing-the-source/"]
+++

Skip whitespace and line comments, and recognize punctuation and paired operators. Identifier, number, and string paths still reject input in this checkpoint.

## Enter the source

Copy R07.IR to R08.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 166

Unchanged source before the edit:

```ir
CUGT
JNZ LETTERNO
LIT 1
```

Insert in its place:

```ir
RETURN

PROC LEX 0 4
LABEL LEXSTART
LD CH
JZ LEXEOF
PUSH
LIT 32
CULE
JZ LEXKIND
CALL NEXT
JMP LEXSTART
LABEL LEXKIND
LD CH
PUSH
INVOKE LETTER 1
JNZ LEXNAME
LD CH
PUSH
INVOKE DIGIT 1
JNZ LEXNUMBER
LD CH
PUSH
LIT 34
CEQ
JNZ LEXSTRING
LD CH
SETLOCAL 0
CALL NEXT
LOCAL 0
PUSH
LIT 47
CNE
JNZ LEXPAIR
LD CH
PUSH
LIT 47
CNE
JNZ LEXPAIR
LABEL LEXCOMMENT
LD CH
JZ LEXSTART
PUSH
LIT 10
CEQ
JNZ LEXSTART
CALL NEXT
JMP LEXCOMMENT
LABEL LEXPAIR
LOCAL 0
ST TOK
LOCAL 0
PUSH
LIT 61
CEQ
JNZ PAIREQUAL
LOCAL 0
PUSH
LIT 33
CEQ
JNZ PAIRNOTEQUAL
LOCAL 0
PUSH
LIT 60
CEQ
JNZ PAIRLESS
LOCAL 0
PUSH
LIT 62
CEQ
JNZ PAIRGREATER
LIT 0
RETURN
LABEL PAIREQUAL
LD CH
PUSH
LIT 61
CNE
JNZ LEXRETURN
LIT 256
ST TOK
CALL NEXT
LIT 0
RETURN
LABEL PAIRNOTEQUAL
LD CH
PUSH
LIT 61
CNE
JNZ LEXRETURN
LIT 257
ST TOK
CALL NEXT
LIT 0
RETURN
LABEL PAIRLESS
LD CH
PUSH
LIT 61
CNE
JNZ PAIRLEFTSHIFT
LIT 258
ST TOK
CALL NEXT
LIT 0
RETURN
LABEL PAIRLEFTSHIFT
LD CH
PUSH
LIT 60
CNE
JNZ LEXRETURN
LIT 260
ST TOK
CALL NEXT
LIT 0
RETURN
LABEL PAIRGREATER
LD CH
PUSH
LIT 61
CNE
JNZ PAIRRIGHTSHIFT
LIT 259
ST TOK
CALL NEXT
LIT 0
RETURN
LABEL PAIRRIGHTSHIFT
LD CH
PUSH
LIT 62
CNE
JNZ LEXRETURN
LIT 261
ST TOK
CALL NEXT
LABEL LEXRETURN
LIT 0
RETURN
LABEL LEXNAME
JMP SYNTAX
LABEL LEXNUMBER
JMP SYNTAX
LABEL LEXSTRING
JMP SYNTAX
LABEL LEXEOF
LIT 0
ST TOK
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 24

Unchanged source before the edit:

```ir
CALL NEXT
LD CH
PUSH
```

Remove:

```ir
LIT 65
```

Insert in its place:

```ir
LIT 256
```

The following old source remains:

```ir
CNE
RETURN
```

### Edit at old physical position 22

Unchanged source before the edit:

```ir
STATUS
JNZ IOFAIL
CALL NEXT
```

Remove:

```ir
LD CH
```

Insert in its place:

```ir
CALL LEX
LD TOK
```

The following old source remains:

```ir
PUSH
LIT 65
```

### Edit at old physical position 3

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
WORD TABLE 0
```

Insert in its place:

```ir
WORD TOK 0
```

The following old source remains:

```ir
WORD CH 0
WORD LINE 1
```

## Build and check

```dos
COPY R08.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 07366 bytes`. Save RESULT.COM as R08.COM. VIEW.BAS must show length 7366.

Create T08.RIL:

```rill
==
```

```dos
COPY T08.RIL SOURCE.RIL
```

```dos
CHECK R08
```

Require PASS.

The driver compares the result with 256 and returns nonzero on a mismatch; it adds no display routine.

