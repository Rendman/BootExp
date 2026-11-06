+++
title = "42 \u00b7 Compiling a Byte Buffer"
weight = 42
description = "Declare a nonempty global byte extent."
download = "RB42.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/075-rb-a-global-byte-extent/"]
reader_names = 1
+++

## The working parts

Declare a nonempty global byte extent. The buffer is materialized in the COM image. Extra allocated blocks are a different service and are not pointers into this declaration.

## Enter the source

Copy RB41.IR to RB42.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 1152.

Insert:

```ir
PROC GLOBALBUFFER 0 1
CALL LEX
LD TOK
PUSH
LIT 1
CNE
JNZ SYNTAX
CALL LOOKGLOBAL
PUSH
LIT 65535
CNE
JNZ NAMEFAIL
LIT 0
ST RECVAL
ST RECLEVEL
LIT 2
CALL NEWGLOBAL
SETLOCAL 0
CALL LEX
LIT 91
PUSH
INVOKE EXPECT 1
LD TOK
PUSH
LIT 2
CNE
JNZ SYNTAX
LD VALUE
JZ CAPFAIL
LITS "BUFFER V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
LIT 32
CALL OUTCHAR
LD VALUE
CALL OUTNUM
CALL NEWLINE
CALL LEX
LIT 93
PUSH
INVOKE EXPECT 1
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

Remove this source at old physical positions 52–52 in RB41.IR:

```ir
CALL GLOBALWORD
```

Replace it with:

```ir
CALL GLOBALBUFFER
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

## Build this stopping point

```dos
COPY RB42.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000056981 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 19097 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB42.COM
```

VIEW.BAS must report RB42.COM length 19097 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB42.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
bytes abc[8];
```

```dos
COPY TRB42.RIL SOURCE.RIL
```

```dos
CHECK RB42
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 20 bytes. The complete bytes must be:

```text
42 55 46 46 45 52 20 56 5F 41 42 43 20 30 30 30
30 38 0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## A rejection or boundary check

Create XRB42.RIL:

```rill
bytes abc[0];
```

```dos
COPY XRB42.RIL SOURCE.RIL
CHECK RB42
```

Require:

```text
ERROR 0000000001 CODE 00005
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare GLOBALBUFFER with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
