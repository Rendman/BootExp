+++
title = "IW23 \u00b7 Checked block access"
weight = 59
description = "Validate an opaque block and byte extent before reading or writing a word."
download = "IW23.ASM"
download_group = "toolchain"
+++

Validate an opaque block and byte extent before reading or writing a word.

## The working parts

Validate an opaque block and byte extent before reading or writing a word. The assembly routines use the inherited bounded reader and owned-file cleanup. The operation table supplies argument class, stack action, and an authored target template. Native encodings belong to this backend; the IR operation retains its abstract meaning.

## Enter the source

Copy IW22.ASM to IW23.ASM. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```asm
DW T_ALLOC
DB 70,82,69,69,66,76,79,67,75,0,0,0,0,0
DW T_FREEBLOCK
```

Insert after old physical line 1961.

Insert:

```asm
DB 82,69,78,65,77,69,0,0,0,0,0,2,0,0
DW T_RENAME
DB 71,69,84,56,0,0,0,0,0,0,0,2,0,0
DW T_GET8
DB 71,69,84,49,54,0,0,0,0,0,0,2,0,0
DW T_GET16
DB 83,69,84,56,0,0,0,0,0,0,0,3,0,0
DW T_SET8
DB 83,69,84,49,54,0,0,0,0,0,0,3,0,0
DW T_SET16
```

### Edit 2

Unchanged source immediately before the edit:

```asm
DW T_LITS
DB 69,88,73,83,84,83,0,0,0,0,0,0,0,0
DW T_EXISTS
```

Remove this source at old physical positions 1954–1957 in IW22.ASM:

```asm
DB 68,69,76,69,84,69,0,0,0,0,0,0,0,0
DW T_DELETE
DB 82,69,78,65,77,69,0,0,0,0,0,2,0,0
DW T_RENAME
```

There is no replacement source.

The following old source remains in place:

```asm
DB 65,76,76,79,67,0,0,0,0,0,0,0,0,0
DW T_ALLOC
```

### Edit 3

Unchanged source immediately before the edit:

```asm
DW T_CSGE
DB 76,73,84,83,0,0,0,0,0,0,6,0,0,0
DW T_LITS
```

Insert after old physical line 1951.

Insert:

```asm
DB 80,85,84,67,0,0,0,0,0,0,0,0,0,0
DW T_PUTC
DB 71,69,84,67,0,0,0,0,0,0,0,0,0,0
DW T_GETC
DB 79,80,69,78,0,0,0,0,0,0,0,0,0,0
DW T_OPEN
DB 67,82,69,65,84,69,0,0,0,0,0,0,0,0
DW T_CREATE
DB 67,76,79,83,69,0,0,0,0,0,0,0,0,0
DW T_CLOSE
DB 83,84,65,84,85,83,0,0,0,0,0,0,0,0
DW T_STATUS
DB 82,69,65,68,0,0,0,0,0,0,0,3,0,0
DW T_READ
DB 87,82,73,84,69,0,0,0,0,0,0,3,0,0
DW T_WRITE
DB 68,69,76,69,84,69,0,0,0,0,0,0,0,0
DW T_DELETE
```

The following old source remains in place:

```asm
DB 69,88,73,83,84,83,0,0,0,0,0,0,0,0
DW T_EXISTS
```

### Edit 4

Unchanged source immediately before the edit:

```asm
DW T_SETPARAM
DB 80,65,68,68,82,0,0,0,0,0,1,0,0,0
DW T_PADDR
```

Remove this source at old physical positions 1916–1949 in IW22.ASM:

```asm
DB 77,85,76,0,0,0,0,0,0,0,0,2,0,0
DW T_MUL
DB 67,69,81,0,0,0,0,0,0,0,0,2,0,0
DW T_CEQ
DB 78,69,71,0,0,0,0,0,0,0,0,0,0,0
DW T_NEG
DB 78,79,84,0,0,0,0,0,0,0,0,0,0,0
DW T_NOT
DB 68,73,86,0,0,0,0,0,0,0,0,2,0,0
DW T_DIV
DB 77,79,68,0,0,0,0,0,0,0,0,2,0,0
DW T_MOD
DB 83,72,76,0,0,0,0,0,0,0,0,2,0,0
DW T_SHL
DB 83,72,82,0,0,0,0,0,0,0,0,2,0,0
DW T_SHR
DB 67,78,69,0,0,0,0,0,0,0,0,2,0,0
DW T_CNE
DB 67,85,76,84,0,0,0,0,0,0,0,2,0,0
DW T_CULT
DB 67,85,76,69,0,0,0,0,0,0,0,2,0,0
DW T_CULE
DB 67,85,71,84,0,0,0,0,0,0,0,2,0,0
DW T_CUGT
DB 67,85,71,69,0,0,0,0,0,0,0,2,0,0
DW T_CUGE
DB 67,83,76,84,0,0,0,0,0,0,0,2,0,0
DW T_CSLT
DB 67,83,76,69,0,0,0,0,0,0,0,2,0,0
DW T_CSLE
DB 67,83,71,84,0,0,0,0,0,0,0,2,0,0
DW T_CSGT
DB 67,83,71,69,0,0,0,0,0,0,0,2,0,0
DW T_CSGE
```

