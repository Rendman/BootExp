+++
title = "03 \u00b7 Quoted text and byte loads"
weight = 3
description = "Keep quoted source bytes separate from folded names. Compile a string pointer and read its bytes through load8; no printing operation is hidden in a literal."
download = "RB03.IR"
download_group = "tools/rillboot"
reader_names = 1
aliases = ["/bootstrap/rb/036-rb-counting-beyond-one-word/", "/bootstrap/rill/036-rb-counting-beyond-one-word/"]
url = "/bootstrap/rb/003-quoted-text-and-byte-loads/"
+++

Keep quoted source bytes separate from folded names. Compile a string pointer and read its bytes through load8; no printing operation is hidden in a literal.

Retain every earlier language feature. This checkpoint edits the complete compiler; it does not replace it with a helper-only driver.

## Enter the source

Copy RB02.IR to RB03.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1750

Unchanged source before the edit:

```ir
CALL OUTSTR
LD VALUE
CALL OUTNUM
```

Insert in its place:

```ir
CALL NEWLINE
CALL LEX
JMP PRIMARYDONE
LABEL PRIMARYSTRING
LITS "LITS "
CALL OUTSTR
ADDR STRING
CALL OUTSTR
```

The following old source remains:

```ir
CALL NEWLINE
CALL LEX
```

### Edit at old physical position 1698

Unchanged source before the edit:

```ir
JNZ PRIMARYNUM
LD TOK
PUSH
```

Insert in its place:

```ir
LIT 3
CEQ
JNZ PRIMARYSTRING
LD TOK
PUSH
```

The following old source remains:

```ir
LIT 40
CEQ
```

### Edit at old physical position 1276

Unchanged source before the edit:

```ir
RETURN

PROC BUILTIN 0 5
```

Remove:

```ir
LITS "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0EXIT\01\0POP\nEXIT\0\0"
```

Insert in its place:

```ir
LITS "PUTC\01\0POP\nPUTC\0STATUS\00\0STATUS\0LOAD8\01\0POP\nFETCHB\0EXIT\01\0POP\nEXIT\0\0"
```

The following old source remains:

```ir
SETLOCAL 0
LABEL BUILTINNEXT
```

### Edit at old physical position 511

Unchanged source before the edit:

```ir
ST TOK
RETURN
LABEL LEXSTRING
```

Remove:

```ir
JMP SYNTAX
```

Insert in its place:

```ir
LIT 0
SETLOCAL 0
LIT 0
SETLOCAL 1
LABEL STRINGLOOP
LD CH
PUSH
LIT 10
CEQ
JNZ SYNTAX
LD CH
PUSH
LIT 13
CEQ
JNZ SYNTAX
LOCAL 0
PUSH
LIT 510
CUGE
JNZ CAPFAIL
LD CH
JZ SYNTAX
ADDR STRING
PUSH
LOCAL 0
ADD
PUSH
LD CH
PUTB
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
LD CH
SETLOCAL 2
CALL NEXT
LOCAL 0
PUSH
LIT 1
CEQ
JNZ STRINGLOOP
LOCAL 1
JNZ STRINGESCAPED
LOCAL 2
PUSH
LIT 34
CEQ
JNZ STRINGDONE
LOCAL 2
PUSH
LIT 92
CNE
JNZ STRINGLOOP
LIT 1
SETLOCAL 1
JMP STRINGLOOP
LABEL STRINGESCAPED
LOCAL 2
PUSH
LIT 110
CEQ
JNZ STRINGESCAPEGOOD
LOCAL 2
PUSH
LIT 114
CEQ
JNZ STRINGESCAPEGOOD
LOCAL 2
PUSH
LIT 116
CEQ
JNZ STRINGESCAPEGOOD
LOCAL 2
PUSH
LIT 48
CEQ
JNZ STRINGESCAPEGOOD
LOCAL 2
PUSH
LIT 92
CEQ
JNZ STRINGESCAPEGOOD
LOCAL 2
PUSH
LIT 34
CNE
JNZ SYNTAX
LABEL STRINGESCAPEGOOD
LIT 0
SETLOCAL 1
JMP STRINGLOOP
LABEL STRINGDONE
ADDR STRING
PUSH
LOCAL 0
ADD
PUSH
LIT 0
PUTB
LIT 3
ST TOK
RETURN
```

The following old source remains:

```ir
LABEL LEXEOF
LIT 0
```

### Edit at old physical position 30

Unchanged source before the edit:

```ir
BUFFER INBUF 4096
BUFFER OUTBUF 4096
BUFFER IDENT 32
```

Insert in its place:

```ir
BUFFER STRING 512
```

The following old source remains:

```ir
WORD CALLBUILTIN 0
WORD EXPRDEPTH 0
```

## Build and check

```dos
COPY RB03.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 18646 bytes`. Save RESULT.COM as RB03.COM. VIEW.BAS must show length 18646.

Create TRB03.RIL:

```rill
fn main(){putc(load8("A"));}
```

```dos
COPY TRB03.RIL SOURCE.RIL
```

```dos
CHECK RB03
```

Require:

```text
OK RESULT.IR 0000000077
PASS
```

Inspect RESULT.IR with VIEW.BAS. Require length 77 bytes and these complete bytes:

```text
50 52 4F 43 20 4D 41 49 4E 20 30 20 31 36 0D 0A
4C 49 54 53 20 22 41 22 0D 0A 50 55 53 48 0D 0A
50 4F 50 0D 0A 46 45 54 43 48 42 0D 0A 50 55 53
48 0D 0A 50 4F 50 0D 0A 50 55 54 43 0D 0A 4C 49
54 20 30 0D 0A 52 45 54 55 52 4E 0D 0A
```

This is a complete IR program. Translate it with IRKEEP, assemble its accepted output with ASMAKEEP, and save RESULT.COM as TRY.COM. Require fresh OK and PASS before both copies. VIEW.BAS must report length 1040. CHECK TRY displays `A` and reports PASS.

## Check the new boundary

Use this separate rejected source:

```rill
fn main(){putc(65536);}
```

Copy it to SOURCE.RIL and run CHECK RB03. Require:

```text
ERROR 0000000001 CODE 00003
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

