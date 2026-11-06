+++
title = "27 \u00b7 Writing a Numeric Operand"
weight = 27
description = "Emit a fixed decimal word spelling through OUTCHAR."
download = "RB27.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/060-rb-print-an-ir-operand/"]
reader_names = 1
+++

## The working parts

Emit a fixed decimal word spelling through OUTCHAR. It uses the same checked output path as instruction names and delimiters.

## Enter the source

Copy RB26.IR to RB27.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 949.

Insert:

```ir
PROC OUTNUM 0 3
SETLOCAL 0
LIT 10000
SETLOCAL 1
LABEL OUTNUMPLACE
LIT 48
SETLOCAL 2
LABEL OUTNUMSUB
LOCAL 0
PUSH
LOCAL 1
CULT
JNZ OUTNUMDIGIT
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
JMP OUTNUMSUB
LABEL OUTNUMDIGIT
LOCAL 2
CALL OUTCHAR
LOCAL 1
PUSH
LIT 10
DIV
SETLOCAL 1
JNZ OUTNUMPLACE
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

Remove this source at old physical positions 42–43 in RB26.IR:

```ir
LITS "HI"
CALL OUTSTR
```

Replace it with:

```ir
LIT 12345
CALL OUTNUM
```

The following old source remains in place:

```ir
CALL FLUSH
LD OUTPUT
```

## Build this stopping point

```dos
COPY RB27.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000030564 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14665 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB27.COM
```

VIEW.BAS must report RB27.COM length 14665 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB27
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 5 bytes. The complete bytes must be:

```text
31 32 33 34 35
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare OUTNUM with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
