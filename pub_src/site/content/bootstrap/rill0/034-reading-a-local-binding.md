+++
title = "34 \u00b7 Reading a local binding"
weight = 34
description = "Compile a numeric value, parenthesized expression, local binding, or accepted builtin call."
download = "R34.IR"
download_group = "tools/rill0"
reader_names = 1
url = "/bootstrap/rill/034-reading-a-local-binding/"
+++

Resolve a local binding or builtin name and save its metadata before scanning further. Numeric and parenthesized primaries remain available. Argument parsing still reaches the rejecting CALLARGS stub in this checkpoint.

## Enter the source

Copy R33.IR to R34.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1239

Unchanged source before the edit:

```ir
CNE
JNZ SYNTAX
JMP NAMEFAIL
```

Insert in its place:

```ir
LABEL PRIMARYLOCAL
LITS "LOCAL "
CALL OUTSTR
LOCAL 2
CALL OUTNUM
CALL NEWLINE
JMP PRIMARYDONE
LABEL PRIMARYCALL
LOCAL 0
PUSH
LOCAL 3
PUSH
INVOKE CALLARGS 2
JMP PRIMARYDONE
```

The following old source remains:

```ir
LABEL PRIMARYNUM
LITS "LIT "
```

### Edit at old physical position 1238

Unchanged source before the edit:

```ir
LIT 1
CNE
JNZ SYNTAX
```

Insert in its place:

```ir
CALL RESOLVEOPTIONAL
SETLOCAL 0
LD RECTYPE
SETLOCAL 1
LD RECVAL
SETLOCAL 2
LD CALLBUILTIN
SETLOCAL 3
CALL LEX
LD TOK
PUSH
LIT 40
CEQ
JNZ PRIMARYCALL
LOCAL 1
PUSH
LIT 5
CEQ
JNZ PRIMARYLOCAL
```

The following old source remains:

```ir
JMP NAMEFAIL
LABEL PRIMARYNUM
```

### Edit at old physical position 1055

Unchanged source before the edit:

```ir
LOCAL 0
RETURN
```

Insert in its place:

```ir
PROC CALLARGS 2 0
LIT 2
PUSH
INVOKE ERROR 1
LIT 0
RETURN
```

The following old source remains:

```ir
PROC PREC 0 0
LD TOK
```

### Edit at old physical position 46

Unchanged source before the edit:

```ir
PUSH
INVOKE RECORD 1
LIT 1
```

Remove:

```ir
ST GLOBALS
```

Insert in its place:

```ir
ST LOCALCOUNT
```

The following old source remains:

```ir
LITS "RILL.TMP"
CREATE
```

### Edit at old physical position 42

Unchanged source before the edit:

```ir
ST RECVAL
LIT 0
ST RECLEVEL
```

Remove:

```ir
LIT 0
```

Insert in its place:

```ir
LIT 20480
```

The following old source remains:

```ir
PUSH
INVOKE RECORD 1
```

### Edit at old physical position 38

Unchanged source before the edit:

```ir
CALL SETIDENT
LIT 1
ST RECTYPE
```

Remove:

```ir
LIT 12345
```

Insert in its place:

```ir
LIT 0
```

The following old source remains:

```ir
ST RECVAL
LIT 0
```

### Edit at old physical position 36

Unchanged source before the edit:

```ir
ST TABLE
LITS "ABC"
CALL SETIDENT
```

Remove:

```ir
LIT 1
```

Insert in its place:

```ir
LIT 5
```

The following old source remains:

```ir
ST RECTYPE
LIT 12345
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
COPY R34.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 15321 bytes`. Save RESULT.COM as R34.COM. VIEW.BAS must show length 15321.

Create T34.RIL:

```rill
ABC+1
```

```dos
COPY T34.RIL SOURCE.RIL
```

```dos
CHECK R34
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 35 bytes and these complete bytes:

```text
4C 4F 43 41 4C 20 30 30 30 30 30 0D 0A 50 55 53
48 0D 0A 4C 49 54 20 30 30 30 30 31 0D 0A 41 44
44 0D 0A
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

## Check the new boundary

Use this separate rejected source:

```rill
UNKNOWN
```

Copy it to SOURCE.RIL and run CHECK R34. Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

