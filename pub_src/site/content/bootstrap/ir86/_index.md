+++
title = "IR86"
weight = 3
description = "A word-oriented intermediate language translated into assembly by a tool we can build."
cover = true
download = "IR86.ASM"
download_group = "ir86"
+++

BOOTASM supplied the BASIC foundation, and ASM86 gave us an assembler written in assembly language. This collection uses the completed ASM86 directly to build **IR86**, a translator from a small intermediate language into the assembly that ASM86 accepts.

The intermediate language describes values and operations without requiring a register choice for every computation. AX holds a word value; a small expression stack retains a left operand; named storage holds persistent state. The translator expands these operations into ordinary 8086/8088 instructions. ASM86 resolves the resulting labels and produces the DOS `.COM` file.

We begin with the source reader already constructed in ASM86. Diagnostic stops expose physical lines, tokens, and table records before translation depends on them. The construction then adds text patterns, names, values, storage, expression operations, control transfers, procedures, and the DOS interface. Each checkpoint is assembled with the completed ASM86. The final pipeline exercise copies a file using a program written in IR86.

IR86 is the intended implementation language for the initial RILL compiler. Its present contract is deliberately modest: unsigned word spelling, explicit storage and pointers, word arithmetic and bit operations, signed and unsigned comparisons, and a defined bridge to DOS. It supplies neither a complete high-level language nor automatic memory safety. Those boundaries matter when writing a program which emits IR86.

Read **The IR workbench** before entering the construction. The complete-source icon opens the finished translator's assembly source. The [disk source collection](../../downloads/ir86/IR86.ZIP) includes the saved checkpoints, tests, expected assembly text, examples, and the published bootstrap sources, without preassembled programs.
