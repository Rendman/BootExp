+++
title = "09 \u00b7 A larger seed workspace"
weight = 9
description = "Separate the resident image, I/O blocks, symbols, and stack."
download = "A09.ASM"
+++

Streamed output frees the old image buffer, making room for more definitions.

## The working parts

The seed moves its line to 4000H, token to 4080H, input block to 4200H, output block to 4600H, and symbol table to 5000H. The 2048 twenty-byte records end at EFFFH. The upper 4 KB remain reserved for the stack.

DEFINE bounds the record count before copying a name. The code/static-data area is reserved below 4000H even though the initial image must still fit ASM86's smaller build limit. Emitted programs are written to disk and do not occupy this workspace.

## Enter the source

Copy `A08.ASM` to `A09.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `FLUSH:`

Unchanged source immediately before this edit:

```asm
CMP CX,0
JE FLUSHDONE
MOV BX,[OUTHANDLE]
```

Remove this exact source at old physical positions 1022–1022:

```asm
MOV DX,6000H
```

Replace it with:

```asm
MOV DX,4600H
```

The following old source stays in place:

```asm
MOV AH,40H
INT 21H
```

### Change 2 near `EMITROOM:`

Unchanged source immediately before this edit:

```asm
CMP AH,2
JNE COUNTBYTE
MOV BX,[OUTCNT]
```

Remove this exact source at old physical positions 900–900:

```asm
ADD BX,6000H
```

Replace it with:

```asm
ADD BX,4600H
```

The following old source stays in place:

```asm
MOV [BX],AL
MOV BX,[OUTCNT]
```

### Change 3 near `TWOOPERANDS:`

Unchanged source immediately before this edit:

```asm
MOV AX,[VAL]
MOV [V1],AX
CALL SCAN
```

Remove this exact source at old physical positions 735–735:

```asm
MOV AL,[2300H]
```

Replace it with:

```asm
MOV AL,[4080H]
```

The following old source stays in place:

```asm
CMP AL,44
JNE TWOBAD
```

### Change 4 near `FINISH:`

Unchanged source immediately before this edit:

```asm

FINISH:
CALL SCAN
```

Remove this exact source at old physical positions 716–716:

```asm
MOV AL,[2300H]
```

Replace it with:

```asm
MOV AL,[4080H]
```

The following old source stays in place:

```asm
CMP AL,0
JE FINISHED
```

### Change 5 near `DATASEP:`

Unchanged source immediately before this edit:

```asm
CALL BYTEVALUE
DATASEP:
CALL SCAN
```

Remove this exact source at old physical positions 638–638:

```asm
MOV AL,[2300H]
```

Replace it with:

```asm
MOV AL,[4080H]
```

The following old source stays in place:

```asm
CMP AL,44
JE DATAITEM
```

### Change 6 near `STATEMENT:`

Unchanged source immediately before this edit:

```asm

STATEMENT:
CALL SCAN
```

Remove this exact source at old physical positions 557–557:

```asm
MOV AL,[2300H]
```

Replace it with:

```asm
MOV AL,[4080H]
```

The following old source stays in place:

```asm
CMP AL,0
JNE STWORD
```

### Change 7 near `MEMORYEND:`

Unchanged source immediately before this edit:

```asm
MOV [REG],AL
MEMORYEND:
CALL SCAN
```

Remove this exact source at old physical positions 545–545:

```asm
MOV AL,[2300H]
```

Replace it with:

```asm
MOV AL,[4080H]
```

The following old source stays in place:

```asm
CMP AL,93
JE MEMORYOK
```

### Change 8 near `MEMORY:`

Unchanged source immediately before this edit:

```asm
MOV AX,[2300H]
CMP AX,5842H
JNE DIRECTMEM
```

Remove this exact source at old physical positions 532–532:

```asm
MOV AL,[2302H]
```

Replace it with:

```asm
MOV AL,[4082H]
```

The following old source stays in place:

```asm
CMP AL,0
JNE DIRECTMEM
```

### Change 9 near `MEMORY:`

Unchanged source immediately before this edit:

```asm

MEMORY:
CALL SCAN
```

Remove this exact source at old physical positions 529–529:

```asm
MOV AX,[2300H]
```

Replace it with:

```asm
MOV AX,[4080H]
```

The following old source stays in place:

```asm
CMP AX,5842H
JNE DIRECTMEM
```

### Change 10 near `OPERAND:`

Unchanged source immediately before this edit:

```asm

