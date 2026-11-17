+++
title = "16 \u00b7 Encoding segment-register moves"
weight = 16
description = "Teach an instruction form before using it in a successor."
download = "A10.ASM"
aliases = ["/bootstrap/asm86a/10-encoding-segment-register-moves/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/10-encoding-segment-register-moves/"
+++

My memory sketch still fits inside one segment. Reading the segment-register MOV forms in the processor manual shows me how another program could select storage elsewhere. I'll teach ASM1 to encode those forms using instructions ASM0 already accepts.

## The working parts

REGISTER adds ES, CS, SS, and DS after the sixteen ordinary registers. OPERAND marks them as a distinct kind. SEGMOV emits 8CH for a segment source or 8EH for a segment destination, with the segment field and ordinary word-register field in ModR/M. CS is never accepted as a destination.

The seed implementation still uses only instructions accepted by ASM0. It encodes these forms as output for another program; it does not yet execute them. Register widths and mixed segment/ordinary forms are checked explicitly.

## Enter the source

Copy `A09.ASM` to `A10.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `CMDCOUNT:`

Find the unique label `CMDCOUNT:`. Insert the new source immediately before this existing label:

```asm
CMDCOUNT:
```

Insert:

```asm
PREFIX:
DB 0
P1:
DB 0
```

### Change 2 · `INOPEN:`

Find the unique label `INOPEN:`. Insert the new source immediately before this existing label:

```asm
INOPEN:
```

Insert:

```asm
SEGCODE:
DW 0
```

### Change 3 · `OPTAB:`

Find the unique label `OPTAB:`. Insert the new source immediately before this existing label:

```asm
OPTAB:
```

Insert:

```asm
DB 69,83,0,16
DB 67,83,0,17
DB 83,83,0,18
DB 68,83,0,19
```

### Change 4 · `CMDINIT:`

Find the unique label `CMDINIT:`. Insert the new source immediately before this existing label:

```asm
CMDINIT:
```

Insert:

```asm
SEGOPERAND:
MOV [SEGCODE],AX
PUSH SI
CALL SCAN
MOV AL,[4080H]
CMP AL,58
JNE SEGREGISTER
POP AX
JMP TWOBAD
SEGREGISTER:
POP SI
MOV AX,[SEGCODE]
SUB AX,16
MOV [REG],AL
MOV AL,1
MOV [WIDTH],AL
MOV AL,4
MOV [KIND],AL
RET
SEGMOV:
MOV AL,[K1]
CMP AL,4
JNE SEGLOAD
MOV AL,[R1]
CMP AL,1
JE SEGBAD
MOV AL,[KIND]
CMP AL,1
JNE SEGBAD
MOV AL,[WIDTH]
CMP AL,1
JNE SEGBAD
MOV AL,142
CALL EMIT
MOV AL,[R1]
CALL TIMES8
MOV DL,[REG]
JMP SEGMOD
SEGLOAD:
MOV AL,[K1]
CMP AL,1
JNE SEGBAD
MOV AL,[W1]
CMP AL,1
JNE SEGBAD
MOV AL,140
CALL EMIT
MOV AL,[REG]
CALL TIMES8
MOV DL,[R1]
SEGMOD:
ADD AL,DL
ADD AL,192
CALL EMIT
RET
SEGBAD:
JMP TWOBAD
```

### Change 5 · `STOREOK:`

Find the unique label `STOREOK:`, then follow this unchanged source through its last displayed instruction:

```asm
STOREOK:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AL,[P1]
CMP AL,0
JE STOREPREFIX
CALL EMIT
STOREPREFIX:
```

### Change 6 · `LOADMEM:`

Find the unique label `LOADMEM:`, then follow this unchanged source through its last displayed instruction:

```asm
LOADMEM:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AL,[PREFIX]
CMP AL,0
JE LOADPREFIX
CALL EMIT
LOADPREFIX:
```

### Change 7 · `MOVOPERANDS:`

Find the unique label `MOVOPERANDS:`, then follow this unchanged source through its last displayed instruction:

```asm
MOVOPERANDS:
MOV AL,[K1]
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CMP AL,4
JNE MOVNOTSEG
JMP SEGMOV
MOVNOTSEG:
MOV AL,[KIND]
CMP AL,4
JNE MOVNOTSRC
JMP SEGMOV
MOVNOTSRC:
MOV AL,[K1]
```

### Change 8 · `TWOOPERANDS:`

Find the unique label `TWOOPERANDS:`, then follow this unchanged source through its last displayed instruction:

```asm
TWOOPERANDS:
CALL OPERAND
MOV AL,[KIND]
MOV [K1],AL
MOV AL,[WIDTH]
MOV [W1],AL
MOV AL,[REG]
MOV [R1],AL
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AL,[PREFIX]
MOV [P1],AL
```

### Change 9 · `DEFINEBAD:`

Find the unique label `DEFINEBAD:`, then follow this unchanged source through its last displayed instruction:

```asm
DEFINEBAD:
MOV AX,3
JMP ERROR
OPERAND:
CALL SCAN
MOV AL,[4080H]
CMP AL,91
JE MEMORY
CALL REGISTER
CMP AX,0FFFFH
JE IMMEDIATE
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CMP AX,16
JB NORMALREGISTER
JMP SEGOPERAND
NORMALREGISTER:
```

### Change 10 · `DEFINEBAD:`

Find the unique label `DEFINEBAD:`, then follow this unchanged source through its last displayed instruction:

```asm
DEFINEBAD:
MOV AX,3
JMP ERROR
OPERAND:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AL,0
MOV [PREFIX],AL
```

### Change 11 · `LOOKMISS:`

Find the unique label `LOOKMISS:`, then follow this unchanged source through its last displayed instruction:

```asm
LOOKMISS:
MOV BX,0
POP SI
RET
REGISTER:
MOV BX,REGTAB
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV CX,16
```

With:

```asm
MOV CX,20
```

## Build the stopping point

Copy `A10.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03705 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A10.COM`.

VIEW.BAS must report A10.COM length 3705 bytes. Keep that executable and source together.

## Acceptance check

Create T10.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
CHECK A10 T10.ASM RESULT.COM
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

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

Create X10.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
CHECK A10 X10.ASM RESULT.COM
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with C:\DOS\FC.EXE /B if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check the saved argument names and terminators, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
