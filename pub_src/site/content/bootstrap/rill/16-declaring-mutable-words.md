+++
title = "16 \u00b7 Declaring mutable words"
weight = 16
description = "Reserve named words before the executable entry label."
download = "R16.IR"
+++

A mutable value needs declared storage and a rule preventing accidental reuse of its name.

## The working parts

Declarations have the form let mut x = 65;. Each name is one lowercase letter. VARADDRESS checks its range, saves it in VARNAME, and forms a pointer into the twenty-six-byte VARS table. A nonzero entry marks a declared variable. DECLARE refuses a second declaration and emits WORD, the name, and its decimal initializer.

Initializers are unsigned literals, and all declarations precede executable statements. Their IR storage therefore precedes LABEL MAIN as required by IR86. USEVAR checks the same table for a previously declared name. VARADDRESS returns a pointer in A; USEVAR returns the letter. Both change VARNAME.

## Enter the source

Copy `R15.IR` to `R16.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL WRITEFILE`

Unchanged source immediately before the edit:

```ir
STATUS
JNZ IOFAIL
RET
```

Insert after old physical line 585, before the following old line.

Insert this source:

```ir
; VARADDRESS
LABEL VARADDRESS
LD TOK
PUSH
LIT 97
ULT NAMEFAIL
LD TOK
PUSH
LIT 122
UGT NAMEFAIL
LD TOK
ST VARNAME
PUSH
LIT 97
SUB
PUSH
ADDR VARS
ADD
RET
LABEL USEVAR
CALL VARADDRESS
FETCHB
JZ NAMEFAIL
LD VARNAME
RET
; DECLARE
LABEL DECLARE
LIT 45236
CALL EXPECT
LIT 46772
CALL EXPECT
CALL VARADDRESS
ST VALUE
FETCHB
JNZ NAMEFAIL
LD VALUE
PUSH
LIT 1
PUTB
CALL LEX
LIT 61
CALL EXPECT
LD TOK
PUSH
LIT 65535
NE SYNTAX
LIT 20311
CALL PAIR
LIT 17490
CALL PAIR
LIT 32
CALL CHAR
LD VARNAME
CALL CHAR
LIT 32
CALL CHAR
LD TOKENVAL
CALL NUMBER
CALL NEWLINE
CALL LEX
LIT 59
CALL EXPECT
RET
```

### Change 2: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
CALL EXPECT
LIT 1
ST DEST
```

Insert after old physical line 47, before the following old line.

Insert this source:

```ir
LABEL DECLLOOP
LD TOK
PUSH
LIT 45236
NE DECLDONE
CALL DECLARE
JMP DECLLOOP
LABEL DECLDONE
```

### Change 3: in the declarations

Unchanged source immediately before the edit:

```ir
WORD SUFFIX 0
WORD WANTTAIL 0
WORD TOK 0
```

Insert after old physical line 17, before the following old line.

Insert this source:

```ir
WORD VARNAME 0
BUFFER VARS 26
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R16` at `IR source name:`. Require `OK R16.ASM 16749 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R16` at `Source name:`, and require `OK 03682 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Create `T16.RIL` with COPY CON or a plain-text editor. Enter this exact text and finish with Ctrl-Z and Enter:

```rill
fn main() { let mut x=65; }
```

Run `COPY T16.RIL SOURCE.RIL`, then `CHECK R16`.

Require:

```text
OK RESULT.IR 00032
PASS
```

Run `TYPE RESULT.IR`. Its complete contents must be:

```ir
WORD x 00065
LABEL MAIN
HALT
```

Copy RESULT.IR to T16.IR. Translate it with CHECK IRKEEP, entering T16; require OK and PASS. Assemble it with CHECK ASMKEEP, entering the same name; require `OK 00470 bytes` and PASS.

VIEW.BAS must report T16.COM length **470 bytes**. These are its first sixteen bytes, not its complete contents:

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 02 00 41
```

Run `CHECK T16`. It returns zero and the checker reports PASS.

## A rejection check

Create X16.RIL with this separate test:

```rill
fn main(){let mut x=0;let mut x=1;}
```

Copy X16.RIL to SOURCE.RIL, then run CHECK R16. Require:

```text
ERROR 00001 CODE 00004
FAIL
```

Keep the accepted RESULT.IR before trying the rejection. TYPE it afterward: source rejection must leave it unchanged. Require a fresh OK before using any output.

An unexpected PASS is a failed rejection test.

## If the result differs

Check both halves of keyword spellings, required delimiters, and saved names or operators. Compare RESULT.IR with the printed text before translating it. A source error and a result-write error have different effects on an old file.
