+++
title = "37 \u00b7 Translating an Expression"
weight = 37
description = "Save the pending operator and precedence in local slots."
download = "RB37.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/070-rb-precedence-with-a-numeric-primary/"]
reader_names = 1
+++

## The working parts

Save the pending operator and precedence in local slots. Emit PUSH for the left operand, recurse at one higher minimum precedence for the right, then emit the operation. A bounded recursion counter prevents uncontrolled nesting.

## Enter the source

Copy RB36.IR to RB37.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LITS "CULT\r\n"
LABEL BINDONE
CALL OUTSTR
```

Insert after old physical line 1450.

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

Insert after old physical line 1326.

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

Require IR86 `OK RESULT.ASM 0000047030 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 17319 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB37.COM
```

VIEW.BAS must report RB37.COM length 17319 bytes. Keep this executable and its source together.

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

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 55 bytes. The complete bytes must be:

```text
4C 49 54 20 30 30 30 30 31 0D 0A 50 55 53 48 0D
0A 4C 49 54 20 30 30 30 30 32 0D 0A 50 55 53 48
0D 0A 4C 49 54 20 30 30 30 30 33 0D 0A 4D 55 4C
0D 0A 41 44 44 0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

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

Compare EXPR with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
