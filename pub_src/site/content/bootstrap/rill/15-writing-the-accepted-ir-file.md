+++
title = "15 \u00b7 Writing the accepted IR file"
weight = 15
description = "Complete a small compiler for the empty program."
download = "R15.IR"
download_group = "tools/rill0"
reader_names = 1
+++

The accepted text can now be saved and passed to the existing translator.

## The working parts

The driver recognizes the whole source, closes INPUT, and only then calls WRITEFILE. RESULTNAME replaces the name buffer with RESULT.IR. CREATE returns a writable opaque token, which reuses INPUT after the source handle has been closed. WRITE supplies that token, ADDR OUTBUF, and OUTCOUNT. Its complete-write status and the final CLOSE status are checked.

Success reports OK RESULT.IR and its text length. A source error leaves an older result unchanged. A failure after CREATE may leave a partial result; require a fresh OK and PASS. The generated program has LABEL MAIN and HALT. It is complete and may be translated, assembled, and run.

## Enter the source

Copy `R14.IR` to `R15.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL SOURCENAME`

Unchanged source immediately before the edit:

```ir
LIT 0
CALL NAMEWORD
RET
```

Insert after old physical line 605, before the following old line.

Insert this source:

```ir
LABEL RESULTNAME
ADDR NAMEBUF
ST PLACE
LIT 17746
CALL NAMEWORD
LIT 21843
CALL NAMEWORD
LIT 21580
CALL NAMEWORD
LIT 18734
CALL NAMEWORD
LIT 82
CALL NAMEWORD
RET
```

### Change 2: following `LABEL ENDTOKEN`

Unchanged source immediately before the edit:

```ir
NE SYNTAX
CALL LEX
RET
```

Insert after old physical line 576, before the following old line.

Insert this source:

```ir
; WRITEFILE
LABEL WRITEFILE
CALL RESULTNAME
ADDR NAMEBUF
CREATE
ST INPUT
STATUS
JNZ IOFAIL
LD INPUT
PUSH
ADDR OUTBUF
PUSH
LD OUTCOUNT
WRITE
STATUS
JNZ IOFAIL
LD INPUT
CLOSE
STATUS
JNZ IOFAIL
RET
```

### Change 3: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
LD OUTCOUNT
CALL NUMBER
CALL NEWLINE
```

Remove these exact old lines (physical positions 88–105 in `R14.IR`):

```ir
LABEL SHOWBUFFER
LD TOKENVAL
PUSH
LD OUTCOUNT
UGE BUFFERDONE
ADDR OUTBUF
PUSH
LD TOKENVAL
ADD
FETCHB
CALL CHAR
LD TOKENVAL
PUSH
LIT 1
ADD
ST TOKENVAL
JMP SHOWBUFFER
LABEL BUFFERDONE
```

No replacement source is needed.

### Change 4: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
CALL PAIR
LIT 17990
CALL PAIR
```

Remove these exact old lines (physical positions 81–81 in `R14.IR`):

```ir
LIT 21061
```

Put this source in their place:

```ir
LIT 21317
CALL PAIR
LIT 19541
CALL PAIR
LIT 11860
CALL PAIR
LIT 21065
```

### Change 5: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
ST TOKENVAL
LIT 21826
CALL PAIR
```

Remove these exact old lines (physical positions 79–79 in `R14.IR`):

```ir
LIT 17990
```

Put this source in their place:

```ir
LIT 21024
```

### Change 6: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
CALL PAIR
LIT 0
ST DEST
```

Remove these exact old lines (physical positions 76–77 in `R14.IR`):

```ir
ST TOKENVAL
LIT 21826
```

Put this source in their place:

```ir
LIT 19279
```

### Change 7: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
CALL PAIR
LIT 2573
CALL PAIR
```

Insert after old physical line 73, before the following old line.

Insert this source:

```ir
CALL WRITEFILE
```

### Change 8: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
CALL PAIR
LIT 2573
CALL PAIR
```

Insert after old physical line 67, before the following old line.

Insert this source:

```ir
LIT 125
CALL EXPECT
LIT 0
CALL EXPECT
LD INPUT
CLOSE
STATUS
JNZ IOFAIL
```

### Change 9: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
CALL EXPECT
LIT 123
CALL EXPECT
```

Remove these exact old lines (physical positions 46–53 in `R14.IR`):

```ir
LIT 125
CALL EXPECT
LIT 0
CALL EXPECT
LD INPUT
CLOSE
STATUS
JNZ IOFAIL
```

No replacement source is needed.

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R15` at `IR source name:`. Require `OK R15.ASM 15447 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R15` at `Source name:`, and require `OK 03431 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T15.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main() {}
```

Run `COPY T15.RIL SOURCE.RIL`, then `CHECK R15`.

Require:

```text
OK RESULT.IR 00018
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
LABEL MAIN
HALT
```

Copy RESULT.IR to T15.IR. Translate it with CHECK IRKEEP, entering T15; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00468 bytes` and PASS.

VIEW.BAS must report T15.COM length **468 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
```

Run `CHECK T15`. It returns zero and the checker reports PASS.

## A rejection check

Create X15.RIL with this separate test:

```rill
fn main( {}
```

Copy X15.RIL to SOURCE.RIL, then run CHECK R15. Require:

```text
ERROR 00001 CODE 00002
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.
