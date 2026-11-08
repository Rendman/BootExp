+++
title = "04 \u00b7 Global mutable words"
weight = 4
description = "Add global mutable words with literal initializers. Reuse the initialized symbol records and resolve a visible local before a global."
download = "RB04.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/037-rb-one-terminal-error-path/", "/bootstrap/rill/037-rb-one-terminal-error-path/"]
url = "/bootstrap/rb/004-global-mutable-words/"
+++

Add global mutable words with literal initializers. Reuse the initialized symbol records and resolve a visible local before a global.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RB03.IR to RB04.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1839

Unchanged source before the edit:

```ir
CEQ
JNZ PRIMARYLOCAL
JMP NAMEFAIL
```

Insert in its place:

```ir
LABEL PRIMARYGLOBAL
LITS "LD V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
CALL NEWLINE
JMP PRIMARYDONE
```

The following old source remains:

```ir
LABEL PRIMARYLOCAL
LITS "LOCAL "
```

### Edit at old physical position 1835

Unchanged source before the edit:

```ir
JNZ PRIMARYCALL
LOCAL 1
PUSH
```

Insert in its place:

```ir
LIT 1
CEQ
JNZ PRIMARYGLOBAL
LOCAL 1
PUSH
```

The following old source remains:

```ir
LIT 5
CEQ
```

### Edit at old physical position 1479

Unchanged source before the edit:

```ir
LD LOCALCOUNT
PUSH
INVOKE FIND 2
```

Insert in its place:

```ir
SETLOCAL 0
PUSH
LIT 65535
CNE
JNZ RESOLVEGOT
CALL LOOKGLOBAL
```

The following old source remains:

```ir
SETLOCAL 0
PUSH
```

### Edit at old physical position 1265

Unchanged source before the edit:

```ir
CEQ
JNZ STLOCAL
JMP NAMEFAIL
```

Insert in its place:

```ir
LABEL STGLOBAL
LITS "ADDR V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
CALL NEWLINE
JMP STASSIGN
```

The following old source remains:

```ir
LABEL STLOCAL
LITS "LADDR "
```

### Edit at old physical position 1261

Unchanged source before the edit:

```ir
JNZ NAMEFAIL
LOCAL 1
PUSH
```

Insert in its place:

```ir
LIT 1
CEQ
JNZ STGLOBAL
LOCAL 1
PUSH
```

The following old source remains:

```ir
LIT 5
CEQ
```

### Edit at old physical position 1108

Unchanged source before the edit:

```ir
LIT 0
RETURN
```

Insert in its place:

```ir
PROC GLOBALWORD 0 1
CALL LEX
LITS "MUT"
CALL ISWORD
JZ SYNTAX
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
LIT 1
CALL NEWGLOBAL
SETLOCAL 0
CALL LEX
LIT 61
PUSH
INVOKE EXPECT 1
LD TOK
PUSH
LIT 2
CNE
JNZ SYNTAX
LITS "WORD V_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
LIT 32
CALL OUTCHAR
LD VALUE
CALL OUTNUM
CALL NEWLINE
CALL LEX
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

### Edit at old physical position 887

Unchanged source before the edit:

```ir
LOCAL 0
PUSH
INVOKE RECORD 1
```

Insert in its place:

```ir
RETURN

PROC LOOKGLOBAL 0 0
LIT 0
PUSH
LD GLOBALS
PUSH
INVOKE FIND 2
RETURN

PROC OUTNAME 0 3
SETLOCAL 0
LIT 0
SETLOCAL 1
LABEL OUTNAMELOOP
LOCAL 0
PUSH
LOCAL 1
ADD
CALL TBYTE
JZ OUTNAMEDONE
CALL OUTCHAR
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
JMP OUTNAMELOOP
LABEL OUTNAMEDONE
LIT 0
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 864

Unchanged source before the edit:

```ir
PARAM 0
RETURN
```

Insert in its place:

```ir
PROC NEWGLOBAL 0 1
ST RECTYPE
LD GLOBALS
PUSH
LIT 511
CUGE
JNZ CAPFAIL
LD GLOBALS
PUSH
LIT 40
MUL
SETLOCAL 0
LD GLOBALS
PUSH
LIT 1
ADD
ST GLOBALS
LOCAL 0
PUSH
INVOKE RECORD 1
RETURN
```

The following old source remains:

```ir
PROC NEWLOCAL 0 1
ST RECTYPE
```

### Edit at old physical position 59

Unchanged source before the edit:

```ir
JNZ CAPFAIL
CALL NEXT
CALL LEX
```

Insert in its place:

```ir
LABEL TOP
LITS "LET"
CALL ISWORD
JZ TOPBUFFER
CALL GLOBALWORD
JMP TOP
LABEL TOPBUFFER
```

The following old source remains:

```ir
LITS "FN"
CALL ISWORD
```

### Edit at old physical position 3

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
WORD TABLE 0
```

Insert in its place:

```ir
WORD GLOBALS 0
```

The following old source remains:

```ir
WORD LOCALCOUNT 0
WORD LEVEL 0
```

## Build and check

```dos
COPY RB04.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 19239 bytes`. Save RESULT.COM as RB04.COM. VIEW.BAS must show length 19239.

Create TRB04.RIL:

```rill
let mut x=65;fn main(){putc(x);}
```

```dos
COPY TRB04.RIL SOURCE.RIL
```

```dos
CHECK RB04
```

Require:

```text
OK RESULT.IR 0000000072
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 72 bytes and these complete bytes:

```text
57 4F 52 44 20 56 5F 58 20 30 30 30 36 35 0D 0A
50 52 4F 43 20 4D 41 49 4E 20 30 20 31 36 0D 0A
4C 44 20 56 5F 58 0D 0A 50 55 53 48 0D 0A 50 4F
50 0D 0A 50 55 54 43 0D 0A 4C 49 54 20 30 0D 0A
52 45 54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1030. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```rill
fn main(){putc(65536);}
```

Copy it to SOURCE.RIL and run CHECK RB04. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

