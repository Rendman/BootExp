+++
title = "30 \u00b7 Defining a Branch Destination"
weight = 30
description = "Emit LABEL, the reserved B_ prefix, and the saved number."
download = "RB30.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/063-rb-define-one-compiler-label/"]
reader_names = 1
+++

## The working parts

Emit LABEL, the reserved B_ prefix, and the saved number. Every definition ends with a record terminator.

## Enter the source

Copy RB29.IR to RB30.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LD LABELNO
RETURN
```

Insert after old physical line 983.

Insert:

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

The following old source remains in place:

```ir
PROC NEWLINE 0 0
LITS "\r\n"
```

### Edit 2

Unchanged source immediately before the edit:

```ir
CALL NEWLABEL
PUSH
LIT 1
```

Remove this source at old physical positions 38–38 in RB29.IR:

```ir
CNE
```

Replace it with:

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

The following old source remains in place:

```ir
RETURN
```

### Edit 3

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–36 in RB29.IR:

```ir
CALL NEWLABEL
PUSH
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
CNE
```

## Build this stopping point

```dos
COPY RB30.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000031359 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14803 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB30.COM
```

VIEW.BAS must report RB30.COM length 14803 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB30
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 15 bytes. The complete bytes must be:

```text
4C 41 42 45 4C 20 42 5F 30 30 30 30 37 0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare LABELDEF with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
