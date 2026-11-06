+++
title = "24 \u00b7 Writing a Buffered Block"
weight = 24
description = "Write only a nonempty output block."
download = "RB24.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/057-rb-write-a-nonempty-output-block/"]
reader_names = 1
+++

## The working parts

Write only a nonempty output block. Check STATUS and the exact returned count before clearing OUTLEN. A zero-count DOS write is never used to flush or truncate the file.

## Enter the source

Copy RB23.IR to RB24.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LD FOUND
RETURN
```

Insert after old physical line 860.

Insert:

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

The following old source remains in place:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit 2

Unchanged source immediately before the edit:

```ir
LIT 0
ST RECLEVEL
LIT 0
```

Remove this source at old physical positions 47–55 in RB23.IR:

```ir
PUSH
INVOKE RECORD 1
LIT 1
ST GLOBALS
CALL RESOLVE
LD RECVAL
PUSH
LIT 12345
CNE
```

There is no replacement source.

The following old source remains in place:

```ir
RETURN
```

### Edit 3

Unchanged source immediately before the edit:

```ir
LIT 12345
ST RECVAL
LIT 0
```

Remove this source at old physical positions 45–45 in RB23.IR:

```ir
ST RECLEVEL
```

Replace it with:

```ir
ST OUTPUT
ST OWN
```

The following old source remains in place:

```ir
LIT 0
PUSH
```

### Edit 4

Unchanged source immediately before the edit:

```ir
LITS "ABC"
CALL SETIDENT
LIT 1
```

Remove this source at old physical positions 41–43 in RB23.IR:

```ir
ST RECTYPE
LIT 12345
ST RECVAL
```

Replace it with:

```ir
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
```

The following old source remains in place:

```ir
LIT 0
ST RECLEVEL
```

### Edit 5

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–39 in RB23.IR:

```ir
LIT 22000
ALLOC
ST TABLE
LITS "ABC"
CALL SETIDENT
```

Replace it with:

```ir
LITS "RILL.TMP"
CREATE
ST OUTPUT
STATUS
JNZ IOFAIL
```

The following old source remains in place:

```ir
LIT 1
ST RECTYPE
```

## Build this stopping point

```dos
COPY RB24.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000028369 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14248 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB24.COM
```

VIEW.BAS must report RB24.COM length 14248 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB24
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 1 bytes. The complete bytes must be:

```text
41
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare FLUSH with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
