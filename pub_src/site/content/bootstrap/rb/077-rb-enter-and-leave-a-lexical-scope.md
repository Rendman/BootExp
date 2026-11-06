+++
title = "RB44 \u00b7 Enter and leave a lexical scope"
weight = 44
description = "Save the active local-name count and next local slot at entry."
download = "RB44.IR"
download_group = "rb"
cartoon = "rill-drawers.png"
aliases = ["/bootstrap/rill/077-rb-enter-and-leave-a-lexical-scope/"]
+++

Save the active local-name count and next local slot at entry.

## The working parts

Save the active local-name count and next local slot at entry. Restore both at the closing brace. This permits a nested binding to shadow an outer one without permanently consuming its name or slot.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB43.IR to RB44.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 59
PUSH
INVOKE EXPECT 1
```

Insert after old physical line 1271.

Insert:

```ir
LIT 0
RETURN

PROC STATEMENT 0 0
LIT 2
PUSH
INVOKE ERROR 1
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 1204.

Insert:

```ir
PROC BLOCK 0 2
LD LOCALCOUNT
SETLOCAL 0
LD NEXTLOCAL
SETLOCAL 1
LD LEVEL
PUSH
LIT 1
ADD
ST LEVEL
PUSH
LIT 16
CUGT
JNZ CAPFAIL
LIT 123
PUSH
INVOKE EXPECT 1
LABEL BLOCKNEXT
LD TOK
PUSH
LIT 125
CEQ
JNZ BLOCKEND
LD TOK
JZ SYNTAX
CALL STATEMENT
JMP BLOCKNEXT
LABEL BLOCKEND
CALL LEX
LOCAL 0
ST LOCALCOUNT
LOCAL 1
ST NEXTLOCAL
LD LEVEL
PUSH
LIT 1
SUB
ST LEVEL
LIT 0
RETURN
```

The following old source remains in place:

```ir
PROC DECLARE 0 2
CALL LEX
```

### Edit 3

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove this source at old physical positions 52–54 in RB43.IR:

```ir
LIT 1
ST LEVEL
CALL DECLARE
```

Replace it with:

```ir
CALL BLOCK
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

## Build this stopping point

```dos
COPY RB44.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000059770 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 19623 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB44.COM
```

VIEW.BAS must report RB44.COM length 19623 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB44.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
{}
```

```dos
COPY TRB44.RIL SOURCE.RIL
```

```dos
CHECK RB44
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir

```

VIEW.BAS must show length 0 bytes. For an empty fragment, length zero is the expected visible result. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRB44.RIL:

```rill
{putc(65);}
```

```dos
COPY XRB44.RIL SOURCE.RIL
CHECK RB44
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
