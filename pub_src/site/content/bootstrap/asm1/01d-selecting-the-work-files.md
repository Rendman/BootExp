+++
title = "04 \u00b7 Selecting the Source and Result"
weight = 4
description = "Connect the saved names to file services and reject collisions before opening files."
download = "A01D.ASM"
download_group = "tools/asm1"
reader_names = 1
command_examples = "literal"
url = "/bootstrap/asma0/01d-selecting-the-work-files/"
+++

The reader can retain names without touching disk. I replace the temporary probe call with file selection and connect those retained spellings to the two existing file services.

**Starting source:** `A01C.ASM`. **Save as:** `A01D.ASM`. **Build with:** `ASMKEEP.COM`.

## What this step adds

CMDFILES calls CMDINIT once. Zero names keep the known SOURCE.ASM and RESULT.COM defaults. Exactly two names are copied from the first and second CMDBUF slots into SRCNAME and RESNAME with the existing COPYZ routine. Any other count, including CMDINIT's 65535 failure value, enters ERROR with category 9.

CMDMATCH compares two complete zero-terminated spellings. SI and DI advance through the names; BX and AH are scratch. AX is one for equality and zero for inequality. A shared prefix alone is not equality. Because CMDINIT folds letters before copying, differently cased spellings of the same filename compare equal.

Five comparisons reject source=result, source=temporary, source=backup, result=temporary and result=backup. TMPNAME names ASMA.TMP; BAKNAME names RESULT.BAK. Those names are reserved internal work names, distinct from the selected source and result. These comparisons check selected spellings; they do not inspect or create recovery files. Existing files under those names are not checked by this helper.

Remove CMDPROBE and its startup call. The retained driver calls CMDFILES after its stack check and before pass counters or file services. The helper changes the working registers, so those counters are initialized afterward. OPENFILE and WRITEOUT already use the two name-buffer addresses. Both input passes still finish before output creation.

The chosen result must also differ from the running checkpoint's executable name. Keep the builder under its own saved name. Use only unquoted 8.3 names in the current directory. This checkpoint reports just OK and the byte count.


## Enter the source

Copy A01C.ASM to A01D.ASM. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OUTPTR:`

Find the unique label `OUTPTR:`. Insert the new source immediately before this existing label:

```asm
OUTPTR:
```

Insert:

```asm
BAKNAME:
DB 82,69,83,85,76,84,46,66,65,75,0
```

### Change 2 · `RESNAME:`

Find the unique label `RESNAME:`. Insert the new source immediately before this existing label:

```asm
RESNAME:
```

Insert:

```asm
TMPNAME:
DB 65,83,77,65,46,84,77,80,0
```

### Change 3 · `OKMSG:`

Find the unique label `OKMSG:`. Insert the new source immediately before this existing label:

```asm
OKMSG:
```

Insert:

```asm
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
```

### Change 4 · `CMDPROBE:`

Find the unique label `CMDPROBE:`. The old block below starts at that label.

Remove this existing source:

```asm
CMDPROBE:
MOV AX,0
MOV [LINENO],AX
CALL CMDINIT
CMP AX,2
JE PROBEOK
MOV AX,9
JMP ERROR
PROBEOK:
MOV AX,4C00H
INT 21H
```

Keep the following `CMDINIT:` label and the source after it in place.

### Change 5 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
CALL CMDPROBE
```

With:

```asm
CALL CMDFILES
```

## Build this stopping point

```dos
COPY A01D.ASM SOURCE.ASM
CHECK ASMKEEP
COPY RESULT.COM A01D.COM
```

Require the preceding ASM0 to report `OK 02890 bytes` and CHECK to report PASS before preserving the result. Keep the source and executable together.

## Check the addition

Create T01D.ASM:

```asm
DW 1234H
```

```dos
CHECK A01D T01D.ASM CHOSEN.COM
```

Require:

```text
OK 00002 bytes
PASS
```

VIEW.BAS must show CHOSEN.COM length 2 bytes and these complete contents:

```text
34 12
```

The file is an encoding check; inspect it rather than executing it.

Run `CHECK A01D T01D.ASM`, then `CHECK A01D T01D.ASM t01d.asm`. Each must report `ERROR 00000 CODE 9` and FAIL before a file is opened. Preserve CHOSEN.COM. With no arguments, A01D still assembles SOURCE.ASM to RESULT.COM.

Continue with [Naming the Result in the Report](../01e-reporting-the-result-name/index.html).
