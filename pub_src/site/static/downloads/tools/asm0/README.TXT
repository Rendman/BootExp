THE BOOTSTRAP PROJECT - ASM0
A practical course in small-system software

Begin with the completed BOOTASM collection and its BASIC workbench.
Read The assembly workbench before the construction installments.

BOOTASM.BAS The completed BASIC assembler from the BOOTASM collection.
AS01.ASM through AS28.ASM: complete saved construction checkpoints.
ASM0.ASM   Completed native assembler, identical to AS28.ASM.
VIEW.BAS    The unchanged BOOTASM length and hexadecimal byte viewer.
CHECK.BAT   The unchanged immediate DOS status checker.
T04.ASM through T28.ASM: checkpoint input fixtures.
X06.ASM through X28.ASM: source rejection fixtures where applicable.
HELLO.ASM, MEMORY.ASM, COUNT.ASM: three complete example programs.

Use your own DOS and period GW-BASIC interpreter. GWBASIC is the name
used in the articles; substitute the actual name on your disk.
COPY AS01.ASM SOURCE.ASM selects the source for GWBASIC BOOTASM.BAS.
After success, COPY RESULT.COM AS01.COM preserves the executable.
Require BASIC's OK and byte count; SYSTEM returns to DOS.
CHECK AS01 executes that complete checkpoint and prints PASS or FAIL.
Keep BOOTKEEP.BAS and a tested BASIC-built ASMKEEP.COM separately.

AS01 through AS28 are complete executable tools or diagnostics.
Their output fixtures are usually data or encoding exercises: inspect
with VIEW.BAS, including file length. Do not execute those outputs.
Only T24, T27, T28, and the three example programs are expressly
complete output programs. The rejection cases must report FAIL.

Copy the desired source to SOURCE.ASM, then run CHECK ASM0.
The output is RESULT.COM; copy it to the desired program name.
Source errors leave an older output unchanged. Require a fresh OK
before use; an I/O error during writing can leave a partial file.
The native tool requires a full 64 KB segment and entry SP=FFFEH.
Its limits are 8192 output bytes, 4000 lines, 120 characters per line,
16 characters per token/name, and 256 labels. See the reference.

All source is ASCII with DOS line endings and 8.3 filenames.
This collection contains no preassembled programs or interpreter.
