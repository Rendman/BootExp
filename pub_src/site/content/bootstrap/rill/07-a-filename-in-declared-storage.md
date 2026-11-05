+++
title = "07 \u00b7 A filename in declared storage"
weight = 7
description = "Build a terminated name through portable pointers."
download = "R07.IR"
+++

OPEN needs a filename in storage. Its pointer must come from ADDR rather than a guessed address.

## The working parts

NAMEBUF reserves twelve bytes. SOURCENAME fills it with SOURCE.RIL and a zero terminator. NAMEWORD stores one packed word at PLACE and advances PLACE by two valid bytes. VALUE temporarily saves the incoming word while the pointer is prepared.

The driver walks that declared buffer with FETCHB until zero. Its cursor is TOKENVAL; CHAR does not change it. The final spare zero byte is harmless. The exact packed constants and the resulting displayed name provide independent ways to inspect the data.

## Enter the source

Copy `R06.IR` to `R07.IR`. Apply these edits **from the bottom of the old file upward**. Physical positions are only locators; the printed old context and nearby labels identify each place. Retain the rest of the file.

### Change 1: following `LABEL ERROR`

Unchanged source immediately before the edit:

```ir
CALL NEWLINE
LIT 1
EXIT
```

Insert after old physical line 138, before the following old line.

Insert this source:

```ir
; NAMETEXT
LABEL NAMEWORD
ST VALUE
LD PLACE
PUSH
LD VALUE
PUT
LD PLACE
PUSH
LIT 2
ADD
ST PLACE
RET
LABEL SOURCENAME
ADDR NAMEBUF
ST PLACE
LIT 20307
CALL NAMEWORD
LIT 21077
CALL NAMEWORD
LIT 17731
CALL NAMEWORD
LIT 21038
CALL NAMEWORD
LIT 19529
CALL NAMEWORD
LIT 0
CALL NAMEWORD
RET
```

### Change 2: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
LABEL MAIN
GETC
PUSH
```

Remove these exact old lines (physical positions 14–19 in `R06.IR`):

```ir
LIT 65
NE SYNTAX
LIT 19279
CALL PAIR
LIT 2573
CALL PAIR
```

Put this source in their place:

```ir
LIT 1
ADD
ST TOKENVAL
JMP NAMEDISPLAY
LABEL NAMEDONE
CALL NEWLINE
```

### Change 3: following `LABEL MAIN`

Unchanged source immediately before the edit:

```ir
WORD COUNT 0
; Driver
LABEL MAIN
```

Remove these exact old lines (physical positions 12–12 in `R06.IR`):

```ir
GETC
```

Put this source in their place:

```ir
CALL SOURCENAME
ADDR NAMEBUF
ST TOKENVAL
LABEL NAMEDISPLAY
LD TOKENVAL
FETCHB
JZ NAMEDONE
CALL CHAR
LD TOKENVAL
```

### Change 4: in the declarations

Unchanged source immediately before the edit:

```ir
WORD PLACE 0
WORD STEP 0
WORD COUNT 0
```

Insert after old physical line 9, before the following old line.

Insert this source:

```ir
WORD TOKENVAL 0
; FILENAMES
BUFFER NAMEBUF 12
```

## Build the stopping point

```dos
CHECK IRKEEP
```

Enter `R07` at `IR source name:`. Require `OK R07.ASM 05147 text bytes` and PASS. Then run `CHECK ASMKEEP`, enter `R07` at `Source name:`, and require `OK 00949 bytes` and PASS. Save the source and executable before testing.

## Acceptance check

Run `CHECK R07`. This checkpoint does not read SOURCE.RIL.

Apart from DOS command echo and the checker's separating blank line, require:

```text
SOURCE.RIL
PASS
```

This is a diagnostic stopping point. It does not create RESULT.IR.

## A rejection check

The program has no source-language reader at this stopping point. Check an IR transcription error independently: create BAD.IR with this text:

```ir
LABEL MAIN
PUTC EXTRA
```

Run CHECK IRKEEP and enter BAD. Require:

```text
IR ERROR 00002 CODE 1
FAIL
```

The unwanted operand must prevent BAD.ASM from being created. If an older BAD.ASM exists, it must remain unchanged.

An unexpected PASS is a failed rejection test.

## If the result differs

Check each service STATUS immediately, the current-byte advance, and any shared work cell needed across a call. Compare token values with the printed result before changing the parser.
