+++
title = "01. A byte on disk"
weight = 1
description = "Write one byte, then inspect it without running it."
checkpoint = "BYTE.BAS"
+++

Before writing an assembler, we need to know how BASIC can put an exact byte on disk. Our first program accepts one decimal value and writes a one-byte file. A second, smaller program shows that byte and the file's length. Together they require 39 BASIC lines; type and test them as two separate programs.

## One byte

At BASIC's `Ok` prompt type `NEW`, then enter this complete 21-line program:

```basic
10 ON ERROR GOTO 900
20 LINE INPUT "Decimal byte (0-255): "; T$
30 IF T$="" THEN PRINT "Bad byte": END
40 N=0
50 FOR I=1 TO LEN(T$)
60 D=ASC(MID$(T$,I,1))-48
70 IF D<0 OR D>9 THEN PRINT "Bad byte": END
80 N=N*10+D
90 IF N>255 THEN PRINT "Bad byte": END
100 NEXT I
110 OPEN "O", #1, "BYTE.COM"
120 CLOSE #1
130 OPEN "R", #1, "BYTE.COM", 1
140 FIELD #1, 1 AS B$
150 LSET B$=CHR$(N)
160 PUT #1, 1
170 CLOSE
180 PRINT "Wrote BYTE.COM: 1 byte"
190 END
900 PRINT "BASIC error"; ERR; "at"; ERL
910 CLOSE: END
```

Save with `SAVE "BYTE.BAS",A`, then `RUN`. At the decimal-byte prompt enter `65`. Expect `Wrote BYTE.COM: 1 byte`. This file is data for inspection; do not run it as a DOS program.

A byte holds 0 through 255. The digit loop checks each character before multiplying the accumulated value by ten and adding the new digit. It rejects a sign, a fraction, or a BASIC expression. `N` holds the value; `I` and `D` are scratch variables. No other program state must be preserved.

The first OPEN empties any existing BYTE.COM. The second OPEN uses random access with a record length of one. FIELD gives the one-byte buffer the string name `B$`; LSET copies one character into it, and PUT writes record one. CHR$ converts the number to the corresponding character code without writing its decimal digits. `PRINT #` would add formatting or line endings, so it is not used for machine bytes.

## Seeing the result

Save BYTE.BAS first. Type `NEW`, then this separate 18-line viewer:

```basic
10 ON ERROR GOTO 900
20 LINE INPUT "File: "; F$
25 OPEN "I", #1, F$: CLOSE #1
30 OPEN "R", #1, F$, 1
40 FIELD #1, 1 AS B$
50 N=LOF(1)
60 PRINT "Length:"; N
70 IF N=0 THEN CLOSE: END
80 FOR I=1 TO N
90 GET #1, I
100 PRINT RIGHT$("0"+HEX$(ASC(B$)),2); " ";
110 IF I MOD 16=0 THEN PRINT
120 NEXT I
130 IF N MOD 16<>0 THEN PRINT
140 CLOSE
150 END
900 PRINT "Cannot read file. BASIC error"; ERR
910 CLOSE: END
```

Save it with `SAVE "VIEW.BAS",A`. Run it and enter `BYTE.COM`. The result must include:

```text
Length: 1
41
```

BASIC may add spaces around numbers. The length must be one, and the hexadecimal byte must be 41. Hexadecimal is a compact way to write bytes; 41H means decimal 65. The viewer uses HEX$ and supplies a leading zero when needed. It shows sixteen bytes per display line.

The viewer takes its filename in `F$`, opens one-byte random records, and uses LOF for the exact length. `N` holds that length and `I` the current record. GET fills `B$`, and ASC reads its byte value. A valid zero-length file reports `Length: 0` and stops. The sequential-input OPEN at line 25 checks that the file already exists before the random OPEN; otherwise random access could create a missing file. A missing or unreadable file produces `Cannot read file. BASIC error` with BASIC's error number; it is not reported as an empty result.

## Rejecting a bad value

Load BYTE.BAS and run it with `256`, then with `-1`. Both must print `Bad byte`, without a `Wrote` report. The earlier BYTE.COM remains unchanged. Load VIEW.BAS again and check that it still has length one and byte 41.

If the viewer shows the decimal digits 6 and 5, check that the writer uses CHR$ and PUT rather than PRINT #. If the file has extra bytes, check both OPEN statements and the one-byte record length. A BASIC error report gives the BASIC line number; compare that line with the listing.
