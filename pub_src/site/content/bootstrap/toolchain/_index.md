+++
title = "Rebuilding Our Tools in RILL"
weight = 9
description = "Use the self-compiling RILL compiler to rebuild the translator, assembler, and complete toolchain."
cover = true
download = "TOOLCHN.ZIP"
download_group = "tools/toolchain"
reader_names = 1
tool_id = "TOOLCHAIN"
collection_key = "toolchain"
+++

The RILL compiler now compiles its own source. We can use that language to write the IR translator and assembler, then let the three RILL-written tools rebuild the complete trio.

Begin after **A Compiler Written in Its Own Language**, including its compiler self-build comparisons. Preserve R0.COM, IWKEEP.COM, and ASMAKEEP.COM. Each has a known source and a successful build behind it.

The work proceeds in four installments:

1. **IR86 in RILL** constructs the translator using RILL procedures and the established IR contract.
2. **ASM86 in RILL** constructs the assembler with the same symbol, encoding, and image limits as its native predecessor.
3. **Building the Three Tools** establishes the compiler, translator, and assembler builds and produces two rebuild generations using the RILL-written trio.
4. **Comparing Two Rebuild Generations** checks every corresponding executable and uses generation two to compile a complete program.

Read the workbench first. The complete source notebooks group each tool by its declarations and procedures. Keep the native builders separately named while building and checking their RILL replacements.

The [disk source collection](../../downloads/tools/toolchain/TOOLCHN.ZIP) includes RILL.RIL, IR86.RIL, ASM86.RIL, TMAKE.BAT, the native prerequisites, inspection helpers, and all earlier continuation checkpoints and fixtures. It contains source only. The language and target contracts remain those established by the completed RILL, native IR86, and ASM86 collections.
