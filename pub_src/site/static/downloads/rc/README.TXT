THE BOOTSTRAP PROJECT - RC
A practical course in small-system software

The compiler construction: RILL0 -> RB compiler seed -> RC.
The preceding native ladder is BOOTASM -> ASM86 -> ASMA0 -> ASM86A
-> streaming IR86. Use the same DOS 3.10 and period BASIC workbench.
All files here are ASCII/CRLF/8.3 source. No executable is supplied.

ASM86A.ASM and IRWIDE.ASM: unchanged native prerequisite sources.
Preserve their tested executables as ASMAKEEP.COM and IWKEEP.COM.
VIEW.BAS and CHECK.BAT: unchanged inspection and status helpers.
RC01 through RC43: complete construction checkpoint sources.
T-prefixed and X-prefixed RIL files: exact acceptance/rejection inputs.
RILL.RIL: complete compiler source, identical to RC44.RIL.
RC44.RIL: the 64-local extension after the first self-build comparisons.
Early checkpoints are executable helper diagnostics. An emitted text
fragment is inspected as text; it is not a complete compiler result.
Require each fresh OK and PASS before copying the next result.

Begin with the completed RB collection and its RILLBOOT.COM.
RILLBOOT.IR is its unchanged source, built with IWKEEP and ASMAKEEP.
Compile RC sources with RILLBOOT, then IWKEEP and ASMAKEEP.
Preserve RC43.COM for the first self-build comparisons of RC43.RIL.
Then apply RC44, compiled with the tested RC43. Compile RC44 with itself
to establish R0 using 64-slot frames; save RC44.RIL as RILL.RIL.
R0 compiles that same source to R1, then R1 to R2; both match R0 exactly.
TLOCAL.RIL, XLOCAL.RIL and TSCOPE.RIL check local/frame bounds and reuse.
ERECUR.RIL, EHEAP.RIL and ECOPY.RIL are complete compiler examples.
IR86.RIL and ASM86A.RIL are the translator and assembler in RILL.
TMAKE.BAT builds all three tools and both closed-loop generations.
The complete TOOLCHN.ZIP also contains earlier continuation sources.

Use fixed SOURCE.RIL/RESULT.IR, SOURCE.IR/RESULT.ASM and
SOURCE.ASM/RESULT.COM files in a hard-disk directory. Keep each builder
separately named. Inspect existing temporary/backup files before a run.
Source rejection preserves accepted output; failed publication can
leave recovery files. Require a new successful status before using it.
The complete RILL language has 24-character folded names, 512 global
or procedure symbols, sixteen parameters and sixty-four live local words, lexical
scopes, recursive calls, byte buffers, strings and opaque file/block
services. RILLBOOT accepts the subset used to implement that compiler.
Consult each compiler's own reference for accepted syntax and bounds.
