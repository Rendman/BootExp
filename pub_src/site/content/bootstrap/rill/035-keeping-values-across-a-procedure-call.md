+++
title = "35 \u00b7 Keeping Values Across a Procedure Call"
weight = 35
description = "Build keeping values across a procedure call.."
download = "R35.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/035-nested-argument-expressions/"]
+++

Build keeping values across a procedure call..

## Enter the source

Copy R34.IR to R35.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1060

Unchanged source before the edit:

```ir
INVOKE ERROR 1
LIT 0
RETURN
```

Insert in its place:

```ir
LABEL ARGUSER
JMP NAMEFAIL
```

The following old source remains:

```ir

PROC PREC 0 0
```

### Edit at old physical position 1057

Unchanged source before the edit:

```ir
PROC CALLARGS 2 0
LIT 2
PUSH
```

Remove:

```ir
INVOKE ERROR 1
```

Insert in its place:

```ir
LIT 48
SUB
PUSH
LOCAL 0
CNE
JNZ NAMEFAIL
PARAM 1
CALL OUTSTR
CALL NEWLINE
```

The following old source remains:

```ir
LIT 0
RETURN
```

### Edit at old physical position 1056

Unchanged source before the edit:

```ir

PROC CALLARGS 2 0
LIT 2
```

Insert in its place:

```ir
SUB
FETCHB
```

The following old source remains:

```ir
PUSH
INVOKE ERROR 1
```

### Edit at old physical position 1054

Unchanged source before the edit:

```ir
LOCAL 0
RETURN
```

Remove:

```ir
PROC CALLARGS 2 0
```

Insert in its place:

```ir
PROC CALLARGS 2 3
LIT 0
SETLOCAL 0
LIT 40
PUSH
INVOKE EXPECT 1
LD TOK
PUSH
LIT 41
CEQ
JNZ ARGSEND
LABEL ARGLOOP
LOCAL 0
PUSH
LIT 16
CUGE
JNZ CAPFAIL
LIT 1
PUSH
INVOKE EXPR 1
LITS "PUSH\r\n"
CALL OUTSTR
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
LD TOK
PUSH
LIT 41
CEQ
JNZ ARGSEND
LIT 44
PUSH
INVOKE EXPECT 1
JMP ARGLOOP
LABEL ARGSEND
CALL LEX
PARAM 1
JZ ARGUSER
PUSH
```

The following old source remains:

```ir
LIT 2
PUSH
```

### Edit at old physical position 45

Unchanged source before the edit:

```ir
PUSH
INVOKE RECORD 1
LIT 1
```

Remove:

```ir
ST LOCALCOUNT
```

Insert in its place:

```ir
ST GLOBALS
```

The following old source remains:

```ir
LITS "RILL.TMP"
CREATE
```

### Edit at old physical position 41

Unchanged source before the edit:

```ir
ST RECVAL
LIT 0
ST RECLEVEL
```

Remove:

```ir
LIT 20480
```

Insert in its place:

```ir
LIT 0
```

The following old source remains:

```ir
PUSH
INVOKE RECORD 1
```

### Edit at old physical position 37

Unchanged source before the edit:

```ir
CALL SETIDENT
LIT 5
ST RECTYPE
```

Remove:

```ir
LIT 0
```

Insert in its place:

```ir
LIT 12345
```

The following old source remains:

```ir
ST RECVAL
LIT 0
```

### Edit at old physical position 35

Unchanged source before the edit:

```ir
ST TABLE
LITS "ABC"
CALL SETIDENT
```

Remove:

```ir
LIT 5
```

Insert in its place:

```ir
LIT 1
```

The following old source remains:

```ir
ST RECTYPE
LIT 0
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
WORD LOCALCOUNT 0
WORD TOK 0
```

## Build and check

```dos
COPY R35.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 15540 bytes`. Save RESULT.COM as R35.COM. VIEW.BAS must show length 15540.

Create T35.RIL:

```rill
putc(65)
```

```dos
COPY T35.RIL SOURCE.RIL
```

```dos
CHECK R35
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 28 bytes and these complete bytes:

```text
4C 49 54 20 30 30 30 36 35 0D 0A 50 55 53 48 0D
0A 50 4F 50 0D 0A 50 55 54 43 0D 0A
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

## Check the new boundary

Use this separate rejected source:

```rill
get8(1)
```

Copy it to SOURCE.RIL and run CHECK R35. Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

