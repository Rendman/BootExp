+++
title = "22 \u00b7 Writing Text Through the Buffer"
weight = 22
description = "Build writing text through the buffer.."
download = "R22.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/022-append-a-text-template/", "/bootstrap/rill/22-byte-input-and-persistent-status/"]
+++

Build writing text through the buffer..

## Enter the source

Copy R21.IR to R22.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 755

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC OUTSTR 0 2
SETLOCAL 0
LIT 0
SETLOCAL 1
LABEL OUTSTRLOOP
LOCAL 0
FETCHB
JZ OUTSTRDONE
PUSH
LIT 10
CNE
JNZ OUTSTRBYTE
LOCAL 1
PUSH
LIT 13
CEQ
JNZ OUTSTRBYTE
LIT 13
CALL OUTCHAR
LABEL OUTSTRBYTE
LOCAL 0
FETCHB
SETLOCAL 1
CALL OUTCHAR
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
JMP OUTSTRLOOP
LABEL OUTSTRDONE
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
LIT 65
CALL OUTCHAR
```

Insert in its place:

```ir
LITS "HI"
CALL OUTSTR
```

The following old source remains:

```ir
CALL FLUSH
LD OUTPUT
```

## Build and check

```dos
COPY R22.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 13283 bytes`. Save RESULT.COM as R22.COM. VIEW.BAS must show length 13283.

```dos
CHECK R22
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 2 bytes and these complete bytes:

```text
48 49
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

