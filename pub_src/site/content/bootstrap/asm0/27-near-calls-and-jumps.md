+++
title = "27 \u00b7 Near calls and jumps"
weight = 27
description = "Subtract the address after the three-byte instruction."
download = "AS27.ASM"
aliases = ["/bootstrap/asm86/28-near-calls-and-jumps/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/27-near-calls-and-jumps/"
+++

I've been writing `CALL` and `JMP` in ASM0's implementation all along, because BOOTASM can assemble them. ASM0 itself still cannot read those instructions. I want its accepted language to catch up with the source I'm using to write it.

**Starting source:** `AS26.ASM`. **Save as:** `AS27.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

Class seven carries E8H for CALL or E9H for JMP. NEARJUMP reads the destination, subtracts PC plus three, and emits the opcode and a word displacement. The 8086/8088 subtraction already wraps into the unsigned sixteen-bit pattern needed for a backward transfer.

CALL pushes the offset of the following instruction. RET takes that offset back from the stack; a routine must restore its own saved words first. JMP pushes nothing. Neither transfer changes arithmetic flags by itself, although a called routine may do so.

NEARJUMP preserves the computed displacement on the stack while emitting the opcode. It changes VALUE's scratch state, AX, DX, PC, OUTPTR, and flags. Every accepted near transfer is three bytes. Far calls, indirect transfers, and automatic short-JMP selection are omitted because this workbench uses one .COM segment and fixed instruction sizes.

The complete test calls SAY, which displays C, then returns to the termination code. SAY begins five bytes beyond the return address, so the CALL displacement is 0005H.

## Source changes

Copy `AS26.ASM` to `AS27.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

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
```

The edit begins immediately after that unchanged block.

Insert:

```asm
DB 67,65,76,76,0,0,7,232
DB 74,77,80,0,0,0,7,233
```

### Change 2 · `INTERRUPT:`

Find the unique label `INTERRUPT:`, then follow this unchanged source through its last displayed instruction:

```asm
INTERRUPT:
CALL SCAN
CALL VALUE
PUSH AX
MOV AL,205
CALL EMIT
POP AX
CALL BYTEVALUE
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CALL FINISH
RET
NEARJUMP:
CALL SCAN
CALL VALUE
MOV DX,[PC]
ADD DX,3
SUB AX,DX
PUSH AX
MOV AL,[OP]
CALL EMIT
POP AX
CALL EMITWORD
```

### Change 3 · `STNEXT6:`

Find the unique label `STNEXT6:`, then follow this unchanged source through its last displayed instruction:

```asm
STNEXT6:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CMP AL,7
JNE STNEXT7
CALL NEARJUMP
RET
STNEXT7:
```

### Change 4 · `INSTRUCTION:`

Find the unique label `INSTRUCTION:`, then follow this unchanged source through its last displayed instruction:

```asm
INSTRUCTION:
DEC SI
MOV BX,OPTAB
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
MOV CX,17
```

With:

```asm
MOV CX,19
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS27.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 2315 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS27.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T27.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
CALL SAY
MOV AX,4C00H
INT 21H
SAY:
MOV DL,43H
MOV AH,2
INT 21H
RET
```

```dos
COPY T27.ASM SOURCE.ASM
```

```dos
CHECK AS27
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00015 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **15 bytes** with these hexadecimal bytes:

```text
E8 05 00 B8 00 4C CD 21 B2 43 B4 02 CD 21 C3
```

Use `SYSTEM` to return to DOS.

`RESULT.COM` is also a complete executable. Preserve it with `COPY RESULT.COM T27.COM`, then run `CHECK T27`. It displays `C` followed by the checker's blank line and `PASS`.

## A rejection check

Enter this separate file as `X27.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
CALL LOST
```

```dos
COPY X27.ASM SOURCE.ASM
CHECK AS27
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 3
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Compute the displacement from PC plus three and retain it while emitting E8H or E9H. For CALL, the called routine must restore its saved words before RET uses the return offset.
