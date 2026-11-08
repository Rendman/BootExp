+++
title = "28 \u00b7 Recognizing Built-in Services"
weight = 28
description = "Build recognizing built-in services.."
download = "R28.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/028-a-table-of-portable-services/", "/bootstrap/rill/28-unsigned-ordering/"]
url = "/bootstrap/rill/028-recognizing-built-in-services/"
+++

Build recognizing built-in services..

## Enter the source

Copy R27.IR to R28.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 915

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC BUILTIN 0 5
LITS "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0EXIT\01\0POP\nEXIT\0\0"
SETLOCAL 0
LABEL BUILTINNEXT
LOCAL 0
FETCHB
JZ BUILTINNONE
LIT 0
SETLOCAL 1
LIT 1
SETLOCAL 2
LABEL BUILTINCHAR
LOCAL 0
PUSH
LOCAL 1
ADD
FETCHB
SETLOCAL 3
JZ BUILTINARG
LOCAL 3
PUSH
ADDR IDENT
PUSH
LOCAL 1
ADD
FETCHB
CEQ
JNZ BUILTINMATCH
LIT 0
SETLOCAL 2
LABEL BUILTINMATCH
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
JMP BUILTINCHAR
LABEL BUILTINARG
ADDR IDENT
PUSH
LOCAL 1
ADD
FETCHB
JZ BUILTINEXACT
LIT 0
SETLOCAL 2
LABEL BUILTINEXACT
LOCAL 0
PUSH
LOCAL 1
ADD
PUSH
LIT 1
ADD
SETLOCAL 0
LOCAL 0
FETCHB
PUSH
LIT 48
SUB
ST RECVAL
LOCAL 0
PUSH
LIT 2
ADD
SETLOCAL 0
LOCAL 2
JNZ BUILTINFOUND
LABEL BUILTINSKIP
LOCAL 0
FETCHB
SETLOCAL 3
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
LOCAL 3
JNZ BUILTINSKIP
JMP BUILTINNEXT
LABEL BUILTINFOUND
LOCAL 0
RETURN
LABEL BUILTINNONE
LIT 0
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
STATUS
JNZ IOFAIL
LIT 1
```

Remove:

```ir
ST OWN
LIT 7
CALL LABELJUMP
CALL FLUSH
LD OUTPUT
CLOSE
LIT 0
ST OUTPUT
ST OWN
LIT 0
```

Insert in its place:

```ir
CNE
```

The following old source remains:

```ir
RETURN
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
LITS "RILL.TMP"
CREATE
ST OUTPUT
STATUS
JNZ IOFAIL
```

Insert in its place:

```ir
LITS "PUTC"
CALL SETIDENT
CALL BUILTIN
LD RECVAL
PUSH
```

The following old source remains:

```ir
LIT 1
ST OWN
```

## Build and check

```dos
COPY R28.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 13949 bytes`. Save RESULT.COM as R28.COM. VIEW.BAS must show length 13949.

```dos
CHECK R28
```

Require PASS.

The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