There is no replacement source.

The following old source remains in place:

```asm
DB 76,73,84,83,0,0,0,0,0,0,6,0,0,0
DW T_LITS
```

### Edit 5

Unchanged source immediately before the edit:

```asm
DW T_CALL
DB 82,69,84,0,0,0,0,0,0,0,0,4,0,0
DW T_RET
```

Remove this source at old physical positions 1882–1897 in IW22.ASM:

```asm
DB 80,85,84,67,0,0,0,0,0,0,0,0,0,0
DW T_PUTC
DB 83,84,65,84,85,83,0,0,0,0,0,0,0,0
DW T_STATUS
DB 71,69,84,67,0,0,0,0,0,0,0,0,0,0
DW T_GETC
DB 79,80,69,78,0,0,0,0,0,0,0,0,0,0
DW T_OPEN
DB 67,82,69,65,84,69,0,0,0,0,0,0,0,0
DW T_CREATE
DB 82,69,65,68,0,0,0,0,0,0,0,3,0,0
DW T_READ
DB 87,82,73,84,69,0,0,0,0,0,0,3,0,0
DW T_WRITE
DB 67,76,79,83,69,0,0,0,0,0,0,0,0,0
DW T_CLOSE
```

There is no replacement source.

The following old source remains in place:

```asm
DB 80,82,79,67,0,0,0,0,0,0,4,0,0,0
DW T_PROC
```

### Edit 6

Unchanged source immediately before the edit:

```asm
DW T_JZ
DB 74,78,90,0,0,0,0,0,0,0,2,4,0,0
DW T_JNZ
```

Remove this source at old physical positions 1858–1877 in IW22.ASM:

```asm
DB 69,81,0,0,0,0,0,0,0,0,2,2,0,0
DW T_EQ
DB 78,69,0,0,0,0,0,0,0,0,2,2,0,0
DW T_NE
DB 85,76,84,0,0,0,0,0,0,0,2,2,0,0
DW T_ULT
DB 85,76,69,0,0,0,0,0,0,0,2,2,0,0
DW T_ULE
DB 85,71,84,0,0,0,0,0,0,0,2,2,0,0
DW T_UGT
DB 85,71,69,0,0,0,0,0,0,0,2,2,0,0
DW T_UGE
DB 83,76,84,0,0,0,0,0,0,0,2,2,0,0
DW T_SLT
DB 83,76,69,0,0,0,0,0,0,0,2,2,0,0
DW T_SLE
DB 83,71,84,0,0,0,0,0,0,0,2,2,0,0
DW T_SGT
DB 83,71,69,0,0,0,0,0,0,0,2,2,0,0
DW T_SGE
```

Replace it with:

```asm
DB 74,77,80,0,0,0,0,0,0,0,2,4,0,0
DW T_JMP
```

The following old source remains in place:

```asm
DB 67,65,76,76,0,0,0,0,0,0,2,0,0,0
DW T_CALL
```

### Edit 7

Unchanged source immediately before the edit:

```asm
DW T_OR
DB 88,79,82,0,0,0,0,0,0,0,0,2,0,0
DW T_XOR
```

Remove this source at old physical positions 1848–1853 in IW22.ASM:

```asm
DB 80,85,84,0,0,0,0,0,0,0,0,2,0,0
DW T_PUT
DB 80,85,84,66,0,0,0,0,0,0,0,2,0,0
DW T_PUTB
DB 74,77,80,0,0,0,0,0,0,0,2,4,0,0
DW T_JMP
```

Replace it with:

