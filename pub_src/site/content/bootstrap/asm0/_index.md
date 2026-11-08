+++
title = "An Assembler That Builds Itself"
weight = 2
description = "From the BASIC foundation to an assembler that can build itself."
cover = true
download = "ASM0.ASM"
download_group = "tools/asm0"
reader_names = 1
tool_id = "ASM0"
collection_key = "asm86"
url = "/bootstrap/asm86/"
+++

The BOOTASM collection supplied a working assembler in GW-BASIC. We shall use that published foundation to build **ASM0**, an assembler written in the assembly language BOOTASM accepts. Its first executable comes from the BASIC tool. Its final test is to assemble its own source, then let that copy do the same job again.

## What we're adding

- **An assembler written in assembly:** BOOTASM builds a native .COM program that runs directly under DOS and can assemble its own source.
- **More source and output room:** Raise the bounds to 4,000 source lines and 8,192 emitted bytes so the native tool can handle larger construction sources.
- **OR instructions:** Extend the small arithmetic encoder with the operation used by the streaming assembler source.
- **DOS status and repeatable self-assembly:** Return success or failure to CHECK.BAT and compare two self-builds so accepted output and reproducible tool construction can be checked separately.

**Removing:** No accepted BOOTASM instruction forms are removed. BOOTASM remains the builder of the first native executable.

## The construction

This is the assembly construction, on the same 8086/8088 and DOS workbench. It begins with a short message program. File handles, physical lines, tokens, tables, numeric values, labels, and instruction encodings each receive their own stopping point. Twenty-eight construction checkpoints lead to the self-assembly test. A language reference and three complete programs close the collection.

The accepted language stays deliberately small: byte and word data, register operations, two simple memory forms, and selected control transfers. ASM0 is neither a complete Intel assembler nor a change of processor. Its native implementation raises the output limit to 8,192 bytes and supplies a DOS success or failure status. The exact language and resource contract provide the foundation for ASM1, the streaming seed used to build ASM86.

Read the workbench guide first. Preserve the completed BOOTASM and use it directly to assemble every construction checkpoint. Do not replace the BASIC tool merely because the native program prints a greeting.

The complete source link above is the finished `ASM0.ASM`. The [disk source collection](../../downloads/tools/asm0/ASM0.ZIP) contains the saved checkpoints, fixtures, BASIC foundation, viewer, batch checker, and examples, without preassembled programs.
