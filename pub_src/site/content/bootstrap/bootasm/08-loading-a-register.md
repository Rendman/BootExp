+++
title = "08. Loading a register"
weight = 8
description = "Register names, operand sizes, and immediate values."
checkpoint = "BA08.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

A DOS service takes its request in registers. We shall first teach MOV to load a constant, with the register name determining its size.

## At the keyboard

Load the preceding checkpoint, `BA07.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 4022 / 4090; 4180 / 4900; 4910 / 9000. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
4024 IF M$="MOV" THEN GOSUB 4200: RETURN
4200 GOSUB 5000: T$=A1$: GOSUB 6000
4210 IF R<0 THEN E$="Register required": GOTO 9000
4220 RD=R: WD=W
4226 T$=A2$: GOSUB 2000
4230 X=176+8*WD+RD: GOSUB 3000
4240 IF WD=0 THEN X=N: GOSUB 3000: RETURN
4250 GOSUB 3100: RETURN
5000 I=INSTR(A$,",")
5010 IF I<2 OR I=LEN(A$) THEN E$="Two operands required": GOTO 9000
5020 A1$=LEFT$(A$,I-1): A2$=MID$(A$,I+1)
5030 IF INSTR(A2$,",")>0 THEN E$="Two operands required": GOTO 9000
5040 RETURN
6000 R=-1: W=0
6010 IF LEN(T$)<>2 THEN RETURN
6020 FOR RI=0 TO 7
6030 IF T$=MID$("ALCLDLBLAHCHDHBH",2*RI+1,2) THEN R=RI: RETURN
6040 NEXT RI
6050 W=1
6060 FOR RI=0 TO 7
6070 IF T$=MID$("AXCXDXBXSPBPSIDI",2*RI+1,2) THEN R=RI: RETURN
6080 NEXT RI: RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
4022 IF X>=0 THEN GOSUB 4900: RETURN
4090 E$="Unknown instruction": GOTO 9000
4180 RETURN
4900 IF A$<>"" THEN E$="Unexpected operand": GOTO 9000
4910 GOSUB 3000: RETURN
9000 PRINT "ERROR line"; L; ": "; E$
```

Save the result before running it:

```basic
SAVE "BA08.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

A register is a small working store inside the processor. AX, CX, DX, BX, SP, BP, SI, and DI are 16-bit registers, numbered zero through seven in that order for these encodings. AL, CL, DL, BL, AH, CH, DH, and BH are the corresponding encoding order for 8-bit registers. AL and AH are the low and high halves of AX; the same rule holds for CX, DX, and BX. The other four word registers have no byte halves accessible by those names.

Routine 5000 splits `A$` into destination `A1$` and source `A2$`, rejecting a missing or extra comma. It changes `I` but no numeric value. Routine 6000 takes a register name in `T$`, returns its number in `R` and width in `W` (zero for byte, one for word), and uses `RI` as its loop index. `R=-1` means no register matched; in that case `W` has no meaning.

The MOV routine saves the destination number and width in `RD` and `WD` before reading the source number. The opcode is B0H plus the register number for a byte, or B8H plus the number for a word. The immediate value follows it. *Immediate* means the value is part of the instruction. MOV does not alter the arithmetic flags.

A word register accepts a value up to 65,535; a byte register accepts at most 255. No automatic truncation is performed. This fixture checks encodings and must not be executed.

## A visible check

At DOS, create `T08.ASM` with the following exact source. `COPY CON T08.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
MOV AL,41H
MOV AX,1234H
MOV DX,65535
```

From DOS start the checkpoint:

```dos
COPY T08.ASM SOURCE.ASM
GWBASIC BA08.BAS
```

The assembler uses the filenames in line 30 without asking for input. The success report must name `RESULT.COM` and report **8 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `RESULT.COM`. The viewer must report length 8 and these bytes (spaces and line wrapping are immaterial):

```text
B0 41 B8 34 12 BA FF FF
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X08.ASM` containing:

```asm
MOV AL,256
```

Return to DOS, copy `X08.ASM` to `SOURCE.ASM`, then run `GWBASIC BA08.BAS`. Expect `ERROR line 1 : Byte out of range`; BASIC may print extra spaces around the line number. There must be no `OK` report. The accepted `RESULT.COM` must remain unchanged. Preserve it as HOLD.COM before this test and compare the files afterward; an older result must not be mistaken for a new successful assembly.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
