+++
title = "02 \u00b7 Making Room for File Names"
weight = 2
description = "Give each selected filename its own terminated buffer and explain the data layout."
download = "A01B.ASM"
download_group = "tools/asm1"
reader_names = 1
command_examples = "literal"
url = "/bootstrap/asma0/01b-storing-file-names/"
+++

I will need two independently saved names. Before reading the command line, I give each name a place in the assembler's data and follow the existing file calls to those places.

## What this step adds

SRCNAME replaces FNAME as the source-name label. OPENFILE loads its address into DX. RESNAME remains the address used by WRITEOUT. Both names still contain SOURCE.ASM and RESULT.COM, so this checkpoint uses fixed files and accepts no filename arguments yet.

Each record now has thirteen bytes: at most eight base characters, one dot, three extension characters, and a terminating zero. The remaining zero bytes are capacity for a later, longer selected spelling. They are not characters in the default name. DOS open/create services expect the address of the first character and stop at the zero.

The name records move after OPTAB, and OUTPTR moves beside them. Moving a variable changes the address of its storage, which the assembler resolves from its label. It does not change the word held there: 24576 is still 6000H, the start of the existing complete-image output buffer. The buffer has not moved or become a stream.

OPTAB still has twenty-five records. Its counted lookup ends before SRCNAME. The DB directives under the name labels describe ordinary data, not additional instructions in the opcode table. HANDLE remains a separate DOS handle word; these buffers hold filenames, not handles.


## Enter the source

Copy A01A.ASM to A01B.ASM. Apply these edits from the bottom of the old file upward. Physical positions locate the old source; the context identifies the exact edit. Keep all other source.

### Change 1

Unchanged source immediately before the edit:

```asm
DB 74,66,69,0,0,0,8,118
DB 74,65,0,0,0,0,8,119
```

Insert after old physical line 1093.

Insert:

```asm
SRCNAME:
DB 83,79,85,82,67,69,46,65,83,77,0,0,0

RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0,0,0

OUTPTR:
DW 24576
```

### Change 2

Unchanged source immediately before the edit:

```asm

PC:
DW 256
```

Remove old physical positions 988–990:

```asm

OUTPTR:
DW 24576
```

There is no replacement source.

The following old source stays in place:

```asm

SYMC:
```

### Change 3

Unchanged source immediately before the edit:

```asm

DIVEND:
```

Remove old physical positions 974–979:

```asm
FNAME:
DB 83,79,85,82,67,69,46,65,83,77,0

RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0
```

There is no replacement source.

The following old source stays in place:

```asm
HANDLE:
DW 0
```

### Change 4

Unchanged source immediately before the edit:

```asm
JMP ERROR

OPENFILE:
```

Remove old physical positions 49–49:

```asm
MOV DX,FNAME
```

Replace with:

```asm
MOV DX,SRCNAME
```

The following old source stays in place:

```asm
MOV AX,3D00H
INT 21H
```

## Build this stopping point

```dos
COPY A01B.ASM SOURCE.ASM
CHECK ASMKEEP
COPY RESULT.COM A01B.COM
```

Require the preceding ASM0 to report `OK 02453 bytes` and CHECK to report PASS before preserving the result. VIEW.BAS must show A01B.COM length 2453 bytes. Keep the source and executable together.

## Check the addition

Create T01B.ASM:

```asm
DB 1,2,3,4
```

```dos
COPY T01B.ASM SOURCE.ASM
CHECK A01B
```

Require:

```text
OK 00004 bytes
PASS
```

VIEW.BAS must show RESULT.COM length 4 bytes and these complete contents:

```text
01 02 03 04
```

The file is an encoding check; inspect it rather than executing it.

Continue with [Reading Names from the PSP](../01c-reading-the-command-tail/index.html).
