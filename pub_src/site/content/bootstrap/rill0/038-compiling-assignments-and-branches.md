+++
title = "38 \u00b7 Compiling Assignments and Branches"
weight = 38
description = "Compile assignments, local declarations, if/else, and while with saved branch destinations."
download = "R38.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/038-statements-and-structured-branches/"]
url = "/bootstrap/rill/038-compiling-assignments-and-branches/"
+++

Compile assignments, local declarations, if/else, and while with saved branch destinations. Every branch boundary has an empty expression stack.

## Enter the source

Copy R37.IR to R38.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1042

Unchanged source before the edit:

```ir
PROC STATEMENT 0 0
LIT 2
PUSH
```

Remove:

```ir
INVOKE ERROR 1
```

Insert in its place:

```ir
LIT 123
CEQ
JNZ STBLOCK
LITS "LET"
CALL ISWORD
JNZ STDECLARE
LITS "IF"
CALL ISWORD
JNZ STIF
LITS "WHILE"
CALL ISWORD
JNZ STWHILE
LITS "RETURN"
CALL ISWORD
JNZ STRETURN
LD TOK
PUSH
LIT 1
CNE
JNZ SYNTAX
CALL RESOLVEOPTIONAL
SETLOCAL 0
LD RECTYPE
SETLOCAL 1
LD RECVAL
SETLOCAL 2
CALL LEX
LD TOK
PUSH
LIT 40
CEQ
JNZ STCALL
LOCAL 0
PUSH
LIT 65535
CEQ
JNZ NAMEFAIL
LOCAL 1
PUSH
LIT 5
CEQ
JNZ STLOCAL
JMP NAMEFAIL
LABEL STLOCAL
LITS "LADDR "
CALL OUTSTR
LOCAL 2
CALL OUTNUM
CALL NEWLINE
JMP STASSIGN
LABEL STASSIGN
LITS "PUSH\r\n"
CALL OUTSTR
LIT 61
PUSH
INVOKE EXPECT 1
LIT 1
PUSH
INVOKE EXPR 1
LITS "PUT\r\n"
CALL OUTSTR
JMP STFINISH
LABEL STFINISH
LIT 59
PUSH
INVOKE EXPECT 1
LIT 0
RETURN
LABEL STCALL
LOCAL 0
PUSH
LD CALLBUILTIN
PUSH
INVOKE CALLARGS 2
JMP STFINISH
LABEL STBLOCK
CALL BLOCK
LIT 0
RETURN
LABEL STDECLARE
CALL DECLARE
LIT 0
RETURN
LABEL STRETURN
CALL LEX
LD TOK
PUSH
LIT 59
CEQ
JNZ STRETURNZERO
LIT 1
PUSH
INVOKE EXPR 1
JMP STRETURNEND
LABEL STRETURNZERO
LITS "LIT 0\r\n"
CALL OUTSTR
LABEL STRETURNEND
LITS "RETURN\r\n"
CALL OUTSTR
JMP STFINISH
LABEL STIF
CALL NEWLABEL
SETLOCAL 0
CALL NEWLABEL
SETLOCAL 1
CALL LEX
LIT 1
PUSH
INVOKE EXPR 1
LITS "JZ"
CALL OUTSTR
LOCAL 0
CALL LABELJUMP
CALL BLOCK
LITS "JMP"
CALL OUTSTR
LOCAL 1
CALL LABELJUMP
LOCAL 0
CALL LABELDEF
LITS "ELSE"
CALL ISWORD
JZ STIFEND
CALL LEX
CALL BLOCK
LABEL STIFEND
LOCAL 1
CALL LABELDEF
LIT 0
RETURN
LABEL STWHILE
CALL NEWLABEL
SETLOCAL 0
CALL NEWLABEL
SETLOCAL 1
LOCAL 0
CALL LABELDEF
CALL LEX
LIT 1
PUSH
INVOKE EXPR 1
LITS "JZ"
CALL OUTSTR
LOCAL 1
CALL LABELJUMP
CALL BLOCK
LITS "JMP"
CALL OUTSTR
LOCAL 0
CALL LABELJUMP
LOCAL 1
CALL LABELDEF
```

The following old source remains:

```ir
LIT 0
RETURN
```

### Edit at old physical position 1039

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Remove:

```ir
PROC STATEMENT 0 0
LIT 2
```

Insert in its place:

```ir
PROC STATEMENT 0 5
LD TOK
```

The following old source remains:

```ir
PUSH
INVOKE ERROR 1
```

### Edit at old physical position 50

Unchanged source before the edit:

```ir
CALL NEXT
CALL LEX
CALL BLOCK
```

Insert in its place:

```ir
LITS "LIT 0\r\nRETURN\r\n"
CALL OUTSTR
```

The following old source remains:

```ir
CALL FLUSH
LD OUTPUT
```

### Edit at old physical position 49

Unchanged source before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Insert in its place:

```ir
LITS "PROC MAIN 0 16\r\n"
CALL OUTSTR
```

The following old source remains:

```ir
CALL BLOCK
CALL FLUSH
```

## Build and check

```dos
COPY R38.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 16691 bytes`. Save RESULT.COM as R38.COM. VIEW.BAS must show length 16691.

Create T38.RIL:

```rill
{let mut x=65;while x<67{putc(x);x=x+1;}}
```

```dos
COPY T38.RIL SOURCE.RIL
```

```dos
CHECK R38
```

Require PASS.

Inspect RILL.TMP with VIEW.BAS. Require length 238 bytes and these complete bytes:

```text
50 52 4F 43 20 4D 41 49 4E 20 30 20 31 36 0D 0A
4C 49 54 20 30 30 30 36 35 0D 0A 53 45 54 4C 4F
43 41 4C 20 30 30 30 30 30 0D 0A 4C 41 42 45 4C
20 42 5F 30 30 30 30 31 0D 0A 4C 4F 43 41 4C 20
30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 4C 49 54
20 30 30 30 36 37 0D 0A 43 55 4C 54 0D 0A 4A 5A
20 42 5F 30 30 30 30 32 0D 0A 4C 4F 43 41 4C 20
30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 50 4F 50
0D 0A 50 55 54 43 0D 0A 4C 41 44 44 52 20 30 30
30 30 30 0D 0A 50 55 53 48 0D 0A 4C 4F 43 41 4C
20 30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 4C 49
54 20 30 30 30 30 31 0D 0A 41 44 44 0D 0A 50 55
54 0D 0A 4A 4D 50 20 42 5F 30 30 30 30 31 0D 0A
4C 41 42 45 4C 20 42 5F 30 30 30 30 32 0D 0A 4C
49 54 20 30 0D 0A 52 45 54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1083. CHECK TRY displays `AB` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```rill
{putc();}
```

Copy it to SOURCE.RIL and run CHECK R38. Require:

```text
ERROR 0000000001 CODE 00004
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

