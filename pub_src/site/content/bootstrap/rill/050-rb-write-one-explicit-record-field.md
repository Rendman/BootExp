+++
title = "RB17 \u00b7 Write one explicit record field"
weight = 50
description = "Pass the record offset and word value explicitly."
download = "RB17.IR"
download_group = "toolchain"
+++

Pass the record offset and word value explicitly.

## The working parts

Pass the record offset and word value explicitly. SET16 performs a checked two-byte access. The caller chooses a field offset within its own record.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB16.IR to RB17.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
GET8
RETURN
```

Insert after old physical line 627.

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
CALL PRINTNUM
LIT 0
```

### Edit 3

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

### Edit 4

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

Require IR86 `OK RESULT.ASM 0000023345 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13298 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB17.COM
```

VIEW.BAS must report RB17.COM length 13298 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB17
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
