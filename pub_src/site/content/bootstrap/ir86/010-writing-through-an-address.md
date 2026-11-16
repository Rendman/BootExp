+++
title = "10 \u00b7 Writing through an address"
weight = 10
description = "Store a word through a portable pointer and inspect the saved result."
download = "IR10.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/046-iw-calls-and-returns/", "/bootstrap/ir86/10-loading-and-storing-a-word/"]
+++

Store a word through a portable pointer and inspect the saved result.

## Enter the source

Copy IR09.ASM to IR10.ASM. Apply the following edits from the bottom of the old file upward, using the old physical positions and unchanged context. Keep all other source.

### Edit at old physical position 1430

Unchanged source before the edit:

```asm
DW T_JNZ
DB 67,69,81,0,0,0,0,0,0,0,0,2,0,0
DW T_CEQ
```

Insert in its place:

```asm
DB 80,85,84,0,0,0,0,0,0,0,0,2,0,0
DW T_PUT
DB 80,85,84,66,0,0,0,0,0,0,0,2,0,0
DW T_PUTB
```

The following old source remains:

```asm

CMDCOUNT:
```

### Edit at old physical position 1339

Unchanged source before the edit:

```asm
DB "POP AX",13,10
DB 0
```

Insert in its place:

```asm
T_PUT:
DB "POP BX",13,10
DB "MOV [BX],AX",13,10
DB 0

T_PUTB:
DB "POP BX",13,10
DB "MOV [BX],AL",13,10
DB 0
```

The following old source remains:

```asm
T_ADD:
DB "POP BX",13,10
```

### Edit at old physical position 872

Unchanged source before the edit:

```asm
CMP AL,0
JE NEAR STATDONE
MOV BX,IRTAB
```

Remove:

```asm
MOV CX,20
```

Insert in its place:

```asm
MOV CX,22
```

The following old source remains:

```asm
MOV AX,16
CALL LOOK
```

## Build and check

```dos
CHECK ASMAKEEP IR10.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 04093 bytes`. Save RESULT.COM as IR10.COM. VIEW.BAS must show length 4093.

Create T10.IR:

```ir
WORD X 0
LABEL MAIN
ADDR X
PUSH
LIT 65
PUT
LD X
EXIT
```

```dos
CHECK IR10 T10.IR RESULT.ASM
```

Require:

```text
OK RESULT.ASM 0000000229 text bytes
PASS
```

```dos
CHECK ASMAKEEP RESULT.ASM RESULT.COM
```

Require OK and PASS. VIEW.BAS must show RESULT.COM length 42 and these leading bytes:

```text
FC 81 FC FE FF 74 03 E9 1B 00 E8 06 00 B4 4C CD 21 00 00 B8 11 01 50 B8 41 00 5B 89 07 8B 06 11
```

Copy it to TRY.COM. CHECK TRY reports FAIL because the test returns 65.

## Check the new boundary

Save this separate rejected source as X10.IR:

```ir
UNKNOWN
```

```dos
CHECK IR10 X10.IR RESULT.ASM
```

Require:

```text
IR ERROR 0000000001 CODE 1
FAIL
```

An unexpected PASS fails this check. Keep a copy of the accepted result before testing; it must remain unchanged.

