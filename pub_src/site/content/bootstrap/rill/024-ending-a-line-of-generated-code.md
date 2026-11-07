+++
title = "24 \u00b7 Ending a Line of Generated Code"
weight = 24
description = "Build ending a line of generated code.."
download = "R24.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/024-terminate-an-emitted-record/", "/bootstrap/rill/24-naming-generated-blocks/"]
+++

Build ending a line of generated code..

## Enter the source

Copy R23.IR to R24.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 825

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC NEWLINE 0 0
LITS "\r\n"
CALL OUTSTR
LIT 0
RETURN
```

The following old source remains:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit at old physical position 34

Unchanged source before the edit:

```ir
JNZ IOFAIL
LIT 1
ST OWN
```

Remove:

```ir
LIT 12345
CALL OUTNUM
```

Insert in its place:

```ir
CALL NEWLINE
```

The following old source remains:

```ir
CALL FLUSH
LD OUTPUT
```

## Build and check

```dos
COPY R24.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 13457 bytes`. Save RESULT.COM as R24.COM. VIEW.BAS must show length 13457.

```dos
CHECK R24
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 2 bytes and these complete bytes:

```text
0D 0A
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

