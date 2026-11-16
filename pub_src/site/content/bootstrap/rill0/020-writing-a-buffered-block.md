+++
title = "20 \u00b7 Writing a Buffered Block"
weight = 20
description = "Build writing a buffered block.."
download = "R20.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/020-write-a-nonempty-output-block/", "/bootstrap/rill/20-parenthesized-expressions/"]
url = "/bootstrap/rill/020-writing-a-buffered-block/"
+++

Build writing a buffered block..

## Enter the source

Copy R19.IR to R20.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 701

Unchanged source before the edit:

```ir
INVOKE RECORD 1
RETURN
```

Insert in its place:

```ir
PROC FLUSH 0 1
LD OUTLEN
JZ FLUSHDONE
LD OUTPUT
PUSH
ADDR OUTBUF
PUSH
LD OUTLEN
WRITE
SETLOCAL 0
STATUS
JNZ IOFAIL
LOCAL 0
PUSH
LD OUTLEN
CNE
JNZ IOFAIL
LIT 0
ST OUTLEN
LABEL FLUSHDONE
LIT 0
RETURN
```

The following old source remains:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit at old physical position 47

Unchanged source before the edit:

```ir
INVOKE FIND 2
LD RECVAL
PUSH
```

Remove:

```ir
LIT 12345
CNE
```

Insert in its place:

```ir
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
ADDR OUTBUF
PUSH
LIT 65
PUTB
LIT 1
ST OUTLEN
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

### Edit at old physical position 44

Unchanged source before the edit:

```ir
PUSH
LIT 1
PUSH
```

Remove:

```ir
INVOKE FIND 2
LD RECVAL
```

Insert in its place:

```ir
LITS "SOURCE.RIL"
```

The following old source remains:

```ir
PUSH
LIT 12345
```

### Edit at old physical position 24

Unchanged source before the edit:

```ir
BUFFER INBUF 4096
BUFFER IDENT 32
PROC MAIN 0 0
```

Remove:

```ir
LIT 22000
ALLOC
ST TABLE
LITS "ABC"
CALL SETIDENT
LIT 1
ST RECTYPE
LIT 12345
ST RECVAL
LIT 0
ST RECLEVEL
LIT 0
PUSH
INVOKE RECORD 1
LIT 1
ST GLOBALS
LIT 0
PUSH
```

The following old source remains:

```ir
LIT 1
PUSH
```

### Edit at old physical position 22

Unchanged source before the edit:

```ir
WORD RECLEVEL 0
BUFFER DECIMAL 10
BUFFER INBUF 4096
```

Insert in its place:

```ir
BUFFER OUTBUF 4096
```

The following old source remains:

```ir
BUFFER IDENT 32
PROC MAIN 0 0
```

### Edit at old physical position 14

Unchanged source before the edit:

```ir
WORD OUTPUT 0
WORD INPOS 0
WORD INLEN 0
```

Insert in its place:

```ir
WORD OUTLEN 0
```

The following old source remains:

```ir
WORD ENDED 0
WORD OWN 0
```

### Edit at old physical position 3

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
WORD TABLE 0
```

Remove:

```ir
WORD GLOBALS 0
```

The following old source remains:

```ir
WORD LOCALCOUNT 0
WORD TOK 0
```

## Build and check

```dos
CHECK IRKEEP R20.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 13814 bytes`. Save RESULT.COM as R20.COM. VIEW.BAS must show length 13814.

```dos
CHECK R20 SOURCE.RIL RESULT.IR
```

Require PASS.

Inspect RESULT.IR with VIEW.BAS. Require length 1 bytes and these complete bytes:

```text
41
```

This is a fragment for inspection, not a complete program. The command-selected RESULT.IR contains that fragment.

