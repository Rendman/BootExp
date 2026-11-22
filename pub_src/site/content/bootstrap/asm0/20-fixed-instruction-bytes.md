+++
title = "20 \u00b7 Fixed instruction bytes"
weight = 20
description = "Five no-operand mnemonics use the same table dispatcher."
download = "AS20.ASM"
aliases = ["/bootstrap/asm86/21-fixed-instruction-bytes/"]
download_group = "tools/asm0"
reader_names = 1
url = "/bootstrap/asm86/20-fixed-instruction-bytes/"
+++

We shall add machine instructions whose complete encodings are one fixed byte each.

**Starting source:** `AS19.ASM`. **Save as:** `AS20.ASM`. **Build with:** `BOOTASM.BAS`.

## How it works

The new OPTAB records have class two and carry their opcode in the parameter byte. FIXED sends that byte through EMIT, then calls FINISH to reject an extra operand.

RET is the near return C3H. CLD is FCH and selects increasing indexes for string instructions. LODSB, ACH, loads AL from DS:SI and adjusts SI; STOSB, AAH, stores AL at ES:DI and adjusts DI. Their direction depends on the direction flag. They are plain, single instructions; no repeat prefix is accepted.

FIXED changes AL, PC, OUTPTR, and the scanner scratch state. It receives its opcode through OP and its argument cursor through SI. These encodings do not make the fixture safe to execute: its stack and index registers have not been prepared. Inspect the bytes only.

## Source changes

Copy `AS19.ASM` to `AS20.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `OPTAB:`

Find the unique label `OPTAB:`, then follow this unchanged source through its last displayed instruction:

```asm
OPTAB:
DB 68,66,0,0,0,0,1,0
DB 68,87,0,0,0,0,1,1
```

The edit begins immediately after that unchanged block.

Insert:

```asm
DB 82,69,84,0,0,0,2,195
DB 67,76,68,0,0,0,2,252
DB 76,79,68,83,66,0,2,172
DB 83,84,79,83,66,0,2,170
```

### Change 2 · `DATASEP:`

Find the unique label `DATASEP:`, then follow this unchanged source through its last displayed instruction:

```asm
DATASEP:
CALL SCAN
MOV AL,[2300H]
CMP AL,44
JE DATAITEM
CMP AL,0
JNE SYNTAXBAD
```

The edit begins immediately after that unchanged block.

Insert:

```asm
RET
FIXED:
MOV AL,[OP]
CALL EMIT
CALL FINISH
```

### Change 3 · `STNEXT1:`

Find the unique label `STNEXT1:`, then follow this unchanged source through its last displayed instruction:

```asm
STNEXT1:
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CMP AL,2
JNE STNEXT2
CALL FIXED
RET
STNEXT2:
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
MOV CX,2
```

With:

```asm
MOV CX,6
```

## Build and stop

Use the BASIC assembler prepared in the workbench guide:

```dos
COPY AS20.ASM SOURCE.ASM
GWBASIC BOOTASM.BAS
```

Require `OK RESULT.COM 1582 bytes`; BASIC may add spaces around the count. If the build reports an error, stop and compare the edited source. Use `SYSTEM` to return to DOS, then `COPY RESULT.COM AS20.COM`. Save this source and executable as a working stopping point.

Use `COPY CON T20.ASM` to enter this exact test text; finish with Ctrl-Z and Enter:

```asm
RET
CLD
LODSB
STOSB
```

```dos
COPY T20.ASM SOURCE.ASM
```

```dos
CHECK AS20
```

The display, apart from DOS command echo and the checker's separating blank line, is:

```text
OK 00004 bytes
PASS
```

Inspect `RESULT.COM` with the workbench viewer. At DOS run `GWBASIC VIEW.BAS`, enter `RESULT.COM`, and require a length of **4 bytes** with these hexadecimal bytes:

```text
C3 FC AC AA
```

Use `SYSTEM` to return to DOS.

This file is an encoding or data fixture. **Inspect it; do not execute it.**

## A rejection check

Enter this separate file as `X20.ASM` with `COPY CON`, ending with Ctrl-Z and Enter:

```asm
RET 1
```

```dos
COPY X20.ASM SOURCE.ASM
CHECK AS20
```

Require this diagnostic followed by the checker's `FAIL`:

```text
ERROR 00001 CODE 1
FAIL
```

`PASS` here means the rejection did not happen. Do not use an older output file as evidence of acceptance; require a new `OK` before inspecting output.

## If the result differs

Check each class-two table parameter against the expected opcode. FIXED emits that byte and FINISH rejects an extra operand. These fragments have no prepared stack or index registers for execution.
