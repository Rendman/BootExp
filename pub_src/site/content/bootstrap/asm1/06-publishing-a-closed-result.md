+++
title = "12 \u00b7 Publishing a closed result"
weight = 12
description = "Rename a completed temporary file into its public name."
download = "A06.ASM"
aliases = ["/bootstrap/asm86a/06-publishing-a-closed-result/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/06-publishing-a-closed-result/"
+++

The copied bytes are safely in a closed temporary file. I want to give that file the result name while keeping a way back if a rename fails. I write the three filenames in my notebook and follow where the accepted copy would be after each DOS call.

## The working parts

COMMIT moves an older RESULT.COM to RESULT.BAK, renames ASMA.TMP to RESULT.COM, then removes the backup. HAVEBAK and OWNTMP record the state of that sequence. If publication fails after the backup move, restoration is attempted; failed restoration retains both recovery files.

A failed backup removal also prevents OK. DOS rename is not atomic replacement, so the recovery names are explicit. The driver here still copies test data. RESULT.COM from this checkpoint is inspected with VIEW.BAS and must not be executed.

## Enter the source

Copy `A05.ASM` to `A06.ASM`. Apply the following edits **from the bottom of the old file upward**. Physical positions locate an edit in the unchanged old file; use the nearby label and printed context to identify it. Keep all other source. The Z labels are ordinary implementation labels for explicit short-branch bridges.

### Change 1 near `PREFLIGHTOK:`

Unchanged source immediately before this edit:

```asm
PREFLIGHTOK:
RET
```

Insert after old physical line 1045.

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

### Change 2 near `COPYDONE:`

Unchanged source immediately before this edit:

```asm
CALL CLOSEOUT
MOV DX,OKMSG
CALL TEXT
```

Remove this exact source at old physical positions 35–35:

```asm
MOV SI,TMPNAME
```

Replace it with:

```asm
MOV SI,RESNAME
```

The following old source stays in place:

```asm
CALL CMDTEXT
MOV DL,32
```

### Change 3 near `COPYDONE:`

Unchanged source immediately before this edit:

```asm
CALL CLOSEFILE
CALL FLUSH
CALL CLOSEOUT
```

Insert after old physical line 32.

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

Copy `A06.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03378 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A06.COM`.

VIEW.BAS must report A06.COM length 3378 bytes. Keep that executable and source together.

## Acceptance check

Create T06.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```text
ABC
```

```dos
CHECK A06 T06.ASM RESULT.COM
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
REN T06.ASM HOLD.ASM
CHECK A06 T06.ASM RESULT.COM
```

Choose an unused HOLD.ASM name before renaming. Restore HOLD.ASM to the selected fixture name afterward.

Require:

```text
ERROR 00000 CODE 6
FAIL
```

The accepted RESULT.COM must remain unchanged. Keep a copy and compare it with C:\DOS\FC.EXE /B if in doubt. Require a fresh OK before using any output.

An unexpected PASS fails this rejection test.

## If the result differs

Check the saved argument names and terminators, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
