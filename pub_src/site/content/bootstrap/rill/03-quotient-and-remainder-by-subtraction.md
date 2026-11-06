+++
title = "03 \u00b7 Quotient and remainder by subtraction"
weight = 3
description = "Compute an unsigned quotient using the operations already available."
download = "R03.IR"
download_group = "tools/rill0"
reader_names = 1
+++

Text formatting needs division, although the small IR vocabulary has no divide instruction.

## The working parts

DIVIDE takes the dividend in A and a nonzero divisor in STEP. It returns the remainder in A and leaves the quotient in COUNT. VALUE is its working remainder. Repeated subtraction stops when VALUE is less than STEP.

The comparison retains its right operand, so VALUE is reloaded before subtraction. Neither operands nor expression temporaries remain on the IR stack across calls. The test divides 16712 by 256 and displays quotient 65 as A. A zero divisor is outside this helper interface.

## Enter the source

Copy `R02.IR` to `R03.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL CHARDONE`

Unchanged source immediately before the edit:

```ir
EXIT
LABEL CHARDONE
RET
```

Insert after old physical line 16, before the following old line.

Insert this source:

```ir
; DIVIDE
LABEL DIVIDE
ST VALUE
LIT 0
ST COUNT
LABEL DIVLOOP
LD VALUE
PUSH
LD STEP
ULT DIVDONE
LD VALUE
PUSH
LD STEP
SUB
ST VALUE
LD COUNT
PUSH
LIT 1
ADD
ST COUNT
JMP DIVLOOP
LABEL DIVDONE
LD VALUE
RET
```

### Change 2: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
; Driver
LABEL MAIN
```

Remove these exact old lines (physical positions 3–5 in `R02.IR`):

```ir
LIT 72
CALL CHAR
LIT 73
```

Put this source in their place:

```ir
LIT 256
ST STEP
LIT 16712
CALL DIVIDE
LD COUNT
```

### Change 3: in the declarations

Insert after old physical line 0, before the following old line.

Insert this source:

```ir
; DATA
WORD VALUE 0
WORD STEP 0
WORD COUNT 0
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R03` at `IR source name:`. Require `OK R03.ASM 03199 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R03` at `Source name:`, and require `OK 00587 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Run `CHECK R03`. This checkpoint does not read SOURCE.RIL.

Apart from DOS command echo and the checker's separating blank line, require:

```text
APASS
```

This is a diagnostic stopping point. It does not create RESULT.IR.

## A rejection check

The program has no source-language reader at this stopping point. Check an IR transcription error independently: create BAD.IR with this text:

```ir
LABEL MAIN
PUTC EXTRA
```

Run CHECK IRKEEP and enter BAD. Require:

```text
IR ERROR 00002 CODE 1
FAIL
```

The unwanted operand must prevent BAD.ASM from being created. If an older BAD.ASM exists, it must remain unchanged.

An unexpected PASS is a failed rejection test.

## If the result differs

Check the IR literal values, operand order, and empty expression boundaries. Translate and assemble afresh; an older COM file can otherwise conceal a source error.
