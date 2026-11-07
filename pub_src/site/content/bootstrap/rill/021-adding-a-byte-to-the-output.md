+++
title = "21 \u00b7 Adding a Byte to the Output"
weight = 21
description = "Build adding a byte to the output.."
download = "R21.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/021-append-one-streamed-byte/", "/bootstrap/rill/21-unary-negation/"]
+++

Build adding a byte to the output..

## Enter the source

Copy R20.IR to R21.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 697

Unchanged source before the edit:

```ir
INVOKE RECORD 1
RETURN
```

Insert in its place:

```ir
PROC OUTCHAR 0 1
SETLOCAL 0
ADDR OUTBUF
PUSH
LD OUTLEN
ADD
PUSH
LOCAL 0
PUTB
LD OUTLEN
PUSH
LIT 1
ADD
ST OUTLEN
LD TOTAL
PUSH
LIT 1
ADD
ST TOTAL
JNZ OUTCOUNTGOOD
LD TOTALHI
PUSH
LIT 1
ADD
ST TOTALHI
JZ CAPFAIL
LABEL OUTCOUNTGOOD
LD OUTLEN
PUSH
LIT 4096
CNE
JNZ OUTCHARDONE
CALL FLUSH
LABEL OUTCHARDONE
LIT 0
RETURN
```

The following old source remains:

```ir
PROC FLUSH 0 1
LD OUTLEN
```

### Edit at old physical position 35

Unchanged source before the edit:

```ir
ADDR OUTBUF
PUSH
LIT 65
```

Remove:

```ir
PUTB
LIT 1
ST OUTLEN
```

Insert in its place:

```ir
CALL OUTCHAR
```

The following old source remains:

```ir
CALL FLUSH
LD OUTPUT
```

### Edit at old physical position 32

Unchanged source before the edit:

```ir
JNZ IOFAIL
LIT 1
ST OWN
```

Remove:

```ir
ADDR OUTBUF
PUSH
```

The following old source remains:

```ir
LIT 65
PUTB
```

### Edit at old physical position 14

Unchanged source before the edit:

```ir
WORD INPOS 0
WORD INLEN 0
WORD OUTLEN 0
```

Insert in its place:

```ir
WORD TOTAL 0
WORD TOTALHI 0
```

The following old source remains:

```ir
WORD ENDED 0
WORD OWN 0
```

## Build and check

```dos
COPY R21.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 13135 bytes`. Save RESULT.COM as R21.COM. VIEW.BAS must show length 13135.

```dos
CHECK R21
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 1 bytes and these complete bytes:

```text
41
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

