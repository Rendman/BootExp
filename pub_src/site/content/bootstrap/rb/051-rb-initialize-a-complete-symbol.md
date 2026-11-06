+++
title = "RB18 \u00b7 Initialize a complete symbol"
weight = 18
description = "Initialize the entire forty-byte record, copy the complete spelling, then write the explicit fields."
download = "RB18.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/051-rb-initialize-a-complete-symbol/"]
+++

Initialize the entire forty-byte record, copy the complete spelling, then write the explicit fields.

## The working parts

Initialize the entire forty-byte record, copy the complete spelling, then write the explicit fields. The global region begins at zero in TABLE; the local region begins at byte offset 20480.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB17.IR to RB18.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
SET16
RETURN
```

Insert after old physical line 635.

Insert:

```ir
PROC RECORD 1 1
LIT 0
SETLOCAL 0
LABEL RECORDCLEAR
LD TABLE
PUSH
PARAM 0
PUSH
LOCAL 0
ADD
PUSH
LIT 0
SET8
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
PUSH
LIT 40
CULT
JNZ RECORDCLEAR
LIT 0
SETLOCAL 0
LABEL RECORDNAME
LD TABLE
PUSH
PARAM 0
PUSH
LOCAL 0
ADD
PUSH
ADDR IDENT
PUSH
LOCAL 0
ADD
FETCHB
SET8
JZ RECORDFIELDS
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
JMP RECORDNAME
LABEL RECORDFIELDS
PARAM 0
PUSH
LIT 32
ADD
PUSH
LD RECTYPE
PUSH
INVOKE WRITEFIELD 2
PARAM 0
PUSH
LIT 34
ADD
PUSH
LD RECVAL
PUSH
INVOKE WRITEFIELD 2
PARAM 0
PUSH
LIT 36
ADD
PUSH
LD RECLEVEL
PUSH
INVOKE WRITEFIELD 2
PARAM 0
RETURN
```

The following old source remains in place:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit 2

Unchanged source immediately before the edit:

```ir
ST TABLE
LIT 100
PUSH
```

Remove this source at old physical positions 40–43 in RB17.IR:

```ir
LIT 4660
PUSH
INVOKE WRITEFIELD 2
LIT 100
```

Replace it with:

```ir
INVOKE RECORD 1
LIT 1
ST GLOBALS
LIT 34
```

The following old source remains in place:

```ir
CALL TWORD
CALL PRINTNUM
```

### Edit 3

Unchanged source immediately before the edit:

```ir
LIT 22000
ALLOC
ST TABLE
```

Remove this source at old physical positions 38–38 in RB17.IR:

```ir
LIT 100
```

Replace it with:

```ir
LITS "ABC"
CALL SETIDENT
LIT 1
ST RECTYPE
LIT 12345
ST RECVAL
LIT 0
ST RECLEVEL
LIT 0
```

The following old source remains in place:

```ir
PUSH
LIT 4660
```

## Build this stopping point

```dos
COPY RB18.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000024910 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13581 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB18.COM
```

VIEW.BAS must report RB18.COM length 13581 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB18
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
