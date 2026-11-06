+++
title = "08 \u00b7 Loading an unsigned word"
weight = 8
description = "Load a checked word into the virtual accumulator."
download = "IR08.ASM"
download_group = "tools/ir86"
reader_names = 1
+++

The accumulator needs a value. LIT supplies an unsigned word, and EXIT makes its low byte observable as a program status.

## Operation and backend

A is the virtual IR accumulator. This backend represents A in AX. LIT emits MOV AX,value. NUMARG uses the published unsigned decimal and hexadecimal reader, saves the numeric result in NUMV, and copies its checked spelling to 2520H. The # template marker inserts that spelling. VALUE preserves SI; AX, BX, CX, DX, DI, BP, and flags are scratch.

Numbers range from zero through 65535. Hexadecimal ends in H and begins with a decimal digit, as in 0FFH. Signs, expressions, and character literals are excluded so the translator can validate one token without evaluating a language expression.

EXIT returns A modulo 256 as the program status. HALT returns zero. The DOS binding implements these operations with its termination service. EXIT is therefore suitable for testing a computed zero result; a nonzero low byte deliberately produces the checker's FAIL report. Arithmetic words and DOS status bytes have different widths.

## Source changes

Copy `IR07.ASM` to `IR08.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

VALUE is the unsigned numeric reader from the published ASM0 source, with a nonnumeric token directed to NUMBERBAD. Copy its routine block if convenient, then compare the complete addition below. It accepts numeric tokens only in this translator.

### Change 1: following `T_LABEL:`

Unchanged code immediately before the edit:

```asm

T_LABEL:
DB 85,95,64,58,13,10,0
```

Insert after old physical line 710, before the following old line.

Insert this source:

```asm

T_LIT:
DB 77,79,86,32,65,88,44,35,13,10,0

T_EXIT:
DB 77,79,86,32,65,72,44,52,67,72,13,10,73,78,84,32
DB 50,49,72,13,10,0
```

### Change 2: following `SPACE:`

Unchanged code immediately before the edit:

```asm
SPACE:
DB 32,36

```

Insert after old physical line 676, before the following old line.

Insert this source:

```asm
NUMV:
DW 0

```

### Change 3: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_HALT
DB 76,65,66,69,76,0,0,0,3,3,0,0
DW T_LABEL
```

Insert after old physical line 610, before the following old line.

Insert this source:

```asm
DB 76,73,84,0,0,0,0,0,1,0,3,0
DW T_LIT
DB 69,88,73,84,0,0,0,0,0,5,4,0
DW T_EXIT
```

### Change 4: following `ARGUMENTS:`

Unchanged code immediately before the edit:

```asm
MOV AL,[CLASS]
CMP AL,0
JE ARGZERO
```

Insert after old physical line 548, before the following old line.

Insert this source:

```asm
CMP AL,1
JNE ARGONE
CALL NUMARG
RET
ARGONE:
```

### Change 5: following `BADIRNAME:`

Unchanged code immediately before the edit:

```asm
MOV AX,3
JMP ERROR

```

Insert after old physical line 544, before the following old line.

Insert this source:

```asm
NUMARG:
CALL SCAN
CALL VALUE
MOV [NUMV],AX
PUSH SI
MOV SI,2300H
MOV DI,2520H
CALL COPYZ
POP SI
RET

```

### Change 6: following `EXPANDNAME:`

Unchanged code immediately before the edit:

```asm
EXPANDNAME:
PUSH SI
MOV SI,2500H
```

Insert after old physical line 520, before the following old line.

Insert this source:

```asm
CALL OUTTEXT
POP SI
JMP EXPAND
EXPANDNUMBER:
PUSH SI
MOV SI,2520H
```

### Change 7: following `EXPAND:`

Unchanged code immediately before the edit:

```asm
JE EXPANDDONE
CMP AL,64
JE EXPANDNAME
```

Insert after old physical line 515, before the following old line.

Insert this source:

```asm
CMP AL,35
JE EXPANDNUMBER
```

### Change 8: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 411–411 in `IR07.ASM`):

```asm
MOV CX,3
```

Put this source in their place:

```asm
MOV CX,5
```

### Change 9: following `SYMBOLBAD:`

Unchanged code immediately before the edit:

```asm
MOV AX,3
JMP ERROR

```

Insert after old physical line 319, before the following old line.

Insert this source:

```asm
VALUE:
MOV AL,[2300H]
CMP AL,48
JB WORDVALUE
CMP AL,57
JBE LITERAL
WORDVALUE:
JMP NUMBERBAD
LITERAL:
PUSH SI
MOV SI,2300H
MOV DI,[TOKLEN]
ADD DI,2300H
MOV BX,DI
DEC BX
MOV AL,[BX]
MOV BP,10
CMP AL,72
JNE NUMBERSTART
MOV BP,16
DEC DI
NUMBERSTART:
CMP SI,DI
JE NUMBERBAD
MOV CX,0
DIGIT:
LODSB
SUB AL,48
CMP AL,9
JBE DIGITOK
SUB AL,7
CMP AL,10
JB NUMBERBAD
CMP AL,15
JA NUMBERBAD
DIGITOK:
MOV AH,0
MOV DX,AX
CMP DX,BP
JAE NUMBERBAD
CMP BP,16
JE HEXDIGIT
CMP CX,6553
JA NUMBERBAD
JB DECDIGIT
CMP DX,5
JA NUMBERBAD
DECDIGIT:
MOV AX,CX
ADD CX,CX
ADD AX,AX
ADD AX,AX
ADD AX,AX
ADD CX,AX
JMP ADDDIGIT
HEXDIGIT:
CMP CX,4095
JA NUMBERBAD
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADD CX,CX
ADDDIGIT:
ADD CX,DX
CMP SI,DI
JB DIGIT
MOV AX,CX
POP SI
RET
NUMBERBAD:
MOV AX,2
JMP ERROR

```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR08` at ASM0's `Source name:` prompt. Require `OK 01776 bytes` followed by PASS. This builds `IR08.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T08.IR` with `COPY CON T08.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
LABEL MAIN
LIT 0
EXIT
```

```dos
CHECK IR08
```

Enter `T08` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T08
OK T08.ASM 00117 text bytes
PASS
```

Run `TYPE T08.ASM`. Its complete text must be:

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
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T08`. Require `OK 00022 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T08.COM`, and require length **22 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 00 00 B8
00 00 B4 4C CD 21
```

`T08.COM` is a complete program. Run `CHECK T08`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X08.IR` using COPY CON and the same end-of-input keystroke:

```ir
LABEL MAIN
LIT 65536
```

Run `CHECK IR08` and enter `X08`. Require this diagnostic and FAIL:

```text
IR ERROR 00002 CODE 2
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the record stride and count, the saved template pointer, and each substitution buffer. The name and numeric token must survive FINISH. Compare the generated assembly before asking ASM0 to assemble it.
