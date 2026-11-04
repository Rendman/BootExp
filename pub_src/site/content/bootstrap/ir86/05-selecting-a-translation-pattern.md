+++
title = "05 \u00b7 Selecting a translation pattern"
weight = 5
description = "A small instruction table selects fixed assembly text."
download = "IR05.ASM"
+++

Repeated target sequences belong in a table. We shall recognize NOP and HALT and emit their fixed assembly patterns.

## How it works

LOOK is the published fixed-record search. BX is the table base, CX the record count, and AX the stride. It returns a record in BX or zero, preserving the source cursor SI. Each IR record reserves eight bytes for its zero-padded name, then argument class, stack effect, target byte count, one padding byte, and a word template pointer. The stride is fourteen.

STATEMENT retains these fields before another routine can change the lookup registers. FINISH rejects an extra token. EXPAND walks the selected zero-terminated assembly pattern from SI; the patterns currently contain only literal characters. Templates are text data, not preassembled instruction bytes.

HALT emits a zero-status DOS termination. LAST records a terminal instruction so the normal end-of-source exit need not be repeated. When the last statement can fall through, FINISHOUTPUT appends HALT. Its target is the same documented ASM86 instruction vocabulary.

## Source changes

Copy `IR04.ASM` to `IR05.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_HALT:`

Unchanged code immediately before the edit:

```asm
T_HALT:
DB 77,79,86,32,65,88,44,52,67,48,48,72,13,10,73,78
DB 84,32,50,49,72,13,10,0
```

Insert after old physical line 520, before the following old line.

Insert this source:

```asm

T_NOP:
DB 78,79,80,13,10,0
```

### Change 2: following `SPACE:`

Unchanged code immediately before the edit:

```asm
SPACE:
DB 32,36

```

Remove these exact old lines (physical positions 515–516 in `IR04.ASM`):

```asm
T_NOP:
DB 78,79,80,13,10,0
```

Put this source in their place:

```asm
TPL:
DW 0

CLASS:
DB 0

EFFECT:
DB 0

INSIZE:
DB 0

LAST:
DB 0
```

### Change 3: following `OUTTEXT:`

Unchanged code immediately before the edit:

```asm
CMP AL,0
JE OUTDONE
CALL EMITCHAR
```

Remove these exact old lines (physical positions 440–441 in `IR04.ASM`):

```asm
JMP OUTTEXT
OUTDONE:
```

Put this source in their place:

```asm
JMP EXPAND
EXPANDDONE:
RET

FINISHOUTPUT:
MOV AL,[LAST]
CMP AL,1
JE OUTPUTDONE
MOV SI,T_HALT
CALL EXPAND
OUTPUTDONE:
```

### Change 4: following `OUTTEXT:`

Unchanged code immediately before the edit:

```asm
OUTTEXT:
LODSB
CMP AL,0
```

Remove these exact old lines (physical positions 438–438 in `IR04.ASM`):

```asm
JE OUTDONE
```

Put this source in their place:

```asm
JE EXPANDDONE
```

### Change 5: following `TEXTFULL:`

Unchanged code immediately before the edit:

```asm
MOV AX,5
JMP ERROR

```

Remove these exact old lines (physical positions 435–435 in `IR04.ASM`):

```asm
OUTTEXT:
```

Put this source in their place:

```asm
EXPAND:
```

### Change 6: following `ZDONE:`

Unchanged code immediately before the edit:

```asm
ZDONE:
RET

```

Insert after old physical line 378, before the following old line.

Insert this source:

```asm
STATEMENT:
CALL SCAN
MOV AL,[2300H]
CMP AL,0
JNE STATWORD
RET
STATWORD:
MOV BX,OPTAB
MOV CX,2
MOV AX,14
CALL LOOK
CMP BX,0
JNE STATFOUND
MOV AX,1
JMP ERROR
STATFOUND:
ADD BX,8
MOV AL,[BX]
MOV [CLASS],AL
INC BX
MOV AL,[BX]
MOV [EFFECT],AL
INC BX
MOV AL,[BX]
MOV [INSIZE],AL
ADD BX,2
MOV AX,[BX]
MOV [TPL],AX
MOV AL,[EFFECT]
CMP AL,5
MOV AL,0
JNE STATLAST
MOV AL,1
STATLAST:
MOV [LAST],AL
CALL FINISH
MOV SI,[TPL]
CALL EXPAND
RET

```

### Change 7: following `DRIVERDONE:`

Unchanged code immediately before the edit:

```asm
JMP DRIVERLINE
DRIVERDONE:
CALL CLOSEFILE
```

Insert after old physical line 39, before the following old line.

Insert this source:

```asm
CALL FINISHOUTPUT
CALL WRITEOUT
```

### Change 8: following `DRIVERLINE:`

Unchanged code immediately before the edit:

```asm
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
```

Remove these exact old lines (physical positions 18–36 in `IR04.ASM`):

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

Put this source in their place:

```asm
CALL STATEMENT
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR05` at ASM86's `Source name:` prompt. Require `OK 01146 bytes` followed by PASS. This builds `IR05.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T05.IR` with `COPY CON T05.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
NOP
HALT
```

```dos
CHECK IR05
```

Enter `T05` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T05
OK T05.ASM 00028 text bytes
PASS
```

Run `TYPE T05.ASM`. Its complete text must be:

```asm
NOP
MOV AX,4C00H
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T05`. Require `OK 00006 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T05.COM`, and require length **6 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
90 B8 00 4C CD 21
```

`T05.COM` is a complete program. Run `CHECK T05`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X05.IR` using COPY CON and the same end-of-input keystroke:

```ir
NOP 1
```

Run `CHECK IR05` and enter `X05`. Require this diagnostic and FAIL:

```text
IR ERROR 00001 CODE 1
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the record stride and count, the saved template pointer, and each substitution buffer. The name and numeric token must survive FINISH. Compare the generated assembly before asking ASM86 to assemble it.
