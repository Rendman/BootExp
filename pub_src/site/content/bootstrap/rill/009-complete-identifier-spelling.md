+++
title = "09 \u00b7 Complete identifier spelling"
weight = 9
description = "Keep the token kind, numeric value, and complete spelling separate."
download = "R09.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/09-a-bounded-byte-reader/"]
+++

Keep the token kind, numeric value, and complete spelling separate. Fold identifiers while preserving source text. Reject decimal overflow before a word wraps.

## Enter the source

Copy R08.IR to R09.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 309

Unchanged source before the edit:

```ir
LIT 0
RETURN
LABEL LEXNAME
```

Remove:

```ir
JMP SYNTAX
```

Insert in its place:

```ir
LIT 0
SETLOCAL 0
LABEL NAMELOOP
LOCAL 0
PUSH
LIT 24
CUGE
JNZ NAMEFAIL
LD CH
SETLOCAL 1
PUSH
LIT 97
CULT
JNZ NAMESTORE
LOCAL 1
PUSH
LIT 122
CUGT
JNZ NAMESTORE
LOCAL 1
PUSH
LIT 32
SUB
SETLOCAL 1
LABEL NAMESTORE
ADDR IDENT
PUSH
LOCAL 0
ADD
PUSH
LOCAL 1
PUTB
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
CALL NEXT
LD CH
PUSH
INVOKE LETTER 1
JNZ NAMELOOP
LD CH
PUSH
INVOKE DIGIT 1
JNZ NAMELOOP
ADDR IDENT
PUSH
LOCAL 0
ADD
PUSH
LIT 0
PUTB
LIT 1
ST TOK
RETURN
```

The following old source remains:

```ir
LABEL LEXNUMBER
JMP SYNTAX
```

### Edit at old physical position 24

Unchanged source before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove:

```ir
LD TOK
PUSH
LIT 256
CNE
```

Insert in its place:

```ir
ADDR IDENT
CALL PRINT
LIT 0
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 16

Unchanged source before the edit:

```ir
WORD BACKUP 0
BUFFER DECIMAL 10
BUFFER INBUF 4096
```

Insert in its place:

```ir
BUFFER IDENT 32
```

The following old source remains:

```ir
PROC MAIN 0 0
LITS "SOURCE.RIL"
```

## Build and check

```dos
COPY R09.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 07601 bytes`. Save RESULT.COM as R09.COM. VIEW.BAS must show length 7601.

Create T09.RIL:

```rill
hello
```

```dos
COPY T09.RIL SOURCE.RIL
```

```dos
CHECK R09
```

Require:

```text
HELLOPASS
```

