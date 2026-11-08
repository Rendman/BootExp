+++
title = "01 \u00b7 Printing a String"
weight = 1
description = "Walk zero-terminated text, preserving its pointer across a byte output call."
download = "R01.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/001-a-terminated-text-pointer/", "/bootstrap/rill/01-a-program-in-the-intermediate-language/"]
url = "/bootstrap/rill/001-printing-a-string/"
+++

Walk zero-terminated text, preserving its pointer across a byte output call. This display routine remains part of the compiler diagnostics.

## Enter the source

Create R01.IR as plain text:

```ir
; RILL compiler construction. Portable IR source.

PROC MAIN 0 0
LITS "HI"
CALL PRINT
LIT 0
RETURN

PROC PRINT 0 1
SETLOCAL 0
LABEL PRINTLOOP
LOCAL 0
FETCHB
JZ PRINTDONE
PUTC
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
JMP PRINTLOOP
LABEL PRINTDONE
LIT 0
RETURN
```

## Build and check

```dos
COPY R01.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 01098 bytes`. Save RESULT.COM as R01.COM. VIEW.BAS must show length 1098.

```dos
CHECK R01
```

Require:

```text
HIPASS
```

