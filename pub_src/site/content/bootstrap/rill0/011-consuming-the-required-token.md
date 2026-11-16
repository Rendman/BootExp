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

### Edit at old physical position 422

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

### Edit at old physical position 37

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

### Edit at old physical position 35

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
CHECK IRKEEP R11.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 08632 bytes`. Save RESULT.COM as R11.COM. VIEW.BAS must show length 8632.

Create T11.RIL:

```rill
+
```

```dos
CHECK R11 T11.RIL RESULT.IR
```

Require:

```text
OKPASS
```

## Check the new boundary

Save this separate rejected source as X11.RIL:

```rill
-
```

```dos
CHECK R11 X11.RIL RESULT.IR
```

Require:

```text
ERROR 0000000001 CODE 00002
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

