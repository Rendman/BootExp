+++
title = "01 \u00b7 Choosing the Source and Result Names"
weight = 1
description = "Read source and result filenames from the PSP and name the accepted result in the report."
download = "A01.ASM"
aliases = ["/bootstrap/asm86a/01-fixed-work-files/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/01-fixed-work-files/"
+++

ASM0 can assemble its own source now. I keep that working copy beside the BASIC listing and copy its source to begin ASM1. This time I want to type the source and result names after the program name, and have its report tell me which result it wrote.

## The working parts

Copy the completed ASM0 source. Keep its two passes, accepted language and whole-image output buffer. OPENFILE uses the selected source buffer; WRITEOUT uses the selected result buffer. With no arguments their defaults remain SOURCE.ASM and RESULT.COM. The success report prints the selected result name.

The two input passes still finish before output creation. Preserve ASMKEEP.COM as the preceding assembler. To build a checkpoint, copy its source to SOURCE.ASM, run CHECK ASMKEEP, then copy the accepted RESULT.COM to the checkpoint executable name.

## Names after the program name

DOS leaves a command tail in the Program Segment Prefix, or PSP, the area before the program's 0100H entry. Its byte at 80H is the tail length; the text starts at 81H. Read that length rather than searching for a zero terminator. At entry DS and ES select the program segment, including the PSP.

CMDINIT walks the bounded tail before any file service. Spaces and tabs separate names. It folds letters, checks an eight-character base and optional three-character extension, and copies each spelling plus a zero terminator into a separate owned slot. A dot needs a nonempty base and extension. Paths, quotes and switches are rejected. The saved names survive DOS services that can reuse the PSP tail area as a disk-transfer area.

CMDFILES accepts no names, preserving SOURCE.ASM and RESULT.COM, or exactly two names selecting source and result. It copies the selections into the source/result buffers and rejects equal names and either recovery name before opening output. CMDMATCH compares complete terminated spellings; CMDTEXT prints the selected result. These routines use only instructions ASM0 already accepts. They change the working registers, so the assembly driver initializes its counters afterward. Error category 9 means invalid command-line names or count.

The temporary ASMA.TMP and backup RESULT.BAK keep their reserved roles. Use ordinary disk files in the current directory. The chosen result is not the running builder; preserve each checkpoint executable separately.

Replace CHECK.BAT with this version, which passes the filename arguments to its program and checks its status immediately:

```dos
ECHO OFF
IF "%1"=="" GOTO USAGE
IF NOT EXIST %1.COM GOTO MISSING
%1 %2 %3 %4 %5 %6 %7 %8 %9
IF ERRORLEVEL 1 GOTO FAIL
ECHO.
ECHO PASS
GOTO END
:FAIL
ECHO.
ECHO FAIL
GOTO END
:MISSING
ECHO Missing program
GOTO END
:USAGE
ECHO Use CHECK name [filenames]
:END
```

The original ASMKEEP still takes no arguments. Build this checkpoint with it using the fixed SOURCE.ASM name. Once A01.COM is saved, `CHECK A01 T01.ASM RESULT.COM` supplies the new names through the PSP.

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
DB 83,79,85,82,67,69,46,65,83,77,0,0,0

TMPNAME:
DB 65,83,77,65,46,84,77,80,0

RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0,0,0

BAKNAME:
DB 82,69,83,85,76,84,46,66,65,75,0

INOPEN:
DB 0

OUTPTR:
DW 24576

CMDCOUNT:
DW 0

CMDPTR:
DW 0

CMDBUF:
DB 0,0,0,0,0,0,0,0,0,0,0,0,0
DB 0,0,0,0,0,0,0,0,0,0,0,0,0
DB 0,0,0,0,0,0,0,0,0,0,0,0,0
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

### Change 4 near `ERROR:`

Unchanged source immediately before this edit:

```asm
MOV AX,4C01H
INT 21H
```

Insert after old physical line 941.

Insert:

```asm
CMDINIT:
MOV SI,81H
MOV DI,CMDBUF
MOV [CMDPTR],DI
MOV AL,[80H]
MOV AH,0
MOV CX,AX
CMP CX,127
JB ZCMDINIT1
JMP CMDBAD
ZCMDINIT1:
CMDSKIP:
CMP CX,0
JNE ZCMDINIT2
JMP CMDDONE
ZCMDINIT2:
LODSB
DEC CX
CMP AL,32
JE CMDSKIP
CMP AL,9
JE CMDSKIP
MOV BX,[CMDCOUNT]
CMP BX,3
JB ZCMDINIT3
JMP CMDBAD
ZCMDINIT3:
INC BX
MOV [CMDCOUNT],BX
MOV BX,0
MOV DX,8
CMDCHAR:
CMP AL,46
JNE ZCMDINIT4
JMP CMDDOT
ZCMDINIT4:
CMP AL,97
JB CMDUP
CMP AL,122
JA CMDUP
SUB AL,32
CMDUP:
CMP AL,65
JB CMDNUM
CMP AL,90
JBE CMDPUT
CMDNUM:
CMP AL,48
JB CMDEXTRA
CMP AL,57
JBE CMDPUT
CMDEXTRA:
CMP AL,95
JE CMDPUT
CMP AL,45
JE ZCMDINIT5
JMP CMDBAD
ZCMDINIT5:
CMDPUT:
INC BX
CMP BX,DX
JBE ZCMDINIT6
JMP CMDBAD
ZCMDINIT6:
STOSB
JMP CMDNEXT
CMDDOT:
CMP DX,8
JE ZCMDINIT7
JMP CMDBAD
ZCMDINIT7:
CMP BX,0
JNE ZCMDINIT8
JMP CMDBAD
ZCMDINIT8:
MOV DX,3
MOV BX,0
STOSB
CMDNEXT:
CMP CX,0
JE CMDEND
LODSB
DEC CX
CMP AL,32
JE CMDEND
CMP AL,9
JE ZCMDINIT9
JMP CMDCHAR
ZCMDINIT9:
CMDEND:
CMP BX,0
JE CMDBAD
MOV AL,0
STOSB
MOV DI,[CMDPTR]
ADD DI,13
MOV [CMDPTR],DI
JMP CMDSKIP
CMDDONE:
MOV AX,[CMDCOUNT]
RET
CMDBAD:
MOV AX,65535
RET

CMDMATCH:
LODSB
MOV BX,DI
MOV AH,[BX]
CMP AL,AH
JNE CMDNO
INC DI
CMP AL,0
JNE CMDMATCH
MOV AX,1
RET
CMDNO:
MOV AX,0
RET

CMDFILES:
CALL CMDINIT
CMP AX,0
JNE ZCMDFILES1
JMP CMDREADY
ZCMDFILES1:
CMP AX,2
JE ZCMDFILES2
JMP CMDFAIL
ZCMDFILES2:
MOV SI,CMDBUF
MOV DI,SRCNAME
CALL COPYZ
MOV SI,CMDBUF
ADD SI,13
MOV DI,RESNAME
CALL COPYZ
MOV SI,SRCNAME
MOV DI,RESNAME
CALL CMDMATCH
CMP AX,0
JE ZCMDFILES3
JMP CMDFAIL
ZCMDFILES3:
MOV SI,SRCNAME
MOV DI,TMPNAME
CALL CMDMATCH
CMP AX,0
JE ZCMDFILES4
JMP CMDFAIL
ZCMDFILES4:
MOV SI,SRCNAME
MOV DI,BAKNAME
CALL CMDMATCH
CMP AX,0
JNE CMDFAIL
MOV SI,RESNAME
MOV DI,TMPNAME
CALL CMDMATCH
CMP AX,0
JNE CMDFAIL
MOV SI,RESNAME
MOV DI,BAKNAME
CALL CMDMATCH
CMP AX,0
JNE CMDFAIL
CMDREADY:
RET
CMDFAIL:
MOV AX,9
JMP ERROR

CMDTEXT:
LODSB
CMP AL,0
JE CMDTEXTEND
MOV DL,AL
MOV AH,2
INT 21H
JMP CMDTEXT
CMDTEXTEND:
RET
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,36
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
JB FILEBAD
MOV DX,OKMSG
CALL TEXT
```

Insert after old physical line 86.

Insert:

```asm
MOV SI,RESNAME
CALL CMDTEXT
MOV DL,32
MOV AH,2
INT 21H
```

The following old source stays in place:

```asm
MOV AX,[PC]
SUB AX,100H
```

### Change 8 near `WRITEOUT:`

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

### Change 9 near `WRITEOUT:`

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

### Change 10 near `WRITEOUT:`

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

### Change 11 near `WRITEOUT:`

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

### Change 12 near `CLOSEFILE:`

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

### Change 13 near `INPUTOPEN:`

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

### Change 14 near `OPENFILE:`

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

### Change 15 near `ROOM:`

Unchanged source immediately before this edit:

```asm
MOV AX,7
JMP ERROR
ROOM:
```

Insert after old physical line 8.

Insert:

```asm
CALL CMDFILES
```

The following old source stays in place:

```asm
MOV AL,1
MOV [PASS],AL
```

### Change 16 at the entry

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

Copy `A01.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 02939 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A01.COM`.

VIEW.BAS must report A01.COM length 2939 bytes. Keep that executable and source together.

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
CHECK A01 T01.ASM RESULT.COM
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
CHECK A01 X01.ASM RESULT.COM
```

Require:

```text
ERROR 00001 CODE 1
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## Check the command tail

With T01.ASM retained, run `CHECK A01 T01.ASM CHOSEN.COM`. Require `OK CHOSEN.COM 00011 bytes` and PASS. Inspect CHOSEN.COM: its bytes must match the accepted fixture. The source itself is unchanged.

Then run `CHECK A01 T01.ASM` and `CHECK A01 T01.ASM t01.asm`. Each must report `ERROR 00000 CODE 9` and FAIL before creating any output. Preserve the accepted CHOSEN.COM and source. A too-long base, a second dot, a path, or either reserved recovery name also fails the argument check.

## If the result differs

Check the saved argument names and terminators, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
