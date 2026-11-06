+++
title = "02 \u00b7 A checked character writer"
weight = 2
description = "Give every displayed byte a checked service result."
download = "R02.IR"
download_group = "tools/rill0"
reader_names = 1
+++

A missing display must not be mistaken for a successful test. One routine can check every character write.

## The working parts

CHAR receives a byte value in A, writes its low byte with PUTC, and reads STATUS immediately. A successful call returns; output failure terminates with status four. The caller cannot assume that A survives.

The driver replaces its direct writes with CALL CHAR. Native return addresses belong to the backend; the IR call requires no knowledge of their representation.

## Enter the source

Copy `R01.IR` to `R02.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
LABEL MAIN
LIT 72
PUTC
```

Remove these exact old lines (physical positions 5–7 in `R01.IR`):

```ir
LIT 73
PUTC
HALT
```

Put this source in their place:

```ir
STATUS
JZ CHARDONE
LIT 4
EXIT
LABEL CHARDONE
RET
```

### Change 2: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
; Driver
LABEL MAIN
LIT 72
```

Insert after old physical line 3, before the following old line.

Insert this source:

```ir
CALL CHAR
LIT 73
CALL CHAR
HALT
; CHAR
LABEL CHAR
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R02` at `IR source name:`. Require `OK R02.ASM 02729 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R02` at `Source name:`, and require `OK 00504 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Run `CHECK R02`. This checkpoint does not read SOURCE.RIL.

Apart from DOS command echo and the checker's separating blank line, require:

```text
HIPASS
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
