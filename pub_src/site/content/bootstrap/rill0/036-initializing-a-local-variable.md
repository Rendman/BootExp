+++
title = "36 \u00b7 Initializing a Local Variable"
weight = 36
description = "Build initializing a local variable.."
download = "R36.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/036-a-local-slot-and-initializer/"]
url = "/bootstrap/rill/036-initializing-a-local-variable/"
+++

Build initializing a local variable..

## Enter the source

Copy R35.IR to R36.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 944

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC DECLARE 0 2
CALL LEX
LITS "MUT"
CALL ISWORD
JZ SYNTAX
CALL LEX
LD TOK
PUSH
LIT 1
CNE
JNZ SYNTAX
LIT 20480
PUSH
LD LOCALCOUNT
PUSH
INVOKE FIND 2
PUSH
LIT 65535
CEQ
JNZ DECLNEW
LD RECLEVEL
PUSH
LD LEVEL
CEQ
JNZ NAMEFAIL
LABEL DECLNEW
LD NEXTLOCAL
PUSH
LIT 16
CUGE
JNZ CAPFAIL
LD NEXTLOCAL
ST RECVAL
SETLOCAL 0
LD LEVEL
ST RECLEVEL
LIT 8
CALL NEWLOCAL
SETLOCAL 1
LD NEXTLOCAL
PUSH
LIT 1
ADD
ST NEXTLOCAL
CALL LEX
LIT 61
PUSH
INVOKE EXPECT 1
LIT 1
PUSH
INVOKE EXPR 1
LOCAL 1
PUSH
LIT 32
ADD
PUSH
LIT 5
PUSH
INVOKE WRITEFIELD 2
LITS "SETLOCAL "
CALL OUTSTR
LOCAL 0
CALL OUTNUM
CALL NEWLINE
LIT 59
PUSH
INVOKE EXPECT 1
LIT 0
RETURN
```

The following old source remains:

```ir
PROC BUILTIN 0 5
LITS "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0EXIT\01\0POP\nEXIT\0\0"
```

### Edit at old physical position 62

Unchanged source before the edit:

```ir
CALL NEXT
CALL LEX
LIT 1
```

Remove:

```ir
PUSH
INVOKE EXPR 1
LD TOK
JNZ SYNTAX
```

Insert in its place:

```ir
ST LEVEL
CALL DECLARE
```

The following old source remains:

```ir
CALL FLUSH
LD OUTPUT
```

### Edit at old physical position 34

Unchanged source before the edit:

```ir
LIT 22000
ALLOC
ST TABLE
```

Remove:

```ir
LITS "ABC"
CALL SETIDENT
LIT 1
ST RECTYPE
LIT 12345
ST RECVAL
LIT 0
ST RECLEVEL
LIT 0
PUSH
INVOKE RECORD 1
LIT 1
ST GLOBALS
```

The following old source remains:

```ir
LITS "RILL.TMP"
CREATE
```

### Edit at old physical position 5

Unchanged source before the edit:

```ir
WORD TABLE 0
WORD GLOBALS 0
WORD LOCALCOUNT 0
```

Insert in its place:

```ir
WORD LEVEL 0
WORD NEXTLOCAL 0
```

The following old source remains:

```ir
WORD TOK 0
WORD VALUE 0
```

### Edit at old physical position 3

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
WORD TABLE 0
```

Remove:

```ir
WORD GLOBALS 0
```

The following old source remains:

```ir
WORD LOCALCOUNT 0
WORD TOK 0
```

## Build and check

```dos
COPY R36.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 15777 bytes`. Save RESULT.COM as R36.COM. VIEW.BAS must show length 15777.

Create T36.RIL:

```rill
let mut x=7;
```

```dos
COPY T36.RIL SOURCE.RIL
```

```dos
CHECK R36
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 27 bytes and these complete bytes:

```text
4C 49 54 20 30 30 30 30 37 0D 0A 53 45 54 4C 4F
43 41 4C 20 30 30 30 30 30 0D 0A
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

## Check the new boundary

Use this separate rejected source:

```rill
let mut x=x;
```

Copy it to SOURCE.RIL and run CHECK R36. Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

