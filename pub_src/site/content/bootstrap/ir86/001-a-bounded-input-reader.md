+++
title = "01 \u00b7 A bounded input reader"
weight = 1
description = "Read the selected source through the inherited block reader and checked source counters."
download = "IR01.ASM"
download_group = "tools/ir86"
reader_names = 1
aliases = ["/bootstrap/ir86/01-reading-an-ir-source/", "/bootstrap/ir86/037-iw-a-bounded-input-reader/"]
+++

The assembler already knows how to read a long source a block at a time. I want to carry that working reader into the translator. For this first stopping point, I shall strip away the assembly parser and ask the inherited file machinery to show me a short input line. There is no IR translation yet.

**Starting source:** `ASM86.ASM`. **Save as:** `IR01.ASM`. **Build with:** `ASMAKEEP.COM`.

## How it works

Read the selected source through the inherited block reader and checked source counters.

The copied source changes jobs. START keeps the full-segment stack check and calls CMDFILES and OPENFILE, then READLINE until EOF. SHOWBYTE displays each character from the completed line; TEXT supplies the line ending. CLOSEFILE finishes the input before the zero-status DOS exit. The first driver creates no output file.

Remove the assembly statement dispatcher, instruction encoders, symbol records, hash table and symbol-page allocation. They describe an assembler's work, which this reader no longer performs. The source retains the scanner, lookup, numeric, file and report helpers; the driver above uses only its reader and display path.

The reader's buffers have explicit new addresses. Keep their pointer constants together with the corresponding capacity checks:

| Offsets | Use |
|---|---|
| C800H–CBFFH | Up to 1023 physical line characters and a zero |
| CC00H–CC3FH | Up to 63 token characters and a zero |
| D000H–DFFFH | 4096-byte input block |
| E000H–EFFFH | Reserved 4096-byte output block |
| F000H–FFFFH | Stack reservation |

NEXTBYTE hands back a buffered byte or EOF. READLINE retains raw character case, normalizes line endings, and checks the physical line length and two-word source counters. The input is reopened by DOS for each new program run; there is no complete source image or allocated symbol workspace in this diagnostic.

The inherited CMDFILES routine obtains two filenames from the PSP before any DOS file operation. Its owned source/result buffers replace only the selected spellings; the streaming reader and publication routines keep their existing interfaces. With no arguments the defaults are SOURCE.IR and RESULT.ASM.

## Enter the source

