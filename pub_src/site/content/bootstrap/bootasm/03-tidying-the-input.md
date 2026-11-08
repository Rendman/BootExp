+++
title = "03. Tidying the input"
weight = 3
description = "Making room for spaces, comments, and lowercase letters."
checkpoint = "BA03.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

I want to leave myself a note beside a byte and indent a line so I can find it again. The magazine listings do that, but my little reader expects everything in just the right place. I'll let it clear away spaces and comments before it tries to understand a line.

## At the keyboard

Load the preceding checkpoint, `BA02.BAS`. Keep its working copy. Replace lines 180. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 120 / 160; 180 / 200; 390 / 2000. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
125 IF L>2000 THEN E$="Too many source lines": GOTO 9000
130 IF LEN(S$)>120 THEN E$="Source line too long": GOTO 9000
150 GOSUB 1000
180 A$=""
185 FOR J=I+1 TO LEN(S$)
190 C$=MID$(S$,J,1): IF C$<>" " THEN A$=A$+C$
195 NEXT J
1000 FOR I=1 TO LEN(S$)
1010 C=ASC(MID$(S$,I,1))
1020 IF C=9 THEN MID$(S$,I,1)=" "
1030 IF C>=97 AND C<=122 THEN MID$(S$,I,1)=CHR$(C-32)
1040 NEXT I
1050 I=INSTR(S$,";"): IF I>0 THEN S$=LEFT$(S$,I-1)
1060 IF LEFT$(S$,1)=" " THEN S$=MID$(S$,2): GOTO 1060
1070 IF RIGHT$(S$,1)=" " THEN S$=LEFT$(S$,LEN(S$)-1): GOTO 1070
1080 RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
120 L=L+1
160 IF S$="" THEN 100
170 I=INSTR(S$+" "," "): M$=LEFT$(S$,I-1)
180 A$=MID$(S$,I+1)
200 GOSUB 4000
390 END
2000 IF T$="" THEN E$="Missing value": GOTO 9000
```

Save the result before running it:

```basic
SAVE "BA03.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

Routine 1000 takes `S$` and returns a cleaned line in the same variable. It changes `I`, `C`, and individual characters. ASCII lowercase letters are 32 greater than their uppercase partners; tabs become spaces. A semicolon begins a comment, and the loops at 1060-1070 remove spaces from the ends. They also handle a line containing only spaces.

The argument builder at 180-195 removes spaces from operands. There are no quoted strings in this language, so there is no quoted space to preserve. Write each number as one token even though this small parser ignores operand spaces. The mnemonic still ends at the first space.

The source is limited to 2,000 physical lines of at most 120 characters each. Both limits keep a typing error from becoming an unmanageable job. Line 30 names SOURCE.ASM and RESULT.COM directly. COPY selects the source before the interpreter starts, so the assembler needs no console filename reader or filename validator.

## A visible check

At DOS, create `T03.ASM` with the following exact source. `COPY CON T03.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
; Three letters
  db 65 ; first

    db 66
DB 67
```

From DOS start the checkpoint:

```dos
COPY T03.ASM SOURCE.ASM
GWBASIC BA03.BAS
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

Create `X03.ASM` containing:

```asm
DB -1
```

Return to DOS, copy `X03.ASM` to `SOURCE.ASM`, then run `GWBASIC BA03.BAS`. Expect `ERROR line 1 : Bad number`; BASIC may print extra spaces around the line number. There must be no `OK` report. The accepted `RESULT.COM` must remain unchanged. Preserve it as HOLD.COM before this test and compare the files afterward; an older result must not be mistaken for a new successful assembly.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
