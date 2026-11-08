+++
title = "13 \u00b7 Copying a Name"
weight = 13
description = "Build copying a name.."
download = "R13.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/013-save-an-explicit-spelling/", "/bootstrap/rill/13-recognizing-the-program-frame/"]
url = "/bootstrap/rill/013-copying-a-name/"
+++

Build copying a name..

## Enter the source

Copy R12.IR to R13.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 466

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC SETIDENT 0 2
SETLOCAL 0
LIT 0
SETLOCAL 1
LABEL SETIDLOOP
ADDR IDENT
PUSH
LOCAL 1
ADD
PUSH
LOCAL 0
PUSH
LOCAL 1
ADD
FETCHB
PUTB
JZ SETIDDONE
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
JMP SETIDLOOP
LABEL SETIDDONE
LIT 0
RETURN
```

The following old source remains:

```ir
PROC PRINT 0 1
SETLOCAL 0
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
LITS "SOURCE.RIL"
OPEN
ST INPUT
STATUS
JNZ IOFAIL
CALL NEXT
CALL LEX
LITS "FN"
```

Insert in its place:

```ir
LITS "ABC"
CALL SETIDENT
LIT 1
ST TOK
LITS "ABC"
```

The following old source remains:

```ir
CALL ISWORD
PUSH
```

## Build and check

```dos
COPY R13.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 08058 bytes`. Save RESULT.COM as R13.COM. VIEW.BAS must show length 8058.

```dos
CHECK R13
```

Require PASS.

The driver compares the result with ABC and returns nonzero on a mismatch; it adds no display routine.

