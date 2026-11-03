+++
title = "Three complete programs"
weight = 20
description = "A message, a memory copy, and a deliberate failure."
download = "BOOTASM.BAS"
+++

These programs use the completed assembler. Save the tested final checkpoint as `BOOTASM.BAS` and preserve another ASCII copy as `BOOTKEEP.BAS`:

```basic
LOAD "BA18.BAS"
SAVE "BOOTASM.BAS",A
SAVE "BOOTKEEP.BAS",A
```

Each example is a complete DOS program. The source names below are base names: enter HELLO, COPYBYTE, or FAIL when BOOTASM asks. Inspect each file with VIEW.BAS before running it from DOS. A byte difference is a reason to stop and compare the source, even if the program seems to display the expected text.

## A message from a named address

Save this as `HELLO.ASM`:

```asm
MOV DX,TEXT
MOV AH,9
INT 21H
MOV AX,4C00H
INT 21H
TEXT:
DB 72,69,76,76,79,13,10,36
```

DX receives the address of TEXT. DOS function 09H displays bytes beginning at DS:DX until a dollar sign, whose character code is 36. The 13 and 10 produce carriage return and line feed. The terminator is not displayed. Function 09H cannot display an embedded dollar sign; function 02H can display a character directly.

Assemble HELLO, then use VIEW.BAS. Expect length 20:

```text
BA 0C 01 B4 09 CD 21 B8 00 4C CD 21 48 45 4C 4C
4F 0D 0A 24
```

Return to DOS with SYSTEM and type `CHECK HELLO`. Expect HELLO on one line and PASS below it, with a possible blank line between them.

A useful rejection check is to change `MOV DX,TEXT` to `MOV DX,MISSING`. Assembly must report `ERROR line 1 : Undefined label`, with no OK report. The earlier HELLO.COM remains unchanged; do not treat it as the failed assembly's result.

## A byte through memory

Save as `COPYBYTE.ASM`:

```asm
MOV BX,SOURCE
MOV AL,[BX]
MOV [DEST],AL
MOV DL,[DEST]
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
SOURCE:
DB 4DH
DEST:
DB 0
```

BX receives the address of SOURCE. The first memory MOV reads that byte; the second stores it at DEST. The third reads it back into DL, and DOS displays it. DEST is real storage in the image, not an unallocated address chosen by guesswork. MOV does not change flags, but this example does not depend on their entry state.

Assemble COPYBYTE and inspect length 24:

```text
BB 16 01 8A 07 88 06 17 01 8A 16 17 01 B4 02 CD
21 B8 00 4C CD 21 4D 00
```

At DOS, `CHECK COPYBYTE` must display M and then PASS on a new line. If it displays another character, compare both direct offsets and the byte stored at SOURCE.

For a rejection test replace `MOV [DEST],AL` with `MOV [DEST],1`. Expect `ERROR line 3 : Register required`; the small memory grammar requires a register on the other side. Restore the original line and require a fresh OK report before running again.

## A return code which the checker can see

Save as `FAIL.ASM`:

```asm
MOV AX,4C01H
INT 21H
```

Expect length 5 and bytes:

```text
B8 01 4C CD 21
```

`CHECK FAIL` must print FAIL. This is the intended result: DOS function 4CH receives the return code one in AL. For comparison, change 4C01H to 4C00H, assemble again, inspect `B8 00 4C CD 21`, and run `CHECK FAIL` again. It must now print PASS. This pair proves that the batch check reports both outcomes rather than treating a quiet return as success.

If both tests give the same report, inspect the new bytes and make certain the ERRORLEVEL test immediately follows the executed program in CHECK.BAT. Do not launch a viewer or another program between the return and the status test.
