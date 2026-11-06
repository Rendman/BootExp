+++
title = "10 \u00b7 Reading Decimal Values"
weight = 10
description = "Keep source position, token kind, numeric value, and complete spelling distinct."
download = "RB10.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/043-rb-checked-decimal-words/"]
reader_names = 1
+++

## The working parts

Keep source position, token kind, numeric value, and complete spelling distinct. Save temporary values in local slots across NEXT calls. Paired punctuation is recognized before returning a single character; comments consume source without manufacturing a token.

## Enter the source

Copy RB09.IR to RB10.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
ST TOK
RETURN
LABEL LEXNUMBER
```

Remove this source at old physical positions 383–383 in RB09.IR:

```ir
JMP SYNTAX
```

Replace it with:

```ir
LIT 0
ST VALUE
LABEL NUMBERLOOP
LD VALUE
PUSH
LIT 6553
CUGT
JNZ NUMBERFAIL
LD VALUE
PUSH
LIT 6553
CNE
JNZ NUMBERCALC
LD CH
PUSH
LIT 53
CUGT
JNZ NUMBERFAIL
LABEL NUMBERCALC
LD VALUE
PUSH
LIT 10
MUL
PUSH
LD CH
ADD
PUSH
LIT 48
SUB
ST VALUE
CALL NEXT
LD CH
PUSH
INVOKE DIGIT 1
JNZ NUMBERLOOP
LIT 2
ST TOK
RETURN
```

The following old source remains in place:

```ir
LABEL LEXSTRING
JMP SYNTAX
```

### Edit 2

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove this source at old physical positions 42–44 in RB09.IR:

```ir
ADDR IDENT
CALL PRINT
LIT 0
```

Replace it with:

```ir
LD VALUE
PUSH
LIT 65535
CNE
```

The following old source remains in place:

```ir
RETURN
```

## Build this stopping point

```dos
COPY RB10.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000019012 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 12444 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB10.COM
```

VIEW.BAS must report RB10.COM length 12444 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB10.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
65535
```

```dos
COPY TRB10.RIL SOURCE.RIL
```

```dos
CHECK RB10
```

The checker must report PASS. The driver compares the result with 65535 and returns nonzero on a mismatch; it adds no display routine.

## A rejection or boundary check

Create XRB10.RIL:

```rill
65536
```

```dos
COPY XRB10.RIL SOURCE.RIL
CHECK RB10
```

Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the token class, complete spelling, and numeric value separately. Preserve the raw quoted bytes while folding names.
