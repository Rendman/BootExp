+++
title = "13 \u00b7 Streaming the two assembly passes"
weight = 13
description = "Return to the assembler with no complete image buffer."
download = "A07.ASM"
aliases = ["/bootstrap/asm86a/07-streaming-the-two-assembly-passes/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/07-streaming-the-two-assembly-passes/"
+++

I have checked the writer with copied characters. Now I can put the parser back in the path and send it assembly source again. Pass one will count the instruction bytes; pass two will feed them to the block writer as they are made.

## The working parts

Pass one records definitions and counts instruction bytes without writing. Its final PC is saved in ENDPC. Pass two creates the temporary output, reopens the source, emits incrementally, and must finish at the same PC. FLUSH, CLOSEOUT, and COMMIT run only after successful source close.

PC describes the target; OUTCNT describes the current block. They are independent. Input, parser, or range errors remove this run's temporary file and preserve an older RESULT.COM. The accepted language remains the published ASM0 vocabulary.

## Enter the source

Copy `A06.ASM` to `A07.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `INOPEN:`

Find the unique label `INOPEN:`. Insert the new source immediately before this existing label:

```asm
INOPEN:
```

Insert:

```asm
ENDPC:
DW 0
```

### Change 2 · `COPYDONE:`

Find the unique label `COPYDONE:`, then follow this unchanged source through its last displayed instruction:

```asm
COPYDONE:
CALL CLOSEFILE
CALL FLUSH
CALL CLOSEOUT
CALL COMMIT
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

The edit begins immediately after that unchanged block.

Insert:

```asm
GOOD:
```

### Change 3 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
CALL CMDFILES
CALL PREFLIGHT
MOV AX,0
MOV [RDPOS],AX
MOV [RDLEN],AX
MOV [OUTCNT],AX
MOV [LINENO],AX
MOV AX,100H
MOV [PC],AX
MOV AL,2
MOV [PASS],AL
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
CALL CREATEOUT
CALL OPENFILE
COPYBYTE:
CALL NEXTBYTE
CMP AX,0
JE COPYDONE
MOV AL,[CHAR]
CALL EMIT
JMP COPYBYTE
COPYDONE:
CALL CLOSEFILE
```

With:

```asm
JMP PASSSTART
PASSCHECK:
MOV AX,[PC]
MOV DX,[ENDPC]
CMP AX,DX
JE PASSVALID
MOV AX,3
JMP ERROR
PASSVALID:
```

### Change 4 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
CALL CMDFILES
CALL PREFLIGHT
MOV AX,0
MOV [RDPOS],AX
MOV [RDLEN],AX
MOV [OUTCNT],AX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV [LINENO],AX
MOV AX,100H
MOV [PC],AX
```

With:

```asm
MOV [ENDED],AL
MOV [SKIPLF],AL
MOV AL,[PASS]
CMP AL,2
JNE PASSINPUT
CALL CREATEOUT
PASSINPUT:
CALL OPENFILE
NEXTLINE:
CALL READLINE
CMP AX,0
JE PASSEND
MOV SI,2200H
CALL STATEMENT
JMP NEXTLINE
PASSEND:
CALL CLOSEFILE
MOV AL,[PASS]
CMP AL,1
JNE PASSCHECK
MOV AX,[PC]
MOV [ENDPC],AX
```

### Change 5 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
CALL CMDFILES
CALL PREFLIGHT
MOV AX,0
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV [SYMC],AX
MOV AX,3000H
MOV [SYMNEXT],AX
PASSSTART:
MOV AX,100H
MOV [PC],AX
MOV AX,0
MOV [LINENO],AX
```

### Change 6 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
CALL CMDFILES
CALL PREFLIGHT
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AL,1
MOV [PASS],AL
```

## Build the stopping point

Copy `A07.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03454 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A07.COM`.

VIEW.BAS must report A07.COM length 3454 bytes. Keep that executable and source together.

## Acceptance check

Create T07.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
CHECK A07 T07.ASM RESULT.COM
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

The instruction bytes match the earlier result. I trace them from the parser through EMIT to the disk file; they no longer accumulate in a buffer for the whole program. I can erase that buffer from the memory sketch.

## A rejection check

Create X07.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
CHECK A07 X07.ASM RESULT.COM
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
