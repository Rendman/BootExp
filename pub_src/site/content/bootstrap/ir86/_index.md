+++
title = "Building an Intermediate Language"
weight = 5
description = "ASM86 builds every saved source in this collection. The translator always reads SOURCE.IR and writes RESULT.ASM. Preserve the completed translator as IRKEEP.COM; make the identical IWKEEP.COM copy used by later workbenches."
download = "IR86.ASM"
download_group = "tools/ir86"
reader_names = 1
cover = true
tool_id = "IR86"
collection_key = "ir86"
+++

This collection builds one native translator from a bounded reader through procedure frames, strings, file streams, and allocated workspace. The first small translator grows into the translator that builds the compiler. ASM86 assembles every stage.

The language defines word values, a virtual accumulator, an expression stack, byte addresses, and opaque service handles. The 8086 instructions appear in the backend templates and DOS binding; they are not part of the IR program interface.

Read the workbench first. The [source collection](../../downloads/tools/ir86/IR86.ZIP) contains plain source and test files.
