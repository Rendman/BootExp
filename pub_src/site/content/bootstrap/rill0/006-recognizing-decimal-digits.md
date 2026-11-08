+++
title = "06 \u00b7 Recognizing Decimal Digits"
weight = 6
description = "Build recognizing decimal digits.."
download = "R06.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/006-decimal-characters/", "/bootstrap/rill/06-one-visible-error-report/"]
url = "/bootstrap/rill/006-recognizing-decimal-digits/"
+++

Build recognizing decimal digits..

## Enter the source

Copy R05.IR to R06.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 50

Unchanged source before the edit:

```ir
RETURN
LABEL LETTERNO
LIT 0
```

Insert in its place:

```ir
RETURN

PROC DIGIT 1 0
PARAM 0
PUSH
LIT 48
CULT
JNZ LETTERNO
PARAM 0
PUSH
LIT 57
CUGT
JNZ LETTERNO
LIT 1
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 13

Unchanged source before the edit:

```ir
PROC MAIN 0 0
LIT 95
PUSH
```

Remove:

```ir
INVOKE LETTER 1
```

Insert in its place:

```ir
INVOKE DIGIT 1
```

The following old source remains:

```ir
PUSH
LIT 1
```

### Edit at old physical position 11

Unchanged source before the edit:

```ir
WORD BACKUP 0
BUFFER DECIMAL 10
PROC MAIN 0 0
```

Remove:

```ir
LIT 95
```

Insert in its place:

```ir
LIT 57
```

The following old source remains:

```ir
PUSH
INVOKE LETTER 1
```

## Build and check

```dos
COPY R06.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 02188 bytes`. Save RESULT.COM as R06.COM. VIEW.BAS must show length 2188.

```dos
CHECK R06
```

Require PASS.

The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

