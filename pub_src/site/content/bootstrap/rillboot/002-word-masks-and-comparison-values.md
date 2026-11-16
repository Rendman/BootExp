+++
title = "02 \u00b7 Word masks and comparison values"
weight = 2
description = "Add masks, logical right shift, and logical negation. Comparison values are zero or one. These are the bit operations used in the compiler source."
download = "RB02.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/035-rb-a-visible-word-value/", "/bootstrap/rill/035-rb-a-visible-word-value/"]
url = "/bootstrap/rb/002-word-masks-and-comparison-values/"
+++

Add masks, logical right shift, and logical negation. Comparison values are zero or one. These are the bit operations used in the compiler source.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RB01.IR to RB02.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1746

Unchanged source before the edit:

```ir
LIT 41
PUSH
INVOKE EXPECT 1
```

Insert in its place:

```ir
JMP PRIMARYDONE
LABEL PRIMARYBOOL
CALL LEX
LIT 8
PUSH
INVOKE EXPR 1
LITS "PUSH\r\nLIT 0\r\nCEQ\r\n"
CALL OUTSTR
```

The following old source remains:

```ir
JMP PRIMARYDONE
LABEL PRIMARYDONE
```

### Edit at old physical position 1691

Unchanged source before the edit:

```ir
LIT 40
CEQ
JNZ PRIMARYPAREN
```

Insert in its place:

```ir
LD TOK
PUSH
LIT 33
CEQ
JNZ PRIMARYBOOL
```

The following old source remains:

```ir
LD TOK
PUSH
```

### Edit at old physical position 1661

Unchanged source before the edit:

```ir
LABEL BINMOD
LITS "MOD\r\n"
JMP BINDONE
```

Insert in its place:

```ir
LABEL BINOR
LITS "OR\r\n"
JMP BINDONE
LABEL BINAND
LITS "AND\r\n"
JMP BINDONE
LABEL BINSHR
LITS "SHR\r\n"
JMP BINDONE
```

The following old source remains:

```ir
LABEL BINEQ
LITS "CEQ\r\n"
```

### Edit at old physical position 1621

Unchanged source before the edit:

```ir
JNZ BINMOD
LOCAL 0
PUSH
```

Insert in its place:

```ir
LIT 124
CEQ
JNZ BINOR
LOCAL 0
PUSH
LIT 38
CEQ
JNZ BINAND
LOCAL 0
PUSH
LIT 261
CEQ
JNZ BINSHR
LOCAL 0
PUSH
```

The following old source remains:

```ir
LIT 256
CEQ
```

### Edit at old physical position 1505

Unchanged source before the edit:

```ir
LIT 62
CEQ
JNZ PRECFOUR
```

Insert in its place:

```ir
LD TOK
PUSH
LIT 261
CEQ
JNZ PRECFIVE
```

The following old source remains:

```ir
LD TOK
PUSH
```

### Edit at old physical position 1477

Unchanged source before the edit:

```ir
PROC PREC 0 0
LD TOK
PUSH
```

Insert in its place:

```ir
LIT 124
CEQ
JNZ PRECONE
LD TOK
PUSH
LIT 38
CEQ
JNZ PRECTHREE
LD TOK
PUSH
```

The following old source remains:

```ir
LIT 256
CEQ
```

## Build and check

```dos
CHECK IRKEEP RB02.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 18494 bytes`. Save RESULT.COM as RB02.COM. VIEW.BAS must show length 18494.

Create TRB02.RIL:

```rill
fn main(){putc((130>>1)|0);}
```

```dos
CHECK RB02 TRB02.RIL RESULT.IR
```

Require:

```text
OK RESULT.IR 0000000102
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 102 bytes and these complete bytes:

```text
50 52 4F 43 20 4D 41 49 4E 20 30 20 31 36 0D 0A
4C 49 54 20 30 30 31 33 30 0D 0A 50 55 53 48 0D
0A 4C 49 54 20 30 30 30 30 31 0D 0A 53 48 52 0D
0A 50 55 53 48 0D 0A 4C 49 54 20 30 30 30 30 30
0D 0A 4F 52 0D 0A 50 55 53 48 0D 0A 50 4F 50 0D
0A 50 55 54 43 0D 0A 4C 49 54 20 30 0D 0A 52 45
54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1409. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Save this separate rejected source as XRB02.RIL:

```rill
fn main(){putc(65536);}
```

```dos
CHECK RB02 XRB02.RIL RESULT.IR
```

Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

