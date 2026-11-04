THE BOOTSTRAP PROJECT - ASM86
A practical course in small-system software

Begin with the completed BOOTASM collection and its BASIC workbench.
Read The assembly workbench before the construction installments.

BAWIDE.BAS  BOOTASM with the printed symbol-table changes.
AS01.ASM through AS29.ASM: complete saved construction checkpoints.
ASM86.ASM   Completed native assembler, identical to AS29.ASM.
VIEW.BAS    The unchanged BOOTASM length and hexadecimal byte viewer.
CHECK.BAT   The unchanged immediate DOS status checker.
T04.ASM through T29.ASM: checkpoint input fixtures.
X07.ASM through X29.ASM: source rejection fixtures where applicable.
HELLO.ASM, MEMORY.ASM, COUNT.ASM: three complete example programs.

Use your own DOS and period GW-BASIC interpreter. GWBASIC is the name
used in the articles; substitute the actual name on your disk.
GWBASIC BAWIDE.BAS builds a checkpoint. Enter AS01, for example.
Require BASIC's OK and byte count; SYSTEM returns to DOS.
CHECK AS01 executes that complete checkpoint and prints PASS or FAIL.
Keep BOOTKEEP.BAS and a tested BASIC-built ASMKEEP.COM separately.

AS01 through AS29 are complete executable tools or diagnostics.
Their output fixtures are usually data or encoding exercises: inspect
with VIEW.BAS, including file length. Do not execute those outputs.
Only T25, T28, T29, and the three example programs are expressly
complete output programs. The rejection cases must report FAIL.

Run CHECK ASM86 and enter a plain 1-8-character source base name.
Use ordinary disk names, not DOS devices such as CON or NUL.
Source errors leave an older output unchanged. Require a fresh OK
before use; an I/O error during writing can leave a partial file.
The native tool requires a full 64 KB segment and entry SP=FFFEH.
Its limits are 8192 output bytes, 4000 lines, 120 characters per line,
16 characters per token/name, and 256 labels. See the reference.

All source is ASCII with DOS line endings and 8.3 filenames.
This collection contains no preassembled programs or interpreter.
