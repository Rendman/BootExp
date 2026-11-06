+++
title = "RB26 \u00b7 Append a text template"
weight = 59
description = "Walk a terminated template while preserving its pointer."
download = "RB26.IR"
download_group = "toolchain"
+++

Walk a terminated template while preserving its pointer.

## The working parts

Walk a terminated template while preserving its pointer. Normalize a bare LF in an IR template to CR/LF while retaining existing CR/LF. Quoted source escapes are still printable backslash spellings at this point.

The entry diagnostic exercises the printed helper. Rejecting placeholders identify forms outside this stopping point. A diagnostic that emits only an IR fragment is inspected as text; it is not a complete compiler or output program.

## Enter the source

Copy RB25.IR to RB26.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 917.

Insert:

```ir
PROC OUTSTR 0 2
SETLOCAL 0
LIT 0
SETLOCAL 1
LABEL OUTSTRLOOP
LOCAL 0
FETCHB
JZ OUTSTRDONE
PUSH
LIT 10
CNE
JNZ OUTSTRBYTE
LOCAL 1
PUSH
LIT 13
CEQ
JNZ OUTSTRBYTE
LIT 13
CALL OUTCHAR
LABEL OUTSTRBYTE
LOCAL 0
FETCHB
SETLOCAL 1
CALL OUTCHAR
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
JMP OUTSTRLOOP
LABEL OUTSTRDONE
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

Remove this source at old physical positions 42–43 in RB25.IR:

```ir
LIT 65
CALL OUTCHAR
```

Replace it with:

```ir
LITS "HI"
CALL OUTSTR
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

## Build this stopping point

```dos
COPY RB26.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000030049 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14546 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB26.COM
```

VIEW.BAS must report RB26.COM length 14546 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB26
```

Require, apart from command echo and the checker's separator:

```text
OK RILL.TMP
PASS
```

TYPE RILL.TMP. Its complete text is:

```ir
HI
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
