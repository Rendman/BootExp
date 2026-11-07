+++
title = "05 \u00b7 Global byte buffers"
weight = 5
description = "Add global byte buffers and indexed reads and stores. The program owns its index bounds; allocated blocks use a different checked interface."
download = "RB05.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/038-rb-identifier-characters/", "/bootstrap/rill/038-rb-identifier-characters/"]
+++

Add global byte buffers and indexed reads and stores. The program owns its index bounds; allocated blocks use a different checked interface.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RB04.IR to RB05.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1982

Unchanged source before the edit:

```ir
LOCAL 2
CALL OUTNUM
CALL NEWLINE
```

Insert in its place:

```ir
JMP PRIMARYDONE
LABEL PRIMARYBUFFER
LITS "ADDR V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
CALL NEWLINE
LD TOK
PUSH
LIT 91
CNE
JNZ PRIMARYDONE
LITS "PUSH\r\n"
CALL OUTSTR
CALL LEX
LIT 1
PUSH
INVOKE EXPR 1
LIT 93
PUSH
INVOKE EXPECT 1
LITS "ADD\r\nFETCHB\r\n"
CALL OUTSTR
```

The following old source remains:

```ir
JMP PRIMARYDONE
LABEL PRIMARYCALL
```

### Edit at old physical position 1965

Unchanged source before the edit:

```ir
JNZ PRIMARYGLOBAL
LOCAL 1
PUSH
```

Insert in its place:

```ir
LIT 2
CEQ
JNZ PRIMARYBUFFER
LOCAL 1
PUSH
```

The following old source remains:

```ir
LIT 5
CEQ
```

### Edit at old physical position 1403

Unchanged source before the edit:

```ir
LITS "PUT\r\n"
CALL OUTSTR
JMP STFINISH
```

Insert in its place:

```ir
LABEL STPUTBYTE
LITS "PUTB\r\n"
CALL OUTSTR
```

The following old source remains:

```ir
LABEL STFINISH
LIT 59
```

### Edit at old physical position 1400

Unchanged source before the edit:

```ir
LIT 1
PUSH
INVOKE EXPR 1
```

Insert in its place:

```ir
LOCAL 1
PUSH
LIT 2
CEQ
JNZ STPUTBYTE
```

The following old source remains:

```ir
LITS "PUT\r\n"
CALL OUTSTR
```

### Edit at old physical position 1391

Unchanged source before the edit:

```ir
CALL OUTNUM
CALL NEWLINE
JMP STASSIGN
```

Insert in its place:

```ir
LABEL STINDEX
LOCAL 1
PUSH
LIT 2
CNE
JNZ NAMEFAIL
LITS "ADDR V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
LITS "\r\nPUSH\r\n"
CALL OUTSTR
CALL LEX
LIT 1
PUSH
INVOKE EXPR 1
LIT 93
PUSH
INVOKE EXPECT 1
LITS "ADD\r\n"
CALL OUTSTR
```

The following old source remains:

```ir
LABEL STASSIGN
LITS "PUSH\r\n"
```

### Edit at old physical position 1366

Unchanged source before the edit:

```ir
LIT 65535
CEQ
JNZ NAMEFAIL
```

Insert in its place:

```ir
LD TOK
PUSH
LIT 91
CEQ
JNZ STINDEX
```

The following old source remains:

```ir
LOCAL 1
PUSH
```

### Edit at old physical position 1215

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC GLOBALBUFFER 0 1
CALL LEX
LD TOK
PUSH
LIT 1
CNE
JNZ SYNTAX
CALL LOOKGLOBAL
PUSH
LIT 65535
CNE
JNZ NAMEFAIL
LIT 0
ST RECVAL
ST RECLEVEL
LIT 2
CALL NEWGLOBAL
SETLOCAL 0
CALL LEX
LIT 91
PUSH
INVOKE EXPECT 1
LD TOK
PUSH
LIT 2
CNE
JNZ SYNTAX
LD VALUE
JZ CAPFAIL
LITS "BUFFER V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
LIT 32
CALL OUTCHAR
LD VALUE
CALL OUTNUM
CALL NEWLINE
CALL LEX
LIT 93
PUSH
INVOKE EXPECT 1
LIT 59
PUSH
INVOKE EXPECT 1
LIT 0
RETURN
```

The following old source remains:

```ir
PROC BLOCK 0 2
LD LOCALCOUNT
```

### Edit at old physical position 67

Unchanged source before the edit:

```ir
CALL GLOBALWORD
JMP TOP
LABEL TOPBUFFER
```

Insert in its place:

```ir
LITS "BYTES"
CALL ISWORD
JZ TOPMAIN
CALL GLOBALBUFFER
JMP TOP
LABEL TOPMAIN
```

The following old source remains:

```ir
LITS "FN"
CALL ISWORD
```

## Build and check

```dos
COPY RB05.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 19809 bytes`. Save RESULT.COM as RB05.COM. VIEW.BAS must show length 19809.

Create TRB05.RIL:

```rill
bytes b[2];fn main(){b[0]=65;putc(b[0]);}
```

```dos
COPY TRB05.RIL SOURCE.RIL
```

```dos
CHECK RB05
```

Require:

```text
OK RESULT.IR 0000000161
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 161 bytes and these complete bytes:

```text
42 55 46 46 45 52 20 56 5F 42 20 30 30 30 30 32
0D 0A 50 52 4F 43 20 4D 41 49 4E 20 30 20 31 36
0D 0A 41 44 44 52 20 56 5F 42 0D 0A 50 55 53 48
0D 0A 4C 49 54 20 30 30 30 30 30 0D 0A 41 44 44
0D 0A 50 55 53 48 0D 0A 4C 49 54 20 30 30 30 36
35 0D 0A 50 55 54 42 0D 0A 41 44 44 52 20 56 5F
42 0D 0A 50 55 53 48 0D 0A 4C 49 54 20 30 30 30
30 30 0D 0A 41 44 44 0D 0A 46 45 54 43 48 42 0D
0A 50 55 53 48 0D 0A 50 4F 50 0D 0A 50 55 54 43
0D 0A 4C 49 54 20 30 0D 0A 52 45 54 55 52 4E 0D
0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1059. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```rill
fn main(){putc(65536);}
```

Copy it to SOURCE.RIL and run CHECK RB05. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

