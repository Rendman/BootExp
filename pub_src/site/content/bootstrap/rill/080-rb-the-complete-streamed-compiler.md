+++
title = "RB47 \u00b7 The complete streamed compiler"
weight = 80
description = "Open the fixed source, stream accepted IR through an owned temporary file, and verify all pending procedures."
download = "RB47.IR"
download_group = "toolchain"
+++

Open the fixed source, stream accepted IR through an owned temporary file, and verify all pending procedures.

## The working parts

Open the fixed source, stream accepted IR through an owned temporary file, and verify all pending procedures. Require an argument-free main. Publish only after parsing, source close, flush, and output close succeed.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB46.IR to RB47.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
CALL PRINT
LIT 1
EXIT
```

Remove this source at old physical positions 2465–2465 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC PRINT32 2 8
PARAM 0
```

### Edit 2

Unchanged source immediately before the edit:

```ir
INVOKE ERROR 1
LIT 1
EXIT
```

Remove this source at old physical positions 2422–2422 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC ERROR 1 0
LD INPUT
```

### Edit 3

Unchanged source immediately before the edit:

```ir
LABEL PRIMARYDONE
LIT 0
RETURN
```

Remove this source at old physical positions 2402–2402 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
LABEL IOFAIL
LIT 1
```

### Edit 4

Unchanged source immediately before the edit:

```ir
CALL OUTSTR
LIT 0
RETURN
```

Remove this source at old physical positions 2176–2176 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC PRIMARY 0 4
LD TOK
```

### Edit 5

Unchanged source immediately before the edit:

```ir
ST EXPRDEPTH
LIT 0
RETURN
```

Remove this source at old physical positions 2049–2049 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC BINARY 0 1
SETLOCAL 0
```

### Edit 6

Unchanged source immediately before the edit:

```ir
LABEL PRECSEVEN
LIT 7
RETURN
```

Remove this source at old physical positions 2007–2007 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC EXPR 1 2
LD EXPRDEPTH
```

### Edit 7

Unchanged source immediately before the edit:

```ir
CALL NEWLINE
LIT 0
RETURN
```

Remove this source at old physical positions 1902–1902 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC PREC 0 0
LD TOK
```

### Edit 8

Unchanged source immediately before the edit:

```ir
LABEL RESOLVEGOT
LOCAL 0
RETURN
```

Remove this source at old physical positions 1791–1791 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC CALLARGS 2 3
LIT 0
```

### Edit 9

Unchanged source immediately before the edit:

```ir
LABEL BUILTINNONE
LIT 0
RETURN
```

Remove this source at old physical positions 1753–1753 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC RESOLVEOPTIONAL 0 1
CALL BUILTIN
```

### Edit 10

Unchanged source immediately before the edit:

```ir
CALL LABELDEF
LIT 0
RETURN
```

Remove this source at old physical positions 1666–1666 in RB46.IR:

```ir

```

Replace it with:

```ir
WORD CALLBUILTIN 0
WORD EXPRDEPTH 0
```

The following old source remains in place:

```ir
PROC BUILTIN 0 5
LITS "PUTC\01\0POP\nPUTC\0GETC\00\0GETC\0STATUS\00\0STATUS\0OPEN\01\0POP\nOPEN\0CREATE\01\0POP\nCREATE\0CLOSE\01\0POP\nCLOSE\0READ\03\0POP\nREAD\0WRITE\03\0POP\nWRITE\0EXISTS\01\0POP\nEXISTS\0DELETE\01\0POP\nDELETE\0RENAME\02\0POP\nRENAME\0ALLOC\01\0POP\nALLOC\0FREE\01\0POP\nFREEBLOCK\0GET8\02\0POP\nGET8\0GET16\02\0POP\nGET16\0SET8\03\0POP\nSET8\0SET16\03\0POP\nSET16\0LOAD8\01\0POP\nFETCHB\0LOAD16\01\0POP\nFETCH\0STORE8\02\0POP\nPUTB\0STORE16\02\0POP\nPUT\0EXIT\01\0POP\nEXIT\0\0"
```

### Edit 11

Unchanged source immediately before the edit:

```ir
INVOKE EXPECT 1
LIT 0
RETURN
```

Remove this source at old physical positions 1449–1449 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC STATEMENT 0 5
LD TOK
```

### Edit 12

Unchanged source immediately before the edit:

```ir
ST LEVEL
LIT 0
RETURN
```

Remove this source at old physical positions 1379–1379 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC DECLARE 0 2
CALL LEX
```

### Edit 13

Unchanged source immediately before the edit:

```ir
CALL OUTSTR
LIT 0
RETURN
```

