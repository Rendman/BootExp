+++
title = "18 \u00b7 Recording a Name and Its Meaning"
weight = 18
description = "Initialize the entire forty-byte record, copy the complete spelling, then write the explicit fields."
download = "RB18.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/051-rb-initialize-a-complete-symbol/"]
reader_names = 1
+++

## The working parts

Initialize the entire forty-byte record, copy the complete spelling, then write the explicit fields. The global region begins at zero in TABLE; the local region begins at byte offset 20480.

## Enter the source

Copy RB17.IR to RB18.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
SET16
RETURN
```

Insert after old physical line 636.

Insert:

```ir
PROC RECORD 1 1
LIT 0
SETLOCAL 0
LABEL RECORDCLEAR
LD TABLE
PUSH
PARAM 0
PUSH
LOCAL 0
ADD
PUSH
LIT 0
SET8
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
PUSH
LIT 40
CULT
JNZ RECORDCLEAR
LIT 0
SETLOCAL 0
LABEL RECORDNAME
LD TABLE
PUSH
PARAM 0
PUSH
LOCAL 0
ADD
PUSH
ADDR IDENT
PUSH
LOCAL 0
ADD
FETCHB
SET8
JZ RECORDFIELDS
LOCAL 0
PUSH
LIT 1
ADD
SETLOCAL 0
JMP RECORDNAME
LABEL RECORDFIELDS
PARAM 0
PUSH
LIT 32
ADD
PUSH
LD RECTYPE
PUSH
INVOKE WRITEFIELD 2
PARAM 0
PUSH
LIT 34
ADD
PUSH
LD RECVAL
PUSH
INVOKE WRITEFIELD 2
PARAM 0
PUSH
LIT 36
ADD
PUSH
LD RECLEVEL
PUSH
INVOKE WRITEFIELD 2
PARAM 0
RETURN
```

The following old source remains in place:

```ir
PROC PRINT 0 1
SETLOCAL 0
```

### Edit 2

Unchanged source immediately before the edit:

```ir
LIT 100
CALL TWORD
PUSH
```

Remove this source at old physical positions 46–46 in RB17.IR:

```ir
LIT 4660
```

Replace it with:

```ir
LIT 12345
```

The following old source remains in place:

```ir
CNE
RETURN
```

### Edit 3

Unchanged source immediately before the edit:

```ir
ST TABLE
LIT 100
PUSH
```

Remove this source at old physical positions 40–43 in RB17.IR:

```ir
LIT 4660
PUSH
INVOKE WRITEFIELD 2
LIT 100
```

Replace it with:

```ir
INVOKE RECORD 1
LIT 1
ST GLOBALS
LIT 34
```

The following old source remains in place:

```ir
CALL TWORD
PUSH
```

### Edit 4

Unchanged source immediately before the edit:

```ir
LIT 22000
ALLOC
ST TABLE
```

Remove this source at old physical positions 38–38 in RB17.IR:

```ir
LIT 100
```

Replace it with:

```ir
LITS "ABC"
CALL SETIDENT
LIT 1
ST RECTYPE
LIT 12345
ST RECVAL
LIT 0
ST RECLEVEL
LIT 0
```

The following old source remains in place:

```ir
PUSH
LIT 4660
```

## Build this stopping point

```dos
COPY RB18.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000024947 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 13588 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB18.COM
```

VIEW.BAS must report RB18.COM length 13588 bytes. Keep this executable and its source together.

## Acceptance check

```dos
CHECK RB18
```

The checker must report PASS. The driver compares the result with 12345 and returns nonzero on a mismatch; it adds no display routine.

## If the result differs

Compare RECORD with the printed addition. Check its arguments and saved state across calls, then inspect the generated text or bytes.
