+++
title = "12 \u00b7 Writing the image"
weight = 12
description = "Create the output only after every source line succeeds."
download = "AS12.ASM"
aliases = ["/bootstrap/asm86/13-writing-the-image/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/12-writing-the-image/"
+++

I have a buffer I can inspect. Now I need DOS to make the file from it. In BASIC I wrote one-byte records; here I can ask DOS to write the collected block and tell me how much it accepted.

**Starting source:** `AS11.ASM`. **Save as:** `AS12.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

WRITEOUT passes the fixed RESULT.COM name at RESNAME to DOS function 3CH. CX=0 requests an ordinary file. Creation truncates an existing file exactly; there is no BASIC sequential-file end marker or .COM header.

The returned handle goes in BX. For function 40H, CX is PC minus 0100H and DS:DX points to the buffer at 6000H. Carry reports a write error; with carry clear AX must equal the requested count. A short write is an error even though carry was clear. The final close is checked as well.

Only a completed write and close produce OK followed by the five-digit byte count. WRITEOUT changes working registers; it returns to the driver's successful termination. A zero-byte image creates a genuine empty file, which is valid for inspection but not execution.

Input errors leave an older output untouched because creation has not occurred. A disk error after creation can leave an empty or partial output; require a fresh OK report. The source is still one numeric byte per line at this checkpoint.

## Source changes

Copy `AS11.ASM` to `AS12.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `BUFFERMSG:`

Find the unique label `BUFFERMSG:`. The old block below starts at that label.

Remove this existing source:

```asm
BUFFERMSG:
DB 66,117,102,102,101,114,101,100,32,36
```

### Change 2 · `HANDLE:`

Find the unique label `HANDLE:`. Insert the new source immediately before this existing label:

```asm
HANDLE:
```

Insert:

```asm
RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0
```

### Change 3 · `BYTEMSG:`

Find the unique label `BYTEMSG:`. Insert the new source immediately before this existing label:

```asm
BYTEMSG:
```

Insert:

```asm
OKMSG:
DB 79,75,32,36
```

### Change 4 · `CLOSEFILE:`

Find the unique label `CLOSEFILE:`, then follow this unchanged source through its last displayed instruction:

```asm
CLOSEFILE:
MOV BX,[HANDLE]
MOV AH,3EH
INT 21H
JB FILEBAD
```

The edit begins immediately after that unchanged block.

Insert:

```asm
RET
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
JB FILEBAD
MOV DX,OKMSG
CALL TEXT
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

### Change 5 · `DRIVERDONE:`

Find the unique label `DRIVERDONE:`, then follow this unchanged source through its last displayed instruction:

```asm
DRIVERDONE:
CALL CLOSEFILE
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV DX,BUFFERMSG
CALL TEXT
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

With:

```asm
CALL WRITEOUT
```

Keep the following `GOOD:` label and the source after it in place.

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS12.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 911 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS12.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T12.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
65
66
```

```dos
COPY T12.ASM SOURCE.ASM
```

```dos
CHECK AS12
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00002 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **2 bytes** with these hexadecimal bytes:

```text
41 42
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X12.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
256
```

```dos
COPY X12.ASM SOURCE.ASM
CHECK AS12
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check that the DOS write count is PC minus 0100H, not PC itself. Test both carry and AX against the requested count, then check the close; an older OK report cannot establish that this write succeeded.
