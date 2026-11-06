+++
title = "12 \u00b7 Consuming the Required Token"
weight = 12
description = "Compare the current token before advancing."
download = "RB12.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/045-rb-consume-an-exact-token/"]
reader_names = 1
+++

## The working parts

Compare the current token before advancing. On success, leave the following token ready; a caller must not advance once more accidentally.

## Enter the source

Copy RB11.IR to RB12.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
ST TOK
RETURN
```

Insert after old physical line 529.

Insert:

```ir
PROC EXPECT 1 0
LD TOK
PUSH
PARAM 0
CNE
JNZ SYNTAX
CALL LEX
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
CALL NEXT
CALL LEX
```

Remove this source at old physical positions 42–42 in RB11.IR:

```ir
ADDR STRING
```

Replace it with:

```ir
LIT 43
PUSH
INVOKE EXPECT 1
LITS "OK"
```

The following old source remains in place:

```ir
CALL PRINT
LIT 0
```

## Build this stopping point

```dos
COPY RB12.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000021552 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 12949 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB12.COM
```

VIEW.BAS must report RB12.COM length 12949 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB12.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
+
```

```dos
COPY TRB12.RIL SOURCE.RIL
```

```dos
CHECK RB12
```

Require:

```text
OK
PASS
```

## A rejection or boundary check

Create XRB12.RIL:

```rill
-
```

```dos
COPY XRB12.RIL SOURCE.RIL
CHECK RB12
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Compare EXPECT with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
