+++
title = "01 \u00b7 Giving Conditional Branches Room"
weight = 1
description = "Use explicit short skips and near jumps before the routines grow."
download = "A01A.ASM"
download_group = "tools/asm1"
reader_names = 1
command_examples = "literal"
url = "/bootstrap/asma0/01a-reaching-error-handlers/"
+++

I start with ASM0's accepted source and mark the branches that will need room as I enlarge its routines. I can make a distant condition out of two instructions that ASM0 already knows.

## What this step adds

Six existing conditional branches become an opposite short condition followed by a near JMP. The accepted instruction table stays at twenty-five records. The assembler still reads SOURCE.ASM and writes RESULT.COM.

An 8086 conditional jump has a signed byte displacement, measured from the following instruction: -128 through +127. A near JMP has a signed word displacement. In `JNE SKIP / JMP DEST / SKIP:`, equality takes the JMP to DEST; inequality skips that JMP. The near JMP occupies three bytes, so the short branch only has to skip three bytes. The condition and destination have the same meaning as the original JE DEST.

These are explicit source bridges. We are not adding a new long-conditional spelling to the assembler. The file paths use JAE to skip an error JMP when carry is clear; the short-write test uses JE to skip its error JMP when the counts agree. INPUTCLOSED and the four ZWRITEOUT labels name those nearby landing points. IMMEDWORD makes the byte-versus-word immediate choice with the same pattern. The Z labels are ordinary labels, not generated instruction forms.

Some branches already fit their present routines. We choose the wider source pattern here so later report and file-handling additions do not rely on that spare reach. No new error category or encoding routine is introduced. Comments and blank lines are left to the reader; they emit no bytes.


## Enter the source

Copy ASM0.ASM to A01A.ASM. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `IMMEDVALUE:`

Find the unique label `IMMEDVALUE:`, then follow this unchanged source through its last displayed instruction:

```asm
IMMEDVALUE:
MOV AL,[W1]
CMP AL,0
MOV AX,[VAL]
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JE BYTEVALUE
```

With:

```asm
JNE IMMEDWORD
JMP BYTEVALUE
IMMEDWORD:
```

### Change 2 · `WRITEOUT:`

Find the unique label `WRITEOUT:`, then follow this unchanged source through its last displayed instruction:

```asm
WRITEOUT:
MOV DX,RESNAME
MOV CX,0
MOV AH,3CH
INT 21H
JB FILEBAD
MOV [HANDLE],AX
MOV BX,AX
MOV CX,[PC]
SUB CX,100H
MOV DX,6000H
MOV AH,40H
INT 21H
JB FILEBAD
CMP AX,CX
JNE FILEBAD
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB FILEBAD
```

With:

```asm
JAE ZWRITEOUT4
JMP FILEBAD
ZWRITEOUT4:
```

### Change 3 · `WRITEOUT:`

Find the unique label `WRITEOUT:`, then follow this unchanged source through its last displayed instruction:

```asm
WRITEOUT:
MOV DX,RESNAME
MOV CX,0
MOV AH,3CH
INT 21H
JB FILEBAD
MOV [HANDLE],AX
MOV BX,AX
MOV CX,[PC]
SUB CX,100H
MOV DX,6000H
MOV AH,40H
INT 21H
JB FILEBAD
CMP AX,CX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JNE FILEBAD
```

With:

```asm
JE ZWRITEOUT3
JMP FILEBAD
ZWRITEOUT3:
```

### Change 4 · `WRITEOUT:`

Find the unique label `WRITEOUT:`, then follow this unchanged source through its last displayed instruction:

```asm
WRITEOUT:
MOV DX,RESNAME
MOV CX,0
MOV AH,3CH
INT 21H
JB FILEBAD
MOV [HANDLE],AX
MOV BX,AX
MOV CX,[PC]
SUB CX,100H
MOV DX,6000H
MOV AH,40H
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB FILEBAD
```

With:

```asm
JAE ZWRITEOUT2
JMP FILEBAD
ZWRITEOUT2:
```

### Change 5 · `WRITEOUT:`

Find the unique label `WRITEOUT:`, then follow this unchanged source through its last displayed instruction:

```asm
WRITEOUT:
MOV DX,RESNAME
MOV CX,0
MOV AH,3CH
INT 21H
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
JB FILEBAD
```

With:

```asm
JAE ZWRITEOUT1
JMP FILEBAD
ZWRITEOUT1:
```

### Change 6 · `CLOSEFILE:`

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
JB FILEBAD
```

With:

```asm
JAE INPUTCLOSED
JMP FILEBAD
INPUTCLOSED:
```

## Build this stopping point

```dos
COPY A01A.ASM SOURCE.ASM
CHECK ASMKEEP
COPY RESULT.COM A01A.COM
```

Require the preceding ASM0 to report `OK 02449 bytes` and CHECK to report PASS before preserving the result. VIEW.BAS must show A01A.COM length 2449 bytes. Keep the source and executable together.

## Check the addition

Create T01A.ASM:

```asm
JNE SKIP
JMP DEST
SKIP:
DB 0
DEST:
RET
```

```dos
COPY T01A.ASM SOURCE.ASM
CHECK A01A
```

Require:

```text
OK 00007 bytes
PASS
```

VIEW.BAS must show RESULT.COM length 7 bytes and these complete contents:

```text
75 03 E9 01 00 00 C3
```

The file is an encoding check; inspect it rather than executing it.

Continue with [Making Room for File Names](../01b-storing-file-names/index.html).
