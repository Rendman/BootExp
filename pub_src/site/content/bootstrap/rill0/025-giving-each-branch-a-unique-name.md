+++
title = "25 \u00b7 Giving Each Branch a Unique Name"
weight = 25
description = "Build giving each branch a unique name.."
download = "R25.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/025-allocate-a-source-label-number/", "/bootstrap/rill/25-a-conditional-block/"]
url = "/bootstrap/rill/025-giving-each-branch-a-unique-name/"
+++

Build giving each branch a unique name..

## Enter the source

Copy R24.IR to R25.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 833

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC NEWLABEL 0 0
LD LABELNO
PUSH
LIT 1
ADD
ST LABELNO
JZ CAPFAIL
LD LABELNO
RETURN
```

The following old source remains:

```ir
PROC NEWLINE 0 0
LITS "\r\n"
```

### Edit at old physical position 28

Unchanged source before the edit:

```ir
BUFFER IDENT 32
PROC MAIN 0 0
LIT 1
```

Remove:

```ir
PUSH
LITS "SOURCE.RIL"
PUSH
INVOKE FILEARG 2
LIT 2
PUSH
LITS "RILL.TMP"
PUSH
INVOKE FILEARG 2
CREATE
ST OUTPUT
STATUS
JNZ IOFAIL
LIT 1
ST OWN
CALL NEWLINE
CALL FLUSH
LD OUTPUT
CLOSE
LIT 0
ST OUTPUT
ST OWN
LIT 0
```

Insert in its place:

```ir
CNE
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 27

Unchanged source before the edit:

```ir
BUFFER OUTBUF 4096
BUFFER IDENT 32
PROC MAIN 0 0
```

Insert in its place:

```ir
CALL NEWLABEL
PUSH
```

The following old source remains:

```ir
LIT 1
PUSH
```

### Edit at old physical position 16

Unchanged source before the edit:

```ir
WORD OUTLEN 0
WORD TOTAL 0
WORD TOTALHI 0
```

Insert in its place:

```ir
WORD LABELNO 0
```

The following old source remains:

```ir
WORD ENDED 0
WORD OWN 0
```

## Build and check

```dos
CHECK IRKEEP R25.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 14223 bytes`. Save RESULT.COM as R25.COM. VIEW.BAS must show length 14223.

```dos
CHECK R25
```

Require PASS.

The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

