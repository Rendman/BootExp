+++
title = "RB36 \u00b7 Emit a word operation"
weight = 69
description = "Emit the selected IR operation after the right expression is complete."
download = "RB36.IR"
download_group = "toolchain"
+++

Emit the selected IR operation after the right expression is complete.

## The working parts

Emit the selected IR operation after the right expression is complete. This routine translates an operation; it does not evaluate the user program during compilation.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB35.IR to RB36.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 7
RETURN
```

Insert after old physical line 1320.

Insert:

```ir
PROC BINARY 0 1
SETLOCAL 0
PUSH
LIT 43
CEQ
JNZ BINADD
LOCAL 0
PUSH
LIT 45
CEQ
JNZ BINSUB
LOCAL 0
PUSH
LIT 42
CEQ
JNZ BINMUL
LOCAL 0
PUSH
LIT 47
CEQ
JNZ BINDIV
LOCAL 0
PUSH
LIT 37
CEQ
JNZ BINMOD
LOCAL 0
PUSH
LIT 124
CEQ
JNZ BINOR
LOCAL 0
PUSH
LIT 94
CEQ
JNZ BINXOR
LOCAL 0
PUSH
LIT 38
CEQ
JNZ BINAND
LOCAL 0
PUSH
LIT 260
CEQ
JNZ BINSHL
LOCAL 0
PUSH
LIT 261
CEQ
JNZ BINSHR
LOCAL 0
PUSH
LIT 256
CEQ
JNZ BINEQ
LOCAL 0
PUSH
LIT 257
CEQ
JNZ BINNE
LOCAL 0
PUSH
LIT 258
CEQ
JNZ BINLE
LOCAL 0
PUSH
LIT 259
CEQ
JNZ BINGE
LOCAL 0
PUSH
LIT 60
CEQ
JNZ BINLT
LITS "CUGT\r\n"
JMP BINDONE
LABEL BINADD
LITS "ADD\r\n"
JMP BINDONE
LABEL BINSUB
LITS "SUB\r\n"
JMP BINDONE
LABEL BINMUL
LITS "MUL\r\n"
JMP BINDONE
LABEL BINDIV
LITS "DIV\r\n"
JMP BINDONE
LABEL BINMOD
LITS "MOD\r\n"
JMP BINDONE
LABEL BINOR
LITS "OR\r\n"
JMP BINDONE
LABEL BINXOR
LITS "XOR\r\n"
JMP BINDONE
LABEL BINAND
LITS "AND\r\n"
JMP BINDONE
LABEL BINSHL
LITS "SHL\r\n"
JMP BINDONE
LABEL BINSHR
LITS "SHR\r\n"
JMP BINDONE
LABEL BINEQ
LITS "CEQ\r\n"
JMP BINDONE
LABEL BINNE
LITS "CNE\r\n"
JMP BINDONE
LABEL BINLE
LITS "CULE\r\n"
JMP BINDONE
LABEL BINGE
LITS "CUGE\r\n"
JMP BINDONE
LABEL BINLT
LITS "CULT\r\n"
LABEL BINDONE
CALL OUTSTR
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
ST INPUT
STATUS
JNZ IOFAIL
```

Remove this source at old physical positions 40–43 in RB35.IR:

```ir
CALL NEXT
CALL LEX
CALL PREC
CALL PRINTNUM
```

Replace it with:

```ir
LIT 1
ST OWN
LIT 43
CALL BINARY
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

### Edit 3

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–37 in RB35.IR:

```ir
LITS "SOURCE.RIL"
OPEN
ST INPUT
```

Replace it with:

```ir
LITS "RILL.TMP"
CREATE
ST OUTPUT
```

The following old source remains in place:

```ir
STATUS
JNZ IOFAIL
```

## Build this stopping point

```dos
COPY RB36.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000045215 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 16968 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB36.COM
```

VIEW.BAS must report RB36.COM length 16968 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB36
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
ADD
```

VIEW.BAS must show length 5 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

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
