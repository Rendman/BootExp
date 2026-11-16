+++
title = "05 \u00b7 Protecting recovery names"
weight = 5
description = "Refuse an occupied temporary or backup name before creating output."
download = "A05.ASM"
aliases = ["/bootstrap/asm86a/05-protecting-recovery-names/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/05-protecting-recovery-names/"
+++

I have given the temporary file a fixed name, but finding that name on disk does not tell me where it came from. It might be left from an interrupted run. I want the program to stop and let me inspect it before creating anything under the same name.

## The working parts

EXISTS opens an ordinary fixed disk name read-only, closes it if found, and returns one; only file-not-found returns zero. Other DOS failures remain errors. PREFLIGHT checks ASMA.TMP and RESULT.BAK and reports category eight if either is present.

The checks occur before CREATEOUT. A reserved file is not silently erased. Inspect or rename a leftover file before trying again. AX, BX, and DOS flags are scratch during existence checks.

## Enter the source

Copy `A04.ASM` to `A05.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `FLUSHDONE:`

Unchanged source immediately before this edit:

```asm
POP AX
RET
```

Insert after old physical line 1010.

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

### Change 2 near `ROOM:`

Unchanged source immediately before this edit:

```asm
JMP ERROR
ROOM:
CALL CMDFILES
```

Insert after old physical line 9.

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

Copy `A05.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03257 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A05.COM`.

VIEW.BAS must report A05.COM length 3257 bytes. Keep that executable and source together.

## Acceptance check

Create T05.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```text
ABC
```

```dos
CHECK A05 T05.ASM RESULT.COM
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
ECHO RECOVERY>ASMA.TMP
CHECK A05 T05.ASM RESULT.COM
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

Check the saved argument names and terminators, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
