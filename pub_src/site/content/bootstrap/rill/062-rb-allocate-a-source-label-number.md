+++
title = "RB29 \u00b7 Allocate a source label number"
weight = 62
description = "Advance a checked word counter."
download = "RB29.IR"
download_group = "toolchain"
+++

Advance a checked word counter.

## The working parts

Advance a checked word counter. The counter supplies names, not physical code addresses.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB28.IR to RB29.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 986.

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
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–50 in RB28.IR:

```ir
LITS "RILL.TMP"
CREATE
ST OUTPUT
STATUS
JNZ IOFAIL
LIT 1
ST OWN
CALL NEWLINE
CALL FLUSH
LD OUTPUT
CLOSE
LIT 0
ST OUTPUT
ST OWN
LITS "OK RILL.TMP\r\n"
CALL PRINT
```

Replace it with:

```ir
CALL NEWLABEL
CALL PRINTNUM
```

The following old source remains in place:

```ir
LIT 0
RETURN
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

Require IR86 `OK RESULT.ASM 0000030676 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14685 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB29.COM
```

VIEW.BAS must report RB29.COM length 14685 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB29
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
