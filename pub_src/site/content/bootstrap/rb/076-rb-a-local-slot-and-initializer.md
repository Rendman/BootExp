+++
title = "RB43 \u00b7 A local slot and initializer"
weight = 43
description = "Allocate a local slot and record its lexical level."
download = "RB43.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/076-rb-a-local-slot-and-initializer/"]
+++

Allocate a local slot and record its lexical level.

## The working parts

Allocate a local slot and record its lexical level. Mark it unavailable during its own initializer, then publish the binding after acceptance. Save its slot across recursive expression parsing.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB42.IR to RB43.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 1202.

Insert:

```ir
PROC DECLARE 0 2
CALL LEX
LITS "MUT"
CALL ISWORD
JZ SYNTAX
CALL LEX
LD TOK
PUSH
LIT 1
CNE
JNZ SYNTAX
LIT 20480
PUSH
LD LOCALCOUNT
PUSH
INVOKE FIND 2
PUSH
LIT 65535
CEQ
JNZ DECLNEW
LD RECLEVEL
PUSH
LD LEVEL
CEQ
JNZ NAMEFAIL
LABEL DECLNEW
LD NEXTLOCAL
PUSH
LIT 16
CUGE
JNZ CAPFAIL
LD NEXTLOCAL
ST RECVAL
SETLOCAL 0
LD LEVEL
ST RECLEVEL
LIT 8
CALL NEWLOCAL
SETLOCAL 1
LD NEXTLOCAL
PUSH
LIT 1
ADD
ST NEXTLOCAL
CALL LEX
LIT 61
PUSH
INVOKE EXPECT 1
LIT 1
PUSH
INVOKE EXPR 1
LOCAL 1
PUSH
LIT 32
ADD
PUSH
LIT 5
PUSH
INVOKE WRITEFIELD 2
LITS "SETLOCAL "
CALL OUTSTR
LOCAL 0
CALL OUTNUM
CALL NEWLINE
LIT 59
PUSH
INVOKE EXPECT 1
LIT 0
RETURN
```

The following old source remains in place:

```ir
PROC BUILTIN 0 5
LITS "PUTC\01\0POP\nPUTC\0GETC\00\0GETC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0GET8\02\0POP\nGET8\0GET16\02\0POP\nGET16\0SET8\03\0POP\nSET8\0SET16\03\0POP\nSET16\0LOAD8\01\0POP\nFETCHB\0LOAD16\01\0POP\nFETCH\0STORE8\02\0POP\nPUTB\0STORE16\02\0POP\nPUT\0EXIT\01\0POP\nEXIT\0\0"
```

### Edit 2

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove this source at old physical positions 52–52 in RB42.IR:

```ir
CALL GLOBALBUFFER
```

Replace it with:

```ir
LIT 1
ST LEVEL
CALL DECLARE
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

## Build this stopping point

```dos
COPY RB43.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000058784 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 19428 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB43.COM
```

VIEW.BAS must report RB43.COM length 19428 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB43.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
let mut x=7;
```

```dos
COPY TRB43.RIL SOURCE.RIL
```

```dos
CHECK RB43
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
LIT 00007
SETLOCAL 00000
```

VIEW.BAS must show length 27 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRB43.RIL:

```rill
let mut x=x;
```

```dos
COPY XRB43.RIL SOURCE.RIL
CHECK RB43
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
