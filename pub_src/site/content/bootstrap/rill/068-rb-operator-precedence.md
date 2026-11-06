+++
title = "RB35 \u00b7 Operator precedence"
weight = 68
description = "Return a precedence number, with zero for a nonoperator."
download = "RB35.IR"
download_group = "toolchain"
+++

Return a precedence number, with zero for a nonoperator.

## The working parts

Return a precedence number, with zero for a nonoperator. Multiplication binds more tightly than addition; word comparisons and bit operators occupy explicitly defined lower levels.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB34.IR to RB35.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LOCAL 0
RETURN
```

Insert after old physical line 1225.

Insert:

```ir
PROC PREC 0 0
LD TOK
PUSH
LIT 124
CEQ
JNZ PRECONE
LD TOK
PUSH
LIT 94
CEQ
JNZ PRECTWO
LD TOK
PUSH
LIT 38
CEQ
JNZ PRECTHREE
LD TOK
PUSH
LIT 256
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 257
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 258
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 259
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 60
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 62
CEQ
JNZ PRECFOUR
LD TOK
PUSH
LIT 260
CEQ
JNZ PRECFIVE
LD TOK
PUSH
LIT 261
CEQ
JNZ PRECFIVE
LD TOK
PUSH
LIT 43
CEQ
JNZ PRECSIX
LD TOK
PUSH
LIT 45
CEQ
JNZ PRECSIX
LD TOK
PUSH
LIT 42
CEQ
JNZ PRECSEVEN
LD TOK
PUSH
LIT 47
CEQ
JNZ PRECSEVEN
LD TOK
PUSH
LIT 37
CEQ
JNZ PRECSEVEN
LIT 0
RETURN
LABEL PRECONE
LIT 1
RETURN
LABEL PRECTWO
LIT 2
RETURN
LABEL PRECTHREE
LIT 3
RETURN
LABEL PRECFOUR
LIT 4
RETURN
LABEL PRECFIVE
LIT 5
RETURN
LABEL PRECSIX
LIT 6
RETURN
LABEL PRECSEVEN
LIT 7
RETURN
```

The following old source remains in place:

```ir
LABEL IOFAIL
LIT 1
```

### Edit 2

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–52 in RB34.IR:

```ir
LIT 22000
ALLOC
ST TABLE
LITS "ABC"
CALL SETIDENT
LIT 1
ST RECTYPE
LIT 12345
ST RECVAL
LIT 0
ST RECLEVEL
LIT 0
PUSH
INVOKE RECORD 1
LIT 1
ST GLOBALS
CALL RESOLVEOPTIONAL
LD RECTYPE
```

Replace it with:

```ir
LITS "SOURCE.RIL"
OPEN
ST INPUT
STATUS
JNZ IOFAIL
CALL NEXT
CALL LEX
CALL PREC
```

The following old source remains in place:

```ir
CALL PRINTNUM
LIT 0
```

## Build this stopping point

```dos
COPY RB35.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000040899 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16269 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB35.COM
```

VIEW.BAS must report RB35.COM length 16269 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB35.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
*
```

```dos
COPY TRB35.RIL SOURCE.RIL
```

```dos
CHECK RB35
```

Require, apart from command echo and the checker's separator:

```text
00007PASS
```

## A rejection or boundary check

Rename SOURCE.RIL to an unused HOLD.RIL and run CHECK RB35. Restore the source afterward.

Require:

```text
ERROR 0000000001 CODE 00001
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
