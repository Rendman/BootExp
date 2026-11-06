+++
title = "RB25 \u00b7 Append one streamed byte"
weight = 25
description = "Append one byte, advance the checked low/high output count, and flush a full 4096-byte block."
download = "RB25.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/058-rb-append-one-streamed-byte/"]
+++

Append one byte, advance the checked low/high output count, and flush a full 4096-byte block.

## The working parts

Append one byte, advance the checked low/high output count, and flush a full 4096-byte block. The output belongs to this assembly, not to the input refill buffer.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB24.IR to RB25.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LD FOUND
RETURN
```

Insert after old physical line 861.

Insert:

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

The following old source remains in place:

```ir
PROC FLUSH 0 1
LD OUTLEN
```

### Edit 2

Unchanged source immediately before the edit:

```ir
ADDR OUTBUF
PUSH
LIT 65
```

Remove this source at old physical positions 45–47 in RB24.IR:

```ir
PUTB
LIT 1
ST OUTLEN
```

Replace it with:

```ir
CALL OUTCHAR
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

### Edit 3

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
LIT 1
ST OWN
```

Remove this source at old physical positions 42–43 in RB24.IR:

```ir
ADDR OUTBUF
PUSH
```

There is no replacement source.

The following old source remains in place:

```ir
LIT 65
PUTB
```

## Build this stopping point

```dos
COPY RB25.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000029239 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14398 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB25.COM
```

VIEW.BAS must report RB25.COM length 14398 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB25
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
