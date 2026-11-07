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

## What we're adding

- **IR86 written in RILL:** Implement the established IR parser and native binding in RILL so the translator can be rebuilt by the RILL compiler.
- **ASM86 written in RILL:** Implement streamed assembly, symbol pages and instruction encoding in RILL so the assembler can join the same rebuild process.
- **An explicit bootstrap handoff:** Use the preserved native builders to establish the first RILL implementations so each replacement has a known source and builder.
- **Two complete rebuild generations:** Let the RILL-written compiler, translator and assembler rebuild all three tools and compare corresponding executables so the complete toolchain is reproducible.

**Removing:** The rebuild generations' dependence on the native translator and assembler. The preserved native tools still establish the initial RILL builds; the accepted languages, encodings and image bounds remain the same.

## The construction

Begin after **A Compiler Written in Its Own Language**, including its compiler self-build comparisons. Preserve R0.COM, IWKEEP.COM, and ASMAKEEP.COM. Each has a known source and a successful build behind it.

The work proceeds in four installments:

1. **IR86 in RILL** constructs the translator using RILL procedures and the established IR contract.
2. **ASM86 in RILL** constructs the assembler with the same symbol, encoding, and image limits as its native predecessor.
3. **Building the Three Tools** establishes the compiler, translator, and assembler builds and produces two rebuild generations using the RILL-written trio.
4. **Comparing Two Rebuild Generations** checks every corresponding executable and uses generation two to compile a complete program.

Read the workbench first. The complete source notebooks group each tool by its declarations and procedures. Keep the native builders separately named while building and checking their RILL replacements.

The [disk source collection](../../downloads/tools/toolchain/TOOLCHN.ZIP) includes RILL.RIL, IR86.RIL, ASM86.RIL, TMAKE.BAT, the native prerequisites, inspection helpers, and the native IR, RILLBOOT, and RILL compiler continuation checkpoints and fixtures. The separate RILL0 source collection supplies R01 through R39. It contains source only. The language and target contracts remain those established by the completed RILL, native IR86, and ASM86 collections.
