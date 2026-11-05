+++
title = "ASM86A"
weight = 3
description = "A streaming assembler with room for larger sources and native tools."
cover = true
download = "ASM86A.ASM"
download_group = "asm86a"
+++

**ASM86A is part of the bootstrap ladder: BOOTASM → ASM86 → ASM86A → IR86 → RILL.** BOOTASM supplied the BASIC foundation; ASM86 supplied a native assembler. This collection uses that unchanged ASM86 to make a streaming seed called ASMA0, then uses the seed to make the larger ASM86A. Both milestones finish by assembling themselves twice and comparing the resulting files.

The new assembler reads and writes bounded blocks rather than keeping a whole source or output image in memory. It supplies 8,192 symbols with names up to 31 characters, allocated symbol pages, longer source lines, and a larger flat `.COM` output profile. Its instruction language adds the legal 8086 memory-address combinations, stack-frame operations, quoted data, constants, zero-filled storage, and explicit bridges for distant conditional transfers. These are useful foundations for expanding IR86 and RILL; those tools still have their own limits to remove.

The construction proceeds through forty saved checkpoints. File handling, publication, the seed handoff, memory allocation, symbol records, expressions, operand descriptions, and instruction families each receive a visible stopping point. A complete ladder exercise, a reference, and four complete programs close the collection. The processor remains the 8086/8088 and the output remains DOS `.COM`.

Read the workbench first. Preserve ASMKEEP.COM as the original ASM86 and ASMA0.COM as the tested seed. The finished fixed-file assembler is preserved separately as ASMAKEEP.COM. No outside assembler, compiler, linker, or supplied executable is needed.

The complete source link above is ASM86A.ASM. The [disk source collection](../../downloads/asm86a/ASM86A.ZIP) contains the seed, construction sources, fixtures, BASIC foundation, unchanged viewer and checker, and complete programs. It contains source only.
