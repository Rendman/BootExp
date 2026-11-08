+++
title = "03 \u00b7 Copying a File in Small Blocks"
weight = 3
description = "Copy a stream through a bounded output block and inspect the result."
download = "A03.ASM"
aliases = ["/bootstrap/asm86a/03-writing-an-output-block/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/03-writing-an-output-block/"
+++

The emitter needs a working file writer before it can replace the assembler image buffer.

## The working parts

This checkpoint is a byte-copy diagnostic. The parser remains in the source but the driver does not call it. CREATEOUT opens ASMA.TMP, EMIT stores one byte into the 1024-byte output block, and FLUSH writes a full or final partial block. PC counts bytes from the chosen 0100H origin and refuses an image beyond EFFFH.

FLUSH preserves AX, BX, CX, and DX. It checks DOS carry and the actual written count; zero buffered bytes cause no DOS write. CLOSEOUT checks the final close. This diagnostic may overwrite ASMA.TMP and leaves that file after success. Its contents are data, not a program to execute.

## Enter the source

Copy `A02.ASM` to `A03.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `INOPEN:`

Unchanged source immediately before this edit:

```asm
INOPEN:
DB 0
```

Remove this exact source at old physical positions 1127–1128:

```asm
OUTPTR:
DW 24576
```

Replace it with:

```asm
OUTOPEN:
DB 0

OWNTMP:
DB 0
```

### Change 2 near `RDLEN:`

Unchanged source immediately before this edit:

```asm
RDLEN:
DW 0
```

Insert after old physical line 1123.

Insert:

```asm
OUTCNT:
DW 0

OUTHANDLE:
DW 0
```

The following old source stays in place:

```asm
INOPEN:
DB 0
```

### Change 3 near `SRCNAME:`

Unchanged source immediately before this edit:

```asm
SRCNAME:
DB 83,79,85,82,67,69,46,65,83,77,0
```

Remove this exact source at old physical positions 1115–1116:

```asm
RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0
```

Replace it with:

```asm
TMPNAME:
DB 65,83,77,65,46,84,77,80,0
```

The following old source stays in place:

```asm

RDPOS:
```

### Change 4 near `OKMSG:`

Unchanged source immediately before this edit:

```asm
INT 21H

OKMSG:
```

Remove this exact source at old physical positions 981–981:

```asm
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

Replace it with:

```asm
DB 79,75,32,65,83,77,65,46,84,77,80,32,36
```

The following old source stays in place:

```asm

BYTEMSG:
```

### Change 5 near `ERROR:`

Unchanged source immediately before this edit:

```asm
MOV AX,4C01H
INT 21H
```

Insert after old physical line 979.

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

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

### Change 6 near `COUNTBYTE:`

Unchanged source immediately before this edit:

```asm
POP BX
POP AX
RET
```

Remove this exact source at old physical positions 914–916:

```asm
IMAGEFULL:
MOV AX,5
JMP ERROR
```

There is no replacement source.

The following old source stays in place:

```asm

COPYZ:
```

### Change 7 near `COUNTBYTE:`

Unchanged source immediately before this edit:

```asm
MOV BX,[PC]
INC BX
MOV [PC],BX
```

Remove this exact source at old physical positions 908–910:

```asm
MOV BX,[OUTPTR]
INC BX
MOV [OUTPTR],BX
```

There is no replacement source.

The following old source stays in place:

```asm
POP BX
POP AX
```

### Change 8 near `EMIT:`

Unchanged source immediately before this edit:

```asm
JNE COUNTBYTE
MOV BX,[OUTPTR]
MOV [BX],AL
```

Insert after old physical line 903.

Insert:

```asm
MOV BX,[OUTCNT]
INC BX
MOV [OUTCNT],BX
CMP BX,1024
JB COUNTBYTE
CALL FLUSH
```

The following old source stays in place:

```asm
COUNTBYTE:
MOV BX,[PC]
```

### Change 9 near `EMIT:`

Unchanged source immediately before this edit:

```asm
MOV AH,[PASS]
CMP AH,2
JNE COUNTBYTE
```

Remove this exact source at old physical positions 902–902:

```asm
MOV BX,[OUTPTR]
```

Replace it with:

```asm
MOV BX,[OUTCNT]
ADD BX,6000H
```

The following old source stays in place:

```asm
MOV [BX],AL
COUNTBYTE:
```

### Change 10 near `EMIT:`

Unchanged source immediately before this edit:

```asm
PUSH AX
PUSH BX
MOV BX,[PC]
```

Remove this exact source at old physical positions 897–898:

```asm
CMP BX,2100H
JAE IMAGEFULL
```

Replace it with:

```asm
CMP BX,0F000H
JB EMITROOM
MOV AX,5
JMP ERROR
EMITROOM:
```

The following old source stays in place:

```asm
MOV AH,[PASS]
CMP AH,2
```

### Change 11 near `INPUTCLOSED:`

Unchanged source immediately before this edit:

```asm
INPUTCLOSED:
MOV AL,0
MOV [INOPEN],AL
```

Remove this exact source at old physical positions 71–107:

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
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

There is no replacement source.

The following old source stays in place:

```asm
RET
```

### Change 12 near `PASSEND:`

Unchanged source immediately before this edit:

```asm
JMP NEXTLINE
PASSEND:
CALL CLOSEFILE
```

Remove this exact source at old physical positions 36–42:

```asm
MOV AL,[PASS]
ADD AL,1
MOV [PASS],AL
CMP AL,3
JB PASSSTART
CALL WRITEOUT
GOOD:
```

Replace it with:

```asm
CALL FLUSH
CALL CLOSEOUT
MOV DX,OKMSG
CALL TEXT
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

The following old source stays in place:

```asm
MOV AX,4C00H
INT 21H
```

### Change 13 near `NEXTLINE:`

Unchanged source immediately before this edit:

```asm
NEXTLINE:
CALL READLINE
CMP AX,0
```

Remove this exact source at old physical positions 30–34:

```asm
JE PASSEND
MOV SI,2200H
CALL STATEMENT
JMP NEXTLINE
PASSEND:
```

Replace it with:

```asm
JE COPYDONE
MOV AL,[CHAR]
CALL EMIT
JMP COPYBYTE
COPYDONE:
```

The following old source stays in place:

```asm
CALL CLOSEFILE
MOV AL,[PASS]
```

### Change 14 near `PASSSTART:`

Unchanged source immediately before this edit:

```asm
MOV [ENDED],AL
MOV [SKIPLF],AL
CALL OPENFILE
```

Remove this exact source at old physical positions 27–28:

```asm
NEXTLINE:
CALL READLINE
```

Replace it with:

```asm
COPYBYTE:
CALL NEXTBYTE
```

The following old source stays in place:

```asm
CMP AX,0
JE PASSEND
```

### Change 15 near `PASSSTART:`

Unchanged source immediately before this edit:

```asm
PASSSTART:
MOV AX,100H
MOV [PC],AX
```

Remove this exact source at old physical positions 18–25:

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

Replace it with:

```asm
MOV AL,2
MOV [PASS],AL
CALL CREATEOUT
```

The following old source stays in place:

```asm
CALL OPENFILE
NEXTLINE:
```

### Change 16 near `ROOM:`

Unchanged source immediately before this edit:

```asm
MOV AL,1
MOV [PASS],AL
MOV AX,0
```

Remove this exact source at old physical positions 12–15:

```asm
MOV [SYMC],AX
MOV AX,3000H
MOV [SYMNEXT],AX
PASSSTART:
```

Replace it with:

```asm
MOV [RDPOS],AX
MOV [RDLEN],AX
MOV [OUTCNT],AX
MOV [LINENO],AX
```

The following old source stays in place:

```asm
MOV AX,100H
MOV [PC],AX
```

### Change 17 near `ROOM:`

Unchanged source immediately before this edit:

```asm
MOV AX,7
JMP ERROR
ROOM:
```

Remove this exact source at old physical positions 9–10:

```asm
MOV AL,1
MOV [PASS],AL
```

There is no replacement source.

The following old source stays in place:

```asm
MOV AX,0
MOV [SYMC],AX
```

## Build the stopping point

Copy `A03.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 02565 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A03.COM`.

VIEW.BAS must report A03.COM length 2565 bytes. Keep that executable and source together.

## Acceptance check

Create T03.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```text
ABC
```

```dos
COPY T03.ASM SOURCE.ASM
```

```dos
CHECK A03
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

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

After inspecting the successful copy, delete ASMA.TMP. It belongs to this copy exercise.

```dos
REN SOURCE.ASM HOLD.ASM
CHECK A03
```

Choose an unused HOLD.ASM name before renaming. Restore HOLD.ASM to SOURCE.ASM afterward.

Require:

```text
ERROR 00000 CODE 6
FAIL
```

This early writer creates an empty ASMA.TMP before discovering the missing source. Inspect it and delete it before another run. RESULT.COM must be unchanged.

An unexpected PASS fails this rejection test.

## If the result differs

Check the fixed name bytes, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
