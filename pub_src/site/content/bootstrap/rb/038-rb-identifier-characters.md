+++
title = "05 \u00b7 Recognizing Identifier Characters"
weight = 5
description = "Accept an underscore or a letter in either ASCII case."
download = "RB05.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/038-rb-identifier-characters/"]
reader_names = 1
+++

## The working parts

Accept an underscore or a letter in either ASCII case. The scanner performs case folding when saving a name; character recognition alone does not modify the source byte.

## Enter the source

Copy RB04.IR to RB05.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
PROC MAIN 0 0
LIT 2
PUSH
```

Remove this source at old physical positions 37–37 in RB04.IR:

```ir
INVOKE ERROR 1
```

Replace it with:

```ir
INVOKE LETTER 1
PUSH
LIT 1
CNE
RETURN

PROC LETTER 1 0
PARAM 0
PUSH
LIT 95
CEQ
JNZ LETTERYES
PARAM 0
PUSH
LIT 65
CULT
JNZ LETTERNO
PARAM 0
PUSH
LIT 90
CULE
JNZ LETTERYES
PARAM 0
PUSH
LIT 97
CULT
JNZ LETTERNO
PARAM 0
PUSH
LIT 122
CUGT
JNZ LETTERNO
LABEL LETTERYES
LIT 1
RETURN
LABEL LETTERNO
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–35 in RB04.IR:

```ir
LIT 2
```

Replace it with:

```ir
LIT 95
```

The following old source remains in place:

```ir
PUSH
INVOKE ERROR 1
```

## Build this stopping point

```dos
COPY RB05.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000011572 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 10937 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB05.COM
```

VIEW.BAS must report RB05.COM length 10937 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB05
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare LETTER with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
