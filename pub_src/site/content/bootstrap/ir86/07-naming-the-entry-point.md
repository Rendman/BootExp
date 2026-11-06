+++
title = "07 \u00b7 Naming the entry point"
weight = 7
description = "Prefix names and require MAIN before executable statements."
download = "IR07.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

A source needs an entry point and a namespace which cannot collide with registers or translator labels.

## Operation and backend

NAMEARG scans and validates a name, then copies it to 2500H while preserving the line cursor. Names begin with a letter or underscore and contain letters, digits, or underscores. Their limit is fourteen characters: the emitted U_ prefix must still fit ASM0's sixteen-character label limit. Register spellings can be IR names because the prefix keeps them distinct.

The @ character in a template inserts that saved name. EXPAND saves SI while OUTTEXT walks the substitution, then resumes the template. LABEL emits a standalone U_name definition. CONTEXT requires the first executable label to be MAIN; ordinary executable statements require that code context.

The header clears direction, checks the full-segment entry stack, and jumps over the declaration area to U_MAIN. A smaller entry stack returns status seven. I_ENTRY belongs to the translator's namespace. The final source must contain MAIN; missing names and duplicate definitions in emitted assembly remain ASM0 diagnostics.

## Source changes

Copy `IR06.ASM` to `IR07.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `LAST:`

Unchanged code immediately before the edit:

```asm

LAST:
DB 0
```

Insert after old physical line 639, before the following old line.

Insert this source:

```asm

T_HEADER:
DB 67,76,68,13,10,67,77,80,32,83,80,44,48,70,70,70
DB 69,72,13,10,74,69,32,73,95,69,78,84,82,89,13,10
DB 77,79,86,32,65,88,44,52,67,48,55,72,13,10,73,78
DB 84,32,50,49,72,13,10,73,95,69,78,84,82,89,58,13
DB 10,74,77,80,32,85,95,77,65,73,78,13,10,0
```

### Change 2: following `INSIZE:`

Unchanged code immediately before the edit:

```asm
INSIZE:
DB 0

```

Insert after old physical line 637, before the following old line.

Insert this source:

```asm
CODE:
DB 0

```

### Change 3: following `ARGZERO:`

Unchanged code immediately before the edit:

```asm
ARGZERO:
RET

```

Insert after old physical line 543, before the following old line.

Insert this source:

```asm
CONTEXT:
MOV AL,[CLASS]
CMP AL,4
JB CODECONTEXT
CMP AL,6
JA CODECONTEXT
MOV AL,[CODE]
CMP AL,0
JE CONTEXTDONE
JMP BADCONTEXT
CODECONTEXT:
MOV AL,[CLASS]
CMP AL,3
JE LABELCONTEXT
MOV AL,[CODE]
CMP AL,1
JE CONTEXTDONE
JMP BADCONTEXT
LABELCONTEXT:
MOV AL,[CODE]
CMP AL,1
JE CONTEXTDONE
MOV AX,[2500H]
CMP AX,414DH
JNE MAINBAD
MOV AX,[2502H]
CMP AX,4E49H
JNE MAINBAD
MOV AL,[2504H]
CMP AL,0
JNE MAINBAD
MOV AL,1
MOV [CODE],AL
CONTEXTDONE:
RET
BADCONTEXT:
MOV AX,1
JMP ERROR
MAINBAD:
MOV AX,3
JMP ERROR

```

### Change 4: following `STATLAST:`

Unchanged code immediately before the edit:

```asm
MOV [LAST],AL
CALL ARGUMENTS
CALL FINISH
```

Insert after old physical line 431, before the following old line.

Insert this source:

```asm
CALL CONTEXT
```

### Change 5: following `DRIVERDONE:`

Unchanged code immediately before the edit:

```asm
JMP DRIVERLINE
DRIVERDONE:
CALL CLOSEFILE
```

Insert after old physical line 21, before the following old line.

Insert this source:

```asm
MOV AL,[CODE]
CMP AL,1
JE MAINPRESENT
MOV AX,3
JMP ERROR
MAINPRESENT:
```

### Change 6: following `ROOM:`

Unchanged code immediately before the edit:

```asm
CALL GETNAME
MOV AX,6000H
MOV [OUTPTR],AX
```

Insert after old physical line 11, before the following old line.

Insert this source:

```asm
MOV SI,T_HEADER
CALL OUTTEXT
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR07` at ASM0's `Source name:` prompt. Require `OK 01518 bytes` followed by PASS. This builds `IR07.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T07.IR` with `COPY CON T07.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
HALT
```

```dos
CHECK IR07
```

Enter `T07` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T07
OK T07.ASM 00109 text bytes
PASS
```

Run `TYPE T07.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_MAIN:
MOV AX,4C00H
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T07`. Require `OK 00020 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T07.COM`, and require length **20 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
00 4C CD 21
```

`T07.COM` is a complete program. Run `CHECK T07`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X07.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL START
HALT
```

Run `CHECK IR07` and enter `X07`. Require this diagnostic and FAIL:

```text
IR ERROR 00001 CODE 3
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the record stride and count, the saved template pointer, and each substitution buffer. The name and numeric token must survive FINISH. Compare the generated assembly before asking ASM0 to assemble it.
