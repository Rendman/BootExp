+++
title = "RB38 \u00b7 Parentheses, strings, and unary values"
weight = 71
description = "A primary can emit a literal, string pointer, binding, addressed slot, indexed byte, or call."
download = "RB38.IR"
download_group = "toolchain"
+++

A primary can emit a literal, string pointer, binding, addressed slot, indexed byte, or call.

## The working parts

A primary can emit a literal, string pointer, binding, addressed slot, indexed byte, or call. Parentheses recurse through EXPR. Save binding metadata before scanning a nested expression, which can change the shared search fields.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB37.IR to RB38.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
CALL OUTNUM
CALL NEWLINE
CALL LEX
```

Insert after old physical line 1535.

Insert:

```ir
JMP PRIMARYDONE
LABEL PRIMARYSTRING
LITS "LITS "
CALL OUTSTR
ADDR STRING
CALL OUTSTR
CALL NEWLINE
CALL LEX
JMP PRIMARYDONE
LABEL PRIMARYPAREN
CALL LEX
LIT 1
PUSH
INVOKE EXPR 1
LIT 41
PUSH
INVOKE EXPECT 1
JMP PRIMARYDONE
LABEL PRIMARYNEG
CALL LEX
LIT 8
PUSH
INVOKE EXPR 1
LITS "NEG\r\n"
CALL OUTSTR
JMP PRIMARYDONE
LABEL PRIMARYNOT
CALL LEX
LIT 8
PUSH
INVOKE EXPR 1
LITS "NOT\r\n"
CALL OUTSTR
JMP PRIMARYDONE
LABEL PRIMARYBOOL
CALL LEX
LIT 8
PUSH
INVOKE EXPR 1
LITS "PUSH\r\nLIT 0\r\nCEQ\r\n"
CALL OUTSTR
JMP PRIMARYDONE
LABEL PRIMARYADDR
CALL LEX
LD TOK
PUSH
LIT 1
CNE
JNZ SYNTAX
CALL RESOLVE
LD RECTYPE
PUSH
LIT 1
CEQ
JNZ ADDRGLOBAL
LD RECTYPE
PUSH
LIT 2
CEQ
JNZ ADDRGLOBAL
LD RECTYPE
PUSH
LIT 5
CEQ
JNZ ADDRLOCAL
LD RECTYPE
PUSH
LIT 6
CNE
JNZ NAMEFAIL
LITS "PADDR "
JMP ADDRSLOT
LABEL ADDRLOCAL
LITS "LADDR "
LABEL ADDRSLOT
CALL OUTSTR
LD RECVAL
CALL OUTNUM
CALL NEWLINE
CALL LEX
JMP PRIMARYDONE
LABEL ADDRGLOBAL
LITS "ADDR V_"
CALL OUTSTR
LD FOUND
CALL OUTNAME
CALL NEWLINE
CALL LEX
LABEL PRIMARYDONE
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir
LIT 2
CNE
JNZ SYNTAX
```

Insert after old physical line 1529.

Insert:

```ir
JMP NAMEFAIL
LABEL PRIMARYNUM
```

The following old source remains in place:

```ir
LITS "LIT "
CALL OUTSTR
```

### Edit 3

Unchanged source immediately before the edit:

```ir
LD TOK
PUSH
LIT 2
```

Insert after old physical line 1527.

Insert:

```ir
CEQ
JNZ PRIMARYNUM
LD TOK
PUSH
LIT 3
CEQ
JNZ PRIMARYSTRING
LD TOK
PUSH
LIT 40
CEQ
JNZ PRIMARYPAREN
LD TOK
PUSH
LIT 45
CEQ
JNZ PRIMARYNEG
LD TOK
PUSH
LIT 126
CEQ
JNZ PRIMARYNOT
LD TOK
PUSH
LIT 33
CEQ
JNZ PRIMARYBOOL
LD TOK
PUSH
LIT 38
CEQ
JNZ PRIMARYADDR
LD TOK
PUSH
LIT 1
```

The following old source remains in place:

```ir
CNE
JNZ SYNTAX
```

### Edit 4

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Remove this source at old physical positions 1524–1524 in RB37.IR:

```ir
PROC PRIMARY 0 0
```

Replace it with:

```ir
PROC PRIMARY 0 4
```

The following old source remains in place:

```ir
LD TOK
PUSH
```

## Build this stopping point

```dos
COPY RB38.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000050537 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 17911 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB38.COM
```

VIEW.BAS must report RB38.COM length 17911 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB38.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
-(1+2)
```

```dos
COPY TRB38.RIL SOURCE.RIL
```

```dos
CHECK RB38
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
ADD
NEG
```

VIEW.BAS must show length 38 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRB38.RIL:

```rill
ABC
```

```dos
COPY XRB38.RIL SOURCE.RIL
CHECK RB38
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
