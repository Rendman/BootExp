+++
title = "18 \u00b7 Adding a Local Name"
weight = 18
description = "Build adding a local name.."
download = "R18.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/018-a-separate-local-name-region/", "/bootstrap/rill/18-saving-an-assignment-name/"]
url = "/bootstrap/rill/018-adding-a-local-name/"
+++

Build adding a local name..

## Enter the source

Copy R17.IR to R18.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 604

Unchanged source before the edit:

```ir
PARAM 0
RETURN
```

Insert in its place:

```ir
PROC NEWLOCAL 0 1
ST RECTYPE
LD LOCALCOUNT
PUSH
LIT 32
CUGE
JNZ CAPFAIL
LD LOCALCOUNT
PUSH
LIT 40
MUL
PUSH
LIT 20480
ADD
SETLOCAL 0
LD LOCALCOUNT
PUSH
LIT 1
ADD
ST LOCALCOUNT
LOCAL 0
PUSH
INVOKE RECORD 1
RETURN
```

The following old source remains:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit at old physical position 42

Unchanged source before the edit:

```ir
LIT 34
CALL TWORD
PUSH
```

Remove:

```ir
LIT 12345
```

Insert in its place:

```ir
LIT 7
```

The following old source remains:

```ir
CNE
RETURN
```

### Edit at old physical position 32

Unchanged source before the edit:

```ir
ST RECTYPE
LIT 12345
ST RECVAL
```

Remove:

```ir
LIT 0
ST RECLEVEL
LIT 0
PUSH
INVOKE RECORD 1
LIT 1
ST GLOBALS
LIT 34
```

Insert in its place:

```ir
LIT 5
CALL NEWLOCAL
LIT 20514
```

The following old source remains:

```ir
CALL TWORD
PUSH
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
LIT 1
ST RECTYPE
LIT 12345
```

Insert in its place:

```ir
LIT 7
```

The following old source remains:

```ir
ST RECVAL
LIT 0
```

### Edit at old physical position 3

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
WORD TABLE 0
```

Remove:

```ir
WORD GLOBALS 0
```

Insert in its place:

```ir
WORD LOCALCOUNT 0
```

The following old source remains:

```ir
WORD TOK 0
WORD VALUE 0
```

## Build and check

```dos
COPY R18.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 08542 bytes`. Save RESULT.COM as R18.COM. VIEW.BAS must show length 8542.

```dos
CHECK R18
```

Require PASS.

The driver compares the result with 7 and returns nonzero on a mismatch; it adds no display routine.

