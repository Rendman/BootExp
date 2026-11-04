+++
title = "13. Copying between registers"
weight = 13
description = "Copy a value with a register-to-register MOV."
checkpoint = "BA13.BAS"
+++

A constant is not the only source for MOV. Copying one register to another gives us a first encounter with the byte which describes operands.

## At the keyboard

Load the preceding checkpoint, `BA12.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 4220 / 4226; 4250 / 4900. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
4222 T$=A2$: GOSUB 6000
4224 IF R>=0 THEN GOSUB 4300: RETURN
4300 IF WD<>W THEN E$="Register sizes differ": GOTO 9000
4310 X=138+WD: GOSUB 3000
4320 X=192+8*RD+R: GOSUB 3000
4330 RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
4220 RD=R: WD=W
4226 T$=A2$: GOSUB 2000
4250 GOSUB 3100: RETURN
4900 IF A$<>"" THEN E$="Unexpected operand": GOTO 9000
```

Save the result before running it:

```basic
SAVE "BA13.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

The source is tried as a register before it is tried as a number or name. The saved `RD` and `WD` describe the destination; `R` and `W` describe the source. The widths must agree. MOV AX,AL would not say which half to extend, and this assembler refuses it.

For this direction of MOV, the opcode is 8AH for a byte or 8BH for a word. A second byte, called ModR/M, describes the operands. Bits 7-6 are 11 for register operands, contributing 192. Bits 5-3 hold the destination register number, contributing eight times `RD`. Bits 2-0 hold the source register number `R`.

Routine 4300 takes those four saved and current register values, emits the opcode and ModR/M byte, and changes `X` and `P`. It preserves the register values. For MOV AX,BX, the second byte is C3H: 192 plus zero plus three. This fixture checks encodings only.

## A visible check

At DOS, create `T13.ASM` with the following exact source. `COPY CON T13.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
MOV AX,BX
MOV DL,AL
MOV CH,BH
```

From DOS start the checkpoint:

```dos
GWBASIC BA13.BAS
```

At its source-name prompt enter `T13` without an extension. The success report must name `T13.COM` and report **6 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `T13.COM`. The viewer must report length 6 and these bytes (spaces and line wrapping are immaterial):

```text
8B C3 8A D0 8A EF
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X13.ASM` containing:

```asm
MOV AX,AL
```

Reload `BA13.BAS` and run it with source name `X13`. Expect `ERROR line 1 : Register sizes differ`; BASIC may print extra spaces around the line number. There must be no `OK` report. On a fresh workbench there must be no `X13.COM`. If an older file exists, it is left unchanged and must not be mistaken for a new result.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
