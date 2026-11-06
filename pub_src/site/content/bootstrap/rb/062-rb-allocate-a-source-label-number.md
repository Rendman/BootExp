+++
title = "29 \u00b7 Giving Each Branch a Unique Name"
weight = 29
description = "Advance a checked word counter."
download = "RB29.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/062-rb-allocate-a-source-label-number/"]
reader_names = 1
+++

## The working parts

Advance a checked word counter. The counter supplies names, not physical code addresses.

## Enter the source

Copy RB28.IR to RB29.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 984.

Insert:

```ir
PROC NEWLABEL 0 0
LD LABELNO
PUSH
LIT 1
ADD
ST LABELNO
JZ CAPFAIL
LD LABELNO
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
STATUS
JNZ IOFAIL
LIT 1
```

Remove this source at old physical positions 41–49 in RB28.IR:

```ir
ST OWN
CALL NEWLINE
CALL FLUSH
LD OUTPUT
CLOSE
LIT 0
ST OUTPUT
ST OWN
LIT 0
```

Replace it with:

```ir
CNE
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

Remove this source at old physical positions 35–39 in RB28.IR:

```ir
LITS "RILL.TMP"
CREATE
ST OUTPUT
STATUS
JNZ IOFAIL
```

Replace it with:

```ir
CALL NEWLABEL
PUSH
```

The following old source remains in place:

```ir
LIT 1
ST OWN
```

## Build this stopping point

```dos
COPY RB29.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000030713 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14692 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB29.COM
```

VIEW.BAS must report RB29.COM length 14692 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB29
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare NEWLABEL with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
