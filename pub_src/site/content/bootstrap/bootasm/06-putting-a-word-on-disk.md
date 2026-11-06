+++
title = "06. Putting a word on disk"
weight = 6
description = "Sixteen-bit values, with the low byte first."
checkpoint = "BA06.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

The processor uses 16-bit quantities as well as bytes. A define-word directive gives us a direct way to check their order on disk.

## At the keyboard

Load the preceding checkpoint, `BA05.BAS`. Keep its working copy. Replace lines 4000, 4110, 4140. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 3030 / 4000; 4110 / 4120. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
3100 X=N-256*INT(N/256): GOSUB 3000
3110 X=INT(N/256): GOSUB 3000
3120 RETURN
4000 IF M$="DB" OR M$="DW" THEN GOSUB 4100: RETURN
4110 DA$=A$: DW=0
4115 IF M$="DW" THEN DW=1
4140 IF DW=0 THEN X=N: GOSUB 3000 ELSE GOSUB 3100
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
3030 P=P+1: RETURN
4000 IF M$="DB" THEN GOSUB 4100: RETURN
4090 E$="Unknown instruction": GOTO 9000
4100 IF A$="" THEN E$="Missing value": GOTO 9000
4110 DA$=A$
4120 DI=INSTR(DA$+",",","): T$=LEFT$(DA$,DI-1)
4130 GOSUB 2000
4140 X=N: GOSUB 3000
4150 DA$=MID$(DA$,DI+1)
```

Save the result before running it:

```basic
SAVE "BA06.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

`DW` means *define word*. A word holds 0 through 65,535. The 8088 stores its low byte first. The word `1234H` is therefore written as `34 12`, not `12 34`.

Routine 3100 takes `N` and emits two bytes through 3000. `INT(N/256)` is the high byte; subtracting 256 times that value leaves the low byte. This arithmetic avoids BASIC's signed integer division and logical operators for unsigned values above 32,767. Routine 3100 changes `X` and `P` and preserves `N`.

`DW` in line 4110 is an ordinary numeric flag, distinct from the text in `M$`. It selects one or two bytes for every item. Do not confuse a word in the file with a BASIC integer variable: BASIC integers are signed.

## A visible check

At DOS, create `T06.ASM` with the following exact source. `COPY CON T06.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
DW 1234H,65535
DB 0
```

From DOS start the checkpoint:

```dos
GWBASIC BA06.BAS
```

At its source-name prompt enter `T06` without an extension. The success report must name `T06.COM` and report **5 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `T06.COM`. The viewer must report length 5 and these bytes (spaces and line wrapping are immaterial):

```text
34 12 FF FF 00
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X06.ASM` containing:

```asm
DW 65536
```

Reload `BA06.BAS` and run it with source name `X06`. Expect `ERROR line 1 : Number too large`; BASIC may print extra spaces around the line number. There must be no `OK` report. On a fresh workbench there must be no `X06.COM`. If an older file exists, it is left unchanged and must not be mistaken for a new result.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
