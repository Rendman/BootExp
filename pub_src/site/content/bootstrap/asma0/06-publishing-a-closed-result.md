+++
title = "06 \u00b7 Publishing a closed result"
weight = 6
description = "Rename a completed temporary file into its public name."
download = "A06.ASM"
aliases = ["/bootstrap/asm86a/06-publishing-a-closed-result/"]
download_group = "tools/asm1"
reader_names = 1
+++

A result should be replaced only after all its bytes and its close have succeeded.

## The working parts

COMMIT moves an older RESULT.COM to RESULT.BAK, renames ASMA.TMP to RESULT.COM, then removes the backup. HAVEBAK and OWNTMP record the state of that sequence. If publication fails after the backup move, restoration is attempted; failed restoration retains both recovery files.

A failed backup removal also prevents OK. DOS rename is not atomic replacement, so the recovery names are explicit. The driver here still copies test data. RESULT.COM from this checkpoint is inspected with VIEW.BAS and must not be executed.

## Enter the source

Copy `A05.ASM` to `A06.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `TMPNAME:`

Unchanged source immediately before this edit:

```asm
TMPNAME:
DB 65,83,77,65,46,84,77,80,0
```

Insert after old physical line 1213.

Insert:

```asm
RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0
```

The following old source stays in place:

```asm
BAKNAME:
DB 82,69,83,85,76,84,46,66,65,75,0
```

### Change 2 near `OKMSG:`

Unchanged source immediately before this edit:

```asm
RET

OKMSG:
```

Remove this exact source at old physical positions 1077–1077:

```asm
DB 79,75,32,65,83,77,65,46,84,77,80,32,36
```

Replace it with:

```asm
DB 79,75,32,82,69,83,85,76,84,46,67,79,77,32,36
```

The following old source stays in place:

```asm

BYTEMSG:
```

### Change 3 near `PREFLIGHTOK:`

Unchanged source immediately before this edit:

```asm
PREFLIGHTOK:
RET
```

Insert after old physical line 1039.

Insert:

```asm
COMMIT:
MOV DX,RESNAME
CALL EXISTS
CMP AX,0
JE PUBLISH
MOV DX,RESNAME
MOV DI,BAKNAME
MOV AH,56H
INT 21H
JAE BACKEDUP
JMP FILEBAD
BACKEDUP:
MOV AL,1
MOV [HAVEBAK],AL
PUBLISH:
MOV DX,TMPNAME
MOV DI,RESNAME
MOV AH,56H
INT 21H
JAE PUBLISHED
MOV AL,[HAVEBAK]
CMP AL,0
JE PUBLISHFAIL
MOV DX,BAKNAME
MOV DI,RESNAME
MOV AH,56H
INT 21H
JAE RESTORED
MOV AL,1
MOV [KEEPFILES],AL
JMP PUBLISHFAIL
RESTORED:
MOV AL,0
MOV [HAVEBAK],AL
PUBLISHFAIL:
JMP FILEBAD
PUBLISHED:
MOV AL,0
MOV [OWNTMP],AL
MOV AL,[HAVEBAK]
CMP AL,0
JE COMMITDONE
MOV DX,BAKNAME
MOV AH,41H
INT 21H
JAE BACKREMOVED
JMP FILEBAD
BACKREMOVED:
MOV AL,0
MOV [HAVEBAK],AL
COMMITDONE:
RET
```

The following old source stays in place:

```asm
CLEANUP:
MOV AL,[INOPEN]
```

### Change 4 near `COPYDONE:`

Unchanged source immediately before this edit:

```asm
CALL CLOSEFILE
CALL FLUSH
CALL CLOSEOUT
```

Insert after old physical line 31.

Insert:

```asm
CALL COMMIT
```

The following old source stays in place:

```asm
MOV DX,OKMSG
CALL TEXT
```

## Build the stopping point

Copy `A06.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 02940 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A06.COM`.

VIEW.BAS must report A06.COM length 2940 bytes. Keep that executable and source together.

## Acceptance check

Create T06.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```text
ABC
```

```dos
COPY T06.ASM SOURCE.ASM
```

```dos
CHECK A06
```

Require:

```text
OK RESULT.COM 00005 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **5 bytes** and these complete contents:

```text
41 42 43 0D 0A
```

The byte inspection is the stopping check for this encoding exercise. Keep the result as data.

## A rejection check

```dos
REN SOURCE.ASM HOLD.ASM
CHECK A06
```

Choose an unused HOLD.ASM name before renaming. Restore HOLD.ASM to SOURCE.ASM afterward.

Require:

```text
ERROR 00000 CODE 6
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with COMP if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check the fixed name bytes, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
