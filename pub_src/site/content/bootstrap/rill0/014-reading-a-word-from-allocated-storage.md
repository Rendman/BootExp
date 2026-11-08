+++
title = "14 \u00b7 Reading a Word from Allocated Storage"
weight = 14
description = "Build reading a word from allocated storage.."
download = "R14.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/014-word-fields-in-an-opaque-block/", "/bootstrap/rill/14-buffering-the-accepted-text/"]
url = "/bootstrap/rill/014-reading-a-word-from-allocated-storage/"
+++

Build reading a word from allocated storage..

## Enter the source

Copy R13.IR to R14.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 490

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC TWORD 0 1
SETLOCAL 0
LD TABLE
PUSH
LOCAL 0
GET16
RETURN
```

The following old source remains:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit at old physical position 26

Unchanged source before the edit:

```ir
LITS "ABC"
CALL ISWORD
PUSH
```

Remove:

```ir
LIT 1
```

Insert in its place:

```ir
LIT 100
PUSH
LIT 4660
SET16
LIT 100
CALL TWORD
PUSH
LIT 4660
```

The following old source remains:

```ir
CNE
RETURN
```

### Edit at old physical position 19

Unchanged source before the edit:

```ir
BUFFER INBUF 4096
BUFFER IDENT 32
PROC MAIN 0 0
```

Remove:

```ir
LITS "ABC"
CALL SETIDENT
LIT 1
ST TOK
LITS "ABC"
CALL ISWORD
```

Insert in its place:

```ir
LIT 22000
ALLOC
ST TABLE
LD TABLE
```

The following old source remains:

```ir
PUSH
LIT 1
```

## Build and check

```dos
COPY R14.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 08101 bytes`. Save RESULT.COM as R14.COM. VIEW.BAS must show length 8101.

```dos
CHECK R14
```

Require PASS.

The driver compares the result with 4660 and returns nonzero on a mismatch; it adds no display routine.

