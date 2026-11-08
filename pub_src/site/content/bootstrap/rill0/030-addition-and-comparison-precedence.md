+++
title = "30 \u00b7 Addition and comparison precedence"
weight = 30
description = "Return a precedence for an accepted operator and zero for a nonoperator."
download = "R30.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/30-the-complete-pipeline/"]
url = "/bootstrap/rill/030-addition-and-comparison-precedence/"
+++

Return a precedence for an accepted operator and zero for a nonoperator. RILL0 starts with addition, subtraction, and unsigned comparisons.

## Enter the source

Copy R29.IR to R30.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1032

Unchanged source before the edit:

```ir
LOCAL 0
RETURN
```

Insert in its place:

```ir
PROC PREC 0 0
LD TOK
PUSH
LIT 256
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 257
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 258
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 259
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 60
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 62
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 43
CEQ
JNZ PRECSIX
LD TOK
PUSH
LIT 45
CEQ
JNZ PRECSIX
LIT 0
RETURN
LABEL PRECONE
LIT 1
RETURN
LABEL PRECTHREE
LIT 3
RETURN
LABEL PRECFOUR
LIT 4
RETURN
LABEL PRECFIVE
LIT 5
RETURN
LABEL PRECSIX
LIT 6
RETURN
LABEL PRECSEVEN
LIT 7
RETURN
```

The following old source remains:

```ir
LABEL IOFAIL
LIT 1
```

### Edit at old physical position 42

Unchanged source before the edit:

```ir
ST RECLEVEL
LIT 20480
PUSH
```

Remove:

```ir
INVOKE RECORD 1
LIT 1
ST LOCALCOUNT
CALL RESOLVEOPTIONAL
LD RECTYPE
PUSH
LIT 5
```

Insert in its place:

```ir
LIT 6
```

The following old source remains:

```ir
CNE
RETURN
```

### Edit at old physical position 29

Unchanged source before the edit:

```ir
BUFFER IDENT 32
WORD CALLBUILTIN 0
PROC MAIN 0 0
```

Remove:

```ir
LIT 22000
ALLOC
ST TABLE
LITS "ABC"
CALL SETIDENT
LIT 5
ST RECTYPE
LIT 0
ST RECVAL
LIT 0
ST RECLEVEL
LIT 20480
```

Insert in its place:

```ir
LITS "SOURCE.RIL"
OPEN
ST INPUT
STATUS
JNZ IOFAIL
CALL NEXT
CALL LEX
CALL PREC
```

The following old source remains:

```ir
PUSH
INVOKE RECORD 1
```

## Build and check

```dos
COPY R30.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 14348 bytes`. Save RESULT.COM as R30.COM. VIEW.BAS must show length 14348.

Create T30.RIL:

```rill
+
```

```dos
COPY T30.RIL SOURCE.RIL
```

```dos
CHECK R30
```

Require PASS.

The driver compares the result with 6 and returns nonzero on a mismatch; it adds no display routine.