Remove this source at old physical positions 1338–1338 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC BLOCK 0 2
LD LOCALCOUNT
```

### Edit 14

Unchanged source immediately before the edit:

```ir
INVOKE EXPECT 1
LIT 0
RETURN
```

Remove this source at old physical positions 1204–1204 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC FUNCTION 0 4
CALL LEX
```

### Edit 15

Unchanged source immediately before the edit:

```ir
INVOKE EXPECT 1
LIT 0
RETURN
```

Remove this source at old physical positions 1156–1156 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC GLOBALBUFFER 0 1
CALL LEX
```

### Edit 16

Unchanged source immediately before the edit:

```ir
JNZ PRINTPLACE
LIT 0
RETURN
```

Remove this source at old physical positions 1109–1109 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC GLOBALWORD 0 1
CALL LEX
```

### Edit 17

Unchanged source immediately before the edit:

```ir
LABEL PRINTDONE
LIT 0
RETURN
```

Remove this source at old physical positions 1073–1073 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC PRINTNUM 0 3
SETLOCAL 0
```

### Edit 18

Unchanged source immediately before the edit:

```ir
CALL OUTSTR
LIT 0
RETURN
```

Remove this source at old physical positions 1056–1056 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit 19

Unchanged source immediately before the edit:

```ir
CALL NEWLINE
LIT 0
RETURN
```

Remove this source at old physical positions 1050–1050 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC NEWLINE 0 0
LITS "\r\n"
```

### Edit 20

Unchanged source immediately before the edit:

```ir
CALL NEWLINE
LIT 0
RETURN
```

Remove this source at old physical positions 1040–1040 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC LABELJUMP 0 1
SETLOCAL 0
```

### Edit 21

Unchanged source immediately before the edit:

```ir
JZ CAPFAIL
LD LABELNO
RETURN
```

Remove this source at old physical positions 1030–1030 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC LABELDEF 0 1
SETLOCAL 0
```

### Edit 22

Unchanged source immediately before the edit:

```ir
JNZ OUTNUMPLACE
LIT 0
RETURN
```

Remove this source at old physical positions 1020–1020 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC NEWLABEL 0 0
LD LABELNO
```

### Edit 23

Unchanged source immediately before the edit:

```ir
LABEL OUTSTRDONE
LIT 0
RETURN
```

Remove this source at old physical positions 984–984 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC OUTNUM 0 3
SETLOCAL 0
```

### Edit 24

Unchanged source immediately before the edit:

```ir
LABEL FLUSHDONE
LIT 0
RETURN
```

Remove this source at old physical positions 950–950 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC OUTSTR 0 2
SETLOCAL 0
```

### Edit 25

Unchanged source immediately before the edit:

```ir
LABEL OUTCHARDONE
LIT 0
RETURN
```

Remove this source at old physical positions 927–927 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC FLUSH 0 1
LD OUTLEN
```

### Edit 26

Unchanged source immediately before the edit:

```ir
LABEL OUTNAMEDONE
LIT 0
RETURN
```

Remove this source at old physical positions 890–890 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC OUTCHAR 0 1
SETLOCAL 0
```

### Edit 27

Unchanged source immediately before the edit:

```ir
LABEL RESOLVED
LD FOUND
RETURN
```

Remove this source at old physical positions 868–868 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC OUTNAME 0 3
SETLOCAL 0
```

### Edit 28

Unchanged source immediately before the edit:

```ir
PUSH
INVOKE FIND 2
RETURN
```

Remove this source at old physical positions 847–847 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC RESOLVE 0 0
LIT 20480
```

### Edit 29

Unchanged source immediately before the edit:

```ir
PUSH
INVOKE RECORD 1
RETURN
```

Remove this source at old physical positions 839–839 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC LOOKGLOBAL 0 0
LIT 0
```

### Edit 30

Unchanged source immediately before the edit:

```ir
PUSH
INVOKE RECORD 1
RETURN
```

Remove this source at old physical positions 814–814 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC NEWLOCAL 0 1
ST RECTYPE
```

### Edit 31

Unchanged source immediately before the edit:

```ir
INVOKE WRITEFIELD 2
PARAM 0
RETURN
```

Remove this source at old physical positions 792–792 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC NEWGLOBAL 0 1
ST RECTYPE
```

### Edit 32

Unchanged source immediately before the edit:

```ir
PARAM 1
SET16
RETURN
```

Remove this source at old physical positions 719–719 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC RECORD 1 1
LIT 0
```

### Edit 33

Unchanged source immediately before the edit:

```ir
LABEL FINDNONE
LIT 65535
RETURN
```

Remove this source at old physical positions 710–710 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC WRITEFIELD 2 0
LD TABLE
```

