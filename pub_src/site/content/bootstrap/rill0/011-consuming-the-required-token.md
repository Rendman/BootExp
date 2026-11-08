+++
title = "11 \u00b7 Consuming the Required Token"
weight = 11
description = "Build consuming the required token.."
download = "R11.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/011-consume-an-exact-token/", "/bootstrap/rill/11-decimal-word-literals/"]
url = "/bootstrap/rill/011-consuming-the-required-token/"
+++

Build consuming the required token..

## Enter the source

Copy R10.IR to R11.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 413

Unchanged source before the edit:

```ir
ST TOK
RETURN
```

Insert in its place:

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

The following old source remains:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit at old physical position 28

Unchanged source before the edit:

```ir
CALL LEX
LD VALUE
PUSH
```

Remove:

```ir
LIT 65535
CNE
```

Insert in its place:

```ir
INVOKE EXPECT 1
LITS "OK"
CALL PRINT
LIT 0
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 26

Unchanged source before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Remove:

```ir
LD VALUE
```

Insert in its place:

```ir
LIT 43
```

The following old source remains:

```ir
PUSH
LIT 65535
```

## Build and check

```dos
COPY R11.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 07822 bytes`. Save RESULT.COM as R11.COM. VIEW.BAS must show length 7822.

Create T11.RIL:

```rill
+
```

```dos
COPY T11.RIL SOURCE.RIL
```

```dos
CHECK R11
```

Require:

```text
OKPASS
```

## Check the new boundary

Use this separate rejected source:

```rill
-
```

Copy it to SOURCE.RIL and run CHECK R11. Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