```asm
DB 83,85,66,0,0,0,0,0,0,0,0,2,0,0
DW T_SUB
DB 77,85,76,0,0,0,0,0,0,0,0,2,0,0
DW T_MUL
DB 68,73,86,0,0,0,0,0,0,0,0,2,0,0
DW T_DIV
DB 77,79,68,0,0,0,0,0,0,0,0,2,0,0
DW T_MOD
DB 83,72,76,0,0,0,0,0,0,0,0,2,0,0
DW T_SHL
DB 83,72,82,0,0,0,0,0,0,0,0,2,0,0
DW T_SHR
DB 69,81,0,0,0,0,0,0,0,0,2,2,0,0
DW T_EQ
DB 67,69,81,0,0,0,0,0,0,0,0,2,0,0
DW T_CEQ
DB 78,69,0,0,0,0,0,0,0,0,2,2,0,0
DW T_NE
DB 67,78,69,0,0,0,0,0,0,0,0,2,0,0
DW T_CNE
DB 85,76,84,0,0,0,0,0,0,0,2,2,0,0
DW T_ULT
DB 67,85,76,84,0,0,0,0,0,0,0,2,0,0
DW T_CULT
DB 85,76,69,0,0,0,0,0,0,0,2,2,0,0
DW T_ULE
DB 67,85,76,69,0,0,0,0,0,0,0,2,0,0
DW T_CULE
DB 85,71,84,0,0,0,0,0,0,0,2,2,0,0
DW T_UGT
DB 67,85,71,84,0,0,0,0,0,0,0,2,0,0
DW T_CUGT
DB 85,71,69,0,0,0,0,0,0,0,2,2,0,0
DW T_UGE
DB 67,85,71,69,0,0,0,0,0,0,0,2,0,0
DW T_CUGE
DB 83,76,84,0,0,0,0,0,0,0,2,2,0,0
DW T_SLT
DB 67,83,76,84,0,0,0,0,0,0,0,2,0,0
DW T_CSLT
DB 83,76,69,0,0,0,0,0,0,0,2,2,0,0
DW T_SLE
DB 67,83,76,69,0,0,0,0,0,0,0,2,0,0
DW T_CSLE
DB 83,71,84,0,0,0,0,0,0,0,2,2,0,0
DW T_SGT
DB 67,83,71,84,0,0,0,0,0,0,0,2,0,0
DW T_CSGT
DB 83,71,69,0,0,0,0,0,0,0,2,2,0,0
DW T_SGE
DB 67,83,71,69,0,0,0,0,0,0,0,2,0,0
DW T_CSGE
```

The following old source remains in place:

```asm
DB 74,90,0,0,0,0,0,0,0,0,2,4,0,0
DW T_JZ
```

### Edit 8

Unchanged source immediately before the edit:

```asm
DW T_POP
DB 65,68,68,0,0,0,0,0,0,0,0,2,0,0
DW T_ADD
```

Remove this source at old physical positions 1840–1841 in IW22.ASM:

```asm
DB 83,85,66,0,0,0,0,0,0,0,0,2,0,0
DW T_SUB
```

There is no replacement source.

The following old source remains in place:

```asm
DB 65,78,68,0,0,0,0,0,0,0,0,2,0,0
DW T_AND
```

### Edit 9

Unchanged source immediately before the edit:

```asm
DW T_PUSH
DB 80,79,80,0,0,0,0,0,0,0,0,2,0,0
DW T_POP
```

Insert after old physical line 1837.

Insert:

```asm
DB 80,85,84,0,0,0,0,0,0,0,0,2,0,0
DW T_PUT
DB 80,85,84,66,0,0,0,0,0,0,0,2,0,0
DW T_PUTB
```

The following old source remains in place:

```asm
DB 65,68,68,0,0,0,0,0,0,0,0,2,0,0
DW T_ADD
```

### Edit 10

Unchanged source immediately before the edit:

```asm
DW T_FETCH
DB 70,69,84,67,72,66,0,0,0,0,0,0,0,0
DW T_FETCHB
```

Insert after old physical line 1833.

Insert:

```asm
DB 78,69,71,0,0,0,0,0,0,0,0,0,0,0
DW T_NEG
DB 78,79,84,0,0,0,0,0,0,0,0,0,0,0
DW T_NOT
```

The following old source remains in place:

```asm
DB 80,85,83,72,0,0,0,0,0,0,0,1,0,0
DW T_PUSH
```

### Edit 11

Unchanged source immediately before the edit:

```asm
DW T_LDB
DB 83,84,66,0,0,0,0,0,0,0,2,0,0,0
DW T_STB
```

Remove this source at old physical positions 1828–1829 in IW22.ASM:

```asm
DB 65,68,68,82,0,0,0,0,0,0,2,0,0,0
DW T_ADDR
```

There is no replacement source.

The following old source remains in place:

