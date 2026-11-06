+++
title = "RC"
weight = 8
description = "Write the RILL compiler in RILL and prove matching rebuilds."
cover = true
download = "RILL.RIL"
download_group = "rc"
+++

**BOOTASM → ASM86 → ASMA0 → ASM86A → IR86 → RILL → RB → RC.** Begin with the completed RB compiler seed, RILLBOOT.COM, and the preserved native IWKEEP and ASMAKEEP. RC expresses the compiler in the RILL language accepted by that seed.

Forty-three construction articles build the compiler one helper at a time. Each early diagnostic has its own visible test. Names, symbol records, streamed text, expression parsing, lexical scopes, procedure arguments, and complete functions become ordinary RILL procedures. RC43.RIL is the complete compiler, saved as RILL.RIL.

The reference states the same language contract as the completed RB seed. Complete programs exercise the RILL-written compiler. The self-build exercise compares two generations against the seed-built executable. The assembler source notebook and complete toolchain exercise then join IR86.RIL to rebuild all three tools twice using only the RILL-written trio.

The [RC disk sources](../../downloads/rc/RC.ZIP) include every compiler checkpoint, its fixtures, the compiler seed and native prerequisites, complete examples, and the RILL tool sources. The [complete toolchain archive](../../downloads/toolchain/TOOLCHN.ZIP) also includes all earlier continuation checkpoints and TMAKE.BAT. Both archives contain source only.

Read the workbench first. Keep the IR-written seed, native translator, and native assembler separately named throughout the self-builds.
