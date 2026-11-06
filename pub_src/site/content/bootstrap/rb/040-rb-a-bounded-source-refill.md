+++
title = "07 \u00b7 Reading a File in Blocks"
weight = 7
description = "INPOS and INLEN describe an already-read block."
download = "RB07.IR"
download_group = "tools/rillboot"
aliases = ["/bootstrap/rill/040-rb-a-bounded-source-refill/"]
reader_names = 1
+++

## The working parts

INPOS and INLEN describe an already-read block. Refill only after consuming it. A short positive read is data, not EOF. Check STATUS before using a count. Control-Z ends source text; the byte services used by a compiled program still preserve that value.

## Enter the source

Copy RB06.IR to RB07.IR. Apply edits **from the bottom of the old file upward**. Physical positions refer to that unchanged old file; use the printed context to identify each place. Keep all other source.

### Edit 1

Unchanged source immediately before the edit:

```ir
PUSH
LIT 1
CNE
```

Insert after old physical line 40.

Insert:

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

The following old source remains in place:

```ir
RETURN
```

### Edit 2

Unchanged source immediately before the edit:

```ir
INVOKE DIGIT 1
PUSH
LIT 1
```

Insert after old physical line 39.

Insert:

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

The following old source remains in place:

```ir
CNE
RETURN
```

### Edit 3

Unchanged source immediately before the edit:

```ir
PROC MAIN 0 0
LIT 57
PUSH
```

Remove this source at old physical positions 37–37 in RB06.IR:

```ir
INVOKE DIGIT 1
```

Replace it with:

```ir
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

The following old source remains in place:

```ir
PUSH
LIT 1
```

### Edit 4

Unchanged source immediately before the edit:

```ir
WORD EXPRDEPTH 0

PROC MAIN 0 0
```

Remove this source at old physical positions 35–35 in RB06.IR:

```ir
LIT 57
```

Replace it with:

```ir
LITS "SOURCE.RIL"
OPEN
ST INPUT
STATUS
JNZ IOFAIL
CALL NEXT
LD CH
```

The following old source remains in place:

```ir
PUSH
INVOKE DIGIT 1
```

## Build this stopping point

```dos
COPY RB07.IR SOURCE.IR
```

```dos
CHECK IWKEEP
COPY RESULT.ASM SOURCE.ASM
CHECK ASMAKEEP
```

Require IR86 `OK RESULT.ASM 0000014102 text bytes` and PASS **before** the copy. Require assembler `OK RESULT.COM 11455 bytes` and PASS before saving:

```dos
COPY RESULT.COM RB07.COM
```

VIEW.BAS must report RB07.COM length 11455 bytes. Keep this executable and its source together.

## Acceptance check

Create TRB07.RIL with COPY CON or a plain-text editor. Finish COPY CON with Ctrl-Z and Enter:

```rill
A
```

```dos
COPY TRB07.RIL SOURCE.RIL
```

```dos
CHECK RB07
```

The checker must report PASS. The driver compares the result with 65 and returns nonzero on a mismatch; it adds no display routine.

## A rejection or boundary check

Rename SOURCE.RIL to an unused HOLD.RIL and run CHECK RB07. Restore the source afterward.

Require:

```text
ERROR 0000000001 CODE 00001
FAIL
```

An unexpected PASS fails the rejection. The pre-existing RESULT.IR must remain unchanged; preserve a copy before the test.

## If the result differs

Check the refill position and returned byte count. A short positive read still contains data; only zero means EOF.