Copy `ASM86.ASM` to `IR01.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `CLEANFAIL:`

Find the unique label `CLEANFAIL:`, then follow this unchanged source through its last displayed instruction:

```asm
CLEANFAIL:
```

The edit begins immediately after that unchanged block.

Remove from the following first source through the ending block below, including both boundaries and everything between them:

```asm
DB 0
PREFIX:
DB 0
```

Find the unique ending label `REGFIELD:`. The removal ends after this existing source:

```asm
REGFIELD:
```

### Change 2 · `OUTHANDLE:`

Find the unique label `OUTHANDLE:`, then follow this unchanged source through its last displayed instruction:

```asm
OUTHANDLE:
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
DW 0
ENDPC:
DW 0
SEGCODE:
```

### Change 3 · `RECOVERMSG:`

Find the unique label `RECOVERMSG:`, then follow this unchanged source through its last displayed instruction:

```asm
RECOVERMSG:
DB 82,101,99,111,118,101,114,121,58,32,105,110,115,112,101,99
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
DB 116,32,65,83,77,65,46,84,77,80,32,97,110,100,32,82
DB 69,83,85,76,84,46,66,65,75,13,10,36
```

With:

```asm
DB 116,32,73,82,84,88,46,84,77,80,32,97,110,100,32,73
DB 82,82,69,83,46,66,65,75,13,10,36
```

Keep the following `RDPOS:` label and the source after it in place.

### Change 4 · `BAKNAME:`

Find the unique label `BAKNAME:`, then follow this unchanged source through its last displayed instruction:

```asm
BAKNAME:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
DB 82,69,83,85,76,84,46,66,65,75,0
```

With:

```asm
DB 73,82,82,69,83,46,66,65,75,0
```

Keep the following `RECOVERMSG:` label and the source after it in place.

### Change 5 · `RESNAME:`

Find the unique label `RESNAME:`, then follow this unchanged source through its last displayed instruction:

```asm
RESNAME:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
DB 82,69,83,85,76,84,46,67,79,77,0,0,0
```

With:

```asm
DB 82,69,83,85,76,84,46,65,83,77,0,0,0
```

Keep the following `BAKNAME:` label and the source after it in place.

### Change 6 · `TMPNAME:`

Find the unique label `TMPNAME:`, then follow this unchanged source through its last displayed instruction:

```asm
TMPNAME:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
DB 65,83,77,65,46,84,77,80,0
```

With:

```asm
DB 73,82,84,88,46,84,77,80,0
```

Keep the following `RESNAME:` label and the source after it in place.

### Change 7 · `SRCNAME:`

Find the unique label `SRCNAME:`, then follow this unchanged source through its last displayed instruction:

```asm
SRCNAME:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
DB 83,79,85,82,67,69,46,65,83,77,0,0,0
```

With:

```asm
DB 83,79,85,82,67,69,46,73,82,0,0,0,0
```

Keep the following `TMPNAME:` label and the source after it in place.

### Change 8 · `REGTAB:`

Find the unique label `REGTAB:`. The old block below starts at that label.

Remove from the following first source through the ending block below, including both boundaries and everything between them:

```asm
REGTAB:
DB 65,76,0,0
DB 67,76,0,1
```

Find the unique ending label `OPTAB:`. The removal ends after this existing source:

```asm
OPTAB:
DB 68,66,0,0,0,0,1,0
DB 68,87,0,0,0,0,1,1
DB 82,69,84,0,0,0,2,195
DB 67,76,68,0,0,0,2,252
DB 76,79,68,83,66,0,2,172
DB 83,84,79,83,66,0,2,170
DB 77,79,86,0,0,0,3,0
DB 65,68,68,0,0,0,4,0
DB 79,82,0,0,0,0,4,1
DB 65,78,68,0,0,0,4,4
DB 83,85,66,0,0,0,4,5
DB 67,77,80,0,0,0,4,7
DB 73,78,67,0,0,0,5,64
DB 68,69,67,0,0,0,5,72
DB 80,85,83,72,0,0,5,80
DB 80,79,80,0,0,0,5,88
DB 73,78,84,0,0,0,6,205
DB 67,65,76,76,0,0,7,232
DB 74,77,80,0,0,0,7,233
DB 74,66,0,0,0,0,8,114
DB 74,65,69,0,0,0,8,115
DB 74,69,0,0,0,0,8,116
DB 74,78,69,0,0,0,8,117
DB 74,66,69,0,0,0,8,118
DB 74,65,0,0,0,0,8,119
DB 88,79,82,0,0,0,4,6
DB 82,69,83,66,0,0,12,0
DB 82,69,83,87,0,0,12,1
DB 76,69,65,0,0,0,11,0
DB 77,85,76,0,0,0,9,4
DB 68,73,86,0,0,0,9,6
DB 83,72,76,0,0,0,10,4
DB 83,72,82,0,0,0,10,5
DB 74,67,0,0,0,0,8,114
```

Keep the following `SRCNAME:` label and the source after it in place.

### Change 9 · `TYPE:`

Find the unique label `TYPE:`. The old block below starts at that label.

Remove this existing source:

```asm
TYPE:
DB 0
OP:
DB 0
KIND:
DB 0
WIDTH:
DB 0
REG:
DB 0
K1:
DB 0
W1:
DB 0
R1:
DB 0
```

Keep the following `ERRCODE:` label and the source after it in place.

### Change 10 · `VAL:`

Find the unique label `VAL:`. The old block below starts at that label.

Remove this existing source:

```asm
VAL:
DW 0
V1:
DW 0
PASS:
DB 1
```

Keep the following `ENDED:` label and the source after it in place.

### Change 11 · `LINENO:`

Find the unique label `LINENO:`, then follow this unchanged source through its last displayed instruction:

```asm
LINENO:
DW 0
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
PC:
DW 256
SYMC:
DW 0
```

Keep the following `TOKLEN:` label and the source after it in place.

### Change 12 · `ERRMSG:`

Find the unique label `ERRMSG:`, then follow this unchanged source through its last displayed instruction:

```asm
ERRMSG:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
DB 69,82,82,79,82,32,36
```

With:

```asm
DB 73,82,32,69,82,82,79,82,32,36
```

Keep the following `CODEMSG:` label and the source after it in place.

### Change 13 · `OKMSG:`

Find the unique label `OKMSG:`. The old block below starts at that label.

Remove this existing source:

```asm
OKMSG:
DB 79,75,32,36
BYTEMSG:
DB 32,98,121,116,101,115,13,10,36
```

Keep the following `ERRMSG:` label and the source after it in place.

### Change 14 · `CMDTEXT:`

Find the unique label `CMDTEXT:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDTEXT:
LODSB
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE CMDTEXTEND
```

With:

```asm
JE NEAR CMDTEXTEND
```

### Change 15 · `ZCMDFILES4:`

Find the unique label `ZCMDFILES4:`, then follow this unchanged source through its last displayed instruction:

```asm
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
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE CMDFAIL
```

With:

```asm
JNE NEAR CMDFAIL
```

Keep the following `CMDREADY:` label and the source after it in place.

### Change 16 · `ZCMDFILES4:`

Find the unique label `ZCMDFILES4:`, then follow this unchanged source through its last displayed instruction:

```asm
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
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE CMDFAIL
```

With:

```asm
JNE NEAR CMDFAIL
```

### Change 17 · `ZCMDFILES4:`

Find the unique label `ZCMDFILES4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCMDFILES4:
MOV SI,SRCNAME
MOV DI,BAKNAME
CALL CMDMATCH
CMP AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE CMDFAIL
```

With:

```asm
JNE NEAR CMDFAIL
```

### Change 18 · `ZCMDFILES3:`

Find the unique label `ZCMDFILES3:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCMDFILES3:
MOV SI,SRCNAME
MOV DI,TMPNAME
CALL CMDMATCH
CMP AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE ZCMDFILES4
JMP CMDFAIL
ZCMDFILES4:
```

With:

```asm
JNE NEAR CMDFAIL
```

### Change 19 · `ZCMDFILES2:`

Find the unique label `ZCMDFILES2:`, then follow this unchanged source through its last displayed instruction:

```asm
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
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE ZCMDFILES3
JMP CMDFAIL
ZCMDFILES3:
```

With:

```asm
JNE NEAR CMDFAIL
```

### Change 20 · `ZCMDFILES1:`

Find the unique label `ZCMDFILES1:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCMDFILES1:
CMP AX,2
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE ZCMDFILES2
JMP CMDFAIL
ZCMDFILES2:
```

With:

```asm
JNE NEAR CMDFAIL
```

### Change 21 · `CMDFILES:`

Find the unique label `CMDFILES:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDFILES:
CALL CMDINIT
CMP AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZCMDFILES1
JMP CMDREADY
ZCMDFILES1:
```

With:

```asm
JE NEAR CMDREADY
```

### Change 22 · `CMDMATCH:`

Find the unique label `CMDMATCH:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDMATCH:
LODSB
MOV BX,DI
MOV AH,[BX]
CMP AL,AH
JNE CMDNO
INC DI
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE CMDMATCH
```

With:

```asm
JNE NEAR CMDMATCH
```

### Change 23 · `CMDMATCH:`

Find the unique label `CMDMATCH:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDMATCH:
LODSB
MOV BX,DI
MOV AH,[BX]
CMP AL,AH
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE CMDNO
```

With:

```asm
JNE NEAR CMDNO
```

### Change 24 · `CMDEND:`

Find the unique label `CMDEND:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDEND:
CMP BX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE CMDBAD
```

With:

```asm
JE NEAR CMDBAD
```

### Change 25 · `CMDNEXT:`

Find the unique label `CMDNEXT:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDNEXT:
CMP CX,0
JE CMDEND
LODSB
DEC CX
CMP AL,32
JE CMDEND
CMP AL,9
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE ZCMDINIT9
JMP CMDCHAR
ZCMDINIT9:
```

With:

```asm
JNE NEAR CMDCHAR
```

Keep the following `CMDEND:` label and the source after it in place.

### Change 26 · `CMDNEXT:`

Find the unique label `CMDNEXT:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDNEXT:
CMP CX,0
JE CMDEND
LODSB
DEC CX
CMP AL,32
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE CMDEND
```

With:

```asm
JE NEAR CMDEND
```

### Change 27 · `CMDNEXT:`

Find the unique label `CMDNEXT:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDNEXT:
CMP CX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE CMDEND
```

With:

```asm
JE NEAR CMDEND
```

### Change 28 · `ZCMDINIT7:`

Find the unique label `ZCMDINIT7:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCMDINIT7:
CMP BX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZCMDINIT8
JMP CMDBAD
ZCMDINIT8:
```

With:

```asm
JE NEAR CMDBAD
```

### Change 29 · `CMDDOT:`

Find the unique label `CMDDOT:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDDOT:
CMP DX,8
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE ZCMDINIT7
JMP CMDBAD
ZCMDINIT7:
```

With:

```asm
JNE NEAR CMDBAD
```

### Change 30 · `CMDPUT:`

Find the unique label `CMDPUT:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDPUT:
INC BX
CMP BX,DX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JBE ZCMDINIT6
JMP CMDBAD
ZCMDINIT6:
```

With:

```asm
JA NEAR CMDBAD
```

### Change 31 · `CMDEXTRA:`

Find the unique label `CMDEXTRA:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDEXTRA:
CMP AL,95
JE CMDPUT
CMP AL,45
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE ZCMDINIT5
JMP CMDBAD
ZCMDINIT5:
```

With:

```asm
JNE NEAR CMDBAD
```

Keep the following `CMDPUT:` label and the source after it in place.

### Change 32 · `CMDEXTRA:`

Find the unique label `CMDEXTRA:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDEXTRA:
CMP AL,95
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE CMDPUT
```

With:

```asm
JE NEAR CMDPUT
```

### Change 33 · `CMDNUM:`

Find the unique label `CMDNUM:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDNUM:
CMP AL,48
JB CMDEXTRA
CMP AL,57
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JBE CMDPUT
```

With:

```asm
JBE NEAR CMDPUT
```

Keep the following `CMDEXTRA:` label and the source after it in place.

### Change 34 · `CMDNUM:`

Find the unique label `CMDNUM:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDNUM:
CMP AL,48
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB CMDEXTRA
```

With:

```asm
JB NEAR CMDEXTRA
```

### Change 35 · `CMDUP:`

Find the unique label `CMDUP:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDUP:
CMP AL,65
JB CMDNUM
CMP AL,90
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JBE CMDPUT
```

With:

```asm
JBE NEAR CMDPUT
```

Keep the following `CMDNUM:` label and the source after it in place.

### Change 36 · `CMDUP:`

Find the unique label `CMDUP:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDUP:
CMP AL,65
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB CMDNUM
```

With:

```asm
JB NEAR CMDNUM
```

### Change 37 · `ZCMDINIT4:`

Find the unique label `ZCMDINIT4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCMDINIT4:
CMP AL,97
JB CMDUP
CMP AL,122
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JA CMDUP
```

With:

```asm
JA NEAR CMDUP
```

### Change 38 · `ZCMDINIT4:`

Find the unique label `ZCMDINIT4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCMDINIT4:
CMP AL,97
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB CMDUP
```

With:

```asm
JB NEAR CMDUP
```

### Change 39 · `CMDCHAR:`

Find the unique label `CMDCHAR:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDCHAR:
CMP AL,46
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZCMDINIT4
JMP CMDDOT
ZCMDINIT4:
```

With:

```asm
JE NEAR CMDDOT
```

### Change 40 · `ZCMDINIT2:`

Find the unique label `ZCMDINIT2:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCMDINIT2:
LODSB
DEC CX
CMP AL,32
JE CMDSKIP
CMP AL,9
JE CMDSKIP
MOV BX,[CMDCOUNT]
CMP BX,3
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB ZCMDINIT3
JMP CMDBAD
ZCMDINIT3:
```

With:

```asm
JAE NEAR CMDBAD
```

### Change 41 · `ZCMDINIT2:`

Find the unique label `ZCMDINIT2:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCMDINIT2:
LODSB
DEC CX
CMP AL,32
JE CMDSKIP
CMP AL,9
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE CMDSKIP
```

With:

```asm
JE NEAR CMDSKIP
```

### Change 42 · `ZCMDINIT2:`

Find the unique label `ZCMDINIT2:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCMDINIT2:
LODSB
DEC CX
CMP AL,32
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE CMDSKIP
```

With:

```asm
JE NEAR CMDSKIP
```

### Change 43 · `CMDSKIP:`

Find the unique label `CMDSKIP:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDSKIP:
CMP CX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZCMDINIT2
JMP CMDDONE
ZCMDINIT2:
```

With:

```asm
JE NEAR CMDDONE
```

### Change 44 · `CMDINIT:`

Find the unique label `CMDINIT:`, then follow this unchanged source through its last displayed instruction:

```asm
CMDINIT:
MOV SI,81H
MOV DI,CMDBUF
MOV [CMDPTR],DI
MOV AL,[80H]
MOV AH,0
MOV CX,AX
CMP CX,127
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB ZCMDINIT1
JMP CMDBAD
ZCMDINIT1:
```

With:

```asm
JAE NEAR CMDBAD
```

Keep the following `CMDSKIP:` label and the source after it in place.

### Change 45 · `ATOM:`

Find the unique label `ATOM:`. The old block below starts at that label.

Remove from the following first source through the ending block below, including both boundaries and everything between them:

```asm
ATOM:
MOV AL,[0CC00H]
CMP AL,48
```

Find the unique ending label `SHIFTRANGE:`. The removal ends after this existing source:

```asm
SHIFTRANGE:
MOV AX,4
JMP ERROR
```

Keep the following `CMDINIT:` label and the source after it in place.

### Change 46 · `N32DIGIT:`

Find the unique label `N32DIGIT:`, then follow this unchanged source through its last displayed instruction:

```asm
N32DIGIT:
MOV DL,CL
ADD DL,48
MOV AH,2
INT 21H
ADD SI,4
CMP SI,DIV32END
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE ZNUMBER323
JMP N32PLACE
ZNUMBER323:
```

With:

```asm
JB NEAR N32PLACE
```

### Change 47 · `N32TAKE:`

Find the unique label `N32TAKE:`, then follow this unchanged source through its last displayed instruction:

```asm
N32TAKE:
MOV AX,[N32LO]
MOV DX,[D32LO]
SUB AX,DX
MOV [N32LO],AX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE N32NOBORROW
```

With:

```asm
JAE NEAR N32NOBORROW
```

### Change 48 · `ZNUMBER321:`

Find the unique label `ZNUMBER321:`, then follow this unchanged source through its last displayed instruction:

```asm
ZNUMBER321:
JA N32TAKE
MOV AX,[N32LO]
MOV DX,[D32LO]
CMP AX,DX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE ZNUMBER322
JMP N32DIGIT
ZNUMBER322:
```

With:

```asm
JB NEAR N32DIGIT
```

Keep the following `N32TAKE:` label and the source after it in place.

### Change 49 · `N32SUB:`

Find the unique label `N32SUB:`, then follow this unchanged source through its last displayed instruction:

```asm
N32SUB:
MOV AX,[N32HI]
MOV DX,[D32HI]
CMP AX,DX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE ZNUMBER321
JMP N32DIGIT
ZNUMBER321:
JA N32TAKE
```

With:

```asm
JB NEAR N32DIGIT
JA NEAR N32TAKE
```

### Change 50 · `COUNTINPUT:`

Find the unique label `COUNTINPUT:`, then follow this unchanged source through its last displayed instruction:

```asm
COUNTINPUT:
MOV AX,[INBYTES]
CMP AX,0FFFFH
JNE INPUTLOW
MOV AX,[INBYTEHI]
CMP AX,0FFFFH
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE COUNTFULL
```

With:

```asm
JE NEAR COUNTFULL
```

### Change 51 · `COUNTINPUT:`

Find the unique label `COUNTINPUT:`, then follow this unchanged source through its last displayed instruction:

```asm
COUNTINPUT:
MOV AX,[INBYTES]
CMP AX,0FFFFH
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE INPUTLOW
```

With:

```asm
JNE NEAR INPUTLOW
```

### Change 52 · `COUNTLINE:`

Find the unique label `COUNTLINE:`, then follow this unchanged source through its last displayed instruction:

```asm
COUNTLINE:
MOV AX,[LINENO]
CMP AX,0FFFFH
JNE LINELOW
MOV AX,[LINEHI]
CMP AX,0FFFFH
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE COUNTFULL
```

With:

```asm
JE NEAR COUNTFULL
```

### Change 53 · `COUNTLINE:`

Find the unique label `COUNTLINE:`, then follow this unchanged source through its last displayed instruction:

```asm
COUNTLINE:
MOV AX,[LINENO]
CMP AX,0FFFFH
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE LINELOW
```

With:

```asm
JNE NEAR LINELOW
```

### Change 54 · `CLEANEND:`

Find the unique label `CLEANEND:`, then follow this unchanged source through its last displayed instruction:

```asm
CLEANEND:
```

The edit begins immediately after that unchanged block.

Remove from the following first source through the ending block below, including both boundaries and everything between them:

```asm
CALL MEMFREE
RET
MEMINIT:
```

Find the unique ending label `DEFINITIONCLEAR:`. The removal ends after this existing source:

```asm
DEFINITIONCLEAR:
STOSB
DEC CX
JNE DEFINITIONCLEAR
MOV DI,[RECORDPTR]
PUSH SI
MOV SI,0CC00H
CALL COPYZ
POP SI
MOV BX,[RECORDPTR]
ADD BX,32
MOV AX,[DEFVALUE]
MOV ES:[BX],AX
ADD BX,2
MOV AX,[HEADID]
MOV ES:[BX],AX
ADD BX,4
MOV AX,[DEFTYPE]
MOV ES:[BX],AX
MOV AX,[HASHSEG]
MOV ES,AX
MOV BX,[BUCKET]
MOV AX,[SYMID]
MOV ES:[BX],AX
```

### Change 55 · `CLEANTEMP:`

Find the unique label `CLEANTEMP:`, then follow this unchanged source through its last displayed instruction:

```asm
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
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE CLEANEND
```

With:

```asm
JAE NEAR CLEANEND
```

### Change 56 · `CLEANTEMP:`

Find the unique label `CLEANTEMP:`, then follow this unchanged source through its last displayed instruction:

```asm
CLEANTEMP:
MOV AL,[OWNTMP]
CMP AL,0
JE CLEANEND
MOV AL,[KEEPFILES]
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE CLEANEND
```

With:

```asm
JNE NEAR CLEANEND
```

### Change 57 · `CLEANTEMP:`

Find the unique label `CLEANTEMP:`, then follow this unchanged source through its last displayed instruction:

```asm
CLEANTEMP:
MOV AL,[OWNTMP]
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE CLEANEND
```

With:

```asm
JE NEAR CLEANEND
```

### Change 58 · `CLEANOUTPUT:`

Find the unique label `CLEANOUTPUT:`, then follow this unchanged source through its last displayed instruction:

```asm
CLEANOUTPUT:
MOV AL,[OUTOPEN]
CMP AL,0
JE CLEANTEMP
MOV BX,[OUTHANDLE]
MOV AH,3EH
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE CLEANTEMP
```

With:

```asm
JAE NEAR CLEANTEMP
```

### Change 59 · `CLEANOUTPUT:`

Find the unique label `CLEANOUTPUT:`, then follow this unchanged source through its last displayed instruction:

```asm
CLEANOUTPUT:
MOV AL,[OUTOPEN]
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE CLEANTEMP
```

With:

```asm
JE NEAR CLEANTEMP
```

### Change 60 · `CLEANUP:`

Find the unique label `CLEANUP:`, then follow this unchanged source through its last displayed instruction:

```asm
CLEANUP:
MOV AL,[INOPEN]
CMP AL,0
JE CLEANOUTPUT
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE CLEANOUTPUT
```

With:

```asm
JAE NEAR CLEANOUTPUT
```

### Change 61 · `CLEANUP:`

Find the unique label `CLEANUP:`, then follow this unchanged source through its last displayed instruction:

```asm
CLEANUP:
MOV AL,[INOPEN]
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE CLEANOUTPUT
```

With:

```asm
JE NEAR CLEANOUTPUT
```

### Change 62 · `PUBLISHED:`

Find the unique label `PUBLISHED:`, then follow this unchanged source through its last displayed instruction:

```asm
PUBLISHED:
MOV AL,0
MOV [OWNTMP],AL
MOV AL,[HAVEBAK]
CMP AL,0
JE COMMITDONE
MOV DX,BAKNAME
MOV AH,41H
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE BACKREMOVED
```

With:

```asm
JAE NEAR BACKREMOVED
```

### Change 63 · `PUBLISHED:`

Find the unique label `PUBLISHED:`, then follow this unchanged source through its last displayed instruction:

```asm
PUBLISHED:
MOV AL,0
MOV [OWNTMP],AL
MOV AL,[HAVEBAK]
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE COMMITDONE
```

With:

```asm
JE NEAR COMMITDONE
```

### Change 64 · `ZCOMMIT1:`

Find the unique label `ZCOMMIT1:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCOMMIT1:
MOV AL,[HAVEBAK]
CMP AL,0
JE PUBLISHFAIL
MOV DX,BAKNAME
MOV DI,RESNAME
MOV AH,56H
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE RESTORED
```

With:

```asm
JAE NEAR RESTORED
```

### Change 65 · `ZCOMMIT1:`

Find the unique label `ZCOMMIT1:`, then follow this unchanged source through its last displayed instruction:

```asm
ZCOMMIT1:
MOV AL,[HAVEBAK]
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE PUBLISHFAIL
```

With:

```asm
JE NEAR PUBLISHFAIL
```

### Change 66 · `PUBLISH:`

Find the unique label `PUBLISH:`, then follow this unchanged source through its last displayed instruction:

```asm
PUBLISH:
MOV DX,TMPNAME
MOV DI,RESNAME
MOV AH,56H
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB ZCOMMIT1
JMP PUBLISHED
ZCOMMIT1:
```

With:

```asm
JAE NEAR PUBLISHED
```

### Change 67 · `COMMIT:`

Find the unique label `COMMIT:`, then follow this unchanged source through its last displayed instruction:

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
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE BACKEDUP
```

