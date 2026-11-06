+++
title = "RB32 \u00b7 Emit a saved symbol spelling"
weight = 32
description = "Read the spelling from its stable symbol record."
download = "RB32.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/065-rb-emit-a-saved-symbol-spelling/"]
+++

Read the spelling from its stable symbol record.

## The working parts

Read the spelling from its stable symbol record. Parsing another argument must not silently change the name being emitted.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB31.IR to RB32.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LD FOUND
RETURN
```

Insert after old physical line 857.

Insert:

```ir
PROC OUTNAME 0 3
SETLOCAL 0
LIT 0
SETLOCAL 1
LABEL OUTNAMELOOP
LOCAL 0
PUSH
LOCAL 1
ADD
CALL TBYTE
JZ OUTNAMEDONE
CALL OUTCHAR
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
JMP OUTNAMELOOP
LABEL OUTNAMEDONE
LIT 0
RETURN
```

The following old source remains in place:

```ir
PROC OUTCHAR 0 1
SETLOCAL 0
```

### Edit 2

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
LIT 1
ST OWN
```

Remove this source at old physical positions 42–43 in RB31.IR:

```ir
LIT 7
CALL LABELJUMP
```

Replace it with:

```ir
LIT 0
CALL OUTNAME
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

### Edit 3

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Insert after old physical line 34.

Insert:

```ir
LIT 22000
ALLOC
ST TABLE
LITS "ABC"
CALL SETIDENT
LIT 1
ST RECTYPE
LIT 12345
ST RECVAL
LIT 0
ST RECLEVEL
LIT 0
PUSH
INVOKE RECORD 1
LIT 1
ST GLOBALS
```

The following old source remains in place:

```ir
LITS "RILL.TMP"
CREATE
```

## Build this stopping point

```dos
COPY RB32.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000032621 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15017 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB32.COM
```

VIEW.BAS must report RB32.COM length 15017 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB32
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
ABC
```

VIEW.BAS must show length 3 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

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
