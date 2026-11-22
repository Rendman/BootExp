+++
title = "11 \u00b7 Protecting recovery names"
weight = 11
description = "Refuse an occupied temporary or backup name before creating output."
download = "A05.ASM"
aliases = ["/bootstrap/asm86a/05-protecting-recovery-names/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/05-protecting-recovery-names/"
+++

I have given the temporary file a fixed name, but finding that name on disk does not tell me where it came from. It might be left from an interrupted run. I want the program to stop and let me inspect it before creating anything under the same name.

**Starting source:** `A04.ASM`. **Save as:** `A05.ASM`. **Build with:** `ASMKEEP.COM`.

## The working parts

EXISTS opens an ordinary fixed disk name read-only, closes it if found, and returns one; only file-not-found returns zero. Other DOS failures remain errors. PREFLIGHT checks ASMA.TMP and RESULT.BAK and reports category eight if either is present.

The checks occur before CREATEOUT. A reserved file is not silently erased. Inspect or rename a leftover file before trying again. AX, BX, and DOS flags are scratch during existence checks.

## Enter the source

Copy `A04.ASM` to `A05.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `CLEANUP:`

Find the unique label `CLEANUP:`. Insert the new source immediately before this existing label:

```asm
CLEANUP:
```

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

### Change 2 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
CALL CMDFILES
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CALL PREFLIGHT
```

## Build the stopping point

Copy `A05.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03257 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A05.COM`.

Keep that executable and source together.

## Acceptance check

Reuse the earlier input unchanged:

```dos
COPY T03.ASM T05.ASM
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

These are the copied text bytes, including their line ending. Inspect the result as data.

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

PREFLIGHT must leave both the pre-existing RESULT.COM and the unowned ASMA.TMP unchanged. No output file should be created or removed by this rejected run.

An unexpected PASS fails this rejection test.

## If the result differs

Run PREFLIGHT before CREATEOUT. A reserved file is evidence to inspect, not permission to truncate it. Remove only the RECOVERY file deliberately created for this test.
