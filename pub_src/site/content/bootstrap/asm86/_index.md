+++
title = "Extending the 8086 Assembler"
weight = 4
description = "Build a larger assembler from the verified streaming seed."
cover = true
download = "ASM86.ASM"
download_group = "tools/asm86"
reader_names = 1
tool_id = "ASM86"
collection_key = "asm86a"
url = "/bootstrap/asm86a/"
+++

ASM1 has taught me to leave the source and the growing output on disk. That made room for more names, but the symbol table still occupies most of the program segment. I turn back to the memory sketch. The machine has more RAM than this one segment can address; using it means asking DOS for storage and keeping track of where each part belongs.

I'll build **ASM86** from the working ASM1 source. Along with a larger table, I want source that lets me write a message as words, name a count, and describe a place inside a table or a procedure's stack frame. These are forms the 8086 can use, but my assembler must learn how to read and encode them. ASM1 will build every construction checkpoint, so the implementation must stay within the language it already accepts.

**BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL.** ASM86 begins with the completed [ASM1 collection](../asma0/index.html). Its first executable is built by that verified streaming seed. ASM86 then assembles the same source twice and both generations must reproduce the seed-built executable.

## What we're adding

- **Allocated symbol storage:** Keep 8,192 definitions with names up to 31 characters, using complete-spelling lookup so larger translator and compiler sources fit.
- **Larger streamed text records:** Use 4 KiB file blocks, 1,023-character lines and checked 32-bit source counts so long sources can be processed with bounded resident buffers.
- **8086 addressing and frame operations:** Add legal base/index combinations, displacements, segment overrides and LEA so generated code can address parameters, locals and tables.
- **Data directives and expressions:** Add quoted DB text, EQU, RESB/RESW and address arithmetic so strings, constants and storage can be expressed without long numeric byte lists.
- **Arithmetic and distant conditions:** Add unsigned multiply/divide, logical shifts and explicit Jcc NEAR expansions so the backend can express word operations and reach distant labels with fixed instruction sizes.

**Removing:** No ASM1 instruction forms are removed. The output remains a single DOS .COM image with the same 61,184-byte bound.

## The construction

The construction adds separately allocated symbol pages, exact-spelling bucket lookup, 8,192 symbols with names up to 31 characters, longer lines, and checked word-pair source counts. Expressions, quoted data, constants, zero-filled storage, legal 8086 memory-address combinations, frame-related instructions, and explicit conditional bridges receive their own stopping points.

Twenty-four construction installments use A13–A33, A36, A37, and A40 as their saved source filenames. The first starts from a copy of ASM1.ASM; the existing seed routines are retained. A complete ladder exercise, a language and memory reference, and four complete programs close the collection.

Read the workbench first and preserve ASM1.COM as the preceding builder. Preserve the completed ASM86.COM separately as ASMAKEEP.COM. SOURCE.ASM and RESULT.COM remain no-argument defaults; the processor remains the 8086/8088 and output remains DOS `.COM`.

The complete source link above is ASM86.ASM. The [ASM86 disk sources](../../downloads/tools/asm86/ASM86.ZIP) include the verified seed prerequisite, all twenty-four construction checkpoints, fixtures, helpers, and examples. The [ASM1 disk sources](../../downloads/tools/asm1/ASM1.ZIP) contain the seed's own construction. Neither archive supplies preassembled programs.
