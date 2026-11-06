+++
title = "11. Giving positions names"
weight = 11
description = "A symbol table gives each label its address."
checkpoint = "BA11.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

The counting pass knows where each source line will lie. We can give a position a name without emitting another byte.

## At the keyboard

Load the preceding checkpoint, `BA10.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 20 / 30; 40 / 70; 150 / 160; 6080 / 8000. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
22 DIM SY$(255), SV(255)
65 SC=0
158 IF RIGHT$(S$,1)=":" THEN T$=LEFT$(S$,LEN(S$)-1): GOSUB 7000: GOTO 100
7000 GOSUB 7100: GOSUB 7200
7010 IF PS=2 THEN RETURN
7020 IF SI>=0 THEN E$="Duplicate label": GOTO 9000
7030 IF SC=256 THEN E$="Too many labels": GOTO 9000
7040 SY$(SC)=T$: SV(SC)=256+P: SC=SC+1
7050 RETURN
7100 IF LEN(T$)<1 OR LEN(T$)>16 THEN E$="Bad label": GOTO 9000
7110 C$=LEFT$(T$,1)
7120 IF INSTR("ABCDEFGHIJKLMNOPQRSTUVWXYZ_",C$)=0 THEN E$="Bad label": GOTO 9000
7130 FOR K=1 TO LEN(T$)
7140 C$=MID$(T$,K,1)
7150 IF INSTR("ABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789",C$)=0 THEN E$="Bad label": GOTO 9000
7160 NEXT K
7170 GOSUB 6000: IF R>=0 THEN E$="Reserved label": GOTO 9000
7180 RETURN
7200 SI=-1
7205 IF SC=0 THEN RETURN
7210 FOR K=0 TO SC-1
7220 IF SY$(K)=T$ THEN SI=K: RETURN
7230 NEXT K: RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
20 DIM B%(4095)
30 LINE INPUT "Source name (no extension): "; F$
40 GOSUB 8000
70 FOR PS=1 TO 2
150 GOSUB 1000
160 IF S$="" THEN 100
6080 NEXT RI: RETURN
8000 IF LEN(F$)<1 OR LEN(F$)>8 THEN E$="Bad filename": GOTO 9000
```

Save the result before running it:

```basic
SAVE "BA11.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

A label is written alone on a line, followed by a colon. Its value is the address of the next byte: 256 plus `P`. A label may precede code or data, and several different labels may name the same position. The colon is a definition mark and is not part of the name.

Routine 7100 checks `T$`. Names contain one to sixteen uppercase letters, digits, or underscores; the first character cannot be a digit. Normalization makes lowercase spelling equivalent. Register names are reserved because they would be ambiguous in operands. The validator changes `K`, `C$`, and the register reader's scratch variables; it preserves `T$`.

Routine 7200 searches the first `SC` entries and returns the matching index `SI`, or -1. Routine 7000 enters a definition only in pass one, using parallel arrays `SY$` for names and `SV` for values. A repeated name is an error, even if its value would be unchanged. The table holds 256 names, a deliberate storage bound. The arrays run from zero through 255; the full-table test prevents a write beyond that allocation. Pass two validates definitions without entering them again.

At this checkpoint names are recorded, but numeric operands are still required. A label line should make no difference to the bytes collected.

## A visible check

At DOS, create `T11.ASM` with the following exact source. `COPY CON T11.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
START:
DB 41H
FINISH:
DB 42H
```

From DOS start the checkpoint:

```dos
GWBASIC BA11.BAS
```

At its source-name prompt enter `T11` without an extension. The success report must name `T11.COM` and report **2 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `T11.COM`. The viewer must report length 2 and these bytes (spaces and line wrapping are immaterial):

```text
41 42
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X11.ASM` containing:

```asm
AGAIN:
DB 1
AGAIN:
```

Reload `BA11.BAS` and run it with source name `X11`. Expect `ERROR line 3 : Duplicate label`; BASIC may print extra spaces around the line number. There must be no `OK` report. On a fresh workbench there must be no `X11.COM`. If an older file exists, it is left unchanged and must not be mistaken for a new result.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
