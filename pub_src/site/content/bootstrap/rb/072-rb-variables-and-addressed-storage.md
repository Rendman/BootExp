+++
title = "RB39 \u00b7 Variables and addressed storage"
weight = 39
description = "A primary can emit a literal, string pointer, binding, addressed slot, indexed byte, or call."
download = "RB39.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/072-rb-variables-and-addressed-storage/"]
+++

A primary can emit a literal, string pointer, binding, addressed slot, indexed byte, or call.

## The working parts

A primary can emit a literal, string pointer, binding, addressed slot, indexed byte, or call. Parentheses recurse through EXPR. Save binding metadata before scanning a nested expression, which can change the shared search fields.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB38.IR to RB39.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
CNE
JNZ SYNTAX
JMP NAMEFAIL
```

Insert after old physical line 1565.

Insert:

```ir
LABEL PRIMARYGLOBAL
LITS "LD V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
CALL NEWLINE
JMP PRIMARYDONE
LABEL PRIMARYLOCAL
LITS "LOCAL "
CALL OUTSTR
LOCAL 2
CALL OUTNUM
CALL NEWLINE
JMP PRIMARYDONE
LABEL PRIMARYPARAM
LITS "PARAM "
CALL OUTSTR
LOCAL 2
CALL OUTNUM
CALL NEWLINE
JMP PRIMARYDONE
LABEL PRIMARYBUFFER
LITS "ADDR V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
CALL NEWLINE
LD TOK
PUSH
LIT 91
CNE
JNZ PRIMARYDONE
LITS "PUSH\r\n"
CALL OUTSTR
CALL LEX
LIT 1
PUSH
INVOKE EXPR 1
LIT 93
PUSH
INVOKE EXPECT 1
LITS "ADD\r\nFETCHB\r\n"
CALL OUTSTR
JMP PRIMARYDONE
LABEL PRIMARYCALL
LOCAL 0
PUSH
LOCAL 3
PUSH
INVOKE CALLARGS 2
JMP PRIMARYDONE
```

The following old source remains in place:

```ir
LABEL PRIMARYNUM
LITS "LIT "
```

### Edit 2

Unchanged source immediately before the edit:

```ir
LIT 1
CNE
JNZ SYNTAX
```

Insert after old physical line 1564.

Insert:

```ir
CALL RESOLVEOPTIONAL
SETLOCAL 0
LD RECTYPE
SETLOCAL 1
LD RECVAL
SETLOCAL 2
LD CALLBUILTIN
SETLOCAL 3
CALL LEX
LD TOK
PUSH
LIT 40
CEQ
JNZ PRIMARYCALL
LOCAL 1
PUSH
LIT 1
CEQ
JNZ PRIMARYGLOBAL
LOCAL 1
PUSH
LIT 2
CEQ
JNZ PRIMARYBUFFER
LOCAL 1
PUSH
LIT 5
CEQ
JNZ PRIMARYLOCAL
LOCAL 1
PUSH
LIT 6
CEQ
JNZ PRIMARYPARAM
```

The following old source remains in place:

```ir
JMP NAMEFAIL
LABEL PRIMARYNUM
```

### Edit 3

Unchanged source immediately before the edit:

```ir
LOCAL 0
RETURN
```

Insert after old physical line 1249.

Insert:

```ir
PROC CALLARGS 2 0
LIT 2
PUSH
INVOKE ERROR 1
LIT 0
RETURN
```

The following old source remains in place:

```ir
PROC PREC 0 0
LD TOK
```

## Build this stopping point

```dos
COPY RB39.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000053067 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 18335 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB39.COM
```

VIEW.BAS must report RB39.COM length 18335 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB39.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
ABC+1
```

```dos
COPY TRB39.RIL SOURCE.RIL
```

```dos
CHECK RB39
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
LD V_ABC
PUSH
LIT 00001
ADD
```

VIEW.BAS must show length 32 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRB39.RIL:

```rill
UNKNOWN
```

```dos
COPY XRB39.RIL SOURCE.RIL
CHECK RB39
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
