+++
title = "34 \u00b7 Remembering Calls Before Their Definitions"
weight = 34
description = "A call can precede its procedure definition."
download = "RB34.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/067-rb-call-names-and-forward-declarations/"]
reader_names = 1
+++

## The working parts

A call can precede its procedure definition. Record its name and required arity as a pending procedure; final acceptance rejects any definition that never arrives. Ordinary undeclared variable use remains an error.

## Enter the source

Copy RB33.IR to RB34.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 1174.

Insert:

```ir
PROC RESOLVEOPTIONAL 0 1
CALL BUILTIN
ST CALLBUILTIN
JZ RESOLVEUSER
LIT 7
ST RECTYPE
LIT 65535
RETURN
LABEL RESOLVEUSER
LIT 20480
PUSH
LD LOCALCOUNT
PUSH
INVOKE FIND 2
SETLOCAL 0
PUSH
LIT 65535
CNE
JNZ RESOLVEGOT
CALL LOOKGLOBAL
SETLOCAL 0
PUSH
LIT 65535
CNE
JNZ RESOLVEGOT
LIT 65535
ST RECVAL
LIT 0
ST RECLEVEL
LIT 4
CALL NEWGLOBAL
SETLOCAL 0
LIT 4
ST RECTYPE
LABEL RESOLVEGOT
LOCAL 0
RETURN
```

The following old source remains in place:

```ir
LABEL IOFAIL
LIT 1
```

### Edit 2

Unchanged source immediately before the edit:

```ir
PROC MAIN 0 0
LITS "PUTC"
CALL SETIDENT
```

Remove this source at old physical positions 37–38 in RB33.IR:

```ir
CALL BUILTIN
LD RECVAL
```

Replace it with:

```ir
LIT 1
ST RECTYPE
LIT 12345
ST RECVAL
LIT 0
ST RECLEVEL
LIT 0
PUSH
INVOKE RECORD 1
LIT 1
ST GLOBALS
CALL RESOLVEOPTIONAL
LD RECTYPE
```

The following old source remains in place:

```ir
PUSH
LIT 1
```

### Edit 3

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–35 in RB33.IR:

```ir
LITS "PUTC"
```

Replace it with:

```ir
LIT 22000
ALLOC
ST TABLE
LITS "ABC"
```

The following old source remains in place:

```ir
CALL SETIDENT
CALL BUILTIN
```

## Build this stopping point

```dos
COPY RB34.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000038664 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15811 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB34.COM
```

VIEW.BAS must report RB34.COM length 15811 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB34
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare RESOLVEOPTIONAL with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