### Edit 34

Unchanged source immediately before the edit:

```ir
LOCAL 0
GET8
RETURN
```

Remove this source at old physical positions 643–643 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC FIND 2 4
PARAM 1
```

### Edit 35

Unchanged source immediately before the edit:

```ir
LOCAL 0
GET16
RETURN
```

Remove this source at old physical positions 635–635 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC TBYTE 0 1
SETLOCAL 0
```

### Edit 36

Unchanged source immediately before the edit:

```ir
LABEL SETIDDONE
LIT 0
RETURN
```

Remove this source at old physical positions 627–627 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC TWORD 0 1
SETLOCAL 0
```

### Edit 37

Unchanged source immediately before the edit:

```ir
LABEL WORDNO
LIT 0
RETURN
```

Remove this source at old physical positions 600–600 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC SETIDENT 0 2
SETLOCAL 0
```

### Edit 38

Unchanged source immediately before the edit:

```ir
CALL LEX
LIT 0
RETURN
```

Remove this source at old physical positions 558–558 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC ISWORD 0 2
SETLOCAL 0
```

### Edit 39

Unchanged source immediately before the edit:

```ir
LIT 0
ST TOK
RETURN
```

Remove this source at old physical positions 548–548 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC EXPECT 1 0
LD TOK
```

### Edit 40

Unchanged source immediately before the edit:

```ir
JNZ LETTERNO
LIT 1
RETURN
```

Remove this source at old physical positions 205–205 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC LEX 0 4
LABEL LEXSTART
```

### Edit 41

Unchanged source immediately before the edit:

```ir
LABEL LETTERNO
LIT 0
RETURN
```

Remove this source at old physical positions 191–191 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC DIGIT 1 0
PARAM 0
```

### Edit 42

Unchanged source immediately before the edit:

```ir
LIT 0
ST CH
RETURN
```

Remove this source at old physical positions 158–158 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC LETTER 1 0
PARAM 0
```

### Edit 43

Unchanged source immediately before the edit:

```ir
CALL PRINT
LIT 0
RETURN
```

Remove this source at old physical positions 65–65 in RB46.IR:

```ir

```

There is no replacement source.

The following old source remains in place:

```ir
PROC NEXT 0 1
LD CH
```

### Edit 44

Unchanged source immediately before the edit:

```ir
LIT 0
ST OUTPUT
ST OWN
```

Remove this source at old physical positions 61–61 in RB46.IR:

```ir
LITS "OK RILL.TMP\r\n"
```

Replace it with:

```ir
LD BACKUP
JZ PUBLISHED
LITS "RILL.BAK"
DELETE
STATUS
JNZ IOFAIL
LABEL PUBLISHED
LD TABLE
FREEBLOCK
STATUS
JNZ IOFAIL
LITS "OK RESULT.IR "
CALL PRINT
LD TOTALHI
PUSH
LD TOTAL
PUSH
INVOKE PRINT32 2
LABEL REPORTDONE
LITS "\r\n"
```

The following old source remains in place:

```ir
CALL PRINT
LIT 0
```

### Edit 45

Unchanged source immediately before the edit:

```ir
LD OUTPUT
CLOSE
LIT 0
```

Remove this source at old physical positions 59–59 in RB46.IR:

```ir
ST OUTPUT
```

There is no replacement source.

The following old source remains in place:

```ir
ST OWN
LITS "OK RILL.TMP\r\n"
```

### Edit 46

Unchanged source immediately before the edit:

```ir
CALL FLUSH
LD OUTPUT
CLOSE
```

Insert after old physical line 57.

Insert:

```ir
STATUS
JNZ IOFAIL
LITS "RESULT.IR"
EXISTS
ST FOUND
STATUS
JNZ IOFAIL
LD FOUND
JZ NOOLD
LITS "RESULT.IR"
PUSH
LITS "RILL.BAK"
RENAME
STATUS
JNZ IOFAIL
LIT 1
ST BACKUP
LABEL NOOLD
LITS "RILL.TMP"
PUSH
LITS "RESULT.IR"
RENAME
STATUS
JNZ IOFAIL
```

The following old source remains in place:

```ir
LIT 0
ST OUTPUT
```

### Edit 47

Unchanged source immediately before the edit:

```ir
ST INPUT
STATUS
JNZ IOFAIL
```

Remove this source at old physical positions 50–54 in RB46.IR:

```ir
CALL NEXT
CALL LEX
CALL FUNCTION
LITS "PROC MAIN 0 0\r\nINVOKE F_MAIN 0\r\nRETURN\r\n"
CALL OUTSTR
```

There is no replacement source.

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

### Edit 48

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
LIT 1
ST OWN
```

