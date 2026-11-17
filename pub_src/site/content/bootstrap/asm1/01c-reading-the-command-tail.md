+++
title = "03 \u00b7 Reading Names from the PSP"
weight = 3
description = "Read a bounded tail, validate 8.3 spellings and keep independent copies."
download = "A01C.ASM"
download_group = "tools/asm1"
reader_names = 1
command_examples = "literal"
url = "/bootstrap/asma0/01c-reading-the-command-tail/"
+++

The file names are still in their default buffers. I place a temporary probe call before the assembly driver so I can check the PSP reader before allowing it to open a disk file.

## What this step adds

DOS supplies a Program Segment Prefix before the program's 0100H entry. The byte at 80H is the command-tail length, and the bytes beginning at 81H are the tail itself. The program name is not part of that tail. At entry DS and ES select this same segment. CLD makes LODSB and STOSB advance their pointers.

CMDINIT sets SI to 81H and CX to the saved length. Each consumed character decrements CX. It never searches beyond that count for a zero. A length of 127 or more is rejected; the supported DOS tail is at most 126 bytes. CMDSKIP consumes spaces and tabs between names.

CMDCOUNT counts name slots as they are begun; malformed input makes the whole parse fail. CMDPTR remembers the start of the current destination slot, while DI advances through its characters. CMDBUF contains three thirteen-byte slots. The third lets the common reader retain an extra name; the assembler's later selection routine will accept exactly two or none. A fourth name is rejected before another slot can be written.

For each name BX counts characters in the current part and DX holds that part's limit: eight for the base, then three for the extension. CMDDOT permits one dot after a nonempty base, switches the limit, and requires a nonempty extension. CMDEND writes a zero and advances the saved slot pointer by thirteen. Empty parts and a second dot fail.

CMDUP folds a through z to A through Z. CMDNUM and CMDEXTRA admit digits, underscore and hyphen in addition to letters. Quotes, paths, drive colons, switches and other characters fail. A copied name is independent of the PSP bytes; later DOS operations may reuse the default disk-transfer area in that region.

On success CMDINIT returns the count in AX. On failure it returns 65535. It changes AX, BX, CX, DX, SI, DI, flags and the command storage. It is a startup operation, called once before assembly counters are initialized; CMDCOUNT starts as zero in the loaded image. Its Z labels use the branch-bridge pattern already introduced.

## The temporary startup probe

At ROOM the driver calls CMDPROBE before initializing either pass. CMDPROBE clears LINENO, calls CMDINIT and returns DOS success only for a count of two. A malformed spelling or another count enters the existing ERROR routine with category 9. PROBEOK returns DOS status zero. The probe exits through DOS rather than returning to its caller. The original driver and source parser remain below its call, ready for reuse, but are not reached at this stopping point. No file is opened or created. This two-name expectation belongs to the probe; the next step replaces its startup call and restores the no-argument defaults without retyping the driver.

Replace CHECK.BAT so it forwards the tail to its program:

```dos
ECHO OFF
IF "%1"=="" GOTO USAGE
IF NOT EXIST %1.COM GOTO MISSING
%1 %2 %3 %4 %5 %6 %7 %8 %9
IF ERRORLEVEL 1 GOTO FAIL
ECHO.
ECHO PASS
GOTO END
:FAIL
ECHO.
ECHO FAIL
GOTO END
:MISSING
ECHO Missing program
GOTO END
:USAGE
ECHO Use CHECK name [filenames]
:END
```



## Enter the source

Copy A01B.ASM to A01C.ASM. Apply these edits from the bottom of the old file upward. Physical positions locate the old source; the context identifies the exact edit. Keep all other source.

### Change 1

Unchanged source immediately before the edit:

```asm
OUTPTR:
DW 24576
```

Insert after old physical line 1093.

Insert:

```asm
CMDCOUNT:
DW 0

CMDPTR:
DW 0

CMDBUF:
DB 0,0,0,0,0,0,0,0,0,0,0,0,0
DB 0,0,0,0,0,0,0,0,0,0,0,0,0
DB 0,0,0,0,0,0,0,0,0,0,0,0,0
```

