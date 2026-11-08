+++
title = "10. Counting twice"
weight = 10
description = "One pass to count the bytes, another to collect them."
checkpoint = "BA10.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

I've begun pencilling the address beside each instruction in my notebook. An extra byte changes every address below it. BOOTASM already counts the bytes it writes; I want it to make a counting pass before it collects the output.

## At the keyboard

Load the preceding checkpoint, `BA09.BAS`. Keep its working copy. Replace lines 3020. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 30 / 80; 300 / 310. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
70 FOR PS=1 TO 2
305 NEXT PS
3020 IF PS=2 THEN B%(P)=X
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
30 SF$="SOURCE.ASM": OF$="RESULT.COM"
80 OPEN "I", #1, SF$
300 CLOSE #1
310 OPEN "O", #2, OF$
3010 IF P=4096 THEN E$="Program too large": GOTO 9000
3020 B%(P)=X
3030 P=P+1: RETURN
```

Save the result before running it:

```basic
SAVE "BA10.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

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
COPY T10.ASM SOURCE.ASM
GWBASIC BA10.BAS
```

The assembler uses the filenames in line 30 without asking for input. The success report must name `RESULT.COM` and report **5 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `RESULT.COM`. The viewer must report length 5 and these bytes (spaces and line wrapping are immaterial):

```text
B8 00 4C CD 21
```

This fixture is a complete program. Return to DOS with `SYSTEM`, preserve the accepted result, then run it through the shared status check:

```dos
COPY RESULT.COM T10.COM
CHECK T10
```

It must display `PASS` from the batch file. `FAIL` means the program returned a nonzero status. The checker is printed in the workbench section.

## An error worth catching

Create `X10.ASM` containing:

```asm
DB 256
```

Return to DOS, copy `X10.ASM` to `SOURCE.ASM`, then run `GWBASIC BA10.BAS`. Expect `ERROR line 1 : Byte out of range`; BASIC may print extra spaces around the line number. There must be no `OK` report. The accepted `RESULT.COM` must remain unchanged. Preserve it as HOLD.COM before this test and compare the files afterward; an older result must not be mistaken for a new successful assembly.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
