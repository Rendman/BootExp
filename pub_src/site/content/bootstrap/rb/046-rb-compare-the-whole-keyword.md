+++
title = "RB13 \u00b7 Compare the whole keyword"
weight = 13
description = "Check the token class and every character through the zero terminator."
download = "RB13.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/046-rb-compare-the-whole-keyword/"]
+++

Check the token class and every character through the zero terminator.

## The working parts

Check the token class and every character through the zero terminator. A keyword prefix is insufficient: FN and FNN are different spellings.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

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
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove this source at old physical positions 42–46 in RB12.IR:

```ir
LIT 43
PUSH
INVOKE EXPECT 1
LITS "OK"
CALL PRINT
```

Replace it with:

```ir
LITS "FN"
CALL ISWORD
CALL PRINTNUM
```

The following old source remains in place:

```ir
LIT 0
RETURN
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

Require IR86 `OK RESULT.ASM 0000022389 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13106 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB13.COM
```

VIEW.BAS must report RB13.COM length 13106 bytes. Keep this executable and its source together.

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

Require, apart from command echo and the checker's separator:

```text
00001PASS
```

## A rejection or boundary check

Rename SOURCE.RIL to an unused HOLD.RIL and run CHECK RB13. Restore the source afterward.

Require:

```text
ERROR 0000000001 CODE 00001
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
