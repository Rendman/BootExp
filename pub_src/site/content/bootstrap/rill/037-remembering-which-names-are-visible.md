+++
title = "37 \u00b7 Remembering Which Names Are Visible"
weight = 37
description = "Build remembering which names are visible.."
download = "R37.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/037-enter-and-leave-a-lexical-scope/"]
+++

Build remembering which names are visible..

## Enter the source

Copy R36.IR to R37.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 997

Unchanged source before the edit:

```ir
LIT 59
PUSH
INVOKE EXPECT 1
```

Insert in its place:

```ir
LIT 0
RETURN

PROC STATEMENT 0 0
LIT 2
PUSH
INVOKE ERROR 1
```

The following old source remains:

```ir
LIT 0
RETURN
```

### Edit at old physical position 930

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC BLOCK 0 2
LD LOCALCOUNT
SETLOCAL 0
LD NEXTLOCAL
SETLOCAL 1
LD LEVEL
PUSH
LIT 1
ADD
ST LEVEL
PUSH
LIT 16
CUGT
JNZ CAPFAIL
LIT 123
PUSH
INVOKE EXPECT 1
LABEL BLOCKNEXT
LD TOK
PUSH
LIT 125
CEQ
JNZ BLOCKEND
LD TOK
JZ SYNTAX
CALL STATEMENT
JMP BLOCKNEXT
LABEL BLOCKEND
CALL LEX
LOCAL 0
ST LOCALCOUNT
LOCAL 1
ST NEXTLOCAL
LD LEVEL
PUSH
LIT 1
SUB
ST LEVEL
LIT 0
RETURN
```

The following old source remains:

```ir
PROC DECLARE 0 2
CALL LEX
```

### Edit at old physical position 49

Unchanged source before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove:

```ir
LIT 1
ST LEVEL
CALL DECLARE
```

Insert in its place:

```ir
CALL BLOCK
```

The following old source remains:

```ir
CALL FLUSH
LD OUTPUT
```

## Build and check

```dos
COPY R37.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 15972 bytes`. Save RESULT.COM as R37.COM. VIEW.BAS must show length 15972.

Create T37.RIL:

```rill
{}
```

```dos
COPY T37.RIL SOURCE.RIL
```

```dos
CHECK R37
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 0 bytes and an empty file.

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

## Check the new boundary

Use this separate rejected source:

```rill
{putc(65);}
```

Copy it to SOURCE.RIL and run CHECK R37. Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

