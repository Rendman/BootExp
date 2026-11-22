+++
title = "14 \u00b7 A longer source count"
weight = 14
description = "Keep source extent separate from the emitted image limit."
download = "A08.ASM"
aliases = ["/bootstrap/asm86a/08-a-longer-source-count/"]
download_group = "tools/asm1"
reader_names = 1
url = "/bootstrap/asma0/08-a-longer-source-count/"
+++

I look at the comments and labels in my source: much of what I type never becomes an instruction byte. The block reader can keep going through a long file, but its line counter still stops at 4000. I'll extend that counter's permitted range while keeping a check against wraparound.

**Starting source:** `A07.ASM`. **Save as:** `A08.ASM`. **Build with:** `ASMKEEP.COM`.

## The working parts

READLINE permits up to 65535 physical lines per pass instead of the earlier 4000. It checks before a count can wrap; at this limit the diagnostic remains saturated at the last representable line. Width remains 120 characters.

READLINE still treats CR/LF as one ending, accepts bare CR or LF and a final unterminated line, and recognizes source Control-Z. A block refill may split any of these sequences. This is a bounded counter change, not a source-file buffer.

## Enter the source

Copy `A07.ASM` to `A08.ASM`. Apply the changes in the order shown, working upward through the old source. Use Find to locate each label, including its colon, and confirm that it stands alone on a source line. The locator blocks are existing source: leave them in place and type only the stated insertion or replacement. Blank lines and comment-only lines may differ in your copy.

### Change 1 · `READFAIL:`

Find the unique label `READFAIL:`, then follow this unchanged source through its last displayed instruction:

```asm
READFAIL:
MOV DX,[LINENO]
INC DX
```

The edit begins immediately after that unchanged block.

Insert:

```asm
READLIMIT:
```

### Change 2 · `READFAIL:`

Find the unique label `READFAIL:`, then follow this unchanged source through its last displayed instruction:

```asm
READFAIL:
MOV DX,[LINENO]
```

The edit begins immediately after that unchanged block.

Insert:

```asm
CMP DX,0FFFFH
JE READLIMIT
```

### Change 3 · `LINEEND:`

Find the unique label `LINEEND:`, then follow this unchanged source through its last displayed instruction:

```asm
LINEEND:
MOV AL,0
STOSB
MOV AX,[LINENO]
INC AX
```

The edit begins immediately after that unchanged block.

Replace this existing source:

```asm
CMP AX,4000
JA READFULL
```

With:

```asm
CMP AX,0
JNE LINECOUNTSAFE
MOV AX,5
JMP ERROR
LINECOUNTSAFE:
```

## Build the stopping point

Copy `A08.ASM` to `SOURCE.ASM`, run `CHECK ASMKEEP`, and require `OK 03466 bytes` and PASS. This uses the preceding published ASM0, not the new checkpoint. Preserve the accepted executable with `COPY RESULT.COM A08.COM`.

Keep that executable and source together.

## Acceptance check

Reuse the earlier input unchanged:

```dos
COPY T02.ASM T08.ASM
```

```dos
CHECK A08 T08.ASM RESULT.COM
```

Require:

```text
OK RESULT.COM 00011 bytes
PASS
```

In VIEW.BAS, inspect RESULT.COM. Require length **11 bytes** and these complete contents:

```text
B2 41 B4 02 CD 21 B8 00 4C CD 21
```

The byte inspection checks the accepted result. Keep it as data.

## Pass the old line-count limit

Reuse STREAM.BAS from the block-reader exercise. Run GWBASIC STREAM.BAS, then replace these two BASIC lines:

```basic
10 N=4000
40 PRINT #1,";"
```

Leave line 60 as `60 PRINT #1,"DB 66"`. Save this version under its own name, then run it:

```basic
SAVE "LINES.BAS",A
RUN
SYSTEM
```

Require LONG.ASM READY before leaving BASIC. The source now has 4000 comment lines and one DB statement: 4001 physical lines with one emitted byte. STREAM.BAS retains the earlier block exercise; LINES.BAS retains these comment-generating lines.

```dos
CHECK A08 LONG.ASM RESULT.COM
```

Require `OK RESULT.COM 00001 bytes` and PASS. VIEW.BAS must show exactly `42`. A07 stops at this source's line 4001 with code 5; A08 must reach the data statement.

## Check the representable limit

Run GWBASIC LINES.BAS. At its prompt set line 10 to `10 N=65534`, RUN, and return to DOS with SYSTEM. This creates 65535 physical lines, including the final DB statement. Run the same CHECK command: require `OK RESULT.COM 00001 bytes` and PASS, with exactly `42` in VIEW.BAS.

Preserve that accepted result with `COPY RESULT.COM HOLD.COM`. Run GWBASIC LINES.BAS again, set line 10 to `10 N=65535`, RUN and return with SYSTEM. There are now 65536 physical lines:

```dos
CHECK A08 LONG.ASM RESULT.COM
C:\DOS\FC.EXE /B HOLD.COM RESULT.COM
```

Require `ERROR 65535 CODE 5` and FAIL, followed by FC reporting no differences. The line report remains at 65535 because the counter cannot represent 65536; it must never wrap to zero. Run the saved LINES.BAS again and return with SYSTEM to restore its 4001-line input. Keep these outputs as data.

An unexpected PASS fails this rejection test.

## If the result differs

Check the limit before LINENO wraps from FFFFH to zero. The rejection report stays at 65535 because a 16-bit counter cannot represent the next line.
