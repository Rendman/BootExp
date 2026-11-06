+++
title = "RB16 \u00b7 Byte fields in an opaque block"
weight = 49
description = "Use the same opaque block with a byte offset."
download = "RB16.IR"
download_group = "toolchain"
+++

Use the same opaque block with a byte offset.

## The working parts

Use the same opaque block with a byte offset. GET8 returns a zero-extended byte; it does not reveal a segment selector or native address.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB15.IR to RB16.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
GET16
RETURN
```

Insert after old physical line 619.

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
CALL PRINTNUM
LIT 0
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

Require IR86 `OK RESULT.ASM 0000023147 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13261 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB16.COM
```

VIEW.BAS must report RB16.COM length 13261 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB16
```

Require, apart from command echo and the checker's separator:

```text
00052PASS
```

## A rejection or boundary check

Check a representable-word boundary in the preceding translator. Create BAD.IR:

```ir
PROC MAIN 0 0
LIT 65536
RETURN
```

```dos
COPY BAD.IR SOURCE.IR
CHECK IWKEEP
```

Require `IR ERROR 0000000002 CODE 2` and FAIL. The accepted RESULT.ASM must remain unchanged. The diagnostic cannot be built from an out-of-range word.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
