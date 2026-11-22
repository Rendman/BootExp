+++
title = "09 \u00b7 Copying a File in Small Blocks"
weight = 9
description = "Copy a stream through a bounded output block and inspect the result."
download = "A03.ASM"
aliases = ["/bootstrap/asm86a/03-writing-an-output-block/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/03-writing-an-output-block/"
+++

The output buffer still has to hold every byte of the assembled program. I want to write a block when it fills and reuse that space. I'll first try the writer by copying a few characters from one file to another, with the parser left out of the path.

**Starting source:** `A02.ASM`. **Save as:** `A03.ASM`. **Build with:** `ASMKEEP.COM`.

## The working parts

This checkpoint is a byte-copy diagnostic. The parser remains in the source but the driver does not call it. CREATEOUT opens ASMA.TMP, EMIT stores one byte into the 1024-byte output block, and FLUSH writes a full or final partial block. PC begins at the chosen 0100H origin. The last permitted loaded byte is at EFFFH, allowing at most 61,184 emitted bytes.

FLUSH preserves AX, BX, CX, and DX. It checks DOS carry and the actual written count; zero buffered bytes cause no DOS write. CLOSEOUT checks the final close. This diagnostic may overwrite ASMA.TMP and leaves that file after success. Its contents are data, not a program to execute.

## Enter the source

Copy `A02.ASM` to `A03.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OUTPTR:`

Find the unique label `OUTPTR:`. The old block below starts at that label.

Replace this existing source:

```asm
OUTPTR:
DW 24576
```

With:

```asm
OUTOPEN:
DB 0
OWNTMP:
DB 0
```

Keep the following `CMDCOUNT:` label and the source after it in place.

### Change 2 · `INOPEN:`

Find the unique label `INOPEN:`. Insert the new source immediately before this existing label:

```asm
INOPEN:
```

Insert:

```asm
OUTCNT:
DW 0
OUTHANDLE:
DW 0
```

### Change 3 · `CMDINIT:`

Find the unique label `CMDINIT:`. Insert the new source immediately before this existing label:

```asm
CMDINIT:
```

Insert:

```asm
CREATEOUT:
MOV DX,TMPNAME
MOV CX,0
MOV AH,3CH
INT 21H
JAE OUTPUTOPEN
JMP FILEBAD
OUTPUTOPEN:
MOV [OUTHANDLE],AX
MOV AL,1
MOV [OUTOPEN],AL
MOV [OWNTMP],AL
RET
CLOSEOUT:
MOV BX,[OUTHANDLE]
MOV AH,3EH
INT 21H
JAE OUTPUTCLOSED
JMP FILEBAD
OUTPUTCLOSED:
MOV AL,0
MOV [OUTOPEN],AL
RET
FLUSH:
PUSH AX
PUSH BX
PUSH CX
PUSH DX
MOV CX,[OUTCNT]
CMP CX,0
JE FLUSHDONE
MOV BX,[OUTHANDLE]
MOV DX,6000H
MOV AH,40H
INT 21H
JAE FLUSHCOUNT
JMP FILEBAD
FLUSHCOUNT:
CMP AX,CX
JE FLUSHGOOD
JMP FILEBAD
FLUSHGOOD:
MOV AX,0
MOV [OUTCNT],AX
FLUSHDONE:
POP DX
POP CX
POP BX
POP AX
RET
```

### Change 4 · `IMAGEFULL:`

Find the unique label `IMAGEFULL:`. The old block below starts at that label.

Remove this existing source:

```asm
IMAGEFULL:
MOV AX,5
JMP ERROR
```

Keep the following `COPYZ:` label and the source after it in place.

### Change 5 · `COUNTBYTE:`

Find the unique label `COUNTBYTE:`, then follow this unchanged source through its last displayed instruction:

```asm
COUNTBYTE:
MOV BX,[PC]
INC BX
MOV [PC],BX
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
MOV BX,[OUTPTR]
INC BX
MOV [OUTPTR],BX
```

### Change 6 · `COUNTBYTE:`

Find the unique label `COUNTBYTE:`. Insert the new source immediately before this existing label:

```asm
COUNTBYTE:
```

Insert:

```asm
MOV BX,[OUTCNT]
INC BX
MOV [OUTCNT],BX
CMP BX,1024
JB COUNTBYTE
CALL FLUSH
```

### Change 7 · `EMIT:`

Find the unique label `EMIT:`, then follow this unchanged source through its last displayed instruction:

```asm
EMIT:
PUSH AX
PUSH BX
MOV BX,[PC]
CMP BX,2100H
JAE IMAGEFULL
MOV AH,[PASS]
CMP AH,2
JNE COUNTBYTE
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV BX,[OUTPTR]
```

With:

```asm
MOV BX,[OUTCNT]
ADD BX,6000H
```

### Change 8 · `EMIT:`

Find the unique label `EMIT:`, then follow this unchanged source through its last displayed instruction:

```asm
EMIT:
PUSH AX
PUSH BX
MOV BX,[PC]
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
CMP BX,2100H
JAE IMAGEFULL
```

With:

```asm
CMP BX,0F000H
JB EMITROOM
MOV AX,5
JMP ERROR
EMITROOM:
```

### Change 9 · `INPUTCLOSED:`

Find the unique label `INPUTCLOSED:`, then follow this unchanged source through its last displayed instruction:

```asm
INPUTCLOSED:
MOV AL,0
MOV [INOPEN],AL
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
RET
WRITEOUT:
MOV DX,RESNAME
MOV CX,0
MOV AH,3CH
INT 21H
JAE ZWRITEOUT1
JMP FILEBAD
ZWRITEOUT1:
MOV [HANDLE],AX
MOV BX,AX
MOV CX,[PC]
SUB CX,100H
MOV DX,6000H
MOV AH,40H
INT 21H
JAE ZWRITEOUT2
JMP FILEBAD
ZWRITEOUT2:
CMP AX,CX
JE ZWRITEOUT3
JMP FILEBAD
ZWRITEOUT3:
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
JAE ZWRITEOUT4
JMP FILEBAD
ZWRITEOUT4:
MOV DX,OKMSG
CALL TEXT
MOV SI,RESNAME
CALL CMDTEXT
MOV DL,32
MOV AH,2
INT 21H
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

### Change 10 · `PASSEND:`

Find the unique label `PASSEND:`, then follow this unchanged source through its last displayed instruction:

```asm
PASSEND:
CALL CLOSEFILE
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AL,[PASS]
ADD AL,1
MOV [PASS],AL
CMP AL,3
JB PASSSTART
CALL WRITEOUT
GOOD:
```

With:

```asm
CALL FLUSH
CALL CLOSEOUT
MOV DX,OKMSG
CALL TEXT
MOV SI,TMPNAME
CALL CMDTEXT
MOV DL,32
MOV AH,2
INT 21H
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

### Change 11 · `NEXTLINE:`

Find the unique label `NEXTLINE:`, then follow this unchanged source through its last displayed instruction:

```asm
NEXTLINE:
CALL READLINE
CMP AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE PASSEND
MOV SI,2200H
CALL STATEMENT
JMP NEXTLINE
PASSEND:
```

With:

```asm
JE COPYDONE
MOV AL,[CHAR]
CALL EMIT
JMP COPYBYTE
COPYDONE:
```

### Change 12 · `NEXTLINE:`

Find the unique label `NEXTLINE:`. The old block below starts at that label.

Replace this existing source:

```asm
NEXTLINE:
CALL READLINE
```

With:

```asm
COPYBYTE:
CALL NEXTBYTE
```

### Change 13 · `PASSSTART:`

Find the unique label `PASSSTART:`, then follow this unchanged source through its last displayed instruction:

```asm
PASSSTART:
MOV AX,100H
MOV [PC],AX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV AX,6000H
MOV [OUTPTR],AX
MOV AX,0
MOV [LINENO],AX
MOV [RDPOS],AX
MOV [RDLEN],AX
MOV [ENDED],AL
MOV [SKIPLF],AL
```

With:

```asm
MOV AL,2
MOV [PASS],AL
CALL CREATEOUT
```

### Change 14 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
CALL CMDFILES
MOV AL,1
MOV [PASS],AL
MOV AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV [SYMC],AX
MOV AX,3000H
MOV [SYMNEXT],AX
PASSSTART:
```

With:

```asm
MOV [RDPOS],AX
MOV [RDLEN],AX
MOV [OUTCNT],AX
MOV [LINENO],AX
```

### Change 15 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
CALL CMDFILES
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
MOV AL,1
MOV [PASS],AL
```

## Build the stopping point

Copy `A03.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03027 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A03.COM`.

Keep that executable and source together.

## Acceptance check

Create T03.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```text
ABC
```

```dos
CHECK A03 T03.ASM RESULT.COM
```

Require:

```text
OK ASMA.TMP 00005 bytes
PASS
```

In VIEW.BAS, inspect ASMA.TMP. Require length **5 bytes** and these complete contents:

```text
41 42 43 0D 0A
```

These are the copied text bytes, including their line ending. Inspect the result as data.

The viewer shows `41 42 43 0D 0A`, matching the characters and line ending I put in the source file. I can trace this small copy through the reader, the output block and DOS before involving instruction encoding again.

## Flush full blocks and a final partial block

Use the valid LONG.ASM made with STREAM.BAS: 1024 lines containing DB 65, then DB 66. If it is absent, run GWBASIC STREAM.BAS, require LONG.ASM READY and return with SYSTEM. This driver copies the source bytes without interpreting assembly or treating Control-Z as a source ending.

```dos
CHECK A03 LONG.ASM RESULT.COM
C:\DOS\FC.EXE /B LONG.ASM ASMA.TMP
```

Require `OK ASMA.TMP 07176 bytes` and PASS, followed by FC reporting no differences. VIEW.BAS must show ASMA.TMP length 7176. Seven full output blocks and an eight-byte tail are required; a missing final flush or a repeated block changes the comparison. Keep this result as data. RESULT.COM is still the saved assembler executable from the construction build.

## A rejection check

After inspecting the successful copy, delete ASMA.TMP. It belongs to this copy exercise.

```dos
REN T03.ASM HOLD.ASM
CHECK A03 T03.ASM RESULT.COM
```

Choose an unused HOLD.ASM name before renaming. Restore HOLD.ASM to the selected fixture name afterward.

Require:

```text
ERROR 00000 CODE 6
FAIL
```

This early writer creates an empty ASMA.TMP before discovering the missing source. Inspect it and delete it before another run. RESULT.COM must be unchanged.

An unexpected PASS fails this rejection test.

## If the result differs

Check that a full block is flushed before another byte is stored and that the final partial block is flushed before close. FLUSH must preserve the caller's byte and counters and verify the actual write count.
