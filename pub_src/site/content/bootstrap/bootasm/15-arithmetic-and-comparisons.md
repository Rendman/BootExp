+++
title = "15. Arithmetic and comparisons"
weight = 15
description = "Adding, subtracting, testing bits, and setting flags."
checkpoint = "BA15.BAS"
+++

To work on a character or count, a program needs arithmetic and tests. The same operand machinery serves six closely related instruction families.

## At the keyboard

Load the preceding checkpoint, `BA14.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 4028 / 4090; 4330 / 4900. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
4030 I=INSTR("ADD OR  AND SUB XOR CMP ",M$+" ")
4032 IF I>0 THEN IF (I-1) MOD 4=0 THEN GOSUB 4390: RETURN
4390 OP=VAL(MID$("014567",(I-1)/4+1,1)): GOTO 4400
4400 GOSUB 5000: T$=A1$: GOSUB 6000
4410 IF R<0 THEN E$="Register required": GOTO 9000
4420 RD=R: WD=W
4430 T$=A2$: GOSUB 6000
4440 IF R>=0 THEN GOSUB 4500: RETURN
4450 T$=A2$: GOSUB 2000
4460 X=128+WD: GOSUB 3000
4470 X=192+8*OP+RD: GOSUB 3000
4480 IF WD=0 THEN X=N: GOSUB 3000: RETURN
4490 GOSUB 3100: RETURN
4500 IF WD<>W THEN E$="Register sizes differ": GOTO 9000
4510 X=8*OP+2+WD: GOSUB 3000
4520 X=192+8*RD+R: GOSUB 3000
4530 RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
4028 IF M$="INC" OR M$="DEC" OR M$="PUSH" OR M$="POP" THEN GOSUB 5200: RETURN
4090 E$="Unknown instruction": GOTO 9000
4330 RETURN
4900 IF A$<>"" THEN E$="Unexpected operand": GOTO 9000
```

Save the result before running it:

```basic
SAVE "BA15.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

ADD and SUB alter the destination by addition or subtraction. CMP sets the subtraction flags without storing the answer. AND, OR, and XOR perform bit-by-bit logical operations. All these forms set flags; logical operations clear carry and overflow and leave auxiliary carry undefined. Arithmetic carries beyond the selected width are not stored in the destination.

The mnemonic table uses four characters per entry, including spaces. A matching name must begin at an entry boundary. The matching position selects an operation number from `014567`: ADD=0, OR=1, AND=4, SUB=5, XOR=6, CMP=7. These are the processor's group numbers, not consecutive entries invented by the assembler. `OP` preserves that choice while the operands are read.

For a register source, routine 4500 emits `8*OP+2+WD` and a register ModR/M byte. For an immediate source, 4400 emits 80H for a byte or 81H for a word. The ModR/M byte has the operation number in its middle field and the destination register in its low field. The immediate follows in the destination's width. We deliberately omit the shorter sign-extended 83H form to keep size decisions fixed.

Both routines take their operands from `A$` through 5000. They change the operand-reader scratch variables, `RD`, `WD`, `R`, `W`, `N`, `X`, and `P`; they preserve `OP`. Memory arithmetic and signed literal syntax are omitted. To represent a negative bit pattern, use its unsigned hexadecimal value, such as 0FFFFH for a word containing all one bits. This fixture is only for inspection.

## A visible check

At DOS, create `T15.ASM` with the following exact source. `COPY CON T15.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
ADD AX,BX
SUB CX,1
CMP AL,41H
XOR DX,DX
AND AL,0DFH
OR BL,20H
```

From DOS start the checkpoint:

```dos
GWBASIC BA15.BAS
```

At its source-name prompt enter `T15` without an extension. The success report must name `T15.COM` and report **17 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `T15.COM`. The viewer must report length 17 and these bytes (spaces and line wrapping are immaterial):

```text
03 C3 81 E9 01 00 80 F8 41 33 D2 80 E0 DF 80 CB 20
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X15.ASM` containing:

```asm
ADD AX,AL
```

Reload `BA15.BAS` and run it with source name `X15`. Expect `ERROR line 1 : Register sizes differ`; BASIC may print extra spaces around the line number. There must be no `OK` report. On a fresh workbench there must be no `X15.COM`. If an older file exists, it is left unchanged and must not be mistaken for a new result.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
