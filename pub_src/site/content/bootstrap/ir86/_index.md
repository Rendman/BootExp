+++
title = "IR86"
weight = 4
description = "A processor-independent language with defined word operations and a portable runtime interface."
download = "IR86.RIL"
cover = true
download_group = "ir86"
+++

BOOTASM supplied the BASIC foundation, and ASM86 gave us an assembler written in assembly language. ASM86A adds the streaming assembler rung between ASM86 and IR86. IR86 adds a processor-independent intermediate language. This collection builds its first translator and backend in the assembly accepted by the completed ASM86.

The language describes a virtual accumulator A, fixed-width values, an expression stack, declared storage, comparisons, and procedures. Its meaning does not depend on a physical register, instruction flag, segment, or operating-system interrupt. A backend chooses how to implement those operations. The backend constructed here produces 8086/8088 assembly; ASM86 resolves its labels and makes a DOS .COM file.

Input and output use a separate runtime contract. GETC and PUTC transfer bytes; OPEN, CREATE, READ, WRITE, and CLOSE use opaque handles; STATUS returns an ordinary success or failure value. The DOS binding supplies these services for our current workbench. The same IR source can be implemented by another backend and environment binding.

Construction begins with the published ASM86 source reader. Diagnostic stops expose lines, tokens, and lookup records before translation depends on them. Small additions build the word operations, storage, control flow, procedures, and runtime services. Every native checkpoint is assembled directly by the completed ASM86. The final pipeline exercise translates and runs a complete file copier.

IR86 is the implementation language for the initial RILL compiler. Its fixed sixteen-bit values are a property of this virtual machine, not a request for a sixteen-bit CPU. Another processor must preserve those semantics, even if it uses different registers, wider instructions, or several instructions per operation.

Read **The IR workbench** first. The complete-source icon opens the translator. The [disk source collection](../../downloads/ir86/IR86.ZIP) contains the saved checkpoints, tests, expected assembly, runtime source, complete examples, and published bootstrap sources without preassembled programs.


## The streaming and RILL constructions

The streaming workbench continues with twenty-three native checkpoints, IW01 through IW23, built by the published ASM86A. They remove the whole-assembly buffer, introduce procedure frames and checked allocated blocks, and preserve the processor-independent contract. The native bridge is IRWIDE.ASM. Its fixed interface is SOURCE.IR → RESULT.ASM.

The complete source link above is **IR86.RIL**, the translator written in RILL with its native backend kept explicit. The RILL toolchain exercise rebuilds it and both other tools twice with matching executable bytes. The [complete toolchain source collection](../../downloads/toolchain/TOOLCHN.ZIP) includes every streaming checkpoint, compiler seed, RILL tool source, helper, and fixture. The earlier IR86.ZIP belongs to the first native construction and retains its own source-name interface.
