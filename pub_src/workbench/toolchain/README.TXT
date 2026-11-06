THE BOOTSTRAP PROJECT - THE TOOLCHAIN IN RILL
A practical course in small-system software

The ladder is BOOTASM -> ASM86 -> ASMA0 -> ASM86A -> streaming IR86
-> IR-written RILL compiler seed -> RILL-written compiler, translator,
and assembler -> two matching rebuild generations of all three tools.

BOOTASM.BAS and ASM86.ASM are the unchanged published foundation.
ASMA0.ASM and ASM86A.ASM are the unchanged native assembler milestones.
IRWIDE.ASM is the streaming native IR86 bootstrap translator.
RILLBOOT.IR is the compiler seed, authored in processor-neutral IR86.
RILL.RIL, IR86.RIL, ASM86A.RIL implement the three tools in RILL.
TMAKE.BAT builds both seed tools and all three RILL implementations,
then rebuilds each tool twice using only the RILL implementations.
VIEW.BAS and CHECK.BAT are the unchanged workbench helpers.
IW01.ASM through IW23.ASM: native streaming IR construction.
RB01.IR through RB47.IR: the IR-written compiler construction.
RC01.RIL through RC43.RIL: the compiler written in RILL.
T-prefixed inputs and X-prefixed rejection cases accompany those tools.
The named example RIL/IR files accompany the interface articles.

Use your own DOS 3.10 and its period BASIC interpreter. Begin with the
completed ASM86A workbench: ASMAKEEP.COM must be the tested 6422-byte
native assembler. Keep it and the sources on a separate labeled disk.
TMAKE deliberately preserves that builder. Do not start from a supplied
binary: none is present. Use a hard-disk working directory, with enough
space for source files, generated IR/assembly, and preserved executables.
The full course archive need not fit a single 360 KB floppy.

TMAKE prints each tool's OK followed by a visible PASS at each build.
A nonzero tool status immediately stops the batch with FAIL. Stop at
that first error; old output never proves a new successful translation.
A0.COM/I0.COM/R0.COM are the first RILL-written assembler/IR/compiler.
A1/I1/R1 and A2/I2/R2 are the next two generations.
ECHO N>NO.TXT answers COMP's compare-more-files question. Compare
A0.COM A1.COM, A0.COM A2.COM, I0.COM I1.COM, I0.COM I2.COM,
R0.COM R1.COM, and R0.COM R2.COM, each with COMP and <NO.TXT.
Every comparison must report no differences. Byte equality and fresh
successful builds are separate checks.

RILL reads SOURCE.RIL and publishes RESULT.IR using RILL.TMP/RILL.BAK.
IR86 reads SOURCE.IR and publishes RESULT.ASM using IRTX.TMP/IRRES.BAK.
ASM86A reads SOURCE.ASM and publishes RESULT.COM using ASMA.TMP and
RESULT.BAK. Existing recovery names prevent a new run; inspect them.
Each tool streams bounded blocks and preserves old output on source
rejection. A failed publication can leave recovery files. Require OK
and immediate status success before copying any result.

The RILL implementations require no outside compiler, assembler,
linker, embedded project executable, or physical-register escape.
IR words are sixteen bits; storage is byte-addressed. File and extra
memory-block handles are opaque. Procedures, local state, arguments,
word expressions, and quoted strings suffice to write the tools.
The target remains a COM image with at most 61184 emitted bytes.
The assembler retains 8192 symbols using separately allocated pages.
RILL supports 512 global/function symbols, 24-character folded names,
16 parameters, 16 simultaneously live local words, and block/expression
nesting of at most 16. Byte buffers are global; use allocated blocks for
larger tables. This is a bounded systems language, without Rust's
ownership checking or a claim of memory safety. Consult the references.

Every archive member is ASCII source with DOS line endings and an
8.3 name. No preassembled executable or historical interpreter is here.
