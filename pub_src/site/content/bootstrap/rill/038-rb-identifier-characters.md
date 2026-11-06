+++
title = "RB05 \u00b7 Identifier characters"
weight = 38
description = "Accept an underscore or a letter in either ASCII case."
download = "RB05.IR"
download_group = "toolchain"
+++

Accept an underscore or a letter in either ASCII case.

## The working parts

Accept an underscore or a letter in either ASCII case. The scanner performs case folding when saving a name; character recognition alone does not modify the source byte.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB04.IR to RB05.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–36 in RB04.IR:

```ir
LITS "READY"
CALL PRINT
```

Replace it with:

```ir
LIT 95
PUSH
INVOKE LETTER 1
CALL PRINTNUM
LIT 0
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

## Build this stopping point

```dos
COPY RB05.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000011535 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 10930 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB05.COM
```

VIEW.BAS must report RB05.COM length 10930 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB05
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
