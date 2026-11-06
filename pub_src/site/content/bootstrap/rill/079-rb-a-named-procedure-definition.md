+++
title = "RB46 \u00b7 A named procedure definition"
weight = 79
description = "Record the procedure name before scanning parameters, verify any earlier call arity, and create parameter bindings."
download = "RB46.IR"
download_group = "toolchain"
+++

Record the procedure name before scanning parameters, verify any earlier call arity, and create parameter bindings.

## The working parts

Record the procedure name before scanning parameters, verify any earlier call arity, and create parameter bindings. PROC reserves the bounded local frame. Every normal fall-through ends with return value zero.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB45.IR to RB46.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 59
PUSH
INVOKE EXPECT 1
```

Insert after old physical line 1203.

Insert:

```ir
LIT 0
RETURN

PROC FUNCTION 0 4
CALL LEX
LD TOK
PUSH
LIT 1
CNE
JNZ SYNTAX
CALL LOOKGLOBAL
SETLOCAL 0
PUSH
LIT 65535
CEQ
JNZ NEWFUNCTION
LD RECTYPE
PUSH
LIT 4
CNE
JNZ NAMEFAIL
JMP FUNCTIONNAME
LABEL NEWFUNCTION
LIT 65535
ST RECVAL
LIT 0
ST RECLEVEL
LIT 4
CALL NEWGLOBAL
SETLOCAL 0
LABEL FUNCTIONNAME
LOCAL 0
PUSH
LIT 34
ADD
CALL TWORD
SETLOCAL 2
LOCAL 0
PUSH
LIT 32
ADD
PUSH
LIT 3
PUSH
INVOKE WRITEFIELD 2
LIT 0
ST LOCALCOUNT
ST NEXTLOCAL
ST LEVEL
SETLOCAL 1
CALL LEX
LIT 40
PUSH
INVOKE EXPECT 1
LABEL PARAMLOOP
LD TOK
PUSH
LIT 41
CEQ
JNZ PARAMDONE
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
CNE
JNZ NAMEFAIL
LOCAL 1
PUSH
LIT 16
CUGE
JNZ CAPFAIL
LOCAL 1
ST RECVAL
LIT 0
ST RECLEVEL
LIT 6
CALL NEWLOCAL
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
CALL LEX
LD TOK
PUSH
LIT 41
CEQ
JNZ PARAMDONE
LIT 44
PUSH
INVOKE EXPECT 1
JMP PARAMLOOP
LABEL PARAMDONE
LOCAL 2
PUSH
LIT 65535
CEQ
JNZ PARAMACCEPTED
LOCAL 2
PUSH
LOCAL 1
CNE
JNZ NAMEFAIL
LABEL PARAMACCEPTED
LOCAL 0
PUSH
LIT 34
ADD
PUSH
LOCAL 1
PUSH
INVOKE WRITEFIELD 2
LITS "PROC F_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
LIT 32
CALL OUTCHAR
LOCAL 1
CALL OUTNUM
LITS " 16\r\n"
CALL OUTSTR
CALL LEX
CALL BLOCK
LITS "LIT 0\r\nRETURN\r\n"
CALL OUTSTR
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove this source at old physical positions 52–55 in RB45.IR:

```ir
LITS "PROC MAIN 0 16\r\n"
CALL OUTSTR
CALL BLOCK
LITS "LIT 0\r\nRETURN\r\n"
```

Replace it with:

```ir
CALL FUNCTION
LITS "PROC MAIN 0 0\r\nINVOKE F_MAIN 0\r\nRETURN\r\n"
```

The following old source remains in place:

```ir
CALL OUTSTR
CALL FLUSH
```

## Build this stopping point

```dos
COPY RB46.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000068989 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 21191 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB46.COM
```

VIEW.BAS must report RB46.COM length 21191 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB46.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
fn main(){putc(65);return 0;}
```

```dos
COPY TRB46.RIL SOURCE.RIL
```

```dos
CHECK RB46
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
PROC F_MAIN 00000 16
LIT 00065
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

VIEW.BAS must show length 124 bytes. This is a complete program. Copy it to SOURCE.IR, run CHECK IWKEEP, copy the accepted RESULT.ASM to SOURCE.ASM, and run CHECK ASMAKEEP. Require OK and PASS at both steps. VIEW.BAS must report RESULT.COM length 1109. Copy that file to TRY.COM; CHECK TRY displays `A` and reports PASS.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRB46.RIL:

```rill
fn main(a,a){}
```

```dos
COPY XRB46.RIL SOURCE.RIL
CHECK RB46
```

Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
