+++
title = "26 \u00b7 Defining a Branch Destination"
weight = 26
description = "Build defining a branch destination.."
download = "R26.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/026-define-one-compiler-label/", "/bootstrap/rill/26-the-alternative-block/"]
url = "/bootstrap/rill/026-defining-a-branch-destination/"
+++

Build defining a branch destination..

## Enter the source

Copy R25.IR to R26.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 824

Unchanged source before the edit:

```ir
LD LABELNO
RETURN
```

Insert in its place:

```ir
PROC LABELDEF 0 1
SETLOCAL 0
LITS "LABEL B_"
CALL OUTSTR
LOCAL 0
CALL OUTNUM
CALL NEWLINE
LIT 0
RETURN
```

The following old source remains:

```ir
PROC NEWLINE 0 0
LITS "\r\n"
```

### Edit at old physical position 31

Unchanged source before the edit:

```ir
CALL NEWLABEL
PUSH
LIT 1
```

Remove:

```ir
CNE
```

Insert in its place:

```ir
ST OWN
LIT 7
CALL LABELDEF
CALL FLUSH
LD OUTPUT
CLOSE
LIT 0
ST OUTPUT
ST OWN
LIT 0
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 30

Unchanged source before the edit:

```ir
PROC MAIN 0 0
CALL NEWLABEL
PUSH
```

Insert in its place:

```ir
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
```

The following old source remains:

```ir
LIT 1
CNE
```

### Edit at old physical position 28

Unchanged source before the edit:

```ir
BUFFER OUTBUF 4096
BUFFER IDENT 32
PROC MAIN 0 0
```

Remove:

```ir
CALL NEWLABEL
```

Insert in its place:

```ir
LIT 1
```

The following old source remains:

```ir
PUSH
LIT 1
```

## Build and check

```dos
CHECK IRKEEP R26.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 14375 bytes`. Save RESULT.COM as R26.COM. VIEW.BAS must show length 14375.

```dos
CHECK R26 SOURCE.RIL RESULT.IR
```

Require PASS.

Inspect RESULT.IR with VIEW.BAS. Require length 15 bytes and these complete bytes:

```text
4C 41 42 45 4C 20 42 5F 30 30 30 30 37 0D 0A
```

This is a fragment for inspection, not a complete program. The command-selected RESULT.IR contains that fragment.

