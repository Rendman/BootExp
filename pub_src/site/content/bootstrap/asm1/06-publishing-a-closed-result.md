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

**Starting source:** `A05.ASM`. **Save as:** `A06.ASM`. **Build with:** `ASMKEEP.COM`.

## The working parts

COMMIT moves an older selected result to RESULT.BAK, renames ASMA.TMP to the selected result name, then removes the backup. With no filename arguments, that result name is RESULT.COM. HAVEBAK and OWNTMP record the state of that sequence. If publication fails after the backup move, restoration is attempted; failed restoration retains both recovery files.

A failed backup removal also prevents OK. DOS rename is not atomic replacement, so the recovery names are explicit. The driver here still copies test data. RESULT.COM from this checkpoint is inspected with VIEW.BAS and must not be executed.

## Enter the source

Copy `A05.ASM` to `A06.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `CLEANUP:`

Find the unique label `CLEANUP:`. Insert the new source immediately before this existing label:

```asm
CLEANUP:
```

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

### Change 2 · `COPYDONE:`

Find the unique label `COPYDONE:`, then follow this unchanged source through its last displayed instruction:

```asm
COPYDONE:
CALL CLOSEFILE
CALL FLUSH
CALL CLOSEOUT
MOV DX,OKMSG
CALL TEXT
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV SI,TMPNAME
```

With:

```asm
MOV SI,RESNAME
```

### Change 3 · `COPYDONE:`

Find the unique label `COPYDONE:`, then follow this unchanged source through its last displayed instruction:

```asm
COPYDONE:
CALL CLOSEFILE
CALL FLUSH
CALL CLOSEOUT
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CALL COMMIT
```

## Build the stopping point

Copy `A06.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03378 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A06.COM`.

Keep that executable and source together.

## Acceptance check

Reuse the earlier input unchanged:

```dos
COPY T03.ASM T06.ASM
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

These are the copied text bytes, including their line ending. Inspect the result as data.

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

Trace HAVEBAK and OWNTMP through each rename. The temporary output must be closed before publication, and a failed replacement must attempt to restore the saved result.
