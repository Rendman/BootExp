+++
title = "Building an Intermediate Language"
weight = 5
description = "ASM86 builds every saved source in this collection. Supply the translator input and output names after its program name; SOURCE.IR and RESULT.ASM remain the no-argument defaults. Preserve the completed translator as IRKEEP.COM; make the identical IWKEEP.COM copy used by later workbenches."
download = "IR86.ASM"
download_group = "tools/ir86"
reader_names = 1
cover = true
tool_id = "IR86"
collection_key = "ir86"
+++

This collection builds one native translator from a bounded reader through procedure frames, strings, file streams, and allocated workspace. The first small translator grows into the translator that builds the compiler. ASM86 assembles every stage.

## What we're adding

- **A processor-independent instruction language:** Define word values, a virtual accumulator and an expression stack so compilers can describe computations without naming physical registers.
- **Declared storage and byte addresses:** Supply words, byte buffers, strings and indirect access so generated programs can keep and manipulate their own data.
- **Procedure frames:** Name parameters and local slots, with up to sixteen parameters and sixty-four locals, so nested and recursive calls keep their state separate.
- **Portable startup arguments:** Supply argument counts and ordinary string pointers so file tools can obtain names from the native binding.
- **Portable service handles:** Provide counted file transfers, persistent status and checked allocated blocks so programs can process files and larger workspaces without exposing DOS descriptors or segments.
- **A separate 8086/DOS binding:** Emit assembly through bounded streams so the native implementation can build the compiler while keeping processor details outside the IR operations.

**Removing:** No earlier IR operation forms are removed. PROC and RETURN add explicit call frames while LABEL remains available for branch destinations and the early flat programs.

## The construction

The language defines word values, a virtual accumulator, an expression stack, byte addresses, and opaque service handles. The 8086 instructions appear in the backend templates and DOS binding; they are not part of the IR program interface.

Read the workbench first. The [source collection](../../downloads/tools/ir86/IR86.ZIP) contains plain source and test files.
