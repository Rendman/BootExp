+++
title = "23 \u00b7 Finding the Visible Binding"
weight = 23
description = "Search active local bindings first, then globals."
download = "RB23.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/056-rb-resolve-a-current-binding/"]
reader_names = 1
+++

## The working parts

Search active local bindings first, then globals. Save the found offset separately from kind and value fields; recursive parsing can replace the shared search result.

## Enter the source

Copy RB22.IR to RB23.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
INVOKE FIND 2
RETURN
```

Insert after old physical line 839.

Insert:

```ir
PROC RESOLVE 0 0
LIT 20480
PUSH
LD LOCALCOUNT
PUSH
INVOKE FIND 2
ST FOUND
PUSH
LIT 65535
CNE
JNZ RESOLVED
CALL LOOKGLOBAL
ST FOUND
PUSH
LIT 65535
CEQ
JNZ NAMEFAIL
LABEL RESOLVED
LD FOUND
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
INVOKE RECORD 1
LIT 1
ST GLOBALS
```

Remove this source at old physical positions 51–51 in RB22.IR:

```ir
CALL LOOKGLOBAL
```

Replace it with:

```ir
CALL RESOLVE
```

The following old source remains in place:

```ir
LD RECVAL
PUSH
```

## Build this stopping point

```dos
COPY RB23.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000027837 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14142 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB23.COM
```

VIEW.BAS must report RB23.COM length 14142 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB23
```

The checker must report PASS. The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare RESOLVE with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
