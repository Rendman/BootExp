+++
title = "22 \u00b7 Finding a Global Name"
weight = 22
description = "Restrict FIND to the active global entries."
download = "RB22.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/055-rb-the-global-namespace/"]
reader_names = 1
+++

## The working parts

Restrict FIND to the active global entries. A local shadow must not change how a procedure definition is found.

## Enter the source

Copy RB21.IR to RB22.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
INVOKE RECORD 1
RETURN
```

Insert after old physical line 835.

Insert:

```ir
PROC LOOKGLOBAL 0 0
LIT 0
PUSH
LD GLOBALS
PUSH
INVOKE FIND 2
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

Remove this source at old physical positions 51–55 in RB21.IR:

```ir
LIT 0
PUSH
LIT 1
PUSH
INVOKE FIND 2
```

Replace it with:

```ir
CALL LOOKGLOBAL
```

The following old source remains in place:

```ir
LD RECVAL
PUSH
```

## Build this stopping point

```dos
COPY RB22.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000027361 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14047 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB22.COM
```

VIEW.BAS must report RB22.COM length 14047 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB22
```

The checker must report PASS. The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare LOOKGLOBAL with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
