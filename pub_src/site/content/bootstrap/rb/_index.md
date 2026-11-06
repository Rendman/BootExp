+++
title = "A Compiler for Writing Tools"
weight = 7
description = "Build the RILL systems-language compiler in IR86."
cover = true
download = "RILLBOOT.IR"
download_group = "tools/rillboot"
reader_names = 1
tool_id = "RILLBOOT"
collection_key = "rb"
+++

**BOOTASM → ASM0 → ASM1 → ASM86 → IR86 → RILL0 → RILLBOOT → RILL.** RILLBOOT constructs the compiler seed used by the following RILL collection. Its implementation is processor-independent IR86. The streaming native translator and ASM86 build every checkpoint.

Forty-seven construction articles add bounded source and output blocks, complete names, explicit symbol records, word expressions, procedure arguments, recursive local state, lexical scopes, byte buffers, strings, and portable file and allocated-block services. Early checkpoints are helper diagnostics. The final source is RB47.IR, preserved as RILLBOOT.IR; its executable is RILLBOOT.COM.

Read the workbench first. The language reference and eight complete programs establish the language used to write the compiler, IR translator, and assembler in RILL. The original small RILL compiler remains a separately named milestone with its own language and limits.

The [RILLBOOT disk sources](../../downloads/tools/rillboot/RILLBOOT.ZIP) contain all seed checkpoints, acceptance and rejection inputs, complete language examples, unchanged native builders, and inspection helpers. The complete source link above is RILLBOOT.IR. No executable is supplied.

Preserve the tested compiler seed and proceed to the separate [RILL collection](../rc/index.html). Its RILL implementation must be built by this seed before it can compile itself.