```asm
DB 70,69,84,67,72,0,0,0,0,0,0,0,0,0
DW T_FETCH
```

### Edit 12

Unchanged source immediately before the edit:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
DW T_LIT
```

Remove this source at old physical positions 1806–1813 in IW22.ASM:

```asm
DB 72,65,76,84,0,0,0,0,0,0,0,4,0,0
DW T_HALT
DB 76,65,66,69,76,0,0,0,0,0,2,0,0,0
DW T_LABEL
DB 78,79,80,0,0,0,0,0,0,0,0,0,0,0
DW T_NOP
DB 69,88,73,84,0,0,0,0,0,0,0,4,0,0
DW T_EXIT
```

Replace it with:

```asm
DB 65,68,68,82,0,0,0,0,0,0,2,0,0,0
DW T_ADDR
```

The following old source remains in place:

```asm
DB 87,79,82,68,0,0,0,0,0,0,3,4,0,0
DW T_WORD
```

### Edit 13

Unchanged source immediately before the edit:

```asm
DB 69,78,65,77,69,13,10,0

IRTAB:
```

Insert after old physical line 1803.

Insert:

```asm
DB 78,79,80,0,0,0,0,0,0,0,0,0,0,0
DW T_NOP
DB 72,65,76,84,0,0,0,0,0,0,0,4,0,0
DW T_HALT
DB 69,88,73,84,0,0,0,0,0,0,0,4,0,0
DW T_EXIT
DB 76,65,66,69,76,0,0,0,0,0,2,0,0,0
DW T_LABEL
```

The following old source remains in place:

```asm
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
DW T_LIT
```

### Edit 14

Unchanged source immediately before the edit:

```asm
DB 80,79,80,32,68,88,13,10,67,65,76,76,32,82,95,82
DB 69,78,65,77,69,13,10,0
```

Insert after old physical line 1802.

Insert:

```asm
T_GET8:
DB 80,79,80,32,66,88,13,10,77,79,86,32,67,88,44,49
DB 13,10,67,65,76,76,32,82,95,71,69,84,77,69,77,13
DB 10,0

T_GET16:
DB 80,79,80,32,66,88,13,10,77,79,86,32,67,88,44,50
DB 13,10,67,65,76,76,32,82,95,71,69,84,77,69,77,13
DB 10,0

T_SET8:
DB 80,79,80,32,68,88,13,10,80,79,80,32,66,88,13,10
DB 77,79,86,32,67,88,44,49,13,10,67,65,76,76,32,82
DB 95,83,69,84,77,69,77,13,10,0