Remove this source at old physical positions 45–47 in RB46.IR:

```ir
LITS "SOURCE.RIL"
OPEN
ST INPUT
```

Replace it with:

```ir
LIT 22000
ALLOC
ST TABLE
STATUS
JNZ CAPFAIL
CALL NEXT
CALL LEX
LABEL TOP
LD TOK
JZ COMPLETE
LITS "FN"
CALL ISWORD
JNZ TOPFN
LITS "LET"
CALL ISWORD
JNZ TOPWORD
LITS "BYTES"
CALL ISWORD
JNZ TOPBYTES
JMP SYNTAX
LABEL TOPFN
CALL FUNCTION
JMP TOP
LABEL TOPWORD
CALL GLOBALWORD
JMP TOP
LABEL TOPBYTES
CALL GLOBALBUFFER
JMP TOP
LABEL COMPLETE
LITS "MAIN"
CALL SETIDENT
LIT 0
PUSH
LD GLOBALS
PUSH
INVOKE FIND 2
PUSH
LIT 65535
CEQ
JNZ NAMEFAIL
LD RECTYPE
PUSH
LIT 3
CNE
JNZ NAMEFAIL
LD RECVAL
JNZ NAMEFAIL
LIT 0
ST FOUND
LABEL CHECKGLOBALS
LD FOUND
PUSH
LD GLOBALS
CUGE
JNZ CHECKDONE
LD FOUND
PUSH
LIT 40
MUL
PUSH
LIT 32
ADD
CALL TWORD
PUSH
LIT 4
CEQ
JNZ NAMEFAIL
LD FOUND
PUSH
LIT 1
ADD
ST FOUND
JMP CHECKGLOBALS
LABEL CHECKDONE
LITS "PROC MAIN 0 0\r\nINVOKE F_MAIN 0\r\nRETURN\r\n"
CALL OUTSTR
LD INPUT
CLOSE
```

The following old source remains in place:

```ir
STATUS
JNZ IOFAIL
```

### Edit 49

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–37 in RB46.IR:

```ir
LIT 22000
ALLOC
ST TABLE
```

Replace it with:

```ir
LITS "RILL.TMP"
EXISTS
JNZ CAPFAIL
LITS "RILL.BAK"
EXISTS
JNZ CAPFAIL
LITS "SOURCE.RIL"
OPEN
ST INPUT
STATUS
JNZ IOFAIL
```

The following old source remains in place:

```ir
LITS "RILL.TMP"
CREATE
```

### Edit 50

Unchanged source immediately before the edit:

```ir
BUFFER OUTBUF 4096
BUFFER IDENT 32
BUFFER STRING 512
```

Remove this source at old physical positions 31–33 in RB46.IR:

```ir
WORD CALLBUILTIN 0
WORD EXPRDEPTH 0
```

There is no replacement source.

The following old source remains in place:

```ir
PROC MAIN 0 0
LIT 22000
```

### Edit 51

Insert after old physical line 0.

Insert:

```ir
; The compiler seed is written in IR86.
```

The following old source remains in place:

```ir
WORD TABLE 0
WORD GLOBALS 0
```

## Build this stopping point

```dos
COPY RB47.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000072692 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 21818 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB47.COM
```

VIEW.BAS must report RB47.COM length 21818 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB47.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
fn main(){putc(72);putc(73);return 0;}
```

```dos
COPY TRB47.RIL SOURCE.RIL
```

```dos
CHECK RB47
```

Require, apart from command echo and the checker's separator:

```text
OK RESULT.IR 0000000152
PASS
```

TYPE RESULT.IR. Its complete text is:

```ir
PROC F_MAIN 00000 16
LIT 00072
PUSH
POP
PUTC
LIT 00073
PUSH
POP
PUTC
LIT 00000
RETURN
LIT 0
RETURN
PROC MAIN 0 0
INVOKE F_MAIN 0
RETURN
```

VIEW.BAS must show length 152 bytes. This is a complete program. Copy it to SOURCE.IR, run CHECK IWKEEP, copy the accepted RESULT.ASM to SOURCE.ASM, and run CHECK ASMAKEEP. Require OK and PASS at both steps. VIEW.BAS must report RESULT.COM length 1117. Copy that file to TRY.COM; CHECK TRY displays `HI` and reports PASS.

## A rejection or boundary check

Create XRB47.RIL:

```rill
fn main(){return 65536;}
```

```dos
COPY XRB47.RIL SOURCE.RIL
CHECK RB47
```

Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.

Preserve RB47.COM as RILLBOOT.COM and RB47.IR as RILLBOOT.IR. This compiler seed was built entirely through the native IR86 and ASM86A tools.
