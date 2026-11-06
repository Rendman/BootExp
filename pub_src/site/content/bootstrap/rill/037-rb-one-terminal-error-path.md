+++
title = "RB04 \u00b7 One terminal error path"
weight = 37
description = "An error category is an explicit parameter."
download = "RB04.IR"
download_group = "toolchain"
+++

An error category is an explicit parameter.

## The working parts

An error category is an explicit parameter. Input, output, temporary ownership, and backup state have separate meanings. Cleanup may close or delete owned files, but an older accepted RESULT.IR is not scratch storage.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB03.IR to RB04.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
EXIT

PROC ERROR 1 0
```

Insert after old physical line 116.

Insert:

```ir
LD INPUT
JZ ERROROUT
CLOSE
LABEL ERROROUT
LD OUTPUT
JZ ERRORTEMP
CLOSE
LABEL ERRORTEMP
LD BACKUP
JZ ERRORDELETE
LITS "RILL.BAK"
PUSH
LITS "RESULT.IR"
RENAME
STATUS
JNZ ERRORREPORT
LABEL ERRORDELETE
LD OWN
JZ ERRORREPORT
LITS "RILL.TMP"
DELETE
LABEL ERRORREPORT
LD TABLE
JZ ERRORDISPLAY
FREEBLOCK
LABEL ERRORDISPLAY
LITS "ERROR "
CALL PRINT
LD LINEHI
PUSH
LD LINE
PUSH
INVOKE PRINT32 2
LITS " CODE "
CALL PRINT
PARAM 0
CALL PRINTNUM
LITS "\r\n"
CALL PRINT
```

The following old source remains in place:

```ir
LIT 1
EXIT
```

### Edit 2

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–39 in RB03.IR:

```ir
LIT 1
PUSH
LIT 1
PUSH
INVOKE PRINT32 2
```

Replace it with:

```ir
LITS "READY"
CALL PRINT
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

## Build this stopping point

```dos
COPY RB04.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000010790 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 10771 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB04.COM
```

VIEW.BAS must report RB04.COM length 10771 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB04
```

Require, apart from command echo and the checker's separator:

```text
READYPASS
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
