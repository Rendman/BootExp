+++
title = "15 \u00b7 Reading a Word from Allocated Storage"
weight = 15
description = "An offset is meaningful only together with the TABLE block handle."
download = "RB15.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/048-rb-word-fields-in-an-opaque-block/"]
reader_names = 1
+++

## The working parts

An offset is meaningful only together with the TABLE block handle. GET16 reads the canonical low-byte-first word after validating its extent.

## Enter the source

Copy RB14.IR to RB15.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 607.

Insert:

```ir
PROC TWORD 0 1
SETLOCAL 0
LD TABLE
PUSH
LOCAL 0
GET16
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
LITS "ABC"
CALL ISWORD
PUSH
```

Remove this source at old physical positions 42–42 in RB14.IR:

```ir
LIT 1
```

Replace it with:

```ir
LIT 100
PUSH
LIT 4660
SET16
LIT 100
CALL TWORD
PUSH
LIT 4660
```

The following old source remains in place:

```ir
CNE
RETURN
```

### Edit 3

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–40 in RB14.IR:

```ir
LITS "ABC"
CALL SETIDENT
LIT 1
ST TOK
LITS "ABC"
CALL ISWORD
```

Replace it with:

```ir
LIT 22000
ALLOC
ST TABLE
LD TABLE
```

The following old source remains in place:

```ir
PUSH
LIT 1
```

## Build this stopping point

```dos
COPY RB15.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000022982 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13228 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB15.COM
```

VIEW.BAS must report RB15.COM length 13228 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB15
```

The checker must report PASS. The driver compares the result with 4660 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare TWORD with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
