+++
title = "14. The stack and single-register work"
weight = 14
description = "Move an index, save a word, and mind the stack."
checkpoint = "BA14.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

Indexes must move, and a routine sometimes needs to put a word aside. Four families of one-byte instructions cover these small jobs.

## At the keyboard

Load the preceding checkpoint, `BA13.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 4026 / 4090; 5120 / 6000. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
4028 IF M$="INC" OR M$="DEC" OR M$="PUSH" OR M$="POP" THEN GOSUB 5200: RETURN
5200 T$=A$: GOSUB 6000
5210 IF R<0 OR W<>1 THEN E$="Word register required": GOTO 9000
5220 X=64+R
5230 IF M$="DEC" THEN X=72+R
5240 IF M$="PUSH" THEN X=80+R
5250 IF M$="POP" THEN X=88+R
5260 GOSUB 3000: RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
4026 IF M$="INT" THEN GOSUB 5100: RETURN
4090 E$="Unknown instruction": GOTO 9000
5120 X=N: GOSUB 3000: RETURN
6000 R=-1: W=0
```

Save the result before running it:

```basic
SAVE "BA14.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

INC adds one and DEC subtracts one, with 16-bit wraparound. They update arithmetic flags but preserve the carry flag. PUSH decrements SP by two and stores a word at SS:SP. POP reads a word there and advances SP by two. PUSH and POP do not change the arithmetic flags.

The opcodes start at 40H, 48H, 50H, and 58H respectively; the register number is added to the starting value. Routine 5200 takes the one argument in `A$`, checks it through 6000, chooses the base, and sends the byte to 3000. It changes `T$`, `R`, `W`, `RI`, `X`, and `P`.

Only word-register forms are accepted. The processor has other INC and DEC forms, but supporting them would require more operand rules. Avoid PUSH SP: on the 8086/8088 it stores the already-decremented SP, unlike later processors. POP SP replaces the stack pointer itself. Never experiment with either form without understanding the resulting stack. Ordinary PUSH and POP pairs must be balanced before a RET.

This fixture is for byte inspection only; its register values have not been initialized.

## A visible check

At DOS, create `T14.ASM` with the following exact source. `COPY CON T14.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
INC BX
DEC CX
PUSH AX
POP DX
```

From DOS start the checkpoint:

```dos
COPY T14.ASM SOURCE.ASM
GWBASIC BA14.BAS
```

The assembler uses the filenames in line 30 without asking for input. The success report must name `RESULT.COM` and report **4 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `RESULT.COM`. The viewer must report length 4 and these bytes (spaces and line wrapping are immaterial):

```text
43 49 50 5A
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X14.ASM` containing:

```asm
INC AL
```

Return to DOS, copy `X14.ASM` to `SOURCE.ASM`, then run `GWBASIC BA14.BAS`. Expect `ERROR line 1 : Word register required`; BASIC may print extra spaces around the line number. There must be no `OK` report. The accepted `RESULT.COM` must remain unchanged. Preserve it as HOLD.COM before this test and compare the files afterward; an older result must not be mistaken for a new successful assembly.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
