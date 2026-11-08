+++
title = "19 \u00b7 Finding a Name in the Table"
weight = 19
description = "Search complete spellings from the innermost live binding outward."
download = "R19.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/019-search-exact-names-from-the-inside-out/", "/bootstrap/rill/19-addition-and-subtraction/"]
url = "/bootstrap/rill/019-finding-a-name-in-the-table/"
+++

Search complete spellings from the innermost live binding outward. Offset zero is valid; 65535 represents absence.

## Enter the source

Copy R18.IR to R19.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 515

Unchanged source before the edit:

```ir
GET8
RETURN
```

Insert in its place:

```ir
PROC FIND 2 4
PARAM 1
SETLOCAL 0
LABEL FINDNEXT
LOCAL 0
JZ FINDNONE
PUSH
LIT 1
SUB
SETLOCAL 0
PUSH
LIT 40
MUL
PUSH
PARAM 0
ADD
SETLOCAL 1
LIT 0
SETLOCAL 2
LABEL FINDCHAR
LOCAL 1
PUSH
LOCAL 2
ADD
CALL TBYTE
SETLOCAL 3
PUSH
ADDR IDENT
PUSH
LOCAL 2
ADD
FETCHB
CNE
JNZ FINDNEXT
LOCAL 3
JZ FOUNDIT
LOCAL 2
PUSH
LIT 1
ADD
SETLOCAL 2
JMP FINDCHAR
LABEL FOUNDIT
LOCAL 1
PUSH
LIT 32
ADD
CALL TWORD
ST RECTYPE
LOCAL 1
PUSH
LIT 34
ADD
CALL TWORD
ST RECVAL
LOCAL 1
PUSH
LIT 36
ADD
CALL TWORD
ST RECLEVEL
LOCAL 1
RETURN
LABEL FINDNONE
LIT 65535
RETURN
```

The following old source remains:

```ir
PROC WRITEFIELD 2 0
LD TABLE
```

### Edit at old physical position 35

Unchanged source before the edit:

```ir
LIT 20514
CALL TWORD
PUSH
```

Remove:

```ir
LIT 7
```

Insert in its place:

```ir
INVOKE RECORD 1
LIT 1
ST GLOBALS
LIT 0
PUSH
LIT 1
PUSH
INVOKE FIND 2
LD RECVAL
PUSH
LIT 12345
```

The following old source remains:

```ir
CNE
RETURN
```

### Edit at old physical position 30

Unchanged source before the edit:

```ir
CALL SETIDENT
LIT 7
ST RECVAL
```

Remove:

```ir
LIT 5
CALL NEWLOCAL
LIT 20514
CALL TWORD
```

Insert in its place:

```ir
LIT 0
ST RECLEVEL
LIT 0
```

The following old source remains:

```ir
PUSH
LIT 7
```

### Edit at old physical position 28

Unchanged source before the edit:

```ir
ST TABLE
LITS "ABC"
CALL SETIDENT
```

Remove:

```ir
LIT 7
```

Insert in its place:

```ir
LIT 1
ST RECTYPE
LIT 12345
```

The following old source remains:

```ir
ST RECVAL
LIT 5
```

### Edit at old physical position 3

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
WORD TABLE 0
```

Insert in its place:

```ir
WORD GLOBALS 0
```

The following old source remains:

```ir
WORD LOCALCOUNT 0
WORD TOK 0
```

## Build and check

```dos
COPY R19.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 08814 bytes`. Save RESULT.COM as R19.COM. VIEW.BAS must show length 8814.

```dos
CHECK R19
```

Require PASS.

The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

