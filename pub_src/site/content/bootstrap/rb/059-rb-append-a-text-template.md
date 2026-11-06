+++
title = "26 \u00b7 Writing Text Through the Buffer"
weight = 26
description = "Walk a terminated template while preserving its pointer."
download = "RB26.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/059-rb-append-a-text-template/"]
reader_names = 1
+++

## The working parts

Walk a terminated template while preserving its pointer. Normalize a bare LF in an IR template to CR/LF while retaining existing CR/LF. Quoted source escapes are still printable backslash spellings at this point.

## Enter the source

Copy RB25.IR to RB26.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 915.

Insert:

```ir
PROC OUTSTR 0 2
SETLOCAL 0
LIT 0
SETLOCAL 1
LABEL OUTSTRLOOP
LOCAL 0
FETCHB
JZ OUTSTRDONE
PUSH
LIT 10
CNE
JNZ OUTSTRBYTE
LOCAL 1
PUSH
LIT 13
CEQ
JNZ OUTSTRBYTE
LIT 13
CALL OUTCHAR
LABEL OUTSTRBYTE
LOCAL 0
FETCHB
SETLOCAL 1
CALL OUTCHAR
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
JMP OUTSTRLOOP
LABEL OUTSTRDONE
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
JNZ IOFAIL
LIT 1
ST OWN
```

Remove this source at old physical positions 42–43 in RB25.IR:

```ir
LIT 65
CALL OUTCHAR
```

Replace it with:

```ir
LITS "HI"
CALL OUTSTR
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

## Build this stopping point

```dos
COPY RB26.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000029850 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14523 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB26.COM
```

VIEW.BAS must report RB26.COM length 14523 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB26
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 2 bytes. The complete bytes must be:

```text
48 49
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare OUTSTR with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
