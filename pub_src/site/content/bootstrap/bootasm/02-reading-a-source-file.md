+++
title = "02. Reading a source file"
weight = 2
description = "From lines of source to an exact sequence of bytes."
checkpoint = "BA02.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

A single byte is a useful disk experiment, but a program needs a sequence. We shall read one decimal byte from each source line and keep the result in memory until the whole source has been accepted.

## At the keyboard

Start a new BASIC program with `NEW`. Type the complete numbered listing below.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
10 ON ERROR GOTO 9500
20 DIM B%(4095)
30 SF$="SOURCE.ASM": OF$="RESULT.COM"
80 OPEN "I", #1, SF$
90 P=0: L=0
100 IF EOF(1) THEN 300
110 LINE INPUT #1, S$
120 L=L+1
160 IF S$="" THEN 100
170 I=INSTR(S$+" "," "): M$=LEFT$(S$,I-1)
180 A$=MID$(S$,I+1)
200 GOSUB 4000
210 GOTO 100
300 CLOSE #1
310 OPEN "O", #2, OF$
320 CLOSE #2
325 KILL OF$
330 OPEN "R", #2, OF$, 1
340 FIELD #2, 1 AS O$
345 IF P=0 THEN 380
350 FOR I=0 TO P-1
360 LSET O$=CHR$(B%(I)): PUT #2, I+1
370 NEXT I
380 CLOSE: PRINT "OK "; OF$; P; "bytes"
390 END
2000 IF T$="" THEN E$="Missing value": GOTO 9000
2020 N=0
2060 FOR NI=1 TO LEN(T$)
2070 D=ASC(MID$(T$,NI,1))-48
2080 IF D<0 OR D>9 THEN E$="Bad number": GOTO 9000
2090 N=N*10+D
2100 IF N>65535 THEN E$="Number too large": GOTO 9000
2110 NEXT NI: RETURN
3000 IF X<0 OR X>255 THEN E$="Byte out of range": GOTO 9000
3010 IF P=4096 THEN E$="Program too large": GOTO 9000
3020 B%(P)=X
3030 P=P+1: RETURN
4000 IF M$="DB" THEN GOSUB 4100: RETURN
4090 E$="Unknown instruction": GOTO 9000
4100 T$=A$: GOSUB 2000
4140 X=N: GOSUB 3000: RETURN
9000 PRINT "ERROR line"; L; ": "; E$
9010 CLOSE: END
9500 PRINT "BASIC error"; ERR; "at"; ERL
9510 CLOSE: END
```


Save the result before running it:

```basic
SAVE "BA02.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

`B%` is an integer array with 4,096 elements, numbered 0 through 4,095. `P` is the number of bytes collected; it is also the index of the next free element. This limit keeps the array to 8,192 bytes of BASIC storage. It deliberately limits our programs, rather than the processor.

Lines 80-210 open `SOURCE.ASM` as a sequential input file. `LINE INPUT` reads a whole line without treating commas as input separators. `L` counts physical source lines, including empty ones. At 170, the first space ends the instruction name `M$`; the remainder becomes the argument `A$`. At this checkpoint use uppercase `DB`, one space, and one decimal number.

The dispatcher at 4000 selects the routine for `DB`, meaning *define byte*. Routine 2000 takes a number in `T$` and returns its value in `N`. It changes `NI` and `D`, but leaves the argument string alone. Each digit is checked before it is included; the bound is checked after each multiplication. This avoids accepting BASIC expressions or mistyped suffixes.

Routine 3000 takes a byte in `X`, checks its range and available space, and advances `P`. It preserves `N`. The output loop opens a fresh file only after the source succeeds. Line 345 skips the FOR loop for an empty image: GW-BASIC enters a FOR body once even when its starting value already exceeds its limit. One-character random records write exactly one byte each. `OPEN "O"` followed by `CLOSE` first ensures that the output name exists. `KILL` then removes it before the random file is created, so a shorter assembly cannot leave an old tail. Closing a sequential output file can leave a DOS end-of-file character; removing that file also makes a truly empty result possible. BASIC's `BSAVE` adds a header, which a `.COM` file must not have.

The error exits close all open files. An assembly error leaves any existing `.COM` file unchanged. An input/output error while writing can leave a partial file; only an `OK` report means the write finished.

## A visible check

At DOS, create `T02.ASM` with the following exact source. `COPY CON T02.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
DB 65
DB 66
DB 67
```

From DOS start the checkpoint:

```dos
COPY T02.ASM SOURCE.ASM
GWBASIC BA02.BAS
```

The assembler uses the filenames in line 30 without asking for input. The success report must name `RESULT.COM` and report **3 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `RESULT.COM`. The viewer must report length 3 and these bytes (spaces and line wrapping are immaterial):

```text
41 42 43
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X02.ASM` containing:

```asm
DB 256
```

Return to DOS, copy `X02.ASM` to `SOURCE.ASM`, then run `GWBASIC BA02.BAS`. Expect `ERROR line 1 : Byte out of range`; BASIC may print extra spaces around the line number. There must be no `OK` report. The accepted `RESULT.COM` must remain unchanged. Preserve it as HOLD.COM before this test and compare the files afterward; an older result must not be mistaken for a new successful assembly.

I don't want a mistyped number to cost me the file that worked. Seeing the same bytes after the rejected input tells me this version is worth keeping.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
