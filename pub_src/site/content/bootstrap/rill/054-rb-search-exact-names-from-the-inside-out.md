+++
title = "RB21 \u00b7 Search exact names from the inside out"
weight = 54
description = "Search entries from the end toward the beginning and compare complete spellings."
download = "RB21.IR"
download_group = "toolchain"
+++

Search entries from the end toward the beginning and compare complete spellings.

## The working parts

Search entries from the end toward the beginning and compare complete spellings. This selects the innermost active binding. Return 65535 for absence; offset zero is a valid found record.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB20.IR to RB21.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
GET8
RETURN
```

Insert after old physical line 627.

Insert:

```ir
PROC FIND 2 4
PARAM 1
SETLOCAL 0
LABEL FINDNEXT
LOCAL 0
JZ FINDNONE
PUSH
LIT 1
SUB
SETLOCAL 0
PUSH
LIT 40
MUL
PUSH
PARAM 0
ADD
SETLOCAL 1
LIT 0
SETLOCAL 2
LABEL FINDCHAR
LOCAL 1
PUSH
LOCAL 2
ADD
CALL TBYTE
SETLOCAL 3
PUSH
ADDR IDENT
PUSH
LOCAL 2
ADD
FETCHB
CNE
JNZ FINDNEXT
LOCAL 3
JZ FOUNDIT
LOCAL 2
PUSH
LIT 1
ADD
SETLOCAL 2
JMP FINDCHAR
LABEL FOUNDIT
LOCAL 1
PUSH
LIT 32
ADD
CALL TWORD
ST RECTYPE
LOCAL 1
PUSH
LIT 34
ADD
CALL TWORD
ST RECVAL
LOCAL 1
PUSH
LIT 36
ADD
CALL TWORD
ST RECLEVEL
LOCAL 1
RETURN
LABEL FINDNONE
LIT 65535
RETURN
```

The following old source remains in place:

```ir
PROC WRITEFIELD 2 0
LD TABLE
```

### Edit 2

Unchanged source immediately before the edit:

```ir
CALL SETIDENT
LIT 7
ST RECVAL
```

Remove this source at old physical positions 42–45 in RB20.IR:

```ir
LIT 5
CALL NEWLOCAL
LIT 20514
CALL TWORD
```

Replace it with:

```ir
LIT 0
ST RECLEVEL
LIT 0
PUSH
INVOKE RECORD 1
LIT 1
ST GLOBALS
LIT 0
PUSH
LIT 1
PUSH
INVOKE FIND 2
LD RECVAL
```

The following old source remains in place:

```ir
CALL PRINTNUM
LIT 0
```

### Edit 3

Unchanged source immediately before the edit:

```ir
ST TABLE
LITS "ABC"
CALL SETIDENT
```

Remove this source at old physical positions 40–40 in RB20.IR:

```ir
LIT 7
```

Replace it with:

```ir
LIT 1
ST RECTYPE
LIT 12345
```

The following old source remains in place:

```ir
ST RECVAL
LIT 5
```

## Build this stopping point

```dos
COPY RB21.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000027190 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14016 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB21.COM
```

VIEW.BAS must report RB21.COM length 14016 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB21
```

Require, apart from command echo and the checker's separator:

```text
12345PASS
```

## A rejection or boundary check

Check a representable-word boundary in the preceding translator. Create BAD.IR:

```ir
PROC MAIN 0 0
LIT 65536
RETURN
```

```dos
COPY BAD.IR SOURCE.IR
CHECK IWKEEP
```

Require `IR ERROR 0000000002 CODE 2` and FAIL. The accepted RESULT.ASM must remain unchanged. The diagnostic cannot be built from an out-of-range word.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
