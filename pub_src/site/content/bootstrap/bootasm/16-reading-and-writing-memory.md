+++
title = "16. Reading and writing memory"
weight = 16
description = "Transfer bytes and words through BX or a named address."
checkpoint = "BA16.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

Registers hold working values; a source buffer belongs in memory. We shall add just two ways to name a memory location.

## At the keyboard

Load the preceding checkpoint, `BA15.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 4200 / 4210; 4220 / 4222; 4530 / 4900. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
4205 IF LEFT$(A1$,1)="[" THEN GOSUB 4700: RETURN
4221 IF LEFT$(A2$,1)="[" THEN GOSUB 4600: RETURN
4600 T$=A2$: GOSUB 4800
4610 X=138+WD: GOSUB 3000
4620 X=8*RD+RM: GOSUB 3000
4630 IF RM=6 THEN N=MA: GOSUB 3100
4640 RETURN
4700 T$=A2$: GOSUB 6000
4710 IF R<0 THEN E$="Register required": GOTO 9000
4720 RD=R: WD=W: T$=A1$: GOSUB 4800
4730 X=136+WD: GOSUB 3000
4740 X=8*RD+RM: GOSUB 3000
4750 IF RM=6 THEN N=MA: GOSUB 3100
4760 RETURN
4800 IF RIGHT$(T$,1)<>"]" THEN E$="Bad memory operand": GOTO 9000
4810 T$=MID$(T$,2,LEN(T$)-2)
4820 MA=0: RM=7
4830 IF T$="BX" THEN RETURN
4840 RM=6: GOSUB 2000: MA=N
4850 RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
4200 GOSUB 5000: T$=A1$: GOSUB 6000
4210 IF R<0 THEN E$="Register required": GOTO 9000
4220 RD=R: WD=W
4222 T$=A2$: GOSUB 6000
4530 RETURN
4900 IF A$<>"" THEN E$="Unexpected operand": GOTO 9000
```

Save the result before running it:

```basic
SAVE "BA16.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

Square brackets mean the contents of memory. `MOV AL,[BX]` loads the byte at DS:BX; `MOV [BX],AL` stores it. `MOV AX,[ITEM]` loads a word at the named offset, and `MOV [ITEM],AX` stores a word there. A word accesses two consecutive bytes. Without brackets, ITEM means the address itself. The register operand determines whether to transfer a byte or a word.

Routine 4800 takes the bracketed text in `T$`. It checks the closing bracket and removes both brackets. `[BX]` returns `RM=7` with no displacement. Every other accepted operand is a numeric or named direct offset, returning `RM=6` and `MA` as its value. It changes the value reader's scratch variables; it preserves `RD` and `WD`.

The ModR/M mode bits are 00. In that mode, r/m=7 means [BX], while r/m=6 is the special direct-address form followed by a low-byte-first 16-bit offset. Routine 4600 uses the load opcode 8AH or 8BH. Routine 4700 first finds the source register, then uses store opcode 88H or 89H. Both place the register number in the middle field and emit the direct offset only when `RM=6`.

The CPU also supports combinations such as [BX+SI] and other segment choices. BOOTASM does not parse them. Fetch or store through BX and adjust BX explicitly, or use a direct label. Memory-to-memory MOV and immediate-to-memory MOV are also excluded. This keeps size and direction unambiguous without BYTE PTR or WORD PTR syntax.

The fixture uses the harmless direct offset 0200H for encoding checks. It is not intended to run.

## A visible check

At DOS, create `T16.ASM` with the following exact source. `COPY CON T16.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
MOV AL,[BX]
MOV [BX],AL
MOV AX,[200H]
MOV [200H],AX
```

From DOS start the checkpoint:

```dos
COPY T16.ASM SOURCE.ASM
GWBASIC BA16.BAS
```

The assembler uses the filenames in line 30 without asking for input. The success report must name `RESULT.COM` and report **12 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `RESULT.COM`. The viewer must report length 12 and these bytes (spaces and line wrapping are immaterial):

```text
8A 07 88 07 8B 06 00 02 89 06 00 02
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X16.ASM` containing:

```asm
MOV [BX],1
```

Return to DOS, copy `X16.ASM` to `SOURCE.ASM`, then run `GWBASIC BA16.BAS`. Expect `ERROR line 1 : Register required`; BASIC may print extra spaces around the line number. There must be no `OK` report. The accepted `RESULT.COM` must remain unchanged. Preserve it as HOLD.COM before this test and compare the files afterward; an older result must not be mistaken for a new successful assembly.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
