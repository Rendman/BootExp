+++
title = "07 \u00b7 Named procedures"
weight = 7
description = "Record named zero-argument procedures and pending calls. Final acceptance rejects an undefined procedure; main must exist and take no arguments."
download = "RB07.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/007-parameters-and-recursion/", "/bootstrap/rb/040-rb-a-bounded-source-refill/", "/bootstrap/rill/040-rb-a-bounded-source-refill/"]
url = "/bootstrap/rb/007-named-procedures/"
+++

Record named zero-argument procedures and pending calls. Final acceptance rejects an undefined procedure; main must exist and take no arguments.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RB06.IR to RB07.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 2149

Unchanged source before the edit:

```ir
JMP PRIMARYDONE
LABEL PRIMARYLOCAL
LITS "LOCAL "
```

Insert in its place:

```ir
CALL OUTSTR
LOCAL 2
CALL OUTNUM
CALL NEWLINE
JMP PRIMARYDONE
LABEL PRIMARYPARAM
LITS "PARAM "
```

The following old source remains:

```ir
CALL OUTSTR
LOCAL 2
```

### Edit at old physical position 2139

Unchanged source before the edit:

```ir
LIT 5
CEQ
JNZ PRIMARYLOCAL
```

Insert in its place:

```ir
LOCAL 1
PUSH
LIT 6
CEQ
JNZ PRIMARYPARAM
```

The following old source remains:

```ir
JMP NAMEFAIL
LABEL PRIMARYGLOBAL
```

### Edit at old physical position 1837

Unchanged source before the edit:

```ir
LIT 0
RETURN
LABEL ARGUSER
```

Remove:

```ir
JMP NAMEFAIL
```

Insert in its place:

```ir
PARAM 0
PUSH
LIT 32
ADD
CALL TWORD
SETLOCAL 1
PUSH
LIT 3
CEQ
JNZ ARGFUNCTION
LOCAL 1
PUSH
LIT 4
CNE
JNZ NAMEFAIL
LABEL ARGFUNCTION
PARAM 0
PUSH
LIT 34
ADD
CALL TWORD
SETLOCAL 1
PUSH
LIT 65535
CEQ
JNZ ARGFIRST
LOCAL 1
PUSH
LOCAL 0
CNE
JNZ NAMEFAIL
JMP ARGEMIT
LABEL ARGFIRST
PARAM 0
PUSH
LIT 34
ADD
PUSH
LOCAL 0
PUSH
INVOKE WRITEFIELD 2
LABEL ARGEMIT
LITS "INVOKE F_"
CALL OUTSTR
PARAM 0
CALL OUTNAME
LIT 32
CALL OUTCHAR
LOCAL 0
CALL OUTNUM
CALL NEWLINE
LIT 0
RETURN
```

The following old source remains:

```ir

PROC PREC 0 0
```

### Edit at old physical position 1775

Unchanged source before the edit:

```ir
LIT 65535
CNE
JNZ RESOLVEGOT
```

Remove:

```ir
JMP NAMEFAIL
```

Insert in its place:

```ir
LIT 65535
ST RECVAL
LIT 0
ST RECLEVEL
LIT 4
CALL NEWGLOBAL
SETLOCAL 0
LIT 4
ST RECTYPE
```

The following old source remains:

```ir
LABEL RESOLVEGOT
LOCAL 0
```

### Edit at old physical position 1523

Unchanged source before the edit:

```ir
JMP STASSIGN
LABEL STLOCAL
LITS "LADDR "
```

Insert in its place:

```ir
CALL OUTSTR
LOCAL 2
CALL OUTNUM
CALL NEWLINE
JMP STASSIGN
LABEL STPARAM
LITS "PADDR "
```

The following old source remains:

```ir
CALL OUTSTR
LOCAL 2
```

### Edit at old physical position 1513

Unchanged source before the edit:

```ir
LIT 5
CEQ
JNZ STLOCAL
```

Insert in its place:

```ir
LOCAL 1
PUSH
LIT 6
CEQ
JNZ STPARAM
```

The following old source remains:

```ir
JMP NAMEFAIL
LABEL STGLOBAL
```

### Edit at old physical position 1261

Unchanged source before the edit:

```ir
RETURN

PROC FUNCTION 0 4
```

Insert in its place:

```ir
CALL LEX
```

The following old source remains:

```ir
LD TOK
PUSH
```

### Edit at old physical position 78

Unchanged source before the edit:

```ir
JZ SYNTAX
CALL LEX
LITS "MAIN"
```

Remove:

