+++
title = "16 \u00b7 Writing a Symbol Field"
weight = 16
description = "Build writing a symbol field.."
download = "R16.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/016-write-one-explicit-record-field/", "/bootstrap/rill/16-declaring-mutable-words/"]
url = "/bootstrap/rill/016-writing-a-symbol-field/"
+++

Build writing a symbol field..

## Enter the source

Copy R15.IR to R16.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 511

Unchanged source before the edit:

```ir
GET8
RETURN
```

Insert in its place:

```ir
PROC WRITEFIELD 2 0
LD TABLE
PUSH
PARAM 0
PUSH
PARAM 1
SET16
RETURN
```

The following old source remains:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit at old physical position 31

Unchanged source before the edit:

```ir
LIT 100
CALL TBYTE
PUSH
```

Remove:

```ir
LIT 52
```

Insert in its place:

```ir
LIT 4660
```

The following old source remains:

```ir
CNE
RETURN
```

### Edit at old physical position 29

Unchanged source before the edit:

```ir
LIT 4660
SET16
LIT 100
```

Remove:

```ir
CALL TBYTE
```

Insert in its place:

```ir
CALL TWORD
```

The following old source remains:

```ir
PUSH
LIT 52
```

### Edit at old physical position 27

Unchanged source before the edit:

```ir
LIT 100
PUSH
LIT 4660
```

Remove:

```ir
SET16
```

Insert in its place:

```ir
PUSH
INVOKE WRITEFIELD 2
```

The following old source remains:

```ir
LIT 100
CALL TBYTE
```

### Edit at old physical position 22

Unchanged source before the edit:

```ir
LIT 22000
ALLOC
ST TABLE
```

Remove:

```ir
LD TABLE
PUSH
```

The following old source remains:

```ir
LIT 100
PUSH
```

## Build and check

```dos
COPY R16.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 08178 bytes`. Save RESULT.COM as R16.COM. VIEW.BAS must show length 8178.

```dos
CHECK R16
```

Require PASS.

The driver compares the result with 4660 and returns nonzero on a mismatch; it adds no display routine.

