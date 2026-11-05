+++
title = "25 \u00b7 A conditional block"
weight = 25
description = "Skip a brace-enclosed body when a word is zero."
download = "R25.IR"
+++

A source condition should describe a value rather than a processor flag.

## The working parts

CONDITION saves the false target in BRANCH, compiles EXPR, and emits JZ to that target. IFSTAT obtains a label, saves it in FRAMES, compiles the condition and block, then restores and defines the target. Zero skips the body; every other word enters it.

The pending target survives any assignments or nested constructs in the body because it is saved explicitly. BODY already supplies the shared nesting check. This stopping point accepts if with one block and no else clause. IR control boundaries remain empty after each compiled expression.

## Enter the source

Copy `R24.IR` to `R25.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL JUMPLABEL`

Unchanged source immediately before the edit:

```ir
CALL NUMBER
CALL NEWLINE
RET
```

Insert after old physical line 993, before the following old line.

Insert this source:

```ir
; CONDITION
LABEL CONDITION
ST BRANCH
CALL EXPR
LABEL VALUECOND
LIT 23114
CALL PAIR
LIT 16928
CALL PAIR
LABEL CONDTARGET
LD BRANCH
CALL NUMBER
CALL NEWLINE
RET
; IFSTAT
LABEL IFSTAT
CALL LEX
CALL NEWLABEL
CALL SAVE
CALL CONDITION
CALL BLOCK
CALL RESTORE
CALL DEFLABEL
RET
```

### Change 2: following `LABEL STATEMENT`

Unchanged source immediately before the edit:

```ir
PUSH
LIT 38665
EQ EXITSTAT
```

Insert after old physical line 909, before the following old line.

Insert this source:

```ir
LD TOK
PUSH
LIT 33062
EQ IFSTAT
```

### Change 3: following `LABEL DECLDONE`

Unchanged source immediately before the edit:

```ir
CALL PAIR
LIT 2573
CALL PAIR
```

Remove these exact old lines (physical positions 75–76 in `R24.IR`):

```ir
CALL NEWLABEL
CALL DEFLABEL
```

No replacement source is needed.

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R25` at `IR source name:`. Require `OK R25.ASM 22448 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R25` at `Source name:`, and require `OK 04763 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T25.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){if 0 {putc(88);}if 1 {putc(65);}}
```

Run `COPY T25.RIL SOURCE.RIL`, then `CHECK R25`.

Require:

```text
OK RESULT.IR 00124
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
LIT 00000
JZ B00001
LIT 00088
PUTC
LABEL B00001
LIT 00001
JZ B00002
LIT 00065
PUTC
LABEL B00002
HALT
```

Copy RESULT.IR to T25.IR. Translate it with CHECK IRKEEP, entering T25; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00504 bytes` and PASS.

VIEW.BAS must report T25.COM length **504 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T25`. It displays `A` and the checker reports PASS.

## A rejection check

Create X25.RIL with this separate test:

```rill
fn main(){if 1 putc(65);}
```

Copy X25.RIL to SOURCE.RIL, then run CHECK R25. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check the order in which targets enter and leave FRAMES. Compare the false relation and label names in RESULT.IR. A branch must consume its saved expression operand before reaching an IR control boundary.
