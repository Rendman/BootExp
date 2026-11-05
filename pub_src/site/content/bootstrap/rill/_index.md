+++
title = "RILL"
weight = 5
description = "A small structured language, compiled by a program written in IR86."
download = "RILL.IR"
download_group = "rill"
cover = true
+++

BOOTASM supplied the BASIC foundation, ASM86 supplied a native assembler, and IR86 supplied a processor-independent language and runtime interface. ASM86A supplies the intervening streaming assembler rung of the bootstrap ladder. RILL uses those tools to build a compiler **written in IR86**. Its output is also IR86. The existing translator and assembler turn that output into a DOS .COM program.

The language has one main function, mutable word variables, arithmetic, brace-enclosed blocks, conditions, loops, and byte input and output. Its source describes values and structured control flow. Physical registers, processor flags, and operating-system service numbers do not appear in either RILL programs or the compiler's IR source.

This first implementation deliberately has a small grammar. The compiler begins as a short IR program, gains checked text and file helpers, then acquires a scanner, a parser, and individual language features. Each stopping point has its own visible test. The complete pipeline exercise carries a RILL counter through IR and assembly to an executable.

RILL is intended to become a language in which we can rebuild the tools. This compiler is implemented in IR86; it is not a self-hosted RILL compiler. User-defined procedures, larger data structures, and a wider language belong beyond the present implementation.

Read **The RILL workbench** first. The complete-source icon opens RILL.IR. The [disk source collection](../../downloads/rill/RILL.ZIP) contains the saved IR checkpoints, test inputs, expected generated text, complete programs, and the published bootstrap sources. It contains no preassembled executable or interpreter.