T_SET16:
DB 80,79,80,32,68,88,13,10,80,79,80,32,66,88,13,10
DB 77,79,86,32,67,88,44,50,13,10,67,65,76,76,32,82
DB 95,83,69,84,77,69,77,13,10,0
```

The following old source remains in place:

```asm
IRTAB:
DB 76,73,84,0,0,0,0,0,0,0,1,0,0,0
```

### Edit 15

Unchanged source immediately before the edit:

```asm
DB 77,79,86,32,65,88,44,68,73,13,10,74,77,80,32,82
DB 95,79,75,13,10,82,95,65,76,76,79,67,66,65,68,58
DB 13,10,77,79,86,32,65,88,44,67,83,13,10,77,79,86
```

Remove this source at old physical positions 1450–1477 in IW22.ASM:

```asm
DB 32,69,83,44,65,88,13,10,74,77,80,32,82,95,70,65
DB 73,76,13,10,82,95,70,82,69,69,66,76,79,67,75,58
DB 13,10,77,79,86,32,66,88,44,65,88,13,10,67,77,80
DB 32,66,88,44,49,13,10,74,66,32,78,69,65,82,32,82
DB 95,68,70,65,73,76,13,10,67,77,80,32,66,88,44,49
DB 54,13,10,74,65,32,78,69,65,82,32,82,95,68,70,65
DB 73,76,13,10,68,69,67,32,66,88,13,10,83,72,76,32
DB 66,88,44,49,13,10,83,72,76,32,66,88,44,49,13,10
DB 65,68,68,32,66,88,44,82,95,66,76,79,67,75,83,13
DB 10,77,79,86,32,83,73,44,66,88,13,10,77,79,86,32
DB 65,88,44,91,83,73,93,13,10,67,77,80,32,65,88,44
DB 48,13,10,74,69,32,78,69,65,82,32,82,95,68,70,65
DB 73,76,13,10,77,79,86,32,69,83,44,65,88,13,10,77
DB 79,86,32,65,72,44,52,57,72,13,10,73,78,84,32,50
DB 49,72,13,10,74,67,32,78,69,65,82,32,82,95,70,82
DB 69,69,66,65,68,13,10,77,79,86,32,87,79,82,68,32
DB 91,83,73,93,44,48,13,10,77,79,86,32,65,88,44,67
DB 83,13,10,77,79,86,32,69,83,44,65,88,13,10,77,79
DB 86,32,65,88,44,48,13,10,74,77,80,32,82,95,79,75
DB 13,10,82,95,70,82,69,69,66,65,68,58,13,10,77,79
DB 86,32,65,88,44,67,83,13,10,77,79,86,32,69,83,44
DB 65,88,13,10,74,77,80,32,82,95,70,65,73,76,13,10
DB 13,10,82,95,83,84,65,67,75,70,65,73,76,58,13,10
DB 77,79,86,32,65,88,44,52,67,48,50,72,13,10,73,78
DB 84,32,50,49,72,13,10,13,10,82,95,87,65,78,84,58
DB 13,10,68,87,32,48,13,10,82,95,77,69,77,86,65,76
DB 85,69,58,13,10,68,87,32,48,13,10,82,95,66,76,79
DB 67,75,83,58,13,10,82,69,83,87,32,51,50,13,10,0
```

Replace it with:

```asm
DB 32,69,83,44,65,88,13,10,77,79,86,32,65,88,44,48
DB 13,10,74,77,80,32,82,95,79,75,13,10,82,95,70,82
DB 69,69,66,65,68,58,13,10,77,79,86,32,65,88,44,67
DB 83,13,10,77,79,86,32,69,83,44,65,88,13,10,74,77
DB 80,32,82,95,70,65,73,76,13,10,82,95,83,84,65,67
DB 75,70,65,73,76,58,13,10,77,79,86,32,65,88,44,52
DB 67,48,50,72,13,10,73,78,84,32,50,49,72,13,10,82
DB 95,87,65,78,84,58,13,10,68,87,32,48,13,10,82,95
DB 77,69,77,86,65,76,85,69,58,13,10,68,87,32,48,13
DB 10,82,95,66,76,79,67,75,83,58,13,10,82,69,83,87
DB 32,51,50,13,10,0
```

The following old source remains in place:

```asm

