+++
title = "ASMA0"
weight = 3
description = "A streaming seed built by ASM86 and proved by self-assembly."
cover = true
download = "ASMA0.ASM"
download_group = "asma0"
+++

**BOOTASM → ASM86 → ASMA0 → ASM86A → IR86 → RILL.** ASMA0 is the streaming seed in this bootstrap ladder. The completed ASM86 builds its first executable directly; the seed then assembles its own source twice and reproduces that executable.

This collection constructs a tool that can handle a source and output larger than its own resident image. Fixed disk names, bounded input and output blocks, two passes, temporary-file ownership, and recoverable publication each receive a separate stopping point. The completed seed has 2,048 symbols in its original segment and the segment-access forms needed to build ASM86A.

Twelve construction checkpoints finish at ASMA0.ASM. A workbench guide, a seed language and memory reference, and three complete programs accompany them. The language remains small enough to be implemented within the preceding ASM86's bounds. The processor remains the 8086/8088 and the output remains DOS `.COM`.

Read the workbench first and preserve ASMKEEP.COM as the original prompted assembler. After the self-assembly comparisons, preserve ASMA0.COM and its source. That verified source is the starting file of the separate [ASM86A collection](../asm86a/index.html), which adds allocated symbol pages and a broader language.

The complete source link above is ASMA0.ASM. The [ASMA0 disk sources](../../downloads/asma0/ASMA0.ZIP) include all twelve checkpoints, acceptance and rejection inputs, the unchanged BASIC foundation and ASM86 source, the viewer and checker, and complete programs. No preassembled executable is included.
