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

## What this step adds

CMDFILES calls CMDINIT once. Zero names keep the known SOURCE.ASM and RESULT.COM defaults. Exactly two names are copied from the first and second CMDBUF slots into SRCNAME and RESNAME with the existing COPYZ routine. Any other count, including CMDINIT's 65535 failure value, enters ERROR with category 9.

CMDMATCH compares two complete zero-terminated spellings. SI and DI advance through the names; BX and AH are scratch. AX is one for equality and zero for inequality. A shared prefix alone is not equality. Because CMDINIT folds letters before copying, differently cased spellings of the same filename compare equal.

Five comparisons reject source=result, source=temporary, source=backup, result=temporary and result=backup. TMPNAME names ASMA.TMP; BAKNAME names RESULT.BAK. Those names are reserved now for the streamed writer and publication routines that will follow. These comparisons check selected spellings; they do not inspect or create recovery files. Existing-recovery-file detection is a later stopping point.

Remove CMDPROBE and its startup call. The retained driver calls CMDFILES after its stack check and before pass counters or file services. The helper changes the working registers, so those counters are initialized afterward. OPENFILE and WRITEOUT already use the two name-buffer addresses. Both input passes still finish before output creation.

The chosen result must also differ from the running checkpoint's executable name. Keep the builder under its own saved name. Use only unquoted 8.3 names in the current directory. This checkpoint still reports just OK and the byte count; the next step adds the result spelling to that report.


## Enter the source

Copy A01C.ASM to A01D.ASM. Apply these edits from the bottom of the old file upward. Physical positions locate the old source; the context identifies the exact edit. Keep all other source.

### Change 1

Unchanged source immediately before the edit:

```asm

RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0,0,0
```

Insert after old physical line 1207.

Insert:

```asm

BAKNAME:
DB 82,69,83,85,76,84,46,66,65,75,0
```

The following old source stays in place:

```asm

OUTPTR:
```

### Change 2

Unchanged source immediately before the edit:

```asm
SRCNAME:
DB 83,79,85,82,67,69,46,65,83,77,0,0,0
```

Insert after old physical line 1205.

Insert:

```asm
TMPNAME:
DB 65,83,77,65,46,84,77,80,0
```

The following old source stays in place:

```asm
RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0,0,0
```

### Change 3

Unchanged source immediately before the edit:

```asm
CMDBAD:
MOV AX,65535
RET
```

Insert after old physical line 1070.

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

The following old source stays in place:

```asm

OKMSG:
```

### Change 4

Unchanged source immediately before the edit:

```asm
MOV AX,4C01H
INT 21H
```

Remove old physical positions 955–966:

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

There is no replacement source.

The following old source stays in place:

```asm
CMDINIT:
MOV SI,81H
```

### Change 5

Unchanged source immediately before the edit:

```asm
MOV AX,7
JMP ERROR
ROOM:
```

Remove old physical positions 9–9:

```asm
CALL CMDPROBE
```

Replace with:

```asm
CALL CMDFILES
```

The following old source stays in place:

```asm
MOV AL,1
MOV [PASS],AL
```

## Build this stopping point

```dos
COPY A01D.ASM SOURCE.ASM
CHECK ASMKEEP
COPY RESULT.COM A01D.COM
```

Require the preceding ASM0 to report `OK 02890 bytes` and CHECK to report PASS before preserving the result. VIEW.BAS must show A01D.COM length 2890 bytes. Keep the source and executable together.

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
