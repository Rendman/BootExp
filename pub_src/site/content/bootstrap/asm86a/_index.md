+++
title = "Extending the 8086 Assembler"
weight = 4
description = "Build a larger assembler from the verified streaming seed."
cover = true
download = "ASM86.ASM"
download_group = "tools/asm86"
reader_names = 1
tool_id = "ASM86"
collection_key = "asm86a"
+++

**BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL.** ASM86 begins with the completed [ASM1 collection](../asma0/index.html). Its first executable is built by that verified streaming seed. ASM86 then assembles the same source twice and both generations must reproduce the seed-built executable.

The construction adds separately allocated symbol pages, exact-spelling bucket lookup, 8,192 symbols with names up to 31 characters, longer lines, and checked word-pair source counts. Expressions, quoted data, constants, zero-filled storage, legal 8086 memory-address combinations, frame-related instructions, and explicit conditional bridges receive their own stopping points.

Twenty-eight construction installments use the saved filenames A13.ASM through A40.ASM. The first starts from a copy of ASM1.ASM; the existing seed routines are retained. A complete ladder exercise, a language and memory reference, and four complete programs close the collection.

Read the workbench first and preserve ASM1.COM as the preceding builder. Preserve the completed ASM86.COM separately as ASMAKEEP.COM. The fixed files remain SOURCE.ASM and RESULT.COM; the processor remains the 8086/8088 and output remains DOS `.COM`.

The complete source link above is ASM86.ASM. The [ASM86 disk sources](../../downloads/tools/asm86/ASM86.ZIP) include the verified seed prerequisite, all twenty-four construction checkpoints, fixtures, helpers, and examples. The [ASM1 disk sources](../../downloads/tools/asm1/ASM1.ZIP) contain the seed's own construction. Neither archive supplies preassembled programs.
