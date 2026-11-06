+++
title = "13 \u00b7 Recognizing a Complete Keyword"
weight = 13
description = "Check the token class and every character through the zero terminator."
download = "RB13.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/046-rb-compare-the-whole-keyword/"]
reader_names = 1
+++

## The working parts

Check the token class and every character through the zero terminator. A keyword prefix is insufficient: FN and FNN are different spellings.

## Enter the source

Copy RB12.IR to RB13.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 542.

Insert:

```ir
PROC ISWORD 0 2
SETLOCAL 0
LD TOK
PUSH
LIT 1
CNE
JNZ WORDNO
LIT 0
SETLOCAL 1
LABEL WORDLOOP
ADDR IDENT
PUSH
LOCAL 1
ADD
FETCHB
PUSH
LOCAL 0
PUSH
LOCAL 1
ADD
FETCHB
CNE
JNZ WORDNO
ADDR IDENT
PUSH
LOCAL 1
ADD
FETCHB
JZ WORDYES
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
JMP WORDLOOP
LABEL WORDYES
LIT 1
RETURN
LABEL WORDNO
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
CALL LEX
LIT 43
PUSH
```

Remove this source at old physical positions 44–47 in RB12.IR:

```ir
INVOKE EXPECT 1
LITS "OK"
CALL PRINT
LIT 0
```

Replace it with:

```ir
LIT 1
CNE
```

The following old source remains in place:

```ir
RETURN
```

### Edit 3

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove this source at old physical positions 42–42 in RB12.IR:

```ir
LIT 43
```

Replace it with:

```ir
LITS "FN"
CALL ISWORD
```

The following old source remains in place:

```ir
PUSH
INVOKE EXPECT 1
```

## Build this stopping point

```dos
COPY RB13.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000022426 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13113 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB13.COM
```

VIEW.BAS must report RB13.COM length 13113 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB13.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
fn
```

```dos
COPY TRB13.RIL SOURCE.RIL
```

```dos
CHECK RB13
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare ISWORD with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
