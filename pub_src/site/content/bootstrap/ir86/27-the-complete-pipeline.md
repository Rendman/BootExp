+++
title = "27 · The complete translation pipeline"
weight = 27
description = "Build the translator with ASM86, then translate, assemble, and run a file-copy program."
download = "IR86.ASM"
+++

The completed IR86 translator is the saved IR26 program. This installment adds no translator source. It checks the complete route from a source program to a DOS executable which reads and writes files.

## Preserve a working translator

At DOS:

```dos
COPY IR26.ASM IR86.ASM
CHECK ASMKEEP
```

Enter IR86 at the assembler prompt. Require `OK 03871 bytes` and PASS. Then preserve the executable:

```dos
COPY IR86.COM IRKEEP.COM
```

ASMKEEP is the completed ASM86 preserved in the workbench guide. Its executable comes from BOOTASM; it directly assembles this translator's source. No other assembler or runtime library participates.

## A program that copies a file

Save the following as COPYFILE.IR. IN0 and OUT0 begin consecutive zero-terminated filename bytes. INPUT and OUTPUT retain DOS handles; DATA is the one-byte transfer buffer.

```ir
BYTE IN0 73
BYTE IN1 78
BYTE IN2 46
BYTE IN3 84
BYTE IN4 88
BYTE IN5 84
BYTE IN6 0
BYTE OUT0 79
BYTE OUT1 85
BYTE OUT2 84
BYTE OUT3 46
BYTE OUT4 84
BYTE OUT5 88
BYTE OUT6 84
BYTE OUT7 0
WORD INPUT 0
WORD OUTPUT 0
BUFFER DATA 1
LABEL MAIN
ADDR IN0
TODX
LIT 3D00H
DOS
JC FAILURE
ST INPUT
ADDR OUT0
TODX
LIT 0
TOCX
LIT 3C00H
DOS
JC FAILURE
ST OUTPUT
LABEL AGAIN
LD INPUT
TOBX
LIT 1
TOCX
ADDR DATA
TODX
LIT 3F00H
DOS
JC FAILURE
JZ FINISH
LD OUTPUT
TOBX
LIT 1
TOCX
ADDR DATA
TODX
LIT 4000H
DOS
JC FAILURE
PUSH
LIT 1
NE FAILURE
JMP AGAIN
LABEL FINISH
LD INPUT
TOBX
LIT 3E00H
DOS
JC FAILURE
LD OUTPUT
TOBX
LIT 3E00H
DOS
JC FAILURE
HALT
LABEL FAILURE
LIT 1
EXIT
```

The names spell IN.TXT and OUT.TXT. Function 3DH opens input read-only. Function 3CH creates or truncates output with ordinary attributes in CX. Both return a handle in AX or set carry on failure. Each JC is the next nonempty instruction after DOS, and ST saves the successful handle before another operation changes AX.

Function 3FH reads one byte into DATA. A zero count means end of file, so JZ selects the closing path. A successful nonempty read is followed by a one-byte write with function 40H. The program checks both carry and the returned count; a short write is a failure even when carry is clear. The comparison consumes the saved count before transferring.

Both handles are closed with function 3EH before HALT returns zero. FAILURE returns one; DOS closes remaining process handles on termination. A failure after output creation can leave an incomplete OUT.TXT. This program copies bytes without treating Ctrl-Z as a file terminator.

## Translate and assemble

```dos
CHECK IRKEEP
```

Enter COPYFILE. Require `OK COPYFILE.ASM 01242 text bytes` and PASS. TYPE COPYFILE.ASM to inspect the generated header, prefixed names, and DOS-call sequences. Then:

```dos
CHECK ASMKEEP
```

Enter COPYFILE again. Require `OK 00198 bytes` and PASS. IR86 produced text; ASM86 produced the machine file. A successful first step cannot substitute for a successful second step.

## Copy and compare

Use COPY CON IN.TXT to enter:

```text
An IR86 file copy.
```

Finish with Ctrl-Z and Enter. Run:

```dos
CHECK COPYFILE
TYPE OUT.TXT
COMP IN.TXT OUT.TXT
```

Require PASS, the same displayed sentence, and the DOS COMP matching-files report with no differing bytes. Answer N when COMP asks whether to compare more files. DOS 3.10 may report `Eof mark not found` for a file without a text end marker; the comparison must still report `Files compare ok`. Comparing displayed text alone would miss differences in undisplayed bytes.

For a failure check, rename the input before running the program:

```dos
REN IN.TXT HOLD.TXT
CHECK COPYFILE
REN HOLD.TXT IN.TXT
```

Use HOLD.TXT only if that name is free. CHECK must report FAIL for the missing input. The earlier OUT.TXT is not replaced because input opening precedes output creation. An unexpected PASS means this rejection check did not behave as specified.

The program exercises declarations, pointers, word storage, loops, comparisons, register transfers, and checked file services. If it differs, inspect the generated assembly before changing the source: verify filename zeroes, handle stores, and the placement of each carry branch. Keep ASMKEEP and IRKEEP intact while diagnosing a failed program.
