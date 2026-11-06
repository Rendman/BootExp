+++
title = "09 \u00b7 Declaring a word"
weight = 9
description = "Put initialized word storage before the entry label."
download = "IR09.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

WORD gives a value a named place in memory, separate from the accumulator.

## Operation and backend

WORD takes a name and an unsigned initializer. ARGUMENTS retains the name before scanning its value, since both use the same token buffer. Its template emits U_name followed by DW value. ASM0 writes the initializer low byte first.

Declarations must precede LABEL MAIN. The header jumps over them, so no declaration byte is executed at program entry. CONTEXT accepts declaration classes only while CODE is zero, and the MAIN label changes CODE to one.

A declaration emits storage in the program's single segment. A name has one common namespace for storage and code; the translator checks spelling while ASM0 resolves references and rejects duplicate definitions. A successful translation is not permission to run a file whose assembly failed.

## Source changes

Copy `IR08.ASM` to `IR09.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_EXIT:`

Unchanged code immediately before the edit:

```asm
T_EXIT:
DB 77,79,86,32,65,72,44,52,67,72,13,10,73,78,84,32
DB 50,49,72,13,10,0
```

Insert after old physical line 821, before the following old line.

Insert this source:

```asm

T_WORD:
DB 85,95,64,58,13,10,68,87,32,35,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_LIT
DB 69,88,73,84,0,0,0,0,0,5,4,0
DW T_EXIT
```

Insert after old physical line 711, before the following old line.

Insert this source:

```asm
DB 87,79,82,68,0,0,0,0,5,0,2,0
DW T_WORD
```

### Change 3: following `ARGZERO:`

Unchanged code immediately before the edit:

```asm
CALL NAMEARG
ARGZERO:
RET
```

Insert after old physical line 648, before the following old line.

Insert this source:

```asm
ARGRANGE:
MOV AX,4
JMP ERROR
```

### Change 4: following `ARGONE:`

Unchanged code immediately before the edit:

```asm
RET
ARGONE:
CALL NAMEARG
```

Remove these exact old lines (physical positions 647–647 in `IR08.ASM`):

```asm
ARGZERO:
```

Put this source in their place:

```asm
MOV AL,[CLASS]
CMP AL,4
JB ARGDONE
CMP AL,6
JA ARGDONE
CALL NUMARG
ARGDONE:
```

### Change 5: following `ARGUMENTS:`

Unchanged code immediately before the edit:

```asm
JNE ARGONE
CALL NUMARG
RET
```

Remove these exact old lines (physical positions 645–645 in `IR08.ASM`):

```asm
ARGONE:
```

Put this source in their place:

```asm
ARGNAME:
```

### Change 6: following `ARGUMENTS:`

Unchanged code immediately before the edit:

```asm
CMP AL,0
JE ARGZERO
CMP AL,1
```

Remove these exact old lines (physical positions 642–642 in `IR08.ASM`):

```asm
JNE ARGONE
```

Put this source in their place:

```asm
JNE ARGNAME
```

### Change 7: following `ARGUMENTS:`

Unchanged code immediately before the edit:

```asm
ARGUMENTS:
MOV AL,[CLASS]
CMP AL,0
```

Remove these exact old lines (physical positions 640–640 in `IR08.ASM`):

```asm
JE ARGZERO
```

Put this source in their place:

```asm
JE ARGDONE
```

### Change 8: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 484–484 in `IR08.ASM`):

```asm
MOV CX,5
```

Put this source in their place:

```asm
MOV CX,6
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR09` at ASM0's `Source name:` prompt. Require `OK 01826 bytes` followed by PASS. This builds `IR09.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T09.IR` with `COPY CON T09.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
WORD TOTAL 7
LABEL MAIN
HALT
```

```dos
CHECK IR09
```

Enter `T09` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T09
OK T09.ASM 00125 text bytes
PASS
```

Run `TYPE T09.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_TOTAL:
DW 7
U_MAIN:
MOV AX,4C00H
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T09`. Require `OK 00022 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T09.COM`, and require length **22 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 02 00 07
00 B8 00 4C CD 21
```

`T09.COM` is a complete program. Run `CHECK T09`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X09.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
WORD TOTAL 0
```

Run `CHECK IR09` and enter `X09`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 1
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the record stride and count, the saved template pointer, and each substitution buffer. The name and numeric token must survive FINISH. Compare the generated assembly before asking ASM0 to assemble it.
