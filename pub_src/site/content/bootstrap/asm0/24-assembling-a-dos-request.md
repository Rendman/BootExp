+++
title = "24 \u00b7 Assembling a DOS request"
weight = 24
description = "Emit CDH and a checked interrupt number."
download = "AS24.ASM"
aliases = ["/bootstrap/asm86/25-assembling-a-dos-request/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/24-assembling-a-dos-request/"
+++

I've already used BOOTASM to make a character appear on the screen. This time I want the new assembler to translate the `MOV` and `INT` instructions itself. I'll still use BOOTASM to build that assembler before asking it to assemble the test program.

**Starting source:** `AS23.ASM`. **Save as:** `AS24.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

INTERRUPT reads one value, saves AX while it emits CDH, then passes the restored value through BYTEVALUE. That bound check is essential: the interrupt number occupies one byte. FINISH rejects another token.

In the test, DL holds Z and AH holds function 02H. INT 21H displays the character. Loading AX with 4C00H then requests function 4CH with a zero return code in AL. The source is a complete executable, unlike the earlier encoding fixtures.

INTERRUPT changes VALUE's scratch registers, AX, PC, OUTPTR, and flags. Its temporary saved AX costs two stack bytes. The interrupt instruction itself causes the processor to save flags, CS, and IP while the service runs; the caller must use the documented DOS register interface, not treat a software interrupt as an ordinary subroutine.

## Source changes

Copy `AS23.ASM` to `AS24.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

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
DB 73,78,67,0,0,0,5,64
DB 68,69,67,0,0,0,5,72
DB 80,85,83,72,0,0,5,80
DB 80,79,80,0,0,0,5,88
```

The edit begins immediately after that unchanged block.

Insert:

```asm
DB 73,78,84,0,0,0,6,205
```

### Change 2 · `SINGLE:`

Find the unique label `SINGLE:`, then follow this unchanged source through its last displayed instruction:

```asm
SINGLE:
CALL SCAN
CALL REGISTER
CMP AX,8
JB SYNTAXBAD
CMP AX,15
JA SYNTAXBAD
SUB AL,8
MOV DL,[OP]
ADD AL,DL
CALL EMIT
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CALL FINISH
RET
INTERRUPT:
CALL SCAN
CALL VALUE
PUSH AX
MOV AL,205
CALL EMIT
POP AX
CALL BYTEVALUE
```

### Change 3 · `STNEXT5:`

Find the unique label `STNEXT5:`, then follow this unchanged source through its last displayed instruction:

```asm
STNEXT5:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CMP AL,6
JNE STNEXT6
CALL INTERRUPT
RET
STNEXT6:
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
MOV CX,11
```

With:

```asm
MOV CX,12
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS24.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1943 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS24.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T24.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
MOV DL,5AH
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

```dos
COPY T24.ASM SOURCE.ASM
```

```dos
CHECK AS24
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00011 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **11 bytes** with these hexadecimal bytes:

```text
B2 5A B4 02 CD 21 B8 00 4C CD 21
```

Use `SYSTEM` to return to DOS.

`RESULT.COM` is also a complete executable. Preserve it with `COPY RESULT.COM T24.COM`, then run `CHECK T24`. It displays `Z` followed by the checker's blank line and `PASS`.

The `Z` comes from the program ASM0 assembled. I have followed two separate translations: BOOTASM built AS24.COM, and AS24.COM built the little DOS program. I keep both source files with their accepted executables.

## A rejection check

Enter this separate file as `X24.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
INT 256
```

```dos
COPY X24.ASM SOURCE.ASM
CHECK AS24
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Save the interrupt value while emitting CDH, then restore it for BYTEVALUE. The runnable test must load AH for each DOS service and finish with AX=4C00H.
