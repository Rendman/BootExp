+++
title = "A Compiler Written in Its Own Language"
weight = 8
description = "Write the RILL compiler in RILL and prove matching rebuilds."
cover = true
download = "RILL.RIL"
download_group = "tools/rill"
reader_names = 1
tool_id = "RILL"
collection_key = "rc"
+++

**BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL.** Begin with the completed RILLBOOT compiler seed, RILLBOOT.COM, and the preserved native IWKEEP and ASMAKEEP. RILL expresses the compiler in the RILL language accepted by that seed.

Forty-three construction articles build the compiler one helper at a time. Each early diagnostic has its own visible test. Names, symbol records, streamed text, expression parsing, lexical scopes, procedure arguments, and complete functions become ordinary RILL procedures. RC43.RIL is the first complete compiler. After its self-build comparisons, More Local Storage adds sixty-four local slots as RC44.RIL, saved as the final RILL.RIL.

The reference describes the complete RILL language. RILLBOOT accepts the smaller subset used to write this compiler; the RILL implementation also accepts XOR, left shift, unary minus, bitwise complement, addresses, and ordinary word-pointer loads and stores. Complete programs exercise the RILL-written compiler. The first self-build exercise compares two generations against the seed-built executable. The local-storage extension then establishes matching copies of the compiler with sixty-four-slot frames. The following [Rebuilding Our Tools in RILL](../toolchain/index.html) collection uses that tested compiler to construct IR86 and ASM86 in RILL and rebuild the complete trio twice.

The [RILL disk sources](../../downloads/tools/rill/RILL.ZIP) include every compiler checkpoint, its fixtures, the compiler seed and native prerequisites, and three complete examples. The separate [toolchain source collection](../../downloads/tools/toolchain/TOOLCHN.ZIP) includes the IR86 and ASM86 replacements and TMAKE.BAT. Both archives contain source only.

Read the workbench first. Keep the IR-written seed, native translator, and native assembler separately named throughout the self-builds.
