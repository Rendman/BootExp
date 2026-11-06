+++
title = "RB19 \u00b7 Add a global definition"
weight = 19
description = "Append one global or procedure record, bounded by 512 entries."
download = "RB19.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/052-rb-add-a-global-definition/"]
+++

Append one global or procedure record, bounded by 512 entries.

## The working parts

Append one global or procedure record, bounded by 512 entries. The record offset remains stable even after scanning changes IDENT.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB18.IR to RB19.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
PARAM 0
RETURN
```

Insert after old physical line 716.

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

Require IR86 `OK RESULT.ASM 0000025253 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13647 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB19.COM
```

VIEW.BAS must report RB19.COM length 13647 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB19
```

Require, apart from command echo and the checker's separator:

```text
12345PASS
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
