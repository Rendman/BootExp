+++
title = "ASM86"
weight = 2
description = "From the BASIC foundation to an assembler that can build itself."
cover = true
download = "ASM86.ASM"
download_group = "asm86"
+++

The BOOTASM collection supplied a working assembler in GW-BASIC. We shall use that published foundation to build **ASM86**, an assembler written in the assembly language BOOTASM accepts. Its first executable comes from the BASIC tool. Its final test is to assemble its own source, then let that copy do the same job again.

This is the assembly construction, on the same 8086/8088 and DOS workbench. It begins with a short message program. File handles, physical lines, tokens, tables, numeric values, labels, and instruction encodings each receive their own stopping point. Twenty-nine construction checkpoints lead to the thirtieth installment's self-assembly test. A language reference and three complete programs close the collection.

The accepted language stays deliberately small: byte and word data, register operations, two simple memory forms, and selected control transfers. ASM86 is neither a complete Intel assembler nor a change of processor. Its native implementation raises the output limit to 8,192 bytes and supplies a DOS success or failure status. The exact language and resource contract provide the foundation for ASMA0, the streaming seed used to build ASM86A.

Read the workbench guide first. Preserve the completed BOOTASM and use it directly to assemble every construction checkpoint. Do not replace the BASIC tool merely because the native program prints a greeting.

The complete source link above is the finished `ASM86.ASM`. The [disk source collection](../../downloads/asm86/ASM86.ZIP) contains the saved checkpoints, fixtures, BASIC foundation, viewer, batch checker, and examples, without preassembled programs.
