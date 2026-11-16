+++
title = "39 \u00b7 The first complete compiler"
weight = 39
description = "Open the source selected by the command arguments and stream generated text through an owned temporary file."
download = "R39.IR"
download_group = "tools/rill0"
reader_names = 1
url = "/bootstrap/rill/039-the-first-complete-compiler/"
+++

Open the source selected by the command arguments and stream generated text through an owned temporary file. Publish the selected result only after the full source, final flush, and both closes succeed.

## Enter the source

Copy R38.IR to R39.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 73

Unchanged source before the edit:

```ir
LIT 0
ST OUTPUT
ST OWN
```

Insert in its place:

```ir
LD BACKUP
JZ PUBLISHED
LITS "RILL.BAK"
DELETE
STATUS
JNZ IOFAIL
LABEL PUBLISHED
LD TABLE
FREEBLOCK
STATUS
JNZ IOFAIL
LITS "OK "
CALL PRINT
LIT 2
PUSH
LITS "RESULT.IR"
PUSH
INVOKE FILEARG 2
CALL PRINT
LITS " "
CALL PRINT
LD TOTALHI
PUSH
LD TOTAL
PUSH
INVOKE PRINT32 2
LABEL REPORTDONE
LITS "\r\n"
CALL PRINT
```

The following old source remains:

```ir
LIT 0
RETURN
```

### Edit at old physical position 71

Unchanged source before the edit:

```ir
LD OUTPUT
CLOSE
LIT 0
```

Remove:

```ir
ST OUTPUT
```

The following old source remains:

```ir
ST OWN
LIT 0
```

### Edit at old physical position 70

Unchanged source before the edit:

```ir
CALL FLUSH
LD OUTPUT
CLOSE
```

Insert in its place:

```ir
STATUS
JNZ IOFAIL
LIT 2
PUSH
LITS "RESULT.IR"
PUSH
INVOKE FILEARG 2
EXISTS
ST FOUND
STATUS
JNZ IOFAIL
LD FOUND
JZ NOOLD
LIT 2
PUSH
LITS "RESULT.IR"
PUSH
INVOKE FILEARG 2
PUSH
LITS "RILL.BAK"
RENAME
STATUS
JNZ IOFAIL
LIT 1
ST BACKUP
LABEL NOOLD
LITS "RILL.TMP"
PUSH
LIT 2
PUSH
LITS "RESULT.IR"
PUSH
INVOKE FILEARG 2
RENAME
STATUS
JNZ IOFAIL
```

The following old source remains:

```ir
LIT 0
ST OUTPUT
```

### Edit at old physical position 67

Unchanged source before the edit:

```ir
CALL BLOCK
LITS "LIT 0\r\nRETURN\r\n"
CALL OUTSTR
```

Insert in its place:

```ir
LD INPUT
CLOSE
STATUS
JNZ IOFAIL
```

The following old source remains:

```ir
CALL FLUSH
LD OUTPUT
```

### Edit at old physical position 65

Unchanged source before the edit:

```ir
LITS "PROC MAIN 0 16\r\n"
CALL OUTSTR
CALL BLOCK
```

Insert in its place:

```ir
LD TOK
JNZ SYNTAX
```

The following old source remains:

```ir
LITS "LIT 0\r\nRETURN\r\n"
CALL OUTSTR
```

### Edit at old physical position 62

Unchanged source before the edit:

```ir
JNZ IOFAIL
CALL NEXT
CALL LEX
```

Insert in its place:

```ir
LITS "FN"
CALL ISWORD
JZ SYNTAX
CALL LEX
LITS "MAIN"
CALL ISWORD
JZ SYNTAX
CALL LEX
LIT 40
PUSH
INVOKE EXPECT 1
LIT 41
PUSH
INVOKE EXPECT 1
```

The following old source remains:

```ir
LITS "PROC MAIN 0 16\r\n"
CALL OUTSTR
```

### Edit at old physical position 60

Unchanged source before the edit:

```ir
ST INPUT
STATUS
JNZ IOFAIL
```

Insert in its place:

```ir
LITS "RILL.TMP"
CREATE
ST OUTPUT
STATUS
JNZ IOFAIL
LIT 1
ST OWN
LIT 22000
ALLOC
ST TABLE
STATUS
JNZ CAPFAIL
```

The following old source remains:

```ir
CALL NEXT
CALL LEX
```

### Edit at old physical position 43

Unchanged source before the edit:

```ir
LIT 2
PUSH
LITS "RILL.TMP"
```

Remove:

```ir
PUSH
INVOKE FILEARG 2
CREATE
ST OUTPUT
STATUS
JNZ IOFAIL
LIT 1
ST OWN
```

Insert in its place:

```ir
EXISTS
JNZ CAPFAIL
LITS "RILL.BAK"
EXISTS
JNZ CAPFAIL
```

The following old source remains:

```ir
LIT 1
PUSH
```

### Edit at old physical position 37

Unchanged source before the edit:

```ir
LITS "SOURCE.RIL"
PUSH
INVOKE FILEARG 2
```

Remove:

```ir
LIT 22000
ALLOC
ST TABLE
LIT 2
PUSH
```

The following old source remains:

```ir
LITS "RILL.TMP"
PUSH
```

### Edit at old physical position 22

Unchanged source before the edit:

```ir
WORD ENDED 0
WORD OWN 0
WORD BACKUP 0
```

Insert in its place:

```ir
WORD FOUND 0
```

The following old source remains:

```ir
WORD RECTYPE 0
WORD RECVAL 0
```

## Build and check

```dos
CHECK IRKEEP R39.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 18022 bytes`. Save RESULT.COM as R39.COM. VIEW.BAS must show length 18022.

Create T39.RIL:

```rill
fn main(){putc(72);putc(73);return 0;}
```

```dos
CHECK R39 T39.RIL RESULT.IR
```

Require:

```text
OK RESULT.IR 0000000106
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 106 bytes and these complete bytes:

```text
50 52 4F 43 20 4D 41 49 4E 20 30 20 31 36 0D 0A
4C 49 54 20 30 30 30 37 32 0D 0A 50 55 53 48 0D
0A 50 4F 50 0D 0A 50 55 54 43 0D 0A 4C 49 54 20
30 30 30 37 33 0D 0A 50 55 53 48 0D 0A 50 4F 50
0D 0A 50 55 54 43 0D 0A 4C 49 54 20 30 30 30 30
30 0D 0A 52 45 54 55 52 4E 0D 0A 4C 49 54 20 30
0D 0A 52 45 54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1404. CHECK TRY displays `HI` and reports PASS.

## Check the new boundary

Save this separate rejected source as X39.RIL:

```rill
fn main(){return 65536;}
```

```dos
CHECK R39 X39.RIL RESULT.IR
```

Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

```dos
COPY R39.COM RLKEEP.COM
```

RILL0.IR is this final source. Continue by editing it in [RILLBOOT](../../rb/index.html).
