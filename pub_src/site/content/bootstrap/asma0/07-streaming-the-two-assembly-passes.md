+++
title = "07 \u00b7 Streaming the two assembly passes"
weight = 7
description = "Return to the assembler with no complete image buffer."
download = "A07.ASM"
aliases = ["/bootstrap/asm86a/07-streaming-the-two-assembly-passes/"]
download_group = "tools/asm1"
reader_names = 1
+++

The tested block writer can now receive bytes as pass two produces them.

## The working parts

Pass one records definitions and counts instruction bytes without writing. Its final PC is saved in ENDPC. Pass two creates the temporary output, reopens the source, emits incrementally, and must finish at the same PC. FLUSH, CLOSEOUT, and COMMIT run only after successful source close.

PC describes the target; OUTCNT describes the current block. They are independent. Input, parser, or range errors remove this run's temporary file and preserve an older RESULT.COM. The accepted language remains the published ASM0 vocabulary.

## Enter the source

Copy `A06.ASM` to `A07.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OUTHANDLE:`

Unchanged source immediately before this edit:

```asm
OUTHANDLE:
DW 0
```

Insert after old physical line 1290.

Insert:

```asm
ENDPC:
DW 0
```

The following old source stays in place:

```asm
INOPEN:
DB 0
```

### Change 2 near `COPYDONE:`

Unchanged source immediately before this edit:

```asm
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

Insert after old physical line 39.

Insert:

```asm
GOOD:
```

The following old source stays in place:

```asm
MOV AX,4C00H
INT 21H
```

### Change 3 near `ROOM:`

Unchanged source immediately before this edit:

```asm
MOV [PC],AX
MOV AL,2
MOV [PASS],AL
```

Remove this exact source at old physical positions 19–29:

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

Replace it with:

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

The following old source stays in place:

```asm
CALL FLUSH
CALL CLOSEOUT
```

### Change 4 near `ROOM:`

Unchanged source immediately before this edit:

```asm
MOV [RDPOS],AX
MOV [RDLEN],AX
MOV [OUTCNT],AX
```

Remove this exact source at old physical positions 14–16:

```asm
MOV [LINENO],AX
MOV AX,100H
MOV [PC],AX
```

Replace it with:

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

The following old source stays in place:

```asm
MOV AL,2
MOV [PASS],AL
```

### Change 5 near `ROOM:`

Unchanged source immediately before this edit:

```asm
ROOM:
CALL PREFLIGHT
MOV AX,0
```

Insert after old physical line 10.

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

The following old source stays in place:

```asm
MOV [RDPOS],AX
MOV [RDLEN],AX
```

### Change 6 near `ROOM:`

Unchanged source immediately before this edit:

```asm
JMP ERROR
ROOM:
CALL PREFLIGHT
```

Insert after old physical line 9.

Insert:

```asm
MOV AL,1
MOV [PASS],AL
```

The following old source stays in place:

```asm
MOV AX,0
MOV [RDPOS],AX
```

## Build the stopping point

Copy `A07.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03016 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A07.COM`.

VIEW.BAS must report A07.COM length 3016 bytes. Keep that executable and source together.

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
COPY T07.ASM SOURCE.ASM
```

```dos
CHECK A07
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

Create X07.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X07.ASM SOURCE.ASM
CHECK A07
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check the fixed name bytes, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
