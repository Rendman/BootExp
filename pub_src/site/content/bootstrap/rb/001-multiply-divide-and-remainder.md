+++
title = "01 \u00b7 Multiply, divide, and remainder"
weight = 1
description = "Add unsigned multiply, quotient, and remainder to the existing precedence parser. The IR runtime rejects a zero divisor; word products wrap."
download = "RB01.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/034-rb-a-terminated-text-pointer/", "/bootstrap/rill/034-rb-a-terminated-text-pointer/"]
+++

Add unsigned multiply, quotient, and remainder to the existing precedence parser. The IR runtime rejects a zero divisor; word products wrap.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RILL0.IR to RB01.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1592

Unchanged source before the edit:

```ir
JMP BINDONE
LABEL BINSUB
LITS "SUB\r\n"
```

Insert in its place:

```ir
JMP BINDONE
LABEL BINMUL
LITS "MUL\r\n"
JMP BINDONE
LABEL BINDIV
LITS "DIV\r\n"
JMP BINDONE
LABEL BINMOD
LITS "MOD\r\n"
```

The following old source remains:

```ir
JMP BINDONE
LABEL BINEQ
```

### Edit at old physical position 1562

Unchanged source before the edit:

```ir
JNZ BINSUB
LOCAL 0
PUSH
```

Insert in its place:

```ir
LIT 42
CEQ
JNZ BINMUL
LOCAL 0
PUSH
LIT 47
CEQ
JNZ BINDIV
LOCAL 0
PUSH
LIT 37
CEQ
JNZ BINMOD
LOCAL 0
PUSH
```

The following old source remains:

```ir
LIT 256
CEQ
```

### Edit at old physical position 1486

Unchanged source before the edit:

```ir
LIT 45
CEQ
JNZ PRECSIX
```

Insert in its place:

```ir
LD TOK
PUSH
LIT 42
CEQ
JNZ PRECSEVEN
LD TOK
PUSH
LIT 47
CEQ
JNZ PRECSEVEN
LD TOK
PUSH
LIT 37
CEQ
JNZ PRECSEVEN
```

The following old source remains:

```ir
LIT 0
RETURN
```

## Build and check

```dos
COPY RB01.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 17345 bytes`. Save RESULT.COM as RB01.COM. VIEW.BAS must show length 17345.

Create TRB01.RIL:

```rill
fn main(){putc(13*5);}
```

```dos
COPY TRB01.RIL SOURCE.RIL
```

```dos
CHECK RB01
```

Require:

```text
OK RESULT.IR 0000000081
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 81 bytes and these complete bytes:

```text
50 52 4F 43 20 4D 41 49 4E 20 30 20 31 36 0D 0A
4C 49 54 20 30 30 30 31 33 0D 0A 50 55 53 48 0D
0A 4C 49 54 20 30 30 30 30 35 0D 0A 4D 55 4C 0D
0A 50 55 53 48 0D 0A 50 4F 50 0D 0A 50 55 54 43
0D 0A 4C 49 54 20 30 0D 0A 52 45 54 55 52 4E 0D
0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1034. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```rill
fn main(){putc(65536);}
```

Copy it to SOURCE.RIL and run CHECK RB01. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

