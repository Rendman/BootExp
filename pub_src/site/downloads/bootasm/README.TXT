THE BOOTSTRAP PROJECT - BOOTASM
A practical course in small-system software

Read the BOOTASM collection in order, beginning with The workbench.

BYTE.BAS    The first one-byte exercise.
VIEW.BAS    A file-length and hexadecimal byte viewer.
BA02.BAS through BA18.BAS: complete saved construction checkpoints.
BOOTASM.BAS The completed assembler; the same program as BA18.BAS.
CHECK.BAT   Runs a complete COM program and prints PASS or FAIL.
T02.ASM through T18.ASM: installment acceptance fixtures.
X02.ASM through X18.ASM: installment rejection fixtures.
HELLO.ASM, COPYBYTE.ASM, FAIL.ASM: complete example programs.

Use your own DOS and GW-BASIC interpreter. The workbench instructions
call the interpreter GWBASIC; use the name supplied on your own disk.
Copy the desired source to SOURCE.ASM, then run GWBASIC BOOTASM.BAS.
The accepted output is RESULT.COM. Preserve it under its program name. Require an OK report before treating output as new.
Save a tested copy of BOOTASM.BAS as BOOTKEEP.BAS before changing it.

Inspect encoding and data fixtures with VIEW.BAS. Do not execute them.
Only T09, T10, T17, T18 and the three complete examples are intended
as executable programs. CHECK FAIL must report FAIL: that example
returns a deliberately nonzero status.

Source is ASCII with DOS line endings and short filenames. BASIC line
numbers belong to the source. There are no preassembled programs in
this collection. Empty assembly output is valid for inspection only.
