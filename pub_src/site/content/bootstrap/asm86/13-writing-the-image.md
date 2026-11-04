+++
title = "13 \u00b7 Writing the image"
weight = 13
description = "Create the output only after every source line succeeds."
download = "AS13.ASM"
+++

The byte buffer is ready to become a file. We shall create a fresh .COM image and check both the write count and the close.

## How it works

WRITEOUT replaces the extension at EXTP with .COM and passes FNAME to DOS function 3CH. CX=0 requests an ordinary file. Creation truncates an existing file exactly; there is no BASIC sequential-file end marker or .COM header.

The returned handle goes in BX. For function 40H, CX is PC minus 0100H and DS:DX points to the buffer at 6000H. Carry reports a write error; with carry clear AX must equal the requested count. A short write is an error even though carry was clear. The final close is checked as well.

Only a completed write and close produce OK followed by the five-digit byte count. WRITEOUT changes working registers and FNAME's extension; it returns to the driver's successful termination. A zero-byte image creates a genuine empty file, which is valid for inspection but not execution.

Input errors leave an older output untouched because creation has not occurred. A disk error after creation can leave an empty or partial output; require a fresh OK report. The source is still one numeric byte per line at this checkpoint.

## Source changes

Copy `AS12.ASM` to `AS13.ASM`. Make the following changes **from the bottom of the old file upward**, in the order printed here. This keeps the old physical line positions valid. Positions count every line, including blank lines; they are locators, not source to type. The nearby label and unchanged context identify each place. Retain everything else.

### Change 1: following `ERRCODE:`

Unchanged code immediately before this edit:

```asm

ERRCODE:
DB 0
```

Remove these exact old lines (physical lines 494–496 of `AS12.ASM`):

```asm

BUFFERMSG:
DB 66,117,102,102,101,114,101,100,32,36
```

No replacement lines are needed.

### Change 2: following `ASMEXT:`

Unchanged code immediately before this edit:

```asm

ASMEXT:
DB 46,65,83,77,0
```

Insert after old physical line 452, before the following old line.

Insert this source:

```asm

COMEXT:
DB 46,67,79,77,0
```

### Change 3: following `PROMPT:`

Unchanged code immediately before this edit:

```asm
PROMPT:
DB 83,111,117,114,99,101,32,110,97,109,101,58,32,36

```

Insert after old physical line 438, before the following old line.

Insert this source:

```asm
OKMSG:
DB 79,75,32,36

```

### Change 4: following `CLOSEFILE:`

Unchanged code immediately before this edit:

```asm
MOV AH,3EH
INT 21H
JB FILEBAD
```

Insert after old physical line 58, before the following old line.

Insert this source:

```asm
RET

WRITEOUT:
MOV DI,[EXTP]
MOV SI,COMEXT
CALL COPYZ
MOV DX,FNAME
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
JB FILEBAD
MOV DX,OKMSG
CALL TEXT
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

### Change 5: following `DRIVERDONE:`

Unchanged code immediately before this edit:

```asm
JMP DRIVERLINE
DRIVERDONE:
CALL CLOSEFILE
```

Remove these exact old lines (physical lines 29–35 of `AS12.ASM`):

```asm
MOV DX,BUFFERMSG
CALL TEXT
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

Put this source in their place:

```asm
CALL WRITEOUT
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
GWBASIC BOOTASM.BAS
```

Enter `AS13` at its source prompt. Require `OK AS13.COM 1062 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS. Save this source and executable as a working stopping point.

Use `COPY CON T13.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
65
66
```

```dos
CHECK AS13
```

Enter `T13` when `Source name:` appears.

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Source name: T13
OK 00002 bytes
PASS
```

Inspect `T13.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `T13.COM`, and require a length of **2 bytes** with these hexadecimal bytes:

```text
41 42
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X13.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
256
```

Run `CHECK AS13` and enter `X13`.

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the edited blocks against their old context, then compare the complete source. A wrong record count or a missing zero terminator can make a correct token look absent. Check brackets and commas in the test input, and read the reported physical line before changing an instruction.
