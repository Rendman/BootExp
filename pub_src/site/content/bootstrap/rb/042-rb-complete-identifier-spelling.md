+++
title = "09 \u00b7 Reading Names Without Losing Letters"
weight = 9
description = "Keep source position, token kind, numeric value, and complete spelling distinct."
download = "RB09.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/042-rb-complete-identifier-spelling/"]
reader_names = 1
+++

## The working parts

Keep source position, token kind, numeric value, and complete spelling distinct. Save temporary values in local slots across NEXT calls. Paired punctuation is recognized before returning a single character; comments consume source without manufacturing a token.

## Enter the source

Copy RB08.IR to RB09.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
LABEL LEXNAME
```

Remove this source at old physical positions 327–327 in RB08.IR:

```ir
JMP SYNTAX
```

Replace it with:

```ir
LIT 0
SETLOCAL 0
LABEL NAMELOOP
LOCAL 0
PUSH
LIT 24
CUGE
JNZ NAMEFAIL
LD CH
SETLOCAL 1
PUSH
LIT 97
CULT
JNZ NAMESTORE
LOCAL 1
PUSH
LIT 122
CUGT
JNZ NAMESTORE
LOCAL 1
PUSH
LIT 32
SUB
SETLOCAL 1
LABEL NAMESTORE
ADDR IDENT
PUSH
LOCAL 0
ADD
PUSH
LOCAL 1
PUTB
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
CALL NEXT
LD CH
PUSH
INVOKE LETTER 1
JNZ NAMELOOP
LD CH
PUSH
INVOKE DIGIT 1
JNZ NAMELOOP
ADDR IDENT
PUSH
LOCAL 0
ADD
PUSH
LIT 0
PUTB
LIT 1
ST TOK
RETURN
```

The following old source remains in place:

```ir
LABEL LEXNUMBER
JMP SYNTAX
```

### Edit 2

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove this source at old physical positions 42–45 in RB08.IR:

```ir
LD TOK
PUSH
LIT 256
CNE
```

Replace it with:

```ir
ADDR IDENT
CALL PRINT
LIT 0
```

The following old source remains in place:

```ir
RETURN
```

## Build this stopping point

```dos
COPY RB09.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000018231 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 12287 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB09.COM
```

VIEW.BAS must report RB09.COM length 12287 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB09.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
hello
```

```dos
COPY TRB09.RIL SOURCE.RIL
```

```dos
CHECK RB09
```

Require:

```text
HELLO
PASS
```

## If the result differs

Check the token class, complete spelling, and numeric value separately. Preserve the raw quoted bytes while folding names.
