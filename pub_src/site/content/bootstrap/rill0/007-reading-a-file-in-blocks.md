+++
title = "07 \u00b7 Reading a File in Blocks"
weight = 7
description = "Refill the input block only after consuming its valid bytes."
download = "R07.IR"
download_group = "tools/rill0"
reader_names = 1
aliases = ["/bootstrap/rill/007-a-bounded-source-refill/", "/bootstrap/rill/07-a-filename-in-declared-storage/"]
url = "/bootstrap/rill/007-reading-a-file-in-blocks/"
+++

Refill the input block only after consuming its valid bytes. A short positive read still contains data; zero is EOF. Keep checked source-line counts separately.

FILEARG and FILESAME select the source through ARGC and ARG. Their default names are used only when there is no command tail. The first file-using driver obtains its selected name before OPEN; the same helpers are retained by later file-using checkpoints. Invalid counts, equal input/output names and reserved recovery names exit with failure before output creation. The native PSP handling remains in IR86, outside this compiler implementation.

## Enter the source

Copy R06.IR to R07.IR. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 17

Unchanged source before the edit:

```ir
PUSH
LIT 1
CNE
```

Insert in its place:

```ir
JNZ SYNTAX
LABEL NEXTDONE
LIT 0
RETURN
LABEL NEXTMARK
LIT 1
ST ENDED
LABEL NEXTEND
LIT 0
ST CH
```

The following old source remains:

```ir
RETURN
```

### Edit at old physical position 16

Unchanged source before the edit:

```ir
INVOKE DIGIT 1
PUSH
LIT 1
```

Insert in its place:

```ir
ADD
ST LINE
JNZ NEXTREAD
LD LINEHI
PUSH
LIT 1
ADD
ST LINEHI
JZ CAPFAIL
LABEL NEXTREAD
LD ENDED
JNZ NEXTEND
LD INPOS
PUSH
LD INLEN
CULT
JNZ NEXTBYTE
LD INPUT
PUSH
ADDR INBUF
PUSH
LIT 4096
READ
ST INLEN
STATUS
JNZ IOFAIL
LIT 0
ST INPOS
LD INLEN
JZ NEXTMARK
LABEL NEXTBYTE
ADDR INBUF
PUSH
LD INPOS
ADD
FETCHB
ST CH
LD INPOS
PUSH
LIT 1
ADD
ST INPOS
LD CH
PUSH
LIT 26
CEQ
JNZ NEXTMARK
LD CH
JZ SYNTAX
PUSH
LIT 127
CUGE
JNZ SYNTAX
LD CH
PUSH
LIT 32
CUGE
JNZ NEXTDONE
LD CH
PUSH
LIT 9
CEQ
JNZ NEXTDONE
LD CH
PUSH
LIT 10
CEQ
JNZ NEXTDONE
LD CH
PUSH
LIT 13
```

The following old source remains:

```ir
CNE
RETURN
```

### Edit at old physical position 13

Unchanged source before the edit:

```ir
PROC MAIN 0 0
LIT 57
PUSH
```

Remove:

```ir
INVOKE DIGIT 1
```

Insert in its place:

```ir
LITS "SOURCE.RIL"
PUSH
INVOKE FILEARG 2
LIT 1
PUSH
LITS "SOURCE.RIL"
PUSH
INVOKE FILEARG 2
OPEN
ST INPUT
STATUS
JNZ IOFAIL
CALL NEXT
LD CH
PUSH
LIT 65
CNE
RETURN

PROC NEXT 0 1
LD CH
PUSH
LIT 10
CNE
JNZ NEXTREAD
LD LINE
```

The following old source remains:

```ir
PUSH
LIT 1
```

### Edit at old physical position 11

Unchanged source before the edit:

```ir
WORD BACKUP 0
BUFFER DECIMAL 10
PROC MAIN 0 0
```

Remove:

```ir
LIT 57
```

Insert in its place:

```ir
LIT 1
```

The following old source remains:

```ir
PUSH
INVOKE DIGIT 1
```

### Edit at old physical position 10

Unchanged source before the edit:

```ir
WORD OWN 0
WORD BACKUP 0
BUFFER DECIMAL 10
```

Insert in its place:

```ir
BUFFER INBUF 4096
```

The following old source remains:

```ir
PROC MAIN 0 0
LIT 57
```

### Edit at old physical position 7

Unchanged source before the edit:

```ir
WORD LINEHI 0
WORD INPUT 0
WORD OUTPUT 0
```

Insert in its place:

```ir
WORD INPOS 0
WORD INLEN 0
WORD ENDED 0
```

The following old source remains:

```ir
WORD OWN 0
WORD BACKUP 0
```

### Edit at old physical position 3

Unchanged source before the edit:

```ir
; RILL compiler construction. Portable IR source.
WORD TABLE 0
```

Insert in its place:

```ir
WORD CH 0
```

The following old source remains:

```ir
WORD LINE 1
WORD LINEHI 0
```

## Build and check

```dos
CHECK IRKEEP R07.IR RESULT.ASM
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 07545 bytes`. Save RESULT.COM as R07.COM. VIEW.BAS must show length 7545.

Create T07.RIL:

```rill
A
```

```dos
CHECK R07 T07.RIL RESULT.IR
```

Require PASS.

The driver compares the result with 65 and returns nonzero on a mismatch; it adds no display routine.

## Check the new boundary

Choose an absent disk filename, ABSENT.RIL, and run:

```dos
CHECK R07 ABSENT.RIL RESULT.IR
```

Require:

```text
ERROR 0000000001 CODE 00001
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

