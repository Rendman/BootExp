+++
title = "05 \u00b7 Displaying an unsigned word"
weight = 5
description = "Make numeric diagnostics readable without another tool."
download = "R05.IR"
download_group = "tools/rill0"
reader_names = 1
+++

A compiler must report numbers which are not printable character codes.

## The working parts

NUMBER prints A as exactly five decimal digits, including leading zeroes. WORK retains the unprinted value and PLACE begins at 10000. DIVIDE produces one digit, which becomes ASCII after adding 48. The remainder becomes the next WORK value.

After a digit, PLACE is divided by ten. The last place is one. CHAR does not change WORK or PLACE, so these values survive each output call. NUMBER changes the formatting work cells and A. The stopping test displays 65535 and a CR/LF.

## Enter the source

Copy `R04.IR` to `R05.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL NEWLINE`

Unchanged source immediately before the edit:

```ir
LIT 2573
CALL PAIR
RET
```

Insert after old physical line 62, before the following old line.

Insert this source:

```ir
; NUMBER
LABEL NUMBER
ST WORK
LIT 10000
ST PLACE
LABEL NUMPRINT
LD PLACE
ST STEP
LD WORK
CALL DIVIDE
ST WORK
LD COUNT
PUSH
LIT 48
ADD
CALL CHAR
LD STEP
PUSH
LIT 1
EQ NUMDONE
LIT 10
ST STEP
LD PLACE
CALL DIVIDE
LD COUNT
ST PLACE
JMP NUMPRINT
LABEL NUMDONE
RET
```

### Change 2: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
WORD COUNT 0
; Driver
LABEL MAIN
```

Remove these exact old lines (physical positions 8–11 in `R04.IR`):

```ir
LIT 18760
CALL PAIR
LIT 2573
CALL PAIR
```

Put this source in their place:

```ir
LIT 65535
CALL NUMBER
CALL NEWLINE
```

### Change 3: in the declarations

Unchanged source immediately before the edit:

```ir
; DATA
WORD VALUE 0
WORD WORK 0
```

Insert after old physical line 3, before the following old line.

Insert this source:

```ir
WORD PLACE 0
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R05` at `IR source name:`. Require `OK R05.ASM 03845 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R05` at `Source name:`, and require `OK 00708 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Run `CHECK R05`. This checkpoint does not read SOURCE.RIL.

Apart from DOS command echo and the checker's separating blank line, require:

```text
65535
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
