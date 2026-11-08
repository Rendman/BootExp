+++
title = "12. Using names as values"
weight = 12
description = "Resolve forward references without hand-counting offsets."
checkpoint = "BA12.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

A recorded address can replace a hand-counted constant. We shall allow a name wherever a whole numeric value is accepted, including a name defined farther down the source.

## At the keyboard

Load the preceding checkpoint, `BA11.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 2000 / 2020; 2110 / 3000. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
2010 IF LEFT$(T$,1)<"0" OR LEFT$(T$,1)>"9" THEN GOSUB 2200: RETURN
2200 GOSUB 7100: GOSUB 7200
2210 IF SI>=0 THEN N=SV(SI): RETURN
2220 IF PS=1 THEN N=0: RETURN
2230 E$="Undefined label": GOTO 9000
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
2000 IF T$="" THEN E$="Missing value": GOTO 9000
2020 Q$=T$: BA=10
2110 NEXT NI: RETURN
3000 IF X<0 OR X>255 THEN E$="Byte out of range": GOTO 9000
```

Save the result before running it:

```basic
SAVE "BA12.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

The numeric reader now examines the first character before parsing digits. A token beginning with a decimal digit is numeric; everything else must pass the label validator. This is why an all-letter hexadecimal number needs a leading zero: write `0ABH`, not `ABH`.

Routine 2200 uses the same name search as a definition. A known name returns its value in `N`. An unknown name returns zero during pass one, because all accepted forms have fixed lengths. In pass two every definition has been seen; an unknown name is then an error.

The routine changes the validator's and searcher's scratch variables, but preserves the DB list's `DA$` and `DI`. A named address in DW is useful because an address normally exceeds one byte. DB still rejects a named value above 255. There is no expression evaluator: `TEXT+1`, a minus sign, or an EQU definition is outside this language.

Our test places the word before the byte it names. The word takes two bytes, so TEXT is at 0102H. Inspect the bytes; this is data, not a program.

## A visible check

At DOS, create `T12.ASM` with the following exact source. `COPY CON T12.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
DW TEXT
TEXT:
DB 41H
```

From DOS start the checkpoint:

```dos
COPY T12.ASM SOURCE.ASM
GWBASIC BA12.BAS
```

The assembler uses the filenames in line 30 without asking for input. The success report must name `RESULT.COM` and report **3 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `RESULT.COM`. The viewer must report length 3 and these bytes (spaces and line wrapping are immaterial):

```text
02 01 41
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X12.ASM` containing:

```asm
DW MISSING
```

Return to DOS, copy `X12.ASM` to `SOURCE.ASM`, then run `GWBASIC BA12.BAS`. Expect `ERROR line 1 : Undefined label`; BASIC may print extra spaces around the line number. There must be no `OK` report. The accepted `RESULT.COM` must remain unchanged. Preserve it as HOLD.COM before this test and compare the files afterward; an older result must not be mistaken for a new successful assembly.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
