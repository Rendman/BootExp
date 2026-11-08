+++
title = "Building a Streaming Assembler"
weight = 3
description = "A streaming seed built by ASM0 and proved by self-assembly."
cover = true
download = "ASM1.ASM"
download_group = "tools/asm1"
reader_names = 1
tool_id = "ASM1"
collection_key = "asma0"
url = "/bootstrap/asma0/"
+++

**BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL.** ASM1 is the streaming seed in this bootstrap ladder. The completed ASM0 builds its first executable directly; the seed then assembles its own source twice and reproduces that executable.

## What we're adding

- **Streamed input and output:** Work through 1 KiB blocks so source and executable size are independent of the resident file buffers.
- **Larger assembly capacity:** Retain 2,048 symbols and emit as many as 61,184 bytes so the seed can build a substantially larger assembler.
- **XOR and segment access:** Add segment-register MOV and ES overrides on the existing MOV memory forms so the assembler can work with separately allocated storage.
- **Checked publication:** Write a temporary file and use backup/recovery names so rejected source does not replace an accepted RESULT.COM.

**Removing:** The complete-image output buffer; streaming removes the resident output-size bottleneck. The fixed SOURCE.ASM/RESULT.COM names are retained from ASM0. ES, CS, SS and DS also become reserved names so labels cannot be confused with the new segment-register operands.

## The construction

This collection constructs a tool that can handle a source and output larger than its own resident image. Fixed disk names, bounded input and output blocks, two passes, temporary-file ownership, and recoverable publication each receive a separate stopping point. The completed seed has 2,048 symbols in its original segment and the segment-access forms needed to build ASM86.

Twelve construction checkpoints finish at ASM1.ASM. A workbench guide, a seed language and memory reference, and three complete programs accompany them. The language remains small enough to be implemented within the preceding ASM0's bounds. The processor remains the 8086/8088 and the output remains DOS `.COM`.

Read the workbench first and preserve ASMKEEP.COM as the original fixed-file assembler. After the self-assembly comparisons, preserve ASM1.COM and its source. That verified source is the starting file of the separate [ASM86 collection](../asm86a/index.html), which adds allocated symbol pages and a broader language.

The complete source link above is ASM1.ASM. The [ASM1 disk sources](../../downloads/tools/asm1/ASM1.ZIP) include all twelve checkpoints, acceptance and rejection inputs, the unchanged BASIC foundation and ASM0 source, the viewer and checker, and complete programs. No preassembled executable is included.
