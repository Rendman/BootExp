+++
title = "11 \u00b7 Collecting output bytes"
weight = 11
description = "Count loaded offsets while retaining bytes in a separate buffer."
download = "AS11.ASM"
aliases = ["/bootstrap/asm86/12-collecting-output-bytes/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/11-collecting-output-bytes/"
+++

I can read values from the source and turn them into words in a register. Before I create an output file, I want somewhere to keep the bytes I have accepted. An error near the end of the source should not make me throw away a working program.

**Starting source:** `AS10.ASM`. **Save as:** `AS11.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

PC begins at 0100H, the loaded address of the first .COM byte. OUTPTR begins at 6000H, the location of the output buffer in the assembler's own segment. These are different addresses with different purposes. Every emitted byte advances both by one.

EMIT takes the byte in AL and preserves AX and BX. On pass two it stores the byte at OUTPTR; on pass one it only counts. The current driver sets PASS to two. The 2100H limit on PC allows 8192 output bytes and refuses the next byte before storing beyond the buffer.

BYTEVALUE takes a full value in AX. Values above 255 select code 4; otherwise it enters EMIT. The caller therefore cannot accidentally truncate a word into a byte. EMIT selects code 5 if the image is full. Its nested PUSH instructions use four stack bytes in addition to the call's return address.

This checkpoint accepts one numeric byte value per line, checks the end of each statement, and reports the count collected. It writes no .COM file yet. The distinction lets us test conversion and capacity without disk-output behavior.

## Source changes

Copy `AS10.ASM` to `AS11.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `ERRCODE:`

Find the unique label `ERRCODE:`, then follow this unchanged source through its last displayed instruction:

```asm
ERRCODE:
DB 0
```

The edit begins immediately after that unchanged block.

Insert:

```asm
BUFFERMSG:
DB 66,117,102,102,101,114,101,100,32,36
```

### Change 2 · `ENDED:`

Find the unique label `ENDED:`. Insert the new source immediately before this existing label:

```asm
ENDED:
```

Insert:

```asm
PASS:
DB 1
```

### Change 3 · `TOKLEN:`

Find the unique label `TOKLEN:`. Insert the new source immediately before this existing label:

```asm
TOKLEN:
```

Insert:

```asm
PC:
DW 256
OUTPTR:
DW 24576
```

### Change 4 · `ERRMSG:`

Find the unique label `ERRMSG:`. Insert the new source immediately before this existing label:

```asm
ERRMSG:
```

Insert:

```asm
BYTEMSG:
DB 32,98,121,116,101,115,13,10,36
```

### Change 5 · `TEXT:`

Find the unique label `TEXT:`. Insert the new source immediately before this existing label:

```asm
TEXT:
```

Insert:

```asm
BYTEVALUE:
CMP AX,255
JBE EMIT
MOV AX,4
JMP ERROR
EMIT:
PUSH AX
PUSH BX
MOV BX,[PC]
CMP BX,2100H
JAE IMAGEFULL
MOV AH,[PASS]
CMP AH,2
JNE COUNTBYTE
MOV BX,[OUTPTR]
MOV [BX],AL
COUNTBYTE:
MOV BX,[PC]
INC BX
MOV [PC],BX
MOV BX,[OUTPTR]
INC BX
MOV [OUTPTR],BX
POP BX
POP AX
RET
IMAGEFULL:
MOV AX,5
JMP ERROR
```

### Change 6 · `GOOD:`

Find the unique label `GOOD:`. Insert the new source immediately before this existing label:

```asm
GOOD:
```

Insert:

```asm
MOV DX,BUFFERMSG
CALL TEXT
MOV AX,[PC]
SUB AX,100H
CALL NUMBER
MOV DX,BYTEMSG
CALL TEXT
```

### Change 7 · `DRIVERLINE:`

Find the unique label `DRIVERLINE:`, then follow this unchanged source through its last displayed instruction:

```asm
DRIVERLINE:
CALL READLINE
CMP AX,0
JE DRIVERDONE
MOV SI,2200H
CALL SCAN
CALL VALUE
PUSH AX
CALL FINISH
```

The edit begins immediately after that unchanged block.

Remove this existing source:

```asm
POP AX
CALL NUMBER
MOV DX,NEWLINE
CALL TEXT
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
CALL VALUE
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
PUSH AX
```

With:

```asm
CALL BYTEVALUE
```

### Change 9 · `ROOM:`

Find the unique label `ROOM:`, then follow this unchanged source through its last displayed instruction:

```asm
ROOM:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
MOV AL,2
MOV [PASS],AL
MOV AX,100H
MOV [PC],AX
MOV AX,6000H
MOV [OUTPTR],AX
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS11.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 853 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS11.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T11.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
65
66
```

```dos
COPY T11.ASM SOURCE.ASM
```

```dos
CHECK AS11
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
Buffered 00002 bytes
PASS
```

## A rejection check

Enter this separate file as `X11.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
256
```

```dos
COPY X11.ASM SOURCE.ASM
CHECK AS11
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 4
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Keep target PC distinct from resident OUTPTR. EMIT must check capacity before storing, and BYTEVALUE must reject a word above 255 before copying AL. This checkpoint reports a count without writing RESULT.COM.
