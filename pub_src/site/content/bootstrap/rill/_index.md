+++
title = "A Compiler Written in Its Own Language"
weight = 8
description = "Write the RILL compiler in RILL and prove matching rebuilds."
cover = true
download = "RILL.RIL"
download_group = "tools/rill"
reader_names = 1
tool_id = "RILL"
collection_key = "rc"
url = "/bootstrap/rc/"
+++

**BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL.** Begin with the completed RILLBOOT compiler seed, RILLBOOT.COM, and the preserved native IWKEEP and ASMAKEEP. RILL expresses the compiler in the RILL language accepted by that seed.

## What we're adding

- **The compiler written in RILL:** Express the scanner, tables, emitter and parser in the language accepted by RILLBOOT so the compiler implementation can be maintained with its own language.
- **Additional word and pointer operations:** Add XOR, left shift, unary minus, complement, address-of and ordinary word loads/stores so the translator and assembler implementations can express their data and encoding operations.
- **More local storage:** Build sixty-four live local slots and eighty active parameter/local name records into the storage and procedure lessons, keeping sixteen parameters, so larger functions fit the existing IR frame contract.
- **Matching compiler generations:** Establish the compiler using its own frame convention, then compare two further self-builds so the completed source reproduces its executable.

**Removing:** No accepted RILLBOOT language features are removed. The native stack guard still bounds active calls even though each emitted procedure reserves a larger local frame.

## The construction

Forty-three construction articles build the compiler one helper at a time. Each early diagnostic has its own visible test. Names, symbol records, streamed text, expression parsing, lexical scopes, procedure arguments, and complete functions become ordinary RILL procedures. The record-storage, local-declaration and procedure lessons establish sixty-four local slots and sixteen parameters. RC43.RIL is the completed compiler, saved as RILL.RIL.

The reference describes the complete RILL language. RILLBOOT accepts the smaller subset used to write this compiler; the RILL implementation also accepts XOR, left shift, unary minus, bitwise complement, addresses, and ordinary word-pointer loads and stores. Complete programs exercise the RILL-written compiler. The self-build exercise first establishes the compiler using its own sixty-four-slot frame convention, then compares two further generations against that executable. The following [Rebuilding Our Tools in RILL](../toolchain/index.html) collection uses that tested compiler to construct IR86 and ASM86 in RILL and rebuild the complete trio twice.

The [RILL disk sources](../../downloads/tools/rill/RILL.ZIP) include every compiler checkpoint, its fixtures, the compiler seed and native prerequisites, and three complete examples. The separate [toolchain source collection](../../downloads/tools/toolchain/TOOLCHN.ZIP) includes the IR86 and ASM86 replacements and TMAKE.BAT. Both archives contain source only.

Read the workbench first. Keep the IR-written seed, native translator, and native assembler separately named throughout the self-builds.
