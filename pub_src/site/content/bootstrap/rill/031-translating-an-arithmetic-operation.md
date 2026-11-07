+++
title = "31 \u00b7 Translating an Arithmetic Operation"
weight = 31
description = "Build translating an arithmetic operation.."
download = "R31.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/031-emit-a-word-operation/"]
+++

Build translating an arithmetic operation..

## Enter the source

Copy R30.IR to R31.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1084

Unchanged source before the edit:

```ir
LIT 7
RETURN
```

Insert in its place:

```ir
PROC BINARY 0 1
SETLOCAL 0
PUSH
LIT 43
CEQ
JNZ BINADD
LOCAL 0
PUSH
LIT 45
CEQ
JNZ BINSUB
LOCAL 0
PUSH
LIT 256
CEQ
JNZ BINEQ
LOCAL 0
PUSH
LIT 257
CEQ
JNZ BINNE
LOCAL 0
PUSH
LIT 258
CEQ
JNZ BINLE
LOCAL 0
PUSH
LIT 259
CEQ
JNZ BINGE
LOCAL 0
PUSH
LIT 60
CEQ
JNZ BINLT
LITS "CUGT\r\n"
JMP BINDONE
LABEL BINADD
LITS "ADD\r\n"
JMP BINDONE
LABEL BINSUB
LITS "SUB\r\n"
JMP BINDONE
LABEL BINEQ
LITS "CEQ\r\n"
JMP BINDONE
LABEL BINNE
LITS "CNE\r\n"
JMP BINDONE
LABEL BINLE
LITS "CULE\r\n"
JMP BINDONE
LABEL BINGE
LITS "CUGE\r\n"
JMP BINDONE
LABEL BINLT
LITS "CULT\r\n"
LABEL BINDONE
CALL OUTSTR
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
ST INPUT
STATUS
JNZ IOFAIL
```

Remove:

```ir
CALL NEXT
CALL LEX
CALL PREC
PUSH
LIT 6
CNE
```

Insert in its place:

```ir
LIT 1
ST OWN
LIT 43
CALL BINARY
CALL FLUSH
LD OUTPUT
CLOSE
LIT 0
ST OUTPUT
ST OWN
LIT 0
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 29

Unchanged source before the edit:

```ir
BUFFER IDENT 32
WORD CALLBUILTIN 0
PROC MAIN 0 0
```

Remove:

```ir
LITS "SOURCE.RIL"
OPEN
ST INPUT
```

Insert in its place:

```ir
LITS "RILL.TMP"
CREATE
ST OUTPUT
```

The following old source remains:

```ir
STATUS
JNZ IOFAIL
```

## Build and check

```dos
COPY R31.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 14690 bytes`. Save RESULT.COM as R31.COM. VIEW.BAS must show length 14690.

```dos
CHECK R31
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 5 bytes and these complete bytes:

```text
41 44 44 0D 0A
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

