+++
title = "08 \u00b7 Looking up a table entry"
weight = 8
description = "Compare a token with fixed-size records."
download = "AS08.ASM"
cartoon = "asm86-postroom.png"
aliases = ["/bootstrap/asm86/09-looking-up-a-table-entry/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/08-looking-up-a-table-entry/"
+++

Instruction names and register names belong in small tables. We shall write one search routine and test it with two records.

## How it works

LOOK takes BX as the first record, CX as the record count, and AX as the record size in bytes. Each record begins with a zero-terminated name. It returns the matching record's address in BX, or zero if no record matches. It preserves SI, the source cursor, and changes AX, BX, CX, DX, DI, BP, STRIDE, and flags.

BP retains the current record's base while DI walks its name. The token is compared from its beginning for every candidate. Both names must reach zero together, so DB cannot match a longer prefix. On a mismatch the saved stride advances BP to the next record and the count is reduced.

The demonstration table uses eight-byte records: six bytes for a short name and its zero padding, then a class byte and a parameter byte. DB's parameter is zero; DW's is one. This is a table test, not yet a parser for either directive. The driver prints the parameter after a successful lookup and rejects an absent name.

The search count is checked before reading a record, including a count of zero. The routine uses two stack bytes for its saved SI, in addition to its return address. Keeping the stride in STRIDE is safe here because LOOK does not call itself or another LOOK while a search is active.

## Source changes

Copy `AS07.ASM` to `AS08.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `ERRCODE:`

Unchanged code immediately before this edit:

```asm

ERRCODE:
DB 0
```

Insert after old physical line 310, before the following old line.

Insert this source:

```asm

OPTAB:
DB 68,66,0,0,0,0,1,0
DB 68,87,0,0,0,0,1,1
```

### Change 2: following `TOKLEN:`

Unchanged code immediately before this edit:

```asm
TOKLEN:
DW 0

```

Insert after old physical line 299, before the following old line.

Insert this source:

```asm
STRIDE:
DW 0

```

### Change 3: following `ERROR:`

Unchanged code immediately before this edit:

```asm
MOV AX,4C01H
INT 21H

```

Remove these exact old lines (physical lines 263–273 of `AS07.ASM`):

```asm
ZTEXT:
LODSB
CMP AL,0
JE ZDONE
MOV DL,AL
MOV AH,2
INT 21H
JMP ZTEXT
ZDONE:
RET

```

No replacement lines are needed.

### Change 4: following `TOKENBAD:`

Unchanged code immediately before this edit:

```asm
MOV AX,1
JMP ERROR

```

Insert after old physical line 207, before the following old line.

Insert this source:

```asm
LOOK:
MOV [STRIDE],AX
PUSH SI
MOV BP,BX
LOOKNEXT:
CMP CX,0
JE LOOKMISS
MOV DI,BP
MOV SI,2300H
LOOKCHAR:
LODSB
MOV BX,DI
MOV DL,[BX]
CMP AL,DL
JNE LOOKSTEP
CMP AL,0
JE LOOKFOUND
INC DI
JMP LOOKCHAR
LOOKSTEP:
MOV AX,[STRIDE]
ADD BP,AX
DEC CX
JMP LOOKNEXT
LOOKFOUND:
MOV BX,BP
POP SI
RET
LOOKMISS:
MOV BX,0
POP SI
RET

FINISH:
CALL SCAN
MOV AL,[2300H]
CMP AL,0
JE FINISHED
MOV AX,1
JMP ERROR
FINISHED:
RET

```

### Change 5: following `TRACETOKEN:`

Unchanged code immediately before this edit:

```asm
INT 21H
MOV DX,NEWLINE
CALL TEXT
```

Remove these exact old lines (physical lines 32–32 of `AS07.ASM`):

```asm
JMP TRACETOKEN
```

Put this source in their place:

```asm
JMP DRIVERLINE
```

### Change 6: following `TRACETOKEN:`

Unchanged code immediately before this edit:

```asm
MOV SI,2200H
TRACETOKEN:
CALL SCAN
```

Remove these exact old lines (physical lines 17–29 of `AS07.ASM`):

```asm
MOV AL,[2300H]
CMP AL,0
JE DRIVERLINE
MOV DL,91
MOV AH,2
INT 21H
PUSH SI
MOV SI,2300H
CALL ZTEXT
POP SI
MOV DL,93
MOV AH,2
INT 21H
```

Put this source in their place:

```asm
MOV BX,OPTAB
MOV CX,2
MOV AX,8
CALL LOOK
CMP BX,0
JNE TRACEFOUND
MOV AX,1
JMP ERROR
TRACEFOUND:
ADD BX,7
MOV AL,[BX]
MOV AH,0
PUSH AX
CALL FINISH
POP AX
CALL NUMBER
```

### Change 7: following `DRIVERLINE:`

Unchanged code immediately before this edit:

```asm
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
```

Remove these exact old lines (physical lines 15–15 of `AS07.ASM`):

```asm
TRACETOKEN:
```

No replacement lines are needed.

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS08.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 682 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS08.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T08.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
DB
DW
```

```dos
COPY T08.ASM SOURCE.ASM
```

```dos
CHECK AS08
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
00000
00001
PASS
```

## A rejection check

Enter this separate file as `X08.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
UNKNOWN
```

```dos
COPY X08.ASM SOURCE.ASM
CHECK AS08
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 1
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