With:

```asm
JAE NEAR BACKEDUP
```

### Change 68 · `COMMIT:`

Find the unique label `COMMIT:`, then follow this unchanged source through its last displayed instruction:

```asm
COMMIT:
MOV DX,RESNAME
CALL EXISTS
CMP AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE PUBLISH
```

With:

```asm
JE NEAR PUBLISH
```

### Change 69 · `PREFLIGHT:`

Find the unique label `PREFLIGHT:`, then follow this unchanged source through its last displayed instruction:

```asm
PREFLIGHT:
MOV DX,TMPNAME
CALL EXISTS
CMP AX,0
JNE NAMEBUSY
MOV DX,BAKNAME
CALL EXISTS
CMP AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE PREFLIGHTOK
```

With:

```asm
JE NEAR PREFLIGHTOK
```

Keep the following `NAMEBUSY:` label and the source after it in place.

### Change 70 · `PREFLIGHT:`

Find the unique label `PREFLIGHT:`, then follow this unchanged source through its last displayed instruction:

```asm
PREFLIGHT:
MOV DX,TMPNAME
CALL EXISTS
CMP AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE NAMEBUSY
```

With:

```asm
JNE NEAR NAMEBUSY
```

### Change 71 · `FILEEXISTS:`

Find the unique label `FILEEXISTS:`, then follow this unchanged source through its last displayed instruction:

