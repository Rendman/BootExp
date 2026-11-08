+++
title = "23 \u00b7 Writing a Numeric Operand"
weight = 23
description = "Build writing a numeric operand.."
download = "R23.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/023-print-an-ir-operand/", "/bootstrap/rill/23-returning-a-program-status/"]
url = "/bootstrap/rill/023-writing-a-numeric-operand/"
+++

Build writing a numeric operand..

## Enter the source

Copy R22.IR to R23.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 789

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC OUTNUM 0 3
SETLOCAL 0
LIT 10000
SETLOCAL 1
LABEL OUTNUMPLACE
LIT 48
SETLOCAL 2
LABEL OUTNUMSUB
LOCAL 0
PUSH
LOCAL 1
CULT
JNZ OUTNUMDIGIT
LOCAL 0
PUSH
LOCAL 1
SUB
SETLOCAL 0
LOCAL 2
PUSH
LIT 1
ADD
SETLOCAL 2
JMP OUTNUMSUB
LABEL OUTNUMDIGIT
LOCAL 2
CALL OUTCHAR
LOCAL 1
PUSH
LIT 10
DIV
SETLOCAL 1
JNZ OUTNUMPLACE
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
LITS "HI"
CALL OUTSTR
```

Insert in its place:

```ir
LIT 12345
CALL OUTNUM
```

The following old source remains:

```ir
CALL FLUSH
LD OUTPUT
```

## Build and check

```dos
COPY R23.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 13425 bytes`. Save RESULT.COM as R23.COM. VIEW.BAS must show length 13425.

```dos
CHECK R23
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 5 bytes and these complete bytes:

```text
31 32 33 34 35
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

