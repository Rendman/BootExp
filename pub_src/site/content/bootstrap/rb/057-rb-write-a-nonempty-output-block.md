+++
title = "RB24 \u00b7 Write a nonempty output block"
weight = 24
description = "Write only a nonempty output block."
download = "RB24.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/057-rb-write-a-nonempty-output-block/"]
+++

Write only a nonempty output block.

## The working parts

Write only a nonempty output block. Check STATUS and the exact returned count before clearing OUTLEN. A zero-count DOS write is never used to flush or truncate the file.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB23.IR to RB24.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LD FOUND
RETURN
```

Insert after old physical line 859.

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
LIT 12345
ST RECVAL
LIT 0
```

Remove this source at old physical positions 45–53 in RB23.IR:

```ir
ST RECLEVEL
LIT 0
PUSH
INVOKE RECORD 1
LIT 1
ST GLOBALS
CALL RESOLVE
LD RECVAL
CALL PRINTNUM
```

Replace it with:

```ir
ST OUTPUT
ST OWN
LITS "OK RILL.TMP\r\n"
CALL PRINT
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

### Edit 3

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

### Edit 4

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

Require IR86 `OK RESULT.ASM 0000028568 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14271 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB24.COM
```

VIEW.BAS must report RB24.COM length 14271 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB24
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
A
```

VIEW.BAS must show length 1 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

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
