+++
title = "RB22 \u00b7 The global namespace"
weight = 55
description = "Restrict FIND to the active global entries."
download = "RB22.IR"
download_group = "toolchain"
+++

Restrict FIND to the active global entries.

## The working parts

Restrict FIND to the active global entries. A local shadow must not change how a procedure definition is found.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB21.IR to RB22.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
INVOKE RECORD 1
RETURN
```

Insert after old physical line 834.

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
CALL PRINTNUM
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

Require IR86 `OK RESULT.ASM 0000027324 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14040 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB22.COM
```

VIEW.BAS must report RB22.COM length 14040 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB22
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
