+++
title = "02 \u00b7 Printing a Number"
weight = 2
description = "Keep the value and decimal place in separate local slots."
download = "R02.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/002-a-visible-word-value/", "/bootstrap/rill/02-a-checked-character-writer/"]
+++

Keep the value and decimal place in separate local slots. Emit the decimal digits without borrowing a parser work cell.

## Enter the source

Copy R01.IR to R02.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 25

Unchanged source before the edit:

```ir
LABEL PRINTDONE
LIT 0
RETURN
```

Insert in its place:

```ir

PROC PRINTNUM 0 3
SETLOCAL 0
LIT 10000
SETLOCAL 1
LABEL PRINTPLACE
LIT 48
SETLOCAL 2
LABEL PRINTSUB
LOCAL 0
PUSH
LOCAL 1
CULT
JNZ PRINTDIGIT
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
JMP PRINTSUB
LABEL PRINTDIGIT
LOCAL 2
PUTC
LOCAL 1
PUSH
LIT 10
DIV
SETLOCAL 1
JNZ PRINTPLACE
LIT 0
RETURN
```

### Edit at old physical position 4

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.

PROC MAIN 0 0
```

Remove:

```ir
LITS "HI"
CALL PRINT
```

Insert in its place:

```ir
LIT 65535
CALL PRINTNUM
```

The following old source remains:

```ir
LIT 0
RETURN
```

## Build and check

```dos
COPY R02.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 01240 bytes`. Save RESULT.COM as R02.COM. VIEW.BAS must show length 1240.

```dos
CHECK R02
```

Require:

```text
65535PASS
```

