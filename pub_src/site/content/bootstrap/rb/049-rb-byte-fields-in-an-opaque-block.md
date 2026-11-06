+++
title = "16 \u00b7 Reading a Byte from Allocated Storage"
weight = 16
description = "Use the same opaque block with a byte offset."
download = "RB16.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/049-rb-byte-fields-in-an-opaque-block/"]
reader_names = 1
+++

## The working parts

Use the same opaque block with a byte offset. GET8 returns a zero-extended byte; it does not reveal a segment selector or native address.

## Enter the source

Copy RB15.IR to RB16.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
GET16
RETURN
```

Insert after old physical line 620.

Insert:

```ir
PROC TBYTE 0 1
SETLOCAL 0
LD TABLE
PUSH
LOCAL 0
GET8
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
CALL TWORD
PUSH
```

Remove this source at old physical positions 47–47 in RB15.IR:

```ir
LIT 4660
```

Replace it with:

```ir
LIT 52
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

Remove this source at old physical positions 45–45 in RB15.IR:

```ir
CALL TWORD
```

Replace it with:

```ir
CALL TBYTE
```

The following old source remains in place:

```ir
PUSH
LIT 4660
```

## Build this stopping point

```dos
COPY RB16.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000023184 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13268 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB16.COM
```

VIEW.BAS must report RB16.COM length 13268 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB16
```

The checker must report PASS. The driver compares the result with 52 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare TBYTE with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
