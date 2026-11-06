+++
title = "RB37 \u00b7 Precedence with a numeric primary"
weight = 37
description = "Save the pending operator and precedence in local slots."
download = "RB37.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/070-rb-precedence-with-a-numeric-primary/"]
+++

Save the pending operator and precedence in local slots.

## The working parts

Save the pending operator and precedence in local slots. Emit PUSH for the left operand, recurse at one higher minimum precedence for the right, then emit the operation. A bounded recursion counter prevents uncontrolled nesting.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB36.IR to RB37.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LITS "CULT\r\n"
LABEL BINDONE
CALL OUTSTR
```

Insert after old physical line 1452.

Insert:

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

The following old source remains in place:

```ir
LIT 0
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir
LIT 7
RETURN
```

Insert after old physical line 1328.

Insert:

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

The following old source remains in place:

```ir
PROC BINARY 0 1
SETLOCAL 0
```

### Edit 3

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
LIT 1
ST OWN
```

Remove this source at old physical positions 42–43 in RB36.IR:

```ir
LIT 43
CALL BINARY
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
LIT 1
PUSH
INVOKE EXPR 1
LD TOK
JNZ SYNTAX
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

### Edit 4

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Insert after old physical line 34.

Insert:

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

The following old source remains in place:

```ir
LITS "RILL.TMP"
CREATE
```

## Build this stopping point

```dos
COPY RB37.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000047229 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 17342 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB37.COM
```

VIEW.BAS must report RB37.COM length 17342 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB37.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
1+2*3
```

```dos
COPY TRB37.RIL SOURCE.RIL
```

```dos
CHECK RB37
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
LIT 00001
PUSH
LIT 00002
PUSH
LIT 00003
MUL
ADD
```

VIEW.BAS must show length 55 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRB37.RIL:

```rill
(1)
```

```dos
COPY XRB37.RIL SOURCE.RIL
CHECK RB37
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
