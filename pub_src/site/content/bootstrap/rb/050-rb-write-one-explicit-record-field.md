+++
title = "17 \u00b7 Writing a Symbol Field"
weight = 17
description = "Pass the record offset and word value explicitly."
download = "RB17.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/050-rb-write-one-explicit-record-field/"]
reader_names = 1
+++

## The working parts

Pass the record offset and word value explicitly. SET16 performs a checked two-byte access. The caller chooses a field offset within its own record.

## Enter the source

Copy RB16.IR to RB17.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
GET8
RETURN
```

Insert after old physical line 628.

Insert:

```ir
PROC WRITEFIELD 2 0
LD TABLE
PUSH
PARAM 0
PUSH
PARAM 1
SET16
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
LIT 100
CALL TBYTE
PUSH
```

Remove this source at old physical positions 47–47 in RB16.IR:

```ir
LIT 52
```

Replace it with:

```ir
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
LIT 4660
SET16
LIT 100
```

Remove this source at old physical positions 45–45 in RB16.IR:

```ir
CALL TBYTE
```

Replace it with:

```ir
CALL TWORD
```

The following old source remains in place:

```ir
PUSH
LIT 52
```

### Edit 4

Unchanged source immediately before the edit:

```ir
LIT 100
PUSH
LIT 4660
```

Remove this source at old physical positions 43–43 in RB16.IR:

```ir
SET16
```

Replace it with:

```ir
PUSH
INVOKE WRITEFIELD 2
```

The following old source remains in place:

```ir
LIT 100
CALL TBYTE
```

### Edit 5

Unchanged source immediately before the edit:

```ir
LIT 22000
ALLOC
ST TABLE
```

Remove this source at old physical positions 38–39 in RB16.IR:

```ir
LD TABLE
PUSH
```

There is no replacement source.

The following old source remains in place:

```ir
LIT 100
PUSH
```

## Build this stopping point

```dos
COPY RB17.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000023382 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13305 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB17.COM
```

VIEW.BAS must report RB17.COM length 13305 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB17
```

The checker must report PASS. The driver compares the result with 4660 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare WRITEFIELD with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
