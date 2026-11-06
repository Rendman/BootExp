+++
title = "06 \u00b7 Recognizing Decimal Digits"
weight = 6
description = "The decimal range is exactly ASCII 48 through 57."
download = "RB06.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/039-rb-decimal-characters/"]
reader_names = 1
+++

## The working parts

The decimal range is exactly ASCII 48 through 57. Punctuation next to a digit is not another numeric digit.

## Enter the source

Copy RB05.IR to RB06.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
RETURN
LABEL LETTERNO
LIT 0
```

Insert after old physical line 73.

Insert:

```ir
RETURN

PROC DIGIT 1 0
PARAM 0
PUSH
LIT 48
CULT
JNZ LETTERNO
PARAM 0
PUSH
LIT 57
CUGT
JNZ LETTERNO
LIT 1
```

The following old source remains in place:

```ir
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir
PROC MAIN 0 0
LIT 95
PUSH
```

Remove this source at old physical positions 37–37 in RB05.IR:

```ir
INVOKE LETTER 1
```

Replace it with:

```ir
INVOKE DIGIT 1
```

The following old source remains in place:

```ir
PUSH
LIT 1
```

### Edit 3

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–35 in RB05.IR:

```ir
LIT 95
```

Replace it with:

```ir
LIT 57
```

The following old source remains in place:

```ir
PUSH
INVOKE LETTER 1
```

## Build this stopping point

```dos
COPY RB06.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000011933 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 11012 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB06.COM
```

VIEW.BAS must report RB06.COM length 11012 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB06
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare DIGIT with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
