+++
title = "04 \u00b7 Cleaning an interrupted output"
weight = 4
description = "Track handles and temporary-file ownership separately."
download = "A04.ASM"
+++

A failed assembly must not leave its own partial temporary output looking usable.

## The working parts

ERROR saves its category before CLEANUP can change AX. INOPEN and OUTOPEN describe live handles; OWNTMP says whether this run created ASMA.TMP. Cleanup closes the owned handles and removes its own temporary file. It never deletes RESULT.COM.

A failed close or delete sets CLEANFAIL. The error report includes a recovery notice when files may need inspection. Cleanup does not recurse into ERROR. The copy driver still leaves ASMA.TMP after success, but a failed input open now removes its newly created empty temporary file.

## Enter the source

Copy `A03.ASM` to `A04.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `OWNTMP:`

Unchanged source immediately before this edit:

```asm

OWNTMP:
DB 0
```

Insert after old physical line 1156.

Insert:

```asm

HAVEBAK:
DB 0

KEEPFILES:
DB 0

CLEANFAIL:
DB 0
```

### Change 2 near `TMPNAME:`

Unchanged source immediately before this edit:

```asm
TMPNAME:
DB 65,83,77,65,46,84,77,80,0
```

Insert after old physical line 1136.

Insert:

```asm
RECOVERMSG:
DB 82,101,99,111,118,101,114,121,58,32,105,110,115,112,101,99
DB 116,32,65,83,77,65,46,84,77,80,32,97,110,100,32,82
DB 69,83,85,76,84,46,66,65,75,13,10,36
```

The following old source stays in place:

```asm
RDPOS:
DW 0
```

### Change 3 near `FLUSHDONE:`

Unchanged source immediately before this edit:

```asm
POP CX
POP BX
POP AX
```

Insert after old physical line 991.

Insert:

```asm
RET

CLEANUP:
MOV AL,[INOPEN]
CMP AL,0
JE CLEANOUTPUT
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
JAE CLEANOUTPUT
MOV AL,1
MOV [CLEANFAIL],AL
CLEANOUTPUT:
MOV AL,[OUTOPEN]
CMP AL,0
JE CLEANTEMP
MOV BX,[OUTHANDLE]
MOV AH,3EH
INT 21H
JAE CLEANTEMP
MOV AL,1
MOV [CLEANFAIL],AL
CLEANTEMP:
MOV AL,[OWNTMP]
CMP AL,0
JE CLEANEND
MOV AL,[KEEPFILES]
CMP AL,0
JNE CLEANEND
MOV DX,TMPNAME
MOV AH,41H
INT 21H
JAE CLEANEND
MOV AL,1
MOV [CLEANFAIL],AL
CLEANEND:
```

The following old source stays in place:

```asm
RET
```

### Change 4 near `ERROR:`

Unchanged source immediately before this edit:

```asm
INT 21H
MOV DX,NEWLINE
CALL TEXT
```

Insert after old physical line 938.

Insert:

```asm
MOV AL,[CLEANFAIL]
MOV DL,[KEEPFILES]
OR AL,DL
MOV DL,[HAVEBAK]
OR AL,DL
CMP AL,0
JE ERROREXIT
MOV DX,RECOVERMSG
CALL TEXT
ERROREXIT:
```

The following old source stays in place:

```asm
MOV AX,4C01H
INT 21H
```

### Change 5 near `ERROR:`

Unchanged source immediately before this edit:

```asm

ERROR:
MOV [ERRCODE],AL
```

Insert after old physical line 925.

Insert:

```asm
CALL CLEANUP
```

The following old source stays in place:

```asm
MOV DX,ERRMSG
CALL TEXT
```

## Build the stopping point

Run `CHECK ASMKEEP`, enter `A04` at `Source name:`, and require `OK 02766 bytes` and PASS. This uses the preceding published ASM86, not the new checkpoint. It creates A04.COM.

VIEW.BAS must report A04.COM length 2766 bytes. Keep that executable and source together.

## Acceptance check

Create T04.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```text
ABC
```

```dos
COPY T04.ASM SOURCE.ASM
```

```dos
CHECK A04
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
REN SOURCE.ASM HOLD.ASM
CHECK A04
```

Choose an unused HOLD.ASM name before renaming. Restore HOLD.ASM to SOURCE.ASM afterward.

Require:

```text
ERROR 00000 CODE 6
FAIL
```

The pre-existing RESULT.COM must remain unchanged. A missing-source failure must remove only the temporary file this run owned.

An unexpected PASS fails this rejection test.

## If the result differs

Check the fixed name bytes, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
