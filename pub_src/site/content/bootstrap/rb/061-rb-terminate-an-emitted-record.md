+++
title = "28 \u00b7 Ending a Line of Generated Code"
weight = 28
description = "End an emitted IR record with carriage return and line feed."
download = "RB28.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/061-rb-terminate-an-emitted-record/"]
reader_names = 1
+++

## The working parts

End an emitted IR record with carriage return and line feed. A record terminator and a zero byte ending an in-memory string have different jobs.

## Enter the source

Copy RB27.IR to RB28.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
LIT 0
RETURN
```

Insert after old physical line 985.

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

Require IR86 `OK RESULT.ASM 0000030761 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 14697 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB28.COM
```

VIEW.BAS must report RB28.COM length 14697 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB28
```

The checker must report PASS. Inspect the emitted file below.

Use VIEW.BAS to inspect RILL.TMP. Require length 2 bytes. The complete bytes must be:

```text
0D 0A
```

This is an IR fragment for inspection. Do not translate it as a complete program or execute any file with its name.

After inspection, delete this deliberately created RILL.TMP before another checkpoint. The file is diagnostic text, not an interrupted accepted compiler build.

## If the result differs

Compare NEWLINE with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