```asm
FILEEXISTS:
MOV BX,AX
MOV AH,3EH
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE EXISTSCLOSED
```

With:

```asm
JAE NEAR EXISTSCLOSED
```

### Change 72 · `FLUSHDONE:`

Find the unique label `FLUSHDONE:`, then follow this unchanged source through its last displayed instruction:

```asm
FLUSHDONE:
POP DX
POP CX
POP BX
POP AX
RET
EXISTS:
MOV AX,3D00H
INT 21H
JAE FILEEXISTS
CMP AX,2
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE FILENONE
```

With:

```asm
JE NEAR FILENONE
```

### Change 73 · `FLUSHDONE:`

Find the unique label `FLUSHDONE:`, then follow this unchanged source through its last displayed instruction:

```asm
FLUSHDONE:
POP DX
POP CX
POP BX
POP AX
RET
EXISTS:
MOV AX,3D00H
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE FILEEXISTS
```

With:

```asm
JAE NEAR FILEEXISTS
```

### Change 74 · `CREATEOUT:`

Find the unique label `CREATEOUT:`. The old block below starts at that label.

Remove from the following first source through the ending block below, including both boundaries and everything between them:

```asm
CREATEOUT:
MOV DX,TMPNAME
MOV CX,0
```

Find the unique ending label `FLUSHDONE:`. The removal ends after this existing source:

