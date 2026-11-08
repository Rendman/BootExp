+++
title = "15 \u00b7 Reading a Byte from Allocated Storage"
weight = 15
description = "Build reading a byte from allocated storage.."
download = "R15.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/015-byte-fields-in-an-opaque-block/", "/bootstrap/rill/15-writing-the-accepted-ir-file/"]
url = "/bootstrap/rill/015-reading-a-byte-from-allocated-storage/"
+++

Build reading a byte from allocated storage..

## Enter the source

Copy R14.IR to R15.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 503

Unchanged source before the edit:

```ir
GET16
RETURN
```

Insert in its place:

```ir
PROC TBYTE 0 1
SETLOCAL 0
LD TABLE
PUSH
LOCAL 0
GET8
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
CALL TWORD
PUSH
```

Remove:

```ir
LIT 4660
```

Insert in its place:

```ir
LIT 52
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
CALL TWORD
```

Insert in its place:

```ir
CALL TBYTE
```

The following old source remains:

```ir
PUSH
LIT 4660
```

## Build and check

```dos
COPY R15.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 08141 bytes`. Save RESULT.COM as R15.COM. VIEW.BAS must show length 8141.

```dos
CHECK R15
```

Require PASS.

The driver compares the result with 52 and returns nonzero on a mismatch; it adds no display routine.

