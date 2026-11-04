THE BOOTSTRAP PROJECT - IR86
A practical course in small-system software

Begin with the completed BOOTASM and ASM86 collections.
Read The IR workbench before the construction installments.

BOOTASM.BAS The identical published BASIC bootstrap assembler.
ASM86.ASM   The identical published native assembler source.
AS07.ASM    The published reader used as the first source base.
IR01.ASM through IR32.ASM: complete construction checkpoints.
IR86.ASM    Completed translator, identical to IR32.ASM.
T01.IR through T32.IR: accepted input fixtures.
X01.IR through X32.IR: rejected input fixtures.
T-prefixed ASM files: expected text produced by the translator tests.
VIEW.BAS and CHECK.BAT: the unchanged published workbench helpers.
HELLO.IR, COUNT.IR, BYTES.IR, ECHOIR.IR: complete portable examples.
RUNTIME.ASM: the 8086/DOS binding fragment; do not run it alone.
COPYFILE.IR: the complete file-copy pipeline program.
Matching example ASM files were produced by the translator.

Use your own DOS and period GW-BASIC interpreter. Build ASM86 with
GWBASIC BOOTASM.BAS, requiring BASIC's OK; SYSTEM returns to DOS.
Preserve a tested ASM86.COM as ASMKEEP.COM. Run CHECK ASMKEEP and
enter IR01, for example, to build a checkpoint directly.
All IR construction checkpoints are complete executable tools.
The first diagnostics do not create an assembly file.
The T03 output is data only: inspect it and do not execute it.
Other published emitted programs are expressly complete executables.

The finished path is NAME.IR -> IR86 -> NAME.ASM -> ASM86 -> NAME.COM.
Run CHECK IR86 and enter NAME. Require OK and PASS. Run CHECK ASMKEEP
and enter NAME again; require its own OK and PASS. Only then use the
new machine file. TYPE inspects text; VIEW.BAS inspects length/bytes.
Preserve a tested translator as IRKEEP.COM and keep its source.

Names at file prompts are 1-8 letters, digits, or underscores, without
path or extension. Use ordinary disk files, not DOS devices.
Source errors leave older assembly output untouched; I/O failures
during writing may leave partial output. Require a fresh OK.

IR86 defines virtual accumulator A and sixteen-bit word semantics.
Its source does not expose processor registers or flags. Runtime
services use opaque file handles, byte streams, and normalized STATUS.
Ordinary computations do not replace that status. READ/WRITE consume
a saved handle and buffer pointer, with the count in A. Consult the
language reference and its separate target-profile section.

COPYFILE reads IN.TXT and creates or truncates OUT.TXT. Test it in
the work directory with the supplied sentence and compare the files.
It returns one on failure and can leave partial output after an I/O
error. It treats file contents as bytes, including Control-Z.

All sources are ASCII with DOS line endings and 8.3 filenames.
No preassembled executable or historical interpreter is included.
