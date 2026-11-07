+++
title = "A Compiler for Writing Tools"
weight = 7
description = "Begin with the completed RILL0. Copy RILL0.IR to RB01.IR and continue editing its working compiler. Use IRKEEP and ASMAKEEP for every build. Each saved compiler accepts the earlier language while gaining one capability."
download = "RILLBOOT.IR"
download_group = "tools/rillboot"
reader_names = 1
cover = true
tool_id = "RILLBOOT"
collection_key = "rb"
+++

Continue the completed RILL0 source. Add word arithmetic, masks, strings, global storage, procedures, and the file and workspace services needed to compile the RILL compiler. Every continuation remains a working compiler for its preceding subset. The seed deliberately omits XOR, left shift, unary minus, bitwise complement, explicit address-of, and unused intrinsic wrappers; RILL adds the operations needed by the later tool sources.

## What we're adding

- **Word arithmetic and masks:** Add multiplication, unsigned division/remainder, bitwise AND/OR, right shift and logical negation so compiler calculations and character tests can be expressed.
- **Strings and global storage:** Add quoted text, mutable global words, byte buffers and byte access so the compiler can retain tokens, tables and output templates.
- **Named procedures and recursion:** Add parameters and separate call frames, with sixteen parameters and sixteen live locals, so the compiler can be divided into reusable and recursive routines.
- **File and workspace services:** Add counted transfers, file publication and checked allocated blocks so the compiler can process long source files and maintain its symbol table.
- **A compiler for its successor source:** Extend the accepted RILL0 implementation only far enough to compile the RILL-written compiler and its construction checkpoints.

**Removing:** No accepted RILL0 language features are removed; every continuation retains the preceding compiler subset.

## The construction

Read the workbench first. The [source collection](../../downloads/tools/rillboot/RILLBOOT.ZIP) contains plain source and test files.
