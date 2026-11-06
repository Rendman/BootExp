+++
title = "RB14 \u00b7 Save an explicit spelling"
weight = 14
description = "Copy an explicit terminated spelling into IDENT."
download = "RB14.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/047-rb-save-an-explicit-spelling/"]
+++

Copy an explicit terminated spelling into IDENT.

## The working parts

Copy an explicit terminated spelling into IDENT. This is a table-test helper as well as a way to ask for a required entry without depending on the current source token.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB13.IR to RB14.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 582.

Insert:

```ir
PROC SETIDENT 0 2
SETLOCAL 0
LIT 0
SETLOCAL 1
LABEL SETIDLOOP
ADDR IDENT
PUSH
LOCAL 1
ADD
PUSH
LOCAL 0
PUSH
LOCAL 1
ADD
FETCHB
PUTB
JZ SETIDDONE
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
JMP SETIDLOOP
LABEL SETIDDONE
LIT 0
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

Remove this source at old physical positions 35–44 in RB13.IR:

```ir
LITS "SOURCE.RIL"
OPEN
ST INPUT
STATUS
JNZ IOFAIL
CALL NEXT
CALL LEX
LITS "FN"
CALL ISWORD
CALL PRINTNUM
```

Replace it with:

```ir
LITS "ABC"
CALL SETIDENT
ADDR IDENT
CALL PRINT
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

## Build this stopping point

```dos
COPY RB14.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000022679 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13161 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB14.COM
```

VIEW.BAS must report RB14.COM length 13161 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB14
```

Require, apart from command echo and the checker's separator:

```text
ABCPASS
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
