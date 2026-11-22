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

In BASIC I kept instruction names in a chain of IF statements. In assembly I want one search routine and a small table it can walk. I'll try that routine on `DB` and `DW` before using it inside the parser.

**Starting source:** `AS07.ASM`. **Save as:** `AS08.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

LOOK takes BX as the first record, CX as the record count, and AX as the record size in bytes. Each record begins with a zero-terminated name. It returns the matching record's address in BX, or zero if no record matches. It preserves SI, the source cursor, and changes AX, BX, CX, DX, DI, BP, STRIDE, and flags.

BP retains the current record's base while DI walks its name. The token is compared from its beginning for every candidate. Both names must reach zero together, so DB cannot match a longer prefix. On a mismatch the saved stride advances BP to the next record and the count is reduced.

The demonstration table uses eight-byte records: six bytes for a short name and its zero padding, then a class byte and a parameter byte. DB's parameter is zero; DW's is one. This is a table test, not yet a parser for either directive. The driver prints the parameter after a successful lookup and rejects an absent name.

The search count is checked before reading a record, including a count of zero. The routine uses two stack bytes for its saved SI, in addition to its return address. Keeping the stride in STRIDE is safe here because LOOK does not call itself or another LOOK while a search is active.

## Source changes

Copy `AS07.ASM` to `AS08.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `ERRCODE:`

Find the unique label `ERRCODE:`, then follow this unchanged source through its last displayed instruction:

```asm
ERRCODE:
DB 0
```

The edit begins immediately after that unchanged block.

Insert:

```asm
OPTAB:
DB 68,66,0,0,0,0,1,0
DB 68,87,0,0,0,0,1,1
```

### Change 2 · `ENDED:`

Find the unique label `ENDED:`. Insert the new source immediately before this existing label:

```asm
ENDED:
```

Insert:

```asm
STRIDE:
DW 0
```

### Change 3 · `ZTEXT:`

Find the unique label `ZTEXT:`. The old block below starts at that label.

Remove this existing source:

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

Keep the following `ERRMSG:` label and the source after it in place.

### Change 4 · `TEXT:`

Find the unique label `TEXT:`. Insert the new source immediately before this existing label:

```asm
TEXT:
```

Insert:

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

### Change 5 · `TRACETOKEN:`

Find the unique label `TRACETOKEN:`, then follow this unchanged source through its last displayed instruction:

```asm
TRACETOKEN:
CALL SCAN
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
MOV DX,NEWLINE
CALL TEXT
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JMP TRACETOKEN
```

With:

```asm
JMP DRIVERLINE
```

Keep the following `DRIVERDONE:` label and the source after it in place.

### Change 6 · `TRACETOKEN:`

Find the unique label `TRACETOKEN:`, then follow this unchanged source through its last displayed instruction:

```asm
TRACETOKEN:
CALL SCAN
```

The edit begins immediately after that unchanged block.

Replace this existing source:

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

With:

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

### Change 7 · `TRACETOKEN:`

Find the unique label `TRACETOKEN:`. The old block below starts at that label.

Remove this existing source:

```asm
TRACETOKEN:
```

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

Check the eight-byte record stride and the explicit record count. LOOK must compare both zero terminators; accepting a prefix would confuse a short name with a longer one.
