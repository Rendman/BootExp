+++
title = "04. Hexadecimal numbers"
weight = 4
description = "Reading base sixteen and catching malformed numbers."
checkpoint = "BA04.BAS"
+++

Machine-code tables are easier to read in hexadecimal. The byte writer need not change; only the reader of numbers needs another base.

## At the keyboard

Load the preceding checkpoint, `BA03.BAS`. Keep its working copy. Replace lines 2020, 2060, 2070, 2080, 2090. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 2020 / 2060. Each pair gives the existing lines on either side.

This block contains **8 required BASIC lines**. BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
2020 Q$=T$: BA=10
2030 IF RIGHT$(Q$,1)="H" THEN BA=16: Q$=LEFT$(Q$,LEN(Q$)-1)
2040 IF Q$="" THEN E$="Bad number": GOTO 9000
2050 N=0
2060 FOR NI=1 TO LEN(Q$)
2070 D=INSTR("0123456789ABCDEF",MID$(Q$,NI,1))-1
2080 IF D<0 OR D>=BA THEN E$="Bad number": GOTO 9000
2090 N=N*BA+D
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
2000 IF T$="" THEN E$="Missing value": GOTO 9000
2020 N=0
2060 FOR NI=1 TO LEN(T$)
2070 D=ASC(MID$(T$,NI,1))-48
2080 IF D<0 OR D>9 THEN E$="Bad number": GOTO 9000
2090 N=N*10+D
2100 IF N>65535 THEN E$="Number too large": GOTO 9000
```

Save the result before running it:

```basic
SAVE "BA04.BAS",A
```

The saved checkpoint contains 70 BASIC lines in total. Keep this filename for the stopping point; it is not a second program to type.

## How it works

A hexadecimal digit describes four bits. The digits run from 0 through 9 and then A through F, meaning ten through fifteen. Thus `41H` is four sixteens plus one, or decimal 65. The suffix `H` selects base sixteen; no suffix selects base ten.

The number routine now copies `T$` into `Q$` and chooses `BA`, its base. The suffix is removed from the copy. `INSTR` finds a digit in the ordered digit string; subtracting one gives its value, or -1 if it is absent. The range test rejects a hexadecimal letter in a decimal number. Multiplication by `BA` moves the preceding digits one place left.

`N` may reach 65,535, because other callers will need words. The byte emitter still rejects anything above 255. Write hexadecimal constants with a leading decimal digit, such as `0FFH`; this spelling will distinguish numbers from names.

## A visible check

At DOS, create `T04.ASM` with the following exact source. `COPY CON T04.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
DB 41H
DB 66
DB 0FFH
```

From DOS start the checkpoint:

```dos
GWBASIC BA04.BAS
```

At its source-name prompt enter `T04` without an extension. The success report must name `T04.COM` and report **3 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `T04.COM`. The viewer must report length 3 and these bytes (spaces and line wrapping are immaterial):

```text
41 42 FF
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X04.ASM` containing:

```asm
DB 1GH
```

Reload `BA04.BAS` and run it with source name `X04`. Expect `ERROR line 1 : Bad number`; BASIC may print extra spaces around the line number. There must be no `OK` report. On a fresh workbench there must be no `X04.COM`. If an older file exists, it is left unchanged and must not be mistaken for a new result.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
