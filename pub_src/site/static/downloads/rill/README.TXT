THE BOOTSTRAP PROJECT - RILL
A practical course in small-system software

Begin with the completed BOOTASM, ASM86, and IR86 collections.
Read The RILL workbench and follow the construction articles in order.

BOOTASM.BAS, ASM86.ASM, IR86.ASM: identical published bootstrap sources.
VIEW.BAS and CHECK.BAT: the unchanged published workbench helpers.
R01.IR through R29.IR: complete IR-written construction checkpoints.
RILL.IR: complete compiler source, identical to R29.IR.
Matching R-prefixed ASM files were produced by the published IR86.
RILL.ASM is the assembly output for the complete compiler.
T-prefixed RIL files: diagnostic or source-language acceptance input.
X-prefixed files: rejection input; early .IR files test IR transcription.
X09.RIL deliberately starts with invalid source byte 01.
T15.IR through T29.IR and their ASM files: expected compiler/IR output.
HELLO.RIL, COUNT.RIL, CHOICE.RIL, RLECHO.RIL: complete RILL programs.
Their matching IR and ASM files came from executing the published tools.

The compiler implementation is .IR; RILL program input is .RIL.
Use the completed BASIC bootstrap to build ASM86 and use ASM86 to build
IR86. Preserve ASM86.COM as ASMKEEP.COM and IR86.COM as IRKEEP.COM.
Translate R01.IR with CHECK IRKEEP, entering R01. Require OK and PASS.
Assemble R01.ASM with CHECK ASMKEEP, entering R01. Require OK and PASS.
Only then run CHECK R01. Repeat using each article's exact stopping test.
Early checkpoints are diagnostics and do not compile complete RILL.
The first empty-program compiler is R15. All checkpoints are executables.

Translate RILL.IR with IRKEEP, then assemble RILL.ASM with ASMKEEP.
The complete compiler image is 5173 bytes. Preserve it as RLKEEP.COM.
The compiler always reads SOURCE.RIL and writes RESULT.IR. Select a
program with COPY HELLO.RIL SOURCE.RIL, then run CHECK RLKEEP.
Require OK RESULT.IR nnnnn and PASS. Copy RESULT.IR to HELLO.IR.
Translate HELLO with IRKEEP, assemble HELLO with ASMKEEP, requiring
both OK reports and PASS. CHECK HELLO displays HI and reports PASS.

Syntax and input errors leave an older RESULT.IR unchanged. A result
create/write/close failure may leave partial output. Require a fresh OK.
CHECK reports a nonzero program status as FAIL. The construction exit
exercise deliberately returns one; its FAIL is the intended result.

RILL has one fn main(), a flat set of mutable one-letter variables,
decimal word literals, assignment, + and -, unary minus, parentheses,
if/else, while, putc, getc(), status(), and exit. All ordering is unsigned.
Arithmetic wraps modulo 65536. Declarations must come first and use
literal initializers. Consult the exact language reference for limits.
There are no user functions, arrays, strings, or native assembly escapes.

RLECHO reads a byte stream, not SOURCE.RIL. Run CHECK RLECHO <KEY.TXT.
It checks service status and distinguishes EOF 65535 from every byte.
The compiler treats Control-Z as source termination; RLECHO preserves it.

All source text is ASCII with DOS line endings and 8.3 filenames.
Use your own DOS and period BASIC interpreter. There is no preassembled
executable, historical interpreter, or outside compiler in this collection.
