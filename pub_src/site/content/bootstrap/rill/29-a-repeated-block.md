+++
title = "29 \u00b7 A repeated block"
weight = 29
description = "Re-evaluate a condition at a named loop entrance."
download = "R29.IR"
cartoon = "rill-paths.png"
download_group = "tools/rill0"
reader_names = 1
+++

A loop must test again after each completed body, rather than reusing its original result.

## The working parts

WHILESTAT creates an entrance and an exit target and saves both in FRAMES. It defines the entrance before compiling CONDITION, compiles the body, emits a jump back to the entrance, and defines the exit afterward. The condition is therefore evaluated on every iteration.

Both value tests and the six comparisons are available. There is no break or continue statement in this subset; exit terminates the entire program. Nested loops and conditionals use the same saved-target discipline. The counter test prints 012 and stops when its word reaches 51.

## Enter the source

Copy `R28.IR` to `R29.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL IFEND`

Unchanged source immediately before the edit:

```ir
CALL RESTORE
CALL DEFLABEL
RET
```

Insert after old physical line 1127, before the following old line.

Insert this source:

```ir
; WHILESTAT
LABEL WHILESTAT
LIT 389
CALL ENDTOKEN
CALL NEWLABEL
CALL SAVE
CALL DEFLABEL
CALL NEWLABEL
CALL SAVE
CALL CONDITION
CALL BLOCK
CALL RESTORE
ST VARNAME
CALL RESTORE
CALL JUMPLABEL
LD VARNAME
CALL DEFLABEL
RET
```

### Change 2: following `LABEL STATEMENT`

Unchanged source immediately before the edit:

```ir
PUSH
LIT 33062
EQ IFSTAT
```

Insert after old physical line 911, before the following old line.

Insert this source:

```ir
LD TOK
PUSH
LIT 56585
EQ WHILESTAT
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R29` at `IR source name:`. Require `OK R29.ASM 24676 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R29` at `Source name:`, and require `OK 05173 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T29.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){let mut x=48;while x<51{putc(x);x=x+1;}}
```

Run `COPY T29.RIL SOURCE.RIL`, then `CHECK R29`.

Require:

```text
OK RESULT.IR 00153
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
WORD x 00048
LABEL MAIN
LABEL B00001
LD x
PUSH
LIT 00051
UGE B00002
LD x
PUTC
LD x
PUSH
LIT 00001
ADD
ST x
JMP B00001
LABEL B00002
HALT
```

Copy RESULT.IR to T29.IR. Translate it with CHECK IRKEEP, entering T29; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00511 bytes` and PASS.

VIEW.BAS must report T29.COM length **511 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 02 00 30
```

Run `CHECK T29`. It displays `012` and the checker reports PASS.

## A rejection check

Create X29.RIL with this separate test:

```rill
fn main(){while 1 {let mut x=0;}}
```

Copy X29.RIL to SOURCE.RIL, then run CHECK R29. Require:

```text
ERROR 00001 CODE 00004
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check the order in which targets enter and leave FRAMES. Compare the false relation and label names in RESULT.IR. A branch must consume its saved expression operand before reaching an IR control boundary.