```asm
FLUSHDONE:
POP DX
POP CX
POP BX
POP AX
RET
```

Keep the following `EXISTS:` label and the source after it in place.

### Change 75 · `ERROR:`

Find the unique label `ERROR:`, then follow this unchanged source through its last displayed instruction:

```asm
ERROR:
MOV [ERRCODE],AL
CALL CLEANUP
MOV DX,ERRMSG
CALL TEXT
MOV AX,[LINENO]
MOV DX,[LINEHI]
CALL NUMBER32
MOV DX,CODEMSG
CALL TEXT
MOV AL,[ERRCODE]
ADD AL,48
MOV DL,AL
MOV AH,2
INT 21H
MOV DX,NEWLINE
CALL TEXT
MOV AL,[CLEANFAIL]
MOV DL,[KEEPFILES]
OR AL,DL
MOV DL,[HAVEBAK]
OR AL,DL
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE ERROREXIT
```

With:

```asm
JE NEAR ERROREXIT
```

### Change 76 · `PRINTDIGIT:`

Find the unique label `PRINTDIGIT:`, then follow this unchanged source through its last displayed instruction:

```asm
PRINTDIGIT:
MOV DL,AL
MOV AH,2
INT 21H
ADD SI,2
CMP SI,DIVEND
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB NEXTPLACE
```

With:

```asm
JB NEAR NEXTPLACE
```

### Change 77 · `SUBTRACT:`

Find the unique label `SUBTRACT:`, then follow this unchanged source through its last displayed instruction:

```asm
SUBTRACT:
CMP CX,DX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB PRINTDIGIT
```

With:

```asm
JB NEAR PRINTDIGIT
```

### Change 78 · `COPYZ:`

Find the unique label `COPYZ:`, then follow this unchanged source through its last displayed instruction:

```asm
COPYZ:
LODSB
STOSB
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE COPYZ
```

With:

```asm
JNE NEAR COPYZ
```

### Change 79 · `FINISHED:`

Find the unique label `FINISHED:`, then follow this unchanged source through its last displayed instruction:

```asm
FINISHED:
```

The edit begins immediately after that unchanged block.

Remove from the following first source through the ending block below, including both boundaries and everything between them:

```asm
RET
TWOOPERANDS:
CALL OPERAND
```

Find the unique ending label `COUNTBYTE:`. The removal ends after this existing source:

```asm
COUNTBYTE:
MOV BX,[PC]
INC BX
MOV [PC],BX
POP BX
POP AX
```

### Change 80 · `FINISH:`

Find the unique label `FINISH:`, then follow this unchanged source through its last displayed instruction:

```asm
FINISH:
CALL SCAN
MOV AL,[0CC00H]
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE FINISHED
```

With:

```asm
JE NEAR FINISHED
```

### Change 81 · `VALUEBAD:`

Find the unique label `VALUEBAD:`, then follow this unchanged source through its last displayed instruction:

```asm
VALUEBAD:
MOV AX,3
JMP ERROR
```

The edit begins immediately after that unchanged block.

Remove from the following first source through the ending block below, including both boundaries and everything between them:

```asm
DEFINE:
CALL VALIDNAME
CALL REGISTER
```

Find the unique ending label `SHORTOK:`. The removal ends after this existing source:

```asm
SHORTOK:
PUSH AX
MOV AL,[OP]
CALL EMIT
POP AX
CALL EMIT
JMP FINISH
```

Keep the following `FINISH:` label and the source after it in place.

### Change 82 · `EXPRESSIONADD:`

Find the unique label `EXPRESSIONADD:`. The old block below starts at that label.

Remove from the following first source through the ending block below, including both boundaries and everything between them:

```asm
EXPRESSIONADD:
POP AX
CALL SCAN
```

Find the unique ending label `VALUEBAD:`. The removal ends after this existing source:

```asm
VALUEBAD:
MOV AX,3
```

With:

```asm
NUMBERBAD:
MOV AX,2
```

### Change 83 · `EXPRESSIONLOOP:`

Find the unique label `EXPRESSIONLOOP:`, then follow this unchanged source through its last displayed instruction:

```asm
EXPRESSIONLOOP:
PUSH AX
PUSH SI
CALL SCAN
MOV AL,[0CC00H]
CMP AL,43
JE EXPRESSIONADD
CMP AL,45
JE EXPRESSIONSUB
POP SI
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
POP AX
```

### Change 84 · `EXPRESSIONLOOP:`

Find the unique label `EXPRESSIONLOOP:`, then follow this unchanged source through its last displayed instruction:

```asm
EXPRESSIONLOOP:
PUSH AX
PUSH SI
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
CALL SCAN
MOV AL,[0CC00H]
CMP AL,43
JE EXPRESSIONADD
CMP AL,45
JE EXPRESSIONSUB
```

With:

```asm
MOV SI,0CC00H
MOV DI,[TOKLEN]
ADD DI,0CC00H
MOV BX,DI
DEC BX
MOV AL,[BX]
MOV BP,10
CMP AL,72
JNE NEAR NUMBERSTART
MOV BP,16
DEC DI
NUMBERSTART:
CMP SI,DI
JE NEAR NUMBERBAD
MOV CX,0
DIGIT:
LODSB
SUB AL,48
CMP AL,9
JBE NEAR DIGITOK
SUB AL,7
CMP AL,10
JB NEAR NUMBERBAD
CMP AL,15
JA NEAR NUMBERBAD
DIGITOK:
MOV AH,0
MOV DX,AX
CMP DX,BP
JAE NEAR NUMBERBAD
CMP BP,16
JE NEAR HEXDIGIT
CMP CX,6553
JA NEAR NUMBERBAD
JB NEAR DECDIGIT
CMP DX,5
JA NEAR NUMBERBAD
DECDIGIT:
MOV AX,CX
ADD CX,CX
ADD AX,AX
ADD AX,AX
ADD AX,AX
ADD CX,AX
JMP ADDDIGIT
HEXDIGIT:
CMP CX,4095
JA NEAR NUMBERBAD
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADDDIGIT:
ADD CX,DX
CMP SI,DI
JB NEAR DIGIT
MOV AX,CX
```

### Change 85 · `VALUE:`

Find the unique label `VALUE:`. The old block below starts at that label.

Replace this existing source:

```asm
VALUE:
CALL FACTOR
EXPRESSIONLOOP:
PUSH AX
```

With:

```asm
ATOM:
MOV AL,[0CC00H]
CMP AL,48
JB NEAR WORDVALUE
CMP AL,57
JBE NEAR LITERAL
WORDVALUE:
JMP NUMBERBAD
LITERAL:
```

### Change 86 · `NAMEVALID:`

Find the unique label `NAMEVALID:`, then follow this unchanged source through its last displayed instruction:

```asm
NAMEVALID:
LODSB
CMP AL,0
JE NAMEVALIDEND
CMP AL,95
JE NAMEVALID
CMP AL,48
JB SYMBOLBAD
CMP AL,57
JBE NAMEVALID
CMP AL,65
JB SYMBOLBAD
CMP AL,90
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JBE NAMEVALID
```

With:

```asm
JBE NEAR NAMEVALID
```

### Change 87 · `NAMEVALID:`

Find the unique label `NAMEVALID:`, then follow this unchanged source through its last displayed instruction:

