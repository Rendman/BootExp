+++
title = "RB34 \u00b7 Call names and forward declarations"
weight = 67
description = "A call can precede its procedure definition."
download = "RB34.IR"
download_group = "toolchain"
+++

A call can precede its procedure definition.

## The working parts

A call can precede its procedure definition. Record its name and required arity as a pending procedure; final acceptance rejects any definition that never arrives. Ordinary undeclared variable use remains an error.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB33.IR to RB34.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 1173.

Insert:

```ir
PROC RESOLVEOPTIONAL 0 1
CALL BUILTIN
ST CALLBUILTIN
JZ RESOLVEUSER
LIT 7
ST RECTYPE
LIT 65535
RETURN
LABEL RESOLVEUSER
LIT 20480
PUSH
LD LOCALCOUNT
PUSH
INVOKE FIND 2
SETLOCAL 0
PUSH
LIT 65535
CNE
JNZ RESOLVEGOT
CALL LOOKGLOBAL
SETLOCAL 0
PUSH
LIT 65535
CNE
JNZ RESOLVEGOT
LIT 65535
ST RECVAL
LIT 0
ST RECLEVEL
LIT 4
CALL NEWGLOBAL
SETLOCAL 0
LIT 4
ST RECTYPE
LABEL RESOLVEGOT
LOCAL 0
RETURN
```

The following old source remains in place:

```ir
LABEL IOFAIL
LIT 1
```

### Edit 2

Unchanged source immediately before the edit:

```ir
PROC MAIN 0 0
LITS "PUTC"
CALL SETIDENT
```

Remove this source at old physical positions 37–38 in RB33.IR:

```ir
CALL BUILTIN
LD RECVAL
```

Replace it with:

```ir
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
CALL RESOLVEOPTIONAL
LD RECTYPE
```

The following old source remains in place:

```ir
CALL PRINTNUM
LIT 0
```

### Edit 3

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–35 in RB33.IR:

```ir
LITS "PUTC"
```

Replace it with:

```ir
LIT 22000
ALLOC
ST TABLE
LITS "ABC"
```

The following old source remains in place:

```ir
CALL SETIDENT
CALL BUILTIN
```

## Build this stopping point

```dos
COPY RB34.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000038627 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15804 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB34.COM
```

VIEW.BAS must report RB34.COM length 15804 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB34
```

Require, apart from command echo and the checker's separator:

```text
00001PASS
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
