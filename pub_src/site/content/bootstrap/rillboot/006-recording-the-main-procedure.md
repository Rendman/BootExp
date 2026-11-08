+++
title = "06 \u00b7 Recording the main procedure"
weight = 6
description = "Give main an initialized procedure record and emit its body through FUNCTION. Its entry wrapper invokes that body with zero arguments; the accepted one-main language remains intact."
download = "RB06.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/006-named-procedures/", "/bootstrap/rb/039-rb-decimal-characters/", "/bootstrap/rill/039-rb-decimal-characters/"]
url = "/bootstrap/rb/006-recording-the-main-procedure/"
+++

Give main an initialized procedure record and emit its body through FUNCTION. Its entry wrapper invokes that body with zero arguments; the accepted one-main language remains intact.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RB05.IR to RB06.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1266

Unchanged source before the edit:

```ir
LIT 59
PUSH
INVOKE EXPECT 1
```

Insert in its place:

```ir
LIT 0
RETURN

PROC FUNCTION 0 4
LD TOK
PUSH
LIT 1
CNE
JNZ SYNTAX
CALL LOOKGLOBAL
SETLOCAL 0
PUSH
LIT 65535
CEQ
JNZ NEWFUNCTION
LD RECTYPE
PUSH
LIT 4
CNE
JNZ NAMEFAIL
JMP FUNCTIONNAME
LABEL NEWFUNCTION
LIT 65535
ST RECVAL
LIT 0
ST RECLEVEL
LIT 4
CALL NEWGLOBAL
SETLOCAL 0
LABEL FUNCTIONNAME
LOCAL 0
PUSH
LIT 34
ADD
CALL TWORD
SETLOCAL 2
LOCAL 0
PUSH
LIT 32
ADD
PUSH
LIT 3
PUSH
INVOKE WRITEFIELD 2
LIT 0
ST LOCALCOUNT
ST NEXTLOCAL
ST LEVEL
SETLOCAL 1
CALL LEX
LIT 40
PUSH
INVOKE EXPECT 1
LABEL PARAMDONE
LOCAL 2
PUSH
LIT 65535
CEQ
JNZ PARAMACCEPTED
LOCAL 2
PUSH
LOCAL 1
CNE
JNZ NAMEFAIL
LABEL PARAMACCEPTED
LOCAL 0
PUSH
LIT 34
ADD
PUSH
LOCAL 1
PUSH
INVOKE WRITEFIELD 2
LITS "PROC F_"
CALL OUTSTR
LOCAL 0
CALL OUTNAME
LIT 32
CALL OUTCHAR
LOCAL 1
CALL OUTNUM
LITS " 16\r\n"
CALL OUTSTR
CALL LEX
CALL BLOCK
LITS "LIT 0\r\nRETURN\r\n"
CALL OUTSTR
```

The following old source remains:

```ir
LIT 0
RETURN
```

### Edit at old physical position 882

Unchanged source before the edit:

```ir
ST RECTYPE
LD GLOBALS
PUSH
```

Remove:

```ir
LIT 511
```

Insert in its place:

```ir
LIT 512
```

The following old source remains:

```ir
CUGE
JNZ CAPFAIL
```

### Edit at old physical position 92

Unchanged source before the edit:

```ir
CALL BLOCK
LD TOK
JNZ SYNTAX
```

Remove:

```ir
LITS "LIT 0\r\nRETURN\r\n"
```

Insert in its place:

```ir
LITS "PROC MAIN 0 0\r\nINVOKE F_MAIN 0\r\nRETURN\r\n"
```

The following old source remains:

```ir
CALL OUTSTR
LD INPUT
```

### Edit at old physical position 80

Unchanged source before the edit:

```ir
LITS "MAIN"
CALL ISWORD
JZ SYNTAX
```

Remove:

```ir
CALL LEX
LIT 40
PUSH
INVOKE EXPECT 1
LIT 41
PUSH
INVOKE EXPECT 1
LITS "PROC MAIN 0 16\r\n"
CALL OUTSTR
CALL BLOCK
```

Insert in its place:

```ir
CALL FUNCTION
```

The following old source remains:

```ir
LD TOK
JNZ SYNTAX
```

## Build and check

```dos
COPY RB06.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 20148 bytes`. Save RESULT.COM as RB06.COM. VIEW.BAS must show length 20148.

Create TRB06.RIL:

```rill
fn main(){putc(65);}
```

```dos
COPY TRB06.RIL SOURCE.RIL
```

```dos
CHECK RB06
```

Require:

```text
OK RESULT.IR 0000000105
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 105 bytes and these complete bytes:

```text
50 52 4F 43 20 46 5F 4D 41 49 4E 20 30 30 30 30
30 20 31 36 0D 0A 4C 49 54 20 30 30 30 36 35 0D
0A 50 55 53 48 0D 0A 50 4F 50 0D 0A 50 55 54 43
0D 0A 4C 49 54 20 30 0D 0A 52 45 54 55 52 4E 0D
0A 50 52 4F 43 20 4D 41 49 4E 20 30 20 30 0D 0A
49 4E 56 4F 4B 45 20 46 5F 4D 41 49 4E 20 30 0D
0A 52 45 54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1054. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```rill
fn main(){putc(65536);}
```

Copy it to SOURCE.RIL and run CHECK RB06. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