```asm
NAMEVALID:
LODSB
CMP AL,0
JE NAMEVALIDEND
CMP AL,95
JE NAMEVALID
CMP AL,48
JB SYMBOLBAD
CMP AL,57
JBE NAMEVALID
CMP AL,65
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB SYMBOLBAD
```

With:

```asm
JB NEAR SYMBOLBAD
```

### Change 88 · `NAMEVALID:`

Find the unique label `NAMEVALID:`, then follow this unchanged source through its last displayed instruction:

```asm
NAMEVALID:
LODSB
CMP AL,0
JE NAMEVALIDEND
CMP AL,95
JE NAMEVALID
CMP AL,48
JB SYMBOLBAD
CMP AL,57
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JBE NAMEVALID
```

With:

```asm
JBE NEAR NAMEVALID
```

### Change 89 · `NAMEVALID:`

Find the unique label `NAMEVALID:`, then follow this unchanged source through its last displayed instruction:

```asm
NAMEVALID:
LODSB
CMP AL,0
JE NAMEVALIDEND
CMP AL,95
JE NAMEVALID
CMP AL,48
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB SYMBOLBAD
```

With:

```asm
JB NEAR SYMBOLBAD
```

### Change 90 · `NAMEVALID:`

Find the unique label `NAMEVALID:`, then follow this unchanged source through its last displayed instruction:

```asm
NAMEVALID:
LODSB
CMP AL,0
JE NAMEVALIDEND
CMP AL,95
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE NAMEVALID
```

With:

```asm
JE NEAR NAMEVALID
```

### Change 91 · `NAMEVALID:`

Find the unique label `NAMEVALID:`, then follow this unchanged source through its last displayed instruction:

```asm
NAMEVALID:
LODSB
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE NAMEVALIDEND
```

With:

```asm
JE NEAR NAMEVALIDEND
```

### Change 92 · `ZVALIDNAM1:`

Find the unique label `ZVALIDNAM1:`, then follow this unchanged source through its last displayed instruction:

```asm
ZVALIDNAM1:
CMP AL,90
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JBE ZVALIDNAM2
JMP SYMBOLBAD
ZVALIDNAM2:
```

With:

```asm
JA NEAR SYMBOLBAD
```

Keep the following `NAMEVALID:` label and the source after it in place.

### Change 93 · `NAMELIMIT:`

Find the unique label `NAMELIMIT:`, then follow this unchanged source through its last displayed instruction:

```asm
NAMELIMIT:
PUSH SI
MOV SI,0CC00H
LODSB
CMP AL,95
JE NAMEVALID
CMP AL,65
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE ZVALIDNAM1
JMP SYMBOLBAD
ZVALIDNAM1:
```

With:

```asm
JB NEAR SYMBOLBAD
```

### Change 94 · `NAMELIMIT:`

Find the unique label `NAMELIMIT:`, then follow this unchanged source through its last displayed instruction:

```asm
NAMELIMIT:
PUSH SI
MOV SI,0CC00H
LODSB
CMP AL,95
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE NAMEVALID
```

With:

```asm
JE NEAR NAMEVALID
```

### Change 95 · `VALIDNAME:`

Find the unique label `VALIDNAME:`, then follow this unchanged source through its last displayed instruction:

```asm
VALIDNAME:
MOV AX,[TOKLEN]
CMP AX,31
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JBE NAMELIMIT
```

With:

```asm
JBE NEAR NAMELIMIT
```

### Change 96 · `LOOKMISS:`

Find the unique label `LOOKMISS:`, then follow this unchanged source through its last displayed instruction:

```asm
LOOKMISS:
MOV BX,0
POP SI
RET
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
REGISTER:
MOV BX,REGTAB
MOV CX,20
MOV AX,4
CALL LOOK
CMP BX,0
JE NOREGISTER
ADD BX,3
MOV AL,[BX]
MOV AH,0
RET
NOREGISTER:
MOV AX,0FFFFH
RET
```

Keep the following `VALIDNAME:` label and the source after it in place.

### Change 97 · `LOOKCHAR:`

Find the unique label `LOOKCHAR:`, then follow this unchanged source through its last displayed instruction:

```asm
LOOKCHAR:
LODSB
MOV BX,DI
MOV DL,[BX]
CMP AL,DL
JNE LOOKSTEP
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE LOOKFOUND
```

With:

```asm
JE NEAR LOOKFOUND
```

### Change 98 · `LOOKCHAR:`

Find the unique label `LOOKCHAR:`, then follow this unchanged source through its last displayed instruction:

```asm
LOOKCHAR:
LODSB
MOV BX,DI
MOV DL,[BX]
CMP AL,DL
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE LOOKSTEP
```

With:

```asm
JNE NEAR LOOKSTEP
```

### Change 99 · `LOOKNEXT:`

Find the unique label `LOOKNEXT:`, then follow this unchanged source through its last displayed instruction:

```asm
LOOKNEXT:
CMP CX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZLOOK1
JMP LOOKMISS
ZLOOK1:
```

With:

```asm
JE NEAR LOOKMISS
```

### Change 100 · `ZSCAN4:`

Find the unique label `ZSCAN4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZSCAN4:
CMP AL,58
JE SEPARATORRET
CMP AL,91
JE SEPARATORRET
CMP AL,93
JE SEPARATORRET
CMP AL,43
JE SEPARATORRET
CMP AL,45
JE SEPARATORRET
CMP AL,40
JE SEPARATORRET
CMP AL,41
JE SEPARATORRET
CMP AL,34
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SEPARATORRET
```

With:

```asm
JE NEAR SEPARATORRET
```

### Change 101 · `ZSCAN4:`

Find the unique label `ZSCAN4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZSCAN4:
CMP AL,58
JE SEPARATORRET
CMP AL,91
JE SEPARATORRET
CMP AL,93
JE SEPARATORRET
CMP AL,43
JE SEPARATORRET
CMP AL,45
JE SEPARATORRET
CMP AL,40
JE SEPARATORRET
CMP AL,41
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SEPARATORRET
```

With:

```asm
JE NEAR SEPARATORRET
```

### Change 102 · `ZSCAN4:`

Find the unique label `ZSCAN4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZSCAN4:
CMP AL,58
JE SEPARATORRET
CMP AL,91
JE SEPARATORRET
CMP AL,93
JE SEPARATORRET
CMP AL,43
JE SEPARATORRET
CMP AL,45
JE SEPARATORRET
CMP AL,40
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SEPARATORRET
```

With:

```asm
JE NEAR SEPARATORRET
```

### Change 103 · `ZSCAN4:`

Find the unique label `ZSCAN4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZSCAN4:
CMP AL,58
JE SEPARATORRET
CMP AL,91
JE SEPARATORRET
CMP AL,93
JE SEPARATORRET
CMP AL,43
JE SEPARATORRET
CMP AL,45
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SEPARATORRET
```

With:

```asm
JE NEAR SEPARATORRET
```

### Change 104 · `ZSCAN4:`

Find the unique label `ZSCAN4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZSCAN4:
CMP AL,58
JE SEPARATORRET
CMP AL,91
JE SEPARATORRET
CMP AL,93
JE SEPARATORRET
CMP AL,43
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SEPARATORRET
```

With:

```asm
JE NEAR SEPARATORRET
```

### Change 105 · `ZSCAN4:`

Find the unique label `ZSCAN4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZSCAN4:
CMP AL,58
JE SEPARATORRET
CMP AL,91
JE SEPARATORRET
CMP AL,93
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SEPARATORRET
```

With:

```asm
JE NEAR SEPARATORRET
```

