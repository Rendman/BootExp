+++
title = "33 \u00b7 Parenthesized values"
weight = 33
description = "Compile a numeric value, parenthesized expression, local binding, or accepted builtin call."
download = "R33.IR"
download_group = "tools/rill0"
reader_names = 1
url = "/bootstrap/rill/033-parenthesized-values/"
+++

Compile numeric literals and parenthesized expressions through the existing EXPR routine. Name and call paths are still rejected.

## Enter the source

Copy R32.IR to R33.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1234

Unchanged source before the edit:

```ir
CALL OUTNUM
CALL NEWLINE
CALL LEX
```

Insert in its place:

```ir
JMP PRIMARYDONE
LABEL PRIMARYPAREN
CALL LEX
LIT 1
PUSH
INVOKE EXPR 1
LIT 41
PUSH
INVOKE EXPECT 1
JMP PRIMARYDONE
LABEL PRIMARYDONE
```

The following old source remains:

```ir
LIT 0
RETURN
```

### Edit at old physical position 1228

Unchanged source before the edit:

```ir
LIT 2
CNE
JNZ SYNTAX
```

Insert in its place:

```ir
JMP NAMEFAIL
LABEL PRIMARYNUM
```

The following old source remains:

```ir
LITS "LIT "
CALL OUTSTR
```

### Edit at old physical position 1226

Unchanged source before the edit:

```ir
LD TOK
PUSH
LIT 2
```

Insert in its place:

```ir
CEQ
JNZ PRIMARYNUM
LD TOK
PUSH
LIT 40
CEQ
JNZ PRIMARYPAREN
LD TOK
PUSH
LIT 1
```

The following old source remains:

```ir
CNE
JNZ SYNTAX
```

### Edit at old physical position 1222

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Remove:

```ir
PROC PRIMARY 0 0
```

Insert in its place:

```ir
PROC PRIMARY 0 4
```

The following old source remains:

```ir
LD TOK
PUSH
```

## Build and check

```dos
COPY R33.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 15154 bytes`. Save RESULT.COM as R33.COM. VIEW.BAS must show length 15154.

Create T33.RIL:

```rill
(1+2)
```

```dos
COPY T33.RIL SOURCE.RIL
```

```dos
CHECK R33
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 33 bytes and these complete bytes:

```text
4C 49 54 20 30 30 30 30 31 0D 0A 50 55 53 48 0D
0A 4C 49 54 20 30 30 30 30 32 0D 0A 41 44 44 0D
0A
```

This is a fragment for inspection. Delete the deliberately created RILL.TMP after checking it.

## Check the new boundary

Use this separate rejected source:

```rill
ABC
```

Copy it to SOURCE.RIL and run CHECK R33. Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

