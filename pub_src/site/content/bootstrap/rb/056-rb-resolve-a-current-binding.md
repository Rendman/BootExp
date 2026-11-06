+++
title = "RB23 \u00b7 Resolve a current binding"
weight = 23
description = "Search active local bindings first, then globals."
download = "RB23.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/056-rb-resolve-a-current-binding/"]
+++

Search active local bindings first, then globals.

## The working parts

Search active local bindings first, then globals. Save the found offset separately from kind and value fields; recursive parsing can replace the shared search result.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB22.IR to RB23.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
INVOKE FIND 2
RETURN
```

Insert after old physical line 838.

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
CALL PRINTNUM
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

Require IR86 `OK RESULT.ASM 0000027800 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14135 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB23.COM
```

VIEW.BAS must report RB23.COM length 14135 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB23
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
