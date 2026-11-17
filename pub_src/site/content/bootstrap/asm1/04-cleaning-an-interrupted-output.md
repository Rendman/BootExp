+++
title = "10 \u00b7 Cleaning an interrupted output"
weight = 10
description = "Track handles and temporary-file ownership separately."
download = "A04.ASM"
aliases = ["/bootstrap/asm86a/04-cleaning-an-interrupted-output/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/04-cleaning-an-interrupted-output/"
+++

The copy writer creates its temporary file before opening the source. If that open fails, an empty file remains. I need to keep track of which handles are open and which file this run created, so the error routine can clean up after itself.

## The working parts

ERROR saves its category before CLEANUP can change AX. INOPEN and OUTOPEN describe live handles; OWNTMP says whether this run created ASMA.TMP. Cleanup closes the owned handles and removes its own temporary file. It never deletes RESULT.COM.

A failed close or delete sets CLEANFAIL. The error report includes a recovery notice when files may need inspection. Cleanup does not recurse into ERROR. The copy driver still leaves ASMA.TMP after success, but a failed input open now removes its newly created empty temporary file.

## Enter the source

Copy `A03.ASM` to `A04.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `CMDCOUNT:`

Find the unique label `CMDCOUNT:`. Insert the new source immediately before this existing label:

```asm
CMDCOUNT:
```

Insert:

```asm
HAVEBAK:
DB 0
KEEPFILES:
DB 0
CLEANFAIL:
DB 0
```

### Change 2 · `RDPOS:`

Find the unique label `RDPOS:`. Insert the new source immediately before this existing label:

```asm
RDPOS:
```

Insert:

```asm
RECOVERMSG:
DB 82,101,99,111,118,101,114,121,58,32,105,110,115,112,101,99
DB 116,32,65,83,77,65,46,84,77,80,32,97,110,100,32,82
DB 69,83,85,76,84,46,66,65,75,13,10,36
```

### Change 3 · `FLUSHDONE:`

Find the unique label `FLUSHDONE:`, then follow this unchanged source through its last displayed instruction:

```asm
FLUSHDONE:
POP DX
POP CX
POP BX
POP AX
```

The edit begins immediately after that unchanged block.

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

### Change 4 · `ERROR:`

Find the unique label `ERROR:`, then follow this unchanged source through its last displayed instruction:

```asm
ERROR:
MOV [ERRCODE],AL
MOV DX,ERRMSG
CALL TEXT
MOV AX,[LINENO]
CALL NUMBER
MOV DX,CODEMSG
CALL TEXT
MOV AL,[ERRCODE]
ADD AL,48
MOV DL,AL
MOV AH,2
INT 21H
MOV DX,NEWLINE
CALL TEXT
```

The edit begins immediately after that unchanged block.

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

### Change 5 · `ERROR:`

Find the unique label `ERROR:`, then follow this unchanged source through its last displayed instruction:

```asm
ERROR:
MOV [ERRCODE],AL
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CALL CLEANUP
```

## Build the stopping point

Copy `A04.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03188 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A04.COM`.

VIEW.BAS must report A04.COM length 3188 bytes. Keep that executable and source together.

## Acceptance check

Create T04.ASM as plain ASCII with COPY CON or an editor. Finish COPY CON with Ctrl-Z and Enter:

```text
ABC
```

```dos
CHECK A04 T04.ASM RESULT.COM
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
REN T04.ASM HOLD.ASM
CHECK A04 T04.ASM RESULT.COM
```

Choose an unused HOLD.ASM name before renaming. Restore HOLD.ASM to the selected fixture name afterward.

Require:

```text
ERROR 00000 CODE 6
FAIL
```

The pre-existing RESULT.COM must remain unchanged. A missing-source failure must remove only the temporary file this run owned.

An unexpected PASS fails this rejection test.

## If the result differs

Check the saved argument names and terminators, handle ownership flags, reader cursors at each pass, and the current output count. Inspect file length as well as the leading bytes. A copied data file is not an executable proof.