T_LITS:
```

### Edit 16

Unchanged source immediately before the edit:

```asm
DB 82,95,68,70,65,73,76,13,10,77,79,86,32,91,82,95
DB 87,65,78,84,93,44,65,88,13,10,77,79,86,32,65,88
DB 44,67,83,13,10,77,79,86,32,69,83,44,65,88,13,10
```

Remove this source at old physical positions 1421–1448 in IW22.ASM:

```asm
DB 77,79,86,32,66,88,44,49,48,48,48,72,13,10,77,79
DB 86,32,65,72,44,52,65,72,13,10,73,78,84,32,50,49
DB 72,13,10,74,67,32,78,69,65,82,32,82,95,68,70,65
DB 73,76,13,10,77,79,86,32,83,73,44,82,95,66,76,79
DB 67,75,83,13,10,77,79,86,32,68,73,44,49,13,10,82
DB 95,65,76,76,79,67,83,76,79,84,58,13,10,67,77,80
DB 32,87,79,82,68,32,91,83,73,93,44,48,13,10,74,69
DB 32,78,69,65,82,32,82,95,65,76,76,79,67,70,79,85
DB 78,68,13,10,65,68,68,32,83,73,44,52,13,10,73,78
DB 67,32,68,73,13,10,67,77,80,32,68,73,44,49,55,13
DB 10,74,66,32,78,69,65,82,32,82,95,65,76,76,79,67
DB 83,76,79,84,13,10,74,77,80,32,82,95,70,65,73,76
DB 13,10,82,95,65,76,76,79,67,70,79,85,78,68,58,13
DB 10,77,79,86,32,66,88,44,91,82,95,87,65,78,84,93
DB 13,10,77,79,86,32,67,76,44,52,13,10,83,72,82,32
DB 66,88,44,67,76,13,10,77,79,86,32,65,88,44,91,82
DB 95,87,65,78,84,93,13,10,65,78,68,32,65,88,44,49
DB 53,13,10,67,77,80,32,65,88,44,48,13,10,74,69,32
DB 78,69,65,82,32,82,95,65,76,76,79,67,82,79,85,78
DB 68,13,10,73,78,67,32,66,88,13,10,82,95,65,76,76
DB 79,67,82,79,85,78,68,58,13,10,77,79,86,32,65,72
DB 44,52,56,72,13,10,73,78,84,32,50,49,72,13,10,74
DB 67,32,78,69,65,82,32,82,95,65,76,76,79,67,66,65
DB 68,13,10,77,79,86,32,91,83,73,93,44,65,88,13,10
DB 77,79,86,32,65,88,44,91,82,95,87,65,78,84,93,13
DB 10,77,79,86,32,91,83,73,43,50,93,44,65,88,13,10
DB 77,79,86,32,65,88,44,68,73,13,10,74,77,80,32,82
DB 95,79,75,13,10,82,95,65,76,76,79,67,66,65,68,58
```

Replace it with:

```asm
DB 77,79,86,32,65,88,44,48,13,10,82,69,84,13,10,82
DB 95,71,69,84,77,69,77,58,13,10,80,85,83,72,32,67
DB 88,13,10,67,65,76,76,32,82,95,66,76,79,67,75,80
DB 84,82,13,10,80,79,80,32,67,88,13,10,67,77,80,32
DB 65,88,44,48,13,10,74,69,32,78,69,65,82,32,82,95
DB 68,70,65,73,76,13,10,77,79,86,32,65,76,44,69,83
DB 58,91,66,88,93,13,10,77,79,86,32,65,72,44,48,13
DB 10,67,77,80,32,67,88,44,49,13,10,74,69,32,78,69
DB 65,82,32,82,95,77,69,77,68,79,78,69,13,10,77,79
DB 86,32,65,88,44,69,83,58,91,66,88,93,13,10,82,95
DB 77,69,77,68,79,78,69,58,13,10,77,79,86,32,68,88
DB 44,67,83,13,10,77,79,86,32,69,83,44,68,88,13,10
DB 74,77,80,32,82,95,79,75,13,10,82,95,83,69,84,77
DB 69,77,58,13,10,77,79,86,32,91,82,95,77,69,77,86
DB 65,76,85,69,93,44,65,88,13,10,77,79,86,32,65,88
DB 44,68,88,13,10,67,65,76,76,32,82,95,66,76,79,67
DB 75,80,84,82,13,10,67,77,80,32,65,88,44,48,13,10
DB 74,69,32,78,69,65,82,32,82,95,68,70,65,73,76,13
DB 10,77,79,86,32,65,88,44,91,82,95,77,69,77,86,65
DB 76,85,69,93,13,10,67,77,80,32,67,88,44,49,13,10
DB 74,78,69,32,78,69,65,82,32,82,95,83,69,84,87,79
DB 82,68,13,10,77,79,86,32,69,83,58,91,66,88,93,44
DB 65,76,13,10,74,77,80,32,82,95,77,69,77,68,79,78
DB 69,13,10,82,95,83,69,84,87,79,82,68,58,13,10,77
DB 79,86,32,69,83,58,91,66,88,93,44,65,88,13,10,74
DB 77,80,32,82,95,77,69,77,68,79,78,69,13,10,82,95
DB 70,82,69,69,66,76,79,67,75,58,13,10,77,79,86,32
DB 66,88,44,65,88,13,10,67,77,80,32,66,88,44,49,13
DB 10,74,66,32,78,69,65,82,32,82,95,68,70,65,73,76
DB 13,10,67,77,80,32,66,88,44,49,54,13,10,74,65,32
DB 78,69,65,82,32,82,95,68,70,65,73,76,13,10,68,69
DB 67,32,66,88,13,10,83,72,76,32,66,88,44,49,13,10
DB 83,72,76,32,66,88,44,49,13,10,65,68,68,32,66,88
DB 44,82,95,66,76,79,67,75,83,13,10,77,79,86,32,83
DB 73,44,66,88,13,10,77,79,86,32,65,88,44,91,83,73
DB 93,13,10,67,77,80,32,65,88,44,48,13,10,74,69,32
DB 78,69,65,82,32,82,95,68,70,65,73,76,13,10,77,79
DB 86,32,69,83,44,65,88,13,10,77,79,86,32,65,72,44
DB 52,57,72,13,10,73,78,84,32,50,49,72,13,10,74,67
DB 32,78,69,65,82,32,82,95,70,82,69,69,66,65,68,13
DB 10,77,79,86,32,87,79,82,68,32,91,83,73,93,44,48
```

The following old source remains in place:

```asm
DB 13,10,77,79,86,32,65,88,44,67,83,13,10,77,79,86
DB 32,69,83,44,65,88,13,10,74,77,80,32,82,95,70,65
```

### Edit 17

Unchanged source immediately before the edit:

```asm
DB 48,13,10,74,77,80,32,82,95,79,75,13,10,82,95,69
DB 70,65,73,76,58,13,10,77,79,86,32,65,88,44,54,53
DB 53,51,53,13,10,74,77,80,32,82,95,69,82,82,79,82
```

Remove this source at old physical positions 1416–1419 in IW22.ASM:

```asm
DB 13,10,13,10,82,95,65,76,76,79,67,58,13,10,67,77
DB 80,32,65,88,44,48,13,10,74,69,32,78,69,65,82,32
DB 82,95,68,70,65,73,76,13,10,77,79,86,32,91,82,95
DB 87,65,78,84,93,44,65,88,13,10,77,79,86,32,65,88
```

Replace it with:

```asm
DB 13,10,82,95,65,76,76,79,67,58,13,10,67,77,80,32
DB 65,88,44,48,13,10,74,69,32,78,69,65,82,32,82,95
DB 68,70,65,73,76,13,10,77,79,86,32,91,82,95,87,65
DB 78,84,93,44,65,88,13,10,77,79,86,32,65,88,44,67
DB 83,13,10,77,79,86,32,69,83,44,65,88,13,10,77,79
DB 86,32,66,88,44,49,48,48,48,72,13,10,77,79,86,32
DB 65,72,44,52,65,72,13,10,73,78,84,32,50,49,72,13
DB 10,74,67,32,78,69,65,82,32,82,95,68,70,65,73,76
DB 13,10,77,79,86,32,83,73,44,82,95,66,76,79,67,75
DB 83,13,10,77,79,86,32,68,73,44,49,13,10,82,95,65
DB 76,76,79,67,83,76,79,84,58,13,10,67,77,80,32,87
DB 79,82,68,32,91,83,73,93,44,48,13,10,74,69,32,78
DB 69,65,82,32,82,95,65,76,76,79,67,70,79,85,78,68
DB 13,10,65,68,68,32,83,73,44,52,13,10,73,78,67,32
DB 68,73,13,10,67,77,80,32,68,73,44,49,55,13,10,74
DB 66,32,78,69,65,82,32,82,95,65,76,76,79,67,83,76
DB 79,84,13,10,74,77,80,32,82,95,70,65,73,76,13,10
DB 82,95,65,76,76,79,67,70,79,85,78,68,58,13,10,77
DB 79,86,32,66,88,44,91,82,95,87,65,78,84,93,13,10
DB 77,79,86,32,67,76,44,52,13,10,83,72,82,32,66,88
DB 44,67,76,13,10,77,79,86,32,65,88,44,91,82,95,87
DB 65,78,84,93,13,10,65,78,68,32,65,88,44,49,53,13
DB 10,67,77,80,32,65,88,44,48,13,10,74,69,32,78,69
DB 65,82,32,82,95,65,76,76,79,67,82,79,85,78,68,13
DB 10,73,78,67,32,66,88,13,10,82,95,65,76,76,79,67
DB 82,79,85,78,68,58,13,10,77,79,86,32,65,72,44,52
DB 56,72,13,10,73,78,84,32,50,49,72,13,10,74,67,32
DB 78,69,65,82,32,82,95,65,76,76,79,67,66,65,68,13
DB 10,77,79,86,32,91,83,73,93,44,65,88,13,10,77,79
DB 86,32,65,88,44,91,82,95,87,65,78,84,93,13,10,77
DB 79,86,32,91,83,73,43,50,93,44,65,88,13,10,77,79
DB 86,32,65,88,44,68,73,13,10,74,77,80,32,82,95,79
DB 75,13,10,82,95,65,76,76,79,67,66,65,68,58,13,10
DB 77,79,86,32,65,88,44,67,83,13,10,77,79,86,32,69
DB 83,44,65,88,13,10,74,77,80,32,82,95,70,65,73,76
DB 13,10,82,95,66,76,79,67,75,80,84,82,58,13,10,67
DB 77,80,32,66,88,44,49,13,10,74,66,32,78,69,65,82
DB 32,82,95,66,76,79,67,75,66,65,68,13,10,67,77,80
DB 32,66,88,44,49,54,13,10,74,65,32,78,69,65,82,32
DB 82,95,66,76,79,67,75,66,65,68,13,10,68,69,67,32
DB 66,88,13,10,83,72,76,32,66,88,44,49,13,10,83,72
DB 76,32,66,88,44,49,13,10,65,68,68,32,66,88,44,82
DB 95,66,76,79,67,75,83,13,10,77,79,86,32,83,73,44
DB 66,88,13,10,77,79,86,32,66,88,44,91,83,73,93,13
DB 10,67,77,80,32,66,88,44,48,13,10,74,69,32,78,69
DB 65,82,32,82,95,66,76,79,67,75,66,65,68,13,10,77
DB 79,86,32,69,83,44,66,88,13,10,77,79,86,32,66,88
DB 44,91,83,73,43,50,93,13,10,67,77,80,32,65,88,44
DB 66,88,13,10,74,65,69,32,78,69,65,82,32,82,95,66
DB 76,79,67,75,66,65,68,13,10,83,85,66,32,66,88,44
DB 65,88,13,10,67,77,80,32,66,88,44,67,88,13,10,74
DB 66,32,78,69,65,82,32,82,95,66,76,79,67,75,66,65
DB 68,13,10,77,79,86,32,66,88,44,65,88,13,10,77,79
DB 86,32,65,88,44,49,13,10,82,69,84,13,10,82,95,66
DB 76,79,67,75,66,65,68,58,13,10,77,79,86,32,65,88
```

The following old source remains in place:

```asm
DB 44,67,83,13,10,77,79,86,32,69,83,44,65,88,13,10
DB 77,79,86,32,66,88,44,49,48,48,48,72,13,10,77,79
```

### Edit 18

Unchanged source immediately before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove this source at old physical positions 834–834 in IW22.ASM:

```asm
MOV CX,79
```

Replace it with:

```asm
MOV CX,83
```

The following old source remains in place:

```asm
MOV AX,16
CALL LOOK
```

### Edit 19

Unchanged source immediately before the edit:

```asm
INT 21H
RET
```

Insert after old physical line 466.

Insert:

```asm
NUMBER:
PUSH AX
PUSH BX
PUSH CX
PUSH DX
PUSH SI
MOV CX,AX
MOV SI,DIVISORS
NEXTPLACE:
MOV BX,SI
MOV DX,[BX]
MOV AL,48
SUBTRACT:
CMP CX,DX
JB NEAR PRINTDIGIT
SUB CX,DX
ADD AL,1
JMP SUBTRACT
PRINTDIGIT:
MOV DL,AL
MOV AH,2
INT 21H
ADD SI,2
CMP SI,DIVEND
JB NEAR NEXTPLACE
POP SI
POP DX
POP CX
POP BX
POP AX
RET
```

The following old source remains in place:

```asm
ERROR:
MOV [ERRCODE],AL
```

## Build this stopping point

```dos
COPY IW23.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 11577 bytes` and PASS, then save it:

```dos
COPY RESULT.COM IW23.COM
```

VIEW.BAS must report IW23.COM length 11577 bytes. Keep this executable and its source together.

## Acceptance check

Create TIW23.IR with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```ir
WORD H 0
PROC MAIN 0 0
LIT 40960
ALLOC
ST H
LD H
PUSH
LIT 40958
PUSH
LIT 4660
SET16
LD H
PUSH
LIT 40958
GET16
PUSH
LIT 4660
CNE
PUSH
LD H
FREEBLOCK
POP
RETURN
```

```dos
COPY TIW23.IR SOURCE.IR
```

```dos
CHECK IW23
```

Require, apart from command echo and the checker's separator:

```text
OK RESULT.ASM 0000005314 text bytes
PASS
```

```dos
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require `OK RESULT.COM 01133 bytes` and PASS before copying it to TRY.COM. VIEW.BAS must show length 1133 and these first thirty-two bytes:

```text
FC 81 FC FE FF 74 03 E9 1A 04 E8 06 00 B4 4C CD 21 00 00 55 8B EC 81 EC 00 00 81 FC 00 F0 73 03
```

Run CHECK TRY. It returns zero and the checker reports PASS.

```dos
COPY IW23.COM IRWIDE.COM
COPY IRWIDE.COM IWKEEP.COM
```

Preserve IWKEEP as the fixed-file translator. The earlier IRKEEP retains its source-name prompt. IRWIDE.ASM and IW23.ASM are identical.

## A rejection or boundary check

Create XIW23.IR:

```ir
UNKNOWN
```

```dos
COPY XIW23.IR SOURCE.IR
CHECK IW23
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

The accepted RESULT.ASM must remain unchanged. An unexpected PASS fails this check.

## If the result differs

Check the saved pointer or slot, argument order, complete token spelling, and STATUS immediately after each service. A helper's local state must survive calls; an output count is independent of input position. Inspect text and file length before interpreting any bytes as a program.
