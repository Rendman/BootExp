+++
title = "10. Counting twice"
weight = 10
description = "One pass to count the bytes, another to collect them."
checkpoint = "BA10.BAS"
+++

A source file can be read once to count its bytes and again to collect them. We shall establish those two passes while all operands are still numeric.

## At the keyboard

Load the preceding checkpoint, `BA09.BAS`. Keep its working copy. Replace lines 3020. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 40 / 80; 300 / 310. Each pair gives the existing lines on either side.

This block contains **3 required BASIC lines**. BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
70 FOR PS=1 TO 2
305 NEXT PS
3020 IF PS=2 THEN B%(P)=X
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
40 GOSUB 8000
80 OPEN "I", #1, F$+".ASM"
300 CLOSE #1
310 OPEN "O", #2, F$+".COM"
3010 IF P=4096 THEN E$="Program too large": GOTO 9000
3020 B%(P)=X
3030 P=P+1: RETURN
```

Save the result before running it:

```basic
SAVE "BA10.BAS",A
```

The saved checkpoint contains 118 BASIC lines in total. Keep this filename for the stopping point; it is not a second program to type.

## How it works

The new FOR loop begins before opening the source and ends after closing it. Each pass resets `P` and `L` at line 90. `PS` is one for the counting pass and two for the collecting pass. Routine 3000 performs the same range and capacity checks in either pass, but only pass two stores bytes in the array.

Nothing is written to disk until both passes finish. The file is reopened rather than retained in a string array, saving BASIC memory. The same instruction always has the same length; no instruction shortening is attempted. Those choices make the second pass reproduce the first pass's positions.

The output loop uses the second pass's byte count. There is still only one OK report and one output file. Do not edit the source while an assembly is running. The test below must produce exactly the same result as a one-pass assembly.

## A visible check

At DOS, create `T10.ASM` with the following exact source. `COPY CON T10.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
MOV AX,4C00H
INT 21H
```

From DOS start the checkpoint:

```dos
GWBASIC BA10.BAS
```

At its source-name prompt enter `T10` without an extension. The success report must name `T10.COM` and report **5 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `T10.COM`. The viewer must report length 5 and these bytes (spaces and line wrapping are immaterial):

```text
B8 00 4C CD 21
```

This fixture is a complete program. Return to DOS with `SYSTEM`, then run it through the shared status check:

```dos
CHECK T10
```

It must display `PASS` from the batch file. `FAIL` means the program returned a nonzero status. The checker is printed in the workbench section.

## An error worth catching

Create `X10.ASM` containing:

```asm
DB 256
```

Reload `BA10.BAS` and run it with source name `X10`. Expect `ERROR line 1 : Byte out of range`; BASIC may print extra spaces around the line number. There must be no `OK` report. On a fresh workbench there must be no `X10.COM`. If an older file exists, it is left unchanged and must not be mistaken for a new result.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
