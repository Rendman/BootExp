+++
title = "RB30 \u00b7 Define one compiler label"
weight = 30
description = "Emit LABEL, the reserved B_ prefix, and the saved number."
download = "RB30.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/063-rb-define-one-compiler-label/"]
+++

Emit LABEL, the reserved B_ prefix, and the saved number.

## The working parts

Emit LABEL, the reserved B_ prefix, and the saved number. Every definition ends with a record terminator.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB29.IR to RB30.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LD LABELNO
RETURN
```

Insert after old physical line 982.

Insert:

```ir
PROC LABELDEF 0 1
SETLOCAL 0
LITS "LABEL B_"
CALL OUTSTR
LOCAL 0
CALL OUTNUM
CALL NEWLINE
LIT 0
RETURN
```

The following old source remains in place:

```ir
PROC NEWLINE 0 0
LITS "\r\n"
```

### Edit 2

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–36 in RB29.IR:

```ir
CALL NEWLABEL
CALL PRINTNUM
```

Replace it with:

```ir
LITS "RILL.TMP"
CREATE
ST OUTPUT
STATUS
JNZ IOFAIL
LIT 1
ST OWN
LIT 7
CALL LABELDEF
CALL FLUSH
LD OUTPUT
CLOSE
LIT 0
ST OUTPUT
ST OWN
LITS "OK RILL.TMP\r\n"
CALL PRINT
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

## Build this stopping point

```dos
COPY RB30.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000031558 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14826 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB30.COM
```

VIEW.BAS must report RB30.COM length 14826 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB30
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
LABEL B_00007
```

VIEW.BAS must show length 15 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

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
