+++
title = "09. Making a DOS request"
weight = 9
description = "Display a character and return control to DOS."
checkpoint = "BA09.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

I've taught BOOTASM the `MOV` from the magazine listing. I can inspect its bytes, but I still need a way to ask DOS to display the character and finish the program. That gives `INT` a very definite job.

## At the keyboard

Load the preceding checkpoint, `BA08.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 4024 / 4090; 5040 / 6000. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
4026 IF M$="INT" THEN GOSUB 5100: RETURN
5100 T$=A$: GOSUB 2000
5110 X=205: GOSUB 3000
5120 X=N: GOSUB 3000: RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
4024 IF M$="MOV" THEN GOSUB 4200: RETURN
4090 E$="Unknown instruction": GOTO 9000
5040 RETURN
6000 R=-1: W=0
```

Save the result before running it:

```basic
SAVE "BA09.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

`INT n` performs a software interrupt. Its encoding is CDH followed by the interrupt number, which must fit in a byte. Routine 5100 takes the argument in `A$`, reads it through `T$`, emits the fixed opcode and then the number, and advances `P`. It changes `T$`, `N`, `X`, and the numeric reader's scratch variables.

DOS uses interrupt 21H. For function 02H, put 2 in AH and a character code in DL; DOS displays the character. Function 4CH terminates a program, with the return code in AL. Loading AX with 4C00H sets both the function and a zero return code in one instruction.

DOS loads a `.COM` file at offset 0100H in a segment. Its first 256 bytes hold the Program Segment Prefix, or PSP, maintained by DOS. At entry CS, DS, ES, and SS identify this segment. The stack normally begins near its upper end. Our test does not change those segment registers or depend on uninitialized general registers. BASIC must return to the DOS prompt before the new program can be run.

## A visible check

At DOS, create `T09.ASM` with the following exact source. `COPY CON T09.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
MOV DL,42H
MOV AH,2
INT 21H
MOV AX,4C00H
INT 21H
```

From DOS start the checkpoint:

```dos
COPY T09.ASM SOURCE.ASM
GWBASIC BA09.BAS
```

The assembler uses the filenames in line 30 without asking for input. The success report must name `RESULT.COM` and report **11 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `RESULT.COM`. The viewer must report length 11 and these bytes (spaces and line wrapping are immaterial):

```text
B2 42 B4 02 CD 21 B8 00 4C CD 21
```

This fixture is a complete program. Return to DOS with `SYSTEM`, preserve the accepted result, then run it through the shared status check:

```dos
COPY RESULT.COM T09.COM
CHECK T09
```

It must display `B`, followed on a new line by `PASS` from the batch file. `FAIL` means the program returned a nonzero status. The checker is printed in the workbench section.

The `B` on the screen is the character from the instruction in my notebook. I go back over the bytes once more, then save the source and the accepted program under their own names. I have used my assembler to make a complete program that runs under DOS.

## An error worth catching

Create `X09.ASM` containing:

```asm
INT 256
```

Return to DOS, copy `X09.ASM` to `SOURCE.ASM`, then run `GWBASIC BA09.BAS`. Expect `ERROR line 1 : Byte out of range`; BASIC may print extra spaces around the line number. There must be no `OK` report. The accepted `RESULT.COM` must remain unchanged. Preserve it as HOLD.COM before this test and compare the files afterward; an older result must not be mistaken for a new successful assembly.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
