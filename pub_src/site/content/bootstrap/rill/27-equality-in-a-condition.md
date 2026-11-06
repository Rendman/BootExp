+++
title = "27 \u00b7 Equality in a condition"
weight = 27
description = "Compare word values while retaining an empty control boundary."
download = "R27.IR"
download_group = "tools/rill0"
reader_names = 1
+++

A comparison needs two expression values and a chosen false branch.

## The working parts

CONDITION accepts == or != between two arithmetic expressions. It emits PUSH for the left value and compiles the right. The inverse IR relation, NE or EQ, transfers to the false target. Both consume the saved left value before the branch.

The comparison is allowed only as the outer condition of if or while. It does not produce a Boolean expression value which could be embedded in arithmetic. This restriction matches the simple IR control interface and avoids hidden expression temporaries across a branch.

## Enter the source

Copy `R26.IR` to `R27.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL CONDITION`

Unchanged source immediately before the edit:

```ir
LABEL CONDITION
ST BRANCH
CALL EXPR
```

Insert after old physical line 999, before the following old line.

Insert this source:

```ir
LD TOK
PUSH
LIT 200
EQ RELATION
LD TOK
PUSH
LIT 201
NE VALUECOND
LABEL RELATION
LIT 21840
CALL PAIR
LIT 18515
CALL PAIR
LIT 2573
CALL PAIR
LD TOK
CALL SAVE
CALL LEX
CALL EXPR
CALL RESTORE
PUSH
LIT 200
EQ CONDNE
LIT 20805
CALL PAIR
LIT 16928
CALL PAIR
JMP CONDTARGET
LABEL CONDNE
LIT 17742
CALL PAIR
LIT 16928
CALL PAIR
JMP CONDTARGET
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R27` at `IR source name:`. Require `OK R27.ASM 23311 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R27` at `Source name:`, and require `OK 04925 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T27.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){if 1==1 {putc(69);}else{putc(88);}if 1!=0{putc(81);}}
```

Run `COPY T27.RIL SOURCE.RIL`, then `CHECK R27`.

Require:

```text
OK RESULT.IR 00227
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
LIT 00001
PUSH
LIT 00001
NE B00001
LIT 00069
PUTC
JMP B00002
LABEL B00001
LIT 00088
PUTC
LABEL B00002
LIT 00001
PUSH
LIT 00000
EQ B00003
LIT 00081
PUTC
JMP B00004
LABEL B00003
LABEL B00004
HALT
```

Copy RESULT.IR to T27.IR. Translate it with CHECK IRKEEP, entering T27; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00522 bytes` and PASS.

VIEW.BAS must report T27.COM length **522 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T27`. It displays `EQ` and the checker reports PASS.

## A rejection check

Create X27.RIL with this separate test:

```rill
fn main(){if 1<2 {}}
```

Copy X27.RIL to SOURCE.RIL, then run CHECK R27. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check the order in which targets enter and leave FRAMES. Compare the false relation and label names in RESULT.IR. A branch must consume its saved expression operand before reaching an IR control boundary.
