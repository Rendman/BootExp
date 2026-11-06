+++
title = "04 \u00b7 Two characters in a word"
weight = 4
description = "Print compact text constants and an explicit line ending."
download = "R04.IR"
download_group = "tools/rill0"
reader_names = 1
+++

Fixed messages occur often enough to benefit from one compact representation.

## The working parts

PAIR receives two nonzero ASCII bytes packed low byte first in A. It stores the original in WORK, masks the low byte with 255, and sends it to CHAR. DIVIDE with divisor 256 obtains the high byte. PAIR then transfers to CHAR, whose return completes the original call.

An unpaired final character uses CHAR directly. NEWLINE supplies 2573, whose bytes are 13 and 10. This is a source-data convention using IR arithmetic; it does not depend on a processor register layout. PAIR changes WORK, STEP, VALUE, COUNT, and A.

## Enter the source

Copy `R03.IR` to `R04.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL DIVDONE`

Unchanged source immediately before the edit:

```ir
LABEL DIVDONE
LD VALUE
RET
```

Insert after old physical line 46, before the following old line.

Insert this source:

```ir
; PAIR
LABEL PAIR
ST WORK
PUSH
LIT 255
AND
CALL CHAR
LIT 256
ST STEP
LD WORK
CALL DIVIDE
LD COUNT
JMP CHAR
LABEL NEWLINE
LIT 2573
CALL PAIR
RET
```

### Change 2: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
WORD COUNT 0
; Driver
LABEL MAIN
```

Remove these exact old lines (physical positions 7–12 in `R03.IR`):

```ir
LIT 256
ST STEP
LIT 16712
CALL DIVIDE
LD COUNT
CALL CHAR
```

Put this source in their place:

```ir
LIT 18760
CALL PAIR
LIT 2573
CALL PAIR
```

### Change 3: in the declarations

Unchanged source immediately before the edit:

```ir
; DATA
WORD VALUE 0
```

Insert after old physical line 2, before the following old line.

Insert this source:

```ir
WORD WORK 0
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R04` at `IR source name:`. Require `OK R04.ASM 03391 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R04` at `Source name:`, and require `OK 00623 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Run `CHECK R04`. This checkpoint does not read SOURCE.RIL.

Apart from DOS command echo and the checker's separating blank line, require:

```text
HI
PASS
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
