+++
title = "RB02 \u00b7 A visible word value"
weight = 35
description = "Save the value, current decimal place, and output digit separately."
download = "RB02.IR"
download_group = "toolchain"
+++

Save the value, current decimal place, and output digit separately.

## The working parts

Save the value, current decimal place, and output digit separately. Repeated subtraction chooses one digit at each place. Formatting cannot borrow a parser work cell that remains live across a call.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB01.IR to RB02.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
SETLOCAL 0
JMP PRINTLOOP
LABEL PRINTDONE
```

Insert after old physical line 53.

Insert:

```ir
LIT 0
RETURN

PROC PRINTNUM 0 3
SETLOCAL 0
LIT 10000
SETLOCAL 1
LABEL PRINTPLACE
LIT 48
SETLOCAL 2
LABEL PRINTSUB
LOCAL 0
PUSH
LOCAL 1
CULT
JNZ PRINTDIGIT
LOCAL 0
PUSH
LOCAL 1
SUB
SETLOCAL 0
LOCAL 2
PUSH
LIT 1
ADD
SETLOCAL 2
JMP PRINTSUB
LABEL PRINTDIGIT
LOCAL 2
PUTC
LOCAL 1
PUSH
LIT 10
DIV
SETLOCAL 1
JNZ PRINTPLACE
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–36 in RB01.IR:

```ir
LITS "HI"
CALL PRINT
```

Replace it with:

```ir
LIT 65535
CALL PRINTNUM
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

## Build this stopping point

```dos
COPY RB02.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000007202 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 10153 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB02.COM
```

VIEW.BAS must report RB02.COM length 10153 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB02
```

Require, apart from command echo and the checker's separator:

```text
65535PASS
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
