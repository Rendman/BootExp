+++
title = "RB01 \u00b7 A terminated text pointer"
weight = 1
description = "A is a pointer to terminated bytes."
download = "RB01.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/034-rb-a-terminated-text-pointer/"]
+++

A is a pointer to terminated bytes.

## The working parts

A is a pointer to terminated bytes. Save the pointer in a local slot before PUTC changes A. A zero byte ends the walk; it is not written.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Create RB01.IR as plain text. This is its complete source:

```ir
WORD TABLE 0
WORD GLOBALS 0
WORD LOCALCOUNT 0
WORD LEVEL 0
WORD NEXTLOCAL 0
WORD TOK 0
WORD VALUE 0
WORD CH 0
WORD LINE 1
WORD LINEHI 0
WORD INPUT 0
WORD OUTPUT 0
WORD INPOS 0
WORD INLEN 0
WORD OUTLEN 0
WORD TOTAL 0
WORD TOTALHI 0
WORD LABELNO 0
WORD ENDED 0
WORD OWN 0
WORD BACKUP 0
WORD FOUND 0
WORD RECTYPE 0
WORD RECVAL 0
WORD RECLEVEL 0
BUFFER DECIMAL 10
BUFFER INBUF 4096
BUFFER OUTBUF 4096
BUFFER IDENT 32
BUFFER STRING 512
WORD CALLBUILTIN 0
WORD EXPRDEPTH 0

PROC MAIN 0 0
LITS "HI"
CALL PRINT
LIT 0
RETURN

PROC PRINT 0 1
SETLOCAL 0
LABEL PRINTLOOP
LOCAL 0
FETCHB
JZ PRINTDONE
PUTC
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
JMP PRINTLOOP
LABEL PRINTDONE
LIT 0
RETURN

LABEL IOFAIL
LIT 1
JMP FAIL
LABEL SYNTAX
LIT 2
JMP FAIL
LABEL NUMBERFAIL
LIT 3
JMP FAIL
LABEL NAMEFAIL
LIT 4
JMP FAIL
LABEL CAPFAIL
LIT 5
LABEL FAIL
PUSH
INVOKE ERROR 1
LIT 1
EXIT

PROC ERROR 1 0
LIT 1
EXIT
```

## Build this stopping point

```dos
COPY RB01.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000006492 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 10011 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB01.COM
```

VIEW.BAS must report RB01.COM length 10011 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB01
```

Require, apart from command echo and the checker's separator:

```text
HIPASS
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
