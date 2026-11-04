+++
title = "06 \u00b7 Substituting a name"
weight = 6
description = "Save one checked name and insert it behind a safe prefix."
download = "IR06.ASM"
+++

A fixed text pattern cannot name a program location. We shall give a template a checked name to insert.

## How it works

NAMEARG scans and validates a name, then copies it to 2500H while preserving the source cursor. A name begins with a letter or underscore and continues with letters, digits, or underscores. Its maximum is fourteen characters, leaving room for U_ within ASM86's name bound.

An @ in a template substitutes the saved name. EXPAND saves SI while OUTTEXT reads the saved name, then restores SI to resume the template. LABEL emits U_name and a colon on a standalone assembly line. An IR name such as AX is harmless because U_AX is not a register.

This checkpoint has no enforced MAIN entry point or declaration area. A label emits no bytes; execution still starts at the first emitted instruction. The test places a label before NOP and HALT, and NAMEARG rejects a name beginning with a digit.

## Source changes

Copy `IR05.ASM` to `IR06.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_NOP:`

Unchanged code immediately before the edit:

```asm

T_NOP:
DB 78,79,80,13,10,0
```

Insert after old physical line 568, before the following old line.

Insert this source:

```asm

T_LABEL:
DB 85,95,64,58,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_NOP
DB 72,65,76,84,0,0,0,0,0,5,5,0
DW T_HALT
```

Insert after old physical line 481, before the following old line.

Insert this source:

```asm
DB 76,65,66,69,76,0,0,0,3,3,0,0
DW T_LABEL
```

### Change 3: following `EXPANDDONE:`

Unchanged code immediately before the edit:

```asm
CALL EMITCHAR
JMP EXPAND
EXPANDDONE:
```

Insert after old physical line 465, before the following old line.

Insert this source:

```asm
RET

NAMEARG:
CALL SCAN
MOV AX,[TOKLEN]
CMP AX,14
JBE NAMELENGTH
JMP BADIRNAME
NAMELENGTH:
CALL VALIDNAME
PUSH SI
MOV SI,2300H
MOV DI,2500H
CALL COPYZ
POP SI
RET
BADIRNAME:
MOV AX,3
JMP ERROR

ARGUMENTS:
MOV AL,[CLASS]
CMP AL,0
JE ARGZERO
CALL NAMEARG
ARGZERO:
```

### Change 4: following `EXPAND:`

Unchanged code immediately before the edit:

```asm
JE EXPANDDONE
CALL EMITCHAR
JMP EXPAND
```

Insert after old physical line 464, before the following old line.

Insert this source:

```asm
EXPANDNAME:
PUSH SI
MOV SI,2500H
CALL OUTTEXT
POP SI
JMP EXPAND
```

### Change 5: following `EXPAND:`

Unchanged code immediately before the edit:

```asm
LODSB
CMP AL,0
JE EXPANDDONE
```

Insert after old physical line 462, before the following old line.

Insert this source:

```asm
CMP AL,64
JE EXPANDNAME
```

### Change 6: following `TEXTFULL:`

Unchanged code immediately before the edit:

```asm
MOV AX,5
JMP ERROR

```

Insert after old physical line 458, before the following old line.

Insert this source:

```asm
OUTTEXT:
LODSB
CMP AL,0
JE OUTDONE
CALL EMITCHAR
JMP OUTTEXT
OUTDONE:
RET

```

### Change 7: following `STATLAST:`

Unchanged code immediately before the edit:

```asm
MOV AL,1
STATLAST:
MOV [LAST],AL
```

Insert after old physical line 397, before the following old line.

Insert this source:

```asm
CALL ARGUMENTS
```

### Change 8: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 371–371 in `IR05.ASM`):

```asm
MOV CX,2
```

Put this source in their place:

```asm
MOV CX,3
```

### Change 9: following `LOOKMISS:`

Unchanged code immediately before the edit:

```asm
POP SI
RET

```

Insert after old physical line 279, before the following old line.

Insert this source:

```asm
VALIDNAME:
PUSH SI
MOV SI,2300H
LODSB
CMP AL,95
JE NAMEVALID
CMP AL,65
JB SYMBOLBAD
CMP AL,90
JA SYMBOLBAD
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
JBE NAMEVALID
JMP SYMBOLBAD
NAMEVALIDEND:
POP SI
RET
SYMBOLBAD:
MOV AX,3
JMP ERROR

```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR06` at ASM86's `Source name:` prompt. Require `OK 01311 bytes` followed by PASS. This builds `IR06.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T06.IR` with `COPY CON T06.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL START
NOP
HALT
```

```dos
CHECK IR06
```

Enter `T06` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T06
OK T06.ASM 00038 text bytes
PASS
```

Run `TYPE T06.ASM`. Its complete text must be:

```asm
U_START:
NOP
MOV AX,4C00H
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T06`. Require `OK 00006 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T06.COM`, and require length **6 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
90 B8 00 4C CD 21
```

`T06.COM` is a complete program. Run `CHECK T06`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X06.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL 1BAD
HALT
```

Run `CHECK IR06` and enter `X06`. Require this diagnostic and FAIL:

```text
IR ERROR 00001 CODE 3
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the record stride and count, the saved template pointer, and each substitution buffer. The name and numeric token must survive FINISH. Compare the generated assembly before asking ASM86 to assemble it.
