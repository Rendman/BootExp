+++
title = "17 \u00b7 Recording a Name and Its Meaning"
weight = 17
description = "Initialize a forty-byte symbol record, copy its complete spelling, and write its kind, value, and lexical level explicitly.."
download = "R17.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/017-initialize-a-complete-symbol/", "/bootstrap/rill/17-literal-byte-output/"]
+++

Initialize a forty-byte symbol record, copy its complete spelling, and write its kind, value, and lexical level explicitly.

## Enter the source

Copy R16.IR to R17.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 519

Unchanged source before the edit:

```ir
SET16
RETURN
```

Insert in its place:

```ir
PROC RECORD 1 1
LIT 0
SETLOCAL 0
LABEL RECORDCLEAR
LD TABLE
PUSH
PARAM 0
PUSH
LOCAL 0
ADD
PUSH
LIT 0
SET8
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
PUSH
LIT 40
CULT
JNZ RECORDCLEAR
LIT 0
SETLOCAL 0
LABEL RECORDNAME
LD TABLE
PUSH
PARAM 0
PUSH
LOCAL 0
ADD
PUSH
ADDR IDENT
PUSH
LOCAL 0
ADD
FETCHB
SET8
JZ RECORDFIELDS
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
JMP RECORDNAME
LABEL RECORDFIELDS
PARAM 0
PUSH
LIT 32
ADD
PUSH
LD RECTYPE
PUSH
INVOKE WRITEFIELD 2
PARAM 0
PUSH
LIT 34
ADD
PUSH
LD RECVAL
PUSH
INVOKE WRITEFIELD 2
PARAM 0
PUSH
LIT 36
ADD
PUSH
LD RECLEVEL
PUSH
INVOKE WRITEFIELD 2
PARAM 0
RETURN
```

The following old source remains:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit at old physical position 30

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
LIT 12345
```

The following old source remains:

```ir
CNE
RETURN
```

### Edit at old physical position 24

Unchanged source before the edit:

```ir
ST TABLE
LIT 100
PUSH
```

Remove:

```ir
LIT 4660
PUSH
INVOKE WRITEFIELD 2
LIT 100
```

Insert in its place:

```ir
INVOKE RECORD 1
LIT 1
ST GLOBALS
LIT 34
```

The following old source remains:

```ir
CALL TWORD
PUSH
```

### Edit at old physical position 22

Unchanged source before the edit:

```ir
LIT 22000
ALLOC
ST TABLE
```

Remove:

```ir
LIT 100
```

Insert in its place:

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
```

The following old source remains:

```ir
PUSH
LIT 4660
```

### Edit at old physical position 15

Unchanged source before the edit:

```ir
WORD ENDED 0
WORD OWN 0
WORD BACKUP 0
```

Insert in its place:

```ir
WORD RECTYPE 0
WORD RECVAL 0
WORD RECLEVEL 0
```

The following old source remains:

```ir
BUFFER DECIMAL 10
BUFFER INBUF 4096
```

### Edit at old physical position 3

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
WORD TABLE 0
```

Insert in its place:

```ir
WORD GLOBALS 0
```

The following old source remains:

```ir
WORD TOK 0
WORD VALUE 0
```

## Build and check

```dos
COPY R17.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 08469 bytes`. Save RESULT.COM as R17.COM. VIEW.BAS must show length 8469.

```dos
CHECK R17
```

Require PASS.

The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

