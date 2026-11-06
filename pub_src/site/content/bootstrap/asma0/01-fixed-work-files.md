+++
title = "01 \u00b7 Fixed work files"
weight = 1
description = "Select source with COPY and keep filename entry out of the new assembler."
download = "A01.ASM"
aliases = ["/bootstrap/asm86a/01-fixed-work-files/"]
download_group = "tools/asm1"
reader_names = 1
+++

The bootstrap ladder already has an assembler. We can retain its tested parser and use fixed files for the next tool.

## The working parts

Copy the completed ASM0 source. OPENFILE uses SOURCE.ASM, and the final writer uses RESULT.COM. The driver no longer calls GETNAME. The instruction language and the old whole-image buffer are otherwise unchanged at this stopping point.

The two input passes still finish before output creation. Keep ASMKEEP.COM as the preceding assembler; its existing filename prompt builds each native checkpoint. COPY selects the source for the new tool.

## Enter the source

Copy `ASM0.ASM` to `A01.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OPTAB:`

Unchanged source immediately before this edit:

```asm
DB 74,71,69,0,0,0,8,125
DB 74,76,69,0,0,0,8,126
DB 74,71,0,0,0,0,8,127
```

Insert after old physical line 1150.

Insert:

```asm

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

Remove this exact source at old physical positions 1040–1042:

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
DW 10000,1000,100,10,1

DIVEND:
```

Remove this exact source at old physical positions 1025–1030:

```asm

FNAME:
DB 0,0,0,0,0,0,0,0,0,0,0,0,0

EXTP:
DW 0
```

There is no replacement source.

The following old source stays in place:

```asm

HANDLE:
```

### Change 4 near `NEWLINE:`

Unchanged source immediately before this edit:

```asm
NEWLINE:
DB 13,10,36
```

Remove this exact source at old physical positions 1015–1020:

```asm
ASMEXT:
DB 46,65,83,77,0

COMEXT:
DB 46,67,79,77,0
```

There is no replacement source.

The following old source stays in place:

```asm
DIVISORS:
DW 10000,1000,100,10,1
```

### Change 5 near `OKMSG:`

Unchanged source immediately before this edit:

```asm
DB 83,111,117,114,99,101,32,110,97,109,101,58,32,36

OKMSG:
```

Remove this exact source at old physical positions 1001–1001:

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

### Change 6 near `ERROR:`

Unchanged source immediately before this edit:

```asm
MOV AX,4C01H
INT 21H
```

Remove this exact source at old physical positions 997–999:

```asm
PROMPT:
DB 83,111,117,114,99,101,32,110,97,109,101,58,32,36
```

There is no replacement source.

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,36
```

### Change 7 near `IMMEDVALUE:`

Unchanged source immediately before this edit:

```asm
MOV AL,[W1]
CMP AL,0
MOV AX,[VAL]
```

Remove this exact source at old physical positions 839–839:

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

### Change 8 near `WRITEOUT:`

Unchanged source immediately before this edit:

```asm
MOV DX,BYTEMSG
CALL TEXT
RET
```

Remove this exact source at old physical positions 97–147:

```asm

GETNAME:
MOV DX,PROMPT
CALL TEXT
MOV BX,2400H
MOV AL,10
MOV [BX],AL
MOV DX,2400H
MOV AH,10
INT 21H
MOV DX,NEWLINE
CALL TEXT
MOV BX,2401H
MOV AL,[BX]
MOV AH,0
CMP AX,1
JB BADNAME
CMP AX,8
JA BADNAME
MOV CX,AX
MOV SI,2402H
MOV DI,FNAME
NAMELOOP:
LODSB
CMP AL,97
JB NAMEUP
CMP AL,122
JA NAMEUP
SUB AL,32
NAMEUP:
CMP AL,95
JE NAMECHAR
CMP AL,48
JB BADNAME
CMP AL,57
JBE NAMECHAR
CMP AL,65
JB BADNAME
CMP AL,90
JA BADNAME
NAMECHAR:
STOSB
DEC CX
JNE NAMELOOP
MOV [EXTP],DI
MOV SI,ASMEXT
CALL COPYZ
RET
BADNAME:
MOV AX,1
JMP ERROR
```

There is no replacement source.

The following old source stays in place:

```asm

NEXTBYTE:
```

### Change 9 near `WRITEOUT:`

Unchanged source immediately before this edit:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

Remove this exact source at old physical positions 88–88:

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

### Change 10 near `WRITEOUT:`

Unchanged source immediately before this edit:

```asm
INT 21H
JB FILEBAD
CMP AX,CX
```

Remove this exact source at old physical positions 84–84:

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

### Change 11 near `WRITEOUT:`

Unchanged source immediately before this edit:

```asm
MOV DX,6000H
MOV AH,40H
INT 21H
```

Remove this exact source at old physical positions 82–82:

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

### Change 12 near `WRITEOUT:`

Unchanged source immediately before this edit:

```asm
MOV CX,0
MOV AH,3CH
INT 21H
```

Remove this exact source at old physical positions 74–74:

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

### Change 13 near `WRITEOUT:`

Unchanged source immediately before this edit:

```asm
RET

WRITEOUT:
```

Remove this exact source at old physical positions 67–70:

```asm
MOV DI,[EXTP]
MOV SI,COMEXT
CALL COPYZ
MOV DX,FNAME
```

Replace it with:

```asm
MOV DX,RESNAME
```

The following old source stays in place:

```asm
MOV CX,0
MOV AH,3CH
```

### Change 14 near `CLOSEFILE:`

Unchanged source immediately before this edit:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

Remove this exact source at old physical positions 63–63:

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

### Change 15 near `INPUTOPEN:`

Unchanged source immediately before this edit:

```asm
JMP FILEBAD
INPUTOPEN:
MOV [HANDLE],AX
```

Insert after old physical line 56.

Insert:

```asm
MOV AL,1
MOV [INOPEN],AL
```

The following old source stays in place:

```asm
RET
```

### Change 16 near `OPENFILE:`

Unchanged source immediately before this edit:

```asm
JMP ERROR

OPENFILE:
```

Remove this exact source at old physical positions 50–50:

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

### Change 17 near `ROOM:`

Unchanged source immediately before this edit:

```asm
MOV AX,7
JMP ERROR
ROOM:
```

Remove this exact source at old physical positions 9–9:

```asm
CALL GETNAME
```

There is no replacement source.

The following old source stays in place:

```asm
MOV AL,1
MOV [PASS],AL
```

### Change 18 at the entry

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

Run `CHECK ASMKEEP`, enter `A01` at `Source name:`, and require `OK 02521 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. It creates A01.COM.

VIEW.BAS must report A01.COM length 2521 bytes. Keep that executable and source together.

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
