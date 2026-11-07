+++
title = "Our First Compiler"
weight = 6
description = "Begin with the completed ASM86 and native IR86 workbenches. Every compiler checkpoint is written in IR86. Translate SOURCE.IR with IRKEEP, copy accepted RESULT.ASM to SOURCE.ASM, then assemble with ASMAKEEP. The finished RILL0 reads SOURCE.RIL and publishes RESULT.IR."
download = "RILL0.IR"
download_group = "tools/rill0"
reader_names = 1
cover = true
tool_id = "RILL0"
collection_key = "rill"
+++

Build a small compiler in the processor-independent IR language. Its scanner, record layout, local bindings, streamed emitter, and parser are the working parts that RILLBOOT extends. The first language has one fn main(), mutable local words, + and -, unsigned comparisons, assignments, if/else, while, putc, status, exit, and return.

Read the workbench first. The [source collection](../../downloads/tools/rill0/RILL0.ZIP) contains plain source and test files.
