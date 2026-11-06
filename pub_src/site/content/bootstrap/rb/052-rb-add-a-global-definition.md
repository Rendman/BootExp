+++
title = "19 \u00b7 Adding a Global Name"
weight = 19
description = "Append one global or procedure record, bounded by 512 entries."
download = "RB19.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/052-rb-add-a-global-definition/"]
reader_names = 1
+++

## The working parts

Append one global or procedure record, bounded by 512 entries. The record offset remains stable even after scanning changes IDENT.

## Enter the source

Copy RB18.IR to RB19.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
PARAM 0
RETURN
```

Insert after old physical line 717.

Insert:

```ir
PROC NEWGLOBAL 0 1
ST RECTYPE
LD GLOBALS
PUSH
LIT 512
CUGE
JNZ CAPFAIL
LD GLOBALS
PUSH
LIT 40
MUL
SETLOCAL 0
LD GLOBALS
PUSH
LIT 1
ADD
ST GLOBALS
LOCAL 0
PUSH
INVOKE RECORD 1
RETURN
```

The following old source remains in place:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit 2

Unchanged source immediately before the edit:

```ir
PUSH
INVOKE RECORD 1
LIT 1
```

Remove this source at old physical positions 50–50 in RB18.IR:

```ir
ST GLOBALS
```

Replace it with:

```ir
CALL NEWGLOBAL
```

The following old source remains in place:

```ir
LIT 34
CALL TWORD
```

### Edit 3

Unchanged source immediately before the edit:

```ir
ST RECTYPE
LIT 12345
ST RECVAL
```

Remove this source at old physical positions 44–48 in RB18.IR:

```ir
LIT 0
ST RECLEVEL
LIT 0
PUSH
INVOKE RECORD 1
```

There is no replacement source.

The following old source remains in place:

```ir
LIT 1
ST GLOBALS
```

### Edit 4

Unchanged source immediately before the edit:

```ir
ST TABLE
LITS "ABC"
CALL SETIDENT
```

Remove this source at old physical positions 40–41 in RB18.IR:

```ir
LIT 1
ST RECTYPE
```

There is no replacement source.

The following old source remains in place:

```ir
LIT 12345
ST RECVAL
```

## Build this stopping point

```dos
COPY RB19.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000025290 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13654 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB19.COM
```

VIEW.BAS must report RB19.COM length 13654 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB19
```

The checker must report PASS. The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare NEWGLOBAL with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
