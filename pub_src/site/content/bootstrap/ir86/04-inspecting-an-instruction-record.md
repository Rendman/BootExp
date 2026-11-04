+++
title = "04 \u00b7 Inspecting an instruction record"
weight = 4
description = "Search fixed records and display the target-size field."
download = "IR04.ASM"
+++

Before using an instruction record to select target text, we can inspect the result of its lookup directly.

## How it works

LOOK is the published ASM86 table search. BX supplies the table address, CX its count, and AX a record stride of fourteen bytes. It returns a record in BX or zero and preserves the source cursor SI. The record begins with a zero-padded name.

After the eight name bytes, each record holds an argument class, expression effect, target-byte count, one padding byte, and a word pointer to its text pattern. The driver advances to the target-byte field, clears AH, and passes the value to NUMBER. FINISH rejects an unwanted operand before anything is reported.

The text-output routines from the preceding checkpoint remain in the source. This diagnostic does not call them or create an assembly file. Keeping the tested routines in place avoids entering them again merely to inspect a table lookup. The display distinguishes NOP and HALT and a missing name is an explicit syntax error.

## Source changes

Copy `IR03.ASM` to `IR04.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

LOOK and FINISH are the routines already entered in the ASM86 collection. Their complete added blocks below may be copied from AS09.ASM; compare the printed source when placing them here.

### Change 1: following `SPACE:`

Unchanged code immediately before the edit:

```asm
SPACE:
DB 32,36

```

Remove these exact old lines (physical positions 390–391 in `IR03.ASM`):

```asm
CRLF:
DB 13,10,0
```

Put this source in their place:

```asm
T_NOP:
DB 78,79,80,13,10,0

T_HALT:
DB 77,79,86,32,65,88,44,52,67,48,48,72,13,10,73,78
DB 84,32,50,49,72,13,10,0
```

### Change 2: following `OUTPTR:`

Unchanged code immediately before the edit:

```asm
OUTPTR:
DW 24576

```

Insert after old physical line 371, before the following old line.

Insert this source:

```asm
TOKLEN:
DW 0

STRIDE:
DW 0

```

### Change 3: following `OUTDONE:`

Unchanged code immediately before the edit:

```asm
OUTDONE:
RET

```

Insert after old physical line 330, before the following old line.

Insert this source:

```asm
OPTAB:
DB 78,79,80,0,0,0,0,0,0,0,1,0
DW T_NOP
DB 72,65,76,84,0,0,0,0,0,5,5,0
DW T_HALT

```

### Change 4: following `READFAIL:`

Unchanged code immediately before the edit:

```asm
MOV [LINENO],DX
JMP ERROR

```

Insert after old physical line 192, before the following old line.

Insert this source:

```asm
SCAN:
MOV DI,2300H
SCANSPACE:
LODSB
CMP AL,32
JE SCANSPACE
CMP AL,0
JE SCANEND
CMP AL,59
JE SCANEND
STOSB
CMP AL,44
JE SCANDONE
CMP AL,58
JE SCANDONE
CMP AL,91
JE SCANDONE
CMP AL,93
JE SCANDONE
SCANMORE:
LODSB
CMP AL,0
JE SCANBACK
CMP AL,32
JE SCANBACK
CMP AL,59
JE SCANBACK
CMP AL,44
JE SCANBACK
CMP AL,58
JE SCANBACK
CMP AL,91
JE SCANBACK
CMP AL,93
JE SCANBACK
CMP DI,2310H
JAE TOKENBAD
STOSB
JMP SCANMORE
SCANBACK:
DEC SI
SCANDONE:
MOV AX,DI
SUB AX,2300H
MOV [TOKLEN],AX
MOV AL,0
STOSB
RET
SCANEND:
DEC SI
JMP SCANDONE
TOKENBAD:
MOV AX,1
JMP ERROR

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

### Change 5: following `DRIVERDONE:`

Unchanged code immediately before the edit:

```asm
JMP DRIVERLINE
DRIVERDONE:
CALL CLOSEFILE
```

Remove these exact old lines (physical positions 24–24 in `IR03.ASM`):

```asm
CALL WRITEOUT
```

No replacement source is needed.

### Change 6: following `DRIVERLINE:`

Unchanged code immediately before the edit:

```asm
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
```

Remove these exact old lines (physical positions 18–20 in `IR03.ASM`):

```asm
CALL OUTTEXT
MOV SI,CRLF
CALL OUTTEXT
```

Put this source in their place:

```asm
CALL SCAN
MOV BX,OPTAB
MOV CX,2
MOV AX,14
CALL LOOK
CMP BX,0
JNE RECORDOK
MOV AX,1
JMP ERROR
RECORDOK:
ADD BX,10
MOV AL,[BX]
MOV AH,0
PUSH AX
CALL FINISH
POP AX
CALL NUMBER
MOV DX,NEWLINE
CALL TEXT
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR04` at ASM86's `Source name:` prompt. Require `OK 01065 bytes` followed by PASS. This builds `IR04.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T04.IR` with `COPY CON T04.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
NOP
HALT
```

```dos
CHECK IR04
```

Enter `T04` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T04
00001
00005
PASS
```

This diagnostic creates no assembly file. Its displayed text is the test result.

## A rejection check

Enter this separate input as `X04.IR` using COPY CON and the same end-of-input keystroke:

```ir
UNKNOWN
```

Run `CHECK IR04` and enter `X04`. Require this diagnostic and FAIL:

```text
IR ERROR 00001 CODE 1
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the record stride and count, the saved template pointer, and each substitution buffer. The name and numeric token must survive FINISH. Compare the generated assembly before asking ASM86 to assemble it.
