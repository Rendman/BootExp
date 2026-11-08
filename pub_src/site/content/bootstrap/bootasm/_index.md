+++
title = "Our First Assembler"
weight = 1
description = "An 8088 assembler you can type in GW-BASIC."
cover = true
download = "BOOTASM.BAS"
download_group = "tools/bootasm"
reader_names = 1
tool_id = "BOOTASM"
collection_key = "bootasm"
+++

The processor does not read `MOV DL,42H`. It reads bytes. An assembler is the program which performs that translation, and a small one is within reach of a BASIC programmer.

## What we're adding

- **Named instructions and data:** Translate a small assembly vocabulary into bytes so programs can be entered and understood without calculating every opcode by hand.
- **Labels and two passes:** Resolve named addresses, including forward references, so inserting code does not require renumbering every branch destination.
- **Fixed work files and a BASIC implementation:** Read SOURCE.ASM and write RESULT.COM directly. Use the interpreter already on the workbench to create the first assembler without an outside assembler or compiler.
- **DOS program files and byte inspection:** Write runnable .COM files and inspect their contents so every small addition has a concrete result to check.

**Removing:** None; this collection establishes the first assembler.

## The construction

This collection builds BOOTASM from its first disk byte to a two-pass assembler with named addresses, a modest instruction vocabulary, and DOS `.COM` output. It is the first tool in the Bootstrap Experiment and the BASIC foundation for the assembly-language collection, ASM0.

Begin with **The workbench**, then follow the eighteen numbered installments in order. The first writes and inspects one byte. Each subsequent installment adds one small capability and provides a saved stopping point.

## The finished tool

BOOTASM accepts `DB` and `DW`, decimal and hexadecimal values, labels, and a selected set of 8086/8088 instructions. It understands the eight ordinary word registers and eight byte registers, direct memory offsets and `[BX]`, near calls and jumps, and six short conditional branches. The reference at the end lists every accepted form.

It is intentionally small: 4,096 output bytes, 256 labels, and 2,000 source lines, each at most 120 characters. It does not include macros, expression arithmetic, segment directives, object modules, or every addressing form of the processor. Those omissions keep the listing and the work of typing it manageable. They are limits of BOOTASM, not limits of the 8088.

## Keep the stopping points

Each installment tells you which existing lines to replace and where to insert new ones. Save the named checkpoint before testing it. The final working copy is `BOOTASM.BAS`; preserve it under `BOOTKEEP.BAS` as well. BOOTASM is interpreted BASIC, so its bootstrap copy is a BASIC source file rather than a compiler-made executable.

Every required program is printed in the collection, including the viewer, status checker, and complete examples. Keep those small helpers beside the saved checkpoint files.
