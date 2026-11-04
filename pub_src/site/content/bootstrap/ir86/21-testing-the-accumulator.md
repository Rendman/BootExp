+++
title = "21 \u00b7 Testing the accumulator"
weight = 21
description = "Lower a conditional transfer through a nearby opposite branch."
download = "IR21.ASM"
cartoon = "ir86-lock.png"
+++

A conditional transfer must reach any label in the bounded image, even though an 8088 conditional branch is short.

## How it works

JZ compares AX with zero, branches around a near JMP when the condition is false, and otherwise takes that near JMP. JNZ uses the opposite short condition. AX is retained, the expression stack must be empty, and arithmetic flags are scratch.

A ? in the template inserts the current branch number as four decimal digits. FOUR preserves all word registers while sending those digits through EMITCHAR. BRANCHNO advances once per conditional statement, and every repeated ? in that pattern uses the same value. Labels I0001 and so forth are separate from all U_ names.

NEWDEF counts the generated skip label as well as user definitions. The only short displacement is across the near JMP itself, so a distant user target cannot overflow that short branch. The test takes its zero branch and avoids a nonzero exit.

## Source changes

Copy `IR20.ASM` to `IR21.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_JMP:`

Unchanged code immediately before the edit:

```asm

T_JMP:
DB 74,77,80,32,85,95,64,13,10,0
```

Insert after old physical line 1109, before the following old line.

Insert this source:

```asm

T_JZ:
DB 67,77,80,32,65,88,44,48,13,10,74,78,69,32,73,63
DB 13,10,74,77,80,32,85,95,64,13,10,73,63,58,13,10
DB 0

T_JNZ:
DB 67,77,80,32,65,88,44,48,13,10,74,69,32,73,63,13
DB 10,74,77,80,32,85,95,64,13,10,73,63,58,13,10,0
```

### Change 2: following `OUTLINES:`

Unchanged code immediately before the edit:

```asm
DW 0

OUTLINES:
```

Insert after old physical line 992, before the following old line.

Insert this source:

```asm
DW 0

BRANCHNO:
```

### Change 3: following `CRLF:`

Unchanged code immediately before the edit:

```asm
CRLF:
DB 13,10,0

```

Insert after old physical line 976, before the following old line.

Insert this source:

```asm
FOURDIV:
DW 1000,100,10,1
FOUREND:

```

### Change 4: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_BUFFER
DB 74,77,80,0,0,0,0,0,2,5,3,0
DW T_JMP
```

Insert after old physical line 907, before the following old line.

Insert this source:

```asm
DB 74,90,0,0,0,0,0,0,7,3,9,0
DW T_JZ
DB 74,78,90,0,0,0,0,0,7,3,9,0
DW T_JNZ
```

### Change 5: following `EXPANDDONE:`

Unchanged code immediately before the edit:

```asm
POP SI
JMP EXPAND
EXPANDDONE:
```

Insert after old physical line 634, before the following old line.

Insert this source:

```asm
RET

FOUR:
PUSH AX
PUSH BX
PUSH CX
PUSH DX
PUSH SI
MOV CX,AX
MOV SI,FOURDIV
FOURPLACE:
MOV BX,SI
MOV DX,[BX]
MOV AL,48
FOURSUB:
CMP CX,DX
JB FOURDIGIT
SUB CX,DX
ADD AL,1
JMP FOURSUB
FOURDIGIT:
CALL EMITCHAR
ADD SI,2
CMP SI,FOUREND
JB FOURPLACE
POP SI
POP DX
POP CX
POP BX
POP AX
```

### Change 6: following `EXPANDNUMBER:`

Unchanged code immediately before the edit:

```asm
CALL OUTTEXT
POP SI
JMP EXPAND
```

Insert after old physical line 633, before the following old line.

Insert this source:

```asm
EXPANDBRANCH:
MOV AX,[BRANCHNO]
CALL FOUR
JMP EXPAND
```

### Change 7: following `EXPAND:`

Unchanged code immediately before the edit:

```asm
JE EXPANDNAME
CMP AL,35
JE EXPANDNUMBER
```

Insert after old physical line 619, before the following old line.

Insert this source:

```asm
CMP AL,63
JE EXPANDBRANCH
```

### Change 8: following `STATNODEF:`

Unchanged code immediately before the edit:

```asm
JA STATNODEF
CALL NEWDEF
STATNODEF:
```

Insert after old physical line 527, before the following old line.

Insert this source:

```asm
MOV AL,[CLASS]
CMP AL,7
JNE STATNOBRANCH
CALL NEWDEF
MOV AX,[BRANCHNO]
INC AX
MOV [BRANCHNO],AX
STATNOBRANCH:
```

### Change 9: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 489–489 in `IR20.ASM`):

```asm
MOV CX,25
```

Put this source in their place:

```asm
MOV CX,27
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR21` at ASM86's `Source name:` prompt. Require `OK 02980 bytes` followed by PASS. This builds `IR21.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T21.IR` with `COPY CON T21.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 0
JZ GOOD
LIT 1
EXIT
LABEL GOOD
LIT 0
EXIT
```

```dos
CHECK IR21
```

Enter `T21` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T21
OK T21.ASM 00208 text bytes
PASS
```

Run `TYPE T21.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_MAIN:
MOV AX,0
CMP AX,0
JNE I0001
JMP U_GOOD
I0001:
MOV AX,1
MOV AH,4CH
INT 21H
U_GOOD:
MOV AX,0
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T21`. Require `OK 00041 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T21.COM`, and require length **41 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
00 00 81 F8 00 00 75 03 E9 07 00 B8 01 00 B4 4C
CD 21 B8 00 00 B4 4C CD 21
```

`T21.COM` is a complete program. Run `CHECK T21`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X21.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
LIT 1
PUSH
JZ MAIN
```

Run `CHECK IR21` and enter `X21`. Require this diagnostic and FAIL:

```text
IR ERROR 00004 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check operand order and the opposite short condition in the pattern. All occurrences of ? in one pattern must use the same branch number. A DOS carry branch must immediately follow DOS apart from empty or comment lines.
