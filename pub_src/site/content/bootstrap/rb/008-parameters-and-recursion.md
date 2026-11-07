+++
title = "08 \u00b7 Parameters and recursion"
weight = 8
description = "Add parameter records and verify call arity. Parameters and local words belong to each call, so recursive procedures preserve their callers."
download = "RB08.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/008-counted-file-services/", "/bootstrap/rb/041-rb-punctuation-and-paired-operators/", "/bootstrap/rill/041-rb-punctuation-and-paired-operators/"]
+++

Add parameter records and verify call arity. Parameters and local words belong to each call, so recursive procedures preserve their callers.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RB07.IR to RB08.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1356

Unchanged source before the edit:

```ir
LIT 40
PUSH
INVOKE EXPECT 1
```

Insert in its place:

```ir
LABEL PARAMLOOP
LD TOK
PUSH
LIT 41
CEQ
JNZ PARAMDONE
LD TOK
PUSH
LIT 1
CNE
JNZ SYNTAX
LIT 20480
PUSH
LD LOCALCOUNT
PUSH
INVOKE FIND 2
PUSH
LIT 65535
CNE
JNZ NAMEFAIL
LOCAL 1
PUSH
LIT 16
CUGE
JNZ CAPFAIL
LOCAL 1
ST RECVAL
LIT 0
ST RECLEVEL
LIT 6
CALL NEWLOCAL
LOCAL 1
PUSH
LIT 1
ADD
SETLOCAL 1
CALL LEX
LD TOK
PUSH
LIT 41
CEQ
JNZ PARAMDONE
LIT 44
PUSH
INVOKE EXPECT 1
JMP PARAMLOOP
```

The following old source remains:

```ir
LABEL PARAMDONE
LOCAL 2
```

## Build and check

```dos
COPY RB08.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 20856 bytes`. Save RESULT.COM as RB08.COM. VIEW.BAS must show length 20856.

Create TRB08.RIL:

```rill
fn main(){putc(twice(32)+1);}fn twice(x){return x*2;}
```

```dos
COPY TRB08.RIL SOURCE.RIL
```

```dos
CHECK RB08
```

Require:

```text
OK RESULT.IR 0000000236
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 236 bytes and these complete bytes:

```text
50 52 4F 43 20 46 5F 4D 41 49 4E 20 30 30 30 30
30 20 31 36 0D 0A 4C 49 54 20 30 30 30 33 32 0D
0A 50 55 53 48 0D 0A 49 4E 56 4F 4B 45 20 46 5F
54 57 49 43 45 20 30 30 30 30 31 0D 0A 50 55 53
48 0D 0A 4C 49 54 20 30 30 30 30 31 0D 0A 41 44
44 0D 0A 50 55 53 48 0D 0A 50 4F 50 0D 0A 50 55
54 43 0D 0A 4C 49 54 20 30 0D 0A 52 45 54 55 52
4E 0D 0A 50 52 4F 43 20 46 5F 54 57 49 43 45 20
30 30 30 30 31 20 31 36 0D 0A 50 41 52 41 4D 20
30 30 30 30 30 0D 0A 50 55 53 48 0D 0A 4C 49 54
20 30 30 30 30 32 0D 0A 4D 55 4C 0D 0A 52 45 54
55 52 4E 0D 0A 4C 49 54 20 30 0D 0A 52 45 54 55
52 4E 0D 0A 50 52 4F 43 20 4D 41 49 4E 20 30 20
30 0D 0A 49 4E 56 4F 4B 45 20 46 5F 4D 41 49 4E
20 30 0D 0A 52 45 54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1107. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```rill
fn main(){putc(65536);}
```

Copy it to SOURCE.RIL and run CHECK RB08. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

