+++
title = "04 \u00b7 Reporting an Error"
weight = 4
description = "Close owned handles and free owned workspace before reporting the line and error category."
download = "R04.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/004-one-terminal-error-path/", "/bootstrap/rill/04-two-characters-in-a-word/"]
url = "/bootstrap/rill/004-reporting-an-error/"
+++

Close owned handles and free owned workspace before reporting the line and error category. Retain recovery files if restoring accepted output fails.

## Enter the source

Copy R03.IR to R04.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 64

Unchanged source before the edit:

```ir
JNZ PRINTPLACE
LIT 0
RETURN
```

Insert in its place:

```ir

LABEL IOFAIL
LIT 1
JMP FAIL
LABEL SYNTAX
LIT 2
JMP FAIL
LABEL NUMBERFAIL
LIT 3
JMP FAIL
LABEL NAMEFAIL
LIT 4
JMP FAIL
LABEL CAPFAIL
LIT 5
LABEL FAIL
PUSH
INVOKE ERROR 1
LIT 1
EXIT
PROC ERROR 1 0
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
LIT 1
EXIT
```

The following old source remains:

```ir

PROC PRINT32 2 8
```

### Edit at old physical position 6

Unchanged source before the edit:

```ir
PROC MAIN 0 0
LIT 1
PUSH
```

Remove:

```ir
LIT 1
PUSH
INVOKE PRINT32 2
```

Insert in its place:

```ir
INVOKE ERROR 1
```

The following old source remains:

```ir
LIT 0
RETURN
```

### Edit at old physical position 4

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
BUFFER DECIMAL 10
PROC MAIN 0 0
```

Remove:

```ir
LIT 1
```

Insert in its place:

```ir
LIT 2
```

The following old source remains:

```ir
PUSH
LIT 1
```

### Edit at old physical position 2

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
```

Insert in its place:

```ir
WORD TABLE 0
WORD LINE 1
WORD LINEHI 0
WORD INPUT 0
WORD OUTPUT 0
WORD OWN 0
WORD BACKUP 0
```

The following old source remains:

```ir
BUFFER DECIMAL 10
PROC MAIN 0 0
```

## Build and check

```dos
COPY R04.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 01943 bytes`. Save RESULT.COM as R04.COM. VIEW.BAS must show length 1943.

```dos
CHECK R04
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

The error routine deliberately exits nonzero; its diagnostic and FAIL are the intended result.

