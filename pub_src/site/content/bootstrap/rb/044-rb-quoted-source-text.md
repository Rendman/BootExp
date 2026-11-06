+++
title = "RB11 \u00b7 Quoted source text"
weight = 11
description = "Keep source position, token kind, numeric value, and complete spelling distinct."
download = "RB11.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/044-rb-quoted-source-text/"]
+++

Keep source position, token kind, numeric value, and complete spelling distinct.

## The working parts

Keep source position, token kind, numeric value, and complete spelling distinct. Save temporary values in local slots across NEXT calls. Paired punctuation is recognized before returning a single character; comments consume source without manufacturing a token.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB10.IR to RB11.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
ST TOK
RETURN
LABEL LEXSTRING
```

Remove this source at old physical positions 422–422 in RB10.IR:

```ir
JMP SYNTAX
```

Replace it with:

```ir
LIT 0
SETLOCAL 0
LIT 0
SETLOCAL 1
LABEL STRINGLOOP
LD CH
PUSH
LIT 10
CEQ
JNZ SYNTAX
LD CH
PUSH
LIT 13
CEQ
JNZ SYNTAX
LOCAL 0
PUSH
LIT 510
CUGE
JNZ CAPFAIL
LD CH
JZ SYNTAX
ADDR STRING
PUSH
LOCAL 0
ADD
PUSH
LD CH
PUTB
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
LD CH
SETLOCAL 2
CALL NEXT
LOCAL 0
PUSH
LIT 1
CEQ
JNZ STRINGLOOP
LOCAL 1
JNZ STRINGESCAPED
LOCAL 2
PUSH
LIT 34
CEQ
JNZ STRINGDONE
LOCAL 2
PUSH
LIT 92
CNE
JNZ STRINGLOOP
LIT 1
SETLOCAL 1
JMP STRINGLOOP
LABEL STRINGESCAPED
LOCAL 2
PUSH
LIT 110
CEQ
JNZ STRINGESCAPEGOOD
LOCAL 2
PUSH
LIT 114
CEQ
JNZ STRINGESCAPEGOOD
LOCAL 2
PUSH
LIT 116
CEQ
JNZ STRINGESCAPEGOOD
LOCAL 2
PUSH
LIT 48
CEQ
JNZ STRINGESCAPEGOOD
LOCAL 2
PUSH
LIT 92
CEQ
JNZ STRINGESCAPEGOOD
LOCAL 2
PUSH
LIT 34
CNE
JNZ SYNTAX
LABEL STRINGESCAPEGOOD
LIT 0
SETLOCAL 1
JMP STRINGLOOP
LABEL STRINGDONE
ADDR STRING
PUSH
LOCAL 0
ADD
PUSH
LIT 0
PUTB
LIT 3
ST TOK
RETURN
```

The following old source remains in place:

```ir
LABEL LEXEOF
LIT 0
```

### Edit 2

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove this source at old physical positions 42–43 in RB10.IR:

```ir
LD VALUE
CALL PRINTNUM
```

Replace it with:

```ir
ADDR STRING
CALL PRINT
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

## Build this stopping point

```dos
COPY RB11.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000021190 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 12879 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB11.COM
```

VIEW.BAS must report RB11.COM length 12879 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB11.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
"Hi"
```

```dos
COPY TRB11.RIL SOURCE.RIL
```

```dos
CHECK RB11
```

Require, apart from command echo and the checker's separator:

```text
"Hi"PASS
```

## A rejection or boundary check

Create XRB11.RIL:

```rill
"open
```

```dos
COPY XRB11.RIL SOURCE.RIL
CHECK RB11
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
