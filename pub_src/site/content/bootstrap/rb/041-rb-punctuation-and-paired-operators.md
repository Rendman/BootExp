+++
title = "08 \u00b7 Reading Punctuation and Paired Operators"
weight = 8
description = "Keep source position, token kind, numeric value, and complete spelling distinct."
download = "RB08.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/041-rb-punctuation-and-paired-operators/"]
reader_names = 1
+++

## The working parts

Keep source position, token kind, numeric value, and complete spelling distinct. Save temporary values in local slots across NEXT calls. Paired punctuation is recognized before returning a single character; comments consume source without manufacturing a token.

## Enter the source

Copy RB07.IR to RB08.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
CUGT
JNZ LETTERNO
LIT 1
```

Insert after old physical line 184.

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
CALL NEXT
LD CH
PUSH
```

Remove this source at old physical positions 43–43 in RB07.IR:

```ir
LIT 65
```

Replace it with:

```ir
LIT 256
```

The following old source remains in place:

```ir
CNE
RETURN
```

### Edit 3

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
PUSH
LIT 65
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

Require IR86 `OK RESULT.ASM 0000017213 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 12084 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB08.COM
```

VIEW.BAS must report RB08.COM length 12084 bytes. Keep this executable and its source together.

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

The checker must report PASS. The driver compares the result with 256 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Check the token class, complete spelling, and numeric value separately. Preserve the raw quoted bytes while folding names.
