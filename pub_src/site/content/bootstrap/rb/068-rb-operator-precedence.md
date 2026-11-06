+++
title = "35 \u00b7 Making Multiplication Come First"
weight = 35
description = "Return a precedence number, with zero for a nonoperator."
download = "RB35.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/068-rb-operator-precedence/"]
reader_names = 1
+++

## The working parts

Return a precedence number, with zero for a nonoperator. Multiplication binds more tightly than addition; word comparisons and bit operators occupy explicitly defined lower levels.

## Enter the source

Copy RB34.IR to RB35.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LOCAL 0
RETURN
```

Insert after old physical line 1226.

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
ST RECLEVEL
LIT 0
PUSH
```

Remove this source at old physical positions 48–54 in RB34.IR:

```ir
INVOKE RECORD 1
LIT 1
ST GLOBALS
CALL RESOLVEOPTIONAL
LD RECTYPE
PUSH
LIT 1
```

Replace it with:

```ir
LIT 7
```

The following old source remains in place:

```ir
CNE
RETURN
```

### Edit 3

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–46 in RB34.IR:

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
PUSH
INVOKE RECORD 1
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

Require IR86 `OK RESULT.ASM 0000040936 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16276 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB35.COM
```

VIEW.BAS must report RB35.COM length 16276 bytes. Keep this executable and its source together.

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

The checker must report PASS. The driver compares the result with 7 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Check the token code against the returned precedence. Multiplication must rank above addition; a nonoperator returns zero.
