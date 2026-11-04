+++
title = "03 \u00b7 Buffering assembly text"
weight = 3
description = "Keep a complete text result before creating its output file."
download = "IR03.ASM"
+++

We shall collect text in memory, then write one .ASM file only after the input has been accepted.

## How it works

OUTPTR begins at 6000H. EMITCHAR takes one character in AL and advances that pointer, preserving AX and BX. It checks the E000H upper bound before a store. OUTTEXT walks a zero-terminated string from SI and sends each character through EMITCHAR; SI, AL, and flags are scratch.

WRITEOUT changes the saved extension to .ASM, uses DOS function 3CH to create or truncate the output, and writes the collected count with function 40H. Carry and the returned byte count are checked. CLOSEFILE must succeed before the OK report. A read or syntax failure leaves an older output untouched; a write or close failure can leave a partial file.

The success count is a count of assembly-text bytes, including CR/LF, not a machine-code image size. At this checkpoint the source lines are simply copied in normalized form. The test is data for inspection, not an executable program.

## Source changes

Copy `IR02.ASM` to `IR03.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `IREXT:`

Unchanged code immediately before the edit:

```asm

IREXT:
DB 46,73,82,0
```

Insert after old physical line 377, before the following old line.

Insert this source:

```asm

SPACE:
DB 32,36

CRLF:
DB 13,10,0
```

### Change 2: following `LINENO:`

Unchanged code immediately before the edit:

```asm
LINENO:
DW 0

```

Remove these exact old lines (physical positions 361–362 in `IR02.ASM`):

```asm
TOKLEN:
DW 0
```

Put this source in their place:

```asm
OUTPTR:
DW 24576
```

### Change 3: following `NEWLINE:`

Unchanged code immediately before the edit:

```asm

NEWLINE:
DB 13,10,36
```

Insert after old physical line 343, before the following old line.

Insert this source:

```asm

ASMEXT:
DB 46,65,83,77,0
```

### Change 4: following `PROMPT:`

Unchanged code immediately before the edit:

```asm
PROMPT:
DB 73,82,32,115,111,117,114,99,101,32,110,97,109,101,58,32
DB 36
```

Insert after old physical line 334, before the following old line.

Insert this source:

```asm

OKMSG:
DB 79,75,32,36

BYTEMSG:
DB 32,116,101,120,116,32,98,121,116,101,115,13,10,36
```

### Change 5: following `ZDONE:`

Unchanged code immediately before the edit:

```asm
ZDONE:
RET

```

Insert after old physical line 331, before the following old line.

Insert this source:

```asm
WRITEOUT:
MOV DI,[EXTP]
MOV SI,ASMEXT
CALL COPYZ
MOV DX,FNAME
MOV CX,0
MOV AH,3CH
INT 21H
JAE OUTPUTOPEN
JMP FILEBAD
OUTPUTOPEN:
MOV [HANDLE],AX
MOV BX,AX
MOV CX,[OUTPTR]
SUB CX,6000H
MOV DX,6000H
MOV AH,40H
INT 21H
JAE OUTPUTCHECK
JMP FILEBAD
OUTPUTCHECK:
CMP AX,CX
JE OUTPUTCLOSE
JMP FILEBAD
OUTPUTCLOSE:
CALL CLOSEFILE
MOV DX,OKMSG
CALL TEXT
MOV SI,FNAME
CALL ZTEXT
MOV DX,SPACE
CALL TEXT
MOV AX,[OUTPTR]
SUB AX,6000H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
RET

EMITCHAR:
PUSH BX
MOV BX,[OUTPTR]
CMP BX,0E000H
JB CHARROOM
JMP TEXTFULL
CHARROOM:
MOV [BX],AL
INC BX
MOV [OUTPTR],BX
CHARDONE:
POP BX
RET
TEXTFULL:
MOV AX,5
JMP ERROR

OUTTEXT:
LODSB
CMP AL,0
JE OUTDONE
CALL EMITCHAR
JMP OUTTEXT
OUTDONE:
RET

```

### Change 6: following `READFAIL:`

Unchanged code immediately before the edit:

```asm
MOV [LINENO],DX
JMP ERROR

```

Remove these exact old lines (physical positions 204–258 in `IR02.ASM`):

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

```

No replacement source is needed.

### Change 7: following `DRIVERDONE:`

Unchanged code immediately before the edit:

```asm
JMP TRACETOKEN
DRIVERDONE:
CALL CLOSEFILE
```

Insert after old physical line 35, before the following old line.

Insert this source:

```asm
CALL WRITEOUT
```

### Change 8: following `DRIVERLINE:`

Unchanged code immediately before the edit:

```asm
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
```

Remove these exact old lines (physical positions 16–33 in `IR02.ASM`):

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
JMP TRACETOKEN
```

Put this source in their place:

```asm
CALL OUTTEXT
MOV SI,CRLF
CALL OUTTEXT
JMP DRIVERLINE
```

### Change 9: following `ROOM:`

Unchanged code immediately before the edit:

```asm
JMP ERROR
ROOM:
CALL GETNAME
```

Insert after old physical line 9, before the following old line.

Insert this source:

```asm
MOV AX,6000H
MOV [OUTPTR],AX
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR03` at ASM86's `Source name:` prompt. Require `OK 00784 bytes` followed by PASS. This builds `IR03.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T03.IR` with `COPY CON T03.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
DB 65
```

```dos
CHECK IR03
```

Enter `T03` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T03
OK T03.ASM 00007 text bytes
PASS
```

Run `TYPE T03.ASM`. Its complete text must be:

```asm
DB 65
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T03`. Require `OK 00001 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T03.COM`, and require length **1 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
41
```

This target contains data only. **Inspect it; do not execute it.**

## A rejection check

Enter this separate input as `X03.IR` using COPY CON and the same end-of-input keystroke:

```ir
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

The unbroken X line has 121 characters, exceeding the 120-character physical input bound.

Run `CHECK IR03` and enter `X03`. Require this diagnostic and FAIL:

```text
IR ERROR 00001 CODE 5
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the .IR extension bytes, zero and dollar-sign terminators, and source-cursor saves. A file error is different from end of file; NEXTBYTE returns an explicit count.
