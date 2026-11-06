THE BOOTSTRAP PROJECT - RB
A practical course in small-system software

The compiler construction: first RILL -> RB compiler seed -> RC.
The preceding native ladder is BOOTASM -> ASM86 -> ASMA0 -> ASM86A
-> streaming IR86. Use the same DOS 3.10 and period BASIC workbench.
All files here are ASCII/CRLF/8.3 source. No executable is supplied.

ASM86A.ASM and IRWIDE.ASM: unchanged native prerequisite sources.
Preserve their tested executables as ASMAKEEP.COM and IWKEEP.COM.
VIEW.BAS and CHECK.BAT: unchanged inspection and status helpers.
RB01 through RB47: complete construction checkpoint sources.
T-prefixed and X-prefixed RIL files: exact acceptance/rejection inputs.
RILLBOOT.IR: complete compiler source, identical to the final checkpoint.
Early checkpoints are executable helper diagnostics. An emitted text
fragment is inspected as text; it is not a complete compiler result.
Require each fresh OK and PASS before copying the next result.

RB sources are IR, built with IWKEEP and ASMAKEEP. At the final
checkpoint preserve RB47.COM as RILLBOOT.COM and RB47.IR as RILLBOOT.IR.
The eight E-prefixed RIL programs use that completed compiler seed.
RILLBOOT reads SOURCE.RIL and streams RESULT.IR via RILL.TMP/RILL.BAK.
Copy accepted RESULT.IR to SOURCE.IR for IWKEEP; copy its accepted
RESULT.ASM to SOURCE.ASM for ASMAKEEP. Preserve every accepted output.
The separate RC collection expresses this same compiler in RILL.

Use fixed SOURCE.RIL/RESULT.IR, SOURCE.IR/RESULT.ASM and
SOURCE.ASM/RESULT.COM files in a hard-disk directory. Keep each builder
separately named. Inspect existing temporary/backup files before a run.
Source rejection preserves accepted output; failed publication can
leave recovery files. Require a new successful status before using it.
The shared systems language has 24-character folded names, 512 global
or procedure symbols, sixteen parameters and live local words, lexical
scopes, recursive calls, byte buffers, strings and opaque file/block
services. Consult the exact language reference for all bounds.
