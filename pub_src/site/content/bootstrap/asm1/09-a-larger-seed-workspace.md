+++
title = "15 \u00b7 A larger seed workspace"
weight = 15
description = "Separate the resident image, I/O blocks, symbols, and stack."
download = "A09.ASM"
aliases = ["/bootstrap/asm86a/09-a-larger-seed-workspace/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/09-a-larger-seed-workspace/"
+++

With the whole-image output buffer gone, I can give more room to names. I redraw the memory sketch before moving anything, marking the line, token, two file blocks, symbol records and stack. Each needs its own part of the segment.

**Starting source:** `A08.ASM`. **Save as:** `A09.ASM`. **Build with:** `ASMKEEP.COM`.

## The working parts

The seed moves its line to 4000H, token to 4080H, input block to 4200H, output block to 4600H, and symbol table to 5000H. The 2048 twenty-byte records end at EFFFH. The upper 4 KB remain reserved for the stack.

DEFINE bounds the record count before copying a name. The code/static-data area is reserved below 4000H even though the initial image must still fit ASM0's smaller build limit. Emitted programs are written to disk and do not occupy this workspace.

## Enter the source

Copy `A08.ASM` to `A09.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `FLUSH:`

Find the unique label `FLUSH:`, then follow this unchanged source through its last displayed instruction:

```asm
FLUSH:
PUSH AX
PUSH BX
PUSH CX
PUSH DX
MOV CX,[OUTCNT]
CMP CX,0
JE FLUSHDONE
MOV BX,[OUTHANDLE]
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV DX,6000H
```

With:

```asm
MOV DX,4600H
```

### Change 2 · `EMITROOM:`

Find the unique label `EMITROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
EMITROOM:
MOV AH,[PASS]
CMP AH,2
JNE COUNTBYTE
MOV BX,[OUTCNT]
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
ADD BX,6000H
```

With:

```asm
ADD BX,4600H
```

### Change 3 · `TWOOPERANDS:`

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
MOV AX,[VAL]
MOV [V1],AX
CALL SCAN
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AL,[2300H]
```

With:

```asm
MOV AL,[4080H]
```

### Change 4 · `FINISH:`

Find the unique label `FINISH:`, then follow this unchanged source through its last displayed instruction:

```asm
FINISH:
CALL SCAN
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AL,[2300H]
```

With:

```asm
MOV AL,[4080H]
```

### Change 5 · `DATASEP:`

Find the unique label `DATASEP:`, then follow this unchanged source through its last displayed instruction:

```asm
DATASEP:
CALL SCAN
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AL,[2300H]
```

With:

```asm
MOV AL,[4080H]
```

### Change 6 · `STATEMENT:`

Find the unique label `STATEMENT:`, then follow this unchanged source through its last displayed instruction:

```asm
STATEMENT:
CALL SCAN
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AL,[2300H]
```

With:

```asm
MOV AL,[4080H]
```

### Change 7 · `MEMORYEND:`

Find the unique label `MEMORYEND:`, then follow this unchanged source through its last displayed instruction:

```asm
MEMORYEND:
CALL SCAN
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AL,[2300H]
```

With:

```asm
MOV AL,[4080H]
```

### Change 8 · `MEMORY:`

Find the unique label `MEMORY:`, then follow this unchanged source through its last displayed instruction:

```asm
MEMORY:
CALL SCAN
MOV AX,[2300H]
CMP AX,5842H
JNE DIRECTMEM
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AL,[2302H]
```

With:

```asm
MOV AL,[4082H]
```

### Change 9 · `MEMORY:`

Find the unique label `MEMORY:`, then follow this unchanged source through its last displayed instruction:

```asm
MEMORY:
CALL SCAN
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AX,[2300H]
```

With:

```asm
MOV AX,[4080H]
```

### Change 10 · `OPERAND:`

Find the unique label `OPERAND:`, then follow this unchanged source through its last displayed instruction:

```asm
OPERAND:
CALL SCAN
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AL,[2300H]
```

With:

```asm
MOV AL,[4080H]
```

### Change 11 · `VALUEBAD:`

Find the unique label `VALUEBAD:`, then follow this unchanged source through its last displayed instruction:

```asm
VALUEBAD:
MOV AX,3
JMP ERROR
DEFINE:
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
JNE DEFINEBAD
MOV BX,3000H
MOV CX,[SYMC]
MOV AX,20
CALL LOOK
MOV AL,[PASS]
CMP AL,1
JNE CHECKDEFINE
CMP BX,0
JNE DEFINEBAD
MOV AX,[SYMC]
CMP AX,256
JAE TABLEFULL
MOV DI,[SYMNEXT]
PUSH SI
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV SI,2300H
```

With:

```asm
MOV SI,4080H
```

### Change 12 · `VALUEBAD:`

Find the unique label `VALUEBAD:`, then follow this unchanged source through its last displayed instruction:

```asm
VALUEBAD:
MOV AX,3
JMP ERROR
DEFINE:
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
JNE DEFINEBAD
MOV BX,3000H
MOV CX,[SYMC]
MOV AX,20
CALL LOOK
MOV AL,[PASS]
CMP AL,1
JNE CHECKDEFINE
CMP BX,0
JNE DEFINEBAD
MOV AX,[SYMC]
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
CMP AX,256
```

With:

```asm
CMP AX,2048
```

### Change 13 · `VALUEBAD:`

Find the unique label `VALUEBAD:`, then follow this unchanged source through its last displayed instruction:

```asm
VALUEBAD:
MOV AX,3
JMP ERROR
DEFINE:
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
JNE DEFINEBAD
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV BX,3000H
```

With:

```asm
MOV BX,5000H
```

### Change 14 · `SYMBOLVALUE:`

Find the unique label `SYMBOLVALUE:`, then follow this unchanged source through its last displayed instruction:

```asm
SYMBOLVALUE:
CALL VALIDNAME
CALL REGISTER
CMP AX,0FFFFH
JNE VALUEBAD
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV BX,3000H
```

With:

```asm
MOV BX,5000H
```

### Change 15 · `LITERAL:`

Find the unique label `LITERAL:`, then follow this unchanged source through its last displayed instruction:

```asm
LITERAL:
PUSH SI
MOV SI,2300H
MOV DI,[TOKLEN]
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
ADD DI,2300H
```

With:

```asm
ADD DI,4080H
```

### Change 16 · `LITERAL:`

Find the unique label `LITERAL:`, then follow this unchanged source through its last displayed instruction:

```asm
LITERAL:
PUSH SI
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV SI,2300H
```

With:

```asm
MOV SI,4080H
```

### Change 17 · `SYMBOLBAD:`

Find the unique label `SYMBOLBAD:`, then follow this unchanged source through its last displayed instruction:

```asm
SYMBOLBAD:
MOV AX,3
JMP ERROR
VALUE:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AL,[2300H]
```

With:

```asm
MOV AL,[4080H]
```

### Change 18 · `VALIDNAME:`

Find the unique label `VALIDNAME:`, then follow this unchanged source through its last displayed instruction:

```asm
VALIDNAME:
PUSH SI
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV SI,2300H
```

With:

```asm
MOV SI,4080H
```

### Change 19 · `LOOKNEXT:`

Find the unique label `LOOKNEXT:`, then follow this unchanged source through its last displayed instruction:

```asm
LOOKNEXT:
CMP CX,0
JE LOOKMISS
MOV DI,BP
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV SI,2300H
```

With:

```asm
MOV SI,4080H
```

Keep the following `LOOKCHAR:` label and the source after it in place.

### Change 20 · `SCANDONE:`

Find the unique label `SCANDONE:`, then follow this unchanged source through its last displayed instruction:

```asm
SCANDONE:
MOV AX,DI
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
SUB AX,2300H
```

With:

```asm
SUB AX,4080H
```

### Change 21 · `SCANMORE:`

Find the unique label `SCANMORE:`, then follow this unchanged source through its last displayed instruction:

```asm
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
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
CMP DI,2310H
```

With:

```asm
CMP DI,4090H
```

### Change 22 · `SCAN:`

Find the unique label `SCAN:`, then follow this unchanged source through its last displayed instruction:

```asm
SCAN:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV DI,2300H
```

With:

```asm
MOV DI,4080H
```

Keep the following `SCANSPACE:` label and the source after it in place.

### Change 23 · `READLINE:`

Find the unique label `READLINE:`, then follow this unchanged source through its last displayed instruction:

```asm
READLINE:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV DI,2200H
```

With:

```asm
MOV DI,4000H
```

### Change 24 · `BUFFERBYTE:`

Find the unique label `BUFFERBYTE:`, then follow this unchanged source through its last displayed instruction:

```asm
BUFFERBYTE:
MOV BX,[RDPOS]
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
ADD BX,5000H
```

With:

```asm
ADD BX,4200H
```

### Change 25 · `NEXTBYTE:`

Find the unique label `NEXTBYTE:`, then follow this unchanged source through its last displayed instruction:

```asm
NEXTBYTE:
MOV AX,[RDPOS]
MOV DX,[RDLEN]
CMP AX,DX
JB BUFFERBYTE
MOV BX,[HANDLE]
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV DX,5000H
```

With:

```asm
MOV DX,4200H
```

### Change 26 · `NEXTLINE:`

Find the unique label `NEXTLINE:`, then follow this unchanged source through its last displayed instruction:

```asm
NEXTLINE:
CALL READLINE
CMP AX,0
JE PASSEND
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV SI,2200H
```

With:

```asm
MOV SI,4000H
```

### Change 27 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
CALL CMDFILES
CALL PREFLIGHT
MOV AL,1
MOV [PASS],AL
MOV AX,0
MOV [SYMC],AX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AX,3000H
```

With:

```asm
MOV AX,5000H
```

## Build the stopping point

Copy `A09.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03466 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A09.COM`.

Keep that executable and source together.

## Acceptance check

Reuse the earlier input unchanged:

```dos
COPY T02.ASM T09.ASM
```

```dos
CHECK A09 T09.ASM RESULT.COM
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

The byte inspection checks the accepted result. Keep it as data.

## A rejection check

Create X09.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
CHECK A09 X09.ASM RESULT.COM
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with C:\DOS\FC.EXE /B if in doubt. Require a fresh OK before using any output.

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

Run GWBASIC SYMS.BAS, require SOURCE.ASM READY, and use SYSTEM to return to DOS. BASIC closes the text file with its normal source Control-Z marker. Run CHECK A09 SOURCE.ASM RESULT.COM. Require `OK RESULT.COM 00004 bytes` and PASS. VIEW.BAS must show `00 01 00 01`: all definitions have value 0100H because none emits bytes. This file is data, not an executable.

Keep a copy of that result. Change BASIC line 10 to `10 N=2049` and RUN again. CHECK A09 SOURCE.ASM RESULT.COM must report `ERROR 02049 CODE 5` and FAIL, preserving the four-byte result. Restore the stated accepted N before another run. The BASIC program creates assembly source, never executable bytes.

An unexpected PASS fails this rejection test.

## If the result differs

Check every relocated line, token and block-buffer address, along with the twenty-byte symbol stride. The 2048th record ends at EFFFH; the next definition must fail before touching the stack reservation.
