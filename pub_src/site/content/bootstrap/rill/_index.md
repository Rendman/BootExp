+++
title = "RILL"
weight = 5
description = "From an IR-written compiler seed to a RILL toolchain that rebuilds itself."
download = "RILL.RIL"
download_group = "rill"
cover = true
+++

BOOTASM supplied the BASIC foundation, ASM86 supplied a native assembler, and IR86 supplied a processor-independent language and runtime interface. ASM86A supplies the intervening streaming assembler rung of the bootstrap ladder. RILL uses those tools to build a compiler **written in IR86**. Its output is also IR86. The existing translator and assembler turn that output into a DOS .COM program.

The language has one main function, mutable word variables, arithmetic, brace-enclosed blocks, conditions, loops, and byte input and output. Its source describes values and structured control flow. Physical registers, processor flags, and operating-system service numbers do not appear in either RILL programs or the compiler's IR source.

This first implementation deliberately has a small grammar. The compiler begins as a short IR program, gains checked text and file helpers, then acquires a scanner, a parser, and individual language features. Each stopping point has its own visible test. The complete pipeline exercise carries a RILL counter through IR and assembly to an executable.

RILL is intended to become a language in which we can rebuild the tools. This compiler is implemented in IR86; it is not a self-hosted RILL compiler. User-defined procedures, larger data structures, and a wider language belong beyond the present implementation.

Read **The RILL workbench** first. The complete-source icon opens RILL.IR. The [disk source collection](../../downloads/rill/RILL.ZIP) contains the saved IR checkpoints, test inputs, expected generated text, complete programs, and the published bootstrap sources. It contains no preassembled executable or interpreter.


## RILL builds the toolchain

The systems workbench continues through forty-seven IR-written compiler checkpoints and forty-three checkpoints expressing the compiler in RILL. Short complete programs introduce general names, word expressions, procedure arguments, recursion, scoped locals, byte buffers, literal strings, and portable file and allocated-block services.

The complete source link above is **RILL.RIL**, the self-compiling compiler. **IR86.RIL** and **ASM86A.RIL** implement the translator and assembler in the same language. The complete exercise builds all three from the IR-written seed, then lets the RILL-written compiler, translator, and assembler rebuild all three twice. Every corresponding executable must match.

The [complete toolchain source collection](../../downloads/toolchain/TOOLCHN.ZIP) includes the native bridge, IR-written seed, RILL implementations, every saved stopping point, exact input/rejection fixtures, examples, and TMAKE.BAT. It contains no preassembled programs. The earlier RILL.ZIP is the first compiler construction with its own deliberately smaller language; keep its builders separately named.
