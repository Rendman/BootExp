+++
title = "21 \u00b7 Finding a Name in the Table"
weight = 21
description = "Search entries from the end toward the beginning and compare complete spellings."
download = "RB21.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/054-rb-search-exact-names-from-the-inside-out/"]
reader_names = 1
+++

## The working parts

Search entries from the end toward the beginning and compare complete spellings. This selects the innermost active binding. Return 65535 for absence; offset zero is a valid found record.

## Enter the source

Copy RB20.IR to RB21.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
GET8
RETURN
```

Insert after old physical line 628.

Insert:

```ir
PROC FIND 2 4
PARAM 1
SETLOCAL 0
LABEL FINDNEXT
LOCAL 0
JZ FINDNONE
PUSH
LIT 1
SUB
SETLOCAL 0
PUSH
LIT 40
MUL
PUSH
PARAM 0
ADD
SETLOCAL 1
LIT 0
SETLOCAL 2
LABEL FINDCHAR
LOCAL 1
PUSH
LOCAL 2
ADD
CALL TBYTE
SETLOCAL 3
PUSH
ADDR IDENT
PUSH
LOCAL 2
ADD
FETCHB
CNE
JNZ FINDNEXT
LOCAL 3
JZ FOUNDIT
LOCAL 2
PUSH
LIT 1
ADD
SETLOCAL 2
JMP FINDCHAR
LABEL FOUNDIT
LOCAL 1
PUSH
LIT 32
ADD
CALL TWORD
ST RECTYPE
LOCAL 1
PUSH
LIT 34
ADD
CALL TWORD
ST RECVAL
LOCAL 1
PUSH
LIT 36
ADD
CALL TWORD
ST RECLEVEL
LOCAL 1
RETURN
LABEL FINDNONE
LIT 65535
RETURN
```

The following old source remains in place:

```ir
PROC WRITEFIELD 2 0
LD TABLE
```

### Edit 2

Unchanged source immediately before the edit:

```ir
LIT 20514
CALL TWORD
PUSH
```

Remove this source at old physical positions 47–47 in RB20.IR:

```ir
LIT 7
```

Replace it with:

```ir
INVOKE RECORD 1
LIT 1
ST GLOBALS
LIT 0
PUSH
LIT 1
PUSH
INVOKE FIND 2
LD RECVAL
PUSH
LIT 12345
```

The following old source remains in place:

```ir
CNE
RETURN
```

### Edit 3

Unchanged source immediately before the edit:

```ir
CALL SETIDENT
LIT 7
ST RECVAL
```

Remove this source at old physical positions 42–45 in RB20.IR:

```ir
LIT 5
CALL NEWLOCAL
LIT 20514
CALL TWORD
```

Replace it with:

```ir
LIT 0
ST RECLEVEL
LIT 0
```

The following old source remains in place:

```ir
PUSH
LIT 7
```

### Edit 4

Unchanged source immediately before the edit:

```ir
ST TABLE
LITS "ABC"
CALL SETIDENT
```

Remove this source at old physical positions 40–40 in RB20.IR:

```ir
LIT 7
```

Replace it with:

```ir
LIT 1
ST RECTYPE
LIT 12345
```

The following old source remains in place:

```ir
ST RECVAL
LIT 5
```

## Build this stopping point

```dos
COPY RB21.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000027227 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14023 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB21.COM
```

VIEW.BAS must report RB21.COM length 14023 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB21
```

The checker must report PASS. The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare FIND with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