OPERAND:
CALL SCAN
```

Remove this exact source at old physical positions 502–502:

```asm
MOV AL,[2300H]
```

Replace it with:

```asm
MOV AL,[4080H]
```

The following old source stays in place:

```asm
CMP AL,91
JE MEMORY
```

### Change 11 near `DEFINE:`

Unchanged source immediately before this edit:

```asm
JAE TABLEFULL
MOV DI,[SYMNEXT]
PUSH SI
```

Remove this exact source at old physical positions 468–468:

```asm
MOV SI,2300H
```

Replace it with:

```asm
MOV SI,4080H
```

The following old source stays in place:

```asm
CALL COPYZ
POP SI
```

### Change 12 near `DEFINE:`

Unchanged source immediately before this edit:

```asm
CMP BX,0
JNE DEFINEBAD
MOV AX,[SYMC]
```

Remove this exact source at old physical positions 464–464:

```asm
CMP AX,256
```

Replace it with:

```asm
CMP AX,2048
```

The following old source stays in place:

```asm
JAE TABLEFULL
MOV DI,[SYMNEXT]
```

### Change 13 near `DEFINE:`

Unchanged source immediately before this edit:

```asm
CALL REGISTER
CMP AX,0FFFFH
JNE DEFINEBAD
```

Remove this exact source at old physical positions 454–454:

```asm
MOV BX,3000H
```

Replace it with:

```asm
MOV BX,5000H
```

The following old source stays in place:

```asm
MOV CX,[SYMC]
MOV AX,20
```

### Change 14 near `SYMBOLVALUE:`

Unchanged source immediately before this edit:

```asm
CALL REGISTER
CMP AX,0FFFFH
JNE VALUEBAD
```

Remove this exact source at old physical positions 430–430:

```asm
MOV BX,3000H
```

Replace it with:

```asm
MOV BX,5000H
```

The following old source stays in place:

```asm
MOV CX,[SYMC]
MOV AX,20
```

### Change 15 near `LITERAL:`

Unchanged source immediately before this edit:

```asm
PUSH SI
MOV SI,2300H
MOV DI,[TOKLEN]
```

Remove this exact source at old physical positions 364–364:

```asm
ADD DI,2300H
```

Replace it with:

```asm
ADD DI,4080H
```

The following old source stays in place:

```asm
MOV BX,DI
DEC BX
```

### Change 16 near `LITERAL:`

Unchanged source immediately before this edit:

```asm
JMP SYMBOLVALUE
LITERAL:
PUSH SI
```

Remove this exact source at old physical positions 362–362:

```asm
MOV SI,2300H
```

Replace it with:

```asm
MOV SI,4080H
```

The following old source stays in place:

```asm
MOV DI,[TOKLEN]
ADD DI,2300H
```

### Change 17 near `VALUE:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

VALUE:
```

Remove this exact source at old physical positions 353–353:

```asm
MOV AL,[2300H]
```

Replace it with:

```asm
MOV AL,[4080H]
```

The following old source stays in place:

```asm
CMP AL,48
JB WORDVALUE
```

### Change 18 near `VALIDNAME:`

Unchanged source immediately before this edit:

```asm

VALIDNAME:
PUSH SI
```

Remove this exact source at old physical positions 322–322:

```asm
MOV SI,2300H
```

Replace it with:

```asm
MOV SI,4080H
```

The following old source stays in place:

```asm
LODSB
CMP AL,95
```

### Change 19 near `LOOKNEXT:`

Unchanged source immediately before this edit:

```asm
CMP CX,0
JE LOOKMISS
MOV DI,BP
```

Remove this exact source at old physical positions 280–280:

```asm
MOV SI,2300H
```

Replace it with:

```asm
MOV SI,4080H
```

The following old source stays in place:

```asm
LOOKCHAR:
LODSB
```

### Change 20 near `SCANDONE:`

Unchanged source immediately before this edit:

```asm
DEC SI
SCANDONE:
MOV AX,DI
```

Remove this exact source at old physical positions 260–260:

```asm
SUB AX,2300H
```

Replace it with:

```asm
SUB AX,4080H
```

The following old source stays in place:

```asm
MOV [TOKLEN],AX
MOV AL,0
```

### Change 21 near `SCANMORE:`

Unchanged source immediately before this edit:

```asm
JE SCANBACK
CMP AL,93
JE SCANBACK
```

Remove this exact source at old physical positions 252–252:

```asm
CMP DI,2310H
```

Replace it with:

```asm
CMP DI,4090H
```

The following old source stays in place:

```asm
JAE TOKENBAD
STOSB
```

### Change 22 near `SCAN:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

