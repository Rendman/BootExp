+++
title = "33 \u00b7 Recognizing Built-in Services"
weight = 33
description = "A terminated spelling selects an intrinsic record containing an arity and IR text."
download = "RB33.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/066-rb-a-table-of-portable-services/"]
reader_names = 1
+++

## The working parts

A terminated spelling selects an intrinsic record containing an arity and IR text. Compare the whole name. A failed match advances past both fields before considering another entry.

## Enter the source

Copy RB32.IR to RB33.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 1112.

Insert:

```ir
PROC BUILTIN 0 5
LITS "PUTC\01\0POP\nPUTC\0GETC\00\0GETC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0GET8\02\0POP\nGET8\0GET16\02\0POP\nGET16\0SET8\03\0POP\nSET8\0SET16\03\0POP\nSET16\0LOAD8\01\0POP\nFETCHB\0LOAD16\01\0POP\nFETCH\0STORE8\02\0POP\nPUTB\0STORE16\02\0POP\nPUT\0EXIT\01\0POP\nEXIT\0\0"
SETLOCAL 0
LABEL BUILTINNEXT
LOCAL 0
FETCHB
JZ BUILTINNONE
LIT 0
SETLOCAL 1
LIT 1
SETLOCAL 2
LABEL BUILTINCHAR
LOCAL 0
PUSH
LOCAL 1
ADD
FETCHB
SETLOCAL 3
JZ BUILTINARG
LOCAL 3
PUSH
ADDR IDENT
PUSH
LOCAL 1
ADD
FETCHB
CEQ
JNZ BUILTINMATCH
LIT 0
SETLOCAL 2
LABEL BUILTINMATCH
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
JMP BUILTINCHAR
LABEL BUILTINARG
ADDR IDENT
PUSH
LOCAL 1
ADD
FETCHB
JZ BUILTINEXACT
LIT 0
SETLOCAL 2
LABEL BUILTINEXACT
LOCAL 0
PUSH
LOCAL 1
ADD
PUSH
LIT 1
ADD
SETLOCAL 0
LOCAL 0
FETCHB
PUSH
LIT 48
SUB
ST RECVAL
LOCAL 0
PUSH
LIT 2
ADD
SETLOCAL 0
LOCAL 2
JNZ BUILTINFOUND
LABEL BUILTINSKIP
LOCAL 0
FETCHB
SETLOCAL 3
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
LOCAL 3
JNZ BUILTINSKIP
JMP BUILTINNEXT
LABEL BUILTINFOUND
LOCAL 0
RETURN
LABEL BUILTINNONE
LIT 0
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
LITS "ABC"
CALL SETIDENT
LIT 1
```

Remove this source at old physical positions 41–66 in RB32.IR:

```ir
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
LITS "RILL.TMP"
CREATE
ST OUTPUT
STATUS
JNZ IOFAIL
LIT 1
ST OWN
LIT 0
CALL OUTNAME
CALL FLUSH
LD OUTPUT
CLOSE
LIT 0
ST OUTPUT
ST OWN
LIT 0
```

Replace it with:

```ir
CNE
```

The following old source remains in place:

```ir
RETURN
```

### Edit 3

Unchanged source immediately before the edit:

```ir
ST TABLE
LITS "ABC"
CALL SETIDENT
```

Insert after old physical line 39.

Insert:

```ir
CALL BUILTIN
LD RECVAL
PUSH
```

The following old source remains in place:

```ir
LIT 1
ST RECTYPE
```

### Edit 4

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–38 in RB32.IR:

```ir
LIT 22000
ALLOC
ST TABLE
LITS "ABC"
```

Replace it with:

```ir
LITS "PUTC"
```

The following old source remains in place:

```ir
CALL SETIDENT
LIT 1
```

## Build this stopping point

```dos
COPY RB33.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000037617 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 15607 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB33.COM
```

VIEW.BAS must report RB33.COM length 15607 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB33
```

The checker must report PASS. The driver compares the result with 1 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare BUILTIN with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
