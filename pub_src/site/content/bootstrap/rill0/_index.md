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
url = "/bootstrap/rill/"
+++

Build a small compiler in the processor-independent IR language. Its scanner, record layout, local bindings, streamed emitter, and parser are the working parts that RILLBOOT extends. The first language has one fn main(), mutable local words, + and -, unsigned comparisons, assignments, if/else, while, putc, status, exit, and return.

## What we're adding

- **Structured source translated into IR:** Add a scanner and parser so expressions, assignments and control statements can be written directly instead of spelling out each IR operation.
- **Local names and lexical scopes:** Provide up to sixteen live local words, with slots reused at closing braces, so blocks can keep temporary state without permanent global scratch cells.
- **Expressions and branches:** Compile addition, subtraction, unsigned comparisons, if/else and while so the first language can express useful decisions and repeated work.
- **A continuing compiler implementation:** Establish the symbol records, bounded streams, parser and publication routines that RILLBOOT extends, keeping this first compiler a required working foundation.

**Removing:** None. IR86 remains the compiler output language, and the first RILL language stays small enough to construct gradually.

## The construction

Read the workbench first. The [source collection](../../downloads/tools/rill0/RILL0.ZIP) contains plain source and test files.
