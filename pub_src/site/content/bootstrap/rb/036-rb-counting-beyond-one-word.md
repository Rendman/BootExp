+++
title = "03 \u00b7 Counting Beyond 65535"
weight = 3
description = "Treat the two words as one unsigned count."
download = "RB03.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/036-rb-counting-beyond-one-word/"]
reader_names = 1
+++

## The working parts

Treat the two words as one unsigned count. Divide the high word by ten, then carry its remainder through the low word one bit at a time. Store the remainders and display them in reverse order, including leading zeroes.

## Enter the source

Copy RB02.IR to RB03.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
PROC ERROR 1 0
LIT 1
EXIT
```

Insert after old physical line 115.

Insert:

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

### Edit 2

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–36 in RB02.IR:

```ir
LIT 65535
CALL PRINTNUM
```

Replace it with:

```ir
LIT 1
PUSH
LIT 1
PUSH
INVOKE PRINT32 2
```

The following old source remains in place:

```ir
LIT 0
RETURN
```

## Build this stopping point

```dos
COPY RB03.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000009364 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 10562 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB03.COM
```

VIEW.BAS must report RB03.COM length 10562 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB03
```

Require:

```text
0000065537
PASS
```

## If the result differs

Compare PRINT32 with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
