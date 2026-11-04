+++
title = "07. Instructions without operands"
weight = 7
description = "The first mnemonics and their one-byte encodings."
checkpoint = "BA07.BAS"
+++

A mnemonic is a name for an instruction. Five instructions with fixed one-byte encodings let us add names without yet designing an operand parser.

## At the keyboard

Load the preceding checkpoint, `BA06.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 4000 / 4090; 4180 / 8000. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
4010 X=-1
4012 IF M$="NOP" THEN X=144
4014 IF M$="RET" THEN X=195
4016 IF M$="CLD" THEN X=252
4018 IF M$="LODSB" THEN X=172
4020 IF M$="STOSB" THEN X=170
4022 IF X>=0 THEN GOSUB 4900: RETURN
4900 IF A$<>"" THEN E$="Unexpected operand": GOTO 9000
4910 GOSUB 3000: RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
4000 IF M$="DB" OR M$="DW" THEN GOSUB 4100: RETURN
4090 E$="Unknown instruction": GOTO 9000
4180 RETURN
8000 IF LEN(F$)<1 OR LEN(F$)>8 THEN E$="Bad filename": GOTO 9000
```

Save the result before running it:

```basic
SAVE "BA07.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

The dispatcher sets `X` to -1, meaning that no fixed instruction has matched. A match replaces it with an opcode, the byte which tells the processor what to do. Routine 4900 checks that there is no argument before passing `X` to the emitter. It changes `P`, preserving the source arguments.

`NOP` performs no operation. `RET` takes a return address from the stack. `CLD` clears the direction flag so string instructions advance their indexes. `LODSB` loads AL from DS:SI, then advances or retreats SI according to that flag. `STOSB` stores AL at ES:DI and adjusts DI. DS and ES are segment registers; SI and DI are index registers. These last instructions are included for explicit byte-by-byte work, rather than repeated string operations.

At this checkpoint we are checking encodings only. In particular, a stray RET or string instruction is not a complete test program: the stack, segment registers, and indexes must have suitable values. Inspect this fixture without running it.

## A visible check

At DOS, create `T07.ASM` with the following exact source. `COPY CON T07.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
NOP
RET
CLD
LODSB
STOSB
```

From DOS start the checkpoint:

```dos
GWBASIC BA07.BAS
```

At its source-name prompt enter `T07` without an extension. The success report must name `T07.COM` and report **5 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `T07.COM`. The viewer must report length 5 and these bytes (spaces and line wrapping are immaterial):

```text
90 C3 FC AC AA
```

This is an encoding or data fixture. Inspect it with the viewer; **do not execute it**.

## An error worth catching

Create `X07.ASM` containing:

```asm
NOP 1
```

Reload `BA07.BAS` and run it with source name `X07`. Expect `ERROR line 1 : Unexpected operand`; BASIC may print extra spaces around the line number. There must be no `OK` report. On a fresh workbench there must be no `X07.COM`. If an older file exists, it is left unchanged and must not be mistaken for a new result.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
