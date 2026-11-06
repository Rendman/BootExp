+++
title = "ASM86A"
weight = 4
description = "Build a larger assembler from the verified streaming seed."
cover = true
download = "ASM86A.ASM"
download_group = "asm86a"
+++

**BOOTASM → ASM86 → ASMA0 → ASM86A → IR86 → RILL.** ASM86A begins with the completed [ASMA0 collection](../asma0/index.html). Its first executable is built by that verified streaming seed. ASM86A then assembles the same source twice and both generations must reproduce the seed-built executable.

The construction adds separately allocated symbol pages, exact-spelling bucket lookup, 8,192 symbols with names up to 31 characters, longer lines, and checked word-pair source counts. Expressions, quoted data, constants, zero-filled storage, legal 8086 memory-address combinations, frame-related instructions, and explicit conditional bridges receive their own stopping points.

Twenty-eight construction installments use the saved filenames A13.ASM through A40.ASM. The first starts from a copy of ASMA0.ASM; the existing seed routines are retained. A complete ladder exercise, a language and memory reference, and four complete programs close the collection.

Read the workbench first and preserve ASMA0.COM as the preceding builder. Preserve the completed ASM86A.COM separately as ASMAKEEP.COM. The fixed files remain SOURCE.ASM and RESULT.COM; the processor remains the 8086/8088 and output remains DOS `.COM`.

The complete source link above is ASM86A.ASM. The [ASM86A disk sources](../../downloads/asm86a/ASM86A.ZIP) include the verified seed prerequisite, all twenty-eight construction checkpoints, fixtures, helpers, and examples. The [ASMA0 disk sources](../../downloads/asma0/ASMA0.ZIP) contain the seed's own construction. Neither archive supplies preassembled programs.
