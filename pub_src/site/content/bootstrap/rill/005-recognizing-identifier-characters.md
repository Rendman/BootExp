+++
title = "05 \u00b7 Recognizing Identifier Characters"
weight = 5
description = "Build recognizing identifier characters.."
download = "R05.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/005-identifier-characters/", "/bootstrap/rill/05-displaying-an-unsigned-word/"]
+++

Build recognizing identifier characters..

## Enter the source

Copy R04.IR to R05.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 13

Unchanged source before the edit:

```ir
PROC MAIN 0 0
LIT 2
PUSH
```

Remove:

```ir
INVOKE ERROR 1
```

Insert in its place:

```ir
INVOKE LETTER 1
PUSH
LIT 1
CNE
RETURN

PROC LETTER 1 0
PARAM 0
PUSH
LIT 95
CEQ
JNZ LETTERYES
PARAM 0
PUSH
LIT 65
CULT
JNZ LETTERNO
PARAM 0
PUSH
LIT 90
CULE
JNZ LETTERYES
PARAM 0
PUSH
LIT 97
CULT
JNZ LETTERNO
PARAM 0
PUSH
LIT 122
CUGT
JNZ LETTERNO
LABEL LETTERYES
LIT 1
RETURN
LABEL LETTERNO
```

The following old source remains:

```ir
LIT 0
RETURN
```

### Edit at old physical position 11

Unchanged source before the edit:

```ir
WORD BACKUP 0
BUFFER DECIMAL 10
PROC MAIN 0 0
```

Remove:

```ir
LIT 2
```

Insert in its place:

```ir
LIT 95
```

The following old source remains:

```ir
PUSH
INVOKE ERROR 1
```

## Build and check

```dos
COPY R05.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 02113 bytes`. Save RESULT.COM as R05.COM. VIEW.BAS must show length 2113.

```dos
CHECK R05
```

Require PASS.

The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

