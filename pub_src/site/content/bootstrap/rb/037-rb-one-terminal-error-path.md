+++
title = "04 \u00b7 Reporting an Error"
weight = 4
description = "An error category is an explicit parameter."
download = "RB04.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/037-rb-one-terminal-error-path/"]
reader_names = 1
+++

## The working parts

An error category is an explicit parameter. Input, output, temporary ownership, and backup state have separate meanings. Cleanup may close or delete owned files, but an older accepted RESULT.IR is not scratch storage.

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
PROC MAIN 0 0
LIT 1
PUSH
```

Remove this source at old physical positions 37–39 in RB03.IR:

```ir
LIT 1
PUSH
INVOKE PRINT32 2
```

Replace it with:

```ir
INVOKE ERROR 1
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

### Edit 3

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–35 in RB03.IR:

```ir
LIT 1
```

Replace it with:

```ir
LIT 2
```

The following old source remains in place:

```ir
PUSH
LIT 1
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

Require IR86 `OK RESULT.ASM 0000010722 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 10767 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB04.COM
```

VIEW.BAS must report RB04.COM length 10767 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB04
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

FAIL is the intended status here: the routine being tested reports an error and terminates with status one.

## If the result differs

Check owned handles and recovery files before the final error report.
