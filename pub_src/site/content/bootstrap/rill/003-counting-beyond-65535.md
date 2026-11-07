+++
title = "03 \u00b7 Counting Beyond 65535"
weight = 3
description = "Report a count as two words without requiring a wider machine value."
download = "R03.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/003-counting-beyond-one-word/", "/bootstrap/rill/03-quotient-and-remainder-by-subtraction/"]
+++

Report a count as two words without requiring a wider machine value. Divide the pair by ten and display its saved digits.

## Enter the source

Copy R02.IR to R03.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 61

Unchanged source before the edit:

```ir
JNZ PRINTPLACE
LIT 0
RETURN
```

Insert in its place:

```ir

PROC PRINT32 2 8
PARAM 0
SETLOCAL 0
PARAM 1
SETLOCAL 1
LIT 0
SETLOCAL 2
LABEL DECIMALPLACE
LOCAL 0
PUSH
LIT 10
DIV
SETLOCAL 3
LOCAL 0
PUSH
LIT 10
MOD
SETLOCAL 4
LIT 0
SETLOCAL 5
LIT 32768
SETLOCAL 6
LABEL DECIMALBIT
LOCAL 4
PUSH
LIT 2
MUL
SETLOCAL 4
LOCAL 1
PUSH
LOCAL 6
AND
JZ DECIMALNOONE
LOCAL 4
PUSH
LIT 1
ADD
SETLOCAL 4
LABEL DECIMALNOONE
LOCAL 5
PUSH
LIT 2
MUL
SETLOCAL 5
LOCAL 4
PUSH
LIT 10
CULT
JNZ DECIMALNOSUB
LOCAL 4
PUSH
LIT 10
SUB
SETLOCAL 4
LOCAL 5
PUSH
LIT 1
ADD
SETLOCAL 5
LABEL DECIMALNOSUB
LOCAL 6
PUSH
LIT 1
SHR
SETLOCAL 6
JNZ DECIMALBIT
ADDR DECIMAL
PUSH
LOCAL 2
ADD
PUSH
LOCAL 4
PUSH
LIT 48
ADD
PUTB
LOCAL 3
SETLOCAL 0
LOCAL 5
SETLOCAL 1
LOCAL 2
PUSH
LIT 1
ADD
SETLOCAL 2
PUSH
LIT 10
CULT
JNZ DECIMALPLACE
LABEL DECIMALSHOW
LOCAL 2
JZ DECIMALDONE
PUSH
LIT 1
SUB
SETLOCAL 2
ADDR DECIMAL
PUSH
LOCAL 2
ADD
FETCHB
PUTC
JMP DECIMALSHOW
LABEL DECIMALDONE
LIT 0
RETURN
```

### Edit at old physical position 4

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.

PROC MAIN 0 0
```

Remove:

```ir
LIT 65535
CALL PRINTNUM
```

Insert in its place:

```ir
LIT 1
PUSH
LIT 1
PUSH
INVOKE PRINT32 2
```

The following old source remains:

```ir
LIT 0
RETURN
```

### Edit at old physical position 2

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
```

Remove:

```ir

```

Insert in its place:

```ir
BUFFER DECIMAL 10
```

The following old source remains:

```ir
PROC MAIN 0 0
LIT 65535
```

## Build and check

```dos
COPY R03.IR SOURCE.IR
CHECK IRKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 01659 bytes`. Save RESULT.COM as R03.COM. VIEW.BAS must show length 1659.

```dos
CHECK R03
```

Require:

```text
0000065537PASS
```

