+++
title = "RB20 \u00b7 A separate local-name region"
weight = 20
description = "Append a record in the separate local-name region."
download = "RB20.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/053-rb-a-separate-local-name-region/"]
+++

Append a record in the separate local-name region.

## The working parts

Append a record in the separate local-name region. Its slot number and lexical level are explicit fields. The region has room for parameters and live local bindings, not a second global namespace.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB19.IR to RB20.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
INVOKE RECORD 1
RETURN
```

Insert after old physical line 731.

Insert:

```ir
PROC NEWLOCAL 0 1
ST RECTYPE
LD LOCALCOUNT
PUSH
LIT 32
CUGE
JNZ CAPFAIL
LD LOCALCOUNT
PUSH
LIT 40
MUL
PUSH
LIT 20480
ADD
SETLOCAL 0
LD LOCALCOUNT
PUSH
LIT 1
ADD
ST LOCALCOUNT
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
CALL SETIDENT
LIT 12345
ST RECVAL
```

Remove this source at old physical positions 42–44 in RB19.IR:

```ir
LIT 1
CALL NEWGLOBAL
LIT 34
```

Replace it with:

```ir
LIT 5
CALL NEWLOCAL
LIT 20514
```

The following old source remains in place:

```ir
CALL TWORD
CALL PRINTNUM
```

### Edit 3

Unchanged source immediately before the edit:

```ir
ST TABLE
LITS "ABC"
CALL SETIDENT
```

Remove this source at old physical positions 40–40 in RB19.IR:

```ir
LIT 12345
```

Replace it with:

```ir
LIT 7
```

The following old source remains in place:

```ir
ST RECVAL
LIT 1
```

## Build this stopping point

```dos
COPY RB20.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000025771 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13746 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB20.COM
```

VIEW.BAS must report RB20.COM length 13746 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB20
```

Require, apart from command echo and the checker's separator:

```text
00007PASS
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
