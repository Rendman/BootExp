+++
title = "31 \u00b7 Translating an Arithmetic Operation"
weight = 31
description = "Build translating an arithmetic operation.."
download = "R31.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/031-emit-a-word-operation/"]
url = "/bootstrap/rill/031-translating-an-arithmetic-operation/"
+++

Build translating an arithmetic operation..

## Enter the source

Copy R30.IR to R31.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1093

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

### Edit at old physical position 43

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

### Edit at old physical position 39

Unchanged source before the edit:

```ir
LITS "SOURCE.RIL"
PUSH
INVOKE FILEARG 2
```

Remove:

```ir
OPEN
ST INPUT
```

Insert in its place:

```ir
CREATE
ST OUTPUT
```

The following old source remains:

```ir
STATUS
JNZ IOFAIL
```

### Edit at old physical position 36

Unchanged source before the edit:

```ir
INVOKE FILEARG 2
LIT 1
PUSH
```

Remove:

```ir
LITS "SOURCE.RIL"
```

Insert in its place:

```ir
LITS "RILL.TMP"
```

The following old source remains:

```ir
PUSH
INVOKE FILEARG 2
```

### Edit at old physical position 34

Unchanged source before the edit:

```ir
LITS "SOURCE.RIL"
PUSH
INVOKE FILEARG 2
```

Remove:

```ir
LIT 1
```

Insert in its place:

```ir
LIT 2
```

The following old source remains:

```ir
PUSH
LITS "SOURCE.RIL"
```

## Build and check

```dos
CHECK IRKEEP R31.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 15500 bytes`. Save RESULT.COM as R31.COM. VIEW.BAS must show length 15500.

```dos
CHECK R31 SOURCE.RIL RESULT.IR
```

Require PASS.

Inspect RESULT.IR with VIEW.BAS. Require length 5 bytes and these complete bytes:

```text
41 44 44 0D 0A
```

This is a fragment for inspection, not a complete program. The command-selected RESULT.IR contains that fragment.

