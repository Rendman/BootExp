+++
title = "RB10 \u00b7 Checked decimal words"
weight = 43
description = "Keep source position, token kind, numeric value, and complete spelling distinct."
download = "RB10.IR"
download_group = "toolchain"
+++

Keep source position, token kind, numeric value, and complete spelling distinct.

## The working parts

Keep source position, token kind, numeric value, and complete spelling distinct. Save temporary values in local slots across NEXT calls. Paired punctuation is recognized before returning a single character; comments consume source without manufacturing a token.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

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

Remove this source at old physical positions 42–43 in RB09.IR:

```ir
ADDR IDENT
CALL PRINT
```

Replace it with:

```ir
LD VALUE
CALL PRINTNUM
```

The following old source remains in place:

```ir
LIT 0
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

Require IR86 `OK RESULT.ASM 0000018975 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 12437 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB10.COM
```

VIEW.BAS must report RB10.COM length 12437 bytes. Keep this executable and its source together.

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

Require, apart from command echo and the checker's separator:

```text
65535PASS
```

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

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
