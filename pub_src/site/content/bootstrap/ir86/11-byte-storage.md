+++
title = "11 \u00b7 Byte storage"
weight = 11
description = "Check byte initializers and clear the high half of a byte load."
download = "IR11.ASM"
+++

Text and file input are bytes. BYTE, LDB, and STB make that width explicit without changing the word accumulator.

## How it works

BYTE declares one initialized byte and refuses an initializer above 255. The common number reader still returns a word; the declaration handler applies the narrower range. STB writes AL and retains AX. LDB loads AL and then clears AH, returning a value from zero through 255.

The same U_ namespace is used for byte and word storage. Width belongs to the operation, not a type inferred from the name. A word access to the last byte of a buffer can reach adjacent storage; the translator cannot protect such a runtime access.

The test replaces the initialized byte with zero, disturbs AX, and loads the byte again. Inspect the emitted MOV AH,0 as well as the zero exit status: it is the operation which makes a byte load an unsigned word result.

## Source changes

Copy `IR10.ASM` to `IR11.ASM`. Make these edits **from the bottom of the old file upward**, in the order printed. Physical line positions count blank lines and are only locators. The nearby label and unchanged context identify each place; retain everything else.

### Change 1: following `T_ST:`

Unchanged code immediately before the edit:

```asm

T_ST:
DB 77,79,86,32,91,85,95,64,93,44,65,88,13,10,0
```

Insert after old physical line 845, before the following old line.

Insert this source:

```asm

T_BYTE:
DB 85,95,64,58,13,10,68,66,32,35,13,10,0

T_LDB:
DB 77,79,86,32,65,76,44,91,85,95,64,93,13,10,77,79
DB 86,32,65,72,44,48,13,10,0

T_STB:
DB 77,79,86,32,91,85,95,64,93,44,65,76,13,10,0
```

### Change 2: following `OPTAB:`

Unchanged code immediately before the edit:

```asm
DW T_LD
DB 83,84,0,0,0,0,0,0,2,0,4,0
DW T_ST
```

Insert after old physical line 726, before the following old line.

Insert this source:

```asm
DB 66,89,84,69,0,0,0,0,4,0,1,0
DW T_BYTE
DB 76,68,66,0,0,0,0,0,2,0,6,0
DW T_LDB
DB 83,84,66,0,0,0,0,0,2,0,4,0
DW T_STB
```

### Change 3: following `ARGNAME:`

Unchanged code immediately before the edit:

```asm
CMP AL,6
JA ARGDONE
CALL NUMARG
```

Insert after old physical line 652, before the following old line.

Insert this source:

```asm
MOV AL,[CLASS]
CMP AL,4
JNE ARGDONE
MOV AX,[NUMV]
CMP AX,255
JBE ARGDONE
JMP ARGRANGE
```

### Change 4: following `STATWORD:`

Unchanged code immediately before the edit:

```asm
RET
STATWORD:
MOV BX,OPTAB
```

Remove these exact old lines (physical positions 484–484 in `IR10.ASM`):

```asm
MOV CX,8
```

Put this source in their place:

```asm
MOV CX,11
```

## Build the checkpoint

```dos
CHECK ASMKEEP
```

Enter `IR11` at ASM86's `Source name:` prompt. Require `OK 02001 bytes` followed by PASS. This builds `IR11.COM` directly with the completed assembler. Save the source and executable before running the test.

Create `T11.IR` with `COPY CON T11.IR`, enter this text, and finish with Ctrl-Z and Enter. The Ctrl-Z keystroke ends console input; it is not a printed language token.

```ir
BYTE LETTER 65
LABEL MAIN
LIT 0
STB LETTER
LIT 65535
LDB LETTER
EXIT
```

```dos
CHECK IR11
```

Enter `T11` at `IR source name:`. Apart from DOS echo and the checker's separating blank line, require:

```text
IR source name: T11
OK T11.ASM 00197 text bytes
PASS
```

Run `TYPE T11.ASM`. Its complete text must be:

```asm
CLD
CMP SP,0FFFEH
JE I_ENTRY
MOV AX,4C07H
INT 21H
I_ENTRY:
JMP U_MAIN
U_LETTER:
DB 65
U_MAIN:
MOV AX,0
MOV [U_LETTER],AL
MOV AX,65535
MOV AL,[U_LETTER]
MOV AH,0
MOV AH,4CH
INT 21H
```

Assemble that generated source with `CHECK ASMKEEP`, entering `T11`. Require `OK 00036 bytes` and PASS. The text-byte count above includes CR/LF and is distinct from this machine-image count.

Run `GWBASIC VIEW.BAS`, enter `T11.COM`, and require length **36 bytes** with these hexadecimal bytes. Use `SYSTEM` afterward to return to DOS.

```text
FC 81 FC FE FF 74 05 B8 07 4C CD 21 E9 01 00 41
B8 00 00 88 06 0F 01 B8 FF FF 8A 06 0F 01 B4 00
B4 4C CD 21
```

`T11.COM` is a complete program. Run `CHECK T11`. It returns zero and the checker reports PASS.

## A rejection check

Enter this separate input as `X11.IR` using COPY CON and the same end-of-input keystroke:

```ir
BYTE LETTER 256
LABEL MAIN
HALT
```

Run `CHECK IR11` and enter `X11`. Require this diagnostic and FAIL:

```text
IR ERROR 00001 CODE 4
FAIL
```

An unexpected PASS is a failed rejection test. Require a fresh OK before using assembly output; a source error leaves an older .ASM untouched.

## If the result differs

Check the record stride and count, the saved template pointer, and each substitution buffer. The name and numeric token must survive FINISH. Compare the generated assembly before asking ASM86 to assemble it.
