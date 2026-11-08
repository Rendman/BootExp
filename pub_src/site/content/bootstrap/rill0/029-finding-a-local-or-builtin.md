+++
title = "29 \u00b7 Finding a local or builtin"
weight = 29
description = "Recognize a builtin or an existing local binding."
download = "R29.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/29-a-repeated-block/"]
url = "/bootstrap/rill/029-finding-a-local-or-builtin/"
+++

Recognize a builtin or an existing local binding. RILL0 rejects an unknown name.

## Enter the source

Copy R28.IR to R29.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 993

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC RESOLVEOPTIONAL 0 1
CALL BUILTIN
ST CALLBUILTIN
JZ RESOLVEUSER
LIT 7
ST RECTYPE
LIT 65535
RETURN
LABEL RESOLVEUSER
LIT 20480
PUSH
LD LOCALCOUNT
PUSH
INVOKE FIND 2
SETLOCAL 0
PUSH
LIT 65535
CNE
JNZ RESOLVEGOT
JMP NAMEFAIL
LABEL RESOLVEGOT
LOCAL 0
RETURN
```

The following old source remains:

```ir
LABEL IOFAIL
LIT 1
```

### Edit at old physical position 34

Unchanged source before the edit:

```ir
LD RECVAL
PUSH
LIT 1
```

Insert in its place:

```ir
ST LOCALCOUNT
CALL RESOLVEOPTIONAL
LD RECTYPE
PUSH
LIT 5
```

The following old source remains:

```ir
CNE
RETURN
```

### Edit at old physical position 33

Unchanged source before the edit:

```ir
CALL BUILTIN
LD RECVAL
PUSH
```

Insert in its place:

```ir
INVOKE RECORD 1
```

The following old source remains:

```ir
LIT 1
CNE
```

### Edit at old physical position 30

Unchanged source before the edit:

```ir
PROC MAIN 0 0
LITS "PUTC"
CALL SETIDENT
```

Remove:

```ir
CALL BUILTIN
LD RECVAL
```

Insert in its place:

```ir
LIT 5
ST RECTYPE
LIT 0
ST RECVAL
LIT 0
ST RECLEVEL
LIT 20480
```

The following old source remains:

```ir
PUSH
LIT 1
```

### Edit at old physical position 28

Unchanged source before the edit:

```ir
BUFFER OUTBUF 4096
BUFFER IDENT 32
PROC MAIN 0 0
```

Remove:

```ir
LITS "PUTC"
```

Insert in its place:

```ir
LIT 22000
ALLOC
ST TABLE
LITS "ABC"
```

The following old source remains:

```ir
CALL SETIDENT
CALL BUILTIN
```

### Edit at old physical position 27

Unchanged source before the edit:

```ir
BUFFER INBUF 4096
BUFFER OUTBUF 4096
BUFFER IDENT 32
```

Insert in its place:

```ir
WORD CALLBUILTIN 0
```

The following old source remains:

```ir
PROC MAIN 0 0
LITS "PUTC"
```

## Build and check

```dos
COPY R29.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 14098 bytes`. Save RESULT.COM as R29.COM. VIEW.BAS must show length 14098.

```dos
CHECK R29
```

Require PASS.

The driver compares the result with 5 and returns nonzero on a mismatch; it adds no display routine.

