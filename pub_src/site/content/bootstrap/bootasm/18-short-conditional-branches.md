+++
title = "18. Short conditional branches"
weight = 18
description = "Let the flags choose a path, within a signed byte's reach."
checkpoint = "BA18.BAS"
download_group = "tools/bootasm"
reader_names = 1
+++

A comparison becomes useful when it can select the next instruction. The 8088 gives these conditional transfers a signed one-byte reach, so the assembler must check the distance.

## At the keyboard

Load the preceding checkpoint, `BA17.BAS`. Keep its working copy. Insert the other numbered lines in their numeric positions; leave all unlisted lines in place. New-line locations in the preceding listing: 4034 / 4090; 5550 / 6000. Each pair gives the existing lines on either side.

BASIC line numbers are part of the source. Enter a whole numbered line when replacing it.

```basic
4036 I=INSTR("JB  JAE JE  JNE JBE JA  ",M$+" ")
4038 IF I>0 THEN IF (I-1) MOD 4=0 THEN BC=(I-1)/4: GOSUB 5600: RETURN
5600 T$=A$: GOSUB 2000
5610 RV=N-(256+P+2)
5620 IF PS=2 THEN IF RV<-128 OR RV>127 THEN E$="Branch out of range": GOTO 9000
5630 C$=MID$("234567",BC+1,1)
5640 X=112+INSTR("0123456789ABCDEF",C$)-1: GOSUB 3000
5650 X=RV-256*INT(RV/256): GOSUB 3000
5660 RETURN
```


The following lines are **context from the preceding checkpoint**, not another block to type. Compare them to locate the replacements and insertion gaps:

```text
4034 IF M$="JMP" OR M$="CALL" THEN GOSUB 5500: RETURN
4090 E$="Unknown instruction": GOTO 9000
5550 GOSUB 3100: RETURN
6000 R=-1: W=0
```

Save the result before running it:

```basic
SAVE "BA18.BAS",A
```

Keep this filename for the stopping point; it is not a second program to type.

## How it works

The supported unsigned conditions are JB (below), JAE (above or equal), JE (equal), JNE (not equal), JBE (below or equal), and JA (above). JE and JNE work for either interpretation. The processor stores bit patterns; the branch instruction chooses how the comparison flags are interpreted.

The opcode table selects 72H through 77H. These conditions test carry and zero as shown in the reference. CMP must be near enough in the execution path that intervening instructions have not changed the flags it set. MOV, PUSH, POP, CALL, RET, and the branches do not themselves alter arithmetic flags; a called routine may do so.

Routine 5600 subtracts `256+P+2`, the address after this two-byte instruction, from the destination. Pass one does not check the reach of an unresolved name. Pass two requires a result from -128 through +127 inclusive. Subtracting `256*INT(RV/256)` converts a negative displacement to its unsigned byte pattern without BASIC's signed logical operators. The routine changes `T$`, the value-reader scratch variables, `RV`, `C$`, `X`, and `P`; `BC` retains the selected condition.

There is no automatic long conditional branch on an 8088. To reach a distant destination, branch on the opposite condition to a nearby label, then use a near JMP. That sequence belongs in the source, where its size and meaning are visible.

The executable test starts DL at the character 0, displays it, advances to the next character, and repeats until DL reaches the character 3. DOS function 02H leaves DL available for this loop; AH is loaded each time.

## A visible check

At DOS, create `T18.ASM` with the following exact source. `COPY CON T18.ASM` accepts text from the keyboard; finish with Ctrl-Z and Enter. Ctrl-Z is the end-of-input keystroke, not a character to include in a source line. A text editor which saves plain ASCII is also suitable.

```asm
MOV DL,30H
AGAIN:
MOV AH,2
INT 21H
INC DX
CMP DL,33H
JB AGAIN
MOV AX,4C00H
INT 21H
```

From DOS start the checkpoint:

```dos
GWBASIC BA18.BAS
```

At its source-name prompt enter `T18` without an extension. The success report must name `T18.COM` and report **17 bytes**. After the program ends at BASIC's `Ok` prompt, inspect the file:

```basic
RUN "VIEW.BAS"
```

At `File:` enter `T18.COM`. The viewer must report length 17 and these bytes (spaces and line wrapping are immaterial):

```text
B2 30 B4 02 CD 21 42 80 FA 33 72 F6 B8 00 4C CD 21
```

This fixture is a complete program. Return to DOS with `SYSTEM`, then run it through the shared status check:

```dos
CHECK T18
```

It must display `012`, followed on a new line by `PASS` from the batch file. `FAIL` means the program returned a nonzero status. The checker is printed in the workbench section.

## An error worth catching

Create `X18.ASM` containing:

```asm
JE 400H
```

Reload `BA18.BAS` and run it with source name `X18`. Expect `ERROR line 1 : Branch out of range`; BASIC may print extra spaces around the line number. There must be no `OK` report. On a fresh workbench there must be no `X18.COM`. If an older file exists, it is left unchanged and must not be mistaken for a new result.

## If the result differs

Check the changed line numbers first, then compare the test source with the listing above. A BASIC error names a BASIC line; `ERROR line` names a line in the assembly input. A missing source file produces a BASIC file error. Keep the preceding checkpoint until both the byte check and rejection check agree.
