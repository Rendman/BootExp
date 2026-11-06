+++
title = "RB08 \u00b7 Punctuation and paired operators"
weight = 41
description = "Keep source position, token kind, numeric value, and complete spelling distinct."
download = "RB08.IR"
download_group = "toolchain"
+++

Keep source position, token kind, numeric value, and complete spelling distinct.

## The working parts

Keep source position, token kind, numeric value, and complete spelling distinct. Save temporary values in local slots across NEXT calls. Paired punctuation is recognized before returning a single character; comments consume source without manufacturing a token.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB07.IR to RB08.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
CUGT
JNZ LETTERNO
LIT 1
```

Insert after old physical line 183.

Insert:

```ir
RETURN

PROC LEX 0 4
LABEL LEXSTART
LD CH
JZ LEXEOF
PUSH
LIT 32
CULE
JZ LEXKIND
CALL NEXT
JMP LEXSTART
LABEL LEXKIND
LD CH
PUSH
INVOKE LETTER 1
JNZ LEXNAME
LD CH
PUSH
INVOKE DIGIT 1
JNZ LEXNUMBER
LD CH
PUSH
LIT 34
CEQ
JNZ LEXSTRING
LD CH
SETLOCAL 0
CALL NEXT
LOCAL 0
PUSH
LIT 47
CNE
JNZ LEXPAIR
LD CH
PUSH
LIT 47
CNE
JNZ LEXPAIR
LABEL LEXCOMMENT
LD CH
JZ LEXSTART
PUSH
LIT 10
CEQ
JNZ LEXSTART
CALL NEXT
JMP LEXCOMMENT
LABEL LEXPAIR
LOCAL 0
ST TOK
LOCAL 0
PUSH
LIT 61
CEQ
JNZ PAIREQUAL
LOCAL 0
PUSH
LIT 33
CEQ
JNZ PAIRNOTEQUAL
LOCAL 0
PUSH
LIT 60
CEQ
JNZ PAIRLESS
LOCAL 0
PUSH
LIT 62
CEQ
JNZ PAIRGREATER
LIT 0
RETURN
LABEL PAIREQUAL
LD CH
PUSH
LIT 61
CNE
JNZ LEXRETURN
LIT 256
ST TOK
CALL NEXT
LIT 0
RETURN
LABEL PAIRNOTEQUAL
LD CH
PUSH
LIT 61
CNE
JNZ LEXRETURN
LIT 257
ST TOK
CALL NEXT
LIT 0
RETURN
LABEL PAIRLESS
LD CH
PUSH
LIT 61
CNE
JNZ PAIRLEFTSHIFT
LIT 258
ST TOK
CALL NEXT
LIT 0
RETURN
LABEL PAIRLEFTSHIFT
LD CH
PUSH
LIT 60
CNE
JNZ LEXRETURN
LIT 260
ST TOK
CALL NEXT
LIT 0
RETURN
LABEL PAIRGREATER
LD CH
PUSH
LIT 61
CNE
JNZ PAIRRIGHTSHIFT
LIT 259
ST TOK
CALL NEXT
LIT 0
RETURN
LABEL PAIRRIGHTSHIFT
LD CH
PUSH
LIT 62
CNE
JNZ LEXRETURN
LIT 261
ST TOK
CALL NEXT
LABEL LEXRETURN
LIT 0
RETURN
LABEL LEXNAME
JMP SYNTAX
LABEL LEXNUMBER
JMP SYNTAX
LABEL LEXSTRING
JMP SYNTAX
LABEL LEXEOF
LIT 0
ST TOK
```

The following old source remains in place:

```ir
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir
STATUS
JNZ IOFAIL
CALL NEXT
```

Remove this source at old physical positions 41–41 in RB07.IR:

```ir
LD CH
```

Replace it with:

```ir
CALL LEX
LD TOK
```

The following old source remains in place:

```ir
CALL PRINTNUM
LIT 0
```

## Build this stopping point

```dos
COPY RB08.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000017176 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 12077 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB08.COM
```

VIEW.BAS must report RB08.COM length 12077 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB08.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
==
```

```dos
COPY TRB08.RIL SOURCE.RIL
```

```dos
CHECK RB08
```

Require, apart from command echo and the checker's separator:

```text
00256PASS
```

## A rejection or boundary check

Rename SOURCE.RIL to an unused HOLD.RIL and run CHECK RB08. Restore the source afterward.

Require:

```text
ERROR 0000000001 CODE 00001
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
