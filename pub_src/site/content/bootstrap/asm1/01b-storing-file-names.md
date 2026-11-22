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

**Starting source:** `A01A.ASM`. **Save as:** `A01B.ASM`. **Build with:** `ASMKEEP.COM`.

## What this step adds

SRCNAME replaces FNAME as the source-name label. OPENFILE loads its address into DX. RESNAME remains the address used by WRITEOUT. Both names still contain SOURCE.ASM and RESULT.COM, so this checkpoint uses fixed files and accepts no filename arguments yet.

Each record now has thirteen bytes: at most eight base characters, one dot, three extension characters, and a terminating zero. The remaining zero bytes provide capacity for longer 8.3 spellings. They are not characters in the default name. DOS open/create services expect the address of the first character and stop at the zero.

The name records move after OPTAB, and OUTPTR moves beside them. Moving a variable changes the address of its storage, which the assembler resolves from its label. It does not change the word held there: 24576 is still 6000H, the start of the existing complete-image output buffer. The buffer has not moved or become a stream.

OPTAB still has twenty-five records. Its counted lookup ends before SRCNAME. The DB directives under the name labels describe ordinary data, not additional instructions in the opcode table. HANDLE remains a separate DOS handle word; these buffers hold filenames, not handles.


## Enter the source

Copy A01A.ASM to A01B.ASM. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OPTAB:`

Find the unique label `OPTAB:`, then follow this unchanged source through its last displayed instruction:

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
```

The edit begins immediately after that unchanged block.

Insert:

```asm
SRCNAME:
DB 83,79,85,82,67,69,46,65,83,77,0,0,0
RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0,0,0
OUTPTR:
DW 24576
```

### Change 2 · `PC:`

Find the unique label `PC:`, then follow this unchanged source through its last displayed instruction:

```asm
PC:
DW 256
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
OUTPTR:
DW 24576
```

Keep the following `SYMC:` label and the source after it in place.

### Change 3 · `FNAME:`

Find the unique label `FNAME:`. The old block below starts at that label.

Remove this existing source:

```asm
FNAME:
DB 83,79,85,82,67,69,46,65,83,77,0
RESNAME:
DB 82,69,83,85,76,84,46,67,79,77,0
```

Keep the following `HANDLE:` label and the source after it in place.

### Change 4 · `OPENFILE:`

Find the unique label `OPENFILE:`, then follow this unchanged source through its last displayed instruction:

```asm
OPENFILE:
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV DX,FNAME
```

With:

```asm
MOV DX,SRCNAME
```

## Build this stopping point

```dos
COPY A01B.ASM SOURCE.ASM
CHECK ASMKEEP
COPY RESULT.COM A01B.COM
```

Require the preceding ASM0 to report `OK 02453 bytes` and CHECK to report PASS before preserving the result. Keep the source and executable together.

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