```ir
CALL ISWORD
JZ SYNTAX
CALL FUNCTION
LD TOK
JNZ SYNTAX
```

Insert in its place:

```ir
CALL SETIDENT
LIT 0
PUSH
LD GLOBALS
PUSH
INVOKE FIND 2
PUSH
LIT 65535
CEQ
JNZ NAMEFAIL
LD RECTYPE
PUSH
LIT 3
CNE
JNZ NAMEFAIL
LD RECVAL
JNZ NAMEFAIL
LIT 0
ST FOUND
LABEL CHECKGLOBALS
LD FOUND
PUSH
LD GLOBALS
CUGE
JNZ CHECKDONE
LD FOUND
PUSH
LIT 40
MUL
PUSH
LIT 32
ADD
CALL TWORD
PUSH
LIT 4
CEQ
JNZ NAMEFAIL
LD FOUND
PUSH
LIT 1
ADD
ST FOUND
JMP CHECKGLOBALS
LABEL CHECKDONE
```

The following old source remains:

```ir
LITS "PROC MAIN 0 0\r\nINVOKE F_MAIN 0\r\nRETURN\r\n"
CALL OUTSTR
```

### Edit at old physical position 72

Unchanged source before the edit:

```ir
JZ TOPMAIN
CALL GLOBALBUFFER
JMP TOP
```

Remove:

```ir
LABEL TOPMAIN
LITS "FN"
CALL ISWORD
JZ SYNTAX
CALL LEX
```

Insert in its place:

```ir
LABEL COMPLETE
```

The following old source remains:

```ir
LITS "MAIN"
CALL ISWORD
```

### Edit at old physical position 66

Unchanged source before the edit:

```ir
JZ TOPBUFFER
CALL GLOBALWORD
JMP TOP
```

Remove:

```ir
LABEL TOPBUFFER
LITS "BYTES"
CALL ISWORD
JZ TOPMAIN
```

Insert in its place:

```ir
LABEL TOPBYTES
```

The following old source remains:

```ir
CALL GLOBALBUFFER
JMP TOP
```

### Edit at old physical position 63

Unchanged source before the edit:

```ir
LABEL TOP
LITS "LET"
CALL ISWORD
```

Remove:

```ir
JZ TOPBUFFER
```

Insert in its place:

```ir
JNZ TOPWORD
LITS "BYTES"
CALL ISWORD
JNZ TOPBYTES
JMP SYNTAX
LABEL TOPFN
CALL FUNCTION
JMP TOP
LABEL TOPWORD
```

The following old source remains:

```ir
CALL GLOBALWORD
JMP TOP
```

### Edit at old physical position 61

Unchanged source before the edit:

```ir
CALL NEXT
CALL LEX
LABEL TOP
```

Insert in its place:

```ir
LD TOK
JZ COMPLETE
LITS "FN"
CALL ISWORD
JNZ TOPFN
```

The following old source remains:

```ir
LITS "LET"
CALL ISWORD
```

## Build and check

```dos
COPY RB07.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 20661 bytes`. Save RESULT.COM as RB07.COM. VIEW.BAS must show length 20661.

Create TRB07.RIL:

```rill
fn main(){putc(value());}fn value(){return 65;}
```

```dos
COPY TRB07.RIL SOURCE.RIL
```

```dos
CHECK RB07
```

Require:

```text
OK RESULT.IR 0000000173
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 173 bytes and these complete bytes:

```text
50 52 4F 43 20 46 5F 4D 41 49 4E 20 30 30 30 30
30 20 31 36 0D 0A 49 4E 56 4F 4B 45 20 46 5F 56
41 4C 55 45 20 30 30 30 30 30 0D 0A 50 55 53 48
0D 0A 50 4F 50 0D 0A 50 55 54 43 0D 0A 4C 49 54
20 30 0D 0A 52 45 54 55 52 4E 0D 0A 50 52 4F 43
20 46 5F 56 41 4C 55 45 20 30 30 30 30 30 20 31
36 0D 0A 4C 49 54 20 30 30 30 36 35 0D 0A 52 45
54 55 52 4E 0D 0A 4C 49 54 20 30 0D 0A 52 45 54
55 52 4E 0D 0A 50 52 4F 43 20 4D 41 49 4E 20 30
20 30 0D 0A 49 4E 56 4F 4B 45 20 46 5F 4D 41 49
4E 20 30 0D 0A 52 45 54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1088. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```rill
fn main(){putc(65536);}
```

Copy it to SOURCE.RIL and run CHECK RB07. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