### Change 106 · `ZSCAN4:`

Find the unique label `ZSCAN4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZSCAN4:
CMP AL,58
JE SEPARATORRET
CMP AL,91
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SEPARATORRET
```

With:

```asm
JE NEAR SEPARATORRET
```

### Change 107 · `ZSCAN4:`

Find the unique label `ZSCAN4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZSCAN4:
CMP AL,58
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SEPARATORRET
```

With:

```asm
JE NEAR SEPARATORRET
```

### Change 108 · `SEPARATOR:`

Find the unique label `SEPARATOR:`, then follow this unchanged source through its last displayed instruction:

```asm
SEPARATOR:
MOV AH,1
CMP AL,44
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZSCAN4
JMP SEPARATORRET
ZSCAN4:
```

With:

```asm
JE NEAR SEPARATORRET
```

### Change 109 · `TOKENCHAR:`

Find the unique label `TOKENCHAR:`, then follow this unchanged source through its last displayed instruction:

```asm
TOKENCHAR:
CMP AL,97
JB TOKENKEPT
CMP AL,122
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JA TOKENKEPT
```

With:

```asm
JA NEAR TOKENKEPT
```

### Change 110 · `TOKENCHAR:`

Find the unique label `TOKENCHAR:`, then follow this unchanged source through its last displayed instruction:

```asm
TOKENCHAR:
CMP AL,97
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB TOKENKEPT
```

With:

```asm
JB NEAR TOKENKEPT
```

### Change 111 · `SCANMORE:`

Find the unique label `SCANMORE:`, then follow this unchanged source through its last displayed instruction:

```asm
SCANMORE:
LODSB
CMP AL,0
JE SCANBACK
CMP AL,32
JE SCANBACK
CMP AL,9
JE SCANBACK
CMP AL,59
JE SCANBACK
CALL SEPARATOR
CMP AH,1
JE SCANBACK
CMP DI,0CC3FH
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE TOKENBAD
```

With:

```asm
JAE NEAR TOKENBAD
```

### Change 112 · `SCANMORE:`

Find the unique label `SCANMORE:`, then follow this unchanged source through its last displayed instruction:

```asm
SCANMORE:
LODSB
CMP AL,0
JE SCANBACK
CMP AL,32
JE SCANBACK
CMP AL,9
JE SCANBACK
CMP AL,59
JE SCANBACK
CALL SEPARATOR
CMP AH,1
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SCANBACK
```

With:

```asm
JE NEAR SCANBACK
```

### Change 113 · `SCANMORE:`

Find the unique label `SCANMORE:`, then follow this unchanged source through its last displayed instruction:

```asm
SCANMORE:
LODSB
CMP AL,0
JE SCANBACK
CMP AL,32
JE SCANBACK
CMP AL,9
JE SCANBACK
CMP AL,59
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SCANBACK
```

With:

```asm
JE NEAR SCANBACK
```

### Change 114 · `SCANMORE:`

Find the unique label `SCANMORE:`, then follow this unchanged source through its last displayed instruction:

```asm
SCANMORE:
LODSB
CMP AL,0
JE SCANBACK
CMP AL,32
JE SCANBACK
CMP AL,9
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SCANBACK
```

With:

```asm
JE NEAR SCANBACK
```

### Change 115 · `SCANMORE:`

Find the unique label `SCANMORE:`, then follow this unchanged source through its last displayed instruction:

```asm
SCANMORE:
LODSB
CMP AL,0
JE SCANBACK
CMP AL,32
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SCANBACK
```

With:

```asm
JE NEAR SCANBACK
```

### Change 116 · `SCANMORE:`

Find the unique label `SCANMORE:`, then follow this unchanged source through its last displayed instruction:

```asm
SCANMORE:
LODSB
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SCANBACK
```

With:

```asm
JE NEAR SCANBACK
```

### Change 117 · `ZSCAN2:`

Find the unique label `ZSCAN2:`, then follow this unchanged source through its last displayed instruction:

```asm
ZSCAN2:
CALL TOKENCHAR
STOSB
CALL SEPARATOR
CMP AH,1
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZSCAN3
JMP SCANDONE
ZSCAN3:
```

With:

```asm
JE NEAR SCANDONE
```

Keep the following `SCANMORE:` label and the source after it in place.

### Change 118 · `ZSCAN1:`

Find the unique label `ZSCAN1:`, then follow this unchanged source through its last displayed instruction:

```asm
ZSCAN1:
CMP AL,59
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZSCAN2
JMP SCANEND
ZSCAN2:
```

With:

```asm
JE NEAR SCANEND
```

### Change 119 · `SCANSPACE:`

Find the unique label `SCANSPACE:`, then follow this unchanged source through its last displayed instruction:

```asm
SCANSPACE:
LODSB
CMP AL,32
JE SCANSPACE
CMP AL,9
JE SCANSPACE
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZSCAN1
JMP SCANEND
ZSCAN1:
```

With:

```asm
JE NEAR SCANEND
```

### Change 120 · `SCANSPACE:`

Find the unique label `SCANSPACE:`, then follow this unchanged source through its last displayed instruction:

```asm
SCANSPACE:
LODSB
CMP AL,32
JE SCANSPACE
CMP AL,9
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SCANSPACE
```

With:

```asm
JE NEAR SCANSPACE
```

### Change 121 · `SCANSPACE:`

Find the unique label `SCANSPACE:`, then follow this unchanged source through its last displayed instruction:

```asm
SCANSPACE:
LODSB
CMP AL,32
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE SCANSPACE
```

With:

```asm
JE NEAR SCANSPACE
```

### Change 122 · `ENDFILE:`

Find the unique label `ENDFILE:`, then follow this unchanged source through its last displayed instruction:

```asm
ENDFILE:
MOV AL,1
MOV [ENDED],AL
CMP BP,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE EMPTYEND
```

With:

```asm
JE NEAR EMPTYEND
```

Keep the following `LINEEND:` label and the source after it in place.

### Change 123 · `LINEFEED:`

Find the unique label `LINEFEED:`, then follow this unchanged source through its last displayed instruction:

```asm
LINEFEED:
MOV AL,[SKIPLF]
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE LINEEND
```

With:

```asm
JE NEAR LINEEND
```

### Change 124 · `ZREADLINE6:`

Find the unique label `ZREADLINE6:`, then follow this unchanged source through its last displayed instruction:

```asm
ZREADLINE6:
CMP AL,126
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JBE ZREADLINE7
JMP READBAD
ZREADLINE7:
```

With:

```asm
JA NEAR READBAD
```

Keep the following `KEEPCHAR:` label and the source after it in place.

### Change 125 · `ZREADLINE5:`

Find the unique label `ZREADLINE5:`, then follow this unchanged source through its last displayed instruction:

```asm
ZREADLINE5:
CMP AL,9
JE KEEPCHAR
CMP AL,32
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE ZREADLINE6
JMP READBAD
ZREADLINE6:
```

With:

```asm
JB NEAR READBAD
```

### Change 126 · `ZREADLINE5:`

Find the unique label `ZREADLINE5:`, then follow this unchanged source through its last displayed instruction:

```asm
ZREADLINE5:
CMP AL,9
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE KEEPCHAR
```

With:

```asm
JE NEAR KEEPCHAR
```

### Change 127 · `ZREADLINE4:`

Find the unique label `ZREADLINE4:`, then follow this unchanged source through its last displayed instruction:

