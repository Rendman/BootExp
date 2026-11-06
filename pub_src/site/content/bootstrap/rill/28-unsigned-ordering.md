+++
title = "28 \u00b7 Unsigned ordering"
weight = 28
description = "Select each false relation without relying on flags."
download = "R28.IR"
download_group = "tools/rill0"
reader_names = 1
+++

Word ordering must state how values with the high bit set are interpreted.

## The working parts

The condition parser adds <, <=, >, and >=. Every RILL value in this implementation is an unsigned sixteen-bit word. Their false relations are UGE, UGT, ULE, and ULT respectively. == and != retain their equality meaning.

The operator token is kept in TOKENVAL after both source expressions have been compiled. Formatting calls do not change it. The output names a relation explicitly, so its meaning is independent of the first backend. A negative expression wraps to an unsigned word before an ordering comparison.

## Enter the source

Copy `R27.IR` to `R28.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL CONDNE`

Unchanged source immediately before the edit:

```ir
CALL PAIR
LIT 16928
CALL PAIR
```

Insert after old physical line 1032, before the following old line.

Insert this source:

```ir
JMP CONDTARGET
LABEL CONDEQ
LIT 20805
CALL PAIR
LIT 16928
CALL PAIR
JMP CONDTARGET
LABEL CONDUGE
LIT 18261
CALL PAIR
LIT 8261
CALL PAIR
LIT 66
CALL CHAR
JMP CONDTARGET
LABEL CONDULE
LIT 19541
CALL PAIR
LIT 8261
CALL PAIR
LIT 66
CALL CHAR
JMP CONDTARGET
LABEL CONDUGT
LIT 18261
CALL PAIR
LIT 8276
CALL PAIR
LIT 66
CALL CHAR
```

### Change 2: following `LABEL RELATION`

Unchanged source immediately before the edit:

```ir
CALL PAIR
LIT 16928
CALL PAIR
```

Insert after old physical line 1026, before the following old line.

Insert this source:

```ir
LIT 66
CALL CHAR
```

### Change 3: following `LABEL RELATION`

Unchanged source immediately before the edit:

```ir
EQ CONDNE
LIT 20805
CALL PAIR
```

Remove these exact old lines (physical positions 1025–1025 in `R27.IR`):

```ir
LIT 16928
```

Put this source in their place:

```ir
LIT 8276
```

### Change 4: following `LABEL RELATION`

Unchanged source immediately before the edit:

```ir
PUSH
LIT 200
EQ CONDNE
```

Remove these exact old lines (physical positions 1023–1023 in `R27.IR`):

```ir
LIT 20805
```

Put this source in their place:

```ir
LD TOKENVAL
PUSH
LIT 201
EQ CONDEQ
LD TOKENVAL
PUSH
LIT 60
EQ CONDUGE
LD TOKENVAL
PUSH
LIT 62
EQ CONDULE
LD TOKENVAL
PUSH
LIT 202
EQ CONDUGT
LIT 19541
```

### Change 5: following `LABEL RELATION`

Unchanged source immediately before the edit:

```ir
CALL LEX
CALL EXPR
CALL RESTORE
```

Insert after old physical line 1019, before the following old line.

Insert this source:

```ir
ST TOKENVAL
```

### Change 6: following `LABEL CONDITION`

Unchanged source immediately before the edit:

```ir
EQ RELATION
LD TOK
PUSH
```

Remove these exact old lines (physical positions 1006–1007 in `R27.IR`):

```ir
LIT 201
NE VALUECOND
```

Put this source in their place:

```ir
LIT 62
EQ RELATION
LD TOK
PUSH
LIT 200
ULT VALUECOND
LD TOK
PUSH
LIT 203
UGT VALUECOND
```

### Change 7: following `LABEL CONDITION`

Unchanged source immediately before the edit:

```ir
CALL EXPR
LD TOK
PUSH
```

Remove these exact old lines (physical positions 1002–1002 in `R27.IR`):

```ir
LIT 200
```

Put this source in their place:

```ir
LIT 60
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R28` at `IR source name:`. Require `OK R28.ASM 24318 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R28` at `Source name:`, and require `OK 05109 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T28.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main(){if 65535>1{putc(85);}else{putc(76);}}
```

Run `COPY T28.RIL SOURCE.RIL`, then `CHECK R28`.

Require:

```text
OK RESULT.IR 00132
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
LIT 65535
PUSH
LIT 00001
ULE B00001
LIT 00085
PUTC
JMP B00002
LABEL B00001
LIT 00076
PUTC
LABEL B00002
HALT
```

Copy RESULT.IR to T28.IR. Translate it with CHECK IRKEEP, entering T28; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00498 bytes` and PASS.

VIEW.BAS must report T28.COM length **498 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T28`. It displays `U` and the checker reports PASS.

## A rejection check

Create X28.RIL with this separate test:

```rill
fn main(){if 1<2<3 {}}
```

Copy X28.RIL to SOURCE.RIL, then run CHECK R28. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check the order in which targets enter and leave FRAMES. Compare the false relation and label names in RESULT.IR. A branch must consume its saved expression operand before reaching an IR control boundary.
