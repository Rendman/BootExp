+++
title = "25 \u00b7 Adding a Byte to the Output"
weight = 25
description = "Append one byte, advance the checked low/high output count, and flush a full 4096-byte block."
download = "RB25.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/058-rb-append-one-streamed-byte/"]
reader_names = 1
+++

## The working parts

Append one byte, advance the checked low/high output count, and flush a full 4096-byte block. The output belongs to this assembly, not to the input refill buffer.

## Enter the source

Copy RB24.IR to RB25.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LD FOUND
RETURN
```

Insert after old physical line 859.

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

Require IR86 `OK RESULT.ASM 0000029040 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14375 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB25.COM
```

VIEW.BAS must report RB25.COM length 14375 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB25
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 1 bytes. The complete bytes must be:

```text
41
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare OUTCHAR with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
