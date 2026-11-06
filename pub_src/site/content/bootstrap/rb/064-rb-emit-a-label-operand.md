+++
title = "31 \u00b7 Naming a Branch Destination"
weight = 31
description = "Emit a saved label number as an operand after the caller has selected the branch operation."
download = "RB31.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/064-rb-emit-a-label-operand/"]
reader_names = 1
+++

## The working parts

Emit a saved label number as an operand after the caller has selected the branch operation. Preserve that target across formatting calls.

## Enter the source

Copy RB30.IR to RB31.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 1005.

Insert:

```ir
PROC LABELJUMP 0 1
SETLOCAL 0
LITS " B_"
CALL OUTSTR
LOCAL 0
CALL OUTNUM
CALL NEWLINE
LIT 0
RETURN
```

The following old source remains in place:

```ir
PROC NEWLINE 0 0
LITS "\r\n"
```

### Edit 2

Unchanged source immediately before the edit:

```ir
LIT 1
ST OWN
LIT 7
```

Remove this source at old physical positions 43–43 in RB30.IR:

```ir
CALL LABELDEF
```

Replace it with:

```ir
CALL LABELJUMP
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

## Build this stopping point

```dos
COPY RB31.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000031651 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14853 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB31.COM
```

VIEW.BAS must report RB31.COM length 14853 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB31
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 10 bytes. The complete bytes must be:

```text
20 42 5F 30 30 30 30 37 0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare LABELJUMP with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
