+++
title = "RB06 \u00b7 Decimal characters"
weight = 6
description = "The decimal range is exactly ASCII 48 through 57."
download = "RB06.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/039-rb-decimal-characters/"]
+++

The decimal range is exactly ASCII 48 through 57.

## The working parts

The decimal range is exactly ASCII 48 through 57. Punctuation next to a digit is not another numeric digit.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB05.IR to RB06.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
RETURN
LABEL LETTERNO
LIT 0
```

Insert after old physical line 72.

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
CALL PRINTNUM
LIT 0
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

Require IR86 `OK RESULT.ASM 0000011896 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 11005 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB06.COM
```

VIEW.BAS must report RB06.COM length 11005 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB06
```

Require, apart from command echo and the checker's separator:

```text
00001PASS
```

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
