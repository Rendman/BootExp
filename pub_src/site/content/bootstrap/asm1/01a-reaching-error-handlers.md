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

Some branches already fit their present routines. We choose the wider source pattern here so later report and file-handling additions do not rely on that spare reach. No new error category or encoding routine is introduced. The opening comment identifies the construction source and emits no bytes.


## Enter the source

Copy ASM0.ASM to A01A.ASM. Apply these edits from the bottom of the old file upward. Physical positions locate the old source; the context identifies the exact edit. Keep all other source.

### Change 1

Unchanged source immediately before the edit:

```asm
DB 74,78,69,0,0,0,8,117
DB 74,66,69,0,0,0,8,118
DB 74,65,0,0,0,0,8,119
```

Insert after old physical line 1080.

Insert:

```asm

```

### Change 2

Unchanged source immediately before the edit:

```asm
MOV AL,[W1]
CMP AL,0
MOV AX,[VAL]
```

Remove old physical positions 784–784:

```asm
JE BYTEVALUE
```

Replace with:

```asm
JNE IMMEDWORD
JMP BYTEVALUE
IMMEDWORD:
```

The following old source stays in place:

```asm
JMP EMITWORD
```

### Change 3

Unchanged source immediately before the edit:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

Remove old physical positions 84–84:

```asm
JB FILEBAD
```

Replace with:

```asm
JAE ZWRITEOUT4
JMP FILEBAD
ZWRITEOUT4:
```

The following old source stays in place:

```asm
MOV DX,OKMSG
CALL TEXT
```

### Change 4

Unchanged source immediately before the edit:

```asm
INT 21H
JB FILEBAD
CMP AX,CX
```

Remove old physical positions 80–80:

```asm
JNE FILEBAD
```

Replace with:

```asm
JE ZWRITEOUT3
JMP FILEBAD
ZWRITEOUT3:
```

The following old source stays in place:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
```

### Change 5

Unchanged source immediately before the edit:

```asm
MOV DX,6000H
MOV AH,40H
INT 21H
```

Remove old physical positions 78–78:

```asm
JB FILEBAD
```

Replace with:

```asm
JAE ZWRITEOUT2
JMP FILEBAD
ZWRITEOUT2:
```

The following old source stays in place:

```asm
CMP AX,CX
JNE FILEBAD
```

### Change 6

Unchanged source immediately before the edit:

```asm
MOV CX,0
MOV AH,3CH
INT 21H
```

Remove old physical positions 70–70:

```asm
JB FILEBAD
```

Replace with:

```asm
JAE ZWRITEOUT1
JMP FILEBAD
ZWRITEOUT1:
```

The following old source stays in place:

```asm
MOV [HANDLE],AX
MOV BX,AX
```

### Change 7

Unchanged source immediately before the edit:

```asm
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
```

Remove old physical positions 62–62:

```asm
JB FILEBAD
```

Replace with:

```asm
JAE INPUTCLOSED
JMP FILEBAD
INPUTCLOSED:
```

The following old source stays in place:

```asm
RET
```

### Change 8

Remove old physical positions 1–1:

```asm
; ASM86 construction checkpoint. Plain BOOTASM source.
```

Replace with:

```asm
; ASM86A construction checkpoint.
```

The following old source stays in place:

```asm
START:
CLD
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
