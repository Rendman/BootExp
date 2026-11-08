+++
title = "17. Calling and jumping"
weight = 17
description = "Near transfers, return addresses, and relative displacements."
checkpoint = "BA17.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

In BASIC I can give a piece of work its own routine and reach it with `GOSUB`. I want to organize my assembly source that way too: call a named routine, let it do its job, and return to the instruction after the call.

## At the keyboard

Load the preceding checkpoint, `BA16.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 4032 / 4090; 5260 / 6000. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
4034 IF M$="JMP" OR M$="CALL" THEN GOSUB 5500: RETURN
5500 T$=A$: GOSUB 2000
5510 RV=N-(256+P+3)
5520 X=233: IF M$="CALL" THEN X=232
5530 GOSUB 3000: N=RV
5540 IF N<0 THEN N=N+65536
5550 GOSUB 3100: RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
4032 IF I>0 THEN IF (I-1) MOD 4=0 THEN GOSUB 4390: RETURN
4090 E$="Unknown instruction": GOTO 9000
5260 GOSUB 3000: RETURN
6000 R=-1: W=0
```

Save the result before running it:

```basic
SAVE "BA17.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

A near transfer stays in the current code segment. JMP replaces the instruction pointer; CALL first pushes the address of the following instruction. RET uses that saved word. Each ordinary call uses two stack bytes until its return, in addition to any words the routine pushes itself. There is no automatic check for stack collision or unmatched pushes.

The opcode is E9H for JMP and E8H for CALL. Both are followed by a 16-bit relative displacement. `P` is a file offset, so the current instruction's loaded address is `256+P`. The following instruction lies three bytes farther on. Routine 5500 subtracts that address from the destination to obtain `RV`, emits the opcode, and writes the displacement as a word. A negative displacement is represented by adding 65,536. The 16-bit instruction pointer wraps when that word is added.

The routine takes the destination from `A$`; it changes `T$`, the numeric-reader scratch variables, `RV`, `N`, `X`, and `P`. Every JMP is three bytes; there is no automatic short-JMP selection. Far transfers and indirect calls are omitted because all our code shares one segment.

In the test, CALL occupies offsets 0100H-0102H. SAY begins at 0108H, so the displacement is five. The routine displays C and returns to the termination code.

## A visible check

At DOS, create `T17.ASM` with the following exact source. `COPY CON T17.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

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

From DOS start the checkpoint:

```dos
COPY T17.ASM SOURCE.ASM
GWBASIC BA17.BAS
```

The assembler uses the filenames in line 30 without asking for input. The success report must name `RESULT.COM` and report **15 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `RESULT.COM`. The viewer must report length 15 and these bytes (spaces and line wrapping are immaterial):

```text
E8 05 00 B8 00 4C CD 21 B2 43 B4 02 CD 21 C3
```

This fixture is a complete program. Return to DOS with `SYSTEM`, preserve the accepted result, then run it through the shared status check:

```dos
COPY RESULT.COM T17.COM
CHECK T17
```

It must display `C`, followed on a new line by `PASS` from the batch file. `FAIL` means the program returned a nonzero status. The checker is printed in the workbench section.

## An error worth catching

Create `X17.ASM` containing:

```asm
CALL LOST
```

Return to DOS, copy `X17.ASM` to `SOURCE.ASM`, then run `GWBASIC BA17.BAS`. Expect `ERROR line 1 : Undefined label`; BASIC may print extra spaces around the line number. There must be no `OK` report. The accepted `RESULT.COM` must remain unchanged. Preserve it as HOLD.COM before this test and compare the files afterward; an older result must not be mistaken for a new successful assembly.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
