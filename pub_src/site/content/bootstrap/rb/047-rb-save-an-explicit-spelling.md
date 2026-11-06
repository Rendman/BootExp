+++
title = "14 \u00b7 Copying a Name"
weight = 14
description = "Copy an explicit terminated spelling into IDENT."
download = "RB14.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/047-rb-save-an-explicit-spelling/"]
reader_names = 1
+++

## The working parts

Copy an explicit terminated spelling into IDENT. This is a table-test helper as well as a way to ask for a required entry without depending on the current source token.

## Enter the source

Copy RB13.IR to RB14.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 583.

Insert:

```ir
PROC SETIDENT 0 2
SETLOCAL 0
LIT 0
SETLOCAL 1
LABEL SETIDLOOP
ADDR IDENT
PUSH
LOCAL 1
ADD
PUSH
LOCAL 0
PUSH
LOCAL 1
ADD
FETCHB
PUTB
JZ SETIDDONE
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
JMP SETIDLOOP
LABEL SETIDDONE
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
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–42 in RB13.IR:

```ir
LITS "SOURCE.RIL"
OPEN
ST INPUT
STATUS
JNZ IOFAIL
CALL NEXT
CALL LEX
LITS "FN"
```

Replace it with:

```ir
LITS "ABC"
CALL SETIDENT
LIT 1
ST TOK
LITS "ABC"
```

The following old source remains in place:

```ir
CALL ISWORD
PUSH
```

## Build this stopping point

```dos
COPY RB14.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000022833 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13185 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB14.COM
```

VIEW.BAS must report RB14.COM length 13185 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB14
```

The checker must report PASS. The driver compares the result with ABC and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare SETIDENT with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
