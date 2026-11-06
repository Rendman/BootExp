+++
title = "RB28 \u00b7 Terminate an emitted record"
weight = 61
description = "End an emitted IR record with carriage return and line feed."
download = "RB28.IR"
download_group = "toolchain"
+++

End an emitted IR record with carriage return and line feed.

## The working parts

End an emitted IR record with carriage return and line feed. A record terminator and a zero byte ending an in-memory string have different jobs.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB27.IR to RB28.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 987.

Insert:

```ir
PROC NEWLINE 0 0
LITS "\r\n"
CALL OUTSTR
LIT 0
RETURN
```

The following old source remains in place:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit 2

Unchanged source immediately before the edit:

```ir
JNZ IOFAIL
LIT 1
ST OWN
```

Remove this source at old physical positions 42–43 in RB27.IR:

```ir
LIT 12345
CALL OUTNUM
```

Replace it with:

```ir
CALL NEWLINE
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

## Build this stopping point

```dos
COPY RB28.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000030960 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14720 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB28.COM
```

VIEW.BAS must report RB28.COM length 14720 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB28
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir

```

VIEW.BAS must show length 2 bytes. This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

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
