+++
title = "05. Several bytes on one line"
weight = 5
description = "A row of data, one comma at a time."
checkpoint = "BA05.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

A row of character codes ought to occupy a row of source. We shall let DB accept a comma-separated list, using the number routine for each item.

## At the keyboard

Load the preceding checkpoint, `BA04.BAS`. Keep its working copy. Replace lines 4100, 4140. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 4100 / 4140; 4140 / 9000. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
4100 IF A$="" THEN E$="Missing value": GOTO 9000
4110 DA$=A$
4120 DI=INSTR(DA$+",",","): T$=LEFT$(DA$,DI-1)
4130 GOSUB 2000
4140 X=N: GOSUB 3000
4150 DA$=MID$(DA$,DI+1)
4160 IF DA$<>"" THEN 4120
4170 IF RIGHT$(A$,1)="," THEN E$="Missing value": GOTO 9000
4180 RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
4090 E$="Unknown instruction": GOTO 9000
4100 T$=A$: GOSUB 2000
4140 X=N: GOSUB 3000: RETURN
9000 PRINT "ERROR line"; L; ": "; E$
```

Save the result before running it:

```basic
SAVE "BA05.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

Routine 4100 keeps the unprocessed part in `DA$`. Searching `DA$+","` guarantees that a separator can be found even for the final item. `DI` locates it, `T$` receives the item, and the existing routines read and store it. `MID$` then removes the item and its comma.

`DA$` and `DI` belong to this loop. The number reader changes `Q$`, `BA`, `NI`, `D`, and `N`, but does not alter them. The emitter preserves them as well. The test at 4170 rejects a comma at the end; two adjacent commas produce an empty item and the same diagnostic. No string constants or repetition syntax are being added.

## A visible check

At DOS, create `T05.ASM` with the following exact source. `COPY CON T05.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
DB 41H,42H,43H,0
```

From DOS start the checkpoint:

```dos
COPY T05.ASM SOURCE.ASM
GWBASIC BA05.BAS
```

The assembler uses the filenames in line 30 without asking for input. The success report must name `RESULT.COM` and report **4 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `RESULT.COM`. The viewer must report length 4 and these bytes (spaces and line wrapping are immaterial):

```text
41 42 43 00
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X05.ASM` containing:

```asm
DB 1,
```

Return to DOS, copy `X05.ASM` to `SOURCE.ASM`, then run `GWBASIC BA05.BAS`. Expect `ERROR line 1 : Missing value`; BASIC may print extra spaces around the line number. There must be no `OK` report. The accepted `RESULT.COM` must remain unchanged. Preserve it as HOLD.COM before this test and compare the files afterward; an older result must not be mistaken for a new successful assembly.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
