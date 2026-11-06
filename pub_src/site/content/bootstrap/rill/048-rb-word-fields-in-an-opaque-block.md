+++
title = "RB15 \u00b7 Word fields in an opaque block"
weight = 48
description = "An offset is meaningful only together with the TABLE block handle."
download = "RB15.IR"
download_group = "toolchain"
+++

An offset is meaningful only together with the TABLE block handle.

## The working parts

An offset is meaningful only together with the TABLE block handle. GET16 reads the canonical low-byte-first word after validating its extent.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB14.IR to RB15.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 603.

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
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–38 in RB14.IR:

```ir
LITS "ABC"
CALL SETIDENT
ADDR IDENT
CALL PRINT
```

Replace it with:

```ir
LIT 22000
ALLOC
ST TABLE
LD TABLE
PUSH
LIT 100
PUSH
LIT 4660
SET16
LIT 100
CALL TWORD
CALL PRINTNUM
```

The following old source remains in place:

```ir
LIT 0
RETURN
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

Require IR86 `OK RESULT.ASM 0000022945 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13221 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB15.COM
```

VIEW.BAS must report RB15.COM length 13221 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB15
```

Require, apart from command echo and the checker's separator:

```text
04660PASS
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
