+++
title = "24 \u00b7 Naming generated blocks"
weight = 24
description = "Give internal code positions names which cannot collide with variables."
download = "R24.IR"
+++

Control-flow output needs a distinct name for each compiler-created code position.

## The working parts

NEWLABEL increments LABELNO and returns its value in A. DEFLABEL and JUMPLABEL save that value in BRANCH while PAIR emits a prefix, then NUMBER supplies five decimal digits. Names such as B00001 differ from the single-letter variable names.

The driver emits an otherwise unused block label before the body so the naming routines have a direct visible test. Inspect it in RESULT.IR. Decimal names are source labels, not machine addresses; IR86 and ASM86 resolve their locations.

## Enter the source

Copy `R23.IR` to `R24.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL EXITSTAT`

Unchanged source immediately before the edit:

```ir
LIT 2573
CALL PAIR
RET
```

Insert after old physical line 955, before the following old line.

Insert this source:

```ir
; LABELS
LABEL NEWLABEL
LD LABELNO
PUSH
LIT 1
ADD
ST LABELNO
RET
LABEL DEFLABEL
ST BRANCH
LIT 16716
CALL PAIR
LIT 17730
CALL PAIR
LIT 8268
CALL PAIR
LIT 66
CALL CHAR
LD BRANCH
CALL NUMBER
CALL NEWLINE
RET
LABEL JUMPLABEL
ST BRANCH
LIT 19786
CALL PAIR
LIT 8272
CALL PAIR
LIT 66
CALL CHAR
LD BRANCH
CALL NUMBER
CALL NEWLINE
RET
```

### Change 2: following `LABEL DECLDONE`

Unchanged source immediately before the edit:

```ir
CALL PAIR
LIT 2573
CALL PAIR
```

Insert after old physical line 72, before the following old line.

Insert this source:

```ir
CALL NEWLABEL
CALL DEFLABEL
```

### Change 3: in the declarations

Unchanged source immediately before the edit:

```ir
WORD TOK 0
WORD VARNAME 0
BUFFER VARS 26
```

Insert after old physical line 19, before the following old line.

Insert this source:

```ir
WORD LABELNO 0
```

### Change 4: in the declarations

Unchanged source immediately before the edit:

```ir
WORD STEP 0
WORD COUNT 0
WORD INPUT 0
```

Insert after old physical line 11, before the following old line.

Insert this source:

```ir
WORD BRANCH 0
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R24` at `IR source name:`. Require `OK R24.ASM 22084 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R24` at `Source name:`, and require `OK 04701 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T24.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){putc(65);}
```

Run `COPY T24.RIL SOURCE.RIL`, then `CHECK R24`.

Require:

```text
OK RESULT.IR 00049
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
LABEL B00001
LIT 00065
PUTC
HALT
```

Copy RESULT.IR to T24.IR. Translate it with CHECK IRKEEP, entering T24; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00474 bytes` and PASS.

VIEW.BAS must report T24.COM length **474 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T24`. It displays `A` and the checker reports PASS.

## A rejection check

Create X24.RIL with this separate test:

```rill
fn main(){putc(1==1);}
```

Copy X24.RIL to SOURCE.RIL, then run CHECK R24. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check the order in which targets enter and leave FRAMES. Compare the false relation and label names in RESULT.IR. A branch must consume its saved expression operand before reaching an IR control boundary.