SCAN:
```

Remove this exact source at old physical positions 218–218:

```asm
MOV DI,2300H
```

Replace it with:

```asm
MOV DI,4080H
```

The following old source stays in place:

```asm
SCANSPACE:
LODSB
```

### Change 23 near `READLINE:`

Unchanged source immediately before this edit:

```asm
RET

READLINE:
```

Remove this exact source at old physical positions 131–131:

```asm
MOV DI,2200H
```

Replace it with:

```asm
MOV DI,4000H
```

The following old source stays in place:

```asm
MOV BP,0
MOV AL,[ENDED]
```

### Change 24 near `BUFFERBYTE:`

Unchanged source immediately before this edit:

```asm
JE BUFFEREND
BUFFERBYTE:
MOV BX,[RDPOS]
```

Remove this exact source at old physical positions 118–118:

```asm
ADD BX,5000H
```

Replace it with:

```asm
ADD BX,4200H
```

The following old source stays in place:

```asm
MOV AL,[BX]
MOV [CHAR],AL
```

### Change 25 near `NEXTBYTE:`

Unchanged source immediately before this edit:

```asm
CMP AX,DX
JB BUFFERBYTE
MOV BX,[HANDLE]
```

Remove this exact source at old physical positions 104–104:

```asm
MOV DX,5000H
```

Replace it with:

```asm
MOV DX,4200H
```

The following old source stays in place:

```asm
MOV CX,1024
MOV AH,3FH
```

### Change 26 near `NEXTLINE:`

Unchanged source immediately before this edit:

```asm
CALL READLINE
CMP AX,0
JE PASSEND
```

Remove this exact source at old physical positions 36–36:

```asm
MOV SI,2200H
```

Replace it with:

```asm
MOV SI,4000H
```

The following old source stays in place:

```asm
CALL STATEMENT
JMP NEXTLINE
```

### Change 27 near `ROOM:`

Unchanged source immediately before this edit:

```asm
MOV [PASS],AL
MOV AX,0
MOV [SYMC],AX
```

Remove this exact source at old physical positions 14–14:

```asm
MOV AX,3000H
```

Replace it with:

```asm
MOV AX,5000H
```

The following old source stays in place:

```asm
MOV [SYMNEXT],AX
PASSSTART:
```

## Build the stopping point

Run `CHECK ASMKEEP`, enter `A09` at `Source name:`, and require `OK 03068 bytes` and PASS. This uses the preceding published ASM86, not the new checkpoint. It creates A09.COM.

VIEW.BAS must report A09.COM length 3068 bytes. Keep that executable and source together.

## Acceptance check

Create T09.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T09.ASM SOURCE.ASM
```

```dos
CHECK A09
```

Require:

```text
OK RESULT.COM 00011 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **11 bytes** and these complete contents:

```text
B2 41 B4 02 CD 21 B8 00 4C CD 21
```

This fixture is a complete program. Save it before another assembly and execute it:

```dos
COPY RESULT.COM TRY.COM
CHECK TRY
```

It displays "A" and the checker reports PASS.

## A rejection check

Create X09.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X09.ASM SOURCE.ASM
CHECK A09
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

## Fill the symbol table

Enter SYMS.BAS as a source-text exercise:

```basic
10 N=2048
20 OPEN "SOURCE.ASM" FOR OUTPUT AS #1
30 FOR I=0 TO N-1
40 PRINT #1,"S"+MID$(STR$(I),2)+":"
50 NEXT I
60 PRINT #1,"DW S0,S"+MID$(STR$(N-1),2)
70 CLOSE #1
80 PRINT "SOURCE.ASM READY"
```

Run GWBASIC SYMS.BAS, require SOURCE.ASM READY, and use SYSTEM to return to DOS. BASIC closes the text file with its normal source Control-Z marker. Run CHECK A09. Require `OK RESULT.COM 00004 bytes` and PASS. VIEW.BAS must show `00 01 00 01`: all definitions have value 0100H because none emits bytes. This file is data, not an executable.

Keep a copy of that result. Change BASIC line 10 to `10 N=2049` and RUN again. CHECK A09 must report `ERROR 02049 CODE 5` and FAIL, preserving the four-byte result. Restore the stated accepted N before another run. The BASIC program creates assembly source, never executable bytes.

An unexpected PASS fails this rejection test.

## If the result differs

Check the fixed name bytes, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