```asm
ZREADLINE4:
CMP BP,1023
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB ZREADLINE5
JMP READFULL
ZREADLINE5:
```

With:

```asm
JAE NEAR READFULL
```

### Change 128 · `ZREADLINE3:`

Find the unique label `ZREADLINE3:`, then follow this unchanged source through its last displayed instruction:

```asm
ZREADLINE3:
CMP AL,26
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZREADLINE4
JMP ENDFILE
ZREADLINE4:
```

With:

```asm
JE NEAR ENDFILE
```

### Change 129 · `ZREADLINE2:`

Find the unique label `ZREADLINE2:`, then follow this unchanged source through its last displayed instruction:

```asm
ZREADLINE2:
MOV AH,0
MOV [SKIPLF],AH
CMP AL,13
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZREADLINE3
JMP CARRIAGE
ZREADLINE3:
```

With:

```asm
JE NEAR CARRIAGE
```

### Change 130 · `ZREADLINE1:`

Find the unique label `ZREADLINE1:`, then follow this unchanged source through its last displayed instruction:

```asm
ZREADLINE1:
MOV AL,[CHAR]
CMP AL,10
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZREADLINE2
JMP LINEFEED
ZREADLINE2:
```

With:

```asm
JE NEAR LINEFEED
```

### Change 131 · `READCHAR:`

Find the unique label `READCHAR:`, then follow this unchanged source through its last displayed instruction:

```asm
READCHAR:
CALL NEXTBYTE
CMP AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE ZREADLINE1
JMP ENDFILE
ZREADLINE1:
```

With:

```asm
JE NEAR ENDFILE
```

### Change 132 · `READLINE:`

Find the unique label `READLINE:`, then follow this unchanged source through its last displayed instruction:

```asm
READLINE:
MOV DI,0C800H
MOV BP,0
MOV AL,[ENDED]
CMP AL,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE READCHAR
```

With:

```asm
JE NEAR READCHAR
```

### Change 133 · `REFILLED:`

Find the unique label `REFILLED:`, then follow this unchanged source through its last displayed instruction:

```asm
REFILLED:
MOV [RDLEN],AX
MOV DX,0
MOV [RDPOS],DX
CMP AX,0
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE BUFFEREND
```

With:

```asm
JE NEAR BUFFEREND
```

Keep the following `BUFFERBYTE:` label and the source after it in place.

### Change 134 · `NEXTBYTE:`

Find the unique label `NEXTBYTE:`, then follow this unchanged source through its last displayed instruction:

```asm
NEXTBYTE:
MOV AX,[RDPOS]
MOV DX,[RDLEN]
CMP AX,DX
JB BUFFERBYTE
MOV BX,[HANDLE]
MOV DX,0D000H
MOV CX,4096
MOV AH,3FH
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE REFILLED
```

With:

```asm
JAE NEAR REFILLED
```

### Change 135 · `NEXTBYTE:`

Find the unique label `NEXTBYTE:`, then follow this unchanged source through its last displayed instruction:

```asm
NEXTBYTE:
MOV AX,[RDPOS]
MOV DX,[RDLEN]
CMP AX,DX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB BUFFERBYTE
```

With:

```asm
JB NEAR BUFFERBYTE
```

### Change 136 · `NEXTBYTE:`

Find the unique label `NEXTBYTE:`. Insert the new source immediately before this existing label:

```asm
NEXTBYTE:
```

Insert:

```asm
CREATEOUT:
MOV DX,TMPNAME
MOV CX,0
MOV AH,3CH
INT 21H
JAE NEAR OUTPUTOPEN
JMP FILEBAD
OUTPUTOPEN:
MOV [OUTHANDLE],AX
MOV AL,1
MOV [OUTOPEN],AL
MOV [OWNTMP],AL
RET
CLOSEOUT:
MOV BX,[OUTHANDLE]
MOV AH,3EH
INT 21H
JAE NEAR OUTPUTCLOSED
JMP FILEBAD
OUTPUTCLOSED:
MOV AL,0
MOV [OUTOPEN],AL
RET
FLUSH:
PUSH AX
PUSH BX
PUSH CX
PUSH DX
MOV CX,[OUTCNT]
CMP CX,0
JE NEAR FLUSHDONE
MOV BX,[OUTHANDLE]
MOV DX,0E000H
MOV AH,40H
INT 21H
JAE NEAR FLUSHCOUNT
JMP FILEBAD
FLUSHCOUNT:
CMP AX,CX
JE NEAR FLUSHGOOD
JMP FILEBAD
FLUSHGOOD:
MOV AX,0
MOV [OUTCNT],AX
FLUSHDONE:
POP DX
POP CX
POP BX
POP AX
RET
```

### Change 137 · `CLOSEFILE:`

Find the unique label `CLOSEFILE:`, then follow this unchanged source through its last displayed instruction:

```asm
CLOSEFILE:
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE INPUTCLOSED
```

With:

```asm
JAE NEAR INPUTCLOSED
```

### Change 138 · `OPENFILE:`

Find the unique label `OPENFILE:`, then follow this unchanged source through its last displayed instruction:

```asm
OPENFILE:
MOV DX,SRCNAME
MOV AX,3D00H
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JAE INPUTOPEN
```

With:

```asm
JAE NEAR INPUTOPEN
```

### Change 139 · `ROOM:`

Find the unique label `ROOM:`. The old block below starts at that label.

Remove from the following first source through the ending block below, including both boundaries and everything between them:

```asm
ROOM:
CALL CMDFILES
CALL MEMINIT
```

Find the unique ending label `GOOD:`. The removal ends after this existing source:

```asm
GOOD:
MOV AX,4C00H
INT 21H
```

Keep the following `FILEBAD:` label and the source after it in place.

### Change 140 · `START:`

Find the unique label `START:`, then follow this unchanged source through its last displayed instruction:

```asm
START:
CLD
CMP SP,0FFFEH
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE ROOM
```

With:

```asm
JNE NEAR MEMORYBAD
CALL CMDFILES
CALL OPENFILE
READNEXT:
CALL READLINE
CMP AX,0
JE NEAR READDONE
MOV SI,0C800H
SHOWBYTE:
LODSB
CMP AL,0
JE NEAR SHOWEND
MOV DL,AL
MOV AH,2
INT 21H
JMP SHOWBYTE
SHOWEND:
MOV DX,NEWLINE
CALL TEXT
JMP READNEXT
READDONE:
CALL CLOSEFILE
MOV AX,4C00H
INT 21H
MEMORYBAD:
```

## Build and check

```dos
CHECK ASMAKEEP IR01.ASM RESULT.COM
```

Require fresh OK and PASS reports before each following copy. The assembler must report `OK RESULT.COM 02534 bytes`. Save RESULT.COM as IR01.COM. VIEW.BAS must show length 2534.

Create T01.IR:

```text
ABC
```

```dos
CHECK IR01 T01.IR RESULT.ASM
```

Require:

```text
ABC
PASS
```

The displayed `ABC` gives me a working reader to keep. The source counters and file errors are already attached to it; the next step can concentrate on recognizing pieces of the line.

## Check the new boundary

Choose an absent disk filename, ABSENT.IR, and run:

```dos
CHECK IR01 ABSENT.IR RESULT.ASM
```

Require:

```text
IR ERROR 0000000000 CODE 6
FAIL
```

An unexpected PASS fails this check. This checkpoint creates no result file; an existing selected result must remain untouched.

