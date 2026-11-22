+++
title = "09 \u00b7 Unsigned decimal values"
weight = 9
description = "Check every digit before multiplying the accumulated value."
download = "AS09.ASM"
aliases = ["/bootstrap/asm86/10-unsigned-decimal-values/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/09-unsigned-decimal-values/"
+++

A token of decimal digits must become a word without accepting a sign, an expression, or an overflow.

**Starting source:** `AS08.ASM`. **Save as:** `AS09.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

VALUE takes the token at 2300H and returns its unsigned value in AX. It preserves the source cursor SI by saving it on the stack. The numeric work uses CX as the accumulated value, DX as the next digit, and DI as the end of the token. AX, BX, CX, DX, DI, BP, and flags are scratch state.

Each character must lie between the codes for 0 and 9. Before multiplying, the accumulated value must be below 6553, or exactly 6553 with a final digit no greater than five. That check admits 65535 and rejects the next value before arithmetic can wrap.

Multiplication by ten is eight times the old value plus twice the old value. ADD performs those doublings with instructions BOOTASM already accepts. This keeps the routine's implementation vocabulary small; it does not imply the CPU lacks a multiply instruction.

The diagnostic driver reads one number per line. It saves AX while FINISH checks that no extra token follows, then prints the result. Empty values, malformed digits, and overflow select code 2. Only decimal numbers are accepted by this checkpoint.

## Source changes

Copy `AS08.ASM` to `AS09.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OPTAB:`

Find the unique label `OPTAB:`. The old block below starts at that label.

Remove this existing source:

```asm
OPTAB:
DB 68,66,0,0,0,0,1,0
DB 68,87,0,0,0,0,1,1
```

### Change 2 · `STRIDE:`

Find the unique label `STRIDE:`. The old block below starts at that label.

Remove this existing source:

```asm
STRIDE:
DW 0
```

Keep the following `ENDED:` label and the source after it in place.

### Change 3 · `LOOKMISS:`

Find the unique label `LOOKMISS:`. The old block below starts at that label.

Replace this existing source:

```asm
LOOKMISS:
MOV BX,0
POP SI
RET
```

With:

```asm
NUMBERBAD:
MOV AX,2
JMP ERROR
```

Keep the following `FINISH:` label and the source after it in place.

### Change 4 · `LOOKCHAR:`

Find the unique label `LOOKCHAR:`, then follow this unchanged source through its last displayed instruction:

```asm
LOOKCHAR:
LODSB
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV BX,DI
MOV DL,[BX]
CMP AL,DL
JNE LOOKSTEP
CMP AL,0
JE LOOKFOUND
INC DI
JMP LOOKCHAR
LOOKSTEP:
MOV AX,[STRIDE]
ADD BP,AX
DEC CX
JMP LOOKNEXT
LOOKFOUND:
MOV BX,BP
```

With:

```asm
SUB AL,48
CMP AL,9
JA NUMBERBAD
DIGITOK:
MOV AH,0
MOV DX,AX
CMP DX,BP
JAE NUMBERBAD
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
ADDDIGIT:
ADD CX,DX
CMP SI,DI
JB DIGIT
MOV AX,CX
```

### Change 5 · `LOOKCHAR:`

Find the unique label `LOOKCHAR:`. The old block below starts at that label.

Replace this existing source:

```asm
LOOKCHAR:
```

With:

```asm
MOV DI,[TOKLEN]
ADD DI,2300H
MOV BP,10
NUMBERSTART:
CMP SI,DI
JE NUMBERBAD
MOV CX,0
DIGIT:
```

### Change 6 · `LOOK:`

Find the unique label `LOOK:`, then follow this unchanged source through its last displayed instruction:

```asm
LOOK:
MOV [STRIDE],AX
PUSH SI
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
MOV BP,BX
LOOKNEXT:
CMP CX,0
JE LOOKMISS
MOV DI,BP
```

### Change 7 · `LOOK:`

Find the unique label `LOOK:`. The old block below starts at that label.

Replace this existing source:

```asm
LOOK:
MOV [STRIDE],AX
```

With:

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
```

### Change 8 · `DRIVERLINE:`

Find the unique label `DRIVERLINE:`, then follow this unchanged source through its last displayed instruction:

```asm
DRIVERLINE:
CALL READLINE
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
CALL SCAN
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV BX,OPTAB
MOV CX,2
MOV AX,8
CALL LOOK
CMP BX,0
JNE TRACEFOUND
MOV AX,1
JMP ERROR
TRACEFOUND:
ADD BX,7
MOV AL,[BX]
MOV AH,0
```

With:

```asm
CALL VALUE
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS09.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 678 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS09.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T09.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
42
65535
```

```dos
COPY T09.ASM SOURCE.ASM
```

```dos
CHECK AS09
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
00042
65535
PASS
```

## A rejection check

Enter this separate file as `X09.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
65536
```

```dos
COPY X09.ASM SOURCE.ASM
CHECK AS09
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 2
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check the decimal overflow comparison before multiplication and the final digit at 6553. VALUE must restore SI so FINISH can inspect the rest of the same statement.
