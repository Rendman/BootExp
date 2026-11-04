THE BOOTSTRAP PROJECT - IR86
A practical course in small-system software

Begin with the completed BOOTASM and ASM86 collections.
Read The IR workbench before the construction installments.

BOOTASM.BAS The identical published BASIC bootstrap assembler.
ASM86.ASM   The identical published native assembler source.
AS07.ASM    The published reader used as the first source base.
IR01.ASM through IR26.ASM: complete construction checkpoints.
IR86.ASM    Completed translator, identical to IR26.ASM.
T01.IR through T26.IR: accepted input fixtures.
X01.IR through X26.IR: rejected input fixtures.
T-prefixed ASM files: expected text produced by the translator tests.
VIEW.BAS and CHECK.BAT: the unchanged published workbench helpers.
HELLO.IR, COUNT.IR, BYTES.IR: complete console example programs.
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

IR86 uses a word accumulator and a bounded expression stack.
Labels, transfers, calls, returns, DOS, and exits require empty
expression depth. JC/JNC must immediately follow DOS apart from
empty lines and comments. Consult the complete language reference
for syntax, register effects, segment use, diagnostics, and limits.

COPYFILE reads IN.TXT and creates or truncates OUT.TXT. Test it in
the work directory with the supplied sentence and compare the files.
It returns one on failure and can leave partial output after an I/O
error. It treats file contents as bytes, including Control-Z.

All sources are ASCII with DOS line endings and 8.3 filenames.
No preassembled executable or historical interpreter is included.
