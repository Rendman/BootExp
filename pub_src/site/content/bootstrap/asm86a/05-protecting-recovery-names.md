+++
title = "05 \u00b7 Protecting recovery names"
weight = 5
description = "Refuse an occupied temporary or backup name before creating output."
download = "A05.ASM"
+++

An earlier interrupted run may have left a file worth recovering.

## The working parts

EXISTS opens an ordinary fixed disk name read-only, closes it if found, and returns one; only file-not-found returns zero. Other DOS failures remain errors. PREFLIGHT checks ASMA.TMP and RESULT.BAK and reports category eight if either is present.

The checks occur before CREATEOUT. A reserved file is not silently erased. Inspect or rename a leftover file before trying again. AX, BX, and DOS flags are scratch during existence checks.

## Enter the source

Copy `A04.ASM` to `A05.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `TMPNAME:`

Unchanged source immediately before this edit:

```asm
TMPNAME:
DB 65,83,77,65,46,84,77,80,0
```

Insert after old physical line 1183.

Insert:

```asm
BAKNAME:
DB 82,69,83,85,76,84,46,66,65,75,0
```

The following old source stays in place:

```asm
RECOVERMSG:
DB 82,101,99,111,118,101,114,121,58,32,105,110,115,112,101,99
```

### Change 2 near `FLUSHDONE:`

Unchanged source immediately before this edit:

```asm
POP AX
RET
```

Insert after old physical line 1004.

Insert:

```asm
EXISTS:
MOV AX,3D00H
INT 21H
JAE FILEEXISTS
CMP AX,2
JE FILENONE
JMP FILEBAD
FILEEXISTS:
MOV BX,AX
MOV AH,3EH
INT 21H
JAE EXISTSCLOSED
JMP FILEBAD
EXISTSCLOSED:
MOV AX,1
RET
FILENONE:
MOV AX,0
RET
PREFLIGHT:
MOV DX,TMPNAME
CALL EXISTS
CMP AX,0
JNE NAMEBUSY
MOV DX,BAKNAME
CALL EXISTS
CMP AX,0
JE PREFLIGHTOK
NAMEBUSY:
MOV AX,8
JMP ERROR
PREFLIGHTOK:
RET
```

The following old source stays in place:

```asm
CLEANUP:
MOV AL,[INOPEN]
```

### Change 3 near `ROOM:`

Unchanged source immediately before this edit:

```asm
MOV AX,7
JMP ERROR
ROOM:
```

Insert after old physical line 8.

Insert:

```asm
CALL PREFLIGHT
```

The following old source stays in place:

```asm
MOV AX,0
MOV [RDPOS],AX
```

## Build the stopping point

Run `CHECK ASMKEEP`, enter `A05` at `Source name:`, and require `OK 02846 bytes` and PASS. This uses the preceding published ASM86, not the new checkpoint. It creates A05.COM.

VIEW.BAS must report A05.COM length 2846 bytes. Keep that executable and source together.

## Acceptance check

Create T05.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```text
ABC
```

```dos
COPY T05.ASM SOURCE.ASM
```

```dos
CHECK A05
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

This result is an encoding or data exercise. Inspect its bytes; do not execute it.

## A rejection check

After inspecting the successful copy, delete ASMA.TMP. It belongs to this copy exercise.

```dos
ECHO RECOVERY>ASMA.TMP
CHECK A05
```

TYPE ASMA.TMP afterward: its RECOVERY text must be unchanged. After inspection, delete this deliberately created test file.

Require:

```text
ERROR 00000 CODE 8
FAIL
```

The pre-existing RESULT.COM must remain unchanged. A missing-source failure must remove only the temporary file this run owned.

An unexpected PASS fails this rejection test.

## If the result differs

Check the fixed name bytes, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
