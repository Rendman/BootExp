+++
title = "01 \u00b7 Fixed work files"
weight = 1
description = "Keep the fixed work files and name the accepted result in the report."
download = "A01.ASM"
aliases = ["/bootstrap/asm86a/01-fixed-work-files/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/01-fixed-work-files/"
+++

Retain the completed assembler and its fixed SOURCE.ASM/RESULT.COM contract while preparing the streaming construction.

## The working parts

Copy the completed ASM0 source. Keep its two passes, accepted language and whole-image output buffer. OPENFILE uses SOURCE.ASM; WRITEOUT uses RESULT.COM. The success report now includes RESULT.COM so the accepted output is named explicitly.

The two input passes still finish before output creation. Preserve ASMKEEP.COM as the preceding assembler. To build a checkpoint, copy its source to SOURCE.ASM, run CHECK ASMKEEP, then copy the accepted RESULT.COM to the checkpoint executable name.

## Enter the source

Copy `ASM0.ASM` to `A01.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 74,78,69,0,0,0,8,117
DB 74,66,69,0,0,0,8,118
DB 74,65,0,0,0,0,8,119
```

Insert after old physical line 1080.

Insert:

```asm
DB 88,79,82,0,0,0,4,6

SRCNAME:
DB 83,79,85,82,67,69,46,65,83,77,0

RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0

INOPEN:
DB 0

OUTPTR:
DW 24576
```

### Change 2 near `PC:`

Unchanged source immediately before this edit:

```asm

PC:
DW 256
```

Remove this exact source at old physical positions 976–978:

```asm

OUTPTR:
DW 24576
```

There is no replacement source.

The following old source stays in place:

```asm

SYMC:
```

### Change 3 near `DIVEND:`

Unchanged source immediately before this edit:

```asm

DIVEND:
```

Remove this exact source at old physical positions 962–967:

```asm
FNAME:
DB 83,79,85,82,67,69,46,65,83,77,0

RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0
```

There is no replacement source.

The following old source stays in place:

```asm
HANDLE:
DW 0
```

### Change 4 near `OKMSG:`

Unchanged source immediately before this edit:

```asm
INT 21H

OKMSG:
```

Remove this exact source at old physical positions 943–943:

```asm
DB 79,75,32,36
```

Replace it with:

```asm
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

The following old source stays in place:

```asm

BYTEMSG:
```

### Change 5 near `IMMEDVALUE:`

Unchanged source immediately before this edit:

```asm
MOV AL,[W1]
CMP AL,0
MOV AX,[VAL]
```

Remove this exact source at old physical positions 784–784:

```asm
JE BYTEVALUE
```

Replace it with:

```asm
JNE IMMEDWORD
JMP BYTEVALUE
IMMEDWORD:
```

The following old source stays in place:

```asm
JMP EMITWORD
```

### Change 6 near `INSTRUCTION:`

Unchanged source immediately before this edit:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

Remove this exact source at old physical positions 544–544:

```asm
MOV CX,25
```

Replace it with:

```asm
MOV CX,26
```

The following old source stays in place:

```asm
MOV AX,8
CALL LOOK
```

### Change 7 near `WRITEOUT:`

Unchanged source immediately before this edit:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

Remove this exact source at old physical positions 84–84:

```asm
JB FILEBAD
```

Replace it with:

```asm
JAE ZWRITEOUT4
JMP FILEBAD
ZWRITEOUT4:
```

The following old source stays in place:

```asm
MOV DX,OKMSG
CALL TEXT
```

### Change 8 near `WRITEOUT:`

Unchanged source immediately before this edit:

```asm
INT 21H
JB FILEBAD
CMP AX,CX
```

Remove this exact source at old physical positions 80–80:

```asm
JNE FILEBAD
```

Replace it with:

```asm
JE ZWRITEOUT3
JMP FILEBAD
ZWRITEOUT3:
```

The following old source stays in place:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
```

### Change 9 near `WRITEOUT:`

Unchanged source immediately before this edit:

```asm
MOV DX,6000H
MOV AH,40H
INT 21H
```

Remove this exact source at old physical positions 78–78:

```asm
JB FILEBAD
```

Replace it with:

```asm
JAE ZWRITEOUT2
JMP FILEBAD
ZWRITEOUT2:
```

The following old source stays in place:

```asm
CMP AX,CX
JNE FILEBAD
```

### Change 10 near `WRITEOUT:`

Unchanged source immediately before this edit:

```asm
MOV CX,0
MOV AH,3CH
INT 21H
```

Remove this exact source at old physical positions 70–70:

```asm
JB FILEBAD
```

Replace it with:

```asm
JAE ZWRITEOUT1
JMP FILEBAD
ZWRITEOUT1:
```

The following old source stays in place:

```asm
MOV [HANDLE],AX
MOV BX,AX
```

### Change 11 near `CLOSEFILE:`

Unchanged source immediately before this edit:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

Remove this exact source at old physical positions 62–62:

```asm
JB FILEBAD
```

Replace it with:

```asm
JAE INPUTCLOSED
JMP FILEBAD
INPUTCLOSED:
MOV AL,0
MOV [INOPEN],AL
```

The following old source stays in place:

```asm
RET
```

### Change 12 near `INPUTOPEN:`

Unchanged source immediately before this edit:

```asm
JMP FILEBAD
INPUTOPEN:
MOV [HANDLE],AX
```

Insert after old physical line 55.

Insert:

```asm
MOV AL,1
MOV [INOPEN],AL
```

The following old source stays in place:

```asm
RET
```

### Change 13 near `OPENFILE:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

OPENFILE:
```

Remove this exact source at old physical positions 49–49:

```asm
MOV DX,FNAME
```

Replace it with:

```asm
MOV DX,SRCNAME
```

The following old source stays in place:

```asm
MOV AX,3D00H
INT 21H
```

### Change 14 at the entry

Remove this exact source at old physical positions 1–1:

```asm
; ASM86 construction checkpoint. Plain BOOTASM source.
```

Replace it with:

```asm
; ASM86A construction checkpoint.
```

The following old source stays in place:

```asm
START:
CLD
```

## Build the stopping point

Copy `A01.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 02481 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A01.COM`.

VIEW.BAS must report A01.COM length 2481 bytes. Keep that executable and source together.

## Acceptance check

Create T01.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```asm
MOV DL,41H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T01.ASM SOURCE.ASM
```

```dos
CHECK A01
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

Create X01.ASM with this separate source:

```asm
MOV AX,AL
```

```dos
COPY X01.ASM SOURCE.ASM
CHECK A01
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