### Change 2

Unchanged source immediately before the edit:

```asm
MOV AX,4C01H
INT 21H
```

Insert after old physical line 953.

Insert:

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

CMDINIT:
MOV SI,81H
MOV DI,CMDBUF
MOV [CMDPTR],DI
MOV AL,[80H]
MOV AH,0
MOV CX,AX
CMP CX,127
JB ZCMDINIT1
JMP CMDBAD
ZCMDINIT1:
CMDSKIP:
CMP CX,0
JNE ZCMDINIT2
JMP CMDDONE
ZCMDINIT2:
LODSB
DEC CX
CMP AL,32
JE CMDSKIP
CMP AL,9
JE CMDSKIP
MOV BX,[CMDCOUNT]
CMP BX,3
JB ZCMDINIT3
JMP CMDBAD
ZCMDINIT3:
INC BX
MOV [CMDCOUNT],BX
MOV BX,0
MOV DX,8
CMDCHAR:
CMP AL,46
JNE ZCMDINIT4
JMP CMDDOT
ZCMDINIT4:
CMP AL,97
JB CMDUP
CMP AL,122
JA CMDUP
SUB AL,32
CMDUP:
CMP AL,65
JB CMDNUM
CMP AL,90
JBE CMDPUT
CMDNUM:
CMP AL,48
JB CMDEXTRA
CMP AL,57
JBE CMDPUT
CMDEXTRA:
CMP AL,95
JE CMDPUT
CMP AL,45
JE ZCMDINIT5
JMP CMDBAD
ZCMDINIT5:
CMDPUT:
INC BX
CMP BX,DX
JBE ZCMDINIT6
JMP CMDBAD
ZCMDINIT6:
STOSB
JMP CMDNEXT
CMDDOT:
CMP DX,8
JE ZCMDINIT7
JMP CMDBAD
ZCMDINIT7:
CMP BX,0
JNE ZCMDINIT8
JMP CMDBAD
ZCMDINIT8:
MOV DX,3
MOV BX,0
STOSB
CMDNEXT:
CMP CX,0
JE CMDEND
LODSB
DEC CX
CMP AL,32
JE CMDEND
CMP AL,9
JE ZCMDINIT9
JMP CMDCHAR
ZCMDINIT9:
CMDEND:
CMP BX,0
JE CMDBAD
MOV AL,0
STOSB
MOV DI,[CMDPTR]
ADD DI,13
MOV [CMDPTR],DI
JMP CMDSKIP
CMDDONE:
MOV AX,[CMDCOUNT]
RET
CMDBAD:
MOV AX,65535
RET
```

The following old source stays in place:

```asm
OKMSG:
DB 79,75,32,36
```

### Change 3

Unchanged source immediately before the edit:

```asm
MOV AX,7
JMP ERROR
ROOM:
```

Insert after old physical line 8.

Insert:

```asm
CALL CMDPROBE
```

The following old source stays in place:

```asm
MOV AL,1
MOV [PASS],AL
```

## Build this stopping point

```dos
COPY A01C.ASM SOURCE.ASM
CHECK ASMKEEP
COPY RESULT.COM A01C.COM
```

Require the preceding ASM0 to report `OK 02743 bytes` and CHECK to report PASS before preserving the result. VIEW.BAS must show A01C.COM length 2743 bytes. Keep the source and executable together.

## Check the addition

```dos
CHECK A01C in.asm out.com
```

Require PASS and no program text before it. The names need not exist: this driver makes no file calls. Repeat with tabs between the names; require PASS.

Try `CHECK A01C ONLY.ASM`, then `CHECK A01C A..ASM OUT.COM`. Each must report `ERROR 00000 CODE 9` and FAIL. The first checks the probe count; the second checks the spelling. There is no result file to inspect and no display helper to add.

Continue with [Selecting the Source and Result](../01d-selecting-the-work-files/index.html).
