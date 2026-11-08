+++
title = "32 \u00b7 Translating an Expression"
weight = 32
description = "Compile the left primary, save its value, and recurse at a higher minimum precedence for the right operand."
download = "R32.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/032-precedence-with-a-numeric-primary/", "/bootstrap/rill/32-programs/"]
url = "/bootstrap/rill/032-translating-an-expression/"
+++

Compile the left primary, save its value, and recurse at a higher minimum precedence for the right operand. Check recursion depth before nesting.

## Enter the source

Copy R31.IR to R32.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1149

Unchanged source before the edit:

```ir
LITS "CULT\r\n"
LABEL BINDONE
CALL OUTSTR
```

Insert in its place:

```ir
LIT 0
RETURN

PROC PRIMARY 0 0
LD TOK
PUSH
LIT 2
CNE
JNZ SYNTAX
LITS "LIT "
CALL OUTSTR
LD VALUE
CALL OUTNUM
CALL NEWLINE
CALL LEX
```

The following old source remains:

```ir
LIT 0
RETURN
```

### Edit at old physical position 1089

Unchanged source before the edit:

```ir
LIT 7
RETURN
```

Insert in its place:

```ir
PROC EXPR 1 2
LD EXPRDEPTH
PUSH
LIT 1
ADD
ST EXPRDEPTH
PUSH
LIT 16
CUGT
JNZ CAPFAIL
CALL PRIMARY
LABEL EXPRLOOP
CALL PREC
SETLOCAL 0
JZ EXPREND
PUSH
PARAM 0
CULT
JNZ EXPREND
LD TOK
SETLOCAL 1
LITS "PUSH\r\n"
CALL OUTSTR
CALL LEX
LOCAL 0
PUSH
LIT 1
ADD
PUSH
INVOKE EXPR 1
LOCAL 1
CALL BINARY
JMP EXPRLOOP
LABEL EXPREND
LD EXPRDEPTH
PUSH
LIT 1
SUB
ST EXPRDEPTH
LIT 0
RETURN
```

The following old source remains:

```ir
PROC BINARY 0 1
SETLOCAL 0
```

### Edit at old physical position 36

Unchanged source before the edit:

```ir
JNZ IOFAIL
LIT 1
ST OWN
```

Remove:

```ir
LIT 43
CALL BINARY
```

Insert in its place:

```ir
LITS "SOURCE.RIL"
OPEN
ST INPUT
STATUS
JNZ IOFAIL
CALL NEXT
CALL LEX
LIT 1
PUSH
INVOKE EXPR 1
LD TOK
JNZ SYNTAX
```

The following old source remains:

```ir
CALL FLUSH
LD OUTPUT
```

### Edit at old physical position 29

Unchanged source before the edit:

```ir
BUFFER IDENT 32
WORD CALLBUILTIN 0
PROC MAIN 0 0
```

Insert in its place:

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
```

The following old source remains:

```ir
LITS "RILL.TMP"
CREATE
```

### Edit at old physical position 28

Unchanged source before the edit:

```ir
BUFFER OUTBUF 4096
BUFFER IDENT 32
WORD CALLBUILTIN 0
```

Insert in its place:

```ir
WORD EXPRDEPTH 0
```

The following old source remains:

```ir
PROC MAIN 0 0
LITS "RILL.TMP"
```

### Edit at old physical position 3

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
WORD TABLE 0
```

Insert in its place:

```ir
WORD GLOBALS 0
```

The following old source remains:

```ir
WORD LOCALCOUNT 0
WORD TOK 0
```

## Build and check

```dos
COPY R32.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 15068 bytes`. Save RESULT.COM as R32.COM. VIEW.BAS must show length 15068.

Create T32.RIL:

```rill
1+2-3
```

```dos
COPY T32.RIL SOURCE.RIL
```

```dos
CHECK R32
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 55 bytes and these complete bytes:

```text
4C 49 54 20 30 30 30 30 31 0D 0A 50 55 53 48 0D
0A 4C 49 54 20 30 30 30 30 32 0D 0A 41 44 44 0D
0A 50 55 53 48 0D 0A 4C 49 54 20 30 30 30 30 33
0D 0A 53 55 42 0D 0A
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

## Check the new boundary

Use this separate rejected source:

```rill
(1)
```

Copy it to SOURCE.RIL and run CHECK R32. Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

