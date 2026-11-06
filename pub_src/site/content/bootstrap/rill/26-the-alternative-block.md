+++
title = "26 \u00b7 The alternative block"
weight = 26
description = "Keep both outgoing paths separate through nested conditionals."
download = "R26.IR"
download_group = "tools/rill0"
reader_names = 1
+++

An else body must be bypassed after the true body has completed.

## The working parts

IFSTAT saves two targets: one for false and one for the join. After the first block it emits a jump to the join and defines the false target. If TOK selects else, ENDTOKEN checks its final e before BLOCK compiles the alternative. The join label is defined afterward.

VARNAME temporarily holds an end target only between label-output calls. It is saved back to FRAMES before another block can change it. A missing else still has a valid empty false path. Braces make the association explicit; else if is not an abbreviation in this subset.

## Enter the source

Copy `R25.IR` to `R26.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL IFSTAT`

Unchanged source immediately before the edit:

```ir
CALL SAVE
CALL CONDITION
CALL BLOCK
```

Insert after old physical line 1016, before the following old line.

Insert this source:

```ir
CALL RESTORE
ST VARNAME
CALL JUMPLABEL
CALL RESTORE
CALL DEFLABEL
LD VARNAME
CALL SAVE
LD TOK
PUSH
LIT 38291
NE IFEND
LIT 5
CALL ENDTOKEN
CALL BLOCK
LABEL IFEND
```

### Change 2: following `LABEL IFSTAT`

Unchanged source immediately before the edit:

```ir
CALL NEWLABEL
CALL SAVE
CALL CONDITION
```

Insert after old physical line 1015, before the following old line.

Insert this source:

```ir
CALL NEWLABEL
CALL SAVE
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R26` at `IR source name:`. Require `OK R26.ASM 22738 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R26` at `Source name:`, and require `OK 04817 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T26.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){if 0 {putc(88);}else{putc(65);}}
```

Run `COPY T26.RIL SOURCE.RIL`, then `CHECK R26`.

Require:

```text
OK RESULT.IR 00114
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
LIT 00000
JZ B00001
LIT 00088
PUTC
JMP B00002
LABEL B00001
LIT 00065
PUTC
LABEL B00002
HALT
```

Copy RESULT.IR to T26.IR. Translate it with CHECK IRKEEP, entering T26; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00495 bytes` and PASS.

VIEW.BAS must report T26.COM length **495 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T26`. It displays `A` and the checker reports PASS.

## A rejection check

Create X26.RIL with this separate test:

```rill
fn main(){if 1 {} elsee {}}
```

Copy X26.RIL to SOURCE.RIL, then run CHECK R26. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check the order in which targets enter and leave FRAMES. Compare the false relation and label names in RESULT.IR. A branch must consume its saved expression operand before reaching an IR control boundary.
