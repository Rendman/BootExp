+++
title = "27 \u00b7 Naming a Branch Destination"
weight = 27
description = "Build naming a branch destination.."
download = "R27.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/027-emit-a-label-operand/", "/bootstrap/rill/27-equality-in-a-condition/"]
url = "/bootstrap/rill/027-naming-a-branch-destination/"
+++

Build naming a branch destination..

## Enter the source

Copy R26.IR to R27.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 846

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC LABELJUMP 0 1
SETLOCAL 0
LITS " B_"
CALL OUTSTR
LOCAL 0
CALL OUTNUM
CALL NEWLINE
LIT 0
RETURN
```

The following old source remains:

```ir
PROC NEWLINE 0 0
LITS "\r\n"
```

### Edit at old physical position 36

Unchanged source before the edit:

```ir
LIT 1
ST OWN
LIT 7
```

Remove:

```ir
CALL LABELDEF
```

Insert in its place:

```ir
CALL LABELJUMP
```

The following old source remains:

```ir
CALL FLUSH
LD OUTPUT
```

## Build and check

```dos
COPY R27.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 13615 bytes`. Save RESULT.COM as R27.COM. VIEW.BAS must show length 13615.

```dos
CHECK R27
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 10 bytes and these complete bytes:

```text
20 42 5F 30 30 30 30 37 0D 0A
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

