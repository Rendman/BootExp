+++
title = "RB45 \u00b7 Statements and structured branches"
weight = 45
description = "Keep assignment destinations, false targets, and loop targets in local slots."
download = "RB45.IR"
download_group = "rb"
aliases = ["/bootstrap/rill/078-rb-statements-and-structured-branches/"]
+++

Keep assignment destinations, false targets, and loop targets in local slots.

## The working parts

Keep assignment destinations, false targets, and loop targets in local slots. An if/else join and a while back edge meet with no expression temporaries. Parse every statement even after an explicit return.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB44.IR to RB45.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
PROC STATEMENT 0 0
LIT 2
PUSH
```

Remove this source at old physical positions 1317–1317 in RB44.IR:

```ir
INVOKE ERROR 1
```

Replace it with:

```ir
INVOKE EXPR 1
LIT 93
PUSH
INVOKE EXPECT 1
LITS "ADD\r\n"
CALL OUTSTR
LABEL STASSIGN
LITS "PUSH\r\n"
CALL OUTSTR
LIT 61
PUSH
INVOKE EXPECT 1
LIT 1
PUSH
INVOKE EXPR 1
LOCAL 1
PUSH
LIT 2
CEQ
JNZ STPUTBYTE
LITS "PUT\r\n"
CALL OUTSTR
JMP STFINISH
LABEL STPUTBYTE
LITS "PUTB\r\n"
CALL OUTSTR
LABEL STFINISH
LIT 59
PUSH
INVOKE EXPECT 1
LIT 0
RETURN
LABEL STCALL
LOCAL 0
PUSH
LD CALLBUILTIN
PUSH
INVOKE CALLARGS 2
JMP STFINISH
LABEL STBLOCK
CALL BLOCK
LIT 0
RETURN
LABEL STDECLARE
CALL DECLARE
LIT 0
RETURN
LABEL STRETURN
CALL LEX
LD TOK
PUSH
LIT 59
CEQ
JNZ STRETURNZERO
LIT 1
PUSH
INVOKE EXPR 1
JMP STRETURNEND
LABEL STRETURNZERO
LITS "LIT 0\r\n"
CALL OUTSTR
LABEL STRETURNEND
LITS "RETURN\r\n"
CALL OUTSTR
JMP STFINISH
LABEL STIF
CALL NEWLABEL
SETLOCAL 0
CALL NEWLABEL
SETLOCAL 1
CALL LEX
LIT 1
PUSH
INVOKE EXPR 1
LITS "JZ"
CALL OUTSTR
LOCAL 0
CALL LABELJUMP
CALL BLOCK
LITS "JMP"
CALL OUTSTR
LOCAL 1
CALL LABELJUMP
LOCAL 0
CALL LABELDEF
LITS "ELSE"
CALL ISWORD
JZ STIFEND
CALL LEX
CALL BLOCK
LABEL STIFEND
LOCAL 1
CALL LABELDEF
LIT 0
RETURN
LABEL STWHILE
CALL NEWLABEL
SETLOCAL 0
CALL NEWLABEL
SETLOCAL 1
LOCAL 0
CALL LABELDEF
CALL LEX
LIT 1
PUSH
INVOKE EXPR 1
LITS "JZ"
CALL OUTSTR
LOCAL 1
CALL LABELJUMP
CALL BLOCK
LITS "JMP"
CALL OUTSTR
LOCAL 0
CALL LABELJUMP
LOCAL 1
CALL LABELDEF
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir

PROC STATEMENT 0 0
LIT 2
```

Insert after old physical line 1315.

Insert:

```ir
CNE
JNZ NAMEFAIL
LITS "ADDR V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
LITS "\r\nPUSH\r\n"
CALL OUTSTR
CALL LEX
LIT 1
```

The following old source remains in place:

```ir
PUSH
INVOKE ERROR 1
```

### Edit 3

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Remove this source at old physical positions 1314–1314 in RB44.IR:

```ir
PROC STATEMENT 0 0
```

Replace it with:

```ir
PROC STATEMENT 0 5
LD TOK
PUSH
LIT 123
CEQ
JNZ STBLOCK
LITS "LET"
CALL ISWORD
JNZ STDECLARE
LITS "IF"
CALL ISWORD
JNZ STIF
LITS "WHILE"
CALL ISWORD
JNZ STWHILE
LITS "RETURN"
CALL ISWORD
JNZ STRETURN
LD TOK
PUSH
LIT 1
CNE
JNZ SYNTAX
CALL RESOLVEOPTIONAL
SETLOCAL 0
LD RECTYPE
SETLOCAL 1
LD RECVAL
SETLOCAL 2
CALL LEX
LD TOK
PUSH
LIT 40
CEQ
JNZ STCALL
LOCAL 0
PUSH
LIT 65535
CEQ
JNZ NAMEFAIL
LD TOK
PUSH
LIT 91
CEQ
JNZ STINDEX
LOCAL 1
PUSH
LIT 1
CEQ
JNZ STGLOBAL
LOCAL 1
PUSH
LIT 5
CEQ
JNZ STLOCAL
LOCAL 1
PUSH
LIT 6
CEQ
JNZ STPARAM
JMP NAMEFAIL
LABEL STGLOBAL
LITS "ADDR V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
CALL NEWLINE
JMP STASSIGN
LABEL STLOCAL
LITS "LADDR "
CALL OUTSTR
LOCAL 2
CALL OUTNUM
CALL NEWLINE
JMP STASSIGN
LABEL STPARAM
LITS "PADDR "
CALL OUTSTR
LOCAL 2
CALL OUTNUM
CALL NEWLINE
JMP STASSIGN
LABEL STINDEX
LOCAL 1
PUSH
```

The following old source remains in place:

```ir
LIT 2
PUSH
```

### Edit 4

Unchanged source immediately before the edit:

```ir
CALL NEXT
CALL LEX
CALL BLOCK
```

Insert after old physical line 52.

Insert:

```ir
LITS "LIT 0\r\nRETURN\r\n"
CALL OUTSTR
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

### Edit 5

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Insert after old physical line 51.

Insert:

```ir
LITS "PROC MAIN 0 16\r\n"
CALL OUTSTR
```

The following old source remains in place:

```ir
CALL BLOCK
CALL FLUSH
```

## Build this stopping point

```dos
COPY RB45.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000065939 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 20629 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB45.COM
```

VIEW.BAS must report RB45.COM length 20629 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB45.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
{let mut x=65;while x<67{putc(x);x=x+1;}}
```

```dos
COPY TRB45.RIL SOURCE.RIL
```

```dos
CHECK RB45
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
PROC MAIN 0 16
LIT 00065
SETLOCAL 00000
LABEL B_00001
LOCAL 00000
PUSH
LIT 00067
CULT
JZ B_00002
LOCAL 00000
PUSH
POP
PUTC
LADDR 00000
PUSH
LOCAL 00000
PUSH
LIT 00001
ADD
PUT
JMP B_00001
LABEL B_00002
LIT 0
RETURN
```

VIEW.BAS must show length 238 bytes. This is a complete program. Copy it to SOURCE.IR, run CHECK IWKEEP, copy the accepted RESULT.ASM to SOURCE.ASM, and run CHECK ASMAKEEP. Require OK and PASS at both steps. VIEW.BAS must report RESULT.COM length 1131. Copy that file to TRY.COM; CHECK TRY displays `AB` and reports PASS.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRB45.RIL:

```rill
{putc();}
```

```dos
COPY XRB45.RIL SOURCE.RIL
CHECK RB45
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
